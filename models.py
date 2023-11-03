from config import config

import os
import json
import openai
import requests
from langchain.agents import (
    load_tools,
    initialize_agent,
    AgentType
)
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.tools.render import render_text_description
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.agents.format_scratchpad import format_log_to_str
from langchain import hub
from langchain.agents import AgentExecutor


openai.api_key = config.openai_api_key
claimbuster_api_key = config.claimbuster_api_key
os.environ["OPENAI_API_KEY"] = config.openai_api_key
os.environ["SERPAPI_API_KEY"] = config.serpapi_api_key


def is_claim(input_text: str) -> list:
    request_headers = {"x-api-key": claimbuster_api_key}
    response = requests.get(url=f"https://idir.uta.edu/claimbuster/api/v2/score/text/sentences/{input_text}", headers=request_headers).json()
    
    labels = [1 if result["score"]>0.52 else 0 for result in response["results"]]

    return labels


def get_claim_verification(row):
    if row['claim_label'] == 0:
        return 'na', 'na'
    
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    tools = load_tools(["serpapi", "llm-math"], llm=llm)

    prompt = hub.pull("hwchase17/react")
    prompt = prompt.partial(
    tools=render_text_description(tools),
    tool_names=", ".join([t.name for t in tools]),
    )

    llm_with_stop = llm.bind(stop=["\nObservation"])

    agent = (
        {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
        }
        | prompt
        | llm_with_stop
        | ReActSingleInputOutputParser()
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True)

    executor_prompt = """You are a claim verification agent. Below I have provided you with a sentence that has one or more than more claim. Your job is to carefully analyze whatever claims are made in the sentence and verify them for correctness and provide the output as json in following format:-
{
   "answer": "yes/no",
   "rationale": reason to accept or deny claim
}

Claim: """ + row['sentences']
    
    response = agent_executor.invoke(
        {
        "input": executor_prompt
        }
    )

    print(response['output'])
    response_output = json.loads(response['output'])
    
    return response_output['answer'], response_output['rationale']




    



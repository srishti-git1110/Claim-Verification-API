import pandas as pd
from typing import Optional
from fastapi import FastAPI
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse

from models import (
    is_claim,
    get_claim_verification
)
from evaluate import evaluate_claim_detection

app = FastAPI()

def create_dataframe(input_text, labels):
    sentences = input_text.split('.')
    df = pd.DataFrame({'sentences': sentences,
                       'claim_label': labels})
    
    return df


@app.post("/process_text")
async def process_text(
    input_text: str,
    target_df: Optional[pd.DataFrame] = None
):
    labels = is_claim(input_text=input_text)
    df = create_dataframe(input_text, labels)

    df[['is_claim_correct', 'Additional info']] = df.apply(get_claim_verification).apply(pd.Series)
    print(df)

    if target_df is not None:
        print('Evaluating claim detection...')

        acc, f1, prec, rec = evaluate_claim_detection(
            target=target_df['claim_label'].tolist(),
            predicted=df['claim_label'].tolist()
            )
        
        print(f'Accuracy={acc}, F1-score={f1}, Precision={prec}, Recall={rec}')


        print()
        print('Evaluating claim verification...')
        temp = df[df['is_claim_correct']!='na']
        temp['is_claim_correct'] = temp['is_claim_correct'].replace({'yes': 1, 'no': 0})

        acc, f1, prec, rec = evaluate_claim_detection(
            target=target_df[target_df['is_claim_correct']!='na']['is_claim_correct'].tolist(),
            predicted=temp['is_claim_correct'].tolist()
            )
        
        print(f'Accuracy={acc}, F1-score={f1}, Precision={prec}, Recall={rec}')
    
    return df

    



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
                       'labels': labels})
    
    return df


@app.post("/process_text")
async def process_text(
    input_text: str,
    target_df: Optional[pd.DataFrame] = None
):
    labels = is_claim(input_text=input_text)
    df = create_dataframe(input_text, labels)

    if target_df is not None:
        acc, f1, prec, rec = evaluate_claim_detection(
            target_df,
            df
        )
        print(f'Accuracy of claim detection model = {acc}')
        print(f'F1 score of claim detection model = {f1}')
        print(f'Precision of claim detection model = {prec}')
        print(f'Recall of claim detection model = {rec}')

    else:
        print('''Cannot evaluate the claim detection process. 
              Please provide a target dataframe having atleast one column called labels;
              labels contains the ground truth of whether the sentences in the input text are claims or not.''')

    claim_df = df[df['labels'] == 1]
    claim_df.drop(columns=['labels'], inplace=True)
    claim_df.reset_index(drop=True)
    claim_df.rename(columns={'sentences': 'claims'},
                    inplace=True
                    )

    claim_df[['is_claim_correct', 'Additional info']] = claim_df['claims'].apply(get_claim_verification).apply(pd.Series)
    print(claim_df)
    return claim_df

    



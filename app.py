import pandas as pd
from typing import Optional
from fastapi import FastAPI, UploadFile, File
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
    file: Optional[UploadFile] = File(None)
):
    labels = is_claim(input_text=input_text)
    df = create_dataframe(input_text, labels)

    df[['is_claim_correct', 'Additional info']] = df.apply(get_claim_verification).apply(pd.Series)
    print(df)


    if file is not None:
        target_df = pd.read_csv(file.file)
        print('Evaluating claim detection...')

        acc, f1, prec, rec = evaluate_claim_detection(
            target=target_df['claim_label'].astype(int).tolist(),
            predicted=df['claim_label'].astype(int).tolist()
            )
        
        print(f'Accuracy={acc}, F1-score={f1}, Precision={prec}, Recall={rec}')


        print()
        print('Evaluating claim verification...')
        temp = df[df['is_claim_correct']!='na']
        temp['is_claim_correct'] = temp['is_claim_correct'].replace({'yes': 1, 'no': 0})

        acc, f1, prec, rec = evaluate_claim_detection(
            target=target_df[target_df['is_claim_correct']!='na']['is_claim_correct'].astype(int).tolist(),
            predicted=temp['is_claim_correct'].tolist()
            )
        
        print(f'Accuracy={acc}, F1-score={f1}, Precision={prec}, Recall={rec}')
    
    return df

    



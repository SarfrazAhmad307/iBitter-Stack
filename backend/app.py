from fastapi import FastAPI, UploadFile, File
from predictor import final_prediction
from pydantic import BaseModel
import pandas as pd

app = FastAPI()


class SequenceInput(BaseModel):
    sequence: str


@app.post("/predict/single")
def predict_single(data: SequenceInput):
    return final_prediction(data.sequence)


@app.post("/predict/batch")
def predict_batch(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    if "sequence" not in df.columns:
        return {"error": "CSV must contain a 'sequence' column."}

    results = []
    for seq in df["sequence"]:
        result = final_prediction(seq)
        result["sequence"] = seq
        results.append(result)

    return results

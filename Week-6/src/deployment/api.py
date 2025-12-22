import uuid
import json
import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime
import os



app = FastAPI(title="ML Prediction API", version="1.0")

MODEL_PATH = "src/models/best_model.pkl"
FEATURES_PATH = "src/features/feature_list.json"
LOG_PATH = "src/logs/prediction_logs.csv"
 
model = joblib.load(MODEL_PATH)
 
with open(FEATURES_PATH) as f:
    FEATURE_COLUMNS = json.load(f)


class PredictionRequest(BaseModel):
    Quantity: int = Field(..., example=6)
    UnitPrice: float = Field(..., example=2.55)
    Country: str = Field(..., example="United Kingdom")
    Description: str = Field(..., example="WHITE HANGING HEART T-LIGHT HOLDER")
    InvoiceDate: str = Field(..., example="2010-12-01 08:26")


def transform_input(payload: dict) -> np.ndarray:
    df = pd.DataFrame([payload])

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["InvoiceYear"] = df["InvoiceDate"].dt.year
    df["InvoiceMonth"] = df["InvoiceDate"].dt.month
    df["InvoiceDay"] = df["InvoiceDate"].dt.day
    df["InvoiceHour"] = df["InvoiceDate"].dt.hour
    df["InvoiceWeekday"] = df["InvoiceDate"].dt.weekday

    df["LogUnitPrice"] = np.log1p(df["UnitPrice"])
    df["UnitPriceSquared"] = df["UnitPrice"] ** 2
    df["DescriptionLength"] = df["Description"].astype(str).apply(len)

    df.drop(columns=["InvoiceDate", "Description"], inplace=True)

    df = pd.get_dummies(df, columns=["Country"])

    df = df.reindex(columns=FEATURE_COLUMNS, fill_value=0)
 
    return df.values


def log_prediction(request_id, payload, prediction, probability):
    log_row = {
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": request_id,
        "prediction": prediction,
        "probability": probability,
        **payload
    }
 
    df_log = pd.DataFrame([log_row])
 
    if not os.path.exists(LOG_PATH):
        df_log.to_csv(LOG_PATH, index=False)
    else:
        df_log.to_csv(LOG_PATH, mode="a", header=False, index=False)


@app.get("/")
def health():
    return {"status": "API is running"}


@app.post("/predict")
def predict(request: PredictionRequest):
    request_id = str(uuid.uuid4())

    payload = request.dict()
    X = transform_input(payload)

    proba = model.predict_proba(X)[0][1]
    probability = float(proba)
    prediction = int(probability >= 0.3)

    log_prediction(request_id, payload, prediction, probability)

    return {
        "request_id": request_id,
        "prediction": prediction,
        "probability": probability
    }

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": True}

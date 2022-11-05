from typing import List, Optional
# from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks, Response
from fastapi_cache.decorator import cache
from joblib import load
import numpy as np
import mlflow
from mlflow.tracking import MlflowClient
import pandas as pd
from sqlalchemy import text
from sklearn.preprocessing import LabelEncoder
import datetime

from app.base.config import settings
from app.base.db import SessionLocal, engine

from . import actions, models, schemas


router = APIRouter()
mlflowclient = MlflowClient()
mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
mlflow.set_registry_uri(settings.MLFLOW_TRACKING_URI)


@router.get("/")
async def root():
    return "Store & Product Quantity Prediction"
    
@router.get("/get_feature_list")
async def get_all_tables():

    query = """
    SELECT COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'podfoods' 
    AND TABLE_NAME = 'features'
    AND COLUMN_NAME not in ('id', 'created_at')
    """

    db = SessionLocal()
    res = db.execute(text(query)).fetchall()
    column_list = [col[0] for col in res]

    return {"table_list": column_list}

@router.post("/predict")
async def predict(request: schemas.QuantityPredictionRequest):
    model_name = "PF_Quantity_Prediction"
    # Fetch the last model in production
    model = mlflow.sklearn.load_model(
        model_uri=f"models:/{model_name}/latest"
    )
    pairs = [f"{pair.store_id}_{pair.product_id}" for pair in request.input]

    query = f"""
    select * from features
    where concat(store_id, '_', product_id) in ('f"{"','".join(pairs)}"')
    """

    features = pd.read_sql(query, engine)

    if len(features) == 0:
        return {"prediction_output":[]}
        
    res = features[['store_id', 'product_id', 'checkout_date']].copy(deep=True)
    # print(features.info())
    features.drop(['id','created_at', 'quantity', 'checkout_date'], axis=1, inplace=True)
    
    res['checkout_date'] = pd.to_datetime(res['checkout_date'], format="%Y-%m-%d")

    today = datetime.datetime.today()
    lb = LabelEncoder()
    features['store_type'] = lb.fit_transform(features['store_type'])
    features['cate'] = lb.fit_transform(features['cate'])
    features['sub_cate'] = lb.fit_transform(features['sub_cate'])

    res['quantity_pred'] = np.ceil(model.predict(features.astype(np.float32)))
    res['checkout_date_pred'] = res['checkout_date'].dt.year.astype(str) + str(today.month).zfill(2) + res['checkout_date'].dt.day.astype(str).str.zfill(2)

    res = res[pd.to_datetime(res['checkout_date_pred'], format="%Y%m%d") >= today]
    res.drop(columns=['checkout_date'], inplace=True)

    print(res.to_dict('records'))
    return schemas.QuantityPredictionReponse(
        prediction_output=res.to_dict('records'),
    )

from typing import  Optional, List
from typing_extensions import TypedDict
from pydantic import BaseModel, Field

class QuantityPredictionObject(BaseModel):
    store_id: int = Field(..., description="id of store")
    product_id: int = Field(..., description="id of product")

class QuantityPredictionOutputObject(BaseModel):
    store_id: int = Field(..., description="id of store")
    product_id: int = Field(..., description="id of product")
    quantity_pred: int = Field(..., description="predicted quantity on a given day in the next 30 days")
    checkout_date_pred: str = Field(..., description="check out date in the next 30 days")

class QuantityPredictionRequest(BaseModel):
    input: List[QuantityPredictionObject]
    date: str = None

class QuantityPredictionReponse(BaseModel):
    prediction_output: List[QuantityPredictionOutputObject]
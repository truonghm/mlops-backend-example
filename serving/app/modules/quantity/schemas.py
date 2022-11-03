from typing import  Optional, List
from typing_extensions import TypedDict
from pydantic import BaseModel, Field

class QuantityPredictionObject(BaseModel):
    store_id: int
    product_id: int


class QuantityPredictionRequest(BaseModel):
    input: List[QuantityPredictionObject]
    date: str = None

class QuantityPredictionReponse(BaseModel):
    predictions: List[float]
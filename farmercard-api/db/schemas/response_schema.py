
from pydantic import BaseModel,Field,validator
from typing import Any
from bson.objectid import ObjectId



class ResponseModel(BaseModel):
    data: Any
    code: int
    message: str

    class Config:
        json_encoders = {
            ObjectId: str
        }

class ErrorResponseModel(BaseModel):
    error: str
    code: int
    message: str

    class Config:
        json_encoders = {
            ObjectId: str
        }
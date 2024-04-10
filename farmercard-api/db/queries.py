from typing import List, Optional
from bson import ObjectId
import logging
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from .models import (
    FarmerSchema,
    FarmingDetails,
    Vaccination,
    ResponseModel,
    ErrorResponseModel
)

from .database import get_farmer_collection

# def farmer_helper(farmer) -> dict:
#     return {
#         "id": str(farmer["_id"]),
#         "f_uuid": farmer["f_uuid"],
#         "PhoneNumber": farmer["PhoneNumber"],
#         "farmer_Card": farmer["farmer_Card"],
#     }


def create_farmer(db, farmer: FarmerSchema) -> ResponseModel:
    try:
        result = db.insert_one(farmer.model_dump())
        return ResponseModel(data=str(result.inserted_id), code=201, message="Farmer created successfully")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error creating farmer")





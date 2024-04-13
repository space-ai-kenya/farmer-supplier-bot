from typing import List, Optional
from bson import ObjectId
import logging
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from db.schemas.farm_card_schema import (
    FarmingDetails,
    LandAndSoilInformation,
)
from db.schemas.response_schema import (
    ResponseModel,
    ErrorResponseModel
)

def get_farming_details(db, f_uuid: str):
    try:
        farmer = db.find_one({"f_uuid": f_uuid})
        if farmer:
            farming_details = farmer["farmer_Card"]["farmingDetails"]
            return ResponseModel(data=farming_details, code=200, message="Farming details retrieved successfully")
        else:
            return ResponseModel(data=None, code=404, message="Farmer not found")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error retrieving farming details")
    

def update_farming_details(db, f_uuid: str, farming_details: FarmingDetails):
    try:
        result = db.update_one({"f_uuid": f_uuid}, {"$set": {"farmer_Card.farmingDetails": farming_details.model_dump()}})
        if result.modified_count > 0:
            return ResponseModel(data=None, code=200, message="Farming details updated successfully")
        else:
            return ResponseModel(data=None, code=404, message="Farmer not found")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error updating farming details")
    

def get_land_and_soil_information(db, f_uuid: str):
    try:
        farmer = db.find_one({"f_uuid": f_uuid})
        if farmer:
            land_and_soil_info = farmer["farmer_Card"]["landAndSoilInformation"]
            return ResponseModel(data=land_and_soil_info, code=200, message="Land and soil information retrieved successfully")
        else:
            return ResponseModel(data=None, code=404, message="Farmer not found")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error retrieving land and soil information")
    

def update_land_and_soil_information(db, f_uuid: str, land_and_soil_info: LandAndSoilInformation):
    try:
        result = db.update_one({"f_uuid": f_uuid}, {"$set": {"farmer_Card.landAndSoilInformation": land_and_soil_info.model_dump()}})
        if result.modified_count > 0:
            return ResponseModel(data=None, code=200, message="Land and soil information updated successfully")
        else:
            return ResponseModel(data=None, code=404, message="Farmer not found")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error updating land and soil information")
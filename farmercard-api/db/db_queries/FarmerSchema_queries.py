from typing import List, Optional
from bson import ObjectId
import logging
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from db.schemas.farm_card_schema import (
    FarmerSchema 
)
from db.schemas.cow_card_schema import (
    CowCard,

)

from db.schemas.response_schema import (
    ResponseModel,
    ErrorResponseModel
)



from fastapi.encoders import jsonable_encoder
import json
# ---------------- farmer

def create_farmer(db, f_uuid: str, phone_number: str, farming_type: str):
    """
    Types of Farming/Farmer:
    ["Dairy Farmer", "Subsistence Farming", "Commercial Farming"]
    """
    try:

        # check first if farmer exisits
        farmer = db.find_one({"f_uuid": f_uuid,"PhoneNumber":phone_number})
        if farmer:
            return ErrorResponseModel(error="Farmer already in database", code=403, message="Farmer already exists")
        else:
            farming_types = ["Dairy Farmer", "Subsistence Farming", "Commercial Farming"]
            # Define the farmer data with empty sections
            f_data = {
                "f_uuid": f_uuid,
                "PhoneNumber": phone_number,
                "farmer_Card": {
                    "typeOfFarming": farming_type,
                    "farmSize": "",
                    "livestockDetails": {
                        "cow_card": [],
                        "animal_inventory": []
                    },
                    "crop_card": []
                }
            }
            if farming_type == "Dairy Farmer":
                # Add dairy-specific fields
                f_data["farmer_Card"].pop("crop_card")
            else:
                if farming_type not in farming_types:
                    return ErrorResponseModel(error="Unknown farming type", code=400, message="Invalid farming type")
            # # Insert the farmer data into the database
            result = db.insert_one(f_data)
            return ResponseModel(data=str(result.inserted_id), code=201, message="Farmer created successfully")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error creating farmer")

def retrieve_all_farmers(db, skip: int = 0, limit: int = 10):
    try:
        farmers = list(db.find({}, skip=skip, limit=limit))
        # logging.info(farmers)
        return ResponseModel(data=farmers, code=200, message="Farmers retrieved successfully")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error retrieving farmers")

def get_farmer(db,f_uuid: str):
    try:
        farmer = db.find_one({"f_uuid": f_uuid})
        if farmer:
            return ResponseModel(data=json.dumps(farmer), code=200, message="Farmer found")
        else:
            return ResponseModel(data=None, code=404, message="Farmer not found")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error retrieving farmer")







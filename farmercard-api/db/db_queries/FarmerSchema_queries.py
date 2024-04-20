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

def create_farmer(db, f_uuid: str,farm_name_id:str, phone_number: str, farming_type: str):
    """
    Types of Farming/Farmer:
    ["Dairy Farmer", "Subsistence Farming", "Commercial Farming"]
    """
    try:
        # Check if farmer exists
        farmer = db.find_one({"f_uuid": f_uuid, "PhoneNumber": phone_number})
        if farmer:
            return ErrorResponseModel(error="Farmer already in database", code=403, message="Farmer already exists")

        farming_types = ["Dairy Farmer", "Subsistence Farming", "Commercial Farming"]
        if farming_type not in farming_types:
            return ErrorResponseModel(error="Unknown farming type", code=400, message="Invalid farming type")

        # Define the farmer data
        f_data = {
            "f_uuid": f_uuid,
            "PhoneNumber": phone_number,
            "FarmingType": farming_type,
            "farm_cards": [
                {
                    "farm_name_id": f"farm_{farm_name_id}",
                    "farmSize": "",
                    "livestockDetails": {
                        "cow_card": [],
                        "animal_inventory": []
                    },
                    # "crop_card": []
                }
            ]
        }

        # Insert the farmer data into the database
        result = db.insert_one(f_data)
        return ResponseModel(data=str(result.inserted_id), code=201, message="Farmer created successfully")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error creating farmer")

def add_farm_card(db, f_uuid: str, farm_card: dict):
    """
    Add a new farm card to an existing farmer.
    """
    try:
        # Find the farmer
        farmer = db.find_one({"f_uuid": f_uuid})
        if not farmer:
            return ErrorResponseModel(error="Farmer not found", code=404, message="Farmer not found")

        # Generate a unique farm_name_id for the new farm card
        farm_count = len(farmer["farm_cards"])
        farm_card["farm_name_id"] = f"{f_uuid}_farm_{farm_count + 1}"

        # Add the new farm card to the farmer's farm_cards list
        farmer["farm_cards"].append(farm_card)

        # Update the farmer's data in the database
        result = db.update_one({"f_uuid": f_uuid}, {"$set": farmer})
        if result.modified_count == 1:
            return ResponseModel(data=str(result.modified_count), code=200, message="Farm card added successfully")
        else:
            return ErrorResponseModel(error="Failed to add farm card", code=500, message="Error adding farm card")

    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error adding farm card")

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







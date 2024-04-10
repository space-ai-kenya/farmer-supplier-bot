from typing import List, Optional
from bson import ObjectId
import logging
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from db.models import (
    FarmerSchema,
    FarmingDetails,
    Vaccination,
    ResponseModel,
    ErrorResponseModel
)

# ---------------- farmer

def create_farmer(db,farmer: FarmerSchema):
    try:
        result = db.insert_one(farmer.model_dump())
        return ResponseModel(data=str(result.inserted_id), code=201, message="Farmer created successfully")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error creating farmer")


def retrieve_all_farmers(db, skip: int = 0, limit: int = 10):
    try:
        farmers = list(db.find({}, skip=skip, limit=limit))
        return ResponseModel(data=farmers, code=200, message="Farmers retrieved successfully")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error retrieving farmers")

def get_farmer(db,f_uuid: str):
    try:
        farmer = db.find_one({"f_uuid": f_uuid})
        if farmer:
            return ResponseModel(data=farmer, code=200, message="Farmer found")
        else:
            return ResponseModel(data=None, code=404, message="Farmer not found")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error retrieving farmer")

def update_farmer(db,f_uuid: str, farmer: FarmerSchema):
    try:
        result = db.update_one({"f_uuid": f_uuid}, {"$set": farmer.model_dump()})
        if result.modified_count > 0:
            return ResponseModel(data=None, code=200, message="Farmer updated successfully")
        else:
            return ResponseModel(data=None, code=404, message="Farmer not found")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error updating farmer")

def delete_farmer(db,f_uuid: str):
    try:
        result = db.delete_one({"f_uuid": f_uuid})
        if result.deleted_count > 0:
            return ResponseModel(data=None, code=200, message="Farmer deleted successfully")
        else:
            return ResponseModel(data=None, code=404, message="Farmer not found")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error deleting farmer")

def list_farmers(db,skip: int = 0, limit: int = 10):
    try:
        farmers = db.find({}, skip=skip, limit=limit).to_list(length=limit)
        return ResponseModel(data=farmers, code=200, message="Farmers retrieved successfully")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error retrieving farmers")


# Add number of cows
def add_num_cows(db, p_number: str, cows: int):
    farmer = db.find_one({"PhoneNumber": p_number})
    if farmer is None:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    farmer_card = farmer.get("farmer_Card", {})
    livestock_details = farmer_card.get("livestockDetails", {})

    # Check numberOfCows else put 0
    numberOfCows = livestock_details.get("numberOfCows", 0)

    if not isinstance(numberOfCows, int):
        numberOfCows = 0
        db.update_one(
            {"PhoneNumber": p_number},
            {"$set": {"farmer_Card.livestockDetails.numberOfCows": numberOfCows}}
        )
    else:
        # Update numberOfCows with the provided value
        numberOfCows += cows
        db.update_one(
            {"PhoneNumber": p_number},
            {"$set": {"farmer_Card.livestockDetails.numberOfCows": numberOfCows}}
        )

    return numberOfCows

def add_vaccinations(db, p_number: str, vaccinations: List[Vaccination]):
    farmer = db.find_one({"PhoneNumber": p_number})
    if farmer is None:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    farmer_card = farmer.get("farmer_Card", {})
    livestock_details = farmer_card.get("livestockDetails", {})

    # Get existing vaccination list or initialize an empty list
    existing_vaccinations = livestock_details.get("vaccinations", [])

    # Append new vaccinations to the existing list
    existing_vaccinations.extend(vaccinations)

    # Update the livestockDetails with the new vaccination list
    db.update_one(
        {"PhoneNumber": p_number},
        {"$set": {"farmer_Card.livestockDetails.vaccinations": existing_vaccinations}}
    )

    return existing_vaccinations




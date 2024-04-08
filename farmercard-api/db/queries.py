from typing import List, Optional
from bson import ObjectId
import logging
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from .models import (
    FarmerSchema,
    FarmingDetails,
    MilkProduction,
    Vaccination,





    ResponseModel,
    ErrorResponseModel
)

def farmer_helper(farmer) -> dict:
    return {
        "id": str(farmer["_id"]),
        "f_uuid": farmer["f_uuid"],
        "PhoneNumber": farmer["PhoneNumber"],
        "farmer_Card": farmer["farmer_Card"],
    }


def add_farmer(db,farmer_data: FarmerSchema) -> Optional[dict]:
    # search for a farmer with similar to given phone numnber
    existing_farmer = db.find_one({"PhoneNumber": farmer_data.get("PhoneNumber")})
    if existing_farmer:
        logging.info("Farmer already exists")
        return ErrorResponseModel(error="Farmer already exists",code=409)
    
    result = db.insert_one(farmer_data)
    logging.info(result)
    if result.inserted_id:
        new_farmer = db.find_one({"_id": result.inserted_id})
        logging.info(new_farmer)
        return farmer_helper(new_farmer)
    return None

def retrieve_all_farmers(db) -> list:
    farmers = []
    for farmer in db.find():
        farmers.append(farmer_helper(farmer))
    return farmers

def add_milk_production(db, p_number: str, milk_production: MilkProduction):
    farmer = db.find_one({"PhoneNumber": p_number})

    if farmer is None:
        raise HTTPException(status_code=404, detail="Farmer not found")

    farmer_card = farmer.get("farmer_Card", {})
    livestock_details = farmer_card.get("livestockDetails", {})

    # If livestockDetails doesn't exist or is not a dictionary, initialize it as an empty dictionary
    if not isinstance(livestock_details, dict):
        livestock_details = {}
        db.update_one(
            {"PhoneNumber": p_number},
            {"$set": {"farmer_Card.livestockDetails": livestock_details}}
        )

    # If "milkProduction" doesn't exist in livestockDetails, initialize it as an empty list
    milk_production_list = livestock_details.get("milkProduction", [])
    
    # Append the new milk production details to the list
    milk_production_list.append(jsonable_encoder(milk_production))
    
    # Update the livestockDetails with the new milkProduction list
    db.update_one(
        {"PhoneNumber": p_number},
        {"$set": {"farmer_Card.livestockDetails": {"milkProduction": milk_production_list}}}
    )

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

from typing import List, Optional
from bson import ObjectId
import logging
from fastapi import HTTPException
from .models import (
    FarmerSchema,
    MilkProduction,

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
    existing_farmer = db.find_one({ "PhoneNumber": farmer_data.get("PhoneNumber")})
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


def add_milk_production(db, f_uuid: str, milk_production: MilkProduction):
    result = db.update_one({"f_uuid": f_uuid},
        {"$push": {"farmer_Card.farmingDetails.livestockDetails.milkProduction": milk_production.dict()}})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Farmer not found")

def update_farmer_by_id(db, id: str, farmer_data: dict) -> Optional[dict]:
    if len(farmer_data) < 1:
        return None
    updated_farmer =  db.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": farmer_data}, return_document=True
    )
    if updated_farmer:
        return farmer_helper(updated_farmer)
    return None


def update_farmer_by_uuid(db,uuid: str, data: dict) -> bool:
    if len(data) < 1:
        return False
    result =  db.update_one(
        {"f_uuid": uuid}, {"$set": data}
    )
    return result.modified_count > 0

def retrieve_farmer_by_uuid(db, uuid: str) -> Optional[dict]:
    farmer =  db.find_one({"f_uuid": uuid})
    if farmer:
        return farmer_helper(farmer)
    return None


def retrieve_all_farmers(db) -> list:
    farmers = []
    for farmer in db.find():
        farmers.append(farmer_helper(farmer))
    return farmers


def delete_farmer(db, uuid: str) -> bool:
    result =  db.delete_one({"f_uuid": uuid})
    return result.deleted_count > 0

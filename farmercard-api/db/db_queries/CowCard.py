from typing import List, Optional
from bson import ObjectId
import logging
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from db.models import (
    FarmerSchema,
    CowCard,
    FarmingDetails,
    Vaccination,

    # -----------------------
    ResponseModel,
    ErrorResponseModel
)

# -------------------- Cow Card

def create_cow_card(db,f_uuid: str, cow_card: CowCard) :
    try:
        farmer = db.find_one({"f_uuid": f_uuid})
        if farmer:
            farmer["farmer_Card"]["farmingDetails"]["livestockDetails"]["cow_card"] = cow_card.dict()
            result = db.update_one({"f_uuid": f_uuid}, {"$set": farmer})
            if result.modified_count > 0:
                return ResponseModel(data=str(result.upserted_id), code=201, message="Cow card created successfully")
            else:
                return ResponseModel(data=None, code=404, message="Farmer not found")
        else:
            return ResponseModel(data=None, code=404, message="Farmer not found")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error creating cow card")

def get_cow_card(db,f_uuid: str, cow_id: str) :
    try:
        farmer = db.find_one({"f_uuid": f_uuid})
        if farmer:
            cow_card = farmer["farmer_Card"]["farmingDetails"]["livestockDetails"]["cow_card"]
            if cow_card and cow_card["identification_info"]["unique_id"] == cow_id:
                return ResponseModel(data=cow_card, code=200, message="Cow card found")
            else:
                return ResponseModel(data=None, code=404, message="Cow card not found")
        else:
            return ResponseModel(data=None, code=404, message="Farmer not found")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error retrieving cow card")

def update_cow_card(db,f_uuid: str, cow_id: str, cow_card: CowCard) :
    try:
        farmer = db.find_one({"f_uuid": f_uuid})
        if farmer:
            farmer["farmer_Card"]["farmingDetails"]["livestockDetails"]["cow_card"] = cow_card.dict()
            result = db.update_one({"f_uuid": f_uuid}, {"$set": farmer})
            if result.modified_count > 0:
                return ResponseModel(data=None, code=200, message="Cow card updated successfully")
            else:
                return ResponseModel(data=None, code=404, message="Cow card not found")
        else:
            return ResponseModel(data=None, code=404, message="Farmer not found")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error updating cow card")

def delete_cow_card(db,f_uuid: str, cow_id: str) :
    try:
        farmer = db.find_one({"f_uuid": f_uuid})
        if farmer:
            if "cow_card" in farmer["farmer_Card"]["farmingDetails"]["livestockDetails"] and farmer["farmer_Card"]["farmingDetails"]["livestockDetails"]["cow_card"]["identification_info"]["unique_id"] == cow_id:
                farmer["farmer_Card"]["farmingDetails"]["livestockDetails"]["cow_card"] = None
                result = db.update_one({"f_uuid": f_uuid}, {"$set": farmer})
                if result.modified_count > 0:
                    return ResponseModel(data=None, code=200, message="Cow card deleted successfully")
                else:
                    return ResponseModel(data=None, code=404, message="Cow card not found")
            else:
                return ResponseModel(data=None, code=404, message="Cow card not found")
        else:
            return ResponseModel(data=None, code=404, message="Farmer not found")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error deleting cow card")
    

# -------------------- vacinations
def create_vaccination(db, f_uuid: str, vaccination: Vaccination) -> ResponseModel:
    try:
        farmer = db.find_one({"f_uuid": f_uuid})
        if farmer:
            if "vaccinations" not in farmer["farmer_Card"]["farmingDetails"]["livestockDetails"]:
                farmer["farmer_Card"]["farmingDetails"]["livestockDetails"]["vaccinations"] = []
            farmer["farmer_Card"]["farmingDetails"]["livestockDetails"]["vaccinations"].append(vaccination.dict())
            result = db.update_one({"f_uuid": f_uuid}, {"$set": farmer})
            if result.modified_count > 0:
                return ResponseModel(data=str(result.upserted_id), code=201, message="Vaccination created successfully")
            else:
                return ResponseModel(data=None, code=404, message="Farmer not found")
        else:
            return ResponseModel(data=None, code=404, message="Farmer not found")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error creating vaccination")

def get_vaccinations(db, f_uuid: str) -> ResponseModel:
    try:
        farmer = db.find_one({"f_uuid": f_uuid})
        if farmer:
            vaccinations = farmer["farmer_Card"]["farmingDetails"]["livestockDetails"]["vaccinations"]
            return ResponseModel(data=vaccinations, code=200, message="Vaccinations retrieved successfully")
        else:
            return ResponseModel(data=None, code=404, message="Farmer not found")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error retrieving vaccinations")

def update_vaccination(db, f_uuid: str, cow_id: str, vaccination: Vaccination) -> ResponseModel:
    try:
        farmer = db.find_one({"f_uuid": f_uuid})
        if farmer:
            vaccinations = farmer["farmer_Card"]["farmingDetails"]["livestockDetails"]["vaccinations"]
            for i, v in enumerate(vaccinations):
                if v["cow_id"] == cow_id:
                    vaccinations[i] = vaccination.dict()
                    break
            farmer["farmer_Card"]["farmingDetails"]["livestockDetails"]["vaccinations"] = vaccinations
            result = db.update_one({"f_uuid": f_uuid}, {"$set": farmer})
            if result.modified_count > 0:
                return ResponseModel(data=None, code=200, message="Vaccination updated successfully")
            else:
                return ResponseModel(data=None, code=404, message="Vaccination not found")
        else:
            return ResponseModel(data=None, code=404, message="Farmer not found")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error updating vaccination")

def delete_vaccination(db, f_uuid: str, cow_id: str) -> ResponseModel:
    try:
        farmer = db.find_one({"f_uuid": f_uuid})
        if farmer:
            vaccinations = farmer["farmer_Card"]["farmingDetails"]["livestockDetails"]["vaccinations"]
            for i, v in enumerate(vaccinations):
                if v["cow_id"] == cow_id:
                    del vaccinations[i]
                    farmer["farmer_Card"]["farmingDetails"]["livestockDetails"]["vaccinations"] = vaccinations
                    result = db.update_one({"f_uuid": f_uuid}, {"$set": farmer})
                    if result.modified_count > 0:
                        return ResponseModel(data=None, code=200, message="Vaccination deleted successfully")
                    else:
                        return ResponseModel(data=None, code=404, message="Vaccination not found")
            return ResponseModel(data=None, code=404, message="Vaccination not found")
        else:
            return ResponseModel(data=None, code=404, message="Farmer not found")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error deleting vaccination")
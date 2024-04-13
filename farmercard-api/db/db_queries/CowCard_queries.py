from typing import List, Optional
from bson import ObjectId
import logging
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from db.schemas.farm_card_schema import (
    FarmerSchema,
)

from db.schemas.response_schema import (
    ResponseModel,
    ErrorResponseModel
)

from db.schemas.cow_card_schema import (
    CowCard,
    VaccineRecord,
    MilkProduction
)

# -------------------- Cow Card
def create_cow_card(db, f_uuid: str, cow_id: str):
    """
    Add a new cow card to the existing document.

    Args:
        db (MongoClient): MongoDB database client.
        f_uuid (str): Unique identifier for the farmer.
        cow_id (str): Unique identifier for the cow.

    Returns:
        ResponseModel or ErrorResponseModel: The response model with the updated document or an error.
    """
    try:
        # Find the document by the f_uuid
        farmer = db.find_one({"f_uuid": f_uuid})

        if farmer:
            # Update the document
            query = {"f_uuid": f_uuid}
            update = {"$push": {"farmer_Card.farmingDetails.livestockDetails.cow_card":CowCard.dict()}}
            result = db.update_one(query, update)

            if result.modified_count > 0:
                updated_doc = db.find_one(query)
                return ResponseModel(data=updated_doc, code=200, message="Cow card added successfully")
            else:
                return ErrorResponseModel(error=f"No document found for f_uuid: {f_uuid}", code=404, message="Document not found")
        else:
            return ErrorResponseModel(error=f"No document found for f_uuid: {f_uuid}", code=404, message="Farmer Not Found")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error adding cow card")

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
    

# --------------------------- add milk production
def add_milk_production_data(db, f_uuid: str, cow_id: str, milk_production_data: MilkProduction):
    """
    Add milk production data to the existing document.

    Args:
        db (MongoClient): MongoDB database client.
        f_uuid (str): Unique identifier for the farmer.
        cow_id (str): Unique identifier for the cow.
        milk_production_data (MilkProduction): Milk production data to be added.

    Returns:
        ResponseModel or ErrorResponseModel: The response model with the updated document or an error.
    """
    try:
        # Find the document by the f_uuid
        farmer = db.find_one({"f_uuid": f_uuid})

        if farmer:
            # Find the cow_card with the given cow_id
            cow_card = farmer["farmer_Card"]["farmingDetails"]["livestockDetails"]["cow_card"]
            logging.info(cow_card)
            if cow_card:
                # logging.info(f"cow_cards: {cow_card}")
                if cow_card["identification_info"]["unique_id"] == cow_id:
                    logging.info(f"cow_card: {cow_id}")

                    # Add the milk production data to the existing cow_card
                    cow_card["milk_production_data"].append(milk_production_data.dict())

                    # Update the document
                    query = {"f_uuid": f_uuid}
                    update = {"$set": {"farmer_Card.farmingDetails.livestockDetails.cow_card.milk_production_data": cow_card["milk_production_data"]}}
                    result = db.update_one(query, update)
                    logging.info(result)

                    if result.modified_count > 0:
                        updated_doc = db.find_one(query)
                        return ResponseModel(data=updated_doc, code=200, message="Milk production data added successfully")
            else:
                # Add a new cow_card to the document
                response = create_cow_card(db, f_uuid, cow_id)
                if isinstance(response, ResponseModel):
                    # Try adding the milk production data again
                    return add_milk_production_data(db, f_uuid, cow_id, milk_production_data)
                else:
                    return response
        else:
            return ErrorResponseModel(error=f"No document found for f_uuid: {f_uuid}", code=404, message="Document not found")

    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error adding milk production data")



# -------------------- vacinations
def create_vaccination(db, f_uuid: str, vaccination: VaccineRecord) -> ResponseModel:
    try:
        farmer = db.find_one({"f_uuid": f_uuid})
        if farmer:
            if "VaccineRecords" not in farmer["farmer_Card"]["farmingDetails"]["livestockDetails"]:
                farmer["farmer_Card"]["farmingDetails"]["livestockDetails"]["VaccineRecords"] = []
            farmer["farmer_Card"]["farmingDetails"]["livestockDetails"]["VaccineRecords"].append(VaccineRecord.dict())
            result = db.update_one({"f_uuid": f_uuid}, {"$set": farmer})
            if result.modified_count > 0:
                return ResponseModel(data=str(result.upserted_id), code=201, message="VaccineRecord created successfully")
            else:
                return ResponseModel(data=None, code=404, message="Farmer not found")
        else:
            return ResponseModel(data=None, code=404, message="Farmer not found")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error creating VaccineRecord")

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

def update_vaccination(db, f_uuid: str, cow_id: str, vaccination: VaccineRecord) -> ResponseModel:
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
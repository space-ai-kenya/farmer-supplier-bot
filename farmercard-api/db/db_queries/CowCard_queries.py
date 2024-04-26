from typing import List, Optional
from bson import ObjectId
import logging
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from db.schemas.response_schema import (
    ResponseModel,
    ErrorResponseModel
)
# -------------------- Cow Card
def create_cow_info(db, PhoneNumber: str, farm_name_id: str, cow_data: dict):
    """
    Create a new cow identification information for the farmer.
    """
    try:
        # Check if the farmer exists
        farmer = db.find_one({"PhoneNumber": PhoneNumber})
        logging.info(farmer)

        if not farmer:
            return ErrorResponseModel(error="Farmer not found", code=404, message="Farmer does not exist")

        # Find the farm card for the given farm_name_id
        farm_card = next((card for card in farmer["farm_cards"] if card["farm_name_id"] == farm_name_id), None)
        if not farm_card:
            return ErrorResponseModel(error="Farm not found", code=404, message="Farm does not exist for the given farmer")

        # Check if the cow_card section exists, if not, create it
        if "cow_card" not in farm_card["livestockDetails"]:
            db.update_one({"PhoneNumber": PhoneNumber, "farm_cards.$.farm_name_id": farm_name_id},
                           {"$set": {"farm_cards.$.livestockDetails.cow_card": []}})

        # Check if a cow with the same unique ID already exists
        existing_cow = next((cow for cow in farm_card["livestockDetails"]["cow_card"] if cow["identification_info"]["unique_id"] == cow_data["unique_id"]), None)
        if existing_cow:
            return ErrorResponseModel(error="Cow already exists", code=409, message="A cow with the same unique ID already exists")
        # Add the new cow identification information to the farmer's livestock details
        cow_info = {
            "identification_info": cow_data
        }
        # Find where farm id and uuid match append cow info
        db.update_one({"PhoneNumber": PhoneNumber, "farm_cards.farm_name_id": farm_name_id},
                      {"$push": {"farm_cards.$.livestockDetails.cow_card": cow_info}})
        return ResponseModel(data=cow_info, code=201, message="Cow identification information created successfully")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error creating cow identification information")
    
def create_milk_production_data(db, PhoneNumber: str, farm_name_id: str, cow_id: str, milk_production_data: list):
    """
    Create a new milk production data for a cow.
    """
    try:
        logging.info(milk_production_data)
        # Check if the farmer exists
        farmer = db.find_one({"PhoneNumber": PhoneNumber})
        if not farmer:
            return ErrorResponseModel(error="Farmer not found", code=404, message="Farmer does not exist")

        # Find the farm card for the given farm_name_id
        farm_card = next((card for card in farmer["farm_cards"] if card["farm_name_id"] == farm_name_id), None)
        if not farm_card:
            return ErrorResponseModel(error="Farm not found", code=404, message="Farm does not exist for the given farmer")

        # Check if the cow_card section exists, if not, create it
        if "cow_card" not in farm_card["livestockDetails"]:
            db.update_one({"PhoneNumber": PhoneNumber, "farm_cards.farm_name_id": farm_name_id},
                          {"$set": {"farm_cards.$.livestockDetails.cow_card": []}})

        # Find the cow card with the given cow_id
        cow_card_info = next((card for card in farm_card["livestockDetails"]["cow_card"] if card["identification_info"]["unique_id"] == cow_id), None)
        if not cow_card_info:
            return ErrorResponseModel(error="Cow card not found", code=404, message=f"Cow of id: {cow_id} does not exist")

        # Check if the milk_production_data section exists, if not, create it
        if "milk_production_data" not in cow_card_info:
            db.update_one(
                {"PhoneNumber": PhoneNumber, "farm_cards.livestockDetails.cow_card.identification_info.unique_id": cow_id},
                {"$set": {"farm_cards.$[].livestockDetails.cow_card.$[].milk_production_data": []}}
            )

        # Update the milk_production_data array for the specific cow card
        db.update_one(
            {"PhoneNumber": PhoneNumber, "farm_cards.livestockDetails.cow_card.identification_info.unique_id": cow_id},
            {"$push": {"farm_cards.$[].livestockDetails.cow_card.$[elem].milk_production_data": milk_production_data}},
            array_filters=[{"elem.identification_info.unique_id": cow_id}]
        )
        return ResponseModel(data=milk_production_data, code=201, message="Milk production data created successfully")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error creating milk production data")

# ---------------------- Reproductive Health Queries ---------------------------------------------------
def create_vaccination_history(db, PhoneNumber: str, cow_id: str,farm_name_id: str, vaccination_record:list):
    """
    Create new vaccination history for a cow.
    """
    try:
        logging.info(vaccination_record)
        # Check if the farmer exists
        farmer = db.find_one({"PhoneNumber": PhoneNumber})
        if not farmer:
            return ErrorResponseModel(error="Farmer not found", code=404, message="Farmer does not exist")

        # Find the farm card for the given farm_name_id
        farm_card = next((card for card in farmer["farm_cards"] if card["farm_name_id"] == farm_name_id), None)
        if not farm_card:
            return ErrorResponseModel(error="Farm not found", code=404, message="Farm does not exist for the given farmer")

        # Check if the cow_card section exists, if not, create it
        if "cow_card" not in farm_card["livestockDetails"]:
            db.update_one({"PhoneNumber": PhoneNumber, "farm_cards.farm_name_id": farm_name_id},
                          {"$set": {"farm_cards.$.livestockDetails.cow_card": []}})

        # Find the cow card with the given cow_id
        cow_card_info = next((card for card in farm_card["livestockDetails"]["cow_card"] if card["identification_info"]["unique_id"] == cow_id), None)
        if not cow_card_info:
            return ErrorResponseModel(error="Cow card not found", code=404, message=f"Cow of id: {cow_id} does not exist")

        # Check if the milk_production_data section exists, if not, create it
        if "vaccination_record" not in cow_card_info:
            db.update_one(
                {"PhoneNumber": PhoneNumber, "farm_cards.livestockDetails.cow_card.identification_info.unique_id": cow_id},
                {"$set": {"farm_cards.$[].livestockDetails.cow_card.$[].vaccination_record": []}}
            )

        # Update the milk_production_data array for the specific cow card
        db.update_one(
            {"PhoneNumber": PhoneNumber, "farm_cards.livestockDetails.cow_card.identification_info.unique_id": cow_id},
            {"$push": {"farm_cards.$[].livestockDetails.cow_card.$[elem].vaccination_record": {"$each": vaccination_record}}},
            array_filters=[{"elem.identification_info.unique_id": cow_id}]
        )
        return ResponseModel(data=vaccination_record, code=201, message="Vaccination Record created successfully ✅")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error creating vaccination history")


def create_calving_history(db, PhoneNumber: str, cow_id: str, farm_name_id: str, calving_info: dict):
    """
    Create new calving information for a cow.
    """
    try:
        # Check if the farmer exists
        farmer = db.find_one({"PhoneNumber": PhoneNumber})
        if not farmer:
            return ErrorResponseModel(error="Farmer not found", code=404, message="Farmer does not exist")

        # Find the farm card for the given farm_name_id
        farm_card = next((card for card in farmer["farm_cards"] if card["farm_name_id"] == farm_name_id), None)
        if not farm_card:
            return ErrorResponseModel(error="Farm not found", code=404, message="Farm does not exist for the given farmer")

        # Check if the cow_card section exists, if not, create it
        if "cow_card" not in farm_card["livestockDetails"]:
            db.update_one({"PhoneNumber": PhoneNumber, "farm_cards.farm_name_id": farm_name_id},
                          {"$set": {"farm_cards.$.livestockDetails.cow_card": []}})

        # Find the cow card with the given cow_id
        cow_card_info = next((card for card in farm_card["livestockDetails"]["cow_card"] if card["identification_info"]["unique_id"] == cow_id), None)
        if not cow_card_info:
            return ErrorResponseModel(error="Cow card not found", code=404, message=f"Cow of id: {cow_id} does not exist")

        # Check if the calving_information section exists, if not, create it
        if "calving_information" not in cow_card_info:
            db.update_one(
                {"PhoneNumber": PhoneNumber, "farm_cards.livestockDetails.cow_card.identification_info.unique_id": cow_id},
                {"$set": {"farm_cards.$[].livestockDetails.cow_card.$[].calving_information": []}}
            )

       # Update the calving_information array for the specific cow card
        db.update_one(
            {"PhoneNumber": PhoneNumber, "farm_cards.livestockDetails.cow_card.identification_info.unique_id": cow_id},
            {"$push": {"farm_cards.$[].livestockDetails.cow_card.$[elem].calving_information": calving_info}},
            array_filters=[{"elem.identification_info.unique_id": cow_id}]
        )
        return ResponseModel(data=calving_info, code=201, message="Calving Information created successfully ✅")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error creating calving record")


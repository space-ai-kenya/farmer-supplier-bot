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



from fastapi.encoders import jsonable_encoder
import json
# ---------------- farmer

def create_farmer(db,farmer: FarmerSchema):
    try:
        # Define the farmer data with empty sections
        f_data = farmer.dict()
        f_data.pop("farmer_Card")
        print(f_data)

        # result = db.insert_one(f_data)
        # return ResponseModel(data=str(result.inserted_id), code=201, message="Farmer created successfully")
        return ResponseModel(data=str(".."), code=201, message="Farmer created successfully")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error creating farmer")

def update_farmer(db, f_uuid: str,phone_no:str, farmer_data: FarmerSchema):
    try:
        # Create a new FarmerSchema instance with the updated f_uuid
        updated_farmer_data = farmer_data.copy(update={'f_uuid': f_uuid,"PhoneNumber":phone_no})
        filter_query = {"f_uuid": f_uuid}
        update_query = {"$set": updated_farmer_data.dict()}
        result = db.update_one(filter_query, update_query)
        if result.matched_count  > 0:
            return ResponseModel(data=None, code=200, message="Farmer updated successfully")
        else:
            return ResponseModel(data=None, code=404, message="Farmer not found")
    except Exception as e:
        logging.error(f"Error updating farmer: {str(e)}")
        return ErrorResponseModel(error=str(e), code=500, message="Error updating farmer")

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




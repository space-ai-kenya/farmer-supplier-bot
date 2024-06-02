from db.schemas.response_schema import (
    ResponseModel,
    ErrorResponseModel
)
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
                    "farm_name_id": farm_name_id,
                    "farmSize": "",
                    "livestockDetails": {
                        "cow_card": [],
                    },
                    "inventory":{},
                    "records":{
                        "milk_production":[],
                        "harvest_records": [],
                        "sales_records": [],
                        "daily_expenses": [],  
                        "monthly_savings_plan": [],  
                        "income_expenditure_plan": []
                    }
                }
            ]
        }

        # Insert the farmer data into the database
        result = db.insert_one(f_data)
        return ResponseModel(data=str(result.inserted_id), code=201, message="Farmer created successfully")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error creating farmer")


def add_farm_card(db,phone_number: str, farm_name_id: str):
    try:
        # Find the farmer by f_uuid
        farmer = db.find_one({"PhoneNumber": phone_number})
        if not farmer:
            return ErrorResponseModel(error="Farmer not found", code=404, message="Farmer does not exist")

        # Create a new farm card
        new_farm_card = {
            "farm_name_id": f"farm_{farm_name_id}",
            "farmSize": "",
            "livestockDetails": {
                "cow_card": [],
                "animal_inventory": []
            }
        }

        # Update the farmer's data in the database
        result = db.update_one({"PhoneNumber": phone_number},
            {"$push": {"farm_cards": new_farm_card}})
        if result.modified_count > 0:
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


def get_farm_name_ids(db, phone_number: str):
    try:
        # Find the farmer by phone number
        farmer = db.find_one({"PhoneNumber": phone_number})
        if not farmer:
            return ErrorResponseModel(
                error="Farmer not found",
                code=404,
                message="Farmer does not exist"
            )

        # Get the farm cards for the farmer
        farm_cards = farmer.get("farm_cards", [])

        # Extract farm_name_ids from farm cards
        farm_name_ids = [farm_card.get("farm_name_id") for farm_card in farm_cards]

        if not farm_name_ids:
            return ErrorResponseModel(
                error="Farm name IDs not found",
                code=404,
                message="No farm name IDs found for the given phone number"
            )

        return ResponseModel(
            data=farm_name_ids,
            code=200,
            message="Farm name IDs retrieved successfully"
        )
    except Exception as e:
        return ErrorResponseModel(
            error=str(e),
            code=500,
            message="Error retrieving farm name IDs"
        )

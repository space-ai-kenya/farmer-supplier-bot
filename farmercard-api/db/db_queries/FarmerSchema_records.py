from db.schemas.response_schema import (
    ResponseModel,
    ErrorResponseModel
)
import json





# -------------------- Record Keeping
def add_daily_expense(db, phone_number: str, farm_name_id: str, daily_expense: dict):
    try:
        # Find the farmer by PhoneNumber
        farmer = db.find_one({"PhoneNumber": phone_number})
        if not farmer:
            return ErrorResponseModel(error="Farmer not found", code=404, message="Farmer does not exist")

        # Find the farm card within the farmer's data
        for farm_card in farmer.get("farm_cards", []):
            if farm_card["farm_name_id"] == farm_name_id:
                farm_card["records"]["daily_expenses"].append(daily_expense.dict())
                result = db.update_one({"PhoneNumber": phone_number}, {"$set": {"farm_cards": farmer["farm_cards"]}})
                if result.modified_count > 0:
                    return ResponseModel(data=str(result.modified_count), code=200, message="Daily expense added successfully")
                else:
                    return ErrorResponseModel(error="Failed to add daily expense", code=500, message="Error adding daily expense")
        return ErrorResponseModel(error="Farm card not found", code=404, message="Farm card does not exist")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error adding daily expense")



def add_monthly_savings_plan(db, phone_number: str, farm_name_id: str, monthly_savings_plan: dict):
    try:
        # Find the farmer by PhoneNumber
        farmer = db.find_one({"PhoneNumber": phone_number})
        if not farmer:
            return ErrorResponseModel(error="Farmer not found", code=404, message="Farmer does not exist")

        # Find the farm card within the farmer's data
        for farm_card in farmer.get("farm_cards", []):
            if farm_card["farm_name_id"] == farm_name_id:
                farm_card["records"]["monthly_savings_plans"].append(monthly_savings_plan.dict())
                result = db.update_one({"PhoneNumber": phone_number}, {"$set": {"farm_cards": farmer["farm_cards"]}})
                if result.modified_count > 0:
                    return ResponseModel(data=str(result.modified_count), code=200, message="Monthly savings plan added successfully")
                else:
                    return ErrorResponseModel(error="Failed to add monthly savings plan", code=500, message="Error adding monthly savings plan")
        return ErrorResponseModel(error="Farm card not found", code=404, message="Farm card does not exist")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error adding monthly savings plan")

def add_income_expenditure_plan(db, phone_number: str, farm_name_id: str, income_expenditure_plan: dict):
    try:
        # Find the farmer by PhoneNumber
        farmer = db.find_one({"PhoneNumber": phone_number})
        if not farmer:
            return ErrorResponseModel(error="Farmer not found", code=404, message="Farmer does not exist")

        # Find the farm card within the farmer's data
        for farm_card in farmer.get("farm_cards", []):
            if farm_card["farm_name_id"] == farm_name_id:
                farm_card["records"]["income_expenditure_plans"].append(income_expenditure_plan.dict())
                result = db.update_one({"PhoneNumber": phone_number}, {"$set": {"farm_cards": farmer["farm_cards"]}})
                if result.modified_count > 0:
                    return ResponseModel(data=str(result.modified_count), code=200, message="Income and expenditure plan added successfully")
                else:
                    return ErrorResponseModel(error="Failed to add income and expenditure plan", code=500, message="Error adding income and expenditure plan")
        return ErrorResponseModel(error="Farm card not found", code=404, message="Farm card does not exist")
    except Exception as e:
        return ErrorResponseModel(error=str(e), code=500, message="Error adding income and expenditure plan")

from fastapi import FastAPI,Body, HTTPException,BackgroundTasks
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
import uvicorn
import logging
from pymongo import MongoClient
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from models import (
    ResponseModel,
    ErrorResponseModel,
    FarmerSchema,
    MilkProduction
    # --------- updates
    # UpdateFarmer,
)


app = FastAPI()

logging.basicConfig(level=logging.INFO)

# MongoDB connection details
MONGO_IP = "mongodb"
MONGO_PORT = 27017
MONGO_USERNAME = "user"
MONGO_PASSWORD = "pass"
MONGO_DB = "farmerdb"
MONGO_DETAILS = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_IP}:{MONGO_PORT}/{MONGO_DB}?authSource=admin&retryWrites=true&w=majority"


client = MongoClient(MONGO_DETAILS)
database = client[MONGO_DB]
farmer_collection = database.get_collection("farmers_collection")

# Event handler to check MongoDB connection on startup
@app.on_event("startup")
async def startup_event():
    try:
        # Attempt to connect to MongoDB and perform a sample query
        client.server_info()
        logging.info("---------Connected to MongoDB successfully!----------")
    except Exception as e:
        logging.error(f"Error connecting to MongoDB: {e}")
        # Optionally, you can raise an exception to halt the startup process if the connection fails
        raise e




def farmer_helper(farmer) -> dict:
    return {
        "id": str(farmer["_id"]),
        "f_uuid": farmer["f_uuid"],
        "PhoneNumber": farmer["PhoneNumber"],
        "farmer_Card": farmer["farmer_Card"],
    }


def update_farmer_by_id(id: str, farmer_data: dict) -> Optional[dict]:
    if len(farmer_data) < 1:
        return None
    updated_farmer =  farmer_collection.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": farmer_data}, return_document=True
    )
    if updated_farmer:
        return farmer_helper(updated_farmer)
    return None


def update_farmer_by_uuid(uuid: str, data: dict) -> bool:
    if len(data) < 1:
        return False
    result =  farmer_collection.update_one(
        {"f_uuid": uuid}, {"$set": data}
    )
    return result.modified_count > 0


def add_farmer(farmer_data: dict) -> Optional[dict]:
    existing_farmer = farmer_collection.find_one({"f_uuid": farmer_data.get("f_uuid")})
    if existing_farmer:
        logging.info("Farmer already exists")
        return None
    
    result = farmer_collection.insert_one(farmer_data)
    logging.info(result)
    if result.inserted_id:
        new_farmer = farmer_collection.find_one({"_id": result.inserted_id})
        logging.info(new_farmer)
        return farmer_helper(new_farmer)
    return None


def add_milk_production(f_uuid: str, milk_production: MilkProduction):
    result = farmer_collection.update_one({"f_uuid": f_uuid},
                                   {"$push": {"farmer_Card.farmingDetails.livestockDetails.milkProduction": milk_production.dict()}})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Farmer not found")



def retrieve_farmer_by_uuid(uuid: str) -> Optional[dict]:
    farmer =  farmer_collection.find_one({"f_uuid": uuid})
    if farmer:
        return farmer_helper(farmer)
    return None


def retrieve_all_farmers() -> list:
    farmers = []
    for farmer in farmer_collection.find():
        farmers.append(farmer_helper(farmer))
    return farmers


def delete_farmer(uuid: str) -> bool:
    result =  farmer_collection.delete_one({"f_uuid": uuid})
    return result.deleted_count > 0





@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Hello World"}



@app.post("/farmers/", response_description="Add new farmer")
def create_farmer(farmer: FarmerSchema):
    farmer = jsonable_encoder(farmer)
    logging.info(farmer)
    new_farmer = add_farmer(farmer)
    if new_farmer:
        return ResponseModel(data=new_farmer,code=200, message= "Farmer added successfully")
    return ErrorResponseModel(error="An error occurred", code=404,message="Farmer not added!")

@app.get("/farmers/", response_description="List all farmers")
def list_farmers():
    return retrieve_all_farmers()


# FastAPI route to add milk production record
@app.post("/farmers/{f_uuid}/milk_production")
async def add_milk_production_route(f_uuid: str, milk_production: MilkProduction):
    add_milk_production(f_uuid, milk_production)
    return {"message": "Milk production record added successfully"}

# @app.get("/farmers/", response_description="List all farmers", response_model=List[FarmerSchema])
#  def list_farmers():
#     farmers =  retrieve_all_farmers()
#     if farmers:
#         return farmers
#     return []

# @app.get("/farmers/{uuid}", response_description="Get a single farmer", response_model=FarmerSchema)
#  def get_farmer(uuid):
#     farmer =  retrieve_farmer_by_uuid(uuid)
#     if farmer:
#         return farmer
#     raise HTTPException(status_code=404, detail="Farmer not found")

# @app.put("/farmers/{uuid}", response_description="Update a farmer", response_model=ResponseModel)
#  def update_farmer_data(uuid: str, req: UpdateFarmer = Body(...)):
#     req = {k: v for k, v in req.dict().items() if v is not None}
#     updated_farmer =  update_farmer_by_uuid(uuid, req)
#     if updated_farmer:
#         return ResponseModel(data="Farmer with UUID: {} has been updated successfully".format(uuid), code=200, message="Farmer updated successfully")
#     raise HTTPException(status_code=404, detail="There was an error updating the farmer data.")

# @app.delete("/farmers/{uuid}", response_description="Delete a farmer", response_model=ResponseModel)
#  def delete_farmer_data(uuid: str):
#     deleted_farmer =  delete_farmer(uuid)
#     if deleted_farmer:
#         return ResponseModel(data="Farmer with UUID: {} removed".format(uuid),code=200,message="Farmer deleted successfully")
#     raise HTTPException(status_code=404, detail="Farmer not found")





if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8086, reload=True)
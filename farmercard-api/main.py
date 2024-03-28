from fastapi import FastAPI,Body, HTTPException,BackgroundTasks
from fastapi.encoders import jsonable_encoder
import uvicorn
import logging
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from db.database import farmer_collection, client
from db.models import (
    ResponseModel,
    ErrorResponseModel,
    FarmerSchema,
    MilkProduction,
    Vaccination,
    # --------- updates
    # UpdateFarmer,
)
from db.queries import(
    add_farmer,
    retrieve_all_farmers,
    add_milk_production,
    add_num_cows,
    add_vaccinations,
)


app = FastAPI()

logging.basicConfig(level=logging.INFO)


def drop_all_records(db, collection_name):
    db[collection_name].delete_many({})



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


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Hello World"}


@app.post("/create_farmcard/", response_description="Add new farmer")
def create_farmer(farmer: FarmerSchema):
    farmer = jsonable_encoder(farmer)
    logging.info(farmer)
    new_farmer = add_farmer(db=farmer_collection, farmer_data=farmer)
    if new_farmer:
        return ResponseModel(data=new_farmer,code=200, message= "Farmer added successfully")
    return ErrorResponseModel(error="An error occurred", code=404,message="Farmer not added!")

@app.get("/farmers/", response_description="List all farmers")
def list_farmers():
    return retrieve_all_farmers(db=farmer_collection)


# FastAPI route to add milk production record
@app.post("/farmer/add_milk_production")
async def add_milk_production_route(p_number: str, milk_production: MilkProduction):
    print(milk_production)
    add_milk_production(db=farmer_collection,p_number=p_number, milk_production=milk_production)
    return {"message": "Milk production record added successfully"}

@app.post("/farmer/add_num_of_cows")
async def add_farmer_cows(p_number: str, cows:int):
    data = add_num_cows(db=farmer_collection,p_number=p_number,cows=cows)
    print(data)
    return {"message": data}

@app.post("/farmer/add_cows_vacination")
async def add_cows_vacination(p_number: str, vaccinations:List[Vaccination]):
    data = add_vaccinations(db=farmer_collection,p_number=p_number,vaccinations=jsonable_encoder(vaccinations))
    print(data)
    return {"message": data}



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8086, reload=True)
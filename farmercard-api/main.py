from fastapi import FastAPI,Body, HTTPException,BackgroundTasks
from fastapi.encoders import jsonable_encoder
import uvicorn
import logging
from fastapi.middleware.cors import CORSMiddleware

from db.database import farmer_collection, client
from db.models import (
    ResponseModel,
    ErrorResponseModel,
    FarmerSchema,
    MilkProduction
    # --------- updates
    # UpdateFarmer,
)
from db.queries import(
    add_farmer,
    retrieve_all_farmers,
    add_milk_production
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
@app.post("/farmer/{p_number}/add_milk_production")
async def add_milk_production_route(p_number: str, milk_production: MilkProduction):
    print(milk_production)
    add_milk_production(db=farmer_collection,p_number=p_number, milk_production=milk_production)
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
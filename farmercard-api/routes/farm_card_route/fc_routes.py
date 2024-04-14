from fastapi import APIRouter,Depends
from fastapi.encoders import jsonable_encoder
from typing import List
from pymongo.collection import Collection
from db.database import get_farmer_collection
from db.schemas.farm_card_schema import (
    FarmerSchema,
)

from db.schemas.cow_card_schema import (
    CowCard
)

from db.db_queries.FarmerSchema_queries import (
    create_farmer,
    retrieve_all_farmers,
)

farm_card_router = APIRouter(
    prefix="/farm_card",
    tags=["farm_card"],
    responses={404: {"description": "Not found"}},
)


@farm_card_router.get("/", tags=["Root"])
def read_root():
    return {"message": "Spaceai.io Says Hello World"}


@farm_card_router.post("/create_farmcard/{f_uuid}/{p_number}/{farming_type}", response_description="Add new farmer")
def create_farmer_card( f_uuid: str, p_number: str, farming_type: str,db: Collection = Depends(get_farmer_collection)):
    response = create_farmer(db, f_uuid, p_number, farming_type)
    return response

@farm_card_router.get("/all_farmers", response_description="List all farmers")
def list_farmers(db: Collection = Depends(get_farmer_collection)): 
    data = retrieve_all_farmers(db)
    return data

@farm_card_router.get("/schema", response_description="List all farmers")
def list_farmers(farmer_schema: FarmerSchema,db: Collection = Depends(get_farmer_collection)): 
    data = farmer_schema.model_dumps()
    # save in a file 
    import json 
    with open("schema.json", "w") as f:
        json.dump(data, f, indent=4)
    return data
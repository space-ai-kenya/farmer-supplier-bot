from fastapi import APIRouter,Depends
from fastapi.encoders import jsonable_encoder
from typing import List
from pymongo.collection import Collection
from db.database import get_farmer_collection
from db.schemas.response_schema import (
    ResponseModel,
)
from db.schemas.farm_card_schema import (
    FarmerSchema,
)

from db.db_queries.FarmerSchema_queries import (
    create_farmer,
    add_farm_card,
    retrieve_all_farmers,
    get_farm_name_ids,
)

farm_card_router = APIRouter(
    prefix="/farm_card",
    tags=["farm_card"],
    responses={404: {"description": "Not found"}},
)




from pydantic import BaseModel

class CreateFarmCard(BaseModel):
    f_uuid: str
    p_number: str
    farming_type: str
    farm_name_id:str

@farm_card_router.post("/create_farmcard", description="Add new farmer", response_model=ResponseModel)
def create_new_farmer(farmer: CreateFarmCard,db: Collection = Depends(get_farmer_collection)):
    f_uuid = farmer.f_uuid
    p_number = farmer.p_number
    farming_type = farmer.farming_type
    farm_name_id = farmer.farm_name_id
    response = create_farmer(db=db, f_uuid=f_uuid,farm_name_id=farm_name_id, phone_number=p_number,farming_type=farming_type)
    return response

class AddFarmCard(BaseModel):
    p_number: str
    farm_name_id:str


@farm_card_router.post("/add_farmcard", description="Add new farm for a farmer", response_model=ResponseModel)
def add_Farm(farmer: AddFarmCard,db: Collection = Depends(get_farmer_collection)):
    p_number = farmer.p_number
    farm_name_id = farmer.farm_name_id
    response = add_farm_card(\
        db=db,farm_name_id=farm_name_id, phone_number=p_number
    )
    return response


@farm_card_router.get("/all_farmers", response_description="List all farmers", response_model=ResponseModel)
def list_farmers(db: Collection = Depends(get_farmer_collection)): 
    data = retrieve_all_farmers(db)
    return data

class FarmNameIds(BaseModel):
    p_number: str

@farm_card_router.post("/farm_name_ids", description="List farm name IDs for a given phone number", response_model=ResponseModel)
async def get_farm_name_ids_endpoint(phone_number: FarmNameIds, db: Collection = Depends(get_farmer_collection)):
    response = get_farm_name_ids(db, phone_number.p_number)
    return response


@farm_card_router.get("/schema", description="Show Case Schema", response_model=ResponseModel)
def farm_card_Schema(farmer_schema: FarmerSchema,db: Collection = Depends(get_farmer_collection)): 
    data = farmer_schema.model_dumps()
    return data
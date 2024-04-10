from fastapi import APIRouter,Depends
from fastapi.encoders import jsonable_encoder

from typing import List
from pymongo.collection import Collection

from db.database import get_farmer_collection
from db.models import (
    ResponseModel,
    ErrorResponseModel,
    FarmerSchema,
    Vaccination,
    CowCard
    # --------- updates
    # UpdateFarmer,
)

from db.db_queries.FarmerSchema import (
    create_farmer,
    retrieve_all_farmers,
    get_farmer,
    update_farmer,
    add_num_cows,
    add_vaccinations
)


farm_card_router = APIRouter(
    prefix="/farm_card",
    tags=["farm_card"],
    responses={404: {"description": "Not found"}},
)


@farm_card_router.get("/", tags=["Root"])
def read_root():
    return {"message": "Spaceai.io Says Hello World"}


@farm_card_router.post("/create_farmcard", response_description="Add new farmer")
def create_farmer(farmer: FarmerSchema,db: Collection = Depends(get_farmer_collection)):
    new_farmer = create_farmer(db, farmer_data=jsonable_encoder(farmer))
    return new_farmer

@farm_card_router.get("/all_farmers", response_description="List all farmers")
def list_farmers(db: Collection = Depends(get_farmer_collection)): 
    data = retrieve_all_farmers(db)
    return data


@farm_card_router.post("/add_num_of_cows")
async def add_farmer_cows(p_number: str, cows:int,db: Collection = Depends(get_farmer_collection)):
    data = add_num_cows(db,p_number=p_number,cows=cows)
    print(data)
    return {"message": data}

@farm_card_router.put("/farmer/{f_uuid}", response_model=ResponseModel)
async def update_single_farmer(
    f_uuid: str,
    farmer: FarmerSchema,
   db: Collection = Depends(get_farmer_collection)
):
    data = update_farmer(db,f_uuid,farmer)
    return 

@farm_card_router.post("/add_cows_vacination")
async def add_cows_vacination(p_number: str, vaccinations:List[Vaccination],db: Collection = Depends(get_farmer_collection)):
    data = add_vaccinations(db,p_number=p_number,vaccinations=jsonable_encoder(vaccinations))
    return {"message": data}

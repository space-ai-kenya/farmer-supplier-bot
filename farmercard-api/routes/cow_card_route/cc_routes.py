from typing import List
from fastapi import APIRouter,Depends,HTTPException
from db.models import (
    FarmerSchema,
    CowCard,
    FarmingDetails,
    Vaccination,
    # -----------------------
    ResponseModel,
    ErrorResponseModel
)
from pymongo.collection import Collection
from db.database import get_farmer_collection

cow_card_router = APIRouter(
    prefix="/cow_card",
    tags=["cow_card"],
    responses={404: {"description": "Not found"}},
)


@cow_card_router.post("/{f_uuid}", response_model=ResponseModel)
def create_cow_card(
    f_uuid: str,
    cow_card: CowCard,
   db: Collection = Depends(get_farmer_collection)
):
    response = create_cow_card(db, f_uuid, cow_card)
    return response

@cow_card_router.get("/{f_uuid}/{cow_id}", response_model=ResponseModel)
def get_cow_card(
    f_uuid: str,
    cow_id: str,
    db: Collection = Depends(get_farmer_collection)
):
    response = get_cow_card(db, f_uuid, cow_id)
    return response

@cow_card_router.put("/{f_uuid}/{cow_id}", response_model=ResponseModel)
def update_cow_card(
    f_uuid: str,
    cow_id: str,
    cow_card: CowCard,
    db: Collection = Depends(get_farmer_collection)
):
    response = update_cow_card(db, f_uuid, cow_id, cow_card)
    return response

@cow_card_router.delete("/{f_uuid}/{cow_id}", response_model=ResponseModel)
def delete_cow_card(
    f_uuid: str,
    cow_id: str,
    db: Collection = Depends(get_farmer_collection)
):
    response = delete_cow_card(db, f_uuid, cow_id)
    return response
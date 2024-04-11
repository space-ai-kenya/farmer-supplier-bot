from typing import List
from fastapi import APIRouter,Depends,HTTPException
from db.models import (
    CowCard,
    MilkProduction,
    # -----------------------
    ResponseModel,
    ErrorResponseModel
)
from pymongo.collection import Collection
from db.database import (
    get_farmer_collection,
    
)
from db.db_queries.CowCard import (
    create_cow_card,
    get_cow_card,
    update_cow_card,
    delete_cow_card,

    # milk production && vaccination
    add_milk_production_data,

)
import logging
cow_card_router = APIRouter(
    prefix="/cow_card",
    tags=["cow_card"],
    responses={404: {"description": "Not found"}},
)


@cow_card_router.post("/{f_uuid}/{cow_id}")
def create_cowcard(
    f_uuid: str,
    cow_id: str,
   db: Collection = Depends(get_farmer_collection)
):
    response = create_cow_card(db, f_uuid, cow_id)
    return response

@cow_card_router.get("/{f_uuid}/{cow_id}")
def get_cowcard(
    f_uuid: str,
    cow_id: str,
    db: Collection = Depends(get_farmer_collection)
):
    response = get_cow_card(db, f_uuid, cow_id)
    return response

@cow_card_router.put("/{f_uuid}/{cow_id}")
def update_cowcard(
    f_uuid: str,
    cow_id: str,
    cow_card: CowCard,
    db: Collection = Depends(get_farmer_collection)
):
    response = update_cow_card(db, f_uuid, cow_id, cow_card)
    return response

@cow_card_router.delete("/{f_uuid}/{cow_id}")
def delete_cowcard(
    f_uuid: str,
    cow_id: str,
    db: Collection = Depends(get_farmer_collection)
):
    response = delete_cow_card(db, f_uuid, cow_id)
    return response


# ------------- milk production
@cow_card_router.post("/add_milk_production/{f_uuid}/{cow_id}")
def add_milkproduction(f_uuid: str,cow_id:str,milk_production_data: MilkProduction,db: Collection = Depends(get_farmer_collection)
):
    """
    Add milk production data to the existing document.

    Args:
        f_uuid (str): Unique identifier for the farmer.
        milk_production_data (MilkProduction): Milk production data to be added.
        db (Collection): MongoDB collection.

    Returns:
        ResponseModel or ErrorResponseModel: The response model with the updated document or an error.
    """
    response = add_milk_production_data(db,f_uuid,cow_id,milk_production_data)
    return response
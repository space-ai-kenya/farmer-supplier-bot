from typing import List
from fastapi import APIRouter,Depends,HTTPException
from pymongo.collection import Collection


from db.database import (
    get_farmer_collection
)
from db.db_queries.CowCard_queries import (
    create_cow_card,
    get_cow_card,
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


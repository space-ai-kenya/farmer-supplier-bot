from typing import List
from fastapi import APIRouter,Depends,HTTPException
from pymongo.collection import Collection
from fastapi.encoders import jsonable_encoder
from db.database import (
    get_farmer_collection
)
from db.db_queries.CowCard_queries import (
    create_cow_info,
    create_heat_cycles,
    create_breeding_events,
    create_calving_history,
    create_milk_production_data,
    create_pregnancy_status,
)
from db.schemas.cow_card_schema import (
    IdentificationInfo,
    MilkProduction,

    # ReproductiveHealth-------------------------------
    HeatCycle,
    BreedingEvent,
    CalvingEvent,
)

from db.schemas.response_schema import (
    ResponseModel
)


import logging
cow_card_router = APIRouter(
    prefix="/cow_card",
    tags=["cow_card"],
    responses={404: {"description": "Not found"}},
)


@cow_card_router.post("/{f_uuid}/create_cow_info")
def createCowinfo(f_uuid: str,cow_info: IdentificationInfo,db: Collection = Depends(get_farmer_collection)):
    response = create_cow_info(db,f_uuid,jsonable_encoder(cow_info))
    return response


@cow_card_router.post("/{f_uuid}/{cow_id}/milk-production", response_model=ResponseModel)
def createMilkProductionData(f_uuid: str,cow_id: str,milk_production_data: MilkProduction,db: Collection = Depends(get_farmer_collection)):
    response = create_milk_production_data(db,f_uuid,cow_id,jsonable_encoder(milk_production_data))
    return response



# ------------------ Health Records ----------------
@cow_card_router.post("/{f_uuid}/{cow_id}/heat-cycles", response_model=ResponseModel)
def createheat_cycles(
    f_uuid: str,
    cow_id: str,
    heat_cycles: List[HeatCycle],
    db: Collection = Depends(get_farmer_collection)
):
    response = create_heat_cycles(db, f_uuid, cow_id, heat_cycles)
    return response

@cow_card_router.post("/{f_uuid}/{cow_id}/breeding-events", response_model=ResponseModel)
def createbreeding_events(
    f_uuid: str,
    cow_id: str,
    breeding_events: List[BreedingEvent],
    db: Collection = Depends(get_farmer_collection)
):
    response = create_breeding_events(db, f_uuid, cow_id, breeding_events)
    return response

@cow_card_router.put("/{f_uuid}/{cow_id}/pregnancy-status", response_model=ResponseModel)
def updatepregnancy_status(
    f_uuid: str,
    cow_id: str,
    pregnancy_status: str,
    db: Collection = Depends(get_farmer_collection)
):
    response = create_pregnancy_status(db, f_uuid, cow_id, pregnancy_status)
    return response

@cow_card_router.post("/{f_uuid}/{cow_id}/calving-history", response_model=ResponseModel)
def createcalving_history(
    f_uuid: str,
    cow_id: str,
    calving_history: List[CalvingEvent],
    db: Collection = Depends(get_farmer_collection)
):
    response = create_calving_history(db, f_uuid, cow_id, calving_history)
    return response
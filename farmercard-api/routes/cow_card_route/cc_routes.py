from typing import List
from fastapi import APIRouter,Depends,HTTPException
from pymongo.collection import Collection
from fastapi.encoders import jsonable_encoder
from db.database import (
    get_farmer_collection
)
from db.db_queries.CowCard_queries import (
    create_cow_info,
    create_vaccination_history,
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
    VaccineRecord
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


@cow_card_router.post("/{PhoneNumber}/create_cow_info", response_model=ResponseModel)
def createCowinfo(PhoneNumber: str,cow_info: IdentificationInfo,db: Collection = Depends(get_farmer_collection)):
    logging.info(cow_info.dict())
    response = create_cow_info(db,PhoneNumber,jsonable_encoder(cow_info))
    logging.info(response.dict())
    return response


@cow_card_router.post("/{PhoneNumber}/{cow_id}/milk-production", response_model=ResponseModel)
def createMilkProductionData(PhoneNumber: str,cow_id: str,milk_production_data: MilkProduction,db: Collection = Depends(get_farmer_collection)):
    response = create_milk_production_data(db,PhoneNumber,cow_id,jsonable_encoder(milk_production_data))
    return response



# ------------------ Health Records ----------------
@cow_card_router.post("/{PhoneNumber}/{cow_id}/vaccinations", response_model=ResponseModel)
def create_VaccinationHistory(PhoneNumber: str,cow_id: str,vaccination:VaccineRecord,db: Collection = Depends(get_farmer_collection)):
    response = create_vaccination_history(db, PhoneNumber, cow_id, jsonable_encoder(vaccination))
    return response



@cow_card_router.post("/{PhoneNumber}/{cow_id}/heat-cycles", response_model=ResponseModel)
def createheat_cycles(PhoneNumber: str,cow_id: str,heat_cycles: List[HeatCycle],db: Collection = Depends(get_farmer_collection)):
    response = create_heat_cycles(db, PhoneNumber, cow_id, heat_cycles)
    return response

@cow_card_router.post("/{PhoneNumber}/{cow_id}/breeding-events", response_model=ResponseModel)
def createbreeding_events(PhoneNumber: str,cow_id: str,breeding_events: List[BreedingEvent],db: Collection = Depends(get_farmer_collection)):
    response = create_breeding_events(db, PhoneNumber, cow_id, breeding_events)
    return response

@cow_card_router.put("/{PhoneNumber}/{cow_id}/{pregnancy_status}/pregnancy-status", response_model=ResponseModel)
def updatepregnancy_status(PhoneNumber: str,cow_id: str,pregnancy_status: str,db: Collection = Depends(get_farmer_collection)):
    response = create_pregnancy_status(db, PhoneNumber, cow_id, pregnancy_status)
    return response

@cow_card_router.post("/{PhoneNumber}/{cow_id}/calving-history", response_model=ResponseModel)
def createcalving_history(PhoneNumber: str,cow_id: str,calving_history: List[CalvingEvent],db: Collection = Depends(get_farmer_collection)):
    response = create_calving_history(db, PhoneNumber, cow_id, calving_history)
    return response
from typing import List
from typing import Union
from fastapi import APIRouter,Depends,HTTPException
from fastapi.responses import JSONResponse
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
    ResponseModel,
    ErrorResponseModel
)


import logging
cow_card_router = APIRouter(
    prefix="/cow_card",
    tags=["cow_card"],
    responses={404: {"description": "Not found"}},
)

from pydantic import BaseModel

class CreateBase(BaseModel):
    f_uuid: str
    p_number: str
    farm_name_id:str

class CreateCowInfo(CreateBase):
    cow_info: IdentificationInfo

@cow_card_router.post("/create_cow_info", response_model=Union[ResponseModel, List[ResponseModel], ErrorResponseModel])
def createCowinfo(cow_identity: Union[CreateCowInfo, List[CreateCowInfo]], db: Collection = Depends(get_farmer_collection)):
    responses = []
    # check from union if its a list or normal
    if isinstance(cow_identity, list):
        logging.info("---------- List of cow info ---------")

        for cow_info in cow_identity:
            logging.info(cow_info.cow_info.dict())
            response = create_cow_info(db, f_uuid=cow_info.f_uuid, farm_name_id=cow_info.farm_name_id, cow_data=jsonable_encoder(cow_info.cow_info))
            logging.info(response.dict())
            responses.append(jsonable_encoder(response))
    else:
        logging.info(cow_identity.cow_info.dict())
        response = create_cow_info(db, f_uuid=cow_identity.f_uuid, farm_name_id=cow_identity.farm_name_id, cow_data=jsonable_encoder(cow_identity.cow_info))
        logging.info(response.dict())
        responses.append(jsonable_encoder(response))
    return JSONResponse(responses[0])


class CreateMilkProduction(CreateBase):
    cow_id: str
    milk_production_data: List[MilkProduction]

@cow_card_router.post("/milk-production", response_model=Union[ResponseModel, ErrorResponseModel])
def createMilkProductionData(milk_prod: Union[CreateMilkProduction, List[CreateMilkProduction]], db: Collection = Depends(get_farmer_collection)):
    responses = []

    if isinstance(milk_prod, list):
        logging.info("---------- List of milk production data ---------")
        for milk_data in milk_prod:
            logging.info(milk_data.milk_production_data)
            response = create_milk_production_data(
                db,
                f_uuid=milk_data.f_uuid,
                farm_name_id=milk_data.farm_name_id,
                cow_id=milk_data.cow_id,
                milk_production_data=jsonable_encoder(milk_data.milk_production_data)
            )
            
            responses.append(jsonable_encoder(response))
    else:
        logging.info(milk_prod.milk_production_data)
        response = create_milk_production_data(
            db,
            f_uuid=milk_prod.f_uuid,
            farm_name_id=milk_prod.farm_name_id,
            cow_id=milk_prod.cow_id,
            milk_production_data=jsonable_encoder(milk_prod.milk_production_data)
        )
        logging.info(response.dict())
        responses.append(jsonable_encoder(response))

    if isinstance(responses[0], ErrorResponseModel):
        return JSONResponse(content=jsonable_encoder(responses[0]))
    else:
        return JSONResponse(content=jsonable_encoder(responses[0]))



# ------------------ Health Records ----------------
@cow_card_router.post("/{PhoneNumber}/{cow_id}/vaccinations", response_model=Union[ResponseModel,ErrorResponseModel])
def create_VaccinationHistory(PhoneNumber: str,cow_id: str,vaccination:VaccineRecord,db: Collection = Depends(get_farmer_collection)):
    response = create_vaccination_history(db, PhoneNumber, cow_id, jsonable_encoder(vaccination))
    return response



@cow_card_router.post("/{PhoneNumber}/{cow_id}/heat-cycles", response_model=Union[ResponseModel,ErrorResponseModel])
def createheat_cycles(PhoneNumber: str,cow_id: str,heat_cycles: List[HeatCycle],db: Collection = Depends(get_farmer_collection)):
    response = create_heat_cycles(db, PhoneNumber, cow_id, heat_cycles)
    return response

@cow_card_router.post("/{PhoneNumber}/{cow_id}/breeding-events", response_model=Union[ResponseModel,ErrorResponseModel])
def createbreeding_events(PhoneNumber: str,cow_id: str,breeding_events:Union[List[BreedingEvent],BreedingEvent],db: Collection = Depends(get_farmer_collection)):
    response = create_breeding_events(db, PhoneNumber, cow_id, breeding_events)
    return response

@cow_card_router.put("/{PhoneNumber}/{cow_id}/{pregnancy_status}/pregnancy-status", response_model=Union[ResponseModel,ErrorResponseModel])
def updatepregnancy_status(PhoneNumber: str,cow_id: str,pregnancy_status: str,db: Collection = Depends(get_farmer_collection)):
    response = create_pregnancy_status(db, PhoneNumber, cow_id, pregnancy_status)
    return response

@cow_card_router.post("/{PhoneNumber}/{cow_id}/calving-history", response_model=Union[ResponseModel,ErrorResponseModel])
def createcalving_history(PhoneNumber: str,cow_id: str,calving_history: List[CalvingEvent],db: Collection = Depends(get_farmer_collection)):
    response = create_calving_history(db, PhoneNumber, cow_id, calving_history)
    return response
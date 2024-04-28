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
    add_milk_production_single,
    add_milk_production_total,

    # ------------------ health
    create_vaccination_history,
    create_calving_history,
)
from db.schemas.cow_card_schema import (
    IdentificationInfo,
    MilkProduction,
    VaccineRecord,
    CalvingEvent
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
    p_number: str
    farm_name_id:str

class CreateCowInfo(CreateBase):
    cow_info: IdentificationInfo

@cow_card_router.post("/create_cow_info", response_model=ResponseModel)
def createCowinfo(cow_identity: CreateCowInfo, db: Collection = Depends(get_farmer_collection)):
    # check from union if its a list or normal
    logging.info(cow_identity.cow_info.dict())
    response = create_cow_info(db,PhoneNumber=cow_identity.p_number, farm_name_id=cow_identity.farm_name_id, cow_data=jsonable_encoder(cow_identity.cow_info))
    logging.info(response.dict())
    return response


class CreateSingleMilkRecord(CreateBase):
    cow_id: str
    milk_production_data: MilkProduction

@cow_card_router.post("/milk-production-single", response_model=ResponseModel)
def milk_Production_single(milk_prod: CreateSingleMilkRecord, db: Collection = Depends(get_farmer_collection)):
    logging.info(milk_prod.milk_production_data)
    response = add_milk_production_single(
        db,
        PhoneNumber=milk_prod.p_number,
        farm_name_id=milk_prod.farm_name_id,
        cow_id=milk_prod.cow_id,
        milk_production_data=jsonable_encoder(milk_prod.milk_production_data)
    )
    return response

class CreateTotalMilkRecord(CreateBase):
    milk_production_data: MilkProduction

@cow_card_router.post("/milk-production-total", response_model=ResponseModel)
def milk_Production_total(milk_prod: CreateTotalMilkRecord, db: Collection = Depends(get_farmer_collection)):
    logging.info(milk_prod.milk_production_data)
    response = add_milk_production_total(
        db,
        PhoneNumber=milk_prod.p_number,
        farm_name_id=milk_prod.farm_name_id,
        milk_production_data=jsonable_encoder(milk_prod.milk_production_data)
    )
    return response 



# ------------------ Health Records ----------------
class CreateVaccinationRc(CreateBase):
    cow_id: str
    v_records: VaccineRecord

@cow_card_router.post("/vaccine-record", response_model=ResponseModel)
def create_Vaccination_Rec(vacc_record: CreateVaccinationRc, db: Collection = Depends(get_farmer_collection)):

    logging.info("---------- List of milk production data ---------")
    logging.info(vacc_record.v_records)
    response = create_vaccination_history(
        db,
        PhoneNumber=vacc_record.p_number,
        farm_name_id=vacc_record.farm_name_id,
        cow_id=vacc_record.cow_id,
        vaccination_record=jsonable_encoder(vacc_record.v_records)
    )
    return response


class CreateCalvingRc(CreateBase):
    cow_id: str
    calf_record: CalvingEvent

@cow_card_router.post("/calving-record", response_model=ResponseModel)
def create_Calving_Rec(calf_records: CreateCalvingRc, db: Collection = Depends(get_farmer_collection)):
    logging.info("---------- List of milk production data ---------")
    logging.info(calf_records.calf_record)
    response = create_calving_history(
        db,
        PhoneNumber=calf_records.p_number,
        farm_name_id=calf_records.farm_name_id,
        cow_id=calf_records.cow_id,
        calving_info=jsonable_encoder(calf_records.calf_record)
    )
    return response
   
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
    create_milk_production_data,

    # ------------------ health
    create_vaccination_history,
)
from db.schemas.cow_card_schema import (
    IdentificationInfo,
    MilkProduction,
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
            response = create_cow_info(db,PhoneNumber=cow_info.p_number, farm_name_id=cow_info.farm_name_id, cow_data=jsonable_encoder(cow_info.cow_info))
            logging.info(response.dict())
            responses.append(jsonable_encoder(response))
    else:
        logging.info(cow_identity.cow_info.dict())
        response = create_cow_info(db, PhoneNumber=cow_identity.p_number, farm_name_id=cow_identity.farm_name_id, cow_data=jsonable_encoder(cow_identity.cow_info))
        logging.info(response.dict())
        responses.append(jsonable_encoder(response))
    return JSONResponse(responses[0])


class CreateVaccinationRecord(CreateBase):
    cow_id: str
    milk_production_data: List[MilkProduction]

@cow_card_router.post("/milk-production", response_model=Union[ResponseModel, ErrorResponseModel])
def createMilkProductionData(milk_prod: Union[CreateVaccinationRecord, List[CreateVaccinationRecord]], db: Collection = Depends(get_farmer_collection)):
    responses = []

    if isinstance(milk_prod, list):
        logging.info("---------- List of milk production data ---------")
        for milk_data in milk_prod:
            logging.info(milk_data.milk_production_data)
            response = create_milk_production_data(
                db,
                PhoneNumber=milk_data.p_number,
                farm_name_id=milk_data.farm_name_id,
                cow_id=milk_data.cow_id,
                milk_production_data=jsonable_encoder(milk_data.milk_production_data)
            )
            responses.append(jsonable_encoder(response))
    else:
        logging.info(milk_prod.milk_production_data)
        response = create_milk_production_data(
            db,
            PhoneNumber=milk_prod.p_number,
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
class CreateMilkProduction(CreateBase):
    cow_id: str
    v_records: List[VaccineRecord]

@cow_card_router.post("/vaccine-record", response_model=Union[ResponseModel, ErrorResponseModel])
def createVaccinationRec(vacc_record: Union[CreateMilkProduction, List[CreateMilkProduction]], db: Collection = Depends(get_farmer_collection)):
    responses = []

    if isinstance(vacc_record, list):
        logging.info("---------- List of milk production data ---------")
        for v_rec in vacc_record:
            logging.info(v_rec.v_records)
            response = create_vaccination_history(
                db,
                PhoneNumber=v_rec.p_number,
                farm_name_id=v_rec.farm_name_id,
                cow_id=v_rec.cow_id,
                vaccination_record=jsonable_encoder(v_rec.v_records)
            )
            responses.append(jsonable_encoder(response))
    else:
        logging.info(vacc_record.v_records)
        response = create_vaccination_history(
            db,
            PhoneNumber=vacc_record.p_number,
            farm_name_id=vacc_record.farm_name_id,
            cow_id=vacc_record.cow_id,
            vaccination_record=jsonable_encoder(vacc_record.v_records)
        )
        logging.info(response.dict())
        responses.append(jsonable_encoder(response))

    if isinstance(responses[0], ErrorResponseModel):
        return JSONResponse(content=jsonable_encoder(responses[0]))
    else:
        return JSONResponse(content=jsonable_encoder(responses[0]))
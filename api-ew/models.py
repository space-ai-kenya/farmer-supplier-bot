from typing import List, Optional
from pydantic import BaseModel,Field,validator
from datetime import datetime
from typing import Any

class MilkProduction(BaseModel):
    collection_date: Optional[str]
    collection_amount: Optional[int]
    variance: Optional[int]

    @validator('collection_date')
    def validate_date(cls, v):
        if v is not None:
            try:
                datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        return v

class LivestockDetails(BaseModel):
    numberOfCows: Optional[int]
    milkProduction: Optional[List[MilkProduction]]

class FarmingDetails(BaseModel):
    typeOfFarming: Optional[str]
    livestockDetails: Optional[LivestockDetails]

class FarmerCard(BaseModel):
    farmingDetails: Optional[FarmingDetails]
  
class FarmerSchema(BaseModel):
    f_uuid: Optional[str]
    PhoneNumber: Optional[str]
    farmer_Card: Optional[FarmerCard]

    class Config:
        schema_extra = {
            "example": {
                "f_uuid": "123456aseavadve",
                "PhoneNumber": "+25474567890",
                "farmer_Card": {
                    "farmingDetails": {
                        "typeOfFarming": "Organic",
                        "livestockDetails": {
                            "numberOfCows": 50,
                            "milkProduction": [
                                {
                                    "collection_date": "2024-03-18",
                                    "collection_amount": 100,
                                    "variance": 5
                                },
                                {
                                    "collection_date": "2024-03-17",
                                    "collection_amount": 110,
                                    "variance": 8
                                }
                            ]
                        }
                    }
                }
            }
        }

# ---------------------------------------------------- update models
class UpdateMilkProduction(BaseModel):
    collection_date: Optional[str] = Field(None, description="Date of milk collection")
    collection_amount: Optional[int] = Field(None, description="Amount of milk collected")
    variance: Optional[int] = Field(None, description="Variance in milk production")

class UpdateLivestockDetails(BaseModel):
    numberOfCows: Optional[int] = Field(None, description="Number of cows")
    milkProduction: Optional[List[UpdateMilkProduction]] = Field(None, description="List of milk production data")

class UpdateFarmingDetails(BaseModel):
    typeOfFarming: Optional[str] = Field(None, description="Type of farming")
    livestockDetails: Optional[UpdateLivestockDetails] = Field(None, description="Details of livestock")

class UpdateFarmerCard(BaseModel):
    farmingDetails: Optional[UpdateFarmingDetails] = Field(None, description="Details of farming")

class UpdateFarmer(BaseModel):
    f_uuid: Optional[str] = Field(None, description="UUID of the farmer")
    PhoneNumber: Optional[str] = Field(None, description="Phone number of the farmer")
    farmer_Card: Optional[UpdateFarmerCard] = Field(None, description="Card details of the farmer")



class ResponseModel(BaseModel):
    data: Any
    code: int
    message: str

class ErrorResponseModel(BaseModel):
    error: str
    code: int
    message: str
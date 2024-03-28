from typing import List, Optional
from pydantic import BaseModel,Field,validator
from datetime import datetime
from typing import Any
import re 


class MilkProduction(BaseModel):
    collection_date: Optional[str]
    collection_amount: Optional[int]
    variance: Optional[int]

    @validator('collection_date')
    def validate_date(cls, v):
        if v is not None or '':
            try:
                datetime.strptime(v, '%Y-%m-%d')
                return v
            except ValueError:
                raise ValueError("Incorrect data format, should be YYYY-MM-DD")
   


class CropDetails(BaseModel):
    mainCrop: Optional[str]
    rotationCrops: Optional[List[str]]

class Vaccination(BaseModel):
    vaccine_name: str
    vaccination_date: str
    dosage: float
    cow_id: str

class LivestockDetails(BaseModel):
    numberOfCows: Optional[int]
    milkProduction: Optional[List[MilkProduction]]
    vaccinations: Optional[List[Vaccination]]
    
class FarmingDetails(BaseModel):
    typeOfFarming: Optional[str]
    farmSize: Optional[int]
    cropDetails: Optional[CropDetails]
    livestockDetails: Optional[LivestockDetails]

class LandAndSoilInformation(BaseModel):
    soilType: Optional[str]
    irrigationMethods: Optional[str]
    landTopography: Optional[str]

class FarmingPractices(BaseModel):
    cropRotationSchedule: Optional[str]
    fertilizerUsage: Optional[str]
    pestControlMethods: Optional[str]

class FinancialInformation(BaseModel):
    incomeSources: Optional[List[str]]
    expenses: Optional[List[str]]
    investments: Optional[List[str]]

class Infrastructure(BaseModel):
    equipmentOwned: Optional[List[str]]
    farmBuildings: Optional[List[str]]
    storageFacilities: Optional[List[str]]

class ChallengesAndConcerns(BaseModel):
    currentChallenges: Optional[List[str]]
    futureConcerns: Optional[List[str]]

class GovernmentAssistanceAndSubsidies(BaseModel):
    availedSubsidies: Optional[List[str]]
    governmentSchemesUtilized: Optional[List[str]]

class TrainingAndEducation(BaseModel):
    workshopsTrainingAttended: Optional[List[str]]
    educationalBackground: Optional[str]

class UpdatesAndNotes(BaseModel):
    recordOfVisits: Optional[List[str]]
    notableChangesEvents: Optional[List[str]]

class NextStepsAndRecommendations(BaseModel):
    futurePlans: Optional[str]
    recommendationsForImprovement: Optional[str]

class FarmerCard(BaseModel):
    farmingDetails: Optional[FarmingDetails]
    landAndSoilInformation: Optional[LandAndSoilInformation]
    farmingPractices: Optional[FarmingPractices]
    financialInformation: Optional[FinancialInformation]
    infrastructure: Optional[Infrastructure]
    challengesAndConcerns: Optional[ChallengesAndConcerns]
    governmentAssistanceAndSubsidies: Optional[GovernmentAssistanceAndSubsidies]
    trainingAndEducation: Optional[TrainingAndEducation]
    updatesAndNotes: Optional[UpdatesAndNotes]
    nextStepsAndRecommendations: Optional[NextStepsAndRecommendations]

class FarmerSchema(BaseModel):
    f_uuid: Optional[str]
    PhoneNumber: Optional[str]
    farmer_Card: FarmerCard

    # @validator('f_uuid')
    # def validate_uuid(cls, v):
    #     if v is not None:
    #         uuid_pattern = re.compile(
    #             r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$'
    #         )
    #         if not uuid_pattern.match(v):
    #             raise ValueError('Not a valid UUIDv4')
    #     return v

    # @validator('PhoneNumber')
    # def validate_phone_number(cls, v):
    #     if v is not None:
    #         phone_pattern = re.compile(
    #             r'^\+?[0-9]{1,3}[- ]?\(?[0-9]{3}\)?[- ]?[0-9]{3}[- ]?[0-9]{4}$'
    #         )
    #         if not phone_pattern.match(v):
    #             raise ValueError('Not a valid phone number')
    #     return v



class ResponseModel(BaseModel):
    data: Any
    code: int
    message: str

class ErrorResponseModel(BaseModel):
    error: str
    code: int
    message: str
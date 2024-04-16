from typing import List, Optional
from pydantic import BaseModel

class MilkProduction(BaseModel):
    collection_date: Optional[str]
    collection_amount: Optional[int]
    variance: Optional[int]

# class CropDetails(BaseModel):
#     mainCrop: Optional[str]
#     rotationCrops: Optional[List[str]]

class LivestockDetails(BaseModel):
    numberOfCows: Optional[int]
    milkProduction: Optional[List[MilkProduction]]

class FarmingDetails(BaseModel):
    typeOfFarming: Optional[str]
    # farmSize: Optional[int]
    # cropDetails: Optional[CropDetails]
    livestockDetails: Optional[LivestockDetails]

# class LandAndSoilInformation(BaseModel):
#     soilType: Optional[str]
#     irrigationMethods: Optional[str]
#     landTopography: Optional[str]

# class FarmingPractices(BaseModel):
#     cropRotationSchedule: Optional[str]
#     fertilizerUsage: Optional[str]
#     pestControlMethods: Optional[str]

# class FinancialInformation(BaseModel):
#     incomeSources: Optional[List[str]]
#     expenses: Optional[List[str]]
#     investments: Optional[List[str]]

# class Infrastructure(BaseModel):
#     equipmentOwned: Optional[List[str]]
#     farmBuildings: Optional[List[str]]
#     storageFacilities: Optional[List[str]]

# class ChallengesAndConcerns(BaseModel):
#     currentChallenges: Optional[List[str]]
#     futureConcerns: Optional[List[str]]

# class GovernmentAssistanceAndSubsidies(BaseModel):
#     availedSubsidies: Optional[List[str]]
#     governmentSchemesUtilized: Optional[List[str]]

# class TrainingAndEducation(BaseModel):
#     workshopsTrainingAttended: Optional[List[str]]
#     educationalBackground: Optional[str]

# class UpdatesAndNotes(BaseModel):
#     recordOfVisits: Optional[List[str]]
#     notableChangesEvents: Optional[List[str]]

# class NextStepsAndRecommendations(BaseModel):
#     futurePlans: Optional[str]
#     recommendationsForImprovement: Optional[str]

class FarmerCard(BaseModel):
    farmingDetails: Optional[FarmingDetails]
    # landAndSoilInformation: Optional[LandAndSoilInformation]
    # farmingPractices: Optional[FarmingPractices]
    # financialInformation: Optional[FinancialInformation]
    # infrastructure: Optional[Infrastructure]
    # challengesAndConcerns: Optional[ChallengesAndConcerns]
    # governmentAssistanceAndSubsidies: Optional[GovernmentAssistanceAndSubsidies]
    # trainingAndEducation: Optional[TrainingAndEducation]
    # updatesAndNotes: Optional[UpdatesAndNotes]
    # nextStepsAndRecommendations: Optional[NextStepsAndRecommendations]

class FarmerSchema(BaseModel):
    f_uuid: Optional[str]
    PhoneNumber: Optional[str]
    farmer_Card: Optional[FarmerCard]

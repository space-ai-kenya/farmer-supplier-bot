from typing import List, Optional
from pydantic import BaseModel,validator
from datetime import datetime

class Record(BaseModel):
    date: str 
    value: str

class IdentificationInfo(BaseModel):
    unique_id: str  # Unique identification number or RFID tag

class HealthEvent(BaseModel):
    event_type: str
    event_date: str

class Calf(BaseModel):
    sex: Optional[str]
    birth_weight: Optional[float]
    weight_record: Optional[List[Record]]
    # https://www.facebook.com/Africanfarmresourcecentre/posts/estimating-the-weight-of-a-cow-using-the-tape-methodthe-tape-has-a-fairly-good-a/2422080981393790/

class ReproductiveHealth(BaseModel):
    heat_cycles: List[str]
    breeding_dates: List[str]
    pregnancy_status: str
    calving_history: List[str]

class MilkComponent(BaseModel):
    fat: Optional[float]
    protein: Optional[float]
    lactose: Optional[float]
    solids_not_fat: Optional[float]
    total_solids: Optional[float]

class MilkHealthReport(BaseModel):
    somatic_cell_count: Optional[int]
    milk_components: Optional[MilkComponent]
    fat_percentage: Optional[float]
    protein_percentage: Optional[float]

    # @validator('fat_percentage', 'protein_percentage')
    # def check_percentage(cls, v):
    #     if v < 0 or v > 100:
    #         raise ValueError('Percentage must be between 0 and 100')
    #     return v

class MilkProduction(BaseModel):
    milking_date: Optional[str]
    milk_yield: Optional[float]
    variance: Optional[float]
    milk_health: Optional[MilkHealthReport]


class FeedingAndNutrition(BaseModel):
    feed_intake: Optional[float]
    supplements: Optional[List[str]]
    body_condition_score: Optional[float]


class CalvingInformation(BaseModel):
    date: Optional[str]
    sex: Optional[str]
    tag: Optional[str]
    weight: Optional[str]


class TreatmentRecord(BaseModel):
    medication: Optional[str]
    dosage: Optional[str]
    withdrawal_period: Optional[str]
    health_event: Optional[str]

class LaboratoryResults(BaseModel):
    blood_tests: Optional[List[str]]
    culture_sensitivity_tests: Optional[List[str]]

class BodyMeasurements(BaseModel):
    body_weight: Optional[float]
    body_measurements: Optional[dict]  # height, length, etc.

class BehavioralObservations(BaseModel):
    lameness: Optional[str]
    aggression: Optional[str]

class EnvironmentalData(BaseModel):
    housing_conditions: Optional[str]
    climate: Optional[dict]  # temperature, humidity, ventilation, etc.

class CowCard(BaseModel):
    identification_info: IdentificationInfo
    health_records: Optional[List[HealthEvent]]
    reproductive_records: Optional[ReproductiveHealth]
    milk_production_data: Optional[List[MilkProduction]]
    feeding_and_nutrition: Optional[FeedingAndNutrition]
    calving_information: Optional[CalvingInformation]
    treatment_records: Optional[List[TreatmentRecord]]
    laboratory_results: Optional[LaboratoryResults]
    body_measurements: Optional[BodyMeasurements]
    behavioral_observations: Optional[BehavioralObservations]
    environmental_data: Optional[EnvironmentalData]
from typing import List, Optional
from datetime import date
from pydantic import BaseModel

class PlantingDetails(BaseModel):
    crop_name: str
    variety: str
    planting_date: date
    expected_harvest_date: date
    actual_harvest_date: Optional[date]
    planted_area: float
    yield_per_acre: Optional[float]

class IrrigationRecord(BaseModel):
    date: date
    duration: float
    amount: float

class FertilizerRecord(BaseModel):
    date: date
    fertilizer_type: str
    amount: float

class PestManagementRecord(BaseModel):
    date: date
    activity_type: str
    description: str

class CropManagementRecord(BaseModel):
    activity_date: date
    activity_type: str
    description: str

class HarvestDetails(BaseModel):
    start_date: date
    end_date: date
    num_harvests: int
    average_yield_per_harvest: float

class YieldRecord(BaseModel):
    harvest_details: HarvestDetails
    total_yield: float
    marketable_yield: float
    waste_or_loss: float
    quality_assessment: Optional[str]

class CropCard(BaseModel):
    field_id: str
    crop_year: int
    planting_details: Optional[List[PlantingDetails]]
    crop_management_records: Optional[List[CropManagementRecord]]
    yield_records: Optional[List[YieldRecord]]
    irrigation_records: Optional[List[IrrigationRecord]]
    fertilizer_records: Optional[List[FertilizerRecord]]
    pest_management_records: Optional[List[PestManagementRecord]]
    notes: Optional[List[str]]
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class ExpenseItem(BaseModel):
    description: str
    amount: float

class DailyExpense(BaseModel):
    date: date
    expenses: List[ExpenseItem]

class SavingsPlanExpense(BaseModel):
    description: str
    planned_amount: float

class MonthlySavingsPlan(BaseModel):
    month: str  # Format "YYYY-MM"
    expenses: List[SavingsPlanExpense]
    budget: float
    actual_expenses: Optional[float] = 0.0

class IncomeExpenditurePlan(BaseModel):
    month: str  # Format "YYYY-MM"
    total_budget: float
    farm_sales: float
    expenses: float
    profit_loss: Optional[float] = 0.0 
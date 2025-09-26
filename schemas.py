from pydantic import BaseModel
from datetime import date
from typing import Optional

class IncomeReport(BaseModel):
    total_income: float
    breakdown: dict
    payment_status: dict

class ExpensesReport(BaseModel):
    total_expenses: float
    breakdown: dict

class OccupancyReport(BaseModel):
    current_rate: float
    historical_trends: list

class ComplaintsReport(BaseModel):
    total_complaints: int
    resolved: int
    pending: int
    avg_resolution_days: Optional[float]
    categorization: dict

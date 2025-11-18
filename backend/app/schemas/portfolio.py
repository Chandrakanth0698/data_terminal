"""
Portfolio Pydantic schemas
"""
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class PortfolioCreate(BaseModel):
    """Portfolio creation schema"""
    name: str
    description: Optional[str] = None


class PortfolioResponse(BaseModel):
    """Portfolio response schema"""
    id: int
    name: str
    description: Optional[str]
    total_value: Optional[float]
    total_invested: Optional[float]
    total_return: Optional[float]
    return_percentage: Optional[float]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HoldingCreate(BaseModel):
    """Holding creation schema"""
    company_id: int
    quantity: float
    average_price: float

"""
Company Pydantic schemas
"""
from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, List
from datetime import datetime


class CompanyBase(BaseModel):
    """Base company schema"""
    symbol: str
    name: str
    exchange: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None


class CompanyResponse(CompanyBase):
    """Company response schema"""
    id: int
    isin: Optional[str] = None
    market_cap: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class CompanyDetail(CompanyBase):
    """Detailed company schema"""
    id: int
    isin: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    headquarters: Optional[str] = None
    founded_year: Optional[int] = None
    employees: Optional[int] = None
    market_cap: Optional[float] = None
    shares_outstanding: Optional[float] = None
    revenue_segments: Optional[Dict] = None
    geographic_breakdown: Optional[Dict] = None
    ceo: Optional[str] = None
    cfo: Optional[str] = None
    management: Optional[List] = None
    peers: Optional[List] = None
    is_active: int
    listing_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

"""
Research Notes Pydantic schemas
"""
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class ResearchNoteCreate(BaseModel):
    """Research note creation schema"""
    company_id: int
    title: str
    content: Optional[str] = None
    thesis_type: Optional[str] = None
    investment_horizon: Optional[str] = None
    confidence_level: Optional[int] = None
    strengths: Optional[List] = None
    weaknesses: Optional[List] = None
    opportunities: Optional[List] = None
    threats: Optional[List] = None
    fair_value_estimate: Optional[float] = None
    valuation_method: Optional[str] = None
    tags: Optional[str] = None


class ResearchNoteResponse(BaseModel):
    """Research note response schema"""
    id: int
    company_id: int
    title: str
    content: Optional[str]
    thesis_type: Optional[str]
    investment_horizon: Optional[str]
    confidence_level: Optional[int]
    fair_value_estimate: Optional[float]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

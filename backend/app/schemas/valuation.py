"""
Valuation Pydantic schemas
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict
from datetime import datetime


class DCFRequest(BaseModel):
    """DCF model creation request"""
    model_name: Optional[str] = None
    projection_years: int = Field(5, ge=1, le=10)
    revenue_growth_rate: float = Field(..., description="Revenue growth rate (%)")
    operating_margin: float = Field(..., description="Operating margin (%)")
    tax_rate: float = Field(..., description="Tax rate (%)")
    capex_percentage: float = Field(..., description="CapEx as % of revenue")
    nwc_percentage: float = Field(..., description="NWC as % of revenue")
    terminal_growth_rate: float = Field(..., description="Terminal growth rate (%)")
    wacc: float = Field(..., description="WACC (%)")


class DCFResponse(BaseModel):
    """DCF model response"""
    id: int
    company_id: int
    model_name: str
    projection_years: int
    revenue_growth_rate: float
    operating_margin: float
    tax_rate: float
    capex_percentage: float
    nwc_percentage: float
    terminal_growth_rate: float
    wacc: float
    intrinsic_value_per_share: Optional[float]
    current_price: Optional[float]
    upside_downside: Optional[float]
    projections: Optional[Dict]
    sensitivity_table: Optional[Dict]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

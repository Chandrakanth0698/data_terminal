"""
Screener Pydantic schemas
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional


class ScreenRequest(BaseModel):
    """Stock screen request"""
    filters: Dict[str, Any] = Field(..., description="Filter criteria")
    limit: int = Field(100, ge=1, le=500)
    offset: int = Field(0, ge=0)


class StockResult(BaseModel):
    """Individual stock result"""
    symbol: str
    name: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    roe: Optional[float] = None
    debt_to_equity: Optional[float] = None
    revenue_growth_3y_cagr: Optional[float] = None


class ScreenResponse(BaseModel):
    """Stock screen response"""
    results: List[Dict[str, Any]]
    total_count: int
    limit: int
    offset: int
    filters: Dict[str, Any]
    execution_time_ms: float
    timestamp: str


class PresetScreensResponse(BaseModel):
    """Preset screens response"""
    presets: Dict[str, Any]

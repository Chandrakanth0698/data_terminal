"""
Financial Analysis Pydantic schemas
"""
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class FinancialStatementResponse(BaseModel):
    """Financial statement response"""
    id: int
    period_end: datetime
    period_type: str
    fiscal_year: int
    fiscal_quarter: Optional[int]
    statement_type: str

    # Income Statement
    revenue: Optional[float]
    gross_profit: Optional[float]
    operating_income: Optional[float]
    net_income: Optional[float]
    eps: Optional[float]

    # Balance Sheet
    total_assets: Optional[float]
    total_liabilities: Optional[float]
    shareholders_equity: Optional[float]

    # Cash Flow
    operating_cash_flow: Optional[float]
    free_cash_flow: Optional[float]

    model_config = ConfigDict(from_attributes=True)


class RatioResponse(BaseModel):
    """Financial ratio response"""
    id: int
    period_end: datetime

    # Profitability
    roe: Optional[float]
    roa: Optional[float]
    roic: Optional[float]
    gross_margin: Optional[float]
    operating_margin: Optional[float]
    net_margin: Optional[float]

    # Valuation
    pe_ratio: Optional[float]
    pb_ratio: Optional[float]
    ps_ratio: Optional[float]
    ev_ebitda: Optional[float]

    # Liquidity
    current_ratio: Optional[float]
    quick_ratio: Optional[float]

    # Solvency
    debt_to_equity: Optional[float]
    interest_coverage: Optional[float]

    # Growth
    revenue_growth_yoy: Optional[float]
    earnings_growth_yoy: Optional[float]

    model_config = ConfigDict(from_attributes=True)

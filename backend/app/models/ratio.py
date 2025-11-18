"""
Financial ratios model - Calculated metrics
"""
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Ratio(Base):
    """Financial ratios and metrics"""

    __tablename__ = "ratios"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    # Period
    period_end = Column(DateTime, nullable=False, index=True)
    period_type = Column(String(20))  # Annual, Quarterly, TTM

    # Profitability Ratios
    gross_margin = Column(Float)
    operating_margin = Column(Float)
    net_margin = Column(Float)
    roe = Column(Float)  # Return on Equity
    roa = Column(Float)  # Return on Assets
    roic = Column(Float)  # Return on Invested Capital
    roce = Column(Float)  # Return on Capital Employed

    # Liquidity Ratios
    current_ratio = Column(Float)
    quick_ratio = Column(Float)
    cash_ratio = Column(Float)

    # Solvency Ratios
    debt_to_equity = Column(Float)
    debt_to_assets = Column(Float)
    interest_coverage = Column(Float)

    # Efficiency Ratios
    asset_turnover = Column(Float)
    inventory_turnover = Column(Float)
    receivables_turnover = Column(Float)
    days_sales_outstanding = Column(Float)
    days_inventory_outstanding = Column(Float)

    # Valuation Ratios
    pe_ratio = Column(Float)
    pb_ratio = Column(Float)
    ps_ratio = Column(Float)
    ev_ebitda = Column(Float)
    peg_ratio = Column(Float)

    # Growth Metrics
    revenue_growth_yoy = Column(Float)
    earnings_growth_yoy = Column(Float)
    fcf_growth_yoy = Column(Float)
    revenue_growth_3y_cagr = Column(Float)
    revenue_growth_5y_cagr = Column(Float)
    earnings_growth_3y_cagr = Column(Float)
    earnings_growth_5y_cagr = Column(Float)

    # Other Metrics
    dividend_yield = Column(Float)
    payout_ratio = Column(Float)
    retention_ratio = Column(Float)

    # Quality Metrics
    altman_z_score = Column(Float)
    piotroski_f_score = Column(Float)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="ratios")

    # Indexes
    __table_args__ = (
        Index('ix_ratios_company_period', 'company_id', 'period_end'),
    )

    def __repr__(self):
        return f"<Ratio(company_id={self.company_id}, period={self.period_end})>"

"""
Analyst estimate model - Consensus estimates
"""
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class AnalystEstimate(Base):
    """Analyst consensus estimates"""

    __tablename__ = "analyst_estimates"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    # Period
    fiscal_year = Column(Integer, nullable=False, index=True)
    fiscal_quarter = Column(Integer)  # None for annual estimates

    # Revenue estimates
    revenue_mean = Column(Float)
    revenue_median = Column(Float)
    revenue_high = Column(Float)
    revenue_low = Column(Float)
    revenue_num_analysts = Column(Integer)

    # Earnings estimates
    eps_mean = Column(Float)
    eps_median = Column(Float)
    eps_high = Column(Float)
    eps_low = Column(Float)
    eps_num_analysts = Column(Integer)

    # EBITDA estimates
    ebitda_mean = Column(Float)
    ebitda_median = Column(Float)

    # Recommendations
    strong_buy = Column(Integer)
    buy = Column(Integer)
    hold = Column(Integer)
    sell = Column(Integer)
    strong_sell = Column(Integer)

    # Target price
    target_price_mean = Column(Float)
    target_price_median = Column(Float)
    target_price_high = Column(Float)
    target_price_low = Column(Float)

    # Metadata
    estimate_date = Column(DateTime, nullable=False)  # When estimate was made
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="analyst_estimates")

    # Indexes
    __table_args__ = (
        Index('ix_analyst_estimates_company_year', 'company_id', 'fiscal_year'),
    )

    def __repr__(self):
        return f"<AnalystEstimate(company_id={self.company_id}, FY{self.fiscal_year})>"

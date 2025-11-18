"""
DCF model - Valuation models
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class DCFModel(Base):
    """DCF valuation models"""

    __tablename__ = "dcf_models"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    # Model details
    model_name = Column(String(200))

    # Assumptions
    projection_years = Column(Integer, default=5)
    revenue_growth_rate = Column(Float)  # %
    operating_margin = Column(Float)  # %
    tax_rate = Column(Float)  # %
    capex_percentage = Column(Float)  # % of revenue
    nwc_percentage = Column(Float)  # % of revenue
    terminal_growth_rate = Column(Float)  # %
    wacc = Column(Float)  # Weighted Average Cost of Capital

    # Results
    intrinsic_value_per_share = Column(Float)
    current_price = Column(Float)
    upside_downside = Column(Float)  # %

    # Projections (JSON)
    projections = Column(JSON)  # Year-by-year projections

    # Sensitivity analysis (JSON)
    sensitivity_table = Column(JSON)  # WACC vs Terminal Growth

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User")
    company = relationship("Company")

    # Indexes
    __table_args__ = (
        Index('ix_dcf_models_user_company', 'user_id', 'company_id'),
    )

    def __repr__(self):
        return f"<DCFModel(company_id={self.company_id}, intrinsic_value={self.intrinsic_value_per_share})>"

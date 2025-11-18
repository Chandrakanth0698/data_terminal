"""
Earnings call model - Transcript storage
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class EarningsCall(Base):
    """Earnings call transcripts"""

    __tablename__ = "earnings_calls"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    # Call info
    fiscal_year = Column(Integer, nullable=False)
    fiscal_quarter = Column(Integer, nullable=False)
    call_date = Column(DateTime, nullable=False, index=True)

    # Content
    transcript = Column(Text)
    summary = Column(Text)

    # Extracted insights (JSON)
    guidance = Column(JSON)  # Future outlook provided by management
    key_points = Column(JSON)  # List of key discussion points
    questions = Column(JSON)  # Analyst questions
    management_commentary = Column(JSON)  # Key statements by management

    # Sentiment analysis
    sentiment_score = Column(Float)
    sentiment_label = Column(String(20))

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="earnings_calls")

    # Indexes
    __table_args__ = (
        Index('ix_earnings_calls_company_date', 'company_id', 'call_date'),
    )

    def __repr__(self):
        return f"<EarningsCall(company_id={self.company_id}, FY{self.fiscal_year}Q{self.fiscal_quarter})>"

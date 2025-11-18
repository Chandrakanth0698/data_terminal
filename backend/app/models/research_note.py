"""
Research note model - User research documentation
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class ResearchNote(Base):
    """User research notes"""

    __tablename__ = "research_notes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    # Note details
    title = Column(String(200), nullable=False)
    content = Column(Text)

    # Investment thesis
    thesis_type = Column(String(50))  # Bull, Bear, Neutral
    investment_horizon = Column(String(20))  # Short, Medium, Long
    confidence_level = Column(Integer)  # 1-5

    # SWOT analysis (JSON)
    strengths = Column(JSON)
    weaknesses = Column(JSON)
    opportunities = Column(JSON)
    threats = Column(JSON)

    # Valuation
    fair_value_estimate = Column(Float)
    valuation_method = Column(String(50))  # DCF, PE Multiple, etc.

    # Tags
    tags = Column(String(500))

    # Reminders
    reminder_date = Column(DateTime)
    reminder_note = Column(Text)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="research_notes")
    company = relationship("Company")

    # Indexes
    __table_args__ = (
        Index('ix_research_notes_user_company', 'user_id', 'company_id'),
    )

    def __repr__(self):
        return f"<ResearchNote(user_id={self.user_id}, title={self.title})>"

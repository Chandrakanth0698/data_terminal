"""
Watchlist model - User watchlists
"""
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Watchlist(Base):
    """User watchlists"""

    __tablename__ = "watchlists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    # Entry details
    added_price = Column(Float)
    target_price = Column(Float)
    stop_loss = Column(Float)

    # User notes
    rationale = Column(Text)
    tags = Column(String(500))  # Comma-separated: value,growth,dividend

    # Status
    status = Column(String(20), default="watching")  # watching, bought, passed

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="watchlists")
    company = relationship("Company")

    # Indexes
    __table_args__ = (
        Index('ix_watchlists_user_company', 'user_id', 'company_id'),
    )

    def __repr__(self):
        return f"<Watchlist(user_id={self.user_id}, company_id={self.company_id})>"

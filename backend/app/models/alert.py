"""
Alert model - User alerts and notifications
"""
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Index, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Alert(Base):
    """User alerts and notifications"""

    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    # Alert type
    alert_type = Column(String(50), nullable=False, index=True)
    # Types: price_above, price_below, pe_below, roe_above,
    #        earnings_date, ex_dividend_date, news_keyword, etc.

    # Conditions
    condition_field = Column(String(50))  # price, pe_ratio, roe, etc.
    condition_operator = Column(String(10))  # >, <, >=, <=, ==
    condition_value = Column(Float)

    # For keyword alerts
    keywords = Column(String(500))

    # Alert details
    title = Column(String(200))
    message = Column(Text)

    # Status
    is_active = Column(Boolean, default=True)
    is_triggered = Column(Boolean, default=False)
    triggered_at = Column(DateTime)
    triggered_value = Column(Float)

    # Notification preferences
    notify_email = Column(Boolean, default=True)
    notify_app = Column(Boolean, default=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = Column(DateTime)  # Optional expiration

    # Relationships
    user = relationship("User", back_populates="alerts")
    company = relationship("Company")

    # Indexes
    __table_args__ = (
        Index('ix_alerts_user_active', 'user_id', 'is_active'),
        Index('ix_alerts_company_active', 'company_id', 'is_active'),
    )

    def __repr__(self):
        return f"<Alert(user_id={self.user_id}, type={self.alert_type}, active={self.is_active})>"

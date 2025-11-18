"""
Stock price model - Time series price data
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class StockPrice(Base):
    """Stock price time series data"""

    __tablename__ = "stock_prices"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    # Date
    date = Column(DateTime, nullable=False, index=True)

    # OHLCV data
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)

    # Adjusted close (for splits, dividends)
    adj_close = Column(Float)

    # Additional metrics
    vwap = Column(Float)  # Volume-weighted average price
    delivery_percentage = Column(Float)  # NSE specific

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="stock_prices")

    # Composite index for efficient queries
    __table_args__ = (
        Index('ix_stock_prices_company_date', 'company_id', 'date'),
    )

    def __repr__(self):
        return f"<StockPrice(company_id={self.company_id}, date={self.date}, close={self.close})>"

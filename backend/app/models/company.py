"""
Company model - Master company data
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Company(Base):
    """Company master table"""

    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    isin = Column(String(12), unique=True, index=True)

    # Exchange info
    exchange = Column(String(10))  # NSE, BSE
    sector = Column(String(100), index=True)
    industry = Column(String(100), index=True)

    # Company details
    description = Column(Text)
    website = Column(String(200))
    headquarters = Column(String(200))
    founded_year = Column(Integer)
    employees = Column(Integer)

    # Market data
    market_cap = Column(Float)
    shares_outstanding = Column(Float)

    # Revenue breakdown (JSON)
    revenue_segments = Column(JSON)  # {"Product A": 40%, "Product B": 60%}
    geographic_breakdown = Column(JSON)  # {"India": 70%, "Export": 30%}

    # Key people
    ceo = Column(String(100))
    cfo = Column(String(100))
    management = Column(JSON)  # List of key management

    # Peers
    peers = Column(JSON)  # List of peer company symbols

    # Status
    is_active = Column(Integer, default=1)
    listing_date = Column(DateTime)
    delisting_date = Column(DateTime, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_synced = Column(DateTime)

    # Relationships
    stock_prices = relationship("StockPrice", back_populates="company", cascade="all, delete-orphan")
    financial_statements = relationship("FinancialStatement", back_populates="company", cascade="all, delete-orphan")
    ratios = relationship("Ratio", back_populates="company", cascade="all, delete-orphan")
    news = relationship("News", back_populates="company", cascade="all, delete-orphan")
    earnings_calls = relationship("EarningsCall", back_populates="company", cascade="all, delete-orphan")
    analyst_estimates = relationship("AnalystEstimate", back_populates="company", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Company(symbol={self.symbol}, name={self.name})>"

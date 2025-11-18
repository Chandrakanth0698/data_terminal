"""
Portfolio models - Portfolio tracking
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Portfolio(Base):
    """User portfolios"""

    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Portfolio details
    name = Column(String(200), nullable=False)
    description = Column(String(500))

    # Performance metrics (cached)
    total_value = Column(Float)
    total_invested = Column(Float)
    total_return = Column(Float)
    return_percentage = Column(Float)
    xirr = Column(Float)  # XIRR return

    # Risk metrics
    beta = Column(Float)
    alpha = Column(Float)
    sharpe_ratio = Column(Float)
    volatility = Column(Float)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="portfolios")
    holdings = relationship("PortfolioHolding", back_populates="portfolio", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Portfolio(name={self.name}, value={self.total_value})>"


class PortfolioHolding(Base):
    """Individual holdings in a portfolio"""

    __tablename__ = "portfolio_holdings"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    # Position details
    quantity = Column(Float, nullable=False)
    average_price = Column(Float, nullable=False)
    current_price = Column(Float)

    # Transactions (JSON) - for XIRR calculation
    transactions = Column(JSON)  # [{date, type, quantity, price}, ...]

    # Calculated metrics
    invested_value = Column(Float)
    current_value = Column(Float)
    unrealized_gain = Column(Float)
    unrealized_gain_percentage = Column(Float)
    realized_gain = Column(Float)

    # Dividends received
    total_dividends = Column(Float)

    # Metadata
    first_buy_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    portfolio = relationship("Portfolio", back_populates="holdings")
    company = relationship("Company")

    # Indexes
    __table_args__ = (
        Index('ix_portfolio_holdings_portfolio_company', 'portfolio_id', 'company_id'),
    )

    def __repr__(self):
        return f"<PortfolioHolding(portfolio_id={self.portfolio_id}, company_id={self.company_id}, qty={self.quantity})>"

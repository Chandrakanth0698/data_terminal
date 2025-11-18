"""
Financial statement model - Income, Balance Sheet, Cash Flow
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class FinancialStatement(Base):
    """Financial statements table"""

    __tablename__ = "financial_statements"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    # Period info
    period_end = Column(DateTime, nullable=False, index=True)
    period_type = Column(String(20), nullable=False)  # Annual, Quarterly
    fiscal_year = Column(Integer, nullable=False, index=True)
    fiscal_quarter = Column(Integer)  # 1, 2, 3, 4 for quarterly

    # Statement type
    statement_type = Column(String(20), nullable=False, index=True)  # Income, Balance, CashFlow

    # Income Statement
    revenue = Column(Float)
    cost_of_revenue = Column(Float)
    gross_profit = Column(Float)
    operating_expenses = Column(Float)
    operating_income = Column(Float)
    interest_expense = Column(Float)
    depreciation = Column(Float)
    ebitda = Column(Float)
    ebt = Column(Float)  # Earnings before tax
    tax_expense = Column(Float)
    net_income = Column(Float)
    eps = Column(Float)
    eps_diluted = Column(Float)

    # Balance Sheet
    cash = Column(Float)
    short_term_investments = Column(Float)
    accounts_receivable = Column(Float)
    inventory = Column(Float)
    current_assets = Column(Float)
    ppe = Column(Float)  # Property, Plant & Equipment
    intangible_assets = Column(Float)
    goodwill = Column(Float)
    total_assets = Column(Float)

    accounts_payable = Column(Float)
    short_term_debt = Column(Float)
    current_liabilities = Column(Float)
    long_term_debt = Column(Float)
    total_liabilities = Column(Float)

    common_stock = Column(Float)
    retained_earnings = Column(Float)
    shareholders_equity = Column(Float)

    # Cash Flow Statement
    operating_cash_flow = Column(Float)
    capex = Column(Float)
    investing_cash_flow = Column(Float)
    financing_cash_flow = Column(Float)
    free_cash_flow = Column(Float)
    dividends_paid = Column(Float)

    # Additional data (store as JSON for flexibility)
    additional_data = Column(JSON)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="financial_statements")

    # Composite indexes
    __table_args__ = (
        Index('ix_fin_stmt_company_period', 'company_id', 'period_end', 'statement_type'),
    )

    def __repr__(self):
        return f"<FinancialStatement(company_id={self.company_id}, period={self.period_end}, type={self.statement_type})>"

"""
Financial Analysis API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models import FinancialStatement, Ratio, Company
from app.schemas.financial import FinancialStatementResponse, RatioResponse

router = APIRouter()


@router.get("/{symbol}/statements")
def get_financial_statements(
    symbol: str,
    statement_type: Optional[str] = Query(None, description="Income, Balance, CashFlow"),
    period_type: Optional[str] = Query(None, description="Annual, Quarterly"),
    years: int = Query(10, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """Get financial statements for a company"""

    # Get company
    company = db.query(Company).filter(Company.symbol == symbol.upper()).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    # Build query
    query = db.query(FinancialStatement).filter(
        FinancialStatement.company_id == company.id
    )

    if statement_type:
        query = query.filter(FinancialStatement.statement_type == statement_type)

    if period_type:
        query = query.filter(FinancialStatement.period_type == period_type)

    statements = query.order_by(
        FinancialStatement.period_end.desc()
    ).limit(years * 4).all()  # 4 quarters per year

    return {
        "symbol": symbol,
        "statements": statements
    }


@router.get("/{symbol}/ratios")
def get_financial_ratios(
    symbol: str,
    years: int = Query(10, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """Get financial ratios for a company"""

    company = db.query(Company).filter(Company.symbol == symbol.upper()).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    ratios = db.query(Ratio).filter(
        Ratio.company_id == company.id
    ).order_by(
        Ratio.period_end.desc()
    ).limit(years * 4).all()

    return {
        "symbol": symbol,
        "ratios": ratios
    }


@router.get("/{symbol}/peer-comparison")
def get_peer_comparison(
    symbol: str,
    db: Session = Depends(get_db)
):
    """Compare company ratios with peers"""

    company = db.query(Company).filter(Company.symbol == symbol.upper()).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    # Get latest ratios for the company
    latest_ratio = db.query(Ratio).filter(
        Ratio.company_id == company.id
    ).order_by(Ratio.period_end.desc()).first()

    # Get peers (from company.peers JSON field)
    peer_symbols = company.peers or []

    # Get peer companies and their ratios
    peer_data = []
    for peer_symbol in peer_symbols[:10]:  # Limit to 10 peers
        peer_company = db.query(Company).filter(
            Company.symbol == peer_symbol
        ).first()

        if peer_company:
            peer_ratio = db.query(Ratio).filter(
                Ratio.company_id == peer_company.id
            ).order_by(Ratio.period_end.desc()).first()

            peer_data.append({
                "symbol": peer_company.symbol,
                "name": peer_company.name,
                "ratios": peer_ratio
            })

    return {
        "company": {
            "symbol": company.symbol,
            "name": company.name,
            "ratios": latest_ratio
        },
        "peers": peer_data
    }

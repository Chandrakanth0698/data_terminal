"""
Companies API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models import Company
from app.schemas.company import CompanyResponse, CompanyDetail

router = APIRouter()


@router.get("/search", response_model=List[CompanyResponse])
def search_companies(
    query: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Search companies by symbol or name"""
    companies = db.query(Company).filter(
        (Company.symbol.ilike(f"%{query}%")) |
        (Company.name.ilike(f"%{query}%"))
    ).filter(
        Company.is_active == 1
    ).limit(limit).all()

    return companies


@router.get("/{symbol}", response_model=CompanyDetail)
def get_company(
    symbol: str,
    db: Session = Depends(get_db)
):
    """Get company details by symbol"""
    company = db.query(Company).filter(
        Company.symbol == symbol.upper()
    ).first()

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    return company


@router.get("/sector/{sector}", response_model=List[CompanyResponse])
def get_companies_by_sector(
    sector: str,
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Get companies by sector"""
    companies = db.query(Company).filter(
        Company.sector == sector,
        Company.is_active == 1
    ).limit(limit).all()

    return companies


@router.get("/", response_model=List[CompanyResponse])
def list_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    exchange: Optional[str] = None,
    sector: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all active companies with optional filters"""
    query = db.query(Company).filter(Company.is_active == 1)

    if exchange:
        query = query.filter(Company.exchange == exchange)

    if sector:
        query = query.filter(Company.sector == sector)

    companies = query.offset(skip).limit(limit).all()
    return companies

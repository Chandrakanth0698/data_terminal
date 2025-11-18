"""
Valuation API endpoints - DCF and relative valuation
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.models import Company, DCFModel
from app.schemas.valuation import DCFRequest, DCFResponse
from app.api.endpoints.auth import get_current_user
from app.models import User

router = APIRouter()


@router.post("/{symbol}/dcf", response_model=DCFResponse)
def create_dcf_model(
    symbol: str,
    request: DCFRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a DCF valuation model

    This endpoint builds a Discounted Cash Flow model with the provided assumptions
    """
    company = db.query(Company).filter(Company.symbol == symbol.upper()).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    # Build DCF model using the assumptions
    # This is a placeholder - actual DCF calculation would go here
    from app.modules.valuation import DCFCalculator

    calculator = DCFCalculator(db)
    dcf_result = calculator.calculate_dcf(
        company_id=company.id,
        projection_years=request.projection_years,
        revenue_growth_rate=request.revenue_growth_rate,
        operating_margin=request.operating_margin,
        tax_rate=request.tax_rate,
        capex_percentage=request.capex_percentage,
        nwc_percentage=request.nwc_percentage,
        terminal_growth_rate=request.terminal_growth_rate,
        wacc=request.wacc
    )

    # Save model to database
    dcf_model = DCFModel(
        user_id=current_user.id,
        company_id=company.id,
        model_name=request.model_name or f"DCF_{symbol}_{datetime.now().strftime('%Y%m%d')}",
        **request.dict(),
        **dcf_result
    )

    db.add(dcf_model)
    db.commit()
    db.refresh(dcf_model)

    return dcf_model


@router.get("/{symbol}/dcf/{model_id}", response_model=DCFResponse)
def get_dcf_model(
    symbol: str,
    model_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a saved DCF model"""
    dcf_model = db.query(DCFModel).filter(
        DCFModel.id == model_id,
        DCFModel.user_id == current_user.id
    ).first()

    if not dcf_model:
        raise HTTPException(status_code=404, detail="DCF model not found")

    return dcf_model

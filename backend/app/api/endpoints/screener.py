"""
Stock Screener API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from app.core.database import get_db
from app.modules.screener import StockScreener
from app.schemas.screener import ScreenRequest, ScreenResponse, PresetScreensResponse

router = APIRouter()


@router.post("/screen", response_model=ScreenResponse)
def screen_stocks(
    request: ScreenRequest,
    db: Session = Depends(get_db)
):
    """
    Screen stocks based on filter criteria

    Example request body:
    {
        "filters": {
            "market_cap": {"min": 1000, "max": 50000},
            "pe_ratio": {"max": 25},
            "roe": {"min": 15},
            "debt_to_equity": {"max": 1}
        },
        "limit": 50,
        "offset": 0
    }
    """
    screener = StockScreener(db)
    result = screener.screen(
        filters=request.filters,
        limit=request.limit,
        offset=request.offset
    )
    return result


@router.get("/filters")
def get_available_filters(db: Session = Depends(get_db)):
    """Get all available filter fields"""
    screener = StockScreener(db)
    return {
        "filters": screener.get_available_filters()
    }


@router.get("/presets", response_model=PresetScreensResponse)
def get_preset_screens(db: Session = Depends(get_db)):
    """Get preset screening strategies"""
    screener = StockScreener(db)
    return {
        "presets": screener.get_preset_screens()
    }


@router.post("/presets/{preset_name}", response_model=ScreenResponse)
def run_preset_screen(
    preset_name: str,
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Run a preset screening strategy"""
    screener = StockScreener(db)
    presets = screener.get_preset_screens()

    if preset_name not in presets:
        raise HTTPException(status_code=404, detail="Preset not found")

    preset = presets[preset_name]
    result = screener.screen(
        filters=preset['filters'],
        limit=limit,
        offset=offset
    )
    return result

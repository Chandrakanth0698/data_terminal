"""
API router - Central router for all API endpoints
"""
from fastapi import APIRouter

from app.api.endpoints import (
    companies,
    screener,
    financial,
    valuation,
    portfolio,
    research,
    alerts,
    auth,
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(companies.router, prefix="/companies", tags=["Companies"])
api_router.include_router(screener.router, prefix="/screener", tags=["Stock Screener"])
api_router.include_router(financial.router, prefix="/financial", tags=["Financial Analysis"])
api_router.include_router(valuation.router, prefix="/valuation", tags=["Valuation"])
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["Portfolio"])
api_router.include_router(research.router, prefix="/research", tags=["Research Notes"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])

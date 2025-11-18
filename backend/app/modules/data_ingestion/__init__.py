"""
Data Ingestion Module - Fetch data from free sources
"""
from app.modules.data_ingestion.price_fetcher import PriceFetcher
from app.modules.data_ingestion.financial_fetcher import FinancialFetcher
from app.modules.data_ingestion.news_fetcher import NewsFetcher
from app.modules.data_ingestion.earnings_fetcher import EarningsFetcher

__all__ = [
    "PriceFetcher",
    "FinancialFetcher",
    "NewsFetcher",
    "EarningsFetcher",
]

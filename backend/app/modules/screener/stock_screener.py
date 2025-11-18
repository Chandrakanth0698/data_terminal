"""
Stock Screener - Filter stocks by multiple criteria
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import Dict, List, Optional, Any
import hashlib
import json
from datetime import datetime, timedelta
from loguru import logger

from app.models import Company, Ratio
from app.core.redis import cache


class StockScreener:
    """Stock screening engine"""

    def __init__(self, db: Session):
        self.db = db

    def screen(
        self,
        filters: Dict[str, Any],
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Screen stocks based on filter criteria

        Args:
            filters: Dictionary of filter criteria
                Example: {
                    'market_cap': {'min': 1000, 'max': 50000},
                    'pe_ratio': {'max': 25},
                    'roe': {'min': 15},
                    'sector': {'eq': 'Technology'}
                }
            limit: Maximum number of results
            offset: Offset for pagination

        Returns:
            Dictionary with results and metadata
        """
        try:
            start_time = datetime.now()

            # Generate cache key
            cache_key = self._generate_cache_key(filters, limit, offset)

            # Check cache
            cached_result = cache.get_screener_results(cache_key)
            if cached_result:
                logger.info(f"Returning cached screener results for key: {cache_key}")
                return cached_result

            # Build query
            query = self._build_query(filters)

            # Execute query with pagination
            total_count = query.count()
            results = query.offset(offset).limit(limit).all()

            # Format results
            formatted_results = []
            for company, ratio in results:
                formatted_results.append({
                    'symbol': company.symbol,
                    'name': company.name,
                    'sector': company.sector,
                    'industry': company.industry,
                    'market_cap': company.market_cap,
                    'pe_ratio': ratio.pe_ratio if ratio else None,
                    'pb_ratio': ratio.pb_ratio if ratio else None,
                    'roe': ratio.roe if ratio else None,
                    'debt_to_equity': ratio.debt_to_equity if ratio else None,
                    'revenue_growth_3y_cagr': ratio.revenue_growth_3y_cagr if ratio else None,
                })

            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            result = {
                'results': formatted_results,
                'total_count': total_count,
                'limit': limit,
                'offset': offset,
                'filters': filters,
                'execution_time_ms': execution_time,
                'timestamp': datetime.now().isoformat()
            }

            # Cache results
            cache.set_screener_results(cache_key, result, ttl=3600)

            logger.info(f"Screener found {total_count} stocks matching criteria in {execution_time:.2f}ms")
            return result

        except Exception as e:
            logger.error(f"Error screening stocks: {e}")
            raise

    def _build_query(self, filters: Dict[str, Any]):
        """Build SQLAlchemy query from filters"""

        # Start with base query joining Company and latest Ratio
        subquery = (
            self.db.query(
                Ratio.company_id,
                func.max(Ratio.period_end).label('max_period')
            )
            .group_by(Ratio.company_id)
            .subquery()
        )

        query = (
            self.db.query(Company, Ratio)
            .outerjoin(
                Ratio,
                and_(
                    Company.id == Ratio.company_id,
                    Ratio.period_end == subquery.c.max_period
                )
            )
            .filter(Company.is_active == 1)
        )

        # Apply filters
        for field, condition in filters.items():
            query = self._apply_filter(query, field, condition)

        return query

    def _apply_filter(self, query, field: str, condition: Dict):
        """Apply a single filter to the query"""

        # Determine if field is in Company or Ratio table
        company_fields = ['market_cap', 'shares_outstanding', 'sector', 'industry', 'exchange']
        ratio_fields = [
            'pe_ratio', 'pb_ratio', 'ps_ratio', 'ev_ebitda', 'peg_ratio',
            'roe', 'roa', 'roic', 'roce',
            'gross_margin', 'operating_margin', 'net_margin',
            'current_ratio', 'quick_ratio', 'cash_ratio',
            'debt_to_equity', 'debt_to_assets', 'interest_coverage',
            'asset_turnover', 'inventory_turnover', 'receivables_turnover',
            'days_sales_outstanding', 'days_inventory_outstanding',
            'revenue_growth_yoy', 'earnings_growth_yoy', 'fcf_growth_yoy',
            'revenue_growth_3y_cagr', 'revenue_growth_5y_cagr',
            'earnings_growth_3y_cagr', 'earnings_growth_5y_cagr',
            'dividend_yield', 'payout_ratio', 'altman_z_score', 'piotroski_f_score'
        ]

        # Get the appropriate model attribute
        if field in company_fields:
            attr = getattr(Company, field)
        elif field in ratio_fields:
            attr = getattr(Ratio, field)
        else:
            logger.warning(f"Unknown filter field: {field}")
            return query

        # Apply condition
        if 'min' in condition and 'max' in condition:
            query = query.filter(and_(attr >= condition['min'], attr <= condition['max']))
        elif 'min' in condition:
            query = query.filter(attr >= condition['min'])
        elif 'max' in condition:
            query = query.filter(attr <= condition['max'])
        elif 'eq' in condition:
            query = query.filter(attr == condition['eq'])
        elif 'ne' in condition:
            query = query.filter(attr != condition['ne'])
        elif 'in' in condition:
            query = query.filter(attr.in_(condition['in']))

        return query

    def _generate_cache_key(self, filters: Dict, limit: int, offset: int) -> str:
        """Generate cache key from filters"""
        key_data = {
            'filters': filters,
            'limit': limit,
            'offset': offset
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()

    def save_screen(
        self,
        user_id: int,
        screen_name: str,
        filters: Dict[str, Any]
    ) -> Dict:
        """
        Save a custom screen for later use

        Args:
            user_id: User ID
            screen_name: Name for the saved screen
            filters: Filter criteria

        Returns:
            Saved screen details
        """
        # This would save to a user_screens table (not implemented in models yet)
        # For now, return the screen definition
        return {
            'user_id': user_id,
            'screen_name': screen_name,
            'filters': filters,
            'created_at': datetime.now()
        }

    def backtest_screen(
        self,
        filters: Dict[str, Any],
        start_date: datetime,
        end_date: datetime
    ) -> Dict:
        """
        Backtest a screening strategy

        Args:
            filters: Filter criteria
            start_date: Start date for backtest
            end_date: End date for backtest

        Returns:
            Backtest results with historical performance
        """
        # This would:
        # 1. Run the screen at historical dates
        # 2. Track which stocks were selected
        # 3. Calculate returns for those stocks
        # 4. Return performance metrics

        logger.info(f"Backtesting screen from {start_date} to {end_date}")

        # Placeholder implementation
        return {
            'start_date': start_date,
            'end_date': end_date,
            'filters': filters,
            'total_return': None,
            'annualized_return': None,
            'sharpe_ratio': None,
            'max_drawdown': None,
            'message': 'Backtesting not yet implemented'
        }

    def get_available_filters(self) -> List[Dict]:
        """Get list of all available filter fields"""
        from app.modules.screener.filters import ScreenerFilters
        return ScreenerFilters.get_all_filter_fields()

    def get_preset_screens(self) -> Dict:
        """Get preset screening strategies"""
        from app.modules.screener.filters import ScreenerFilters
        return ScreenerFilters.get_preset_screens()

"""
Screener Filters - Define all available filters
"""
from typing import Dict, Any, List
from enum import Enum


class FilterOperator(str, Enum):
    """Filter operators"""
    GT = ">"
    GTE = ">="
    LT = "<"
    LTE = "<="
    EQ = "="
    BETWEEN = "between"


class ScreenerFilters:
    """Available screener filters"""

    # Market Cap filters
    MARKET_CAP_LARGE = {'field': 'market_cap', 'min': 20000}  # > 20,000 Cr
    MARKET_CAP_MID = {'field': 'market_cap', 'min': 5000, 'max': 20000}  # 5,000 - 20,000 Cr
    MARKET_CAP_SMALL = {'field': 'market_cap', 'max': 5000}  # < 5,000 Cr

    @staticmethod
    def get_all_filter_fields() -> List[Dict[str, Any]]:
        """
        Get all available filter fields with their descriptions

        Returns:
            List of filter field definitions
        """
        return [
            # Market Metrics
            {
                'field': 'market_cap',
                'label': 'Market Cap (Cr)',
                'type': 'number',
                'category': 'Market Metrics'
            },
            {
                'field': 'shares_outstanding',
                'label': 'Shares Outstanding',
                'type': 'number',
                'category': 'Market Metrics'
            },

            # Valuation Ratios
            {
                'field': 'pe_ratio',
                'label': 'P/E Ratio',
                'type': 'number',
                'category': 'Valuation'
            },
            {
                'field': 'pb_ratio',
                'label': 'P/B Ratio',
                'type': 'number',
                'category': 'Valuation'
            },
            {
                'field': 'ps_ratio',
                'label': 'P/S Ratio',
                'type': 'number',
                'category': 'Valuation'
            },
            {
                'field': 'ev_ebitda',
                'label': 'EV/EBITDA',
                'type': 'number',
                'category': 'Valuation'
            },
            {
                'field': 'peg_ratio',
                'label': 'PEG Ratio',
                'type': 'number',
                'category': 'Valuation'
            },
            {
                'field': 'dividend_yield',
                'label': 'Dividend Yield (%)',
                'type': 'number',
                'category': 'Valuation'
            },

            # Profitability Ratios
            {
                'field': 'roe',
                'label': 'ROE (%)',
                'type': 'number',
                'category': 'Profitability'
            },
            {
                'field': 'roa',
                'label': 'ROA (%)',
                'type': 'number',
                'category': 'Profitability'
            },
            {
                'field': 'roic',
                'label': 'ROIC (%)',
                'type': 'number',
                'category': 'Profitability'
            },
            {
                'field': 'roce',
                'label': 'ROCE (%)',
                'type': 'number',
                'category': 'Profitability'
            },
            {
                'field': 'gross_margin',
                'label': 'Gross Margin (%)',
                'type': 'number',
                'category': 'Profitability'
            },
            {
                'field': 'operating_margin',
                'label': 'Operating Margin (%)',
                'type': 'number',
                'category': 'Profitability'
            },
            {
                'field': 'net_margin',
                'label': 'Net Margin (%)',
                'type': 'number',
                'category': 'Profitability'
            },

            # Liquidity Ratios
            {
                'field': 'current_ratio',
                'label': 'Current Ratio',
                'type': 'number',
                'category': 'Liquidity'
            },
            {
                'field': 'quick_ratio',
                'label': 'Quick Ratio',
                'type': 'number',
                'category': 'Liquidity'
            },
            {
                'field': 'cash_ratio',
                'label': 'Cash Ratio',
                'type': 'number',
                'category': 'Liquidity'
            },

            # Solvency Ratios
            {
                'field': 'debt_to_equity',
                'label': 'Debt/Equity',
                'type': 'number',
                'category': 'Solvency'
            },
            {
                'field': 'debt_to_assets',
                'label': 'Debt/Assets',
                'type': 'number',
                'category': 'Solvency'
            },
            {
                'field': 'interest_coverage',
                'label': 'Interest Coverage',
                'type': 'number',
                'category': 'Solvency'
            },

            # Efficiency Ratios
            {
                'field': 'asset_turnover',
                'label': 'Asset Turnover',
                'type': 'number',
                'category': 'Efficiency'
            },
            {
                'field': 'inventory_turnover',
                'label': 'Inventory Turnover',
                'type': 'number',
                'category': 'Efficiency'
            },
            {
                'field': 'receivables_turnover',
                'label': 'Receivables Turnover',
                'type': 'number',
                'category': 'Efficiency'
            },
            {
                'field': 'days_sales_outstanding',
                'label': 'Days Sales Outstanding',
                'type': 'number',
                'category': 'Efficiency'
            },
            {
                'field': 'days_inventory_outstanding',
                'label': 'Days Inventory Outstanding',
                'type': 'number',
                'category': 'Efficiency'
            },

            # Growth Metrics
            {
                'field': 'revenue_growth_yoy',
                'label': 'Revenue Growth YoY (%)',
                'type': 'number',
                'category': 'Growth'
            },
            {
                'field': 'earnings_growth_yoy',
                'label': 'Earnings Growth YoY (%)',
                'type': 'number',
                'category': 'Growth'
            },
            {
                'field': 'fcf_growth_yoy',
                'label': 'FCF Growth YoY (%)',
                'type': 'number',
                'category': 'Growth'
            },
            {
                'field': 'revenue_growth_3y_cagr',
                'label': 'Revenue Growth 3Y CAGR (%)',
                'type': 'number',
                'category': 'Growth'
            },
            {
                'field': 'revenue_growth_5y_cagr',
                'label': 'Revenue Growth 5Y CAGR (%)',
                'type': 'number',
                'category': 'Growth'
            },
            {
                'field': 'earnings_growth_3y_cagr',
                'label': 'Earnings Growth 3Y CAGR (%)',
                'type': 'number',
                'category': 'Growth'
            },
            {
                'field': 'earnings_growth_5y_cagr',
                'label': 'Earnings Growth 5Y CAGR (%)',
                'type': 'number',
                'category': 'Growth'
            },

            # Quality Metrics
            {
                'field': 'altman_z_score',
                'label': 'Altman Z-Score',
                'type': 'number',
                'category': 'Quality'
            },
            {
                'field': 'piotroski_f_score',
                'label': 'Piotroski F-Score',
                'type': 'number',
                'category': 'Quality'
            },
            {
                'field': 'payout_ratio',
                'label': 'Payout Ratio (%)',
                'type': 'number',
                'category': 'Quality'
            },

            # Category Filters
            {
                'field': 'sector',
                'label': 'Sector',
                'type': 'string',
                'category': 'Category'
            },
            {
                'field': 'industry',
                'label': 'Industry',
                'type': 'string',
                'category': 'Category'
            },
            {
                'field': 'exchange',
                'label': 'Exchange',
                'type': 'string',
                'category': 'Category'
            },
        ]

    @staticmethod
    def get_preset_screens() -> Dict[str, Dict]:
        """
        Get preset screening strategies

        Returns:
            Dictionary of preset screens
        """
        return {
            'value_stocks': {
                'name': 'Value Stocks',
                'description': 'Low P/E, High ROE, Low Debt',
                'filters': {
                    'pe_ratio': {'max': 15},
                    'pb_ratio': {'max': 3},
                    'roe': {'min': 15},
                    'debt_to_equity': {'max': 1},
                    'market_cap': {'min': 1000}
                }
            },
            'growth_stocks': {
                'name': 'Growth Stocks',
                'description': 'High Revenue & Earnings Growth',
                'filters': {
                    'revenue_growth_3y_cagr': {'min': 15},
                    'earnings_growth_3y_cagr': {'min': 15},
                    'roe': {'min': 15},
                    'market_cap': {'min': 500}
                }
            },
            'dividend_aristocrats': {
                'name': 'Dividend Aristocrats',
                'description': 'High Dividend Yield, Low Payout Ratio',
                'filters': {
                    'dividend_yield': {'min': 3},
                    'payout_ratio': {'max': 60},
                    'roe': {'min': 12},
                    'debt_to_equity': {'max': 1.5}
                }
            },
            'quality_stocks': {
                'name': 'Quality Stocks',
                'description': 'High ROE, ROIC, Low Debt',
                'filters': {
                    'roe': {'min': 20},
                    'roic': {'min': 15},
                    'debt_to_equity': {'max': 0.5},
                    'interest_coverage': {'min': 5},
                    'current_ratio': {'min': 1.5}
                }
            },
            'undervalued_growth': {
                'name': 'Undervalued Growth',
                'description': 'PEG < 1, High Growth',
                'filters': {
                    'peg_ratio': {'max': 1},
                    'revenue_growth_3y_cagr': {'min': 12},
                    'roe': {'min': 15},
                    'market_cap': {'min': 1000}
                }
            },
            'strong_financials': {
                'name': 'Strong Financials',
                'description': 'Altman Z-Score > 3, Piotroski F-Score > 7',
                'filters': {
                    'altman_z_score': {'min': 3},
                    'piotroski_f_score': {'min': 7},
                    'debt_to_equity': {'max': 1}
                }
            },
            'small_cap_growth': {
                'name': 'Small Cap Growth',
                'description': 'Small Cap with High Growth',
                'filters': {
                    'market_cap': {'min': 100, 'max': 5000},
                    'revenue_growth_3y_cagr': {'min': 20},
                    'roe': {'min': 15}
                }
            },
            'large_cap_stable': {
                'name': 'Large Cap Stable',
                'description': 'Large Cap, Low Volatility, Consistent Returns',
                'filters': {
                    'market_cap': {'min': 20000},
                    'roe': {'min': 12},
                    'debt_to_equity': {'max': 1},
                    'current_ratio': {'min': 1.2}
                }
            }
        }

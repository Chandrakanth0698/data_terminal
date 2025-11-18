"""
DCF Calculator - Discounted Cash Flow valuation
"""
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from typing import Dict, List
from loguru import logger

from app.models import Company, FinancialStatement, StockPrice


class DCFCalculator:
    """DCF Valuation Calculator"""

    def __init__(self, db: Session):
        self.db = db

    def calculate_dcf(
        self,
        company_id: int,
        projection_years: int = 5,
        revenue_growth_rate: float = 10.0,
        operating_margin: float = 15.0,
        tax_rate: float = 25.0,
        capex_percentage: float = 5.0,
        nwc_percentage: float = 10.0,
        terminal_growth_rate: float = 3.0,
        wacc: float = 10.0
    ) -> Dict:
        """
        Calculate DCF valuation

        Args:
            company_id: Company ID
            projection_years: Number of years to project (default 5)
            revenue_growth_rate: Annual revenue growth rate (%)
            operating_margin: Operating margin (%)
            tax_rate: Tax rate (%)
            capex_percentage: CapEx as % of revenue
            nwc_percentage: Net Working Capital as % of revenue
            terminal_growth_rate: Perpetual growth rate (%)
            wacc: Weighted Average Cost of Capital (%)

        Returns:
            Dictionary with DCF results
        """
        try:
            # Get company
            company = self.db.query(Company).filter(Company.id == company_id).first()
            if not company:
                raise ValueError("Company not found")

            # Get latest financial data
            latest_statement = self.db.query(FinancialStatement).filter(
                FinancialStatement.company_id == company_id,
                FinancialStatement.statement_type == "Income",
                FinancialStatement.period_type == "Annual"
            ).order_by(FinancialStatement.period_end.desc()).first()

            if not latest_statement or not latest_statement.revenue:
                raise ValueError("No financial data available for DCF calculation")

            base_revenue = latest_statement.revenue

            # Project revenues
            revenues = []
            for year in range(1, projection_years + 1):
                projected_revenue = base_revenue * ((1 + revenue_growth_rate / 100) ** year)
                revenues.append(projected_revenue)

            # Calculate Free Cash Flows
            fcfs = []
            projections = []

            for year, revenue in enumerate(revenues, start=1):
                # Operating Income (EBIT)
                ebit = revenue * (operating_margin / 100)

                # Tax
                tax = ebit * (tax_rate / 100)

                # NOPAT (Net Operating Profit After Tax)
                nopat = ebit - tax

                # CapEx
                capex = revenue * (capex_percentage / 100)

                # Change in NWC
                nwc_change = revenue * (nwc_percentage / 100) * (revenue_growth_rate / 100)

                # Free Cash Flow = NOPAT + Depreciation - CapEx - Change in NWC
                # Simplified: assuming depreciation = capex for steady state
                fcf = nopat - capex - nwc_change

                fcfs.append(fcf)

                projections.append({
                    'year': year,
                    'revenue': revenue,
                    'ebit': ebit,
                    'tax': tax,
                    'nopat': nopat,
                    'capex': capex,
                    'nwc_change': nwc_change,
                    'fcf': fcf
                })

            # Terminal Value
            terminal_fcf = fcfs[-1] * (1 + terminal_growth_rate / 100)
            terminal_value = terminal_fcf / ((wacc / 100) - (terminal_growth_rate / 100))

            # Discount all cash flows to present value
            discount_factors = [(1 + wacc / 100) ** year for year in range(1, projection_years + 1)]
            pv_fcfs = [fcf / df for fcf, df in zip(fcfs, discount_factors)]
            pv_terminal_value = terminal_value / ((1 + wacc / 100) ** projection_years)

            # Enterprise Value
            enterprise_value = sum(pv_fcfs) + pv_terminal_value

            # Equity Value = Enterprise Value - Net Debt
            # For simplification, assume net debt = 0 (would need balance sheet data)
            equity_value = enterprise_value

            # Value per share
            shares_outstanding = company.shares_outstanding or 1
            intrinsic_value_per_share = equity_value / shares_outstanding

            # Get current price
            latest_price = self.db.query(StockPrice).filter(
                StockPrice.company_id == company_id
            ).order_by(StockPrice.date.desc()).first()

            current_price = latest_price.close if latest_price else None

            # Calculate upside/downside
            upside_downside = None
            if current_price:
                upside_downside = ((intrinsic_value_per_share - current_price) / current_price) * 100

            # Generate sensitivity table
            sensitivity_table = self._generate_sensitivity_table(
                fcfs, terminal_fcf, shares_outstanding, projection_years
            )

            result = {
                'intrinsic_value_per_share': intrinsic_value_per_share,
                'current_price': current_price,
                'upside_downside': upside_downside,
                'enterprise_value': enterprise_value,
                'equity_value': equity_value,
                'terminal_value': terminal_value,
                'pv_terminal_value': pv_terminal_value,
                'projections': projections,
                'sensitivity_table': sensitivity_table
            }

            logger.info(f"DCF calculation completed for company_id={company_id}")
            return result

        except Exception as e:
            logger.error(f"Error calculating DCF: {e}")
            raise

    def _generate_sensitivity_table(
        self,
        fcfs: List[float],
        terminal_fcf: float,
        shares_outstanding: float,
        projection_years: int
    ) -> Dict:
        """Generate sensitivity analysis table (WACC vs Terminal Growth)"""

        wacc_range = np.arange(8, 13, 0.5)  # 8% to 12% in 0.5% steps
        terminal_growth_range = np.arange(2, 5, 0.5)  # 2% to 4% in 0.5% steps

        sensitivity_data = []

        for wacc in wacc_range:
            row = {'wacc': wacc}

            for tg in terminal_growth_range:
                # Recalculate with new assumptions
                terminal_value = terminal_fcf / ((wacc / 100) - (tg / 100))

                discount_factors = [(1 + wacc / 100) ** year for year in range(1, projection_years + 1)]
                pv_fcfs = [fcf / df for fcf, df in zip(fcfs, discount_factors)]
                pv_terminal_value = terminal_value / ((1 + wacc / 100) ** projection_years)

                equity_value = sum(pv_fcfs) + pv_terminal_value
                value_per_share = equity_value / shares_outstanding

                row[f'tg_{tg:.1f}'] = value_per_share

            sensitivity_data.append(row)

        return {
            'wacc_range': wacc_range.tolist(),
            'terminal_growth_range': terminal_growth_range.tolist(),
            'values': sensitivity_data
        }

    def calculate_relative_valuation(self, company_id: int) -> Dict:
        """
        Calculate relative valuation metrics vs peers

        Args:
            company_id: Company ID

        Returns:
            Dictionary with relative valuation analysis
        """
        # Get company and peers
        company = self.db.query(Company).filter(Company.id == company_id).first()

        if not company or not company.peers:
            return {}

        # This would compare P/E, P/B, EV/EBITDA ratios with peers
        # Placeholder implementation

        return {
            'company_symbol': company.symbol,
            'peer_comparison': 'Not yet implemented'
        }

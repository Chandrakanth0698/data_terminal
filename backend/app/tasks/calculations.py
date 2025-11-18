"""
Calculation tasks - Background jobs for calculating ratios and metrics
"""
from celery import shared_task
from loguru import logger
from sqlalchemy import func

from app.core.database import SessionLocal
from app.models import Company, FinancialStatement, Ratio, StockPrice


@shared_task(name="app.tasks.calculations.calculate_all_ratios")
def calculate_all_ratios():
    """Calculate financial ratios for all companies"""
    logger.info("Starting ratio calculations for all companies")

    db = SessionLocal()
    try:
        companies = db.query(Company).filter(Company.is_active == 1).all()
        success_count = 0

        for company in companies:
            try:
                # Calculate ratios for this company
                result = calculate_company_ratios(company.id)
                if result:
                    success_count += 1

            except Exception as e:
                logger.error(f"Error calculating ratios for {company.symbol}: {e}")
                continue

        logger.info(f"Successfully calculated ratios for {success_count} companies")
        return {'success': success_count, 'total': len(companies)}

    except Exception as e:
        logger.error(f"Error in calculate_all_ratios task: {e}")
        raise
    finally:
        db.close()


def calculate_company_ratios(company_id: int) -> bool:
    """
    Calculate financial ratios for a specific company

    Args:
        company_id: Company ID

    Returns:
        True if successful
    """
    db = SessionLocal()
    try:
        # Get latest financial statements
        latest_income = db.query(FinancialStatement).filter(
            FinancialStatement.company_id == company_id,
            FinancialStatement.statement_type == "Income",
            FinancialStatement.period_type == "Annual"
        ).order_by(FinancialStatement.period_end.desc()).first()

        latest_balance = db.query(FinancialStatement).filter(
            FinancialStatement.company_id == company_id,
            FinancialStatement.statement_type == "Balance",
            FinancialStatement.period_type == "Annual"
        ).order_by(FinancialStatement.period_end.desc()).first()

        latest_cashflow = db.query(FinancialStatement).filter(
            FinancialStatement.company_id == company_id,
            FinancialStatement.statement_type == "CashFlow",
            FinancialStatement.period_type == "Annual"
        ).order_by(FinancialStatement.period_end.desc()).first()

        if not latest_income or not latest_balance:
            logger.warning(f"Insufficient data for company_id={company_id}")
            return False

        # Get latest stock price
        latest_price = db.query(StockPrice).filter(
            StockPrice.company_id == company_id
        ).order_by(StockPrice.date.desc()).first()

        # Get company
        company = db.query(Company).filter(Company.id == company_id).first()

        # Calculate ratios
        ratios = Ratio(
            company_id=company_id,
            period_end=latest_income.period_end,
            period_type="Annual"
        )

        # Profitability Ratios
        if latest_income.revenue and latest_income.revenue > 0:
            ratios.gross_margin = (latest_income.gross_profit / latest_income.revenue * 100) if latest_income.gross_profit else None
            ratios.operating_margin = (latest_income.operating_income / latest_income.revenue * 100) if latest_income.operating_income else None
            ratios.net_margin = (latest_income.net_income / latest_income.revenue * 100) if latest_income.net_income else None

        if latest_balance.shareholders_equity and latest_balance.shareholders_equity > 0:
            ratios.roe = (latest_income.net_income / latest_balance.shareholders_equity * 100) if latest_income.net_income else None

        if latest_balance.total_assets and latest_balance.total_assets > 0:
            ratios.roa = (latest_income.net_income / latest_balance.total_assets * 100) if latest_income.net_income else None

        # Liquidity Ratios
        if latest_balance.current_liabilities and latest_balance.current_liabilities > 0:
            ratios.current_ratio = latest_balance.current_assets / latest_balance.current_liabilities if latest_balance.current_assets else None
            quick_assets = (latest_balance.current_assets or 0) - (latest_balance.inventory or 0)
            ratios.quick_ratio = quick_assets / latest_balance.current_liabilities

        # Solvency Ratios
        if latest_balance.shareholders_equity and latest_balance.shareholders_equity > 0:
            total_debt = (latest_balance.short_term_debt or 0) + (latest_balance.long_term_debt or 0)
            ratios.debt_to_equity = total_debt / latest_balance.shareholders_equity

        # Valuation Ratios
        if latest_price and latest_income.eps and latest_income.eps > 0:
            ratios.pe_ratio = latest_price.close / latest_income.eps

        if latest_price and latest_balance.shareholders_equity and company.shares_outstanding:
            book_value_per_share = latest_balance.shareholders_equity / company.shares_outstanding
            if book_value_per_share > 0:
                ratios.pb_ratio = latest_price.close / book_value_per_share

        # Save ratios
        db.add(ratios)
        db.commit()

        logger.info(f"Calculated ratios for company_id={company_id}")
        return True

    except Exception as e:
        logger.error(f"Error calculating ratios for company_id={company_id}: {e}")
        db.rollback()
        return False
    finally:
        db.close()

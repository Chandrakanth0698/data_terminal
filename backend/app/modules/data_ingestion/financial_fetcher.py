"""
Financial Fetcher - Fetch financial statements from various sources
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import Optional, Dict
from loguru import logger
import yfinance as yf
import time


class FinancialFetcher:
    """Fetch financial statements data"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def fetch_from_yahoo_finance(self, symbol: str) -> Dict[str, pd.DataFrame]:
        """
        Fetch financial statements from Yahoo Finance

        Args:
            symbol: Stock symbol

        Returns:
            Dictionary with income_statement, balance_sheet, cash_flow DataFrames
        """
        try:
            ticker = yf.Ticker(f"{symbol}.NS")

            # Fetch all three statements
            income_statement = ticker.income_stmt
            balance_sheet = ticker.balance_sheet
            cash_flow = ticker.cashflow

            result = {}

            if income_statement is not None and not income_statement.empty:
                result['income_statement'] = income_statement
                logger.info(f"Fetched income statement for {symbol}")

            if balance_sheet is not None and not balance_sheet.empty:
                result['balance_sheet'] = balance_sheet
                logger.info(f"Fetched balance sheet for {symbol}")

            if cash_flow is not None and not cash_flow.empty:
                result['cash_flow'] = cash_flow
                logger.info(f"Fetched cash flow for {symbol}")

            return result

        except Exception as e:
            logger.error(f"Error fetching financials from Yahoo Finance for {symbol}: {e}")
            return {}

    def fetch_from_screener(self, symbol: str) -> Dict:
        """
        Scrape financial data from Screener.in

        Args:
            symbol: Stock symbol

        Returns:
            Dictionary with financial metrics
        """
        try:
            url = f"https://www.screener.in/company/{symbol}/consolidated/"
            response = self.session.get(url, timeout=10)

            if response.status_code != 200:
                logger.warning(f"Screener.in returned status {response.status_code} for {symbol}")
                return {}

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract financial tables
            data = {
                'quarters': self._extract_quarterly_results(soup),
                'profit_loss': self._extract_profit_loss(soup),
                'balance_sheet': self._extract_balance_sheet(soup),
                'cash_flow': self._extract_cash_flow(soup),
                'ratios': self._extract_ratios(soup)
            }

            logger.info(f"Scraped financial data for {symbol} from Screener.in")
            return data

        except Exception as e:
            logger.error(f"Error scraping Screener.in for {symbol}: {e}")
            return {}

    def _extract_quarterly_results(self, soup: BeautifulSoup) -> pd.DataFrame:
        """Extract quarterly results table"""
        try:
            # Find the quarterly results section
            section = soup.find('section', {'id': 'quarters'})
            if not section:
                return pd.DataFrame()

            table = section.find('table')
            if not table:
                return pd.DataFrame()

            df = pd.read_html(str(table))[0]
            return df

        except Exception as e:
            logger.error(f"Error extracting quarterly results: {e}")
            return pd.DataFrame()

    def _extract_profit_loss(self, soup: BeautifulSoup) -> pd.DataFrame:
        """Extract profit & loss statement"""
        try:
            section = soup.find('section', {'id': 'profit-loss'})
            if not section:
                return pd.DataFrame()

            table = section.find('table')
            if not table:
                return pd.DataFrame()

            df = pd.read_html(str(table))[0]
            return df

        except Exception as e:
            logger.error(f"Error extracting P&L: {e}")
            return pd.DataFrame()

    def _extract_balance_sheet(self, soup: BeautifulSoup) -> pd.DataFrame:
        """Extract balance sheet"""
        try:
            section = soup.find('section', {'id': 'balance-sheet'})
            if not section:
                return pd.DataFrame()

            table = section.find('table')
            if not table:
                return pd.DataFrame()

            df = pd.read_html(str(table))[0]
            return df

        except Exception as e:
            logger.error(f"Error extracting balance sheet: {e}")
            return pd.DataFrame()

    def _extract_cash_flow(self, soup: BeautifulSoup) -> pd.DataFrame:
        """Extract cash flow statement"""
        try:
            section = soup.find('section', {'id': 'cash-flow'})
            if not section:
                return pd.DataFrame()

            table = section.find('table')
            if not table:
                return pd.DataFrame()

            df = pd.read_html(str(table))[0]
            return df

        except Exception as e:
            logger.error(f"Error extracting cash flow: {e}")
            return pd.DataFrame()

    def _extract_ratios(self, soup: BeautifulSoup) -> Dict:
        """Extract key financial ratios"""
        try:
            ratios = {}

            # Find all ratio elements
            ratio_list = soup.find_all('li', {'class': 'flex flex-space-between'})

            for item in ratio_list:
                name_elem = item.find('span', {'class': 'name'})
                value_elem = item.find('span', {'class': 'number'})

                if name_elem and value_elem:
                    name = name_elem.text.strip()
                    value = value_elem.text.strip()
                    ratios[name] = value

            return ratios

        except Exception as e:
            logger.error(f"Error extracting ratios: {e}")
            return {}

    def get_company_info(self, symbol: str) -> Dict:
        """
        Get comprehensive company information

        Args:
            symbol: Stock symbol

        Returns:
            Dictionary with company details
        """
        try:
            ticker = yf.Ticker(f"{symbol}.NS")
            info = ticker.info

            company_data = {
                'symbol': symbol,
                'name': info.get('longName'),
                'sector': info.get('sector'),
                'industry': info.get('industry'),
                'website': info.get('website'),
                'description': info.get('longBusinessSummary'),
                'employees': info.get('fullTimeEmployees'),
                'market_cap': info.get('marketCap'),
                'shares_outstanding': info.get('sharesOutstanding'),
                'headquarters': f"{info.get('city', '')}, {info.get('country', '')}",
            }

            return company_data

        except Exception as e:
            logger.error(f"Error fetching company info for {symbol}: {e}")
            return {}

    def fetch_all_financials(self, symbol: str, years: int = 10) -> Dict:
        """
        Fetch all financial data for a company

        Args:
            symbol: Stock symbol
            years: Number of years of data

        Returns:
            Dictionary with all financial data
        """
        result = {
            'company_info': self.get_company_info(symbol),
            'statements': self.fetch_from_yahoo_finance(symbol),
            'screener_data': self.fetch_from_screener(symbol)
        }

        return result

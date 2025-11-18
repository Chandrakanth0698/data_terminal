"""
Price Fetcher - Fetch stock prices from NSE/BSE/Yahoo Finance
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
from loguru import logger

try:
    from nsepython import nsefetch, nse_eq_symbols
except ImportError:
    logger.warning("nsepython not installed, NSE direct fetch will be unavailable")
    nsepython = None


class PriceFetcher:
    """Fetch stock price data from multiple sources"""

    def __init__(self):
        self.yf_suffix = ".NS"  # Yahoo Finance suffix for NSE stocks

    def fetch_yahoo_finance(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        period: str = "1y"
    ) -> pd.DataFrame:
        """
        Fetch price data from Yahoo Finance

        Args:
            symbol: Stock symbol (without .NS suffix)
            start_date: Start date for historical data
            end_date: End date for historical data
            period: Period for data (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)

        Returns:
            DataFrame with OHLCV data
        """
        try:
            ticker = yf.Ticker(f"{symbol}{self.yf_suffix}")

            if start_date and end_date:
                df = ticker.history(start=start_date, end=end_date)
            else:
                df = ticker.history(period=period)

            if df.empty:
                logger.warning(f"No data found for {symbol} on Yahoo Finance")
                return pd.DataFrame()

            # Rename columns to match our schema
            df = df.rename(columns={
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume'
            })

            # Add adj_close if not present
            if 'Adj Close' in df.columns:
                df['adj_close'] = df['Adj Close']
            else:
                df['adj_close'] = df['close']

            # Select relevant columns
            df = df[['open', 'high', 'low', 'close', 'volume', 'adj_close']]

            # Reset index to have date as a column
            df.reset_index(inplace=True)
            df.rename(columns={'Date': 'date'}, inplace=True)

            logger.info(f"Fetched {len(df)} rows for {symbol} from Yahoo Finance")
            return df

        except Exception as e:
            logger.error(f"Error fetching Yahoo Finance data for {symbol}: {e}")
            return pd.DataFrame()

    def fetch_nse_current_price(self, symbol: str) -> Optional[dict]:
        """
        Fetch current price from NSE

        Args:
            symbol: NSE stock symbol

        Returns:
            Dictionary with current price data
        """
        if nsepython is None:
            logger.warning("nsepython not available, falling back to Yahoo Finance")
            return self._get_current_price_yahoo(symbol)

        try:
            # Fetch quote from NSE
            quote = nsefetch(f'https://www.nseindia.com/api/quote-equity?symbol={symbol}')

            if not quote or 'priceInfo' not in quote:
                return None

            price_info = quote['priceInfo']

            return {
                'symbol': symbol,
                'last_price': price_info.get('lastPrice'),
                'open': price_info.get('open'),
                'high': price_info.get('intraDayHighLow', {}).get('max'),
                'low': price_info.get('intraDayHighLow', {}).get('min'),
                'close': price_info.get('close'),
                'volume': quote.get('preOpenMarket', {}).get('totalTradedVolume', 0),
                'change': price_info.get('change'),
                'pChange': price_info.get('pChange'),
                'timestamp': datetime.now()
            }

        except Exception as e:
            logger.error(f"Error fetching NSE current price for {symbol}: {e}")
            return self._get_current_price_yahoo(symbol)

    def _get_current_price_yahoo(self, symbol: str) -> Optional[dict]:
        """Fallback method to get current price from Yahoo Finance"""
        try:
            ticker = yf.Ticker(f"{symbol}{self.yf_suffix}")
            info = ticker.info

            return {
                'symbol': symbol,
                'last_price': info.get('currentPrice') or info.get('regularMarketPrice'),
                'open': info.get('regularMarketOpen'),
                'high': info.get('dayHigh'),
                'low': info.get('dayLow'),
                'close': info.get('previousClose'),
                'volume': info.get('volume'),
                'change': info.get('regularMarketChange'),
                'pChange': info.get('regularMarketChangePercent'),
                'timestamp': datetime.now()
            }

        except Exception as e:
            logger.error(f"Error fetching Yahoo Finance current price for {symbol}: {e}")
            return None

    def fetch_bulk_prices(
        self,
        symbols: list,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        period: str = "1y"
    ) -> dict:
        """
        Fetch prices for multiple symbols

        Args:
            symbols: List of stock symbols
            start_date: Start date
            end_date: End date
            period: Period string

        Returns:
            Dictionary {symbol: DataFrame}
        """
        results = {}

        for symbol in symbols:
            df = self.fetch_yahoo_finance(symbol, start_date, end_date, period)
            if not df.empty:
                results[symbol] = df

        logger.info(f"Fetched prices for {len(results)}/{len(symbols)} symbols")
        return results

    def get_historical_data(
        self,
        symbol: str,
        years: int = 10
    ) -> pd.DataFrame:
        """
        Get historical data for specified number of years

        Args:
            symbol: Stock symbol
            years: Number of years of data

        Returns:
            DataFrame with historical OHLCV data
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=years * 365)

        return self.fetch_yahoo_finance(symbol, start_date, end_date)

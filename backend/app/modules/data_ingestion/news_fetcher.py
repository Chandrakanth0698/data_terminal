"""
News Fetcher - Fetch news from various sources
"""
import requests
from bs4 import BeautifulSoup
import feedparser
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from loguru import logger


class NewsFetcher:
    """Fetch news articles from various sources"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def fetch_google_news(self, query: str, days: int = 7) -> List[Dict]:
        """
        Fetch news from Google News RSS

        Args:
            query: Search query (company name or stock symbol)
            days: Number of days to look back

        Returns:
            List of news articles
        """
        try:
            # Google News RSS URL
            url = f"https://news.google.com/rss/search?q={query}+stock+india&hl=en-IN&gl=IN&ceid=IN:en"

            # Parse RSS feed
            feed = feedparser.parse(url)

            articles = []
            cutoff_date = datetime.now() - timedelta(days=days)

            for entry in feed.entries:
                # Parse published date
                published = datetime(*entry.published_parsed[:6])

                if published < cutoff_date:
                    continue

                article = {
                    'title': entry.title,
                    'url': entry.link,
                    'source': entry.get('source', {}).get('title', 'Google News'),
                    'published_at': published,
                    'summary': entry.get('summary', ''),
                }

                articles.append(article)

            logger.info(f"Fetched {len(articles)} articles from Google News for '{query}'")
            return articles

        except Exception as e:
            logger.error(f"Error fetching Google News for '{query}': {e}")
            return []

    def fetch_moneycontrol_news(self, symbol: str) -> List[Dict]:
        """
        Scrape news from MoneyControl

        Args:
            symbol: Stock symbol

        Returns:
            List of news articles
        """
        try:
            # MoneyControl news page (note: may need adjustment based on actual site structure)
            url = f"https://www.moneycontrol.com/india/stockpricequote/{symbol}"

            response = self.session.get(url, timeout=10)

            if response.status_code != 200:
                logger.warning(f"MoneyControl returned status {response.status_code}")
                return []

            soup = BeautifulSoup(response.content, 'html.parser')

            articles = []

            # Find news articles (structure may vary)
            news_items = soup.find_all('div', {'class': 'news_item'})

            for item in news_items[:20]:  # Limit to 20 articles
                try:
                    title_elem = item.find('a')
                    if not title_elem:
                        continue

                    title = title_elem.text.strip()
                    url = title_elem.get('href', '')

                    # Get date if available
                    date_elem = item.find('span', {'class': 'date'})
                    published_at = datetime.now()

                    if date_elem:
                        # Parse date (format may vary)
                        try:
                            published_at = datetime.strptime(date_elem.text.strip(), '%B %d, %Y')
                        except:
                            pass

                    article = {
                        'title': title,
                        'url': url if url.startswith('http') else f"https://www.moneycontrol.com{url}",
                        'source': 'MoneyControl',
                        'published_at': published_at,
                        'summary': ''
                    }

                    articles.append(article)

                except Exception as e:
                    logger.debug(f"Error parsing news item: {e}")
                    continue

            logger.info(f"Fetched {len(articles)} articles from MoneyControl for {symbol}")
            return articles

        except Exception as e:
            logger.error(f"Error scraping MoneyControl for {symbol}: {e}")
            return []

    def fetch_all_news(self, symbol: str, company_name: str, days: int = 7) -> List[Dict]:
        """
        Fetch news from all sources

        Args:
            symbol: Stock symbol
            company_name: Company name
            days: Number of days to look back

        Returns:
            Consolidated list of news articles
        """
        all_news = []

        # Fetch from Google News
        google_news = self.fetch_google_news(company_name, days)
        all_news.extend(google_news)

        # Fetch from MoneyControl
        mc_news = self.fetch_moneycontrol_news(symbol)
        all_news.extend(mc_news)

        # Remove duplicates based on title
        seen_titles = set()
        unique_news = []

        for article in all_news:
            title_lower = article['title'].lower()
            if title_lower not in seen_titles:
                seen_titles.add(title_lower)
                unique_news.append(article)

        # Sort by published date (newest first)
        unique_news.sort(key=lambda x: x['published_at'], reverse=True)

        logger.info(f"Total {len(unique_news)} unique articles fetched for {symbol}")
        return unique_news

    def analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment of news text (basic implementation)

        Args:
            text: News text

        Returns:
            Dictionary with sentiment score and label
        """
        try:
            from textblob import TextBlob

            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 to 1

            # Classify sentiment
            if polarity > 0.1:
                label = "Positive"
            elif polarity < -0.1:
                label = "Negative"
            else:
                label = "Neutral"

            return {
                'score': polarity,
                'label': label
            }

        except ImportError:
            logger.warning("TextBlob not installed, sentiment analysis unavailable")
            return {'score': 0.0, 'label': 'Neutral'}
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {'score': 0.0, 'label': 'Neutral'}

"""
Data ingestion tasks - Background jobs for fetching data
"""
from celery import shared_task
from loguru import logger
from datetime import datetime

from app.core.database import SessionLocal
from app.models import Company, StockPrice, FinancialStatement, News
from app.modules.data_ingestion import PriceFetcher, FinancialFetcher, NewsFetcher


@shared_task(name="app.tasks.data_ingestion.fetch_all_stock_prices")
def fetch_all_stock_prices():
    """Fetch stock prices for all active companies"""
    logger.info("Starting daily stock price fetch")

    db = SessionLocal()
    try:
        # Get all active companies
        companies = db.query(Company).filter(Company.is_active == 1).all()
        logger.info(f"Fetching prices for {len(companies)} companies")

        price_fetcher = PriceFetcher()
        success_count = 0

        for company in companies:
            try:
                # Fetch current price
                price_data = price_fetcher.fetch_nse_current_price(company.symbol)

                if price_data:
                    # Save to database
                    stock_price = StockPrice(
                        company_id=company.id,
                        date=price_data['timestamp'],
                        open=price_data['open'],
                        high=price_data['high'],
                        low=price_data['low'],
                        close=price_data['last_price'],
                        volume=price_data['volume'],
                        adj_close=price_data['last_price']
                    )

                    db.add(stock_price)
                    success_count += 1

                if success_count % 50 == 0:
                    db.commit()
                    logger.info(f"Committed {success_count} price records")

            except Exception as e:
                logger.error(f"Error fetching price for {company.symbol}: {e}")
                continue

        db.commit()
        logger.info(f"Successfully fetched prices for {success_count}/{len(companies)} companies")

        return {'success': success_count, 'total': len(companies)}

    except Exception as e:
        logger.error(f"Error in fetch_all_stock_prices task: {e}")
        db.rollback()
        raise
    finally:
        db.close()


@shared_task(name="app.tasks.data_ingestion.fetch_all_financials")
def fetch_all_financials():
    """Fetch financial statements for all companies"""
    logger.info("Starting weekly financials fetch")

    db = SessionLocal()
    try:
        companies = db.query(Company).filter(Company.is_active == 1).all()
        logger.info(f"Fetching financials for {len(companies)} companies")

        financial_fetcher = FinancialFetcher()
        success_count = 0

        for company in companies:
            try:
                # Fetch all financials
                data = financial_fetcher.fetch_all_financials(company.symbol)

                if data and data.get('statements'):
                    # Process and save financial statements
                    # This is a simplified version - actual implementation would parse all data
                    success_count += 1

            except Exception as e:
                logger.error(f"Error fetching financials for {company.symbol}: {e}")
                continue

        logger.info(f"Successfully processed financials for {success_count} companies")

        return {'success': success_count, 'total': len(companies)}

    except Exception as e:
        logger.error(f"Error in fetch_all_financials task: {e}")
        raise
    finally:
        db.close()


@shared_task(name="app.tasks.data_ingestion.fetch_all_news")
def fetch_all_news():
    """Fetch news for all companies"""
    logger.info("Starting hourly news fetch")

    db = SessionLocal()
    try:
        # Fetch for top 100 companies by market cap
        companies = db.query(Company).filter(
            Company.is_active == 1
        ).order_by(
            Company.market_cap.desc()
        ).limit(100).all()

        logger.info(f"Fetching news for {len(companies)} companies")

        news_fetcher = NewsFetcher()
        total_articles = 0

        for company in companies:
            try:
                articles = news_fetcher.fetch_all_news(
                    company.symbol,
                    company.name,
                    days=1
                )

                for article in articles:
                    # Check if article already exists
                    existing = db.query(News).filter(
                        News.company_id == company.id,
                        News.url == article['url']
                    ).first()

                    if not existing:
                        # Analyze sentiment
                        sentiment = news_fetcher.analyze_sentiment(
                            article.get('summary', '') or article.get('title', '')
                        )

                        news_item = News(
                            company_id=company.id,
                            title=article['title'],
                            url=article['url'],
                            source=article['source'],
                            published_at=article['published_at'],
                            summary=article.get('summary', ''),
                            sentiment_score=sentiment['score'],
                            sentiment_label=sentiment['label']
                        )

                        db.add(news_item)
                        total_articles += 1

                if total_articles % 100 == 0:
                    db.commit()

            except Exception as e:
                logger.error(f"Error fetching news for {company.symbol}: {e}")
                continue

        db.commit()
        logger.info(f"Successfully fetched {total_articles} new articles")

        return {'articles': total_articles, 'companies': len(companies)}

    except Exception as e:
        logger.error(f"Error in fetch_all_news task: {e}")
        db.rollback()
        raise
    finally:
        db.close()

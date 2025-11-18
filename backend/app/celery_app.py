"""
Celery application configuration
"""
from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "stockanalysis",
    broker=str(settings.CELERY_BROKER_URL),
    backend=str(settings.CELERY_RESULT_BACKEND),
    include=[
        'app.tasks.data_ingestion',
        'app.tasks.calculations',
        'app.tasks.alerts',
    ]
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Kolkata',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour
    task_soft_time_limit=3000,  # 50 minutes
)

# Periodic tasks schedule
celery_app.conf.beat_schedule = {
    'fetch-stock-prices-daily': {
        'task': 'app.tasks.data_ingestion.fetch_all_stock_prices',
        'schedule': crontab(hour=16, minute=30),  # 4:30 PM daily (after market close)
    },
    'fetch-news-hourly': {
        'task': 'app.tasks.data_ingestion.fetch_all_news',
        'schedule': crontab(minute=0),  # Every hour
    },
    'fetch-financials-weekly': {
        'task': 'app.tasks.data_ingestion.fetch_all_financials',
        'schedule': crontab(day_of_week=0, hour=2),  # Sunday 2 AM
    },
    'calculate-ratios-daily': {
        'task': 'app.tasks.calculations.calculate_all_ratios',
        'schedule': crontab(hour=17, minute=0),  # 5 PM daily
    },
    'check-alerts-every-5-min': {
        'task': 'app.tasks.alerts.check_all_alerts',
        'schedule': crontab(minute='*/5'),  # Every 5 minutes
    },
}

if __name__ == '__main__':
    celery_app.start()

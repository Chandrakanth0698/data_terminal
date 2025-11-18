"""
Screener result model - Cached screening results
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime

from app.core.database import Base


class ScreenerResult(Base):
    """Cached screener results"""

    __tablename__ = "screener_results"

    id = Column(Integer, primary_key=True, index=True)

    # Screen identification
    screen_name = Column(String(200))
    screen_hash = Column(String(64), unique=True, index=True)  # Hash of filter criteria

    # Filter criteria (JSON)
    filters = Column(JSON, nullable=False)

    # Results (JSON)
    results = Column(JSON)  # List of company symbols that match
    result_count = Column(Integer)

    # Performance metrics
    execution_time_ms = Column(Integer)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

    def __repr__(self):
        return f"<ScreenerResult(screen_name={self.screen_name}, count={self.result_count})>"

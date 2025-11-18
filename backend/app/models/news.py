"""
News model - Aggregated news articles
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class News(Base):
    """News articles table"""

    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    # Article info
    title = Column(String(500), nullable=False)
    url = Column(String(1000))
    source = Column(String(100), index=True)
    published_at = Column(DateTime, nullable=False, index=True)

    # Content
    summary = Column(Text)
    content = Column(Text)

    # Sentiment (if analyzed)
    sentiment_score = Column(Float)  # -1 to 1
    sentiment_label = Column(String(20))  # Positive, Negative, Neutral

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="news")

    # Indexes
    __table_args__ = (
        Index('ix_news_company_published', 'company_id', 'published_at'),
    )

    def __repr__(self):
        return f"<News(company_id={self.company_id}, title={self.title[:50]})>"

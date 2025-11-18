"""
Redis connection and caching utilities
"""
import json
from typing import Any, Optional
import redis
from app.core.config import settings

# Create Redis client
redis_client = redis.from_url(
    str(settings.REDIS_URL),
    encoding="utf-8",
    decode_responses=True
)


class RedisCache:
    """Redis caching utility"""

    def __init__(self, client: redis.Redis = redis_client):
        self.client = client
        self.default_ttl = settings.REDIS_CACHE_TTL

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        value = self.client.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache"""
        ttl = ttl or self.default_ttl
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            return self.client.setex(key, ttl, value)
        except Exception:
            return False

    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        return self.client.delete(key) > 0

    def exists(self, key: str) -> bool:
        """Check if key exists"""
        return self.client.exists(key) > 0

    def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching pattern"""
        keys = self.client.keys(pattern)
        if keys:
            return self.client.delete(*keys)
        return 0

    def get_stock_price(self, symbol: str) -> Optional[dict]:
        """Get cached stock price"""
        return self.get(f"stock_price:{symbol}")

    def set_stock_price(self, symbol: str, price_data: dict, ttl: int = 300) -> bool:
        """Cache stock price (5 min default)"""
        return self.set(f"stock_price:{symbol}", price_data, ttl)

    def get_screener_results(self, screen_hash: str) -> Optional[list]:
        """Get cached screener results"""
        return self.get(f"screener:{screen_hash}")

    def set_screener_results(self, screen_hash: str, results: list, ttl: int = 3600) -> bool:
        """Cache screener results (1 hour default)"""
        return self.set(f"screener:{screen_hash}", results, ttl)


cache = RedisCache()

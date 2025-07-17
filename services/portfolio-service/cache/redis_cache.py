import redis
from lib_utils.config import get_config
import json
from datetime import timedelta

config = get_config()
redis_client = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    password=config.REDIS_PASSWORD,
    ssl=True,
    decode_responses=True
)

def get_cached_portfolio(portfolio_id: int) -> dict | None:
    """Fetch portfolio from Redis with 15min TTL"""
    if data := redis_client.get(f"portfolio:{portfolio_id}"):
        return json.loads(data)
    return None

def cache_portfolio(portfolio_id: int, data: dict, ttl: int = 900):
    """Cache portfolio in Redis with expiration"""
    redis_client.setex(
        name=f"portfolio:{portfolio_id}",
        time=timedelta(seconds=ttl),
        value=json.dumps(data)
    )
import redis

from src.utils.settings import settings


redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    ssl=settings.REDIS_SSL,
    decode_responses=True,
)
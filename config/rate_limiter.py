import os
import redis
from dotenv import load_dotenv
from fastapi import HTTPException, Request
from handlers.custom_exceptions import RateLimitException

load_dotenv()
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_LIMITER_DB = int(os.environ.get("REDIS_LIMITER_DB", 1))

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_LIMITER_DB,
    decode_responses=True
)


def bot_token_rate_limiter(limit: int = 20, ttl: int = 60):
    async def limiter_dep(request: Request):
        body = await request.json()
        bot_token = body.get("bot_token")
        if not bot_token:
            raise HTTPException(status_code=400, detail="Missing bot_token")

        key = f"bot-token-limit:{bot_token}"
        current = r.get(key)

        if current:
            if int(current) >= limit:
                raise RateLimitException(
                    status=429,
                    message="Rate limit exceeded for this Bot!"
                )
            else:
                r.incr(key)
        else:
            r.set(key, 1, ex=ttl)
    return limiter_dep

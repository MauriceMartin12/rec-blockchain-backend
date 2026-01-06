import os
import time
import redis
from fastapi import Request, HTTPException, status


def get_redis_client():
    redis_url = os.getenv("REDIS_URL")

    if not redis_url:
        raise RuntimeError("REDIS_URL is not set in environment variables")

    return redis.from_url(redis_url, decode_responses=True)


class RateLimiter:
    def __init__(
        self,
        max_requests: int,
        window_seconds: int,
        identifier: str = "default"
    ):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.identifier = identifier

    async def __call__(self, request: Request):
        redis_client = get_redis_client()  # ✅ ICI seulement

        client_ip = request.client.host
        endpoint = request.url.path
        current_time = int(time.time())

        key = f"rate_limit:{self.identifier}:{client_ip}:{endpoint}"

        pipeline = redis_client.pipeline()
        pipeline.zadd(key, {current_time: current_time})
        pipeline.zremrangebyscore(key, 0, current_time - self.window_seconds)
        pipeline.zcard(key)
        pipeline.expire(key, self.window_seconds)

        _, _, request_count, _ = pipeline.execute()

        if request_count > self.max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded",
                headers={
                    "X-RateLimit-Limit": str(self.max_requests),
                    "X-RateLimit-Remaining": "0",
                }
            )

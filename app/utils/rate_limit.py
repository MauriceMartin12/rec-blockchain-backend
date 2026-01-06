import time
import redis
from fastapi import Request, HTTPException, status

# Connexion Redis (à déplacer dans core/config si besoin)
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

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
            reset_time = redis_client.zrange(key, 0, 0, withscores=True)
            reset_in = (
                self.window_seconds - (current_time - int(reset_time[0][1]))
                if reset_time else self.window_seconds
            )

            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded",
                headers={
                    "X-RateLimit-Limit": str(self.max_requests),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(reset_in),
                }
            )

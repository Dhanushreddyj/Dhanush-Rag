"""
Rate limiting for FastAPI via dependency injection.
Prevents abuse by limiting requests per time window.
"""

import time
from typing import Dict, List
from fastapi import Request, HTTPException


class RateLimiter:
    """Simple in-memory rate limiter."""

    def __init__(self, max_requests: int = 60, window_seconds: float = 60.0):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: Dict[str, List[float]] = {}

    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        if client_id not in self._requests:
            self._requests[client_id] = []

        # Remove expired entries
        self._requests[client_id] = [
            ts for ts in self._requests[client_id]
            if now - ts < self.window_seconds
        ]

        if len(self._requests[client_id]) >= self.max_requests:
            return False

        self._requests[client_id].append(now)
        return True

    def get_remaining(self, client_id: str) -> int:
        now = time.time()
        if client_id not in self._requests:
            return self.max_requests

        active = [ts for ts in self._requests.get(client_id, []) if now - ts < self.window_seconds]
        return max(0, self.max_requests - len(active))


# Module-level singleton
_rate_limiter = RateLimiter(max_requests=60, window_seconds=60.0)


def get_rate_limiter() -> RateLimiter:
    return _rate_limiter


async def rate_limit_dependency(request: Request):
    """FastAPI dependency for rate limiting."""
    client_ip = request.client.host or "unknown"
    limiter = get_rate_limiter()

    if not limiter.is_allowed(client_ip):
        remaining = limiter.get_remaining(client_ip)
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
            headers={
                "Retry-After": str(int(limiter.window_seconds)),
                "X-Rate-Limit-Remaining": str(remaining),
            },
        )


def create_rate_limit_middleware(app):
    """Create rate limit middleware instance (for backward compatibility)."""
    # FastAPI handles dependencies via dependency injection, not ASGI middleware.
    return app

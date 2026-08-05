"""
Caching layer for RAG queries to reduce API calls and latency.
Uses in-memory LRU cache with TTL support.
"""

import json
import hashlib
from typing import Any, Optional
from datetime import datetime
from dataclasses import dataclass, field
from functools import wraps


@dataclass
class CacheEntry:
    """Represents a single cached entry."""
    value: Any
    created_at: datetime = field(default_factory=datetime.now)
    ttl_seconds: float = 300.0

    @property
    def is_expired(self) -> bool:
        return (datetime.now() - self.created_at).total_seconds() > self.ttl_seconds


class QueryCache:
    """Thread-safe in-memory LRU cache with TTL support."""

    def __init__(self, max_size: int = 1000, default_ttl: float = 300.0):
        self._cache: dict[str, CacheEntry] = {}
        self._access_order: list[str] = []
        self.max_size = max_size
        self.default_ttl = default_ttl

    def _make_key(self, query: str) -> str:
        return hashlib.md5(query.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        if key not in self._cache:
            return None
        entry = self._cache[key]
        if entry.is_expired:
            del self._cache[key]
            self._access_order.remove(key)
            return None
        # Update access order (LRU)
        if key in self._access_order:
            self._access_order.remove(key)
        self._access_order.append(key)
        return entry.value

    def set(self, key: str, value: Any, ttl: Optional[float] = None):
        # Evict expired entries on cache full
        if len(self._cache) >= self.max_size:
            oldest_key = next(iter(k for k in self._access_order))
            del self._cache[oldest_key]
            self._access_order.remove(oldest_key)

        ttl = ttl or self.default_ttl
        self._cache[key] = CacheEntry(value=value, created_at=datetime.now(), ttl_seconds=ttl)
        if key not in self._access_order:
            self._access_order.append(key)

    def clear(self):
        self._cache.clear()
        self._access_order.clear()

    def stats(self) -> dict[str, int]:
        return {
            "total_entries": len(self._cache),
            "max_size": self.max_size,
        }


# Module-level singleton
_query_cache = QueryCache(max_size=1000, default_ttl=300.0)


def get_query_cache() -> QueryCache:
    return _query_cache


def cache_result(ttl: Optional[float] = None):
    """Decorator to cache function results by query string."""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract query from args or kwargs
            query = None
            if len(args) > 0:
                query = str(args[0])
            elif "query" in kwargs:
                query = str(kwargs["query"])

            if not query:
                return await func(*args, **kwargs)

            key = get_query_cache()._make_key(query)
            cached = get_query_cache().get(key)
            if cached is not None:
                return cached

            result = await func(*args, **kwargs)
            ttl_val = ttl or 300.0
            get_query_cache().set(key, result, ttl=ttl_val)
            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            query = None
            if len(args) > 0:
                query = str(args[0])
            elif "query" in kwargs:
                query = str(kwargs["query"])

            if not query:
                return func(*args, **kwargs)

            key = get_query_cache()._make_key(query)
            cached = get_query_cache().get(key)
            if cached is not None:
                return cached

            result = func(*args, **kwargs)
            ttl_val = ttl or 300.0
            get_query_cache().set(key, result, ttl=ttl_val)
            return result

        # Support both sync and async usage
        import inspect
        if inspect.iscoroutinefunction(func):
            return wrapper
        else:
            return sync_wrapper

    return decorator


def clear_caching():
    """Clear all cached data."""
    get_query_cache().clear()


def get_cache_stats() -> dict[str, int]:
    """Get cache statistics."""
    return get_query_cache().stats()
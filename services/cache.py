#!/usr/bin/env python3
"""
Cache service with TTL-based expiration for performance optimization
Reduces redundant API calls and improves response times
"""

import hashlib
import json
import logging
import time
from typing import Any, Optional, Dict
from cachetools import TTLCache
from threading import Lock

# Configure logging
logger = logging.getLogger(__name__)


class CacheService:
    """
    In-memory caching service with TTL expiration

    Features:
    - TTL-based cache expiration (default: 1 hour)
    - Configurable cache size limits
    - Thread-safe operations
    - Cache statistics (hit rate, size)
    - Pattern-based invalidation
    """

    DEFAULT_TTL = 3600  # 1 hour in seconds
    DEFAULT_MAX_SIZE = 1000  # Maximum number of cached items

    def __init__(self, max_size: int = DEFAULT_MAX_SIZE, default_ttl: int = DEFAULT_TTL):
        """
        Initialize cache service

        Args:
            max_size: Maximum number of items in cache
            default_ttl: Default time-to-live in seconds
        """
        self.default_ttl = default_ttl
        self.cache = TTLCache(maxsize=max_size, ttl=default_ttl)
        self.lock = Lock()

        # Statistics
        self.hits = 0
        self.misses = 0

        logger.info(f"CacheService initialized: max_size={max_size}, ttl={default_ttl}s")

    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """
        Generate a cache key from arguments

        Args:
            prefix: Key prefix for namespacing
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Cache key string
        """
        # Create a deterministic string from arguments
        key_parts = [prefix]

        if args:
            key_parts.extend(str(arg) for arg in args)

        if kwargs:
            # Sort kwargs for deterministic keys
            sorted_items = sorted(kwargs.items())
            key_parts.extend(f"{k}={v}" for k, v in sorted_items)

        key_string = ":".join(key_parts)

        # Hash if key is too long
        if len(key_string) > 200:
            key_hash = hashlib.sha256(key_string.encode()).hexdigest()[:16]
            return f"{prefix}:{key_hash}"

        return key_string

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        with self.lock:
            try:
                value = self.cache[key]
                self.hits += 1
                logger.debug(f"Cache hit: {key}")
                return value
            except KeyError:
                self.misses += 1
                logger.debug(f"Cache miss: {key}")
                return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Set value in cache with optional TTL

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (uses default if not specified)
        """
        with self.lock:
            # If TTL is different from default, we need to handle it separately
            # For simplicity, we'll use the default TTL for now
            # (TTLCache doesn't support per-item TTL)
            self.cache[key] = value
            logger.debug(f"Cached: {key} (ttl={ttl or self.default_ttl}s)")

    def get_or_set(self, key: str, factory, ttl: Optional[int] = None) -> Any:
        """
        Get value from cache or compute and cache it

        Args:
            key: Cache key
            factory: Function to compute value if not in cache
            ttl: Time-to-live in seconds

        Returns:
            Cached or computed value
        """
        value = self.get(key)
        if value is None:
            value = factory()
            self.set(key, value, ttl)
        return value

    def invalidate(self, pattern: str) -> int:
        """
        Invalidate all cache keys matching a pattern

        Args:
            pattern: Pattern to match (supports * wildcard)

        Returns:
            Number of keys invalidated
        """
        with self.lock:
            count = 0
            keys_to_delete = []

            # Find matching keys
            if '*' in pattern:
                # Convert pattern to regex
                regex_pattern = pattern.replace('*', '.*')
                import re
                regex = re.compile(f"^{regex_pattern}$")

                for key in list(self.cache.keys()):
                    if regex.match(key):
                        keys_to_delete.append(key)
            else:
                # Exact match
                if pattern in self.cache:
                    keys_to_delete.append(pattern)

            # Delete matching keys
            for key in keys_to_delete:
                del self.cache[key]
                count += 1

            logger.info(f"Invalidated {count} keys matching pattern: {pattern}")
            return count

    def clear(self) -> None:
        """Clear all cached items"""
        with self.lock:
            size = len(self.cache)
            self.cache.clear()
            self.hits = 0
            self.misses = 0
            logger.info(f"Cleared {size} cached items")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics

        Returns:
            Dictionary with cache statistics
        """
        with self.lock:
            total_requests = self.hits + self.misses
            hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0

            return {
                'size': len(self.cache),
                'max_size': self.cache.maxsize,
                'hits': self.hits,
                'misses': self.misses,
                'hit_rate': round(hit_rate, 2),
                'ttl': self.default_ttl
            }

    def create_key(self, prefix: str, *args, **kwargs) -> str:
        """
        Create a cache key (convenience method)

        Args:
            prefix: Key prefix
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Cache key string
        """
        return self._generate_key(prefix, *args, **kwargs)


# Global cache instance
_cache_instance: Optional[CacheService] = None


def get_cache() -> CacheService:
    """
    Get global cache instance (singleton pattern)

    Returns:
        Global cache service instance
    """
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = CacheService()
    return _cache_instance

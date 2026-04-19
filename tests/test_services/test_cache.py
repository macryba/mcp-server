#!/usr/bin/env python3
"""
Unit tests for cache service
"""

import pytest
import time
from services.cache import CacheService, get_cache


@pytest.fixture
def cache():
    """Fixture for cache service"""
    cache = CacheService(max_size=100, default_ttl=1)
    yield cache
    cache.clear()


def test_cache_initialization(cache):
    """Test cache initialization"""
    assert cache.default_ttl == 1
    assert cache.cache.maxsize == 100
    assert cache.hits == 0
    assert cache.misses == 0


def test_cache_set_and_get(cache):
    """Test basic set and get operations"""
    cache.set("test_key", "test_value")
    assert cache.get("test_key") == "test_value"


def test_cache_get_nonexistent(cache):
    """Test getting non-existent key"""
    assert cache.get("nonexistent") is None


def test_cache_miss_increments_counter(cache):
    """Test that cache miss increments miss counter"""
    cache.get("nonexistent")
    assert cache.misses == 1


def test_cache_hit_increments_counter(cache):
    """Test that cache hit increments hit counter"""
    cache.set("test_key", "test_value")
    cache.get("test_key")
    assert cache.hits == 1


def test_cache_key_generation(cache):
    """Test cache key generation"""
    key1 = cache.create_key("prefix", "arg1", "arg2", param="value")
    key2 = cache.create_key("prefix", "arg1", "arg2", param="value")
    key3 = cache.create_key("prefix", "arg1", "different", param="value")

    assert key1 == key2
    assert key1 != key3


def test_cache_invalidate_exact_match(cache):
    """Test invalidating exact key"""
    cache.set("test_key", "value")
    count = cache.invalidate("test_key")
    assert count == 1
    assert cache.get("test_key") is None


def test_cache_invalidate_pattern(cache):
    """Test invalidating keys by pattern"""
    cache.set("search:test1", "value1")
    cache.set("search:test2", "value2")
    cache.set("other:key", "value3")

    count = cache.invalidate("search:*")
    assert count == 2
    assert cache.get("search:test1") is None
    assert cache.get("search:test2") is None
    assert cache.get("other:key") == "value3"


def test_cache_clear(cache):
    """Test clearing all cache"""
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.clear()
    assert cache.get("key1") is None
    assert cache.get("key2") is None


def test_cache_stats(cache):
    """Test cache statistics"""
    cache.set("key1", "value1")
    cache.set("key2", "value2")

    # Generate some hits and misses
    cache.get("key1")  # hit
    cache.get("key2")  # hit
    cache.get("nonexistent")  # miss

    stats = cache.get_stats()
    assert stats['size'] == 2
    assert stats['hits'] == 2
    assert stats['misses'] == 1
    assert stats['hit_rate'] == 66.67  # 2/3
    assert stats['max_size'] == 100


def test_cache_get_or_set(cache):
    """Test get_or_set method"""
    call_count = 0

    def factory():
        nonlocal call_count
        call_count += 1
        return "computed_value"

    # First call should use factory
    result1 = cache.get_or_set("test_key", factory)
    assert result1 == "computed_value"
    assert call_count == 1

    # Second call should use cache
    result2 = cache.get_or_set("test_key", factory)
    assert result2 == "computed_value"
    assert call_count == 1  # Factory not called again


def test_cache_ttl_expiration():
    """Test TTL-based expiration"""
    cache = CacheService(max_size=100, default_ttl=1)  # 1 second TTL
    cache.set("test_key", "test_value")
    assert cache.get("test_key") == "test_value"

    # Wait for expiration
    time.sleep(1.1)
    assert cache.get("test_key") is None


def test_global_cache_singleton():
    """Test global cache singleton pattern"""
    cache1 = get_cache()
    cache2 = get_cache()
    assert cache1 is cache2


def test_cache_key_hashing_for_long_keys(cache):
    """Test that long keys are hashed"""
    long_key = "prefix:" + "x" * 250
    generated_key = cache.create_key(long_key)
    assert len(generated_key) < 100  # Should be hashed
    assert "prefix:" in generated_key

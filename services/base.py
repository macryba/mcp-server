#!/usr/bin/env python3
"""
Base service class for all domain services
Provides common interface and functionality for search and extraction
"""

import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

from services.http_client import HTTPClient, HTTPClientError
from services.cache import CacheService, get_cache

# Configure logging
logger = logging.getLogger(__name__)


class BaseDomainService(ABC):
    """
    Abstract base class for all domain services

    All domain services (Wikipedia, IPN, Dzieje, etc.) must inherit from this class
    and implement the required methods.

    Features:
    - Standardized search interface
    - Standardized extract interface
    - Common error handling
    - Integrated HTTP client
    - Integrated cache service
    - Logging support
    """

    def __init__(self, name: str, http_client: Optional[HTTPClient] = None, cache_service: Optional[CacheService] = None):
        """
        Initialize domain service

        Args:
            name: Service name (e.g., 'wikipedia', 'ipn')
            http_client: HTTP client instance (creates new one if not provided)
            cache_service: Cache service instance (uses global if not provided)
        """
        self.name = name
        self.http_client = http_client or HTTPClient()
        self.cache = cache_service or get_cache()

        logger.info(f"Initialized {self.name} service")

    @abstractmethod
    async def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search the domain for matching content

        Args:
            query: Search query string
            limit: Maximum number of results to return

        Returns:
            List of search results with keys: title, url, snippet, source, metadata

        Raises:
            HTTPClientError: If search request fails
        """
        pass

    @abstractmethod
    async def extract_content(self, url: str) -> Dict[str, Any]:
        """
        Extract full content from a URL

        Args:
            url: URL to extract content from

        Returns:
            Dictionary with keys: title, content, url, metadata

        Raises:
            HTTPClientError: If extraction request fails
        """
        pass

    def _create_search_cache_key(self, query: str, limit: int) -> str:
        """
        Create cache key for search results

        Args:
            query: Search query
            limit: Result limit

        Returns:
            Cache key string
        """
        return self.cache.create_key(f"{self.name}:search", query, limit=limit)

    def _create_extract_cache_key(self, url: str) -> str:
        """
        Create cache key for extracted content

        Args:
            url: URL to extract

        Returns:
            Cache key string
        """
        return self.cache.create_key(f"{self.name}:extract", url)

    async def _cached_search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Perform search with caching

        Args:
            query: Search query
            limit: Result limit

        Returns:
            List of search results
        """
        cache_key = self._create_search_cache_key(query, limit)

        # Try cache first
        cached_result = self.cache.get(cache_key)
        if cached_result is not None:
            logger.debug(f"Cache hit for search: {query}")
            return cached_result

        # Perform search
        logger.debug(f"Cache miss for search: {query}, performing search")
        results = await self.search(query, limit)

        # Cache results
        self.cache.set(cache_key, results)

        return results

    async def _cached_extract(self, url: str) -> Dict[str, Any]:
        """
        Perform content extraction with caching

        Args:
            url: URL to extract

        Returns:
            Extracted content
        """
        cache_key = self._create_extract_cache_key(url)

        # Try cache first
        cached_result = self.cache.get(cache_key)
        if cached_result is not None:
            logger.debug(f"Cache hit for extract: {url}")
            return cached_result

        # Perform extraction
        logger.debug(f"Cache miss for extract: {url}, performing extraction")
        content = await self.extract_content(url)

        # Cache results
        self.cache.set(cache_key, content)

        return content

    async def close(self):
        """Close the service and cleanup resources"""
        await self.http_client.close()
        logger.info(f"Closed {self.name} service")

    async def __aenter__(self):
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()

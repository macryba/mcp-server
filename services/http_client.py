#!/usr/bin/env python3
"""
HTTP client service with retry logic, timeouts, and proper error handling
Provides centralized HTTP request handling for all domain services
"""

import httpx
import logging
from typing import Optional, Dict, Any
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

# Configure logging
logger = logging.getLogger(__name__)


class HTTPClientError(Exception):
    """Custom exception for HTTP client errors"""
    pass


class HTTPClient:
    """
    Centralized HTTP client with retry logic and error handling

    Features:
    - Automatic retry with exponential backoff
    - Configurable timeouts
    - Proper user-agent headers
    - Request/response logging
    - Connection pooling via httpx
    """

    DEFAULT_TIMEOUT = 10  # seconds
    MAX_RETRIES = 3
    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

    def __init__(self, timeout: int = DEFAULT_TIMEOUT, max_retries: int = MAX_RETRIES):
        """
        Initialize HTTP client

        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.headers = {
            'User-Agent': self.USER_AGENT,
            'Accept': 'application/json, text/html',
            'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7'
        }

        # Create async client with connection pooling
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            headers=self.headers,
            follow_redirects=True,
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.RequestError))
    )
    async def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform GET request with retry logic

        Args:
            url: Request URL
            params: Query parameters

        Returns:
            Response data as dictionary

        Raises:
            HTTPClientError: If request fails after retries
        """
        try:
            logger.debug(f"GET request: {url} with params: {params}")

            response = await self.client.get(url, params=params)
            response.raise_for_status()

            # Try to parse JSON, fallback to text
            try:
                data = response.json()
            except ValueError:
                data = {'text': response.text, 'status_code': response.status_code}

            logger.debug(f"GET response: status={response.status_code}, size={len(response.content)}")

            return data

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP status error: {e.response.status_code} for {url}")
            raise HTTPClientError(f"HTTP error {e.response.status_code}: {e}") from e
        except httpx.RequestError as e:
            logger.error(f"Request error for {url}: {e}")
            raise HTTPClientError(f"Request failed: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error in GET request to {url}: {e}")
            raise HTTPClientError(f"Unexpected error: {e}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.RequestError))
    )
    async def post(self, url: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform POST request with retry logic

        Args:
            url: Request URL
            data: Form data
            json_data: JSON data

        Returns:
            Response data as dictionary

        Raises:
            HTTPClientError: If request fails after retries
        """
        try:
            logger.debug(f"POST request: {url}")

            # Use json_data if provided, otherwise use data
            if json_data:
                response = await self.client.post(url, json=json_data)
            else:
                response = await self.client.post(url, data=data)

            response.raise_for_status()

            # Try to parse JSON, fallback to text
            try:
                result = response.json()
            except ValueError:
                result = {'text': response.text, 'status_code': response.status_code}

            logger.debug(f"POST response: status={response.status_code}")

            return result

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP status error: {e.response.status_code} for {url}")
            raise HTTPClientError(f"HTTP error {e.response.status_code}: {e}") from e
        except httpx.RequestError as e:
            logger.error(f"Request error for {url}: {e}")
            raise HTTPClientError(f"Request failed: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error in POST request to {url}: {e}")
            raise HTTPClientError(f"Unexpected error: {e}") from e

    async def close(self):
        """Close the HTTP client connection"""
        await self.client.aclose()

    async def __aenter__(self):
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()

#!/usr/bin/env python3
"""
Wikipedia domain service
Refactored from original wikipedia_client.py to use BaseDomainService
"""

import re
from typing import List, Dict, Any
from urllib.parse import quote

from services.base import BaseDomainService
from services.http_client import HTTPClient
from services.cache import CacheService


class WikipediaService(BaseDomainService):
    """
    Wikipedia domain service for search and content extraction

    Supports multiple Wikipedia language editions
    """

    def __init__(self, language: str = 'pl', http_client: HTTPClient = None, cache_service: CacheService = None):
        """
        Initialize Wikipedia service

        Args:
            language: Wikipedia language code (e.g., 'pl', 'en')
            http_client: HTTP client instance
            cache_service: Cache service instance
        """
        super().__init__(f"wikipedia_{language}", http_client, cache_service)
        self.language = language
        self.base_url = f"https://{language}.wikipedia.org"
        self.api_url = f"{self.base_url}/w/api.php"

    async def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search Wikipedia using MediaWiki API

        Args:
            query: Search query string
            limit: Maximum number of results

        Returns:
            List of search results with title, snippet, url, source, metadata
        """
        params = {
            'action': 'query',
            'list': 'search',
            'srsearch': query,
            'format': 'json',
            'utf8': 1,
            'srlimit': limit
        }

        try:
            data = await self.http_client.get(self.api_url, params=params)

            results = []
            for item in data.get('query', {}).get('search', []):
                title = item['title']
                # Clean up HTML snippets
                snippet = re.sub('<[^<]+?>', '', item.get('snippet', ''))
                url = f"{self.base_url}/wiki/{quote(title.replace(' ', '_'))}"

                results.append({
                    'title': title,
                    'snippet': snippet,
                    'url': url,
                    'source': f'wikipedia_{self.language}',
                    'relevance_score': item.get('wordcount', 0) / 1000.0,  # Simple relevance metric
                    'metadata': {
                        'wordcount': item.get('wordcount', 0),
                        'timestamp': item.get('timestamp', ''),
                        'language': self.language
                    }
                })

            return results

        except Exception as e:
            return [{
                'error': str(e),
                'source': f'wikipedia_{self.language}',
                'query': query
            }]

    async def extract_content(self, url: str) -> Dict[str, Any]:
        """
        Extract full page content from Wikipedia

        Args:
            url: Wikipedia page URL

        Returns:
            Dictionary with title, content, url, metadata
        """
        # Extract page title from URL
        # URL format: https://pl.wikipedia.org/wiki/Page_Title
        if '/wiki/' in url:
            title = url.split('/wiki/')[-1].replace('_', ' ')
        else:
            return {
                'error': 'Invalid Wikipedia URL format',
                'url': url,
                'source': f'wikipedia_{self.language}'
            }

        params = {
            'action': 'query',
            'prop': 'extracts|pageprops',
            'exintro': True,
            'explaintext': True,
            'titles': title,
            'format': 'json',
            'utf8': 1
        }

        try:
            data = await self.http_client.get(self.api_url, params=params)

            pages = data.get('query', {}).get('pages', {})
            page_id = next(iter(pages))

            if page_id == '-1':
                return {
                    'error': 'Page not found',
                    'url': url,
                    'source': f'wikipedia_{self.language}'
                }

            page_data = pages[page_id]

            return {
                'title': page_data.get('title', ''),
                'content': page_data.get('extract', ''),
                'url': url,
                'source': f'wikipedia_{self.language}',
                'metadata': {
                    'pageid': page_data.get('pageid', ''),
                    'language': self.language,
                    'full_url': url
                }
            }

        except Exception as e:
            return {
                'error': str(e),
                'url': url,
                'source': f'wikipedia_{self.language}'
            }

    async def search_by_domain(self, query: str, domains: List[str]) -> List[Dict[str, Any]]:
        """
        Search Wikipedia and filter results (for compatibility)

        Args:
            query: Search query
            domains: List of domains (ignored, always Wikipedia)

        Returns:
            List of search results
        """
        return await self.search(query)

    async def get_page_content(self, title: str) -> Dict[str, Any]:
        """
        Get full page content by title (compatibility method)

        Args:
            title: Page title

        Returns:
            Page content dictionary
        """
        url = f"{self.base_url}/wiki/{quote(title.replace(' ', '_'))}"
        return await self.extract_content(url)

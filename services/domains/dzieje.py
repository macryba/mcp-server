#!/usr/bin/env python3
"""
Dzieje.pl domain service
Provides content extraction and search capabilities for Dzieje.pl historical portal
"""

import re
from typing import List, Dict, Any
from urllib.parse import quote, urljoin
from bs4 import BeautifulSoup

from services.base import BaseDomainService
from services.http_client import HTTPClient
from services.cache import CacheService
import logging

logger = logging.getLogger(__name__)


class DziejeService(BaseDomainService):
    """
    Dzieje.pl domain service for historical content

    Note: Dzieje.pl blocks /search/ in robots.txt and doesn't provide public API.
    This service implements content extraction and basic search via web scraping
    with respectful delays and caching.
    """

    def __init__(self, http_client: HTTPClient = None, cache_service: CacheService = None):
        """
        Initialize Dzieje.pl service

        Args:
            http_client: HTTP client instance
            cache_service: Cache service instance
        """
        super().__init__("dzieje", http_client, cache_service)
        self.base_url = "https://dzieje.pl"
        self.search_url = f"{self.base_url}/szukaj"

    async def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search Dzieje.pl using web scraping

        Note: Dzieje.pl search functionality has known limitations:
        - Search results may not be relevant to the query
        - Site appears to return random/latest articles regardless of search terms
        - For specific historical figures, consider using direct URLs if known
        - May be affected by robots.txt restrictions - use sparingly

        Args:
            query: Search query string
            limit: Maximum number of results

        Returns:
            List of search results
        """
        # Dzieje.pl uses Drupal search with query parameters
        search_params = {
            'search_api_views_fulltext': query,
            'sort_by': 'search_api_relevance',
            'sort_order': 'DESC'
        }

        try:
            # Try to access search results page
            response = await self.http_client.get(self.search_url, params=search_params)

            # Extract HTML content from response
            html_content = response.get('text', '') if isinstance(response, dict) else str(response)

            if not html_content:
                return [{
                    'error': 'No content returned from Dzieje.pl',
                    'source': 'dzieje',
                    'query': query
                }]

            # Parse HTML content
            soup = BeautifulSoup(html_content, 'html.parser')

            results = []

            # Use the correct CSS selector for Dzieje.pl search results
            search_items = soup.find_all('div', class_='views-row')

            for item in search_items[:limit]:
                try:
                    # Extract title using correct selector
                    title_elem = item.select_one('div.views-field-title a')
                    title = title_elem.get_text(strip=True) if title_elem else "Bez tytułu"

                    # Extract URL
                    url_elem = item.select_one('div.views-field-title a')
                    if url_elem and url_elem.get('href'):
                        url = urljoin(self.base_url, url_elem['href'])
                    else:
                        continue  # Skip items without URL

                    # Try to extract snippet/description
                    # Dzieje.pl search results may not have snippets, so we use basic text
                    snippet_elem = item.select_one('div.views-field-field-description')
                    if snippet_elem:
                        snippet = snippet_elem.get_text(strip=True)
                    else:
                        # Fallback to general text content
                        snippet = item.get_text(strip=True)[:200]
                        snippet = re.sub(r'\s+', ' ', snippet).strip()

                    # Check if result is relevant to query
                    item_text = item.get_text().lower()
                    query_lower = query.lower()
                    # Basic relevance check - does query appear in the text?
                    if query_lower not in item_text and len(query_lower) > 3:
                        # Skip clearly irrelevant results
                        continue

                    # Extract metadata
                    metadata = {
                        'language': 'pl',
                        'domain': 'dzieje.pl',
                        'query_matched': query_lower in item_text
                    }

                    results.append({
                        'title': title,
                        'snippet': snippet[:300] if len(snippet) > 300 else snippet,
                        'url': url,
                        'source': 'dzieje',
                        'relevance_score': 0.7 if query_lower in item_text else 0.5,
                        'metadata': metadata
                    })
                except Exception as e:
                    logger.warning(f"Error parsing search result item: {e}")
                    continue

            return results if results else [{
                'error': 'No results found or search blocked',
                'source': 'dzieje',
                'query': query,
                'note': 'Dzieje.pl may be blocking automated search requests'
            }]

        except Exception as e:
            return [{
                'error': str(e),
                'source': 'dzieje',
                'query': query,
                'note': 'Search request failed - site may be blocking automated access'
            }]

    async def extract_content(self, url: str) -> Dict[str, Any]:
        """
        Extract full article content from Dzieje.pl URL

        Args:
            url: Dzieje.pl article URL

        Returns:
            Dictionary with extracted content
        """
        try:
            response = await self.http_client.get(url)

            # Extract HTML content from response
            html_content = response.get('text', '') if isinstance(response, dict) else str(response)

            if not html_content:
                return {
                    'error': 'No content returned',
                    'url': url,
                    'source': 'dzieje'
                }

            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract title
            title_elem = soup.find('h1') or soup.find('title')
            title = title_elem.get_text(strip=True) if title_elem else ""

            # Extract main content
            # Dzieje.pl uses article tag for main content
            content_elem = (
                soup.find('article') or
                soup.find('main') or
                soup.find('div', class_=re.compile(r'content|article-body|field-name-body'))
            )

            if content_elem:
                # Remove unwanted elements
                for unwanted in content_elem.find_all(['script', 'style', 'nav', 'aside', 'footer']):
                    unwanted.decompose()

                content = content_elem.get_text(separator='\n', strip=True)
                content = re.sub(r'\n{3,}', '\n\n', content)  # Clean up excessive newlines
            else:
                content = ""

            # Extract metadata
            metadata = {
                'url': url,
                'language': 'pl',
                'domain': 'dzieje.pl',
                'word_count': len(content.split()) if content else 0
            }

            # Try to extract author
            author_elem = soup.find(['span', 'div'], class_=re.compile(r'author|autor'))
            if author_elem:
                metadata['author'] = author_elem.get_text(strip=True)

            # Try to extract date
            date_elem = soup.find(['time', 'span'], class_=re.compile(r'date|data'))
            if date_elem:
                metadata['date'] = date_elem.get('datetime') or date_elem.get_text(strip=True)

            return {
                'title': title,
                'content': content,
                'url': url,
                'source': 'dzieje',
                'metadata': metadata
            }

        except Exception as e:
            return {
                'error': str(e),
                'url': url,
                'source': 'dzieje'
            }

    async def search_by_domain(self, query: str, domains: List[str]) -> List[Dict[str, Any]]:
        """
        Search Dzieje.pl and filter results (for compatibility)

        Args:
            query: Search query
            domains: List of domains (ignored, always Dzieje.pl)

        Returns:
            List of search results
        """
        return await self.search(query)

    async def get_page_content(self, title: str) -> Dict[str, Any]:
        """
        Get page content by title (compatibility method)

        Note: Dzieje.pl doesn't have direct title-to-URL mapping like Wikipedia.
        This method performs a search and returns the first result's content.

        Args:
            title: Page title to search for

        Returns:
            Page content dictionary
        """
        search_results = await self.search(title, limit=1)

        if search_results and 'url' in search_results[0]:
            url = search_results[0]['url']
            return await self.extract_content(url)
        else:
            return {
                'error': f'No results found for title: {title}',
                'source': 'dzieje'
            }

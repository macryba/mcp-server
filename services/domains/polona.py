#!/usr/bin/env python3
"""
Polona domain service
Provides content extraction and search capabilities for Polona digital library
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


class PolonaService(BaseDomainService):
    """
    Polona domain service for digital library collections

    Uses official Polona API for search and content extraction.
    API endpoints:
    - Simple search: POST /api/search-service/search/simple
    - Advanced search: POST /api/search-service/search/advanced
    - Fulltext search: POST /api/search-service/fulltext/polona/fulltext/{page}/{pageSize}
    """

    def __init__(self, http_client: HTTPClient = None, cache_service: CacheService = None):
        """
        Initialize Polona service

        Args:
            http_client: HTTP client instance
            cache_service: Cache service instance
        """
        super().__init__("polona", http_client, cache_service)
        self.base_url = "https://polona.pl"
        self.api_base = "https://polona.pl/api/search-service"
        self.simple_search_url = f"{self.api_base}/search/simple"

    async def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search Polona using official API

        Uses Polona's simple search API endpoint with proper query parameters.

        Args:
            query: Search query string
            limit: Maximum number of results

        Returns:
            List of search results from Polona API
        """
        try:
            # Build URL parameters for simple search
            page_size = min(limit, 50)  # API limit

            # Use httpx directly for POST with params
            import httpx

            # Build params dict
            params = {
                'query': query,
                'page': 0,
                'pageSize': page_size,
                'sort': 'RELEVANCE'
            }

            # Make POST request with params in URL and empty JSON body
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(
                    self.simple_search_url,
                    params=params,
                    json={},
                    headers={'Content-Type': 'application/json'}
                )

                if response.status_code != 200:
                    logger.error(f"Polona API returned {response.status_code}")
                    return [{
                        'error': f'API returned status {response.status_code}',
                        'source': 'polona',
                        'query': query
                    }]

                response_data = response.json()

            if not response_data or 'hits' not in response_data:
                return [{
                    'error': 'Invalid response from Polona API',
                    'source': 'polona',
                    'query': query
                }]

            results = []

            # Parse API response
            for hit in response_data.get('hits', []):
                try:
                    # Extract fields from nested structure
                    basic_fields = hit.get('basicFields', {})
                    expanded_fields = hit.get('expandedFields', {})

                    # Extract title from basicFields
                    title_data = basic_fields.get('title', {})
                    if isinstance(title_data, dict):
                        title = title_data.get('values', ['Bez tytułu'])[0]
                    else:
                        title = str(title_data) if title_data else 'Bez tytułu'

                    # Extract URL from objectId
                    object_id = hit.get('objectId', '')
                    if object_id:
                        url = f"{self.base_url}/api/entities/{object_id}"
                    else:
                        # Fallback: try url field
                        url = hit.get('url', '')
                        if not url:
                            continue  # Skip items without URL

                    # Ensure URL is absolute
                    if not url.startswith('http'):
                        url = urljoin(self.base_url, url)

                    # Build description from available fields
                    snippet_parts = []

                    # Date
                    date_data = basic_fields.get('dateDescriptive', {})
                    if isinstance(date_data, dict):
                        date_values = date_data.get('values', [])
                        if date_values:
                            snippet_parts.append(f"Data: {date_values[0]}")

                    # Author/Creator
                    author_data = basic_fields.get('author', {})
                    if isinstance(author_data, dict):
                        author_values = author_data.get('values', [])
                        if author_values:
                            snippet_parts.append(f"Autor: {author_values[0]}")

                    # Publisher
                    publisher_data = expanded_fields.get('publisher', {})
                    if isinstance(publisher_data, dict):
                        publisher_values = publisher_data.get('values', [])
                        if publisher_values:
                            snippet_parts.append(f"Wydawca: {publisher_values[0]}")

                    # Publish place
                    place_data = expanded_fields.get('publishPlace', {})
                    if isinstance(place_data, dict):
                        place_values = place_data.get('values', [])
                        if place_values:
                            snippet_parts.append(f"Miejsce: {place_values[0]}")

                    # Description
                    description_data = expanded_fields.get('description', {})
                    if isinstance(description_data, dict):
                        desc_values = description_data.get('values', [])
                        if desc_values:
                            snippet_parts.append(desc_values[0])

                    snippet = '; '.join(snippet_parts) if snippet_parts else ""

                    # Extract metadata
                    metadata = {
                        'language': 'pl',
                        'domain': 'polona.pl',
                        'source_type': 'digital_library'
                    }

                    # Add additional metadata
                    if date_values:
                        metadata['date'] = date_values[0]
                    if author_values:
                        metadata['author'] = author_values[0]
                    if place_values:
                        metadata['publish_place'] = place_values[0]
                    if publisher_values:
                        metadata['publisher'] = publisher_values[0]

                    # Add format/type if available
                    format_data = basic_fields.get('format', {})
                    if isinstance(format_data, dict):
                        format_values = format_data.get('values', [])
                        if format_values:
                            metadata['format'] = format_values[0]

                    # Calculate relevance score based on position
                    position = response_data.get('hits', []).index(hit) if hit in response_data.get('hits', []) else 0
                    relevance_score = max(0.1, 1.0 - (position * 0.1))

                    results.append({
                        'title': title,
                        'snippet': snippet[:500] if len(snippet) > 500 else snippet,
                        'url': url,
                        'source': 'polona',
                        'relevance_score': relevance_score,
                        'metadata': metadata
                    })
                except Exception as e:
                    logger.warning(f"Error parsing Polona API result: {e}")
                    continue

            # Add search metadata
            search_metadata = {
                'total_results': response_data.get('totalElements', len(results)),
                'page': response_data.get('number', 0),
                'page_size': response_data.get('size', len(results)),
                'total_pages': response_data.get('totalPages', 1)
            }

            if results:
                results[0]['search_metadata'] = search_metadata

            return results

        except Exception as e:
            logger.error(f"Error searching Polona API: {e}")
            return [{
                'error': str(e),
                'source': 'polona',
                'query': query,
                'note': 'API search request failed'
            }]

    async def extract_content(self, url: str) -> Dict[str, Any]:
        """
        Extract full item content from Polona URL

        Args:
            url: Polona item URL

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
                    'source': 'polona'
                }

            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract title
            title_elem = soup.find('h1') or soup.find('title')
            title = title_elem.get_text(strip=True) if title_elem else ""

            # Extract main content/description
            content_elem = (
                soup.find('div', class_=re.compile(r'description|content|item-info')) or
                soup.find('article') or
                soup.find('main')
            )

            if content_elem:
                # Remove unwanted elements
                for unwanted in content_elem.find_all(['script', 'style', 'nav', 'aside', 'footer']):
                    unwanted.decompose()

                content = content_elem.get_text(separator='\n', strip=True)
                content = re.sub(r'\n{3,}', '\n\n', content)
            else:
                content = ""

            # Extract metadata
            metadata = {
                'url': url,
                'language': 'pl',
                'domain': 'polona.pl',
                'word_count': len(content.split()) if content else 0
            }

            # Try to extract author
            author_elem = soup.find(['span', 'div'], class_=re.compile(r'author|creator'))
            if author_elem:
                metadata['author'] = author_elem.get_text(strip=True)

            # Try to extract date/year
            date_elem = soup.find(['time', 'span'], class_=re.compile(r'date|year'))
            if date_elem:
                metadata['date'] = date_elem.get('datetime') or date_elem.get_text(strip=True)

            # Try to extract item type (book, photo, document, etc.)
            type_elem = soup.find(['span', 'div'], class_=re.compile(r'type|kind'))
            if type_elem:
                metadata['item_type'] = type_elem.get_text(strip=True)

            return {
                'title': title,
                'content': content,
                'url': url,
                'source': 'polona',
                'metadata': metadata
            }

        except Exception as e:
            logger.error(f"Error extracting content from Polona: {e}")
            return {
                'error': str(e),
                'url': url,
                'source': 'polona'
            }

    async def search_by_domain(self, query: str, domains: List[str]) -> List[Dict[str, Any]]:
        """
        Search Polona and filter results (for compatibility)

        Args:
            query: Search query
            domains: List of domains (ignored, always Polona)

        Returns:
            List of search results
        """
        return await self.search(query)

    async def get_page_content(self, title: str) -> Dict[str, Any]:
        """
        Get page content by title (compatibility method)

        Note: Polona doesn't have direct title-to-URL mapping.
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
                'source': 'polona'
            }

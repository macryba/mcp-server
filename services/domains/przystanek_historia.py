#!/usr/bin/env python3
"""
Przystanek Historia domain service
Provides content extraction and search capabilities for Przystanek Historia portal
"""

import re
from typing import List, Dict, Any
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from services.base import BaseDomainService
from services.http_client import HTTPClient
from services.cache import CacheService
import logging

logger = logging.getLogger(__name__)


class PrzystanekHistoriaService(BaseDomainService):
    """
    Przystanek Historia domain service for historical articles and multimedia

    Note: Przystanek Historia focuses on 20th century Polish history.
    This service implements content extraction and search via web scraping.
    """

    def __init__(self, http_client: HTTPClient = None, cache_service: CacheService = None):
        """
        Initialize Przystanek Historia service

        Args:
            http_client: HTTP client instance
            cache_service: Cache service instance
        """
        super().__init__("przystanek_historia", http_client, cache_service)
        self.base_url = "https://przystanekhistoria.pl"

    async def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search Przystanek Historia portal

        Args:
            query: Search query string
            limit: Maximum number of results

        Returns:
            List of search results
        """
        try:
            # Try the main page or texts section
            response = await self.http_client.get(f"{self.base_url}/pa2/teksty")

            html_content = response.get('text', '') if isinstance(response, dict) else str(response)

            if not html_content:
                return [{
                    'error': 'No content returned from Przystanek Historia',
                    'source': 'przystanek_historia',
                    'query': query
                }]

            soup = BeautifulSoup(html_content, 'html.parser')

            results = []

            # Przystanek Historia structure
            text_items = (
                soup.find_all('div', class_='text-item') or
                soup.find_all('article') or
                soup.find_all('div', class_=re.compile(r'article|post|entry'))
            )

            # Filter by query relevance
            query_lower = query.lower()

            for item in text_items[:limit * 3]:
                try:
                    item_text = item.get_text().lower()

                    # Basic relevance filter
                    if query_lower not in item_text and len(query_lower) > 3:
                        continue

                    # Extract title
                    title_elem = item.find(['h2', 'h3']) or item.find('a', class_=re.compile(r'title'))
                    title = title_elem.get_text(strip=True) if title_elem else "Bez tytułu"

                    # Extract URL
                    url_elem = item.find('a', href=True)
                    if url_elem:
                        url = urljoin(self.base_url, url_elem['href'])
                    else:
                        continue

                    # Extract description/preview
                    desc_elem = item.find(['p', 'div'], class_=re.compile(r'excerpt|summary|preview'))
                    description = desc_elem.get_text(strip=True) if desc_elem else ""

                    # Extract metadata
                    metadata = {
                        'language': 'pl',
                        'domain': 'przystanekhistoria.pl',
                        'source_type': 'historical_articles'
                    }

                    # Try to extract author
                    author_elem = item.find(['span', 'div'], class_=re.compile(r'author|by'))
                    if author_elem:
                        metadata['author'] = author_elem.get_text(strip=True)

                    # Try to extract date
                    date_elem = item.find(['time', 'span'], class_=re.compile(r'date|time'))
                    if date_elem:
                        metadata['date'] = date_elem.get('datetime') or date_elem.get_text(strip=True)

                    results.append({
                        'title': title,
                        'snippet': description[:300] if len(description) > 300 else description,
                        'url': url,
                        'source': 'przystanek_historia',
                        'relevance_score': 0.7,
                        'metadata': metadata
                    })

                    if len(results) >= limit:
                        break

                except Exception as e:
                    logger.warning(f"Error parsing Przystanek Historia result: {e}")
                    continue

            if not results:
                return [{
                    'error': 'No matching results found',
                    'source': 'przystanek_historia',
                    'query': query
                }]

            return results

        except Exception as e:
            logger.error(f"Error searching Przystanek Historia: {e}")
            return [{
                'error': str(e),
                'source': 'przystanek_historia',
                'query': query
            }]

    async def extract_content(self, url: str) -> Dict[str, Any]:
        """
        Extract content from Przystanek Historia URL

        Args:
            url: Przystanek Historia page URL

        Returns:
            Dictionary with extracted content
        """
        try:
            response = await self.http_client.get(url)

            html_content = response.get('text', '') if isinstance(response, dict) else str(response)

            if not html_content:
                return {
                    'error': 'No content returned',
                    'url': url,
                    'source': 'przystanek_historia'
                }

            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract title
            title_elem = soup.find('h1') or soup.find('title')
            title = title_elem.get_text(strip=True) if title_elem else ""

            # Extract main content
            content_elem = (
                soup.find('div', class_=re.compile(r'content|article|text|body')) or
                soup.find('article') or
                soup.find('main')
            )

            if content_elem:
                for unwanted in content_elem.find_all(['script', 'style', 'nav', 'aside', 'footer', 'iframe']):
                    unwanted.decompose()

                content = content_elem.get_text(separator='\n', strip=True)
                content = re.sub(r'\n{3,}', '\n\n', content)
            else:
                content = ""

            # Extract metadata
            metadata = {
                'url': url,
                'language': 'pl',
                'domain': 'przystanekhistoria.pl',
                'word_count': len(content.split()) if content else 0,
                'source_type': 'historical_articles',
                'focus_period': '20th_century'
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
                'source': 'przystanek_historia',
                'metadata': metadata
            }

        except Exception as e:
            logger.error(f"Error extracting content from Przystanek Historia: {e}")
            return {
                'error': str(e),
                'url': url,
                'source': 'przystanek_historia'
            }

    async def search_by_domain(self, query: str, domains: List[str]) -> List[Dict[str, Any]]:
        """Search Przystanek Historia and filter results (for compatibility)"""
        return await self.search(query)

    async def get_page_content(self, title: str) -> Dict[str, Any]:
        """Get page content by title (compatibility method)"""
        search_results = await self.search(title, limit=1)

        if search_results and 'url' in search_results[0]:
            url = search_results[0]['url']
            return await self.extract_content(url)
        else:
            return {
                'error': f'No results found for title: {title}',
                'source': 'przystanek_historia'
            }

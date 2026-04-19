#!/usr/bin/env python3
"""
IPN (Edukacja IPN) domain service
Provides content extraction and search capabilities for IPN educational portal
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


class IPNService(BaseDomainService):
    """
    IPN Edukacja domain service for historical education materials

    Note: IPN uses POST forms for search. This service implements
    content extraction and search via web scraping.
    """

    def __init__(self, http_client: HTTPClient = None, cache_service: CacheService = None):
        """
        Initialize IPN service

        Args:
            http_client: HTTP client instance
            cache_service: Cache service instance
        """
        super().__init__("ipn", http_client, cache_service)
        self.base_url = "https://edukacja.ipn.gov.pl"
        self.search_url = f"{self.base_url}/edu/search"

    async def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search IPN education portal

        Note: IPN uses POST form for search. This method tries GET approximation.

        Args:
            query: Search query string
            limit: Maximum number of results

        Returns:
            List of search results
        """
        try:
            # Try GET with search parameters (may not work well with POST forms)
            # Alternative: could try material listing pages
            response = await self.http_client.get(f"{self.base_url}/edu/materialy-edukacyjne")

            html_content = response.get('text', '') if isinstance(response, dict) else str(response)

            if not html_content:
                return [{
                    'error': 'No content returned from IPN',
                    'source': 'ipn',
                    'query': query
                }]

            soup = BeautifulSoup(html_content, 'html.parser')

            results = []

            # IPN material listing structure
            material_items = (
                soup.find_all('div', class_='material-item') or
                soup.find_all('article') or
                soup.find_all('div', class_=re.compile(r'item|material|resource'))
            )

            # Filter items that contain query (basic text search)
            query_lower = query.lower()

            for item in material_items[:limit * 3]:  # Get more items for filtering
                try:
                    item_text = item.get_text().lower()

                    # Basic relevance filter - check if query appears in text
                    if query_lower not in item_text:
                        continue

                    # Extract title
                    title_elem = item.find(['h2', 'h3', 'h4']) or item.find('a', class_=re.compile(r'title'))
                    title = title_elem.get_text(strip=True) if title_elem else "Bez tytułu"

                    # Extract URL
                    url_elem = item.find('a', href=True)
                    if url_elem:
                        url = urljoin(self.base_url, url_elem['href'])
                    else:
                        continue

                    # Extract description
                    desc_elem = item.find(['p', 'div'], class_=re.compile(r'desc|summary|content'))
                    description = desc_elem.get_text(strip=True) if desc_elem else ""

                    # Extract metadata
                    metadata = {
                        'language': 'pl',
                        'domain': 'edukacja.ipn.gov.pl',
                        'source_type': 'educational_materials'
                    }

                    # Try to extract category/type
                    type_elem = item.find(['span', 'div'], class_=re.compile(r'category|type|tag'))
                    if type_elem:
                        metadata['category'] = type_elem.get_text(strip=True)

                    results.append({
                        'title': title,
                        'snippet': description[:300] if len(description) > 300 else description,
                        'url': url,
                        'source': 'ipn',
                        'relevance_score': 0.6,
                        'metadata': metadata
                    })

                    if len(results) >= limit:
                        break

                except Exception as e:
                    logger.warning(f"Error parsing IPN result item: {e}")
                    continue

            if not results:
                return [{
                    'error': 'IPN uses POST forms for search - automated search limited',
                    'source': 'ipn',
                    'query': query,
                    'note': 'Use extract_content() with known IPN URLs for full functionality'
                }]

            return results

        except Exception as e:
            logger.error(f"Error searching IPN: {e}")
            return [{
                'error': str(e),
                'source': 'ipn',
                'query': query
            }]

    async def extract_content(self, url: str) -> Dict[str, Any]:
        """
        Extract content from IPN URL

        Args:
            url: IPN page URL

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
                    'source': 'ipn'
                }

            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract title
            title_elem = soup.find('h1') or soup.find('title')
            title = title_elem.get_text(strip=True) if title_elem else ""

            # Extract main content
            content_elem = (
                soup.find('div', class_=re.compile(r'content|article|main|text')) or
                soup.find('article') or
                soup.find('main')
            )

            if content_elem:
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
                'domain': 'edukacja.ipn.gov.pl',
                'word_count': len(content.split()) if content else 0,
                'source_type': 'educational_materials'
            }

            return {
                'title': title,
                'content': content,
                'url': url,
                'source': 'ipn',
                'metadata': metadata
            }

        except Exception as e:
            logger.error(f"Error extracting content from IPN: {e}")
            return {
                'error': str(e),
                'url': url,
                'source': 'ipn'
            }

    async def search_by_domain(self, query: str, domains: List[str]) -> List[Dict[str, Any]]:
        """Search IPN and filter results (for compatibility)"""
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
                'source': 'ipn'
            }

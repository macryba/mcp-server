#!/usr/bin/env python3
"""
GWO (Gdańskie Wydawnictwo Oświatowe) domain service
Provides content extraction and search capabilities for GWO history materials
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


class GWOService(BaseDomainService):
    """
    GWO Historia domain service for educational materials

    Note: GWO provides teaching materials for Polish schools.
    This service implements content extraction and search via web scraping.
    """

    def __init__(self, http_client: HTTPClient = None, cache_service: CacheService = None):
        """
        Initialize GWO service

        Args:
            http_client: HTTP client instance
            cache_service: Cache service instance
        """
        super().__init__("gwo", http_client, cache_service)
        self.base_url = "https://gwo.pl"
        self.history_url = f"{self.base_url}/przedmioty/historia/materialy-dydaktyczne"

    async def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search GWO history materials

        Args:
            query: Search query string
            limit: Maximum number of results

        Returns:
            List of search results
        """
        try:
            # Get history materials page
            response = await self.http_client.get(self.history_url)

            html_content = response.get('text', '') if isinstance(response, dict) else str(response)

            if not html_content:
                return [{
                    'error': 'No content returned from GWO',
                    'source': 'gwo',
                    'query': query
                }]

            soup = BeautifulSoup(html_content, 'html.parser')

            results = []

            # GWO material structure
            material_items = (
                soup.find_all('div', class_='material-item') or
                soup.find_all('article') or
                soup.find_all('div', class_=re.compile(r'product|item|material'))
            )

            # Filter by query relevance
            query_lower = query.lower()

            for item in material_items[:limit * 3]:
                try:
                    item_text = item.get_text().lower()

                    # Basic relevance filter
                    if query_lower not in item_text and len(query_lower) > 3:
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
                    desc_elem = item.find(['p', 'div'], class_=re.compile(r'desc|description|excerpt'))
                    description = desc_elem.get_text(strip=True) if desc_elem else ""

                    # Extract metadata for educational materials
                    metadata = {
                        'language': 'pl',
                        'domain': 'gwo.pl',
                        'source_type': 'teaching_materials',
                        'publisher': 'GWO'
                    }

                    # Try to extract education level
                    level_elem = item.find(['span', 'div'], class_=re.compile(r'klasa|level|poziom'))
                    if level_elem:
                        metadata['education_level'] = level_elem.get_text(strip=True)

                    results.append({
                        'title': title,
                        'snippet': description[:300] if len(description) > 300 else description,
                        'url': url,
                        'source': 'gwo',
                        'relevance_score': 0.5,
                        'metadata': metadata
                    })

                    if len(results) >= limit:
                        break

                except Exception as e:
                    logger.warning(f"Error parsing GWO result item: {e}")
                    continue

            if not results:
                return [{
                    'error': 'No matching results found',
                    'source': 'gwo',
                    'query': query
                }]

            return results

        except Exception as e:
            logger.error(f"Error searching GWO: {e}")
            return [{
                'error': str(e),
                'source': 'gwo',
                'query': query
            }]

    async def extract_content(self, url: str) -> Dict[str, Any]:
        """
        Extract content from GWO URL

        Args:
            url: GWO page URL

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
                    'source': 'gwo'
                }

            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract title
            title_elem = soup.find('h1') or soup.find('title')
            title = title_elem.get_text(strip=True) if title_elem else ""

            # Extract main content
            content_elem = (
                soup.find('div', class_=re.compile(r'content|description|product')) or
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
                'domain': 'gwo.pl',
                'word_count': len(content.split()) if content else 0,
                'source_type': 'teaching_materials',
                'publisher': 'Gdańskie Wydawnictwo Oświatowe'
            }

            # Try to extract grade level
            grade_elem = soup.find(['span', 'div'], class_=re.compile(r'klasa|grade'))
            if grade_elem:
                metadata['grade_level'] = grade_elem.get_text(strip=True)

            # Try to extract subject
            subject_elem = soup.find(['span', 'div'], class_=re.compile(r'przedmiot|subject'))
            if subject_elem:
                metadata['subject'] = subject_elem.get_text(strip=True)

            return {
                'title': title,
                'content': content,
                'url': url,
                'source': 'gwo',
                'metadata': metadata
            }

        except Exception as e:
            logger.error(f"Error extracting content from GWO: {e}")
            return {
                'error': str(e),
                'url': url,
                'source': 'gwo'
            }

    async def search_by_domain(self, query: str, domains: List[str]) -> List[Dict[str, Any]]:
        """Search GWO and filter results (for compatibility)"""
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
                'source': 'gwo'
            }

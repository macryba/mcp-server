#!/usr/bin/env python3
"""
SuperKid domain service
Provides content extraction and search capabilities for SuperKid educational portal
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


class SuperkidService(BaseDomainService):
    """
    SuperKid domain service for educational content

    Note: SuperKid uses POST forms for search and has complex structure.
    This service implements content extraction and limited search functionality.
    """

    def __init__(self, http_client: HTTPClient = None, cache_service: CacheService = None):
        """
        Initialize SuperKid service

        Args:
            http_client: HTTP client instance
            cache_service: Cache service instance
        """
        super().__init__("superkid", http_client, cache_service)
        self.base_url = "https://www.superkid.pl"
        self.search_url = f"{self.base_url}/wyszukaj"
        self.history_url = f"{self.base_url}/historia-online"

    async def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search SuperKid using web scraping

        Note: SuperKid uses POST for search, this method tries GET with query parameters.

        Args:
            query: Search query string
            limit: Maximum number of results

        Returns:
            List of search results
        """
        try:
            # Try GET with query parameter (may not work, POST is used for search)
            params = {
                'tag': query,
                'typ': 'page'
            }

            response = await self.http_client.get(self.search_url, params=params)

            # Extract HTML content from response
            html_content = response.get('text', '') if isinstance(response, dict) else str(response)

            if not html_content:
                return [{
                    'error': 'No content returned from SuperKid',
                    'source': 'superkid',
                    'query': query
                }]

            # Parse HTML content
            soup = BeautifulSoup(html_content, 'html.parser')

            results = []

            # SuperKid uses specific selectors for search results
            search_items = (
                soup.find_all('div', class_='search-result') or
                soup.find_all('div', class_='item') or
                soup.find_all('article') or
                soup.find_all('div', class_=re.compile(r'result|content'))
            )

            for item in search_items[:limit]:
                try:
                    # Extract title
                    title_elem = (
                        item.find('h2') or
                        item.find('h3') or
                        item.find('a', class_=re.compile(r'title|link'))
                    )
                    title = title_elem.get_text(strip=True) if title_elem else "Bez tytułu"

                    # Extract URL
                    url_elem = item.find('a', href=True)
                    if url_elem:
                        url = urljoin(self.base_url, url_elem['href'])
                    else:
                        continue  # Skip items without URL

                    # Extract snippet/description
                    snippet_elem = (
                        item.find('p', class_=re.compile(r'desc|summary|snippet')) or
                        item.find('div', class_=re.compile(r'desc|summary|content'))
                    )
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""

                    # Clean up snippet
                    snippet = re.sub(r'\s+', ' ', snippet).strip()

                    # Extract metadata for educational content
                    metadata = {
                        'language': 'pl',
                        'domain': 'superkid.pl',
                        'education_level': 'primary_school'
                    }

                    # Try to extract grade level
                    grade_elem = item.find(['span', 'div'], class_=re.compile(r'klasa|grade|poziom'))
                    if grade_elem:
                        metadata['grade_level'] = grade_elem.get_text(strip=True)

                    results.append({
                        'title': title,
                        'snippet': snippet[:300] if len(snippet) > 300 else snippet,
                        'url': url,
                        'source': 'superkid',
                        'relevance_score': 0.6,  # Default relevance for educational content
                        'metadata': metadata
                    })
                except Exception as e:
                    logger.warning(f"Error parsing SuperKid search result item: {e}")
                    continue

            if not results:
                return [{
                    'error': 'No results found or search method limited',
                    'source': 'superkid',
                    'query': query,
                    'note': 'SuperKid uses POST forms for search - automated search limited. Use extract_content() with known URLs.'
                }]

            return results

        except Exception as e:
            logger.error(f"Error searching SuperKid: {e}")
            return [{
                'error': str(e),
                'source': 'superkid',
                'query': query,
                'note': 'Search request failed - site may be blocking automated access'
            }]

    async def extract_content(self, url: str) -> Dict[str, Any]:
        """
        Extract full educational content from SuperKid URL

        Args:
            url: SuperKid page URL

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
                    'source': 'superkid'
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
                # Remove unwanted elements
                for unwanted in content_elem.find_all(['script', 'style', 'nav', 'aside', 'footer', 'iframe']):
                    unwanted.decompose()

                content = content_elem.get_text(separator='\n', strip=True)
                content = re.sub(r'\n{3,}', '\n\n', content)
            else:
                content = ""

            # Extract metadata for educational content
            metadata = {
                'url': url,
                'language': 'pl',
                'domain': 'superkid.pl',
                'word_count': len(content.split()) if content else 0,
                'education_level': 'primary_school'
            }

            # Try to extract grade level
            grade_elem = soup.find(['span', 'div'], class_=re.compile(r'klasa|grade|poziom'))
            if grade_elem:
                metadata['grade_level'] = grade_elem.get_text(strip=True)

            # Try to extract subject
            subject_elem = soup.find(['span', 'div'], class_=re.compile(r'przedmiot|subject|dziedzina'))
            if subject_elem:
                metadata['subject'] = subject_elem.get_text(strip=True)

            # Try to extract educational tags
            tags_elem = soup.find('div', class_=re.compile(r'tag|label'))
            if tags_elem:
                tags = tags_elem.find_all('a')
                if tags:
                    metadata['tags'] = [tag.get_text(strip=True) for tag in tags]

            return {
                'title': title,
                'content': content,
                'url': url,
                'source': 'superkid',
                'metadata': metadata
            }

        except Exception as e:
            logger.error(f"Error extracting content from SuperKid: {e}")
            return {
                'error': str(e),
                'url': url,
                'source': 'superkid'
            }

    async def search_by_domain(self, query: str, domains: List[str]) -> List[Dict[str, Any]]:
        """
        Search SuperKid and filter results (for compatibility)

        Args:
            query: Search query
            domains: List of domains (ignored, always SuperKid)

        Returns:
            List of search results
        """
        return await self.search(query)

    async def get_page_content(self, title: str) -> Dict[str, Any]:
        """
        Get page content by title (compatibility method)

        Note: SuperKid doesn't have direct title-to-URL mapping.
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
                'source': 'superkid'
            }

    async def get_history_topics(self) -> List[Dict[str, Any]]:
        """
        Get available history topics from SuperKid history section

        Returns:
            List of history topics with URLs and descriptions
        """
        try:
            response = await self.http_client.get(self.history_url)

            html_content = response.get('text', '') if isinstance(response, dict) else str(response)

            if not html_content:
                return []

            soup = BeautifulSoup(html_content, 'html.parser')

            topics = []

            # Find history topic links
            topic_links = soup.find_all('a', href=re.compile(r'/historia'))

            for link in topic_links:
                try:
                    title = link.get_text(strip=True)
                    url = urljoin(self.base_url, link['href'])

                    if title and not title.isspace():
                        topics.append({
                            'title': title,
                            'url': url,
                            'source': 'superkid',
                            'type': 'history_topic'
                        })
                except Exception as e:
                    logger.warning(f"Error parsing history topic link: {e}")
                    continue

            return topics[:50]  # Limit to first 50 topics

        except Exception as e:
            logger.error(f"Error getting history topics: {e}")
            return []

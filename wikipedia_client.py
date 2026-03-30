#!/usr/bin/env python3
"""
Wikipedia search client for Polish history research
Supports multiple Wikipedia languages and page extraction
"""

import requests
import json
import re
from typing import List, Dict, Optional
from urllib.parse import quote


class WikipediaClient:
    """Client for searching and fetching Wikipedia content"""

    def __init__(self, language: str = 'pl'):
        self.language = language
        self.base_url = f"https://{language}.wikipedia.org"
        self.api_url = f"{self.base_url}/w/api.php"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search Wikipedia using the MediaWiki API

        Args:
            query: Search query string
            max_results: Maximum number of results to return

        Returns:
            List of search results with title, snippet, and URL
        """
        params = {
            'action': 'query',
            'list': 'search',
            'srsearch': query,
            'format': 'json',
            'utf8': 1,
            'srlimit': max_results
        }

        try:
            response = requests.get(self.api_url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()

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
                    'wordcount': item.get('wordcount', 0),
                    'timestamp': item.get('timestamp', '')
                })

            return results

        except Exception as e:
            return [{'error': str(e)}]

    def get_page_content(self, title: str) -> Dict:
        """
        Get full page content from Wikipedia

        Args:
            title: Page title

        Returns:
            Dictionary with page content, metadata, and cleaned text
        """
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
            response = requests.get(self.api_url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            pages = data.get('query', {}).get('pages', {})
            page_id = next(iter(pages))

            if page_id == '-1':
                return {'error': 'Page not found'}

            page_data = pages[page_id]
            url = f"{self.base_url}/wiki/{quote(title.replace(' ', '_'))}"

            return {
                'title': page_data.get('title', ''),
                'extract': page_data.get('extract', ''),
                'url': url,
                'pageid': page_data.get('pageid', ''),
                'language': self.language
            }

        except Exception as e:
            return {'error': str(e)}

    def search_by_domain(self, query: str, domains: List[str]) -> List[Dict]:
        """
        Search Wikipedia and filter results by domain (for future expansion)

        Args:
            query: Search query
            domains: List of domains to search (currently Wikipedia only)

        Returns:
            List of search results
        """
        # For now, just use Wikipedia search
        # This can be expanded to include other domains in the future
        return self.search(query)


def main():
    """CLI interface for testing"""
    import sys

    if len(sys.argv) < 2:
        print(json.dumps({'error': 'Usage: wikipedia_client.py "<query>" [language] [max_results]'}))
        sys.exit(1)

    query = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else 'pl'
    max_results = int(sys.argv[3]) if len(sys.argv) > 3 else 5

    client = WikipediaClient(language)
    results = client.search(query, max_results)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

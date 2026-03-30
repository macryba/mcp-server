#!/usr/bin/env python3
"""
Simple Wikipedia search API for Polish history queries
Direct interface to Wikipedia API, bypassing SearXNG
"""

import requests
import json
import sys
from urllib.parse import quote

def search_wikipedia(query, language='pl', max_results=5):
    """
    Search Wikipedia using the MediaWiki API
    """
    base_url = f"https://{language}.wikipedia.org/w/api.php"

    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': query,
        'format': 'json',
        'utf8': 1,
        'srlimit': max_results
    }

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get('query', {}).get('search', []):
            title = item['title']
            snippet = item.get('snippet', '').replace('<span class="searchmatch">', '').replace('</span>', '')
            url = f"https://{language}.wikipedia.org/wiki/{quote(title.replace(' ', '_'))}"

            results.append({
                'title': title,
                'snippet': snippet,
                'url': url
            })

        return results

    except Exception as e:
        return {'error': str(e)}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'Usage: wikipedia_search.py "<query>" [language] [max_results]'}))
        sys.exit(1)

    query = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else 'pl'
    max_results = int(sys.argv[3]) if len(sys.argv) > 3 else 5

    results = search_wikipedia(query, language, max_results)
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()

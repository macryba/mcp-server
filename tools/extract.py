#!/usr/bin/env python3
"""
Content extraction tools for Polish history research
Provides tools to extract and process content from various sources
"""

from services.domains.wikipedia import WikipediaService
from services.http_client import HTTPClient
from services.cache import get_cache
from utils.text import normalize_whitespace
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize services
_http_client = HTTPClient()
_cache = get_cache()
_wikipedia_pl = WikipediaService(language='pl', http_client=_http_client, cache_service=_cache)


async def extract_article(url: str) -> str:
    """
    Fetch a page and return cleaned title, URL, and article text

    Args:
        url: URL of the article to extract

    Returns:
        JSON string with title, content, url, and metadata
    """
    try:
        # Check if it's a Wikipedia URL
        if 'wikipedia.org' in url:
            content = await _wikipedia_pl._cached_extract(url)
        else:
            # For non-Wikipedia URLs, we'll need to implement generic extraction
            # For now, return an error
            return str({
                'error': 'Only Wikipedia URLs are currently supported',
                'url': url,
                'supported_domains': ['pl.wikipedia.org', 'en.wikipedia.org']
            })

        # Clean and normalize the content
        if 'content' in content:
            content['content'] = normalize_whitespace(content['content'])

        return str(content)
    except Exception as e:
        logger.error(f"Error in extract_article: {e}")
        return str({'error': str(e), 'url': url})












# Helper functions





# Cleanup function
async def cleanup():
    """Cleanup resources"""
    await _http_client.close()

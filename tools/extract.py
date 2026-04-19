#!/usr/bin/env python3
"""
Content extraction tools for Polish history research
Provides tools to extract and process content from various Polish historical sources
"""

from services.domains.wikipedia import WikipediaService
from services.domains.dzieje import DziejeService
from services.http_client import HTTPClient
from services.cache import get_cache
from utils.text import normalize_whitespace
from typing import Dict, Any, Optional
from urllib.parse import urlparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize services
_http_client = HTTPClient()
_cache = get_cache()

# Initialize all domain services that support URL extraction (Polish only)
_wikipedia = WikipediaService(language='pl', http_client=_http_client, cache_service=_cache)
_dzieje = DziejeService(http_client=_http_client, cache_service=_cache)


def _detect_domain_from_url(url: str) -> Optional[str]:
    """
    Detect which Polish domain service should handle the URL based on the hostname

    Args:
        url: URL to analyze

    Returns:
        Domain service name or None if not recognized
    """
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname or parsed.netloc or ""

        # Convert to lowercase for case-insensitive matching
        hostname = hostname.lower()

        # Domain detection patterns (Polish sources only)
        if 'wikipedia.org' in hostname:
            # Only Polish Wikipedia is supported
            if hostname.startswith('pl.'):
                return 'wikipedia'
            else:
                # Reject non-Polish Wikipedia URLs
                logger.warning(f"Non-Polish Wikipedia URL detected: {hostname}")
                return None
        elif 'dzieje.pl' in hostname:
            return 'dzieje'
        else:
            return None

    except Exception as e:
        logger.warning(f"Error parsing URL {url}: {e}")
        return None


def _get_service_for_domain(domain: str):
    """
    Get the service instance for a given domain name

    Args:
        domain: Domain service name

    Returns:
        Domain service instance or None if not found
    """
    service_map = {
        'wikipedia': _wikipedia,
        'dzieje': _dzieje,
    }

    return service_map.get(domain)


async def extract_article(url: str) -> str:
    """
    Fetch a page and return cleaned title, URL, and article text

    Supports all configured Polish history domains with URL extraction capability:
    - Wikipedia Polska (pl.wikipedia.org)
    - Dzieje.pl (dzieje.pl)

    Args:
        url: URL of the article to extract

    Returns:
        JSON string with title, content, url, and metadata
    """
    try:
        # Detect which domain service should handle this URL
        domain = _detect_domain_from_url(url)

        if domain is None:
            return str({
                'error': 'Unsupported domain - URL not recognized or not a Polish source',
                'url': url,
                'supported_domains': [
                    'pl.wikipedia.org',
                    'dzieje.pl'
                ],
                'note': 'This MCP server supports only Polish historical sources. Non-Polish Wikipedia editions and other non-Polish domains are not supported.'
            })

        # Get the appropriate service for this domain
        service = _get_service_for_domain(domain)

        if service is None:
            return str({
                'error': f'Domain {domain} detected but service not available',
                'url': url
            })

        # Extract content using the domain-specific service
        content = await service._cached_extract(url)

        # Clean and normalize the content
        if 'content' in content and isinstance(content['content'], str):
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

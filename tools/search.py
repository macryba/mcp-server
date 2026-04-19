#!/usr/bin/env python3
"""
Search tools for Polish history research
Provides multi-domain search capabilities across Polish Wikipedia and other Polish historical sources
"""

from fastmcp import FastMCP
from services.domains.wikipedia import WikipediaService
from services.domains.dzieje import DziejeService
from services.domains.polona import PolonaService
from services.domains.superkid import SuperkidService
from services.domains.ipn import IPNService
from services.domains.przystanek_historia import PrzystanekHistoriaService
from services.domains.gwo import GWOService
from services.http_client import HTTPClient
from services.cache import get_cache
from models.domains import DomainRegistry
from typing import Dict, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize services
_http_client = HTTPClient()
_cache = get_cache()

# Initialize domain services (Polish only)
_wikipedia = WikipediaService(language='pl', http_client=_http_client, cache_service=_cache)
_dzieje = DziejeService(http_client=_http_client, cache_service=_cache)
_polona = PolonaService(http_client=_http_client, cache_service=_cache)
_superkid = SuperkidService(http_client=_http_client, cache_service=_cache)
_ipn = IPNService(http_client=_http_client, cache_service=_cache)
_przystanek_historia = PrzystanekHistoriaService(http_client=_http_client, cache_service=_cache)
_gwo = GWOService(http_client=_http_client, cache_service=_cache)


async def search_polish_history(query: str, domains: List[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Search trusted Polish history sources and return matching pages

    Args:
        query: Search query string
        domains: List of domains to search (None = all implemented domains)
        limit: Maximum number of results per domain

    Returns:
        List of search results from all specified domains
    """
    if not query:
        return []

    results = []

    # Get all implemented domains (both API search and web scraping)
    # Currently implemented: Wikipedia (API), Dzieje.pl (web scraping), Polona (API), SuperKid (web scraping), IPN (web scraping), Przystanek Historia (web scraping), GWO (web scraping)
    implemented_domains = {
        'wikipedia', 'wikipedia_pl',        # Wikipedia - API search
        'dzieje', 'dzieje_pl',              # Dzieje.pl - web scraping
        'polona',                           # Polona - API search
        'superkid', 'superkid_pl',         # SuperKid - web scraping
        'ipn', 'ipn_pl',                   # IPN - web scraping
        'przystanek_historia', 'przystanek', # Przystanek Historia - web scraping
        'gwo', 'gwo_pl'                    # GWO - web scraping
    }

    logger.info(f"Implemented domains: {implemented_domains}")

    # If no domains specified, search all implemented domains
    if domains is None:
        domains = list(implemented_domains)
        logger.info(f"No domains specified, searching all implemented: {domains}")

    # Filter to only implemented domains
    domains_to_search = [d for d in domains if d.lower() in implemented_domains]

    if len(domains_to_search) < len(domains):
        skipped = set(domains) - set(domains_to_search)
        logger.warning(f"Skipping unimplemented domains: {skipped}")

    # Search Polish Wikipedia (implemented - API search)
    if 'wikipedia' in domains_to_search or 'wikipedia_pl' in domains_to_search:
        try:
            wiki_results = await _wikipedia._cached_search(query, limit)
            results.extend(wiki_results)
            logger.info(f"Successfully searched Wikipedia: {len(wiki_results)} results")
        except Exception as e:
            logger.error(f"Error searching Polish Wikipedia: {e}")

    # Search Dzieje.pl (implemented - web scraping)
    if 'dzieje' in domains_to_search or 'dzieje_pl' in domains_to_search:
        try:
            dzieje_results = await _dzieje._cached_search(query, limit)
            results.extend(dzieje_results)
            logger.info(f"Successfully searched Dzieje.pl: {len(dzieje_results)} results")
        except Exception as e:
            logger.error(f"Error searching Dzieje.pl: {e}")

    # Search Polona (implemented - API search)
    if 'polona' in domains_to_search:
        try:
            polona_results = await _polona._cached_search(query, limit)
            results.extend(polona_results)
            logger.info(f"Successfully searched Polona: {len(polona_results)} results")
        except Exception as e:
            logger.error(f"Error searching Polona: {e}")

    # Search SuperKid (implemented - web scraping)
    if 'superkid' in domains_to_search or 'superkid_pl' in domains_to_search:
        try:
            superkid_results = await _superkid._cached_search(query, limit)
            results.extend(superkid_results)
            logger.info(f"Successfully searched SuperKid: {len(superkid_results)} results")
        except Exception as e:
            logger.error(f"Error searching SuperKid: {e}")

    # Search IPN (implemented - web scraping)
    if 'ipn' in domains_to_search or 'ipn_pl' in domains_to_search:
        try:
            ipn_results = await _ipn._cached_search(query, limit)
            results.extend(ipn_results)
            logger.info(f"Successfully searched IPN: {len(ipn_results)} results")
        except Exception as e:
            logger.error(f"Error searching IPN: {e}")

    # Search Przystanek Historia (implemented - web scraping)
    if 'przystanek_historia' in domains_to_search or 'przystanek' in domains_to_search:
        try:
            przystanek_results = await _przystanek_historia._cached_search(query, limit)
            results.extend(przystanek_results)
            logger.info(f"Successfully searched Przystanek Historia: {len(przystanek_results)} results")
        except Exception as e:
            logger.error(f"Error searching Przystanek Historia: {e}")

    # Search GWO (implemented - web scraping)
    if 'gwo' in domains_to_search or 'gwo_pl' in domains_to_search:
        try:
            gwo_results = await _gwo._cached_search(query, limit)
            results.extend(gwo_results)
            logger.info(f"Successfully searched GWO: {len(gwo_results)} results")
        except Exception as e:
            logger.error(f"Error searching GWO: {e}")

    # All domains are now implemented!

    return results


async def search_wikipedia(query: str, max_results: int = 5) -> str:
    """
    Search Polish Wikipedia for historical information

    Best for:
    - General Polish history topics
    - Historical figures (kings, queens, leaders)
    - Historical events (battles, uprisings, treaties)

    Args:
        query: Search query (e.g., "Bolesław III Krzywousty")
        max_results: Maximum number of results to return (1-20)

    Returns:
        JSON string with search results including titles, snippets, and URLs
    """
    try:
        results = await _wikipedia._cached_search(query, max_results)
        return str(results)  # Return as string for MCP compatibility
    except Exception as e:
        logger.error(f"Error in search_wikipedia: {e}")
        return str({'error': str(e)})


async def list_domains(include_unimplemented: bool = False) -> str:
    """
    List all configured domains in the MCP server

    Returns comprehensive information about all historical source domains,
    including their capabilities, categories, difficulty levels, and what they cover.

    Args:
        include_unimplemented: Include domains that are registered but not yet implemented (default: False)

    Returns:
        JSON string with domain information including:
        - name: Domain name
        - base_url: Base URL
        - description: What the domain covers
        - categories: Content categories (e.g., "ogolnoedukacyjne", "popularnonaukowe")
        - difficulties: Difficulty levels (e.g., "łatwy", "średni", "trudny")
        - tags: Relevant tags
        - capabilities: Search capabilities (api_search, web_scraping, url_extraction)
        - implementation_status: Whether the domain is implemented
    """
    try:
        # Get all domains from registry
        all_domains = DomainRegistry.get_all_domains()

        # Map domain names to implementation status
        # Based on what's actually implemented in tools/search.py
        implemented_domain_map = {
            'Wikipedia': True,                    # wikipedia_pl - API search
            'Edukacja IPN': True,                 # ipn - web scraping
            'Dzieje.pl': True,                    # dzieje - web scraping
            'Przystanek Historia': True,          # przystanek_historia - web scraping
            'SuperKid - Historia online': True,   # superkid - web scraping
            'GWO - Historia': True,               # gwo - web scraping
            'Polona': True,                       # polona - API search
        }

        domains_list = []
        for domain in all_domains:
            # Check if domain is implemented
            is_implemented = implemented_domain_map.get(domain.name, False)

            # Skip unimplemented domains if requested
            if not include_unimplemented and not is_implemented:
                continue

            domain_info = {
                'name': domain.name,
                'base_url': domain.base_url,
                'description': domain.description,
                'categories': [c.value for c in domain.categories],
                'difficulties': [d.value for d in domain.difficulties],
                'tags': list(domain.tags),
                'capabilities': {
                    'api_search': domain.supports_api_search,
                    'web_scraping': domain.supports_web_scraping,
                    'url_extraction': domain.supports_url_extraction
                },
                'language': domain.language,
                'central_for_ai': domain.central_for_ai,
                'api_documentation_url': domain.api_documentation_url,
                'implementation_status': 'implemented' if is_implemented else 'planned'
            }

            domains_list.append(domain_info)

        result = {
            'total_domains': len(domains_list),
            'implemented_count': sum(1 for d in domains_list if d['implementation_status'] == 'implemented'),
            'planned_count': sum(1 for d in domains_list if d['implementation_status'] == 'planned'),
            'domains': domains_list
        }

        logger.info(f"Listed {len(domains_list)} domains ({result['implemented_count']} implemented, {result['planned_count']} planned)")
        return str(result)

    except Exception as e:
        logger.error(f"Error in list_domains: {e}")
        return str({'error': str(e)})


# Cleanup function to close HTTP client
async def cleanup():
    """Cleanup resources"""
    await _http_client.close()

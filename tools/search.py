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


async def search_historical_figures(query: str, period: str = None) -> str:
    """
    Search Polish Wikipedia specifically for historical figures

    Optimized for searching Polish kings, queens, leaders, and historical personalities.

    Args:
        query: Name or description of historical figure
        period: Optional time period (e.g., "XVII wiek", "1945-1989")

    Returns:
        JSON string with relevant biographical information
    """
    try:
        # Add context-specific search terms for better results
        enhanced_query = f"{query} król Polska książę historia" if len(query.split()) < 3 else query

        if period:
            enhanced_query += f" {period}"

        results = await _wikipedia._cached_search(enhanced_query, 5)

        # Add context about Polish historical sources
        suggested_domains = DomainRegistry.get_suggested_domains_for_tool("search_historical_figures")

        for result in results:
            if 'error' not in result:
                result['source_type'] = 'Polish historical figure'
                result['suggested_domains'] = suggested_domains

        return str(results)
    except Exception as e:
        logger.error(f"Error in search_historical_figures: {e}")
        return str({'error': str(e)})


async def search_historical_events(query: str, date_range: str = None) -> str:
    """
    Search Polish Wikipedia for historical events

    Optimized for searching battles, uprisings, treaties, and historical events.

    Args:
        query: Event name or description (e.g., "Powstanie styczniowe", "Bitwa pod Grunwaldem")
        date_range: Optional date range (e.g., "1939-1945")

    Returns:
        JSON string with event information
    """
    try:
        # Enhance query for historical events
        enhanced_query = f"{query} wydarzenie historia Polska"

        if date_range:
            enhanced_query += f" {date_range}"

        results = await _wikipedia._cached_search(enhanced_query, 5)

        suggested_domains = DomainRegistry.get_suggested_domains_for_tool("search_historical_events")

        for result in results:
            if 'error' not in result:
                result['source_type'] = 'Polish historical event'
                result['suggested_domains'] = suggested_domains

        return str(results)
    except Exception as e:
        logger.error(f"Error in search_historical_events: {e}")
        return str({'error': str(e)})


async def search_historical_places(query: str, region: str = None) -> str:
    """
    Search for historical places and locations

    Args:
        query: Place name or description
        region: Optional region filter

    Returns:
        JSON string with place information
    """
    try:
        enhanced_query = f"{query} miejsce historyczne Polska"

        if region:
            enhanced_query += f" {region}"

        results = await _wikipedia._cached_search(enhanced_query, 5)

        for result in results:
            if 'error' not in result:
                result['source_type'] = 'Historical place'

        return str(results)
    except Exception as e:
        logger.error(f"Error in search_historical_places: {e}")
        return str({'error': str(e)})


async def search_primary_sources(query: str, source_type: str = None) -> str:
    """
    Search for primary sources and documents

    Args:
        query: Search query
        source_type: Type of source (documents, archives, newspapers)

    Returns:
        JSON string with primary source results
    """
    try:
        # For now, search Wikipedia with primary source keywords
        enhanced_query = f"{query} dokumenty archiwa źródła historyczne"

        results = await _wikipedia._cached_search(enhanced_query, 5)

        suggested_domains = DomainRegistry.get_suggested_domains_for_tool("search_primary_sources")

        for result in results:
            if 'error' not in result:
                result['source_type'] = 'Primary source'
                result['suggested_domains'] = suggested_domains

        return str(results)
    except Exception as e:
        logger.error(f"Error in search_primary_sources: {e}")
        return str({'error': str(e)})


async def search_biographies(query: str, profession: str = None) -> str:
    """
    Search for biographical entries

    Args:
        query: Person name
        profession: Optional profession filter

    Returns:
        JSON string with biographical information
    """
    try:
        enhanced_query = f"{query} biografia życiorys"

        if profession:
            enhanced_query += f" {profession}"

        results = await _wikipedia._cached_search(enhanced_query, 5)

        suggested_domains = DomainRegistry.get_suggested_domains_for_tool("search_biographies")

        for result in results:
            if 'error' not in result:
                result['source_type'] = 'Biography'
                result['suggested_domains'] = suggested_domains

        return str(results)
    except Exception as e:
        logger.error(f"Error in search_biographies: {e}")
        return str({'error': str(e)})


async def search_timelines(topic: str, period: str = None) -> str:
    """
    Search for timeline data

    Args:
        topic: Topic to search timeline for
        period: Optional time period

    Returns:
        JSON string with timeline results
    """
    try:
        enhanced_query = f"{topic} chronologia timeline historia"

        if period:
            enhanced_query += f" {period}"

        results = await _wikipedia._cached_search(enhanced_query, 5)

        for result in results:
            if 'error' not in result:
                result['source_type'] = 'Timeline data'

        return str(results)
    except Exception as e:
        logger.error(f"Error in search_timelines: {e}")
        return str({'error': str(e)})


async def search_definitions(term: str, domain: str = None) -> str:
    """
    Search for definitions in encyclopedias

    Args:
        term: Term to define
        domain: Specific domain (pwn, wikipedia)

    Returns:
        JSON string with definitions
    """
    try:
        enhanced_query = f"{term} definicja encyklopedia"

        results = await _wikipedia._cached_search(enhanced_query, 5)

        for result in results:
            if 'error' not in result:
                result['source_type'] = 'Definition'
                result['suggested_domains'] = [
                    'encyklopedia.pwn.pl',
                    'pl.wikipedia.org'
                ]

        return str(results)
    except Exception as e:
        logger.error(f"Error in search_definitions: {e}")
        return str({'error': str(e)})


# Cleanup function to close HTTP client
async def cleanup():
    """Cleanup resources"""
    await _http_client.close()

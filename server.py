#!/usr/bin/env python3
"""
FastMCP server for Polish History Research
Provides multi-domain search and content extraction tools

This is the NEW server entry point - replaces wikipedia_mcp_server.py
"""

from fastmcp import FastMCP
from tools import search, extract
from models.domains import DomainRegistry, Difficulty
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("Polish History Tools")

# Version
SERVER_VERSION = "2.0.0"


# ============================================================================
# SEARCH TOOLS
# ============================================================================

@mcp.tool()
async def search_polish_history(query: str, domains: list = None, limit: int = 10) -> str:
    """
    Search trusted Polish history sources and return matching pages

    RECOMMENDED WORKFLOW: After using list_domains to understand domain specializations, use this tool
    with specific domains for targeted searches.

    Currently implemented domains:
    - wikipedia (Polish Wikipedia) - ✅ available (API search)
    - dzieje (Dzieje.pl) - ✅ available (web scraping)

    Note: This server now focuses on 2 fully-functional domains for reliable Polish historical research.

    Args:
        query: Search query string (e.g., "Bolesław III Krzywousty")
        domains: List of domains to search (None = all implemented domains)
        limit: Maximum number of results per domain (default: 10)

    Returns:
        JSON string with search results from all specified domains
    """
    try:
        results = await search.search_polish_history(query, domains, limit)
        return str(results)
    except Exception as e:
        logger.error(f"Error in search_polish_history: {e}")
        return str({'error': str(e)})


@mcp.tool()
async def search_wikipedia(query: str, max_results: int = 5) -> str:
    """
    Search Polish Wikipedia for historical information

    RECOMMENDED WORKFLOW: Use this tool first for quick lookups. If you need more specialized
    or comprehensive information, call list_domains to learn about available domains, then use
    search_polish_history with specific domains.

    Best for:
    - Quick basic information about Polish history topics
    - General overviews of historical figures, events, places
    - Initial research before diving into specialized sources

    Args:
        query: Search query (e.g., "Bolesław III Krzywousty")
        max_results: Maximum number of results to return (1-20)

    Returns:
        JSON string with search results including titles, snippets, and URLs
    """
    try:
        results = await search.search_wikipedia(query, max_results)
        return results
    except Exception as e:
        logger.error(f"Error in search_wikipedia: {e}")
        return str({'error': str(e)})


@mcp.tool()
async def usage_guide() -> str:
    """
    Get detailed usage guide and workflow recommendations for this MCP server

    RECOMMENDED: Call this tool after server_info for comprehensive workflow guidance.
    This tool provides detailed examples and best practices for effective use of
    Polish history search tools.

    Returns:
        JSON string with detailed usage guide, examples, and best practices
    """
    try:
        guide = {
            'server_name': 'Polskie Narzędzia Historyczne',
            'version': SERVER_VERSION,
            'introduction': 'This MCP server provides intelligent, multi-domain search across Polish historical sources. The tools are designed for progressive research: start quick, go deep when needed. Focus on Wikipedia and Dzieje.pl for best results. Other domains have limited functionality.',
            'core_workflow': {
                'title': '3-Step Progressive Research Workflow',
                'philosophy': 'Start with broad Wikipedia search, then target specialized sources based on domain expertise',
                'steps': [
                    {
                        'step': 1,
                        'name': 'Quick Basic Research',
                        'tool': 'search_wikipedia',
                        'when_to_use': 'Basic information, general overviews, quick facts',
                        'why': 'Fast, comprehensive, good starting point',
                        'examples': [
                            'search_wikipedia("Bolesław III Krzywousty")',
                            'search_wikipedia("Powstanie styczniowe")',
                            'search_wikipedia("Zamek Królewski Warszawa")'
                        ]
                    },
                    {
                        'step': 2,
                        'name': 'Assess Research Depth Needed',
                        'decision_points': [
                            'Does user need primary sources or archival documents?',
                            'Does user need specialized academic research?',
                            'Does user need multiple perspectives beyond Wikipedia?',
                            'Is this a specialized topic (e.g., WWII, communism)?'
                        ],
                        'action': 'If YES to any → Proceed to Step 3'
                    },
                    {
                        'step': 3,
                        'name': 'Learn Domain Specializations',
                        'tool': 'list_domains',
                        'when_to_use': 'Before targeted searches, to understand source expertise',
                        'why': 'Different domains specialize in different periods and types of content',
                        'examples': [
                            'list_domains() # Returns all domain specializations',
                            '# Learn: Dzieje.pl → Popular history, articles',
                            '# Learn: Wikipedia → General knowledge'
                        ]
                    },
                    {
                        'step': 4,
                        'name': 'Targeted Domain-Specific Search',
                        'tool': 'search_polish_history with domains parameter',
                        'when_to_use': 'After learning domain specializations for targeted research',
                        'why': 'Get highly relevant results from expert sources',
                        'examples': [
                            '# Primary sources about WWII',
                            'search_polish_history("II wojna światowa dokumenty", domains=["ipn"])',
                            '',
                            '# Educational content about medieval history',
                            'search_polish_history("król Polski średniowiecze", domains=["wikipedia", "dzieje", "gwo"])',
                            '',
                            '# Comprehensive search across all sources',
                            'search_polish_history("Powstanie warszawskie") # No domains = all'
                        ]
                    }
                ]
            },
            'domain_specializations': {
                'description': 'Quick reference for domain expertise (see list_domains for full details)',
                'domains': [
                    {'name': 'wikipedia', 'best_for': 'General knowledge, quick overviews', 'examples': 'Kings, battles, basic facts'},
                    {'name': 'dzieje', 'best_for': 'Popular history, articles', 'examples': 'History magazines, educational content'}
                ]
            },
            'query_optimization_tips': {
                'polish_language': 'Use Polish names and diacritics: "Bolesław III" not "Boleslaw III"',
                'add_context_terms': 'Include relevant keywords: "król" (king), "bitwa" (battle), "dokumenty" (documents)',
                'specify_periods': 'Add time periods: "XVII wiek" (17th century), "1939-1945"',
                'source_types': 'Add source type keywords: "dokumenty", "biografia", "życiorys"'
            },
            'best_practices': [
                'Always start with search_wikipedia for basic information',
                'Use list_domains before targeted searches to understand source expertise',
                'Specify domains in search_polish_history for better relevance',
                'Use Polish language and diacritics for best results',
                'Add context keywords based on research goals',
                'Start broad, then narrow down based on initial results'
            ],
            'example_research_scenarios': [
                {
                    'scenario': 'User wants detailed information about the Warsaw Uprising',
                    'workflow': [
                        'search_wikipedia("Powstanie warszawskie") # Basic overview',
                        '# User wants more detailed information →',
                        'search_polish_history("Powstanie warszawskie", domains=["wikipedia", "dzieje"])'
                    ]
                },
                {
                    'scenario': 'User needs educational content about Polish kings',
                    'workflow': [
                        'search_wikipedia("król Polski") # Basic info',
                        '# User wants educational materials →',
                        'list_domains() # Learn GWO and SuperKid have educational content',
                        'search_polish_history("król Polski średniowiecze", domains=["wikipedia", "gwo", "superkid"])'
                    ]
                }
            ]
        }

        return str(guide)
    except Exception as e:
        logger.error(f"Error in usage_guide: {e}")
        return str({'error': str(e)})


@mcp.tool()
async def list_domains(include_unimplemented: bool = False) -> str:
    """
    List all configured domains in the MCP server

    RECOMMENDED WORKFLOW: Use this tool to discover what domains are available and their specializations.
    After learning which domains specialize in your topic, use search_polish_history with specific domains
    for targeted, relevant results.

    Returns comprehensive information about all historical source domains,
    including their capabilities, categories, difficulty levels, and what they cover.

    Args:
        include_unimplemented: Include domains that are registered but not yet implemented (default: False)

    Returns:
        JSON string with domain information including:
        - name: Domain name
        - base_url: Base URL
        - description: What the domain covers
        - categories: Content categories (ogolnoedukacyjne, popularnonaukowe, szkolne_materialy, biografie_postacie, zrodla_swiadectwa)
        - difficulties: Difficulty levels (łatwy, średni, trudny)
        - tags: Relevant tags
        - capabilities: Search capabilities (api_search, web_scraping, url_extraction)
        - implementation_status: "implemented" or "planned"
    """
    try:
        results = await search.list_domains(include_unimplemented)
        return results
    except Exception as e:
        logger.error(f"Error in list_domains: {e}")
        return str({'error': str(e)})


# ============================================================================
# EXTRACT TOOLS
# ============================================================================

@mcp.tool()
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
        results = await extract.extract_article(url)
        return results
    except Exception as e:
        logger.error(f"Error in extract_article: {e}")
        return str({'error': str(e)})



# ============================================================================
# SERVER INFO
# ============================================================================

@mcp.tool()
async def server_info() -> str:
    """
    Get server information and capabilities

    RECOMMENDED: Call this tool first when connecting to understand available tools
    and the recommended workflow for using this MCP server effectively.

    Returns:
        JSON string with server information, recommended workflow, and capabilities
    """

    # Get domain information from centralized registry
    api_search_domains = DomainRegistry.get_domains_with_api_search()
    web_scraping_domains = DomainRegistry.get_domains_with_web_scraping()
    url_extraction_domains = DomainRegistry.get_domains_with_url_extraction()

    info = {
        'name': 'Polskie Narzędzia Historyczne',
        'version': SERVER_VERSION,
        'description': 'Serwer MCP dla polskich badań historycznych z wyszukiwaniem wielodomenowym i ekstrakcją treści',
        'recommended_workflow': {
            'summary': '3-step intelligent search workflow for best results',
            'steps': [
                {
                    'step': 1,
                    'action': 'Quick Basic Research',
                    'tool': 'search_wikipedia',
                    'description': 'Use for fast overviews and basic facts',
                    'example': 'search_wikipedia("Bitwa pod Grunwaldem")'
                },
                {
                    'step': 2,
                    'action': 'Learn Domain Specializations',
                    'tool': 'list_domains',
                    'description': 'Understand which sources specialize in your topic',
                    'example': 'list_domains() # Returns domain specializations'
                },
                {
                    'step': 3,
                    'action': 'Targeted Deep Search',
                    'tool': 'search_polish_history',
                    'description': 'Use specific domains for highly relevant results',
                    'example': 'search_polish_history("II wojna światowa", domains=["wikipedia", "dzieje"])'
                }
            ],
            'key_principle': 'Start broad with Wikipedia, then target specialized sources based on domain expertise learned from list_domains'
        },
        'capabilities': {
            'search': [
                'Wyszukiwanie wielodomenowe (Wikipedia polska, Dzieje.pl)',
                'Wyszukiwanie Wikipedia polska',
                'Informacje o domenach historycznych'
            ],
            'extract': [
                'Article extraction (Polish sources only: Wikipedia Polska, Dzieje.pl)'
            ]
        },
        'domains': {
            'wyszukiwanie_api': [d.base_url for d in api_search_domains],
            'web_scraping_obsługiwane': [d.base_url for d in web_scraping_domains],
            'ekstrakcja_url_obsługiwana': [d.base_url for d in url_extraction_domains],
        },
        'poziomy_trudnosci': [d.value for d in Difficulty],
        'lączna_liczba_domen': len(DomainRegistry.get_all_domains()),
        'liczba_api_search': len(api_search_domains),
        'liczba_web_scraping': len(web_scraping_domains),
        'liczba_url_extraction': len(url_extraction_domains)
    }

    return str(info)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point for the server"""
    logger.info(f"Starting Polish History Tools MCP Server v{SERVER_VERSION}")
    logger.info("Multi-domain search and content extraction tools")
    mcp.run()


if __name__ == "__main__":
    main()

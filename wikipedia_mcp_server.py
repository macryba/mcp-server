#!/usr/bin/env python3
"""
FastMCP server for Wikipedia search optimized for Polish history
Exposes search and page extraction tools to Claude Code
"""

from fastmcp import FastMCP
from wikipedia_client import WikipediaClient
import json

# Initialize FastMCP server
mcp = FastMCP("Polish History Wikipedia Search")

# Initialize Wikipedia clients for different languages
clients = {
    'pl': WikipediaClient('pl'),  # Polish
    'en': WikipediaClient('en'),  # English
}


@mcp.tool()
def search_wikipedia(query: str, max_results: int = 5) -> str:
    """
    Search Polish Wikipedia for historical information

    Args:
        query: Search query (e.g., "Bolesław III Krzywousty")
        max_results: Maximum number of results to return (1-20)

    Returns:
        JSON string with search results including titles, snippets, and URLs
    """
    try:
        client = clients['pl']
        results = client.search(query, max_results)
        return json.dumps(results, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({'error': str(e)}, ensure_ascii=False)


@mcp.tool()
def search_wikipedia_english(query: str, max_results: int = 5) -> str:
    """
    Search English Wikipedia for additional context

    Args:
        query: Search query in English
        max_results: Maximum number of results to return (1-20)

    Returns:
        JSON string with search results
    """
    try:
        client = clients['en']
        results = client.search(query, max_results)
        return json.dumps(results, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({'error': str(e)}, ensure_ascii=False)


@mcp.tool()
def get_wikipedia_page(title: str, language: str = 'pl') -> str:
    """
    Get full Wikipedia page content and summary

    Args:
        title: Exact page title (e.g., "Bolesław III Krzywousty")
        language: Wikipedia language edition ('pl' or 'en')

    Returns:
        JSON string with page content, URL, and metadata
    """
    try:
        client = clients.get(language, clients['pl'])
        page_data = client.get_page_content(title)
        return json.dumps(page_data, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({'error': str(e)}, ensure_ascii=False)


@mcp.tool()
def search_polish_historical_figures(query: str) -> str:
    """
    Search Polish Wikipedia specifically for historical figures

    Optimized for searching Polish kings, queens, leaders, and historical personalities.

    Args:
        query: Name or description of historical figure

    Returns:
        JSON string with relevant biographical information
    """
    try:
        # Add context-specific search terms for better results
        enhanced_query = f"{query} król Polski książę historii" if len(query.split()) < 3 else query

        client = clients['pl']
        results = client.search(enhanced_query, 5)

        # Add context about Polish historical sources
        for result in results:
            if 'error' not in result:
                result['source_type'] = 'Polish historical figure'
                result['suggested_domains'] = [
                    'pl.wikipedia.org',
                    'ipn.gov.pl',
                    'dzieje.pl',
                    'psb.org.pl'  # Polish Biographical Dictionary
                ]

        return json.dumps(results, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({'error': str(e)}, ensure_ascii=False)


@mcp.tool()
def search_polish_historical_events(query: str) -> str:
    """
    Search Polish Wikipedia for historical events

    Optimized for searching battles, uprisings, treaties, and historical events.

    Args:
        query: Event name or description (e.g., "Powstanie styczniowe", "Bitwa pod Grunwaldem")

    Returns:
        JSON string with event information
    """
    try:
        # Enhance query for historical events
        enhanced_query = f"{query} wydarzenie historia Polska"

        client = clients['pl']
        results = client.search(enhanced_query, 5)

        for result in results:
            if 'error' not in result:
                result['source_type'] = 'Polish historical event'
                result['suggested_domains'] = [
                    'pl.wikipedia.org',
                    'dzieje.pl',
                    'ipn.gov.pl',
                    'encyklopedia.pwn.pl'
                ]

        return json.dumps(results, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({'error': str(e)}, ensure_ascii=False)


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()

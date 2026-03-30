#!/usr/bin/env python3
"""
FastMCP server for Polish History Quiz Application
Provides multi-domain search, content extraction, and quiz generation tools

This is the NEW server entry point - replaces wikipedia_mcp_server.py
"""

from fastmcp import FastMCP
from tools import search, extract, quiz
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

    Supports multi-domain search across:
    - Wikipedia (Polish and English)
    - IPN (Institute of National Remembrance) - coming soon
    - Dzieje.pl - coming soon
    - Polona digital library - coming soon
    - PSB (Polish Biographical Dictionary) - coming soon
    - PWN Encyclopedia - coming soon

    Args:
        query: Search query string (e.g., "Bolesław III Krzywousty")
        domains: List of domains to search (empty = all available domains)
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
async def search_wikipedia_polish(query: str, max_results: int = 5) -> str:
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
        results = await search.search_wikipedia_polish(query, max_results)
        return results
    except Exception as e:
        logger.error(f"Error in search_wikipedia_polish: {e}")
        return str({'error': str(e)})


@mcp.tool()
async def search_wikipedia_english(query: str, max_results: int = 5) -> str:
    """
    Search English Wikipedia for additional context

    Use this when you need:
    - English-language perspective
    - International context for Polish events
    - Additional details not in Polish Wikipedia

    Args:
        query: Search query in English
        max_results: Maximum number of results to return (1-20)

    Returns:
        JSON string with search results
    """
    try:
        results = await search.search_wikipedia_english(query, max_results)
        return results
    except Exception as e:
        logger.error(f"Error in search_wikipedia_english: {e}")
        return str({'error': str(e)})


@mcp.tool()
async def search_historical_figures(query: str, period: str = None) -> str:
    """
    Search Polish Wikipedia specifically for historical figures

    Optimized for searching Polish kings, queens, leaders, and historical personalities.

    Args:
        query: Name or description of historical figure
        period: Optional time period (e.g., "XVII wiek", "1945-1989")

    Returns:
        JSON string with relevant biographical information and suggested sources
    """
    try:
        results = await search.search_historical_figures(query, period)
        return results
    except Exception as e:
        logger.error(f"Error in search_historical_figures: {e}")
        return str({'error': str(e)})


@mcp.tool()
async def search_historical_events(query: str, date_range: str = None) -> str:
    """
    Search Polish Wikipedia for historical events

    Optimized for searching battles, uprisings, treaties, and historical events.

    Args:
        query: Event name or description (e.g., "Powstanie styczniowe", "Bitwa pod Grunwaldem")
        date_range: Optional date range (e.g., "1939-1945")

    Returns:
        JSON string with event information and suggested sources
    """
    try:
        results = await search.search_historical_events(query, date_range)
        return results
    except Exception as e:
        logger.error(f"Error in search_historical_events: {e}")
        return str({'error': str(e)})


@mcp.tool()
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
        results = await search.search_historical_places(query, region)
        return results
    except Exception as e:
        logger.error(f"Error in search_historical_places: {e}")
        return str({'error': str(e)})


@mcp.tool()
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
        results = await search.search_primary_sources(query, source_type)
        return results
    except Exception as e:
        logger.error(f"Error in search_primary_sources: {e}")
        return str({'error': str(e)})


@mcp.tool()
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
        results = await search.search_biographies(query, profession)
        return results
    except Exception as e:
        logger.error(f"Error in search_biographies: {e}")
        return str({'error': str(e)})


# ============================================================================
# EXTRACT TOOLS
# ============================================================================

@mcp.tool()
async def extract_article(url: str) -> str:
    """
    Fetch a page and return cleaned title, URL, and article text

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


@mcp.tool()
async def extract_facts(url: str) -> str:
    """
    Extract dates, people, places, and events from a history article

    Args:
        url: URL of the article

    Returns:
        JSON string with structured facts (dates, figures, events, locations)
    """
    try:
        results = await extract.extract_facts(url)
        return results
    except Exception as e:
        logger.error(f"Error in extract_facts: {e}")
        return str({'error': str(e)})


@mcp.tool()
async def extract_timeline(url: str) -> str:
    """
    Extract timeline events from an article

    Args:
        url: URL of the article

    Returns:
        JSON string with timeline events
    """
    try:
        results = await extract.extract_timeline(url)
        return results
    except Exception as e:
        logger.error(f"Error in extract_timeline: {e}")
        return str({'error': str(e)})


@mcp.tool()
async def extract_biography(url: str) -> str:
    """
    Extract biographical data from an article

    Args:
        url: URL of the biographical article

    Returns:
        JSON string with biographical information
    """
    try:
        results = await extract.extract_biography(url)
        return results
    except Exception as e:
        logger.error(f"Error in extract_biography: {e}")
        return str({'error': str(e)})


# ============================================================================
# QUIZ TOOLS
# ============================================================================

@mcp.tool()
async def generate_quiz_question(topic: str, difficulty: str = 'medium', question_type: str = 'multiple_choice') -> str:
    """
    Generate a single quiz question on a historical topic

    Supported question types:
    - multiple_choice: Multiple choice question
    - date: Date-based question
    - figure_identification: Identify historical figure
    - event_identification: Identify historical event

    Args:
        topic: Historical topic (e.g., "Bolesław III Krzywousty", "Bitwa pod Grunwaldem")
        difficulty: Difficulty level (easy, medium, hard, expert)
        question_type: Type of question to generate

    Returns:
        JSON string with quiz question
    """
    try:
        results = await quiz.generate_quiz_question(topic, difficulty, question_type)
        return results
    except Exception as e:
        logger.error(f"Error in generate_quiz_question: {e}")
        return str({'error': str(e)})


@mcp.tool()
async def generate_quiz_questions(topic: str, count: int = 5, difficulty: str = 'medium') -> str:
    """
    Generate multiple quiz questions on a historical topic

    Args:
        topic: Historical topic
        count: Number of questions to generate (default: 5)
        difficulty: Difficulty level (easy, medium, hard, expert)

    Returns:
        JSON string with list of quiz questions
    """
    try:
        results = await quiz.generate_quiz_questions(topic, count, difficulty)
        return results
    except Exception as e:
        logger.error(f"Error in generate_quiz_questions: {e}")
        return str({'error': str(e)})


@mcp.tool()
async def validate_quiz_answer(question_url: str, user_answer: str) -> str:
    """
    Validate a quiz answer against the source material

    Args:
        question_url: URL of the source article
        user_answer: User's answer

    Returns:
        JSON string with validation result and feedback
    """
    try:
        results = await quiz.validate_quiz_answer(question_url, user_answer)
        return results
    except Exception as e:
        logger.error(f"Error in validate_quiz_answer: {e}")
        return str({'error': str(e)})


@mcp.tool()
async def extract_quiz_facts(topic: str, count: int = 10) -> str:
    """
    Extract facts suitable for quiz generation

    Args:
        topic: Historical topic
        count: Number of facts to extract (default: 10)

    Returns:
        JSON string with quiz-relevant facts
    """
    try:
        results = await quiz.extract_quiz_facts(topic, count)
        return results
    except Exception as e:
        logger.error(f"Error in extract_quiz_facts: {e}")
        return str({'error': str(e)})


@mcp.tool()
async def generate_multiple_choice(topic: str, difficulty: str = 'medium') -> str:
    """
    Generate a multiple choice question

    Args:
        topic: Historical topic
        difficulty: Difficulty level

    Returns:
        JSON string with multiple choice question
    """
    try:
        results = await quiz.generate_multiple_choice(topic, difficulty)
        return results
    except Exception as e:
        logger.error(f"Error in generate_multiple_choice: {e}")
        return str({'error': str(e)})


# ============================================================================
# SERVER INFO
# ============================================================================

@mcp.tool()
async def server_info() -> str:
    """
    Get server information and capabilities

    Returns:
        JSON string with server information
    """
    info = {
        'name': 'Polish History Tools',
        'version': SERVER_VERSION,
        'description': 'MCP server for Polish history research with multi-domain search, content extraction, and quiz generation',
        'capabilities': {
            'search': [
                'Multi-domain search',
                'Wikipedia search (Polish & English)',
                'Historical figures search',
                'Historical events search',
                'Places search',
                'Primary sources search',
                'Biographies search'
            ],
            'extract': [
                'Article extraction',
                'Fact extraction',
                'Timeline extraction',
                'Biography extraction'
            ],
            'quiz': [
                'Question generation',
                'Multiple questions generation',
                'Answer validation',
                'Quiz fact extraction',
                'Multiple choice generation',
                'Date questions',
                'Figure identification',
                'Event identification'
            ]
        },
        'supported_domains': [
            'pl.wikipedia.org',
            'en.wikipedia.org'
        ],
        'coming_soon': [
            'ipn.gov.pl',
            'dzieje.pl',
            'polona.pl',
            'psb.org.pl',
            'encyklopedia.pwn.pl'
        ]
    }

    return str(info)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point for the server"""
    logger.info(f"Starting Polish History Tools MCP Server v{SERVER_VERSION}")
    logger.info("Multi-domain search, content extraction, and quiz generation tools")
    mcp.run()


if __name__ == "__main__":
    main()

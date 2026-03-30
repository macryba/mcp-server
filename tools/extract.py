#!/usr/bin/env python3
"""
Content extraction tools for Polish history research
Provides tools to extract and process content from various sources
"""

from services.domains.wikipedia import WikipediaService
from services.http_client import HTTPClient
from services.cache import get_cache
from utils.text import clean_html, normalize_whitespace, extract_snippet
from utils.dates import extract_dates, parse_polish_date
from typing import Dict, Any, List
import logging
import re

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


async def extract_facts(url: str) -> str:
    """
    Extract dates, people, places, and events from a history article

    Args:
        url: URL of the article

    Returns:
        JSON string with structured facts (dates, figures, events, locations)
    """
    try:
        # First, extract the article content
        article_data = await extract_article(url)
        article = eval(article_data)  # Convert back to dict (hacky, but works for now)

        if 'error' in article:
            return str(article)

        content = article.get('content', '')
        title = article.get('title', '')

        # Extract facts
        facts = {
            'url': url,
            'title': title,
            'dates': extract_dates(content),
            'figures': extract_figures(content),
            'events': extract_events(content),
            'locations': extract_locations(content)
        }

        return str(facts)
    except Exception as e:
        logger.error(f"Error in extract_facts: {e}")
        return str({'error': str(e), 'url': url})


async def extract_timeline(url: str) -> str:
    """
    Extract timeline events from an article

    Args:
        url: URL of the article

    Returns:
        JSON string with timeline events
    """
    try:
        article_data = await extract_article(url)
        article = eval(article_data)

        if 'error' in article:
            return str(article)

        content = article.get('content', '')

        # Extract timeline events (this is a simplified version)
        # In a full implementation, this would use more sophisticated NLP
        timeline = []
        sentences = re.split(r'[.!?]+', content)

        for sentence in sentences[:20]:  # First 20 sentences
            dates = extract_dates(sentence)
            if dates:
                timeline.append({
                    'date': dates[0],
                    'event': sentence.strip(),
                    'source_url': url
                })

        result = {
            'url': url,
            'timeline': timeline
        }

        return str(result)
    except Exception as e:
        logger.error(f"Error in extract_timeline: {e}")
        return str({'error': str(e), 'url': url})


async def extract_biography(url: str) -> str:
    """
    Extract biographical data from an article

    Args:
        url: URL of the biographical article

    Returns:
        JSON string with biographical information
    """
    try:
        article_data = await extract_article(url)
        article = eval(article_data)

        if 'error' in article:
            return str(article)

        content = article.get('content', '')
        title = article.get('title', '')

        # Extract biographical information
        bio = {
            'name': title,
            'birth_date': None,
            'death_date': None,
            'nationality': 'Polish',  # Default assumption
            'occupation': None,
            'biography': extract_snippet(content, 500),
            'source_url': url
        }

        # Try to extract birth and death dates
        dates = extract_dates(content)
        if len(dates) >= 1:
            bio['birth_date'] = dates[0]
        if len(dates) >= 2:
            bio['death_date'] = dates[-1]

        # Try to extract occupation (simplified)
        # Look for common patterns like "Był polskim [occupation]"
        occupation_match = re.search(r'był[a-z]*\s+(polskim[a-z]*)?\s*(\w+)', content, re.IGNORECASE)
        if occupation_match:
            bio['occupation'] = occupation_match.group(2)

        return str(bio)
    except Exception as e:
        logger.error(f"Error in extract_biography: {e}")
        return str({'error': str(e), 'url': url})


async def extract_locations(url: str) -> str:
    """
    Extract geographical references from an article

    Args:
        url: URL of the article

    Returns:
        JSON string with geographical locations mentioned
    """
    try:
        article_data = await extract_article(url)
        article = eval(article_data)

        if 'error' in article:
            return str(article)

        content = article.get('content', '')

        locations = extract_locations_from_text(content)

        result = {
            'url': url,
            'locations': locations
        }

        return str(result)
    except Exception as e:
        logger.error(f"Error in extract_locations: {e}")
        return str({'error': str(e), 'url': url})


async def extract_dates(url: str) -> str:
    """
    Extract and normalize dates from an article

    Args:
        url: URL of the article

    Returns:
        JSON string with extracted dates in ISO format
    """
    try:
        article_data = await extract_article(url)
        article = eval(article_data)

        if 'error' in article:
            return str(article)

        content = article.get('content', '')

        dates = extract_dates(content)

        result = {
            'url': url,
            'dates': dates,
            'count': len(dates)
        }

        return str(result)
    except Exception as e:
        logger.error(f"Error in extract_dates: {e}")
        return str({'error': str(e), 'url': url})


# Helper functions

def extract_figures(text: str) -> List[str]:
    """
    Extract historical figures mentioned in text

    Args:
        text: Text to analyze

    Returns:
        List of figure names
    """
    # This is a simplified implementation
    # In a full version, this would use NER (Named Entity Recognition)
    figures = []

    # Look for patterns like "Jan Sobieski", "Mieszko I", etc.
    # Polish name pattern: First letter capital, possibly with Roman numerals
    name_pattern = r'\b[A-ZŻŁĆŚŃÓĘ][a-zążłćśńóę]+(?:\s+[A-ZŻŁĆŚŃÓĘ][a-zążłćśńóę]+)+\b'
    matches = re.findall(name_pattern, text)

    # Filter common non-figure words
    common_words = {'Polska', 'Polski', 'Historia', 'Warszawa', 'Kraków'}
    figures = [name for name in matches if name not in common_words]

    return list(set(figures))[:10]  # Return unique, max 10


def extract_events(text: str) -> List[str]:
    """
    Extract historical events mentioned in text

    Args:
        text: Text to analyze

    Returns:
        List of event descriptions
    """
    events = []

    # Look for event-related keywords
    event_keywords = ['bitwa', 'powstanie', 'traktat', 'wojna', 'zjazd', 'unia', 'akt', 'rozbiór']

    sentences = re.split(r'[.!?]+', text)

    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in event_keywords):
            events.append(sentence.strip())

    return events[:10]  # Max 10 events


def extract_locations_from_text(text: str) -> List[str]:
    """
    Extract geographical locations from text

    Args:
        text: Text to analyze

    Returns:
        List of location names
    """
    locations = []

    # Capitalized words that might be locations
    # This is simplified - a full implementation would use a gazetteer
    location_pattern = r'\b[A-ZŻŁĆŚŃÓĘ][a-zążłćśńóę]+(?:\s+[A-ZŻŁĆŚŃÓĘ][a-zążłćśńóę]+)*\b'
    matches = re.findall(location_pattern, text)

    # Filter to likely locations (would need a gazetteer for accuracy)
    location_indicators = ['rzeka', 'miasto', 'województwo', 'region', 'góra', 'jeziero']

    for match in matches:
        if any(indicator in text.lower() for indicator in location_indicators):
            locations.append(match)

    return list(set(locations))[:10]  # Return unique, max 10


# Cleanup function
async def cleanup():
    """Cleanup resources"""
    await _http_client.close()

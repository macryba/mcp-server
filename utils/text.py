#!/usr/bin/env python3
"""
Text processing utilities
"""

import re
import html
from typing import Optional, List


def clean_html(text: str) -> str:
    """
    Remove HTML tags from text

    Args:
        text: Text with HTML tags

    Returns:
        Clean text without HTML tags
    """
    if not text:
        return ""

    # Remove HTML tags
    clean = re.sub(r'<[^<]+?>', '', text)

    # Decode HTML entities
    clean = html.unescape(clean)

    return clean


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in text

    Args:
        text: Text with irregular whitespace

    Returns:
        Text with normalized whitespace
    """
    if not text:
        return ""

    # Replace multiple spaces with single space
    clean = re.sub(r'\s+', ' ', text)

    # Strip leading/trailing whitespace
    clean = clean.strip()

    return clean


def extract_snippet(text: str, max_length: int = 200, suffix: str = "...") -> str:
    """
    Extract a snippet from text

    Args:
        text: Source text
        max_length: Maximum length of snippet
        suffix: Suffix to add if text is truncated

    Returns:
        Text snippet
    """
    if not text:
        return ""

    if len(text) <= max_length:
        return text

    # Truncate at max_length
    snippet = text[:max_length]

    # Try to find a good break point (space, comma, period)
    for i in range(max_length - 1, max_length - 50, -1):
        if snippet[i] in ' ,.;:!?\n':
            snippet = snippet[:i + 1]
            break

    return snippet + suffix


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to maximum length

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text
    """
    if not text:
        return ""

    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def extract_keywords(text: str, min_length: int = 4) -> List[str]:
    """
    Extract keywords from text

    Args:
        text: Source text
        min_length: Minimum word length

    Returns:
        List of keywords
    """
    if not text:
        return []

    # Remove punctuation and convert to lowercase
    words = re.sub(r'[^\w\s]', ' ', text.lower()).split()

    # Filter by length and remove common words
    common_words = {'the', 'and', 'that', 'have', 'for', 'not', 'with', 'you', 'this', 'but', 'his', 'from', 'they', 'she', 'her', 'been', 'than', 'its', 'are', 'was', 'were'}

    keywords = [word for word in words if len(word) >= min_length and word not in common_words]

    return keywords


def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent injection attacks

    Args:
        text: User input text

    Returns:
        Sanitized text
    """
    if not text:
        return ""

    # Remove potentially dangerous characters
    text = re.sub(r'[<>"\']', '', text)

    # Normalize whitespace
    text = normalize_whitespace(text)

    return text


def remove_polish_diacritics(text: str) -> str:
    """
    Remove Polish diacritics from text

    Args:
        text: Text with Polish diacritics

    Returns:
        Text without diacritics
    """
    if not text:
        return ""

    polish_map = {
        'ą': 'a', 'ć': 'c', 'ę': 'e',
        'ł': 'l', 'ń': 'n', 'ó': 'o',
        'ś': 's', 'ź': 'z', 'ż': 'z',
        'Ą': 'A', 'Ć': 'C', 'Ę': 'E',
        'Ł': 'L', 'Ń': 'N', 'Ó': 'O',
        'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
    }

    for char, replacement in polish_map.items():
        text = text.replace(char, replacement)

    return text


def count_words(text: str) -> int:
    """
    Count words in text

    Args:
        text: Text to count

    Returns:
        Number of words
    """
    if not text:
        return 0

    words = text.split()
    return len(words)


def extract_sentences(text: str, max_sentences: int = 3) -> str:
    """
    Extract first N sentences from text

    Args:
        text: Source text
        max_sentences: Maximum number of sentences

    Returns:
        Text with first N sentences
    """
    if not text:
        return ""

    # Split by sentence boundaries
    sentences = re.split(r'[.!?]+', text)

    # Filter empty sentences
    sentences = [s.strip() for s in sentences if s.strip()]

    # Take first N sentences
    selected = sentences[:max_sentences]

    # Rejoin with periods
    result = '. '.join(selected)

    if result and not result.endswith('.'):
        result += '.'

    return result

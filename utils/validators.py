#!/usr/bin/env python3
"""
Input validation utilities
"""

import re
from typing import Optional, List
from urllib.parse import urlparse
from models.domains import get_trusted_domains


# Trusted Polish history domains - centralized from models/domains.py
TRUSTED_DOMAINS: List[str] = list(get_trusted_domains())


def validate_url(url: str) -> bool:
    """
    Validate URL format

    Args:
        url: URL to validate

    Returns:
        True if valid, False otherwise
    """
    if not url:
        return False

    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def is_trusted_domain(url: str) -> bool:
    """
    Check if URL is from a trusted domain

    Args:
        url: URL to check

    Returns:
        True if from trusted domain, False otherwise
    """
    if not url:
        return False

    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        # Check if domain or parent domain is in trusted list
        for trusted in TRUSTED_DOMAINS:
            if domain == trusted or domain.endswith('.' + trusted):
                return True

        return False
    except Exception:
        return False


def validate_domain(domain: str) -> bool:
    """
    Validate domain name

    Args:
        domain: Domain name to validate

    Returns:
        True if valid, False otherwise
    """
    if not domain:
        return False

    # Basic domain validation
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]?(\.[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]?)*$'
    return bool(re.match(pattern, domain))


def sanitize_search_query(query: str) -> str:
    """
    Sanitize search query to prevent injection

    Args:
        query: Search query

    Returns:
        Sanitized query
    """
    if not query:
        return ""

    # Remove special characters that could be used for injection
    query = re.sub(r'[<>"\'\\]', '', query)

    # Remove excessive whitespace
    query = re.sub(r'\s+', ' ', query)

    return query.strip()


def validate_search_query(query: str, min_length: int = 2, max_length: int = 200) -> bool:
    """
    Validate search query

    Args:
        query: Search query
        min_length: Minimum length
        max_length: Maximum length

    Returns:
        True if valid, False otherwise
    """
    if not query:
        return False

    query = query.strip()

    if len(query) < min_length or len(query) > max_length:
        return False

    return True


def validate_limit(limit: int, min_val: int = 1, max_val: int = 100) -> bool:
    """
    Validate limit parameter

    Args:
        limit: Limit value
        min_val: Minimum allowed value
        max_val: Maximum allowed value

    Returns:
        True if valid, False otherwise
    """
    return min_val <= limit <= max_val


def validate_language_code(code: str) -> bool:
    """
    Validate ISO language code

    Args:
        code: Language code (e.g., 'pl', 'en')

    Returns:
        True if valid, False otherwise
    """
    if not code:
        return False

    return len(code) == 2 and code.isalpha()


def validate_email(email: str) -> bool:
    """
    Validate email address (if needed for notifications)

    Args:
        email: Email address

    Returns:
        True if valid, False otherwise
    """
    if not email:
        return False

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file system usage

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    if not filename:
        return "unnamed"

    # Remove path separators
    filename = filename.replace('/', '').replace('\\', '')

    # Remove dangerous characters
    filename = re.sub(r'[<>:"|?*]', '', filename)

    # Replace spaces with underscores
    filename = filename.replace(' ', '_')

    # Limit length
    if len(filename) > 255:
        filename = filename[:255]

    return filename


def validate_positive_integer(value: int) -> bool:
    """
    Validate that value is a positive integer

    Args:
        value: Value to validate

    Returns:
        True if positive integer, False otherwise
    """
    return isinstance(value, int) and value > 0


def validate_date_string(date_str: str) -> bool:
    """
    Validate date string format

    Args:
        date_str: Date string

    Returns:
        True if valid date format, False otherwise
    """
    if not date_str:
        return False

    # ISO format: YYYY-MM-DD
    iso_pattern = r'^\d{4}-\d{2}-\d{2}$'
    if re.match(iso_pattern, date_str):
        return True

    # Year only: YYYY
    year_pattern = r'^\d{4}$'
    if re.match(year_pattern, date_str):
        return True

    return False


def get_allowed_domains() -> List[str]:
    """
    Get list of allowed/trusted domains

    Returns:
        List of trusted domains
    """
    return TRUSTED_DOMAINS.copy()

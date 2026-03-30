#!/usr/bin/env python3
"""
Date parsing and normalization utilities for Polish historical dates
"""

import re
from typing import Optional, List, Tuple
from datetime import datetime


# Polish month names
POLISH_MONTHS = {
    'stycznia': 1, 'styczeń': 1,
    'lutego': 2, 'luty': 2,
    'marca': 3, 'marzec': 3,
    'kwietnia': 4, 'kwiecień': 4,
    'maja': 5, 'maj': 5,
    'czerwca': 6, 'czerwiec': 6,
    'lipca': 7, 'lipiec': 7,
    'sierpnia': 8, 'sierpień': 8,
    'września': 9, 'wrzesień': 9,
    'października': 10, 'październik': 10,
    'listopada': 11, 'listopad': 11,
    'grudnia': 12, 'grudzień': 12
}


def parse_polish_date(date_str: str) -> Optional[str]:
    """
    Parse Polish date string and convert to ISO format

    Args:
        date_str: Date string in Polish format

    Returns:
        ISO format date string (YYYY-MM-DD) or None if parsing fails
    """
    if not date_str:
        return None

    date_str = date_str.strip()

    # Try ISO format first
    if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
        return date_str

    # Try Polish format: "DD month YYYY"
    polish_pattern = r'(\d{1,2})\s+(\w+)\s+(\d{4})'
    match = re.search(polish_pattern, date_str, re.IGNORECASE)

    if match:
        day = int(match.group(1))
        month_name = match.group(2).lower()
        year = int(match.group(3))

        if month_name in POLISH_MONTHS:
            month = POLISH_MONTHS[month_name]
            try:
                return f"{year:04d}-{month:02d}-{day:02d}"
            except ValueError:
                pass

    # Try year only
    year_match = re.search(r'\d{4}', date_str)
    if year_match:
        return year_match.group(0) + "-01-01"

    return None


def extract_dates(text: str) -> List[str]:
    """
    Extract all dates from text

    Args:
        text: Text to search for dates

    Returns:
        List of ISO format date strings
    """
    if not text:
        return []

    dates = []

    # Find all potential date patterns
    # ISO format
    iso_dates = re.findall(r'\b\d{4}-\d{2}-\d{2}\b', text)
    dates.extend(iso_dates)

    # Polish format dates
    polish_dates = re.findall(r'\b\d{1,2}\s+\w+\s+\d{4}\b', text)
    for date_str in polish_dates:
        parsed = parse_polish_date(date_str)
        if parsed:
            dates.append(parsed)

    # Years
    years = re.findall(r'\b\d{4}\b', text)
    for year in years:
        # Filter reasonable year ranges
        if 1000 <= int(year) <= datetime.now().year + 1:
            iso_date = f"{year}-01-01"
            if iso_date not in dates:
                dates.append(iso_date)

    # Remove duplicates and sort
    dates = sorted(list(set(dates)))

    return dates


def parse_date_range(date_range_str: str) -> Optional[Tuple[str, str]]:
    """
    Parse date range string

    Args:
        date_range_str: Date range string (e.g., "1939-1945", "XVI-XVII wiek")

    Returns:
        Tuple of (start_date, end_date) in ISO format or None
    """
    if not date_range_str:
        return None

    # Try numeric range: "1939-1945"
    match = re.match(r'(\d{4})\s*-\s*(\d{4})', date_range_str)
    if match:
        start = match.group(1) + "-01-01"
        end = match.group(2) + "-12-31"
        return (start, end)

    # Try century: "XX wiek", "XIX wieku"
    century_match = re.search(r'([IVX]+)\s*(?:wiek|wieku|century)', date_range_str, re.IGNORECASE)
    if century_match:
        roman = century_match.group(1).upper()
        century = roman_to_int(roman)
        if century:
            start_year = (century - 1) * 100 + 1
            end_year = century * 100
            return (f"{start_year}-01-01", f"{end_year}-12-31")

    return None


def roman_to_int(roman: str) -> Optional[int]:
    """
    Convert Roman numeral to integer

    Args:
        roman: Roman numeral string

    Returns:
        Integer value or None if invalid
    """
    roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}

    total = 0
    prev_value = 0

    for char in reversed(roman):
        if char not in roman_values:
            return None

        value = roman_values[char]
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value

    return total


def validate_date(date_str: str) -> bool:
    """
    Validate date string

    Args:
        date_str: Date string to validate

    Returns:
        True if valid, False otherwise
    """
    if not date_str:
        return False

    # Try ISO format
    try:
        datetime.fromisoformat(date_str)
        return True
    except ValueError:
        pass

    # Try Polish format
    parsed = parse_polish_date(date_str)
    return parsed is not None


def format_year_range(start_year: int, end_year: int) -> str:
    """
    Format year range for display

    Args:
        start_year: Start year
        end_year: End year

    Returns:
        Formatted range string
    """
    if start_year == end_year:
        return str(start_year)

    return f"{start_year}-{end_year}"


def calculate_century(year: int) -> int:
    """
    Calculate century from year

    Args:
        year: Year

    Returns:
        Century number
    """
    return (year - 1) // 100 + 1


def get_century_name(century: int) -> str:
    """
    Get Polish century name

    Args:
        century: Century number

    Returns:
        Century name in Polish (e.g., "XX wiek")
    """
    roman_numerals = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X',
                      'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX',
                      'XXI', 'XXII']

    if 1 <= century <= len(roman_numerals):
        return f"{roman_numerals[century - 1]} wiek"

    return f"{century} wiek"

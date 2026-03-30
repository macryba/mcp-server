#!/usr/bin/env python3
"""
Data models for search functionality
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class SearchResult:
    """
    Represents a single search result

    Attributes:
        title: Result title
        url: Result URL
        snippet: Brief description/snippet
        source: Source domain (e.g., 'wikipedia', 'ipn')
        relevance_score: Relevance score (0-1)
        metadata: Additional metadata
    """
    title: str
    url: str
    snippet: str
    source: str
    relevance_score: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'title': self.title,
            'url': self.url,
            'snippet': self.snippet,
            'source': self.source,
            'relevance_score': self.relevance_score,
            'metadata': self.metadata
        }


@dataclass
class QueryParams:
    """
    Search query parameters

    Attributes:
        query: Search query string
        limit: Maximum number of results
        offset: Result offset for pagination
        domains: List of domains to search (empty = all)
        date_range: Optional date range filter
        filters: Additional filters
    """
    query: str
    limit: int = 10
    offset: int = 0
    domains: list[str] = field(default_factory=list)
    date_range: Optional[tuple[str, str]] = None
    filters: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'query': self.query,
            'limit': self.limit,
            'offset': self.offset,
            'domains': self.domains,
            'date_range': self.date_range,
            'filters': self.filters
        }

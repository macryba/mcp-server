#!/usr/bin/env python3
"""
Data models for historical facts and events
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class HistoricalFact:
    """
    Represents a historical fact

    Attributes:
        fact: The fact statement
        date: Date of the fact (ISO format or None)
        location: Location where the fact occurred
        figures: List of historical figures involved
        category: Fact category (e.g., 'battle', 'treaty', 'birth')
        source_url: URL of the source
        confidence: Confidence score (0-1)
        metadata: Additional metadata
    """
    fact: str
    category: str
    source_url: str
    date: Optional[str] = None
    location: Optional[str] = None
    figures: List[str] = field(default_factory=list)
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'fact': self.fact,
            'date': self.date,
            'location': self.location,
            'figures': self.figures,
            'category': self.category,
            'source_url': self.source_url,
            'confidence': self.confidence,
            'metadata': self.metadata
        }


@dataclass
class TimelineEvent:
    """
    Represents an event on a historical timeline

    Attributes:
        title: Event title
        date: Event date (ISO format)
        description: Event description
        location: Event location
        participants: List of participants
        significance: Event significance (1-10)
        source_url: URL of the source
        related_events: URLs of related events
        metadata: Additional metadata
    """
    title: str
    date: str
    description: str
    source_url: str
    location: Optional[str] = None
    participants: List[str] = field(default_factory=list)
    significance: int = 5
    related_events: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'title': self.title,
            'date': self.date,
            'description': self.description,
            'location': self.location,
            'participants': self.participants,
            'significance': self.significance,
            'source_url': self.source_url,
            'related_events': self.related_events,
            'metadata': self.metadata
        }


@dataclass
class Biography:
    """
    Represents a biographical entry

    Attributes:
        name: Person's name
        birth_date: Birth date (ISO format or None)
        death_date: Death date (ISO format or None)
        nationality: Nationality
        occupation: Occupation/role
        biography: Brief biography
        notable_achievements: List of notable achievements
        source_url: URL of the source
        metadata: Additional metadata
    """
    name: str
    biography: str
    source_url: str
    birth_date: Optional[str] = None
    death_date: Optional[str] = None
    nationality: Optional[str] = None
    occupation: Optional[str] = None
    notable_achievements: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def life_span(self) -> Optional[str]:
        """Get life span as a string"""
        if self.birth_date and self.death_date:
            return f"{self.birth_date} - {self.death_date}"
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'birth_date': self.birth_date,
            'death_date': self.death_date,
            'life_span': self.life_span,
            'nationality': self.nationality,
            'occupation': self.occupation,
            'biography': self.biography,
            'notable_achievements': self.notable_achievements,
            'source_url': self.source_url,
            'metadata': self.metadata
        }

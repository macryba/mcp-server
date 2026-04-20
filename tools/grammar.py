#!/usr/bin/env python3
"""
Grammar checking tools for Polish language
Provides MCP tools for grammar checking using LanguageTool
"""

import logging
from typing import Dict, Any
from services.grammar import GrammarCheckerService
from services.http_client import HTTPClient
from services.cache import get_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize service
_http_client = HTTPClient()
_cache = get_cache()
_grammar_service = None


def get_grammar_service() -> GrammarCheckerService:
    """
    Get or create grammar service instance

    Returns:
        GrammarCheckerService instance
    """
    global _grammar_service
    if _grammar_service is None:
        _grammar_service = GrammarCheckerService(http_client=_http_client)
    return _grammar_service


async def check_grammar(text: str, language: str = "pl-PL") -> str:
    """
    Check Polish grammar using LanguageTool

    This tool checks text for grammar, spelling, and style errors using
    the LanguageTool API. Returns detailed error information with suggestions.

    Args:
        text: Text to check for grammar errors
        language: Language code (default: pl-PL for Polish)
                 Examples: pl-PL, en-US, en-GB, de-DE, fr-FR

    Returns:
        JSON string with grammar errors and suggestions:
        {
            "matches": [
                {
                    "message": "Detailed error message",
                    "shortMessage": "Short error description",
                    "replacements": ["suggestion1", "suggestion2"],
                    "context": {
                        "text": "Context text",
                        "offset": 0,
                        "length": 5
                    },
                    "rule": {
                        "id": "RULE_ID",
                        "description": "Rule description",
                        "issueType": "grammar|spelling|style",
                        "category": {
                            "id": "CATEGORY_ID",
                            "name": "Category name"
                        }
                    },
                    "sentence": "Full sentence with error"
                }
            ],
            "language": {
                "name": "Polish",
                "code": "pl-PL",
                "detectedLanguage": {
                    "name": "Polish",
                    "code": "pl-PL",
                    "confidence": 1.0
                }
            }
        }

    Examples:
        >>> check_grammar("On poszedł do sklep.")
        >>> check_grammar("Ala ma kota.", language="pl-PL")
        >>> check_grammar("This are a test.", language="en-US")
    """
    try:
        if not text or not text.strip():
            logger.warning("Empty text provided for grammar check")
            return str({
                'matches': [],
                'language': {'code': language, 'name': 'Unknown'},
                'warning': 'No text provided'
            })

        logger.info(f"Checking grammar for text (length: {len(text)}, language: {language})")

        # Get grammar service and check text
        service = get_grammar_service()
        result = await service.check_grammar(text, language)

        # Add summary statistics
        match_count = len(result.get('matches', []))
        if match_count > 0:
            # Count by type
            type_counts = {}
            for match in result['matches']:
                issue_type = match.get('rule', {}).get('issueType', 'unknown')
                type_counts[issue_type] = type_counts.get(issue_type, 0) + 1

            result['summary'] = {
                'total_errors': match_count,
                'by_type': type_counts
            }
            logger.info(f"Found {match_count} errors: {type_counts}")
        else:
            result['summary'] = {
                'total_errors': 0,
                'message': 'No errors found - text looks good!'
            }
            logger.info("No grammar errors found")

        return str(result)

    except Exception as e:
        logger.error(f"Error in check_grammar: {e}")
        error_result = {
            'matches': [],
            'language': {'code': language, 'name': 'Unknown'},
            'error': str(e),
            'message': 'Failed to check grammar. Please ensure LanguageTool server is running.'
        }
        return str(error_result)


# Cleanup function to close HTTP client
async def cleanup():
    """Cleanup resources"""
    global _grammar_service
    if _grammar_service:
        await _grammar_service.close()
    await _http_client.close()

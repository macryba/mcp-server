#!/usr/bin/env python3
"""
Grammar checking service using LanguageTool
Provides Polish grammar checking capabilities through HTTP API
"""

import logging
from typing import Dict, Any, List, Optional
from services.http_client import HTTPClient
from config import config

logger = logging.getLogger(__name__)


class GrammarCheckerService:
    """
    Service for checking grammar using LanguageTool API

    Features:
    - Polish grammar checking
    - Multi-language support
    - Detailed error messages with suggestions
    - Context-aware error detection
    """

    def __init__(
        self,
        server_url: str = None,
        http_client: HTTPClient = None,
        timeout: int = None
    ):
        """
        Initialize GrammarCheckerService

        Args:
            server_url: LanguageTool server URL (default from config)
            http_client: HTTP client instance
            timeout: Request timeout in seconds
        """
        self.server_url = server_url or getattr(config, 'LANGUAGETOOL_SERVER_URL', 'http://localhost:8081')
        self.api_endpoint = f"{self.server_url}/v2/check"
        self.http_client = http_client or HTTPClient(timeout=timeout or 10)
        self.default_language = getattr(config, 'LANGUAGETOOL_DEFAULT_LANGUAGE', 'pl-PL')

        logger.info(f"Initialized GrammarCheckerService with server: {self.server_url}")

    async def check_grammar(
        self,
        text: str,
        language: str = None
    ) -> Dict[str, Any]:
        """
        Check grammar using LanguageTool API

        Args:
            text: Text to check for grammar errors
            language: Language code (e.g., 'pl-PL', 'en-US')

        Returns:
            Dictionary with grammar matches and language info

        Raises:
            HTTPClientError: If API request fails
        """
        if not text:
            return {
                'matches': [],
                'language': {
                    'name': 'Unknown',
                    'code': language or self.default_language,
                    'detectedLanguage': None
                },
                'error': 'No text provided'
            }

        language = language or self.default_language

        try:
            # Prepare request data for LanguageTool API
            params = {
                'text': text,
                'language': language,
                'enabledOnly': 'false'
            }

            logger.debug(f"Checking grammar for text: {text[:50]}... (language: {language})")

            # Send POST request to LanguageTool API
            # Note: LanguageTool expects form data, not JSON
            response = await self.http_client.post(
                self.api_endpoint,
                data=params  # Use form data, not JSON
            )

            # Parse response
            result = self._parse_response(response)

            logger.info(f"Grammar check completed: {len(result['matches'])} errors found")

            return result

        except Exception as e:
            logger.error(f"Error checking grammar: {e}")
            return {
                'matches': [],
                'language': {
                    'name': 'Unknown',
                    'code': language,
                    'detectedLanguage': None
                },
                'error': str(e)
            }

    def _parse_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse LanguageTool API response

        Args:
            response: Raw API response

        Returns:
            Parsed response with matches and language info
        """
        matches = []

        # Extract matches (grammar errors)
        for match in response.get('matches', []):
            match_data = {
                'message': match.get('message', ''),
                'shortMessage': match.get('shortMessage', ''),
                'replacements': [r.get('value', '') for r in match.get('replacements', [])],
                'context': {
                    'text': match.get('context', {}).get('text', ''),
                    'offset': match.get('context', {}).get('offset', 0),
                    'length': match.get('context', {}).get('length', 0)
                },
                'offset': match.get('offset', 0),
                'length': match.get('length', 0),
                'rule': {
                    'id': match.get('rule', {}).get('id', ''),
                    'description': match.get('rule', {}).get('description', ''),
                    'issueType': match.get('rule', {}).get('issueType', ''),
                    'category': {
                        'id': match.get('rule', {}).get('category', {}).get('id', ''),
                        'name': match.get('rule', {}).get('category', {}).get('name', '')
                    }
                },
                'sentence': match.get('sentence', '')
            }
            matches.append(match_data)

        # Extract language information
        language_info = response.get('language', {})
        parsed_language = {
            'name': language_info.get('name', ''),
            'code': language_info.get('code', ''),
            'detectedLanguage': {
                'name': language_info.get('detectedLanguage', {}).get('name', ''),
                'code': language_info.get('detectedLanguage', {}).get('code', ''),
                'confidence': language_info.get('detectedLanguage', {}).get('confidence', 0.0)
            }
        }

        return {
            'matches': matches,
            'language': parsed_language
        }

    async def close(self):
        """Close the HTTP client connection"""
        if self.http_client:
            await self.http_client.close()

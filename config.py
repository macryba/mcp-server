#!/usr/bin/env python3
"""
Configuration management for MCP server
"""

import os
from typing import List
from models.domains import get_trusted_domains


class Config:
    """Configuration settings for the MCP server"""

    # Server settings
    SERVER_NAME = "polish-history-tools"
    SERVER_VERSION = "2.0.0"

    # HTTP settings
    HTTP_TIMEOUT = 10
    HTTP_MAX_RETRIES = 3
    HTTP_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

    # Cache settings
    CACHE_ENABLED = True
    CACHE_TTL = 3600  # 1 hour in seconds
    CACHE_MAX_SIZE = 1000

    # Search settings
    DEFAULT_SEARCH_LIMIT = 10
    MAX_SEARCH_LIMIT = 100

    # Trusted domains - centralized from models/domains.py
    TRUSTED_DOMAINS: List[str] = list(get_trusted_domains())

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Wikipedia settings
    WIKIPEDIA_DEFAULT_LANGUAGE = 'pl'

    # Quiz settings
    QUIZ_DEFAULT_DIFFICULTY = 'medium'
    QUIZ_DEFAULT_COUNT = 5

    @classmethod
    def from_env(cls):
        """Load configuration from environment variables"""
        config = cls()

        # Override with environment variables if present
        if 'HTTP_TIMEOUT' in os.environ:
            config.HTTP_TIMEOUT = int(os.environ['HTTP_TIMEOUT'])
        if 'CACHE_TTL' in os.environ:
            config.CACHE_TTL = int(os.environ['CACHE_TTL'])
        if 'LOG_LEVEL' in os.environ:
            config.LOG_LEVEL = os.environ['LOG_LEVEL']

        return config


# Global configuration instance
config = Config.from_env()

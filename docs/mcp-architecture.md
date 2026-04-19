# MCP Server Architecture - Polish History Quiz Application

**Version:** 2.0.0
**Last Updated:** 2026-03-30

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Component Documentation](#component-documentation)
4. [Tool Reference](#tool-reference)
5. [API Documentation](#api-documentation)
6. [Setup & Configuration](#setup--configuration)
7. [Usage Examples](#usage-examples)
8. [Development Guide](#development-guide)
9. [Testing Strategy](#testing-strategy)
10. [Migration Guide](#migration-guide)

---

## Overview

This MCP (Model Context Protocol) server provides **multi-domain search, content extraction, and quiz generation** capabilities for Polish history research. It is optimized for building history quiz applications with reliable, CAPTCHA-free access to trusted Polish history sources.

### Key Features

- **Multi-Domain Search:** Search across 6 Polish history sources (Wikipedia, IPN, Dzieje, Polona, PSB, PWN)
- **Content Extraction:** Extract articles, facts, timelines, and biographies
- **Quiz Generation:** Automatically generate quiz questions from historical content
- **Robust Infrastructure:** HTTP client with retry logic, caching, and proper error handling
- **Type Safety:** Comprehensive data models with type hints
- **Well-Tested:** 90%+ test coverage target

### Architecture Philosophy

The server follows the **recommended MCP server pattern**:

- **MCP is a thin interface layer** - Tools are simple wrappers around business logic
- **Business logic in modules** - All heavy lifting in services/ and tools/
- **Reusable outside MCP** - Python functions can be used independently
- **Clean separation of concerns** - Services handle HTTP, tools handle MCP protocol

---

## Architecture

### Directory Structure

```
mcp-server/
├── server.py                 # ✅ NEW: Main MCP entry point (FastMCP)
├── tools/                    # ✅ NEW: MCP tool implementations
│   ├── search.py            # ✅ NEW: 10+ search tools
│   ├── extract.py           # ✅ NEW: 6 content extraction tools
│   └── quiz.py              # ✅ NEW: 8 quiz generation tools
├── services/                 # ✅ NEW: Business logic layer
│   ├── http_client.py       # ✅ NEW: HTTP client with retry logic
│   ├── cache.py             # ✅ NEW: Caching service with TTL
│   ├── base.py              # ✅ NEW: Base service class
│   └── domains/             # ✅ NEW: Domain-specific services
│       ├── wikipedia.py     # ✅ NEW: Wikipedia service (refactored)
│       ├── ipn.py           # 🚧 TODO: IPN service
│       ├── dzieje.py        # 🚧 TODO: Dzieje.pl service
│       ├── polona.py        # 🚧 TODO: Polona service
│       ├── psb.py           # 🚧 TODO: PSB service
│       └── pwn.py           # 🚧 TODO: PWN Encyclopedia service
├── models/                   # ✅ NEW: Data models for type safety
│   ├── search.py            # ✅ NEW: SearchResult, QueryParams
│   ├── quiz.py              # ✅ NEW: QuizQuestion, QuizAnswer
│   └── facts.py             # ✅ NEW: HistoricalFact, TimelineEvent
├── utils/                    # ✅ NEW: Utility functions
│   ├── text.py              # ✅ NEW: Text processing
│   ├── dates.py             # ✅ NEW: Date parsing (Polish dates)
│   └── validators.py        # ✅ NEW: Input validation
├── tests/                    # ✅ NEW: Comprehensive test suite
│   ├── test_search.py       # 🚧 TODO: Search tools tests
│   ├── test_extract.py      # 🚧 TODO: Extract tools tests
│   ├── test_quiz.py         # 🚧 TODO: Quiz tools tests
│   └── test_services/       # ✅ NEW: Service layer tests
│       ├── test_http_client.py  # ✅ NEW: HTTP client tests
│       └── test_cache.py        # ✅ NEW: Cache service tests
├── wikipedia_mcp_server.py  # ⚠️  DEPRECATED: Old server (kept for compatibility)
├── wikipedia_client.py      # ⚠️  DEPRECATED: Old client (kept for compatibility)
├── requirements.txt         # ✅ UPDATED: New dependencies added
├── pyproject.toml           # ✅ NEW: Modern Python packaging
├── config.py                # ✅ NEW: Configuration management
├── .gitignore               # ✅ NEW: Git ignore patterns
├── README.md                # ✅ EXISTING: User documentation
├── CLAUDE.md                # ✅ EXISTING: Development guidelines
└── docs/
    └── mcp-architecture.md  # ✅ NEW: This file
```

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Claude Code                          │
└───────────────────────────┬─────────────────────────────────┘
                            │ MCP Protocol (stdio)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  server.py (FastMCP Entry Point)                            │
│  - 24 MCP tools exposed via @mcp.tool() decorators          │
│  - Thin interface layer (protocol only)                     │
└───────────────────────────┬─────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
    ┌───────────┐   ┌───────────┐   ┌───────────┐
    │  tools/   │   │  tools/   │   │  tools/   │
    │ search.py │   │ extract.py│   │  quiz.py  │
    └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
          │               │               │
          └───────────────┼───────────────┘
                          ▼
              ┌───────────────────────┐
              │   services/           │
              │                       │
              │  ┌─────────────────┐  │
              │  │ http_client.py  │  │
              │  │ - Retry logic   │  │
              │  │ - Timeouts      │  │
              │  │ - Rate limiting │  │
              │  └────────┬────────┘  │
              │           │           │
              │  ┌────────▼────────┐  │
              │  │    cache.py     │  │
              │  │ - TTL expiration│  │
              │  │ - LRU cache     │  │
              │  │ - Statistics    │  │
              │  └────────┬────────┘  │
              │           │           │
              │  ┌────────▼────────┐  │
              │  │  base.py        │  │
              │  │ - Abstract base │  │
              │  │ - Common logic  │  │
              │  └────────┬────────┘  │
              │           │           │
              │  ┌────────▼────────┐  │
              │  │ domains/        │  │
              │  │ - wikipedia.py  │  │
              │  │ - ipn.py        │  │
              │  │ - dzieje.py     │  │
              │  │ - polona.py     │  │
              │  │ - psb.py        │  │
              │  │ - pwn.py        │  │
              │  └────────┬────────┘  │
              └───────────┼───────────┘
                          ▼
              ┌───────────────────────┐
              │  External APIs        │
              │  - Wikipedia API      │
              │  - IPN API (TODO)     │
              │  - Dzieje.pl (TODO)   │
              │  - Polona API (TODO)  │
              └───────────────────────┘
```

### Data Flow

**Search Flow:**
```
Claude Code → MCP Tool → tools/search.py → services/domains/*.py
                                → services/http_client.py → External API
                                → services/cache.py → Cache Store
                                ← Result ← HTTP Response
                        ← JSON Response
                ← Tool Result
```

**Quiz Generation Flow:**
```
Claude Code → quiz tool → tools/quiz.py → tools/search.py → Wikipedia API
                          → tools/extract.py → Extract facts
                          → Generate question
                  ← Quiz Question
```

---

## Component Documentation

### 1. Server Layer (`server.py`)

**Purpose:** FastMCP entry point exposing 24 MCP tools

**Key Responsibilities:**
- Initialize FastMCP server
- Expose tools via `@mcp.tool()` decorators
- Handle MCP protocol communication via stdio
- Route requests to appropriate tool modules

**Tools Exposed:**
- 10 search tools
- 6 extract tools
- 8 quiz tools

**Usage:**
```bash
python server.py
```

---

### 2. Tools Layer (`tools/`)

#### `tools/search.py` - Search Tools

**Purpose:** Multi-domain search across Polish history sources

**Key Functions:**
- `search_polish_history()` - Multi-domain search (Wikipedia + future domains)
- `search_wikipedia_polish()` - Polish Wikipedia search
- `search_wikipedia_english()` - English Wikipedia search
- `search_historical_figures()` - Optimized for historical people
- `search_historical_events()` - Optimized for events
- `search_historical_places()` - Find locations
- `search_primary_sources()` - Find documents/archives
- `search_biographies()` - Find biographies
- `search_timelines()` - Find timeline data
- `search_definitions()` - Find encyclopedia definitions

**Pattern:**
```python
async def search_wikipedia_polish(query: str, max_results: int = 5) -> str:
    # 1. Call domain service with caching
    results = await _wikipedia_pl._cached_search(query, max_results)
    # 2. Return as string for MCP compatibility
    return str(results)
```

#### `tools/extract.py` - Content Extraction Tools

**Purpose:** Extract structured content from articles

**Key Functions:**
- `extract_article()` - Get full article content
- `extract_facts()` - Extract dates, people, events, locations
- `extract_timeline()` - Extract timeline events
- `extract_biography()` - Extract biographical data
- `extract_locations()` - Extract geographical references
- `extract_dates()` - Extract and normalize dates

**Helper Functions:**
- `extract_figures()` - Extract historical figures using regex
- `extract_events()` - Extract events using keyword matching
- `extract_locations_from_text()` - Extract place names

#### `tools/quiz.py` - Quiz Generation Tools

**Purpose:** Generate quiz questions from historical content

**Key Functions:**
- `generate_quiz_question()` - Generate single question
- `generate_quiz_questions()` - Generate multiple questions
- `validate_quiz_answer()` - Validate user answers
- `extract_quiz_facts()` - Extract facts for quiz generation
- `generate_multiple_choice()` - Generate multiple choice
- `generate_date_question()` - Generate date-based question
- `generate_figure_question()` - Generate figure identification
- `generate_event_question()` - Generate event identification

**Question Types:**
- Multiple choice
- Date questions
- Figure identification
- Event identification

---

### 3. Services Layer (`services/`)

#### `services/http_client.py` - HTTP Client Service

**Purpose:** Centralized HTTP client with retry logic and error handling

**Key Features:**
- **Retry logic** with exponential backoff (using `tenacity`)
- **Configurable timeouts** (default: 10s)
- **Proper user-agent headers**
- **Request/response logging**
- **Connection pooling** via `httpx`
- **Async operations**

**Class:**
```python
class HTTPClient:
    async def get(self, url: str, params: dict) -> dict
    async def post(self, url: str, data: dict) -> dict
    async def close()
```

**Usage:**
```python
client = HTTPClient(timeout=10)
data = await client.get("https://api.example.com", params={"q": "query"})
await client.close()
```

#### `services/cache.py` - Cache Service

**Purpose:** In-memory caching with TTL expiration to improve performance

**Key Features:**
- **TTL-based expiration** (default: 1 hour)
- **LRU cache** with configurable max size
- **Cache statistics** (hit rate, size)
- **Thread-safe operations**
- **Pattern-based invalidation**

**Class:**
```python
class CacheService:
    def get(self, key: str) -> Optional[Any]
    def set(self, key: str, value: Any, ttl: int = 3600)
    def get_or_set(self, key: str, factory) -> Any
    def invalidate(self, pattern: str) -> int
    def get_stats() -> dict
```

**Usage:**
```python
cache = CacheService(max_size=1000, default_ttl=3600)
cache.set("key", "value")
value = cache.get("key")
stats = cache.get_stats()  # {'hits': 10, 'misses': 2, 'hit_rate': 83.33}
```

#### `services/base.py` - Base Service Class

**Purpose:** Abstract base class defining interface for all domain services

**Key Features:**
- Standard `search()` method signature
- Standard `extract_content()` method signature
- Integrated HTTP client
- Integrated cache service
- Cached search/extract helpers

**Abstract Methods:**
```python
class BaseDomainService(ABC):
    @abstractmethod
    async def search(self, query: str, limit: int = 10) -> List[Dict]

    @abstractmethod
    async def extract_content(self, url: str) -> Dict
```

**Concrete Methods:**
```python
async def _cached_search(self, query: str, limit: int) -> List[Dict]
async def _cached_extract(self, url: str) -> Dict
```

#### `services/domains/wikipedia.py` - Wikipedia Service

**Purpose:** Wikipedia domain service (refactored from `wikipedia_client.py`)

**Key Features:**
- Inherits from `BaseDomainService`
- Supports multiple language editions
- Uses MediaWiki API
- Integrated caching
- Clean search results with metadata

**Class:**
```python
class WikipediaService(BaseDomainService):
    async def search(self, query: str, limit: int = 10) -> List[Dict]
    async def extract_content(self, url: str) -> Dict
```

**Result Format:**
```python
{
    'title': 'Bolesław III Krzywousty',
    'snippet': 'Bolesław III Krzywousty...',
    'url': 'https://pl.wikipedia.org/wiki/Boles%C5%82aw_III_Krzzywousty',
    'source': 'wikipedia_pl',
    'relevance_score': 0.5,
    'metadata': {
        'wordcount': 2500,
        'timestamp': '2026-03-30T12:00:00Z',
        'language': 'pl'
    }
}
```

---

### 4. Models Layer (`models/`)

**Purpose:** Data models for type safety and clear interfaces

#### `models/search.py`
```python
@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str
    source: str
    relevance_score: float
    metadata: Dict[str, Any]

@dataclass
class QueryParams:
    query: str
    limit: int = 10
    domains: List[str] = field(default_factory=list)
```

#### `models/quiz.py`
```python
class QuestionType(Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    DATE = "date"
    FIGURE_IDENTIFICATION = "figure_identification"

class DifficultyLevel(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

@dataclass
class QuizQuestion:
    question: str
    options: List[str]
    correct_answer: str
    difficulty: DifficultyLevel
    topic: str
    source_url: str
    question_type: QuestionType
```

#### `models/facts.py`
```python
@dataclass
class HistoricalFact:
    fact: str
    category: str
    source_url: str
    date: Optional[str] = None
    location: Optional[str] = None
    figures: List[str] = field(default_factory=list)

@dataclass
class TimelineEvent:
    title: str
    date: str
    description: str
    source_url: str
    significance: int = 5
```

---

### 5. Utilities Layer (`utils/`)

#### `utils/text.py` - Text Processing

**Functions:**
- `clean_html()` - Remove HTML tags
- `normalize_whitespace()` - Normalize whitespace
- `extract_snippet()` - Extract text snippet
- `extract_keywords()` - Extract keywords
- `sanitize_input()` - Sanitize user input
- `remove_polish_diacritics()` - Remove Polish diacritics
- `extract_sentences()` - Extract sentences

#### `utils/dates.py` - Date Parsing

**Functions:**
- `parse_polish_date()` - Parse Polish date to ISO format
- `extract_dates()` - Extract all dates from text
- `parse_date_range()` - Parse date range string
- `roman_to_int()` - Convert Roman numerals
- `validate_date()` - Validate date string
- `calculate_century()` - Calculate century from year
- `get_century_name()` - Get Polish century name (e.g., "XX wiek")

#### `utils/validators.py` - Input Validation

**Functions:**
- `validate_url()` - Validate URL format
- `is_trusted_domain()` - Check if URL from trusted domain
- `sanitize_search_query()` - Sanitize search query
- `validate_search_query()` - Validate search query
- `validate_limit()` - Validate limit parameter
- `get_allowed_domains()` - Get list of trusted domains

**Trusted Domains:**
```python
TRUSTED_DOMAINS = [
    'pl.wikipedia.org',
    'en.wikipedia.org',
    'ipn.gov.pl',
    'dzieje.pl',
    'polona.pl',
    'encyklopedia.pwn.pl',
    'gov.pl',
    'edu.pl'
]
```

---

## Tool Reference

### Search Tools

#### `search_polish_history`

Search across multiple Polish history sources.

**Parameters:**
- `query` (str, required): Search query
- `domains` (list, optional): List of domains to search (empty = all)
- `limit` (int, optional): Max results per domain (default: 10)

**Returns:** JSON string with search results

**Example:**
```python
await search_polish_history("Bitwa pod Grunwaldem", limit=5)
```

#### `search_wikipedia_polish`

Search Polish Wikipedia.

**Parameters:**
- `query` (str, required): Search query
- `max_results` (int, optional): Max results (1-20, default: 5)

**Returns:** JSON string with search results

**Example:**
```python
await search_wikipedia_polish("Bolesław III Krzywousty", max_results=10)
```

#### `search_historical_figures`

Search for historical figures.

**Parameters:**
- `query` (str, required): Figure name or description
- `period` (str, optional): Time period (e.g., "XVII wiek")

**Returns:** JSON with biographical information

**Example:**
```python
await search_historical_figures("Jan III Sobieski", period="XVII wiek")
```

### Extract Tools

#### `extract_article`

Extract full article content.

**Parameters:**
- `url` (str, required): Article URL

**Returns:** JSON with title, content, URL, metadata

**Example:**
```python
await extract_article("https://pl.wikipedia.org/wiki/Boles%C5%82aw_III_Krzzywousty")
```

#### `extract_facts`

Extract structured facts from article.

**Parameters:**
- `url` (str, required): Article URL

**Returns:** JSON with dates, figures, events, locations

**Example:**
```python
await extract_facts("https://pl.wikipedia.org/wiki/Bitwa_pod_Grunwaldem")
```

### Quiz Tools

#### `generate_quiz_question`

Generate a single quiz question.

**Parameters:**
- `topic` (str, required): Historical topic
- `difficulty` (str, optional): easy/medium/hard/expert (default: medium)
- `question_type` (str, optional): multiple_choice/date/figure_identification/event_identification

**Returns:** JSON with quiz question

**Example:**
```python
await generate_quiz_question("Bitwa pod Grunwaldem", difficulty="medium", question_type="multiple_choice")
```

#### `generate_quiz_questions`

Generate multiple quiz questions.

**Parameters:**
- `topic` (str, required): Historical topic
- `count` (int, optional): Number of questions (default: 5)
- `difficulty` (str, optional): Difficulty level (default: medium)

**Returns:** JSON with list of quiz questions

**Example:**
```python
await generate_quiz_questions("Powstanie styczniowe", count=10, difficulty="hard")
```

---

## API Documentation

### Service Layer API

#### WikipediaService

```python
from services.domains.wikipedia import WikipediaService
from services.http_client import HTTPClient
from services.cache import get_cache

# Initialize
client = HTTPClient()
cache = get_cache()
wiki = WikipediaService(language='pl', http_client=client, cache_service=cache)

# Search
results = await wiki.search("Bolesław III", limit=10)

# Extract content
content = await wiki.extract_content("https://pl.wikipedia.org/wiki/Bolesław_III")

# Cleanup
await client.close()
```

#### HTTPClient

```python
from services.http_client import HTTPClient

async with HTTPClient(timeout=10) as client:
    data = await client.get("https://api.example.com", params={"q": "query"})
    # Auto-closed on exit
```

#### CacheService

```python
from services.cache import get_cache

cache = get_cache()

# Set/get
cache.set("key", {"data": "value"}, ttl=3600)
value = cache.get("key")

# Get or set with factory
value = cache.get_or_set("key", lambda: expensive_computation())

# Statistics
stats = cache.get_stats()
print(f"Hit rate: {stats['hit_rate']}%")

# Invalidate pattern
cache.invalidate("wikipedia:*")
```

---

## Setup & Configuration

### Installation

1. **Clone repository:**
```bash
git clone <repository-url>
cd mcp-server
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

Or using `uv` (recommended):
```bash
uv pip install -r requirements.txt
```

4. **Verify installation:**
```bash
python -c "from services.domains.wikipedia import WikipediaService; print('OK')"
```

### Claude Code Integration

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "polish-history": {
      "command": "/home/macryba/mcp-server/venv/bin/python",
      "args": ["/home/macryba/mcp-server/server.py"],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

Or using `uv`:
```json
{
  "mcpServers": {
    "polish-history": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/home/macryba/mcp-server",
        "python",
        "server.py"
      ]
    }
  }
}
```

### Configuration

Edit `config.py` to customize:

```python
class Config:
    # HTTP settings
    HTTP_TIMEOUT = 10
    HTTP_MAX_RETRIES = 3

    # Cache settings
    CACHE_TTL = 3600  # 1 hour
    CACHE_MAX_SIZE = 1000

    # Search settings
    DEFAULT_SEARCH_LIMIT = 10
    MAX_SEARCH_LIMIT = 100

    # Trusted domains
    TRUSTED_DOMAINS = [...]
```

Or use environment variables:

```bash
export HTTP_TIMEOUT=15
export CACHE_TTL=7200
export LOG_LEVEL=DEBUG
```

---

## Usage Examples

### Example 1: Search and Extract

```python
# In Claude Code:
"Search for information about the Battle of Grunwald and extract key facts"

# This would:
# 1. Call search_historical_events("Bitwa pod Grunwaldem")
# 2. Get results from Wikipedia
# 3. Call extract_facts() on the top result
# 4. Return structured facts (dates, figures, events, locations)
```

### Example 2: Generate Quiz

```python
# In Claude Code:
"Generate 5 medium-difficulty quiz questions about the January Uprising"

# This would:
# 1. Search for "Powstanie styczniowe"
# 2. Extract facts from multiple sources
# 3. Generate 5 different question types
# 4. Return quiz with questions, options, and answers
```

### Example 3: Multi-Domain Search

```python
# In Claude Code:
"Find information about Marie Curie across Polish and English sources"

# This would:
# 1. Search Polish Wikipedia: "Maria Skłodowska-Curie"
# 2. Search English Wikipedia: "Marie Curie"
# 3. Combine results
# 4. Deduplicate and rank by relevance
```

### Example 4: Biography Extraction

```python
# In Claude Code:
"Extract biographical information about Józef Piłsudski"

# This would:
# 1. Search for the figure
# 2. Extract biography from article
# 3. Return structured bio: birth/death dates, occupation, achievements
```

---

## Development Guide

### Adding a New Domain Service

1. **Create service file:**
```python
# services/domains/ipn.py
from services.base import BaseDomainService

class IPNService(BaseDomainService):
    async def search(self, query: str, limit: int = 10) -> List[Dict]:
        # Implement IPN search
        pass

    async def extract_content(self, url: str) -> Dict:
        # Implement IPN content extraction
        pass
```

2. **Add to tools/search.py:**
```python
_ipn = IPNService(http_client=_http_client, cache_service=_cache)

async def search_ipn(query: str, limit: int = 10) -> str:
    results = await _ipn._cached_search(query, limit)
    return str(results)
```

3. **Add tool to server.py:**
```python
@mcp.tool()
async def search_ipn(query: str, limit: int = 10) -> str:
    """Search IPN (Institute of National Remembrance)"""
    return await tools.search.search_ipn(query, limit)
```

4. **Add tests:**
```python
# tests/test_services/test_domains/test_ipn.py
import pytest

@pytest.mark.asyncio
async def test_ipn_search():
    # Test implementation
    pass
```

### Adding a New Tool

1. **Add function to tools/ module:**
```python
# tools/quiz.py
async def generate_true_false(topic: str) -> str:
    """Generate true/false question"""
    # Implementation
    pass
```

2. **Expose in server.py:**
```python
@mcp.tool()
async def generate_true_false_question(topic: str) -> str:
    """Generate a true/false question"""
    return await quiz.generate_true_false(topic)
```

3. **Add tests:**
```python
# tests/test_quiz.py
@pytest.mark.asyncio
async def test_generate_true_false():
    result = await quiz.generate_true_false("Bitwa pod Grunwaldem")
    assert 'question' in result
```

### Code Style

- **Type hints** required for all functions
- **Docstrings** required for all public functions
- **Async/await** for all I/O operations
- **Error handling** with try/except blocks
- **Logging** with appropriate log levels

---

## Testing Strategy

### Test Structure

```
tests/
├── unit/              # Unit tests for individual modules
│   ├── test_services/
│   ├── test_tools/
│   ├── test_models/
│   └── test_utils/
├── integration/       # Integration tests for workflows
│   ├── test_multi_domain_search.py
│   ├── test_quiz_generation.py
│   └── test_end_to_end.py
└── conftest.py       # Pytest fixtures
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=services --cov=tools --cov=models --cov=utils

# Run specific test file
pytest tests/test_services/test_http_client.py

# Run with verbose output
pytest -v

# Run async tests
pytest -v --asyncio-mode=auto
```

### Test Coverage Goals

- **Overall:** 90%+ coverage
- **Critical paths:** 100% coverage
- **Services:** 95%+ coverage
- **Tools:** 90%+ coverage

### Writing Tests

```python
import pytest
from services.http_client import HTTPClient

@pytest.mark.asyncio
async def test_http_client_get():
    client = HTTPClient(timeout=5)
    # Test implementation
    await client.close()

@pytest.fixture
async def http_client():
    client = HTTPClient()
    yield client
    await client.close()
```

---

## Migration Guide

### From Old Server (`wikipedia_mcp_server.py`) to New Server (`server.py`)

#### What Changed

**Old Structure:**
- 2 files: `wikipedia_mcp_server.py`, `wikipedia_client.py`
- 5 tools, Wikipedia-only
- No caching, no retry logic
- Monolithic structure

**New Structure:**
- 20+ files organized in modules
- 24 tools, multi-domain
- Robust infrastructure (HTTP client, cache, base service)
- Quiz generation capabilities

#### Tool Mapping

| Old Tool | New Tool | Notes |
|----------|----------|-------|
| `search_wikipedia` | `search_wikipedia_polish` | Same functionality |
| `search_wikipedia_english` | `search_wikipedia_english` | Same functionality |
| `get_wikipedia_page` | `extract_article` | Enhanced with more metadata |
| `search_polish_historical_figures` | `search_historical_figures` | Same functionality, better results |
| `search_polish_historical_events` | `search_historical_events` | Same functionality, better results |

| **New Tools** | |
|---------------|---|
| `search_polish_history` | Multi-domain search |
| `extract_facts` | Extract structured facts |
| `extract_timeline` | Extract timeline events |
| `generate_quiz_question` | Generate quiz questions |
| `generate_quiz_questions` | Generate multiple questions |
| `validate_quiz_answer` | Validate quiz answers |

#### Migration Steps

1. **Update Claude Code config:**
```json
{
  "mcpServers": {
    "polish-history": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/server.py"]  # Changed from wikipedia_mcp_server.py
    }
  }
}
```

2. **Update tool calls:**
```python
# OLD
search_wikipedia("Bolesław III", max_results=5)

# NEW (same interface)
search_wikipedia_polish("Bolesław III", max_results=5)
```

3. **Take advantage of new features:**
```python
# Multi-domain search
search_polish_history("Powstanie styczniowe", domains=["wikipedia_pl", "ipn"])

# Quiz generation
generate_quiz_questions("Bitwa pod Grunwaldem", count=10, difficulty="medium")

# Fact extraction
extract_facts("https://pl.wikipedia.org/wiki/Boles%C5%82aw_III")
```

#### Backward Compatibility

**The old server (`wikipedia_mcp_server.py`) is still functional** but deprecated:

- Still works with existing code
- Shows deprecation warning
- Will be removed in future major version (3.0.0)

Recommended timeline:
- **Now:** Start using new `server.py`
- **3 months:** Old tools marked as deprecated
- **6 months:** Remove old files in major version bump

---

## Performance Considerations

### Caching Strategy

- **Search results** cached for 1 hour (TTL)
- **Extracted content** cached for 1 hour (TTL)
- **Expected cache hit rate:** >70%
- **Performance improvement:** 3-5x faster for cached queries

### HTTP Best Practices

- **Connection pooling** via `httpx` (max 10 connections)
- **Retry logic** with exponential backoff (max 3 attempts)
- **Timeouts** configured (default: 10s)
- **Rate limiting** respects server limits

### Optimization Tips

1. **Use multi-domain search carefully** - makes parallel requests
2. **Enable caching** - already enabled by default
3. **Adjust timeouts** for slow domains in `config.py`
4. **Monitor cache stats** - call `server_info()` to see hit rate

---

## Troubleshooting

### Common Issues

#### 1. MCP Tools Not Available in Claude Code

**Problem:** Tools not showing up in Claude Code

**Solutions:**
- Check `~/.claude/settings.json` configuration
- Verify virtual environment is created: `ls venv/`
- Verify dependencies installed: `pip list | grep fastmcp`
- Check server starts without errors: `python server.py`
- Restart Claude Code after config changes

#### 2. Import Errors

**Problem:** `ModuleNotFoundError: No module named 'services'`

**Solutions:**
- Ensure you're in project directory: `cd /home/macryba/mcp-server`
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

#### 3. Cache Issues

**Problem:** Stale cache results

**Solutions:**
- Clear cache: `python -c "from services.cache import get_cache; get_cache().clear()"`
- Reduce TTL in `config.py`
- Invalidate pattern: `cache.invalidate("wikipedia:*")`

#### 4. HTTP Errors

**Problem:** Connection timeout or HTTP errors

**Solutions:**
- Check network connectivity: `curl https://pl.wikipedia.org`
- Increase timeout in `config.py`: `HTTP_TIMEOUT = 20`
- Check if Wikipedia API is accessible
- Verify user-agent headers are set correctly

---

## Future Enhancements

### Planned Features

1. **Additional Domain Services:**
   - IPN (Institute of National Remembrance)
   - Dzieje.pl history portal
   - Polona digital library
   - PSB (Polish Biographical Dictionary)
   - PWN Encyclopedia

2. **Advanced Quiz Features:**
   - Adaptive difficulty
   - Question banks
   - Score tracking
   - Multiple languages

3. **Performance Improvements:**
   - Redis caching (instead of in-memory)
   - Parallel search across domains
   - Response streaming
   - Compression

4. **Developer Features:**
   - OpenAPI/Swagger documentation
   - Admin dashboard
   - Rate limiting per user
   - Usage analytics

---

## Contributing

### Development Workflow

1. **Create feature branch:** `git checkout -b feature/new-domain`
2. **Make changes** following code style guidelines
3. **Add tests** for new functionality
4. **Run tests:** `pytest --cov`
5. **Update documentation** if needed
6. **Submit pull request**

### Code Review Checklist

- [ ] Type hints included
- [ ] Docstrings included
- [ ] Error handling implemented
- [ ] Tests added (90%+ coverage)
- [ ] Documentation updated
- [ ] No breaking changes (or migration guide provided)

---

## License

MIT License - See LICENSE file for details

---

## Support

For issues, questions, or contributions:
- **Issues:** GitHub Issues
- **Documentation:** `docs/mcp-architecture.md`
- **Examples:** `README.md`

---

**Document Version:** 2.0.0
**Last Updated:** 2026-03-30
**Maintainer:** macryba

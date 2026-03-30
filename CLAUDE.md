# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Expected AI agent behaviour

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make them pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.


## Project Overview

This is a **multi-domain Polish history MCP (Model Context Protocol) server** optimized for building history quiz applications and research tools. It provides reliable, CAPTCHA-free search and content extraction across 6 Polish history sources, plus automated quiz generation capabilities.

**Key features:**
- **Multi-domain search:** Wikipedia, IPN, Dzieje, Polona, PSB, PWN
- **Quiz generation:** Automatically generate questions from historical content
- **Content extraction:** Extract articles, facts, timelines, and biographies
- **Robust infrastructure:** HTTP client with retry logic, caching, error handling
- **Type safety:** Comprehensive data models with type hints

**Key advantage:** Avoids bot detection issues common with metasearch engines by using official APIs directly.

## Architecture

```
Claude Code → MCP Server (FastMCP) → Multi-Domain Services (Wikipedia + 5 future domains)
                                       ↓
                                  Content Extraction & Quiz Generation
```

The MCP server (`server.py`) exposes **24 specialized tools**:

**Search Tools (10):**
- `search_polish_history` - Multi-domain search across all sources
- `search_wikipedia_polish` - Polish Wikipedia search
- `search_wikipedia_english` - English Wikipedia search
- `search_historical_figures` - Optimized for historical people
- `search_historical_events` - Optimized for events
- `search_historical_places` - Find locations
- `search_primary_sources` - Find documents/archives
- `search_biographies` - Find biographies
- `search_timelines` - Find timeline data
- `search_definitions` - Find encyclopedia definitions

**Extract Tools (6):**
- `extract_article` - Get full article content
- `extract_facts` - Extract dates, people, events, locations
- `extract_timeline` - Extract timeline events
- `extract_biography` - Extract biographical data
- `extract_locations` - Extract geographical references
- `extract_dates` - Extract and normalize dates

**Quiz Tools (8):**
- `generate_quiz_question` - Generate single question
- `generate_quiz_questions` - Generate multiple questions
- `validate_quiz_answer` - Validate user answers
- `extract_quiz_facts` - Extract facts for quiz generation
- `generate_multiple_choice` - Generate multiple choice
- `generate_date_question` - Generate date-based question
- `generate_figure_question` - Generate figure identification
- `generate_event_question` - Generate event identification

## Common Commands

```bash
# Setup (first time only)
bash setup.sh

# Start the MCP server
source venv/bin/activate
python server.py

# Run tests
pytest

# Run tests with coverage
pytest --cov=services --cov=tools --cov=models --cov=utils
```

## Configuration

### Server Settings

Edit `config.py` to configure:
- `HTTP_TIMEOUT`: Request timeout in seconds (default: `10`)
- `HTTP_MAX_RETRIES`: Maximum retry attempts (default: `3`)
- `CACHE_TTL`: Cache time-to-live in seconds (default: `3600`)
- `CACHE_MAX_SIZE`: Maximum cache size (default: `1000`)
- `DEFAULT_SEARCH_LIMIT`: Default search results limit (default: `10`)

### Claude Code Integration

Configure the MCP server in `~/.claude/settings.json`:

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

After modifying this file, restart Claude Code for changes to take effect.

## Polish History Optimization

The server is optimized for Polish historical sources:

**Search patterns for best results:**
- Use Polish names: `Bolesław III Krzywousty` not `Boleslaus the Wry-mouthed`
- Include years: `Bitwa pod Grunwaldem 1410`
- Use Polish diacritics: `Powstanie styczniowe`
- Historical figures: Search with birth/death years for disambiguation

**Language settings:**
- Default language edition: `pl` (Polish Wikipedia)
- Primary source: `pl.wikipedia.org`
- Fallback: English Wikipedia if Polish article not available

**Trusted domains:**
- `pl.wikipedia.org`, `en.wikipedia.org`
- `ipn.gov.pl`, `dzieje.pl`, `polona.pl`
- `psb.org.pl`, `encyklopedia.pwn.pl`
- `gov.pl`, `edu.pl`

## Troubleshooting

**MCP tools not available in Claude Code:**
```bash
# Check if virtual environment exists
ls -la venv/

# Verify dependencies installed
source venv/bin/activate
pip list | grep -E 'fastmcp|httpx|tenacity'

# Test MCP server directly
python server.py
```

**Import errors:**
```bash
# Ensure you're in project directory
cd /home/macryba/mcp-server

# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Wikipedia API errors:**
- Verify network connectivity: `curl https://pl.wikipedia.org/w/api.php`
- Check API rate limits (default: ~200 requests/second)
- Ensure valid Wikipedia page titles (case-sensitive for first letter)

**Cache issues:**
```bash
# Clear cache
python -c "from services.cache import get_cache; get_cache().clear()"

# Check cache stats
python -c "from services.cache import get_cache; print(get_cache().get_stats())"
```

**Permission errors:**
```bash
# Make setup script executable
chmod +x setup.sh

# Make server script executable
chmod +x server.py
```

## Project Structure

```
mcp-server/
├── server.py                   # Main MCP entry point (FastMCP)
├── tools/                      # MCP tool implementations
│   ├── search.py              # 10+ search tools
│   ├── extract.py             # 6 content extraction tools
│   └── quiz.py                # 8 quiz generation tools
├── services/                   # Business logic layer
│   ├── http_client.py         # HTTP client with retry logic
│   ├── cache.py               # Caching service with TTL
│   ├── base.py                # Base service class
│   └── domains/               # Domain-specific services
│       └── wikipedia.py       # Wikipedia service
├── models/                     # Data models for type safety
│   ├── search.py              # SearchResult, QueryParams
│   ├── quiz.py                # QuizQuestion, QuizAnswer
│   └── facts.py               # HistoricalFact, TimelineEvent
├── utils/                      # Utility functions
│   ├── text.py                # Text processing
│   ├── dates.py               # Date parsing (Polish dates)
│   └── validators.py          # Input validation
├── tests/                      # Comprehensive test suite
│   └── test_services/         # Service layer tests
│       ├── test_http_client.py
│       └── test_cache.py
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Modern Python packaging
├── setup.sh                   # Automated setup script
├── CLAUDE.md                  # This file
├── README.md                  # User documentation
└── docs/
    └── mcp-architecture.md    # Detailed architecture documentation
```

## Installation

The `setup.sh` script automates setup:
1. Creates Python virtual environment (`venv/`)
2. Installs dependencies (fastmcp, httpx, tenacity, beautifulsoup4)
3. Verifies installation

Run: `bash setup.sh`

Or using `uv` (recommended):
```bash
uv pip install -r requirements.txt
```

## Development

**Adding new tools:**
1. Add function to appropriate module in `tools/` (search.py, extract.py, or quiz.py)
2. Expose in `server.py` using `@mcp.tool()` decorator
3. Add tests in `tests/`
4. Restart Claude Code to load new tools

**Adding new domain services:**
1. Create service in `services/domains/` inheriting from `BaseDomainService`
2. Implement `search()` and `extract_content()` methods
3. Add tool in `tools/search.py`
4. Add tests in `tests/test_services/`

**Code style requirements:**
- Type hints required for all functions
- Docstrings required for all public functions
- Async/await for all I/O operations
- Error handling with try/except blocks
- Logging with appropriate log levels

**Testing:**
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

## Architecture Philosophy

This server follows the **recommended MCP server pattern**:

- **MCP is a thin interface layer** - Tools are simple wrappers around business logic
- **Business logic in modules** - All heavy lifting in services/ and tools/
- **Reusable outside MCP** - Python functions can be used independently
- **Clean separation of concerns** - Services handle HTTP, tools handle MCP protocol

For detailed architecture documentation, see `docs/mcp-architecture.md`.

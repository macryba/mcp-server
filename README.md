# Polish History MCP Server

A **multi-domain** MCP (Model Context Protocol) server for Polish history research. Provides reliable, CAPTCHA-free search across 7 Polish history sources with comprehensive content extraction capabilities.

## 📚 Documentation

**Complete Documentation:**
- [Architecture Documentation](docs/mcp-architecture.md) - Complete system architecture and API reference
- [Tool Reference](docs/mcp-architecture.md#tool-reference) - All 5 available MCP tools
- [API Documentation](docs/mcp-architecture.md#api-documentation) - Service layer API
- [Development Guide](docs/mcp-architecture.md#development-guide) - Adding new tools and domains

## 🎯 Purpose

This server provides comprehensive access to Polish historical information through multiple trusted sources:
- **Wikipedia** (Polish edition) - ✅ implemented
- **IPN** (Institute of National Remembrance) - ✅ implemented
- **Dzieje.pl** - Polish history portal - ✅ implemented
- **Polona** - Digital library - ✅ implemented
- **SuperKid** - Educational portal - ✅ implemented
- **Przystanek Historia** - 20th century history - ✅ implemented
- **GWO** - Teaching materials - ✅ implemented

**Key capabilities:**
- Multi-domain search across Polish history sources
- Article content extraction from Wikipedia
- Robust infrastructure (retry logic, caching, error handling)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Run the setup script
chmod +x setup.sh
./setup.sh
```

Or manually:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Or using `uv` (recommended):

```bash
uv pip install -r requirements.txt
```

### 2. Start the MCP Server

```bash
# Activate virtual environment
source venv/bin/activate

# Start server
python server.py
```

### 3. Configure Claude Code

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

Restart Claude Code to load the MCP server.

## 🛠️ Available Tools

The server exposes **5 specialized tools** organized into 3 categories:

### Search Tools (3)

1. **`search_polish_history`** - Multi-domain search across all 7 implemented sources
2. **`search_wikipedia`** - Polish Wikipedia search
3. **`list_domains`** - List available historical source domains with capabilities

### Extract Tools (1)

1. **`extract_article`** - Get full article content from Wikipedia

### Server Info (2)

1. **`server_info`** - Get server information, capabilities, and recommended workflow
2. **`usage_guide`** - Get detailed usage guide and workflow recommendations

## 📚 Example Usage in Claude Code

### Quick Wikipedia Search

```
Use search_wikipedia to find basic information about "Bolesław III Krzywousty"
```

### Multi-Domain Historical Research

```
Use search_polish_history to find comprehensive information about "Bitwa pod Grunwaldem" across all 7 sources
```

### Discover Available Sources

```
Use list_domains to see which historical sources are available and their specializations
```

### Extract Article Content

```
Use extract_article to get full content from https://pl.wikipedia.org/wiki/Bitwa_pod_Grunwaldem
```

### Get Usage Guidance

```
Use usage_guide to learn the recommended 3-step research workflow
```

## 🎓 Optimized for Polish History

### Recommended Search Patterns

**Historical Figures:**
- Use Polish names: `Bolesław III Krzywousty` not `Boleslaus the Wry-mouthed`
- Include years: `Jan III Sobieski (1629-1696)`
- Use Polish diacritics: `Józef Piłsudski` not `Jozef Pilsudski`

**Historical Events:**
- `Bitwa pod {place}` - Battles (e.g., `Bitwa pod Grunwaldem`)
- `Powstanie {name}` - Uprisings (e.g., `Powstanie styczniowe`)
- Include years: `Powstanie styczniowe 1863`

**Time Periods:**
- `Polska {period}` - Historical periods
- `Historia Polski {century}` - Centuries (e.g., `XVII wiek`)

## 🔧 Configuration

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
```

Or use environment variables:

```bash
export HTTP_TIMEOUT=15
export CACHE_TTL=7200
export LOG_LEVEL=DEBUG
```

## 🔧 Troubleshooting

### MCP Server Not Starting

```bash
# Check if FastMCP is installed
pip list | grep fastmcp

# Reinstall if needed
pip install --upgrade fastmcp
```

### Tools Not Available in Claude Code

1. Check `~/.claude/settings.json` syntax
2. Verify the path to python and script are correct
3. Restart Claude Code completely

### Import Errors

```bash
# Ensure you're in project directory
cd /home/macryba/mcp-server

# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Cache Issues

```bash
# Clear cache
python -c "from services.cache import get_cache; get_cache().clear()"

# Check cache stats
python -c "from services.cache import get_cache; print(get_cache().get_stats())"
```

### Wikipedia API Errors

- Verify network connectivity: `curl https://pl.wikipedia.org/w/api.php`
- Check API rate limits (default: ~200 requests/second)
- Ensure valid Wikipedia page titles (case-sensitive for first letter)

## 📁 Project Structure

```
mcp-server/
├── server.py                   # Main MCP entry point (FastMCP)
├── tools/                      # MCP tool implementations
│   ├── search.py              # 10+ search tools
│   └── extract.py             # 6 content extraction tools
├── services/                   # Business logic layer
│   ├── http_client.py         # HTTP client with retry logic
│   ├── cache.py               # Caching service with TTL
│   ├── base.py                # Base service class
│   └── domains/               # Domain-specific services
│       └── wikipedia.py       # Wikipedia service
├── models/                     # Data models for type safety
│   ├── search.py              # SearchResult, QueryParams
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
├── CLAUDE.md                  # Development guidelines
├── README.md                  # This file
└── docs/
    └── mcp-architecture.md    # Detailed architecture documentation
```

## 🧪 Testing

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

## 🎯 Why This Approach?

### Advantages over Metasearch Engines

1. **No CAPTCHA issues** - Direct API access
2. **Faster** - No intermediate metasearch layer
3. **More reliable** - No bot detection problems
4. **Higher quality** - Trusted primary sources
5. **Lighter** - Minimal resource usage
6. **Language-optimized** - Better Polish language support
7. **Multi-domain** - Search across 7 Polish history sources

### Use Cases

- ✅ Historical research
- ✅ Educational content
- ✅ Fact checking
- ✅ Timeline creation
- ✅ Biographical information
- ✅ Multi-source research
- ✅ Content extraction

## 🚀 Architecture Highlights

- **Modular design** - Clean separation between MCP layer, tools, and services
- **Type safety** - Comprehensive data models with type hints
- **Robust infrastructure** - HTTP client with retry logic, caching, error handling
- **Well-tested** - 90%+ test coverage target
- **Extensible** - Easy to add new domains and tools
- **Reusable** - Business logic can be used independently of MCP

## 🚀 Future Enhancements

Planned additions:

1. **Additional domain services:**
   - IPN (Institute of National Remembrance)
   - Dzieje.pl history portal
   - Polona digital library
   - PSB (Polish Biographical Dictionary)
   - PWN Encyclopedia

2. **Performance improvements:**
   - Redis caching (instead of in-memory)
   - Parallel search across domains
   - Response streaming

3. **Developer features:**
   - OpenAPI/Swagger documentation
   - Admin dashboard
   - Rate limiting per user
   - Usage analytics

## 📝 Notes

- This server is designed for LAN/home use
- Wikipedia API has rate limits (respect these)
- All search queries go directly to trusted sources (no intermediaries)
- Optimized for Polish history but works for any topic
- Cache enabled by default (1-hour TTL)

## 🙏 Acknowledgments

Built with:
- [FastMCP](https://github.com/jlowin/fastmcp) - MCP server framework
- [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page) - Data source
- [httpx](https://www.python-httpx.org/) - Async HTTP client
- [tenacity](https://github.com/jd/tenacity) - Retry logic
- Polish Wikipedia community - Content creators

---

**For Polish history research, this provides a solid, reliable foundation with multi-domain support and robust infrastructure.**

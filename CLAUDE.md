# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Wikipedia-focused MCP (Model Context Protocol) server optimized for Polish historical sources. It provides reliable, CAPTCHA-free search and content extraction capabilities to Claude Code using the Wikipedia API directly.

**Key advantage:** Avoids bot detection issues common with metasearch engines by using Wikipedia's official API.

## Architecture

```
Claude Code → MCP Server (FastMCP) → Wikipedia API (pl.wikipedia.org)
```

The MCP server exposes 5 specialized tools:
- `wikipedia_search_polish`: Search Polish Wikipedia for historical content
- `wikipedia_get_page`: Extract full page content by title
- `wikipedia_search_historical_figure`: Specialized search for historical people
- `wikipedia_search_historical_event`: Specialized search for historical events
- `wikipedia_search_general`: General Wikipedia search (all language editions)

## Common Commands

```bash
# Setup (first time only)
bash setup.sh

# Start the MCP server
source venv/bin/activate
python wikipedia_mcp_server.py

# Test Wikipedia client directly
python wikipedia_client.py

# View Wikipedia client usage
python wikipedia_client.py --help
```

## Configuration

### Wikipedia Client Settings

Edit `wikipedia_client.py` to configure:
- `USER_AGENT`: Browser user agent string
- `DEFAULT_LANGUAGE`: Default Wikipedia language edition (default: `pl`)
- `API_TIMEOUT`: Request timeout in seconds (default: `10`)
- `MAX_RESULTS`: Maximum search results (default: `10`)

### Claude Code Integration

Configure the MCP server in `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "wikipedia-polish": {
      "command": "/home/macryba/mcp-server/venv/bin/python",
      "args": ["/home/macryba/mcp-server/wikipedia_mcp_server.py"],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

After modifying this file, restart Claude Code for changes to take effect.

## Polish History Optimization

The Wikipedia client is optimized for Polish historical sources:

**Search patterns for best results:**
- Use Polish names: `Bolesław III Krzywousty` not `Boleslaus the Wry-mouthed`
- Include years: `Bitwa pod Grunwaldem 1410`
- Use Polish diacritics: `Powstanie styczniowe` not `Powstanie styczniowe`
- Historical figures: Search with birth/death years for disambiguation

**Language settings:**
- Default language edition: `pl` (Polish Wikipedia)
- Primary source: `pl.wikipedia.org`
- Fallback: English Wikipedia if Polish article not available

## Troubleshooting

**MCP tools not available in Claude Code:**
```bash
# Check if virtual environment exists
ls -la venv/

# Verify dependencies installed
source venv/bin/activate
pip list | grep -E 'fastmcp|requests|beautifulsoup4'

# Test MCP server directly
python wikipedia_mcp_server.py
```

**Wikipedia API errors:**
- Verify network connectivity: `curl https://pl.wikipedia.org/w/api.php`
- Check API rate limits (default: ~200 requests/second)
- Ensure valid Wikipedia page titles (case-sensitive for first letter)

**Permission errors:**
```bash
# Make setup script executable
chmod +x setup.sh

# Make server script executable
chmod +x wikipedia_mcp_server.py
```

## Project Structure

```
mcp-server/
├── wikipedia_client.py          # Wikipedia API client library
├── wikipedia_mcp_server.py      # FastMCP server with 5 tools
├── requirements.txt             # Python dependencies
├── setup.sh                     # Automated setup script
├── CLAUDE.md                    # This file
└── README.md                    # User documentation
```

## Installation

The `setup.sh` script automates setup:
1. Creates Python virtual environment (`venv/`)
2. Installs dependencies (fastmcp, requests, beautifulsoup4)
3. Verifies installation

Run: `bash setup.sh`

## Development

**Adding new Wikipedia tools:**
1. Add method to `WikipediaClient` class in `wikipedia_client.py`
2. Create new tool in `wikipedia_mcp_server.py` using `@mcp.tool()` decorator
3. Restart Claude Code to load new tools

**Testing Wikipedia client:**
```bash
# Test search
python -c "from wikipedia_client import WikipediaClient; client = WikipediaClient(); print(client.search('Bolesław III Krzywousty'))"

# Test page extraction
python -c "from wikipedia_client import WikipediaClient; client = WikipediaClient(); print(client.get_page('Bitwa pod Grunwaldem'))"
```

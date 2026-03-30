# Wikipedia MCP Server for Polish History

A lightweight, FastMCP-based server for searching Wikipedia and other Polish historical sources. Optimized for Polish history research and quiz generation.

## 📚 Documentation

**🆕 New Architecture (v2.0):** The server has been refactored with a modular architecture supporting multi-domain search, content extraction, and quiz generation. See [docs/mcp-architecture.md](docs/mcp-architecture.md) for complete documentation.

**Quick Links:**
- [Architecture Documentation](docs/mcp-architecture.md) - Complete system architecture and API reference
- [Migration Guide](docs/mcp-architecture.md#migration-guide) - Upgrading from v1.x to v2.0
- [Tool Reference](docs/mcp-architecture.md#tool-reference) - All available MCP tools
- [API Documentation](docs/mcp-architecture.md#api-documentation) - Service layer API

## 🎯 Purpose

This server provides reliable, CAPTCHA-free access to Polish historical information through Wikipedia's official API, bypassing the complexity and reliability issues of metasearch engines like SearXNG.

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

### 2. Test the Wikipedia Client

```bash
# Activate virtual environment
source venv/bin/activate

# Test search
python wikipedia_client.py "Bolesław III Krzywousty" pl 3

# Test page extraction
python wikipedia_client.py "Bolesław III Krzywousty" pl
```

### 3. Start the MCP Server

**Option A: New Server (Recommended - v2.0)**

```bash
# Activate virtual environment
source venv/bin/activate

# Start new server with multi-domain search and quiz generation
python server.py
```

**Option B: Legacy Server (v1.x - Deprecated)**

```bash
# Activate virtual environment
source venv/bin/activate

# Start legacy server (Wikipedia-only)
python wikipedia_mcp_server.py
```

> **Note:** The new server (`server.py`) provides multi-domain search, content extraction, and quiz generation. The legacy server (`wikipedia_mcp_server.py`) is deprecated but still functional for backward compatibility.

### 4. Configure Claude Code

**Option A: New Server (Recommended)**

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "polish-history": {
      "command": "/home/macryba/mcp-server/venv/bin/python",
      "args": ["/home/macryba/mcp-server/server.py"]
    }
  }
}
```

**Option B: Legacy Server**

```json
{
  "mcpServers": {
    "polish-history-wikipedia": {
      "command": "/home/macryba/mcp-server/venv/bin/python",
      "args": ["/home/macryba/mcp-server/wikipedia_mcp_server.py"]
    }
  }
}
```

Restart Claude Code to load the MCP server.

## 🛠️ Available Tools

### 1. `search_wikipedia`
Search Polish Wikipedia for any topic

**Parameters:**
- `query` (string): Search query
- `max_results` (number): Results count (1-20, default: 5)

**Example:**
```
Search for "Bolesław III Krzywousty" with max_results=5
```

### 2. `search_wikipedia_english`
Search English Wikipedia for additional context

**Parameters:**
- `query` (string): Search query in English
- `max_results` (number): Results count (1-20, default: 5)

### 3. `get_wikipedia_page`
Get full page content and summary

**Parameters:**
- `title` (string): Exact page title
- `language` (string): 'pl' or 'en' (default: 'pl')

### 4. `search_polish_historical_figures`
Search specifically for Polish historical figures

**Optimized for:**
- Kings, queens, and rulers
- Political and military leaders
- Historical personalities

**Returns additional metadata:**
- Source type classification
- Suggested domains for further research

### 5. `search_polish_historical_events`
Search for Polish historical events

**Optimized for:**
- Battles and wars
- Uprisings and revolutions
- Treaties and political events
- Cultural and scientific milestones

## 📚 Example Usage in Claude Code

### Research Historical Figures

```
Use search_polish_historical_figures to find information about "Bolesław III Krzywousty"
```

### Research Historical Events

```
Use search_polish_historical_events to find information about "Powstanie styczniowe"
```

### Get Detailed Information

```
Use get_wikipedia_page with title="Bolesław III Krzywousty" and language="pl"
```

## 🎓 Optimized for Polish History

### Recommended Search Patterns

**Historical Figures:**
- `"{name} król"` - Polish kings
- `"{name} książę"` - Polish dukes
- `"{name} przywódca"` - Polish leaders

**Historical Events:**
- `"Bitwa pod {place}"` - Battles
- `"Powstanie {name}"` - Uprisings
- `"Rok {year}"` - Specific years

**Time Periods:**
- `"Polska {period}"` - Historical periods
- `"Historia Polski {century}"` - Centuries

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

### Wikipedia API Errors

- Wikipedia API may be temporarily unavailable
- Try again after a few seconds
- Check internet connection

## 📁 Project Structure

```
mcp-server/
├── wikipedia_client.py          # Wikipedia API client library
├── wikipedia_mcp_server.py      # FastMCP server implementation
├── requirements.txt             # Python dependencies
├── setup.sh                     # Automated setup script
├── CLAUDE.md                    # Project documentation
└── README.md                    # This file
```

## 🎯 Why This Approach?

### Advantages over SearXNG

1. **No CAPTCHA issues** - Direct API access
2. **Faster** - No intermediate metasearch layer
3. **More reliable** - No bot detection problems
4. **Higher quality** - Wikipedia as primary source
5. **Lighter** - Minimal resource usage
6. **Language-optimized** - Better Polish language support

### Use Cases

- ✅ Historical research
- ✅ Quiz generation
- ✅ Educational content
- ✅ Fact checking
- ✅ Timeline creation
- ✅ Biographical information

## 🚀 Future Enhancements

Potential additions:

1. **Trusted Polish domains** - Add direct search of:
   - ipn.gov.pl (Institute of National Remembrance)
   - dzieje.pl (Polish history portal)
   - psb.org.pl (Polish Biographical Dictionary)
   - muzeum domains (Polish museums)

2. **Content extraction** - Better text extraction and summarization

3. **Quiz generation tools** - Specialized tools for creating history quizzes

4. **Timeline tools** - Extract and organize historical timelines

5. **Multi-source search** - Combine results from multiple Polish sources

## 📝 Notes

- This server is designed for LAN/home use
- Wikipedia API has rate limits (respect these)
- All search queries go directly to Wikipedia (no intermediaries)
- Optimized for Polish history but works for any topic

## 🙏 Acknowledgments

Built with:
- [FastMCP](https://github.com/jlowin/fastmcp) - MCP server framework
- [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page) - Data source
- Polish Wikipedia community - Content creators

---

**For Polish history quiz generation and research, this provides a solid, reliable foundation without the complexity of metasearch engines.**

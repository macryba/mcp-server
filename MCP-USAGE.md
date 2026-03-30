# Using Local MCP Server for Question Generation

## Quick Reference

### MCP Tools Available

The local MCP server provides these tools for Claude Code:

1. **web_search** - Search for Polish historical sources
2. **web_scrape** - Extract content from specific URLs
3. **web_extract** - Structured extraction (requires LLM endpoint, not configured)

### Web Search Usage

When generating questions, use web_search with Polish-specific queries:

```text
Site-restricted searches (best for historical accuracy):
- "site:pl.wikipedia.org Chrzt Polski 966"
- "site:historiaposzkola.pl Piastowie dynastia"
- "site:edu.pl bitwa pod Grunwaldem 1410"
- "site:ipn.gov.pl powstanie styczniowe"
- "site:muzeum historia Polski"

General searches:
- "Piastowie dynastia historia Polski"
- "chrystianizacja Polski skutki"
```

### Typical Workflow

1. **Search for sources**
   ```
   Use web_search to find 3-5 reliable Polish sources about the topic
   ```

2. **Review search results**
   ```
   Identify the most relevant URLs from the search results
   ```

3. **Scrape relevant pages**
   ```
   Use web_scrape on the most promising URLs to get full content
   ```

4. **Generate questions based on scraped content**
   ```
   Use the scraped historical information to create accurate questions
   ```

### Integration with Loop Instructions

Update research section in `.claude/instructions.md`:

```markdown
## 3. Research Sources (ONCE per iteration)

Use the local MCP server web_search tool to find Polish historical sources:

**Priority sources:**
- pl.wikipedia.org (Polish Wikipedia)
- historiaposzkola.pl
- dlaucznia.pl
- edu.pl (Polish educational sites)
- ipn.gov.pl (Institute of National Remembrance)
- muzeum domains (Polish museums)

**Search query format:**
```
site:pl.wikipedia.org [epoka] [rozdział] historia Polski
site:historiaposzkola.pl [wydarzenie] lekcja
site:edu.pl [postać] biografia
```

Then use web_scrape to read the full content of the most relevant pages.
```

### Example Questions Generation Flow

**Step 1: Search**
```
Topic: Chrystianizacja Polski (Piastowie epoch)

Search queries:
- "site:pl.wikipedia.org Chrzt Polski 966"
- "site:historiaposzkola.pl chrystianizacja Polski skutki"
- "site:edu.pl Bolesław Chrobry chrzest Polski"

Get 10-15 search results
```

**Step 2: Scrape**
```
Select 3-5 most relevant URLs from search results
Use web_scrape on each to get full historical content
```

**Step 3: Generate**
```
Based on scraped content, create 10 questions covering:
- Key figures (Mieszko I, Bolesław Chrobry)
- Dates (966, consequences timeline)
- Causes (why Poland accepted Christianity)
- Effects (political, cultural, religious changes)
- Locations (Gniezno, Poznań)
```

### Benefits Over WebSearch Tool

1. **No rate limits** - Self-hosted, no API quotas
2. **Polish-focused** - Configured for Polish historical sources
3. **Consistent results** - Same search engine configuration
4. **Site-specific** - Easy to restrict to trusted domains
5. **Faster** - Local queries, no external API calls
6. **Privacy** - No search queries sent to third parties

### Testing MCP Connection

Test that MCP server is accessible from Claude Code:

```bash
# Check containers are running
cd ~/mcp-server && docker compose ps

# Should show:
# searxng          Up     0.0.0.0:8080->8080/tcp
# mcp-web-search   Up     0.0.0.0:8100->8100/tcp

# Test SearXNG directly
curl "http://localhost:8080/search?q=Piastowie&language=pl" | grep "Polish History"

# Test MCP server endpoint
curl -X POST http://localhost:8100/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

### Troubleshooting

**MCP tools not available in Claude Code:**
1. Check containers are running: `docker compose ps`
2. Check Claude Code config: `cat ~/.claude/settings.json`
3. Restart Claude Code
4. Check MCP server logs: `docker compose logs -f web-mcp`

**Poor search results:**
1. Use site-restricted searches (site:pl.wikipedia.org)
2. Try different search engines in SearXNG config
3. Use broader search terms
4. Check SearXNG logs: `docker compose logs -f searxng`

**Containers not starting:**
1. Check Docker is running: `docker ps`
2. Check port availability: `sudo netstat -tulpn | grep -E '8080|8100'`
3. View logs: `docker compose logs -f`
4. Restart services: `docker compose restart`

### Management Commands

```bash
# Start services
cd ~/mcp-server && docker compose up -d

# Stop services
docker compose stop

# Restart services
docker compose restart

# View logs
docker compose logs -f

# Update services
docker compose pull && docker compose up -d

# Check status
docker compose ps

# Remove everything
docker compose down -v
```

### Search Engine Configuration

The SearXNG instance is configured with:
- **Wikipedia Polish** - Primary source for historical facts
- **DuckDuckGo** - General web search

To add more engines, edit `~/mcp-server/searxng-settings/settings.yml` and restart:
```bash
cd ~/mcp-server
nano searxng-settings/settings.yml
docker compose restart searxng
```

### Performance Tips

1. **Use site-specific searches first** - Higher quality, faster
2. **Batch searches** - Do multiple searches in one session
3. **Scrape selectively** - Only scrape pages that look relevant
4. **Reuse sources** - Save good URLs for future questions
5. **Monitor logs** - Check `docker compose logs -f` to debug

### Next Steps

1. Verify MCP server is running
2. Test web_search with a Polish history query
3. Test web_scrape on a Wikipedia page
4. Update question generation workflow to use MCP tools
5. Run the loop and monitor results

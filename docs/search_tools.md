# Search Tools - MCP Server Reference

Complete reference for all search tools available in the Polish History MCP server.

## Overview

The Polish History MCP server provides **10 search tools** optimized for historical research across Polish Wikipedia, with planned support for IPN, Dzieje.pl, and other Polish historical sources.

## Search Tools Reference Table

| Tool Name | Short Description | Input Schema | Output Schema |
|-----------|------------------|--------------|---------------|
| `search_polish_history` | Multi-domain search across Polish Wikipedia and future Polish sources | `query: str`<br>`domains: List[str] = None`<br>`limit: int = 10` | `List[Dict]` with:<br>`- title: str`<br>`- url: str`<br>`- snippet: str`<br>`- source: str`<br>`- relevance_score: float`<br>`- metadata: Dict` |
| `search_wikipedia` | Search Polish Wikipedia for historical topics | `query: str`<br>`max_results: int = 5` | `str(JSON)` with search results array<br>Each result: title, snippet, url, source, relevance_score, metadata |
| `search_historical_figures` | Optimized search for Polish kings, queens, leaders, historical personalities | `query: str`<br>`period: str = None` (e.g., "XVII wiek", "1945-1989") | `str(JSON)` with enhanced results including:<br>`- source_type: 'Polish historical figure'`<br>`- suggested_domains: ['pl.wikipedia.org', 'ipn.gov.pl', 'dzieje.pl']` |
| `search_historical_events` | Optimized for battles, uprisings, treaties, historical events | `query: str`<br>`date_range: str = None` (e.g., "1939-1945") | `str(JSON)` with enhanced results including:<br>`- source_type: 'Polish historical event'`<br>`- suggested_domains: ['pl.wikipedia.org', 'dzieje.pl', 'ipn.gov.pl', 'encyklopedia.pwn.pl']` |
| `search_historical_places` | Find historical locations and places | `query: str`<br>`region: str = None` | `str(JSON)` with results including:<br>`- source_type: 'Historical place'` |
| `search_primary_sources` | Search for documents, archives, newspapers | `query: str`<br>`source_type: str = None` ("documents", "archives", "newspapers") | `str(JSON)` with results including:<br>`- source_type: 'Primary source'`<br>`- suggested_domains: ['polona.pl', 'ipn.gov.pl', 'pl.wikipedia.org']` |
| `search_biographies` | Find biographical entries and life stories | `query: str`<br>`profession: str = None` | `str(JSON)` with results including:<br>`- source_type: 'Biography'`<br>`- suggested_domains: ['pl.wikipedia.org']` |
| `search_timelines` | Search for chronological data and timelines | `topic: str`<br>`period: str = None` | `str(JSON)` with results including:<br>`- source_type: 'Timeline data'` |
| `search_definitions` | Search encyclopedic definitions and explanations | `term: str`<br>`domain: str = None` ("pwn", "wikipedia") | `str(JSON)` with results including:<br>`- source_type: 'Definition'`<br>`- suggested_domains: ['encyklopedia.pwn.pl', 'pl.wikipedia.org']` |
| `server_info` | Get server capabilities, version, supported domains | `None` | `str(JSON)` with:<br>`- name: str`<br>`- version: str`<br>`- capabilities: Dict`<br>`- supported_domains: List[str]` |

## Common Output Schema Structure

All search tools return results in this base format (with tool-specific enhancements):

```python
{
    "title": "Page title",
    "url": "https://domain.org/page",
    "snippet": "Brief description",
    "source": "wikipedia_pl" | "wikipedia_en",
    "relevance_score": 0.0-1.0,
    "metadata": {
        "wordcount": int,
        "timestamp": str,
        "language": "pl" | "en"
    }
    # Tool-specific additions:
    # "source_type": str
    # "suggested_domains": List[str]
}
```

## Tool Categories

### General Search Tools
- **`search_polish_history`** - Primary multi-domain search tool
- **`search_wikipedia_polish`** - Direct Polish Wikipedia search
- **`search_wikipedia_english`** - Direct English Wikipedia search
- **`server_info`** - Server metadata and capabilities

### Specialized Search Tools
- **`search_historical_figures`** - Optimized for people (kings, queens, leaders)
- **`search_historical_events`** - Optimized for events (battles, uprisings, treaties)
- **`search_historical_places`** - Find geographical locations

### Research Tools
- **`search_biographies`** - Biographical entries and life stories
- **`search_primary_sources`** - Documents, archives, newspapers
- **`search_timelines`** - Chronological data and timelines
- **`search_definitions`** - Encyclopedic definitions

## Usage Examples

### Basic Search
```python
# Search Polish Wikipedia
results = await search_wikipedia_polish("Bolesław III Krzywousty", 10)

# Multi-domain search
results = await search_polish_history("Bitwa pod Grunwaldem", ["wikipedia_pl", "wikipedia_en"], 5)
```

### Specialized Search
```python
# Historical figure with period
results = await search_historical_figures("Jan Sobieski", "XVII wiek")

# Historical event with date range
results = await search_historical_events("Powstanie styczniowe", "1863-1865")

# Primary sources
results = await search_primary_sources("Konstytucja 3 maja", "documents")
```

## Best Practices

### Query Optimization
- **Use Polish names**: "Bolesław III Krzywousty" not "Boleslaus the Wry-mouthed"
- **Include years**: "Bitwa pod Grunwaldem 1410"
- **Use Polish diacritics**: "Powstanie styczniowe"
- **Add context**: Include historical periods for better results

### Tool Selection
- **Start with specialized tools**: `search_historical_figures` for people, `search_historical_events` for events
- **Use English Wikipedia for**: International context, English-language sources
- **Primary sources**: Use `search_primary_sources` for documents and archives

### Domain Selection
- **Current support**: Wikipedia (Polish & English)
- **Coming soon**: IPN, Dzieje.pl, Polona, PSB, PWN Encyclopedia
- **Trusted domains**: gov.pl, edu.pl, established Polish historical sources

## Response Formats

### JSON String Response
Most tools return `str(JSON)` for MCP protocol compatibility:
```python
# Parse response
import json
results = json.loads(await search_wikipedia_polish("query"))
```

### Direct List Response
`search_polish_history` returns `List[Dict]` directly:
```python
# Direct usage
results = await search_polish_history("query")
for result in results:
    print(result['title'], result['url'])
```

## Error Handling

All tools include error handling:
```python
# Error response format
{
    "error": "Error message",
    "source": "wikipedia_pl",
    "query": "original_query"
}
```

## Related Tools

- **Extract Tools**: `extract_article`, `extract_facts`, `extract_timeline`, `extract_biography`
- **Quiz Tools**: `generate_quiz_question`, `generate_quiz_questions`, `validate_quiz_answer`

See also:
- [Extract Tools Documentation](extract_tools.md)
- [Quiz Tools Documentation](quiz_tools.md)
- [Server Architecture](mcp-architecture.md)
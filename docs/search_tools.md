# Search Tools - MCP Server Reference

Complete reference for all search tools available in the Polish History MCP server.

## Quick Start: AI Agent Workflow

**For AI Agents: This MCP server supports a 3-step intelligent search workflow:**

1. **Quick Basic Research** → `search_wikipedia` for fast overviews
2. **Learn Domain Specializations** → `list_domains` to understand available sources
3. **Targeted Deep Search** → `search_polish_history` with specific domains

**Example:**
```python
# Step 1: Quick Wikipedia lookup
basic_info = await search_wikipedia("Powstanie warszawskie")

# Step 2: If user needs primary sources, learn what's available
domains = await list_domains()
# → Learn that IPN and Polona specialize in WWII primary sources

# Step 3: Targeted search with appropriate domains
deep_research = await search_polish_history(
    "Powstanie warszawskie dokumenty",
    domains=["ipn", "polona"]  # Use specialized sources
)
```

**See "Recommended Workflow for AI Agents" section below for detailed guidance.**

## Overview

The Polish History MCP server provides **3 core search tools** for historical research across 7 Polish historical sources. The tools follow a simple, powerful design that lets AI agents enhance queries naturally rather than providing specialized wrappers for every search type.

## Philosophy

**Why only 3 search tools?**

Modern AI agents are capable of formulating context-appropriate search queries. Rather than providing specialized tools like `search_historical_figures` or `search_historical_events`, we provide two flexible search tools and let the agent enhance queries as needed:

```
User: "Find Polish kings from 17th century"
Agent: → search_polish_history("król Polski XVII wiek")
```

This approach:
- **Reduces tool bloat** - Fewer tools to learn and maintain
- **Increases flexibility** - Agent can adapt search strategy to context
- **Improves performance** - Fewer tool options to consider
- **Simplifies architecture** - Clean separation of concerns

## Recommended Workflow for AI Agents

This MCP server is designed to support an intelligent, progressive search workflow:

### Step 1: Quick Basic Research
**Tool:** `search_wikipedia`
**Use when:** You need basic information, general overviews, or quick facts
**Example:**
```python
# User asks about a historical topic
results = await search_wikipedia("Bitwa pod Grunwaldem")
# Returns: Wikipedia overview - good for basic facts
```

### Step 2: Assess Need for Specialized Sources
**Question:** Does the user need specialized, authoritative, or comprehensive information?
- **Need depth:** Primary sources, archival documents, academic research
- **Need specificity:** Regional history, specific periods, specialized topics
- **Need diversity:** Multiple perspectives beyond Wikipedia

If **YES** → Proceed to Step 3

### Step 3: Learn Available Domains
**Tool:** `list_domains`
**Purpose:** Understand what sources are available and their specializations
**Example:**
```python
# Learn what domains are available
domains = await list_domains(include_unimplemented=False)

# Analyze the results to find relevant domains:
# - IPN: specializes in 20th century, WWII, communism
# - Polona: primary sources, documents, archival materials
# - Dzieje.pl: popular history, magazines, articles
# - Wikipedia: general knowledge (always available)
```

### Step 4: Targeted Domain-Specific Search
**Tool:** `search_polish_history` with specific `domains` parameter
**Purpose:** Get highly relevant results from the most appropriate sources
**Example:**
```python
# User wants primary sources about World War II
results = await search_polish_history(
    "II wojna światowa dokumenty",
    domains=["ipn", "polona"],  # Target domains that specialize in this
    limit=10
)

# User wants educational content about medieval kings
results = await search_polish_history(
    "król Polski średniowiecze",
    domains=["wikipedia", "dzieje", "gwo"],  # Educational + general sources
    limit=5
)
```

### Workflow Summary

```
┌─────────────────────────────────────────────────────────────┐
│ User Request: "Tell me about the Warsaw Uprising"          │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Quick Wikipedia lookup                             │
│ search_wikipedia("Powstanie warszawskie")                  │
│ → Good basic overview, but user wants primary sources      │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 2: User wants primary sources and archival documents   │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 3: Learn domain specializations                       │
│ list_domains()                                             │
│ → Learn IPN specializes in WWII, Polona has archives       │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 4: Targeted search with appropriate domains            │
│ search_polish_history(                                     │
│   "Powstanie warszawskie dokumenty",                      │
│   domains=["ipn", "polona"]                               │
│ )                                                         │
│ → Highly relevant primary sources from experts            │
└─────────────────────────────────────────────────────────────┘
```

### Key Points for AI Agents

1. **Start simple:** Use `search_wikipedia` first for basic information
2. **Progress intelligently:** If user needs depth, use `list_domains` to learn about specialized sources
3. **Search strategically:** Use `search_polish_history` with specific domains based on learned specializations
4. **Think about user intent:** Different questions require different sources
   - Quick facts → Wikipedia
   - Academic research → Polona + IPN
   - Educational content → GWO + SuperKid + Dzieje
   - Popular history → Dzieje + Przystanek Historia

Modern AI agents are capable of formulating context-appropriate search queries. Rather than providing specialized tools like `search_historical_figures` or `search_historical_events`, we provide two flexible search tools and let the agent enhance queries as needed:

```
User: "Find Polish kings from 17th century"
Agent: → search_polish_history("król Polski XVII wiek")
```

This approach:
- **Reduces tool bloat** - Fewer tools to learn and maintain
- **Increases flexibility** - Agent can adapt search strategy to context
- **Improves performance** - Fewer tool options to consider
- **Simplifies architecture** - Clean separation of concerns

## Search Tools Reference Table

| Tool Name | Short Description | Input Schema | Output Schema |
|-----------|------------------|--------------|---------------|
| `search_polish_history` | Multi-domain search across 7 Polish historical sources | `query: str`<br>`domains: List[str] = None`<br>`limit: int = 10` | `List[Dict]` with:<br>`- title: str`<br>`- url: str`<br>`- snippet: str`<br>`- source: str`<br>`- relevance_score: float`<br>`- metadata: Dict` |
| `search_wikipedia` | Search Polish Wikipedia for historical topics | `query: str`<br>`max_results: int = 5` | `str(JSON)` with search results array<br>Each result: title, snippet, url, source, relevance_score, metadata |
| `list_domains` | Get information about available historical source domains | `include_unimplemented: bool = False` | `str(JSON)` with domain information including:<br>`- name: str`<br>`- base_url: str`<br>`- description: str`<br>`- capabilities: Dict`<br>`- implementation_status: str` |

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

### Multi-Domain Search
- **`search_polish_history`** - Primary search tool across all 7 implemented Polish historical sources

### Wikipedia Search
- **`search_wikipedia`** - Direct Polish Wikipedia search for quick lookups

### Informational
- **`list_domains`** - Discover available historical sources and their capabilities

## Implemented Domains

The `search_polish_history` tool searches across these 7 implemented domains:

1. **Wikipedia** (Polish) - API search
2. **Dzieje.pl** - Web scraping
3. **Polona** (National Library) - API search
4. **SuperKid** - Web scraping
5. **IPN** (Edukacja IPN) - Web scraping
6. **Przystanek Historia** - Web scraping
7. **GWO** (Historia) - Web scraping

## Usage Examples

### Basic Multi-Domain Search
```python
# Search all implemented domains
results = await search_polish_history("Bitwa pod Grunwaldem")

# Search specific domains
results = await search_polish_history("Powstanie styczniowe", ["wikipedia", "ipn"], 5)
```

### Wikipedia-Only Search
```python
# Quick Wikipedia lookup
results = await search_wikipedia("Bolesław III Krzywousty")
```

### Context-Enhanced Search
The AI agent naturally enhances queries based on context:

```python
# User: "Find Polish kings from 17th century"
results = await search_polish_history("król Polski XVII wiek")

# User: "Primary sources about May 3 Constitution"
results = await search_polish_history("Konstytucja 3 maja dokumenty źródła")

# User: "Battles involving Jan III Sobieski"
results = await search_polish_history("bitwy Jan III Sobieski")
```

### Domain Discovery
```python
# List all implemented domains
domains = await list_domains(include_unimplemented=False)

# Get information about specific domain capabilities
all_domains = await list_domains(include_unimplemented=True)
```

## Best Practices

### Query Optimization
- **Use Polish names**: "Bolesław III Krzywousty" not "Boleslaus the Wry-mouthed"
- **Include years**: "Bitwa pod Grunwaldem 1410"
- **Use Polish diacritics**: "Powstanie styczniowe"
- **Add context terms**: Include historical periods, source types, or keywords
  - "król" for kings, "bitwa" for battles, "dokumenty" for primary sources

### Tool Selection
- **Use `search_polish_history` for**: Comprehensive research across multiple Polish historical sources
- **Use `search_wikipedia` for**: Quick Wikipedia lookups when multi-domain search isn't needed
- **Use `list_domains` for**: Discovering available sources and their capabilities

### Domain Selection
- **Default**: Let the tool search all implemented domains for comprehensive results
- **Specific research**: Target domains by expertise:
  - `["polona", "ipn"]` for primary sources and documents
  - `["wikipedia", "dzieje"]` for general historical overviews
  - `["ipn", "przystanek_historia"]` for 20th century history

### Query Enhancement Strategies
Instead of specialized tools, enhance queries naturally:

| Research Goal | Query Enhancement |
|---------------|-------------------|
| Historical figures | Add "król", "książę", "władca" or name + period |
| Events | Add "bitwa", "powstanie", "traktat", date ranges |
| Primary sources | Add "dokumenty", "archiwa", "źródła", "manuskrypty" |
| Places | Add "miasto", "zamek", "miejsce historyczne" |
| Biographies | Add "biografia", "życiorys", "postać" |

## Response Formats

### JSON String Response
`search_wikipedia` and `list_domains` return `str(JSON)` for MCP protocol compatibility:
```python
# Parse response
import json
results = json.loads(await search_wikipedia("Bolesław III Krzywousty"))
```

### Direct List Response
`search_polish_history` returns `List[Dict]` directly:
```python
# Direct usage
results = await search_polish_history("Bitwa pod Grunwaldem")
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
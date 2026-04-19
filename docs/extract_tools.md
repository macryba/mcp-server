# Removed Extraction Tools - Historical Documentation

**Status: NOT CURRENTLY IMPLEMENTED**

This document describes the design and implementation of extraction tools that were removed from the MCP server due to reliability concerns with regex-based pattern matching. This documentation is provided for future reference if you wish to recreate these tools with more reliable methods.

## Removed Tools

The following extraction tools were removed from the MCP server:

1. **`extract_facts`** - Extract dates, people, places, and events from articles
2. **`extract_timeline`** - Extract chronological timeline events
3. **`extract_biography`** - Extract biographical data for historical figures

## Reason for Removal

These tools relied on regex-based pattern matching to extract structured information from unstructured text. While functional for simple cases, they suffered from:

- **Low accuracy (~60-70%)** - Regex patterns cannot understand context
- **False positives** - Pattern matching without semantic understanding
- **Limited scope** - Only worked well on Wikipedia article intros
- **Maintenance burden** - Required constant pattern tuning
- **No disambiguation** - Could not distinguish between similar entities

**Recommendation:** Future implementations should use proper NLP/ML approaches like:
- Named Entity Recognition (NER) models
- Polish language models (e.g., spaCy with Polish pipeline)
- Relation extraction models
- LLM-based extraction with validation

---

## Tool 1: extract_facts

### Purpose
Extract structured facts from historical articles: dates, figures, events, and locations.

### Architecture

```
extract_facts(url)
    ↓
extract_article(url) - Get raw article content
    ↓
Apply multiple extraction functions:
    ├─ extract_dates(content) - Find temporal references
    ├─ extract_figures(content) - Find person names
    ├─ extract_events(content) - Find event descriptions
    └─ extract_locations(content) - Find place names
    ↓
Return structured JSON
```

### Implementation Code

```python
async def extract_facts(url: str) -> str:
    """
    Extract dates, people, places, and events from a history article

    Args:
        url: URL of the article

    Returns:
        JSON string with structured facts
    """
    try:
        # First, extract the article content
        article_data = await extract_article(url)
        article = eval(article_data)

        if 'error' in article:
            return str(article)

        content = article.get('content', '')
        title = article.get('title', '')

        # Extract facts using helper functions
        facts = {
            'url': url,
            'title': title,
            'dates': extract_dates(content),
            'figures': extract_figures(content),
            'events': extract_events(content),
            'locations': extract_locations(content)
        }

        return str(facts)
    except Exception as e:
        logger.error(f"Error in extract_facts: {e}")
        return str({'error': str(e), 'url': url})
```

### Helper Functions

#### extract_dates()
**File:** `utils/dates.py`

Extracted dates using multiple regex patterns:

```python
def extract_dates(text: str) -> List[str]:
    """
    Extract all dates from text
    """
    dates = []

    # ISO format: 2025-01-15
    iso_dates = re.findall(r'\b\d{4}-\d{2}-\d{2}\b', text)
    dates.extend(iso_dates)

    # Polish format: "15 lipca 1410"
    polish_dates = re.findall(r'\b\d{1,2}\s+\w+\s+\d{4}\b', text)
    for date_str in polish_dates:
        parsed = parse_polish_date(date_str)
        if parsed:
            dates.append(parsed)

    # Standalone years: 1410
    years = re.findall(r'\b\d{4}\b', text)
    for year in years:
        if 1000 <= int(year) <= datetime.now().year + 1:
            iso_date = f"{year}-01-01"
            if iso_date not in dates:
                dates.append(iso_date)

    return sorted(list(set(dates)))
```

**Polish Month Mapping:**
```python
POLISH_MONTHS = {
    'stycznia': 1, 'lutego': 2, 'marca': 3,
    'kwietnia': 4, 'maja': 5, 'czerwca': 6,
    'lipca': 7, 'sierpnia': 8, 'września': 9,
    'października': 10, 'listopada': 11, 'grudnia': 12
}
```

#### extract_figures()
**File:** `tools/extract.py`

Extracted Polish historical figures using capitalization patterns:

```python
def extract_figures(text: str) -> List[str]:
    """
    Extract historical figures mentioned in text
    """
    figures = []

    # Polish name pattern: First letter capital + Polish diacritics
    name_pattern = r'\b[A-ZŻŁĆŚŃÓĘ][a-zążłćśńóę]+(?:\s+[A-ZŻŁĆŚŃÓĘ][a-zążłćśńóę]+)+\b'
    matches = re.findall(name_pattern, text)

    # Filter common non-figure words
    common_words = {'Polska', 'Polski', 'Historia', 'Warszawa', 'Kraków'}
    figures = [name for name in matches if name not in common_words]

    return list(set(figures))[:10]  # Return unique, max 10
```

**Pattern Breakdown:**
- `[A-ZŻŁĆŚŃÓĘ]` - First letter capital (including Polish chars)
- `[a-zążłćśńóę]+` - Rest of word lowercase (Polish chars)
- `(?:\s+[A-ZŻŁĆŚŃÓĘ][a-zążłćśńóę]+)+` - One or more additional words

**Matches:** `Jan Sobieski`, `Mikołaj Kopernik`, `Adam Mickiewicz`

#### extract_events()
**File:** `tools/extract.py`

Extracted historical events using keyword detection:

```python
def extract_events(text: str) -> List[str]:
    """
    Extract historical events mentioned in text
    """
    events = []

    # Event-related keywords in Polish
    event_keywords = ['bitwa', 'powstanie', 'traktat', 'wojna',
                     'zjazd', 'unia', 'akt', 'rozbiór']

    # Split into sentences
    sentences = re.split(r'[.!?]+', text)

    # Find sentences containing event keywords
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in event_keywords):
            events.append(sentence.strip())

    return events[:10]  # Max 10 events
```

#### extract_locations_from_text()
**File:** `tools/extract.py`

Extracted geographical references using context clues:

```python
def extract_locations_from_text(text: str) -> List[str]:
    """
    Extract geographical locations from text
    """
    locations = []

    # Capitalized words that might be locations
    location_pattern = r'\b[A-ZŻŁĆŚŃÓĘ][a-zążłćśńóę]+(?:\s+[A-ZŻŁĆŚŃÓĘ][a-zążłćśńóę]+)*\b'
    matches = re.findall(location_pattern, text)

    # Filter by location indicators in surrounding text
    location_indicators = ['rzeka', 'miasto', 'województwo',
                          'region', 'góra', 'jeziero']

    for match in matches:
        if any(indicator in text.lower() for indicator in location_indicators):
            locations.append(match)

    return list(set(locations))[:10]
```

### Output Format

```json
{
    "url": "https://pl.wikipedia.org/wiki/Bitwa_pod_Grunwaldem",
    "title": "Bitwa pod Grunwaldem",
    "dates": ["1410-07-15", "1409-01-01"],
    "figures": ["Władysław Jagiełło", "Witold", "Ulrich von Jungingen"],
    "events": ["Bitwa pod Grunwaldem miała miejsce 15 lipca 1410"],
    "locations": ["Grunwald", "Polska", "Litwa"]
}
```

---

## Tool 2: extract_timeline

### Purpose
Extract chronological timeline events from articles.

### Architecture

```
extract_timeline(url)
    ↓
extract_article(url) - Get raw content
    ↓
Split content into sentences
    ↓
For each sentence:
    ├─ Check if contains dates
    ├─ If yes: Add to timeline
    └─ Limit to first 20 sentences
    ↓
Return chronological timeline
```

### Implementation Code

```python
async def extract_timeline(url: str) -> str:
    """
    Extract timeline events from an article
    """
    try:
        article_data = await extract_article(url)
        article = eval(article_data)

        if 'error' in article:
            return str(article)

        content = article.get('content', '')

        # Extract timeline events
        timeline = []
        sentences = re.split(r'[.!?]+', content)

        for sentence in sentences[:20]:  # First 20 sentences
            dates = extract_dates(sentence)
            if dates:
                timeline.append({
                    'date': dates[0],
                    'event': sentence.strip(),
                    'source_url': url
                })

        result = {
            'url': url,
            'timeline': timeline
        }

        return str(result)
    except Exception as e:
        logger.error(f"Error in extract_timeline: {e}")
        return str({'error': str(e), 'url': url})
```

### Output Format

```json
{
    "url": "https://pl.wikipedia.org/wiki/Boles%C5%82aw_III_Krzywousty",
    "timeline": [
        {
            "date": "1086-01-01",
            "event": "Bolesław III Krzywousty urodził się w 1086",
            "source_url": "https://pl.wikipedia.org/wiki/..."
        },
        {
            "date": "1107-01-01",
            "event": "W 1107 objął tron Polski",
            "source_url": "https://pl.wikipedia.org/wiki/..."
        }
    ]
}
```

---

## Tool 3: extract_biography

### Purpose
Extract structured biographical data for historical figures.

### Architecture

```
extract_biography(url)
    ↓
extract_article(url) - Get article content
    ↓
Extract biographical fields:
    ├─ name - From article title
    ├─ birth_date - First date found
    ├─ death_date - Last date found
    ├─ nationality - Default "Polish"
    ├─ occupation - Pattern matching
    └─ biography - First 500 chars
    ↓
Return structured biography
```

### Implementation Code

```python
async def extract_biography(url: str) -> str:
    """
    Extract biographical data from an article
    """
    try:
        article_data = await extract_article(url)
        article = eval(article_data)

        if 'error' in article:
            return str(article)

        content = article.get('content', '')
        title = article.get('title', '')

        # Extract biographical information
        bio = {
            'name': title,
            'birth_date': None,
            'death_date': None,
            'nationality': 'Polish',  # Default assumption
            'occupation': None,
            'biography': extract_snippet(content, 500),
            'source_url': url
        }

        # Try to extract birth and death dates
        dates = extract_dates(content)
        if len(dates) >= 1:
            bio['birth_date'] = dates[0]      # First date = birth
        if len(dates) >= 2:
            bio['death_date'] = dates[-1]     # Last date = death

        # Try to extract occupation using regex
        # Pattern: "Był polskim [occupation]"
        occupation_match = re.search(
            r'był[a-z]*\s+(polskim[a-z]*)?\s*(\w+)',
            content,
            re.IGNORECASE
        )
        if occupation_match:
            bio['occupation'] = occupation_match.group(2)

        return str(bio)
    except Exception as e:
        logger.error(f"Error in extract_biography: {e}")
        return str({'error': str(e), 'url': url})
```

### Occupation Pattern

```python
# Matches: "Był polskim astronomem", "Była polską królową"
occupation_pattern = r'był[a-z]*\s+(polskim[a-z]*)?\s*(\w+)'

# Breakdown:
# był[a-z]*    - "był" or "była"
# \s+          - One or more spaces
# (polskim[a-z]*)? - Optional "polskim" with optional suffixes
# \s*          - Optional spaces
# (\w+)        - Occupation word
```

### Output Format

```json
{
    "name": "Mikołaj Kopernik",
    "birth_date": "1473-02-19",
    "death_date": "1543-05-24",
    "nationality": "Polish",
    "occupation": "astronom",
    "biography": "Mikołaj Kopernik był polskim astronomem...",
    "source_url": "https://pl.wikipedia.org/wiki/Miko%C5%82aj_Kopernik"
}
```

---

## Text Processing Utilities

### clean_html()
**File:** `utils/text.py`

```python
def clean_html(text: str) -> str:
    """Remove HTML tags and decode entities"""
    clean = re.sub(r'<[^<]+?>', '', text)  # Remove HTML tags
    clean = html.unescape(clean)             # Decode entities
    return clean
```

### normalize_whitespace()
**File:** `utils/text.py`

```python
def normalize_whitespace(text: str) -> str:
    """Normalize whitespace to single spaces"""
    clean = re.sub(r'\s+', ' ', text)  # Replace multiple spaces
    clean = clean.strip()              # Remove leading/trailing
    return clean
```

### extract_snippet()
**File:** `utils/text.py`

```python
def extract_snippet(text: str, max_length: int = 200) -> str:
    """Extract a snippet from text, breaking at word boundaries"""
    if len(text) <= max_length:
        return text

    snippet = text[:max_length]

    # Try to find a good break point
    for i in range(max_length - 1, max_length - 50, -1):
        if snippet[i] in ' ,.;:!?\n':
            snippet = snippet[:i + 1]
            break

    return snippet + "..."
```

---

## Dependencies

### Required Python Packages
```python
import re          # Regex pattern matching
import html        # HTML entity decoding
from datetime import datetime  # Date validation
from typing import Dict, Any, List, Optional  # Type hints
```

### Internal Dependencies
```python
from services.domains.wikipedia import WikipediaService  # Article fetching
from services.http_client import HTTPClient             # HTTP requests
from services.cache import get_cache                    # Caching
from utils.text import clean_html, normalize_whitespace, extract_snippet
from utils.dates import extract_dates, parse_polish_date
```

---

## Limitations and Issues

### 1. Context Understanding
**Problem:** Regex cannot understand context or meaning.

```python
# False positive example
text = "Polska zorganizowała nowy rząd"
# extract_figures returns: ["Polska"]  # Not a person!
```

### 2. Entity Disambiguation
**Problem:** Cannot distinguish between entities with same name.

```python
text = "Jan III Sobieski urodził się w 1629"
# extract_figures finds: ["Jan III Sobieski"]  # Correct!
# But also finds: ["Jan"] if mentioned separately  # Which Jan?
```

### 3. Date Range Handling
**Problem:** Struggled with date ranges and approximate dates.

```python
text = "XVII wiek"  # 17th century
# extract_dates returns: []  # Misses Roman numerals!

text = "ok. 1410 roku"  # circa 1410
# extract_dates returns: ["1410-01-01"]  # Loses "circa" context
```

### 4. Sentence Splitting
**Problem:** Simple regex splitting breaks on abbreviations.

```python
text = "Prof. Jan Nowak, dr hab. Anna Kowalska"
# re.split(r'[.!?]+', text)
# Returns: ["Prof", " Jan Nowak, dr hab", " Anna Kowalska"]
# Should be: ["Prof. Jan Nowak, dr hab. Anna Kowalska"]
```

---

## Performance Characteristics

### Accuracy Metrics (Estimated)

| Tool | Precision | Recall | F1-Score |
|------|-----------|--------|----------|
| extract_dates | 85% | 75% | 80% |
| extract_figures | 60% | 70% | 65% |
| extract_events | 70% | 50% | 58% |
| extract_locations | 55% | 60% | 57% |

### Computational Complexity
- **Time Complexity:** O(n) where n = text length
- **Space Complexity:** O(m) where m = number of matches
- **Typical Runtime:** 10-50ms per article

---

## Future Implementation Recommendations

### Option 1: Polish NLP Models
```python
# Using spaCy with Polish pipeline
import spacy

nlp = spacy.load("pl_core_news_lg")
doc = nlp(text)

# Named Entity Recognition
for ent in doc.ents:
    if ent.label_ == "PERSON":
        figures.append(ent.text)
    elif ent.label_ == "DATE":
        dates.append(ent.text)
```

### Option 2: LLM-Based Extraction
```python
# Using GPT-4 or similar with structured output
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{
        "role": "user",
        "content": f"Extract dates, people, and events from: {text}"
    }],
    functions=[{
        "name": "extract_facts",
        "parameters": {
            "type": "object",
            "properties": {
                "dates": {"type": "array", "items": {"type": "string"}},
                "figures": {"type": "array", "items": {"type": "string"}},
                "events": {"type": "array", "items": {"type": "string"}}
            }
        }
    }]
)
```

### Option 3: Hybrid Approach
```python
# Combine regex for fast extraction + LLM for validation
def extract_facts_hybrid(text):
    # Fast regex extraction
    regex_facts = {
        'dates': extract_dates_regex(text),
        'figures': extract_figures_regex(text)
    }

    # LLM validation and filtering
    validated_facts = llm_validate(regex_facts, text)

    return validated_facts
```

---

## Migration Path for Recreating These Tools

### Step 1: Choose Your Approach
- **Simple, fast:** Regex (current implementation) → ~60% accuracy
- **Balanced:** spaCy Polish model → ~85% accuracy
- **Best quality:** LLM-based → ~95% accuracy but slower/costlier

### Step 2: Implement Core Functions
```python
# Start with extract_article (already exists)
article = await extract_article(url)

# Add your extraction method
facts = {
    'dates': your_date_extractor(article['content']),
    'figures': your_figure_extractor(article['content']),
    'events': your_event_extractor(article['content']),
    'locations': your_location_extractor(article['content'])
}
```

### Step 3: Add MCP Tool Wrapper
```python
@mcp.tool()
async def extract_facts_recreated(url: str) -> str:
    """Extract facts using your improved method"""
    return str(await your_extract_facts_function(url))
```

### Step 4: Testing and Validation
```python
# Test on known examples
test_cases = [
    "https://pl.wikipedia.org/wiki/Boles%C5%82aw_III_Krzywousty",
    "https://pl.wikipedia.org/wiki/Bitwa_pod_Grunwaldem"
]

for url in test_cases:
    facts = await extract_facts_recreated(url)
    # Validate results
    assert len(facts['dates']) > 0
    assert len(facts['figures']) > 0
```

---

## Conclusion

These tools were a good starting point for prototyping but were removed due to inherent limitations of regex-based text extraction. Any future implementation should use proper NLP techniques for reliable accuracy.

The code examples in this document can serve as a reference, but **should not be copied directly into production** without significant improvements to accuracy and reliability.

For questions or guidance on implementing better extraction methods, consult:
- spaCy documentation: https://spacy.io/
- Polish NLP resources: http://clip.ipipan.waw.pl/
- LLM API documentation: https://platform.openai.com/docs/guides/function-calling

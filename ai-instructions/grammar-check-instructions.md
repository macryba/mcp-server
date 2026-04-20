# Grammar Check Instructions

## When to Use Grammar Checking

Use the grammar checking tool (`check_grammar`) when:

**Polish Text Quality:**
- User asks to check, proofread, or improve Polish text
- User mentions "grammar", "spelling", "język polski", "polszczyzna"
- User wants to validate Polish documents, emails, or messages
- Writing Polish content that needs verification

**Multi-language Text:**
- User asks to check grammar in any supported language (pl-PL, en-US, en-GB, de-DE, fr-FR, etc.)
- Text contains language-specific errors or style issues
- User wants suggestions for better wording

**Content Creation:**
- Writing documentation, emails, articles in Polish/English
- Creating formal or professional text
- Proofreading before publishing or sending

## Tool Usage

### Basic Syntax

```
check_grammar("text to check")
check_grammar("text to check", "language-code")
```

### Parameters

- `text` (required): The text to check for grammar errors
- `language` (optional): Language code, default is "pl-PL"
  - Polish: "pl-PL"
  - English US: "en-US"
  - English GB: "en-GB"
  - German: "de-DE"
  - French: "fr-FR"
  - Spanish: "es-ES"
  - And many more supported by LanguageTool

### Return Format

The tool returns a JSON string with:

```json
{
  "matches": [
    {
      "message": "Detailed error explanation",
      "shortMessage": "Brief error description",
      "replacements": ["suggestion1", "suggestion2"],
      "context": {
        "text": "Context with error",
        "offset": 0,
        "length": 5
      },
      "rule": {
        "id": "RULE_ID",
        "description": "Rule description",
        "issueType": "grammar|spelling|style",
        "category": {
          "id": "CATEGORY_ID",
          "name": "Category name"
        }
      },
      "sentence": "Full sentence with error",
      "offset": 0,
      "length": 5
    }
  ],
  "language": {
    "name": "Polish",
    "code": "pl-PL",
    "detectedLanguage": {
      "name": "Polish",
      "code": "pl-PL",
      "confidence": 1.0
    }
  },
  "summary": {
    "total_errors": 1,
    "by_type": {
      "grammar": 1
    }
  }
}
```

## Common Examples

### Polish Grammar Check

```python
# Check Polish text
result = await check_grammar("On poszedł do sklep.")
# Returns: Error "do sklep" should be "do sklepu" (dopełniacz)

# Check correct Polish text
result = await check_grammar("Ala ma kota.")
# Returns: No errors found
```

### English Grammar Check

```python
# Check English text
result = await check_grammar("This are a test.", "en-US")
# Returns: 2 errors - "This" should be "These", "are" should be "is"

# Check correct English
result = await check_grammar("These are tests.", "en-US")
# Returns: No errors found
```

### Different Text Types

```python
# Formal email
check_grammar("Szanowny Panie, przesyłam wymagane dokumenty.", "pl-PL")

# Technical documentation
check_grammar("System supports multiple languages including Polish and English.", "en-US")

# Casual message
check_grammar("Hej, co robisz wieczorem?", "pl-PL")
```

## Best Practices

**When calling the tool:**
1. Always provide the full text, not just snippets
2. Use the appropriate language code for non-Polish text
3. Don't break text into artificial sentences - provide natural paragraphs
4. Include punctuation marks for better context

**When interpreting results:**
1. `total_errors: 0` means the text is grammatically correct
2. Check `issueType` to understand error category:
   - `grammar` - Grammar mistakes
   - `spelling` - Spelling errors
   - `style` - Style suggestions
3. Use `replacements` array for suggested corrections
4. Consider `shortMessage` for quick error overview
5. Use `message` for detailed explanations

**When fixing errors:**
1. Present errors to user with context and suggestions
2. Don't auto-fix without user confirmation
3. Consider the context - some suggestions may not fit the intended meaning
4. Prioritize grammar and spelling errors over style suggestions
5. Explain the error in the target language when possible

## Error Types Explained

### Grammar Errors
- Incorrect verb forms, conjugations
- Wrong case usage (Polish: mianownik, dopełniacz, etc.)
- Subject-verb agreement issues
- Incorrect preposition usage

### Spelling Errors
- Typos and misspellings
- Capitalization errors
- Punctuation mistakes

### Style Suggestions
- Better word choices
- More formal/informal alternatives
- Clarity improvements

## Workflow Pattern

**Standard grammar check workflow:**
1. Receive text from user
2. Call `check_grammar()` with appropriate language
3. Parse results
4. Present errors clearly with context
5. Show replacement suggestions
6. Ask user if they want help implementing corrections

**Example interaction:**
```
User: "Check this Polish text: On poszedł do sklep."
Agent: [Calls check_grammar()]
Agent: "Found 1 grammar error:
       Error: 'do sklep' → should be 'do sklepu'
       Rule: Przyimek wymaga dopełniacza (preposition requires genitive case)
       Suggestion: Use 'do sklepu' instead of 'do sklep'"
```

## Limitations

**What the tool CAN do:**
- Detect grammar and spelling errors
- Provide replacement suggestions
- Support multiple languages
- Give detailed error explanations
- Work with various text types

**What the tool CANNOT do:**
- Understand context or intent
- Detect semantic errors (wrong meaning but correct grammar)
- Verify factual accuracy
- Handle code or technical syntax
- Process very long texts (consider breaking into chunks)

## Integration Notes

**Tool availability:**
- Available in MCP server: `check_grammar(text, language="pl-PL")`
- Service endpoint: `http://localhost:8082/v2/check`
- Requires: LanguageTool systemd service running on port 8082

**Service management:**
- Start: `sudo systemctl start languagetool`
- Stop: `sudo systemctl stop languagetool`
- Status: `sudo systemctl status languagetool`
- Restart: `sudo systemctl restart languagetool`

If service is not running, the tool will return an error message indicating the connection failed.

## Testing

**Verify tool availability:**
```python
# Quick test
result = await check_grammar("Test sentence.", "pl-PL")
print(result)
```

**Expected behavior:**
- Correct text: Returns `total_errors: 0`
- Incorrect text: Returns matches with suggestions
- Service down: Returns error message about connection failure

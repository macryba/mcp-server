# Grammar Check Command

Use the grammar checking tool when user asks to:
- Check, proofread, or improve Polish text
- Verify grammar, spelling, or style in any language
- Validate Polish/English documents, emails, or messages

## Tool Syntax

```python
check_grammar("text to check")
check_grammar("text to check", "language-code")
```

## Common Languages

- Polish: `"pl-PL"` (default)
- English US: `"en-US"`
- English GB: `"en-GB"`
- German: `"de-DE"`
- French: `"fr-FR"`

## Examples

```python
# Polish grammar check
await check_grammar("On poszedł do sklep.")  # Detects case error

# English grammar check
await check_grammar("This are a test.", "en-US")  # Detects 2 errors

# Correct text
await check_grammar("Ala ma kota.")  # No errors found
```

## Return Format

Tool returns JSON with:
- `matches` - Array of grammar errors with suggestions
- `language` - Detected language info
- `summary` - Error count by type (grammar/spelling/style)

For detailed instructions, see: `ai-instructions/grammar-check-instructions.md`

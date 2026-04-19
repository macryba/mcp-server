# Commit Message Guidelines

## Format

```
<type>(<scope>): <subject>

<body (optional)>

read daily log work-log/YYYY-MM-DD.md item XX for details
```

**IMPORTANT:** Always include the daily log footer. Replace `YYYY-MM-DD` with today's date and `XX` with the item number from the daily log.

## Types

- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructuring
- `docs`: Documentation changes
- `chore`: Build/deps/tooling
- `test`: Test changes
- `perf`: Performance
- `style`: Code style only

## Rules

**Subject line (mandatory):**
- Imperative mood: "add" not "added", "fix" not "fixed"
- Max 72 characters
- Capitalize first letter
- No period at end
- Describe what and why, not how

**Body (use for complex changes):**
- Blank line after subject
- Wrap at 72 characters
- Use bullet points for multiple changes
- Explain reasoning
- **Max 5 lines total** (subject + body combined, excluding footer)

## Examples

✅ **Good:**
```
feat(wikipedia): add full article content extraction

Implement extract_article tool for complete Wikipedia articles with Polish
support, section parsing, and error handling for missing pages.

read daily log work-log/2026-04-19.md item 3 for details
```

✅ **Good:**
```
fix: polish character support in Wikipedia API responses

Force UTF-8 encoding in http_client for Polish characters (ą, ć, ę, ł, ń, ó, ś, ź, ż).

read daily log work-log/2026-04-19.md item 9 for details
```

❌ **Bad:**
```
fix: stuff
update things
feat: added new functionality.
fix: Fixed the bug
refactor: changed the code
```

## Checklist

- [ ] Starts with type (feat, fix, refactor, docs, chore)
- [ ] Subject ≤72 characters
- [ ] Imperative mood ("add" not "added")
- [ ] No period at end
- [ ] Max 5 lines (subject + body combined)
- [ ] Daily log footer included with correct date and item number
- [ ] No typos

## Language

**English commit messages only** - even though this is a Polish project.

✅ `feat: add Polish Wikipedia domain support`
✅ `fix: handle diacritics in Polish character encoding`

## Quick Template

```bash
git commit -m "type(scope): subject

Brief explanation of changes (max 4 lines)

read daily log work-log/YYYY-MM-DD.md item XX for details"
```

**Note:** Replace `YYYY-MM-DD` with today's date and `XX` with the item number from your daily log.

---

**Remember:** Commit messages are project documentation. Keep them clear and consistent.
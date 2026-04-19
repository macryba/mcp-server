# Commit Message Guidelines

## Format

```
<type>(<scope>): <subject>

<body>
```

**IMPORTANT:** No footers allowed. Do not include issue numbers, breaking change notices, or co-author tags. Keep commits to subject line only (and body if needed).

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
- **Max 10 lines total** (subject + body combined)

## Examples

✅ **Good:**
```
feat(wikipedia): add full article content extraction

Implement extract_article tool that retrieves complete Wikipedia article
content including sections and metadata. Handles Polish Wikipedia by default.

- Add extract_article() function in tools/extract.py
- Implement section parsing and content reconstruction
- Add error handling for missing pages
```

✅ **Good:**
```
fix: polish character support in Wikipedia API responses

Force UTF-8 encoding in http_client to properly handle Polish characters
(ą, ć, ę, ł, ń, ó, ś, ź, ż).
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
- [ ] Body included for complex changes
- [ ] No typos

## Language

**English commit messages only** - even though this is a Polish project.

✅ `feat: add Polish Wikipedia domain support`
✅ `fix: handle diacritics in Polish character encoding`

## Quick Template

```bash
git commit -m "type(scope): subject

- Change 1
- Change 2

Reasoning if needed"
```

---

**Remember:** Commit messages are project documentation. Keep them clear and consistent.
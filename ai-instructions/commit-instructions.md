# Commit Instructions

## File Staging Rules

**Stage files individually:**
```bash
git add path/to/file1.py
git add path/to/file2.js
git add docs/work/log/YYYY-MM-DD.md
```

**Critical:**
- Stage ONLY files from your conversation context
- Include deleted files: `git add <deleted-file-path>`
- NEVER use `git add .` or `git add -A`
- Multiple agents may work in parallel on same branch
- Do NOT ask permission to stage - do it automatically

---

## Commit Message Format

**Structure:** `type: short description`

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `refactor` - Code restructuring
- `test` - Test additions/changes
- `chore` - Maintenance tasks

**Rules:**
- Keep to 1-2 lines maximum
- First line: concise, direct (50-72 chars ideal)
- Optional second line: brief context if needed
- NO footers, NO signatures, NO attribution lines

---

## ⚠️ MUST NOT DO - Critical Rules

**NEVER include these in commit messages:**
- ❌ "Generated with Claude Code"
- ❌ "Co-Authored-By: Claude <noreply@anthropic.com>"
- ❌ "Co-Authored-By: Claude <any email>"
- ❌ Any AI tool attribution or branding
- ❌ URLs to AI tools or services
- ❌ Footer signatures of any kind

**WHY:** User uses z.AI models, NOT Anthropic. AI attribution is incorrect and unwanted.

**Violation examples (DO NOT USE):**
```
feat: add new feature

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Correct format:**
```
feat: add new feature

Implements user authentication and profile management
```

**Examples:**

Single line:
```
feat: test results modal
fix: site scraper validation
docs: design system modal patterns
```

Multi-line (when needed):
```
feat: implement search provider config system

Refactors site scraper config to use centralized search provider
definitions with template-based configuration
```

---

## Process Flow

This workflow is executed by the `/daily-log` command.

1. Stage files (automatic, no permission needed)
2. Generate commit message from work log title
3. Display summary: log entry + staged files + commit message
4. Ask: "Do you want to commit?"
5. If yes → commit | If no → leave files staged

**Note:** The Main Agent and Test Agent should ask "Do you want to run /daily-log? (Yes/No)" after completing work.
The actual commit happens within the `/daily-log` command execution.

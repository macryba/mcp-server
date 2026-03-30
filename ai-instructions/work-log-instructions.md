# Work Log Instructions

## Workflow

When `/daily-log` is executed:

1. **Analyze context** - Identify files created/modified in THIS conversation only
2. **Create/update log** - Write to `work-log/YYYY-MM-DD.md` using template below
3. **Stage files** - Run `git add` for each context file + log file (see commit-instruction.md)
4. **Generate commit** - Create message from work title (see commit-instruction.md) - NO Co-Authored-By footers
5. **Display summary** - Show: log entry, staged files, commit message
6. **Ask confirmation** - "Do you want to commit?" → Yes = commit, No = leave staged

**Critical:** Use conversation context for file detection, NOT `git status` (parallel sessions may exist)

---

## Daily Log Template

### File: `work-log/YYYY-MM-DD.md`

**First entry of day:**
```markdown
# YYYY-MM-DD - Work Session Log

## Work Completed

1. Work Title

---

## 1. Work Title

**Summary:** [2-3 sentences: Why needed, problem solved, goal achieved]

**Type:** `frontend` | `backend` | `infra` | `design-system` | `bugfix` | `docs`
**Scope:** `small` | `medium` | `large`
**Tokens:** Input: X | Output: Y | Total: Z
**Time:** Session: X min | Model: Y min

### What Changed
- ✅ Specific change with outcome
- ✅ Another change with impact

### Technical Approach
- **Architecture:** [Pattern/structure]
- **Key decisions:** [Important choices]
- **Integration:** [Connection points]

### Files Changed
**Added:**
- `path/to/new_file.py`

**Modified:**
- `path/to/existing_file.py`

**Deleted:**
- `path/to/removed_file.py`
```

**Subsequent entries:**
1. Read existing file
2. Count entries, use next number (N)
3. Add `N. Work Title` to "Work Completed" list (no blank line between items)
4. Append `---` separator
5. Append `## N. Work Title` with full entry
6. DO NOT modify existing entries

---

## Metadata Reference

### Type
- `frontend` - UI/UX, templates, CSS, JavaScript, design system
- `backend` - Models, views, business logic, APIs, services
- `infra` - DevOps, deployment, CI/CD, environment config
- `design-system` - Design system docs, component library, patterns
- `bugfix` - Bug fixes, error corrections, validation fixes
- `docs` - Documentation updates, README changes, guides

### Scope
- `small` - Single file or minor change, <2 hours, <50 lines
- `medium` - Multiple files or moderate complexity, 2-6 hours, 50-200 lines
- `large` - Significant feature or refactoring, >6 hours, >200 lines

### Token & Time
- **Session time:** Total time including human review/testing
- **Model time:** AI processing time only
- Use session summary if available, estimate otherwise
- Track THIS session only (not cumulative)

### Technical Approach Variations
- **Features:** Architecture, key decisions, integration
- **Bug fixes:** Root cause, solution, prevention
- **Refactoring:** Before, after, benefits
- **Documentation:** Focus area, additions, removals

---

## Quality Checklist

### ✅ Required
- Numbered entries (1., 2., 3...) in both header and body
- All 4 metadata fields (Type, Scope, Tokens, Time)
- Summary explains WHY and GOAL (2-3 sentences)
- High-level technical approach (details in git diff)
- File paths only in "Files Changed" section
- Checkmarks (✅) for "What Changed" items
- Files grouped by Added/Modified/Deleted

### ❌ Prohibited
- Skipping entry numbers
- Omitting metadata
- Verbose technical explanations
- File path descriptions or line counts
- Vague titles (be specific)
- Modifying existing entries
- Using `git status` or `git add .`

---

## Example Entry

```markdown
# 2026-01-08 - Work Session Log

## Work Completed

1. Test Results Modal Implementation

---

## 1. Test Results Modal Implementation

**Summary:** Product testing results were displayed inline, making the page cluttered and non-interactive. Implemented a reusable modal system to show test results in a clean, accessible overlay. Goal was to improve UX and create reusable modal pattern for other features.

**Type:** `frontend`
**Scope:** `medium`
**Tokens:** Input: 4,200 | Output: 1,600 | Total: 5,800
**Time:** Session: 35 min | Model: 10 min

### What Changed
- ✅ Created reusable modal component with backdrop, header, scrollable body, and multiple close methods
- ✅ Added auto-initialization for static modals and `ModalUtils` API for AJAX-injected modals
- ✅ Refactored site_detail.html to use AJAX form submission with loading states
- ✅ Removed 120 lines of inline HTML test results display

### Technical Approach
- **Pattern:** IIFE module with global utils exposure for dynamic use
- **Features:** Close on ESC/overlay click, auto-init on DOMContentLoaded, exposed API for AJAX
- **Integration:** Global script in base.html, modal partial templates included as needed

### Files Changed
**Added:**
- `static/js/modal.js`
- `templates/jobs/partials/site_test_results_modal.html`

**Modified:**
- `templates/base.html`
- `templates/jobs/site_detail.html`
- `apps/jobs/views.py`
```

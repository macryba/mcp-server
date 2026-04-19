# TODO - Next Session Issues and Improvements

## Summary Status

**✅ COMPLETED:**
- Extended `extract_article` tool to support all 7 Polish history domains
- Fixed English Wikipedia removal (Polish-only service)
- Fixed Dzieje.pl service (title extraction, content extraction, relevance filtering)
- Generated test files: `jadwiga-wikipedia-pl.md` (3,845 words) and `jadwiga-dzieje.md` (744 words)

**⚠️ IN PROGRESS / NEEDS FIXING:**
- IPN Edukacja service has significant issues with search and content discovery

---

## Current Issues Found

### 1. IPN Edukacja Service - CRITICAL ISSUES

**Problem:** IPN service cannot find or extract content effectively

**Root Causes Identified:**

1. **Search Functionality Broken**
   - IPN uses POST forms for search → automated searching returns limited/no results
   - Search for "Solidarność" (core 20th century topic) returns no results
   - Site structure appears to have changed significantly

2. **Content Discovery Issues**
   - Main materials page (`/edu/materialy-edukacyjne`) is navigation-only, not content listing
   - No direct content items found on expected pages
   - Site uses complex JavaScript/interactive elements that may not be accessible via simple HTTP requests

3. **Wrong Scope Expectations**
   - IPN specializes in 20th century history (1939-1990)
   - Medieval topics like Jadwiga Andegaweńska are outside scope
   - Service needs better scope documentation

**Evidence:**
- Materials page shows navigation categories, not actual materials
- Found 25 "potential content links" but no actual content items
- "Solidarność" not found on main materials page
- Site uses complex class structure (column, competion-grid, mediumelement-bg, etc.)

**Next Steps to Fix:**

1. **Investigate IPN Site Structure**
   ```bash
   # Try accessing these sections:
   https://edukacja.ipn.gov.pl/edu/lekcje-i-warsztaty
   https://edukacja.ipn.gov.pl/edu/konkursy-i-projekty
   https://edukacja.ipn.gov.pl/edu/rajdy-i-zajecia-terenowe
   ```

2. **Find Working IPN Content**
   - Look for actual lesson/material pages (not navigation)
   - Try different URL patterns for IPN content
   - Check if IPN content is accessible via direct URLs

3. **Alternative Approaches**
   - Check if IPN has RSS feeds or sitemaps
   - Look for API endpoints (may exist but not documented)
   - Consider if IPN should be marked as "limited functionality" domain

4. **Update Service Documentation**
   - Clearly document IPN's 20th century focus
   - Warn about search limitations
   - Provide examples of working direct URLs

---

### 2. Other Domain Services - NEED TESTING

**Status:** Not yet tested with actual content extraction

**Domains to Test:**
- Polona (digital library) - has API, should work better
- SuperKid (educational) - limited search functionality expected
- Przystanek Historia (IPN portal) - 20th century focus, similar issues to IPN
- GWO (educational materials) - not tested yet

**Testing Approach:**
```bash
# For each domain:
1. Search for domain-appropriate topic
2. Test extraction from found URLs
3. Generate test file: tests/data/{topic}-{domain}.md
4. Document any issues found
```

**Suggested Test Topics:**
- Polona: "Warsaw Uprising photographs" or historical documents
- SuperKid: "powstania warszawskie" (school level)
- Przystanek Historia: "Solidarność" or "II wojna światowa"
- GWO: "II wojna światowa" (teaching materials)

---

## Technical Issues Found

### 1. HTTP Client Redirect Issues
- **Problem:** IPN URLs causing "Exceeded maximum allowed redirects"
- **Impact:** Cannot access many IPN pages directly
- **Potential Fix:** Configure HTTP client to handle redirects better or increase redirect limit

### 2. JavaScript-Heavy Sites
- **Problem:** Some modern educational sites may use JavaScript for content loading
- **Impact:** Simple HTTP requests may not get full content
- **Potential Fix:** May need headless browser or API access for some domains

### 3. Content Quality Filtering
- **Problem:** Search returns irrelevant results (Dzieje.pl, IPN)
- **Current Solution:** Basic text matching for relevance
- **Improvement Needed:** Better relevance scoring and filtering

---

## Recommended Next Steps

### Priority 1: Fix IPN Service
1. Explore IPN site structure manually to find working content URLs
2. Update IPN service to work with actual site structure
3. Test with "Solidarność" content to generate `solidarnosc-ipn.md`
4. Document IPN limitations clearly

### Priority 2: Test Remaining Domains
1. Test Polona (likely to work well - has official API)
2. Test SuperKid, Przystanek Historia, GWO
3. Generate test files for working domains
4. Document issues for problematic domains

### Priority 3: Improve Search Quality
1. Implement better relevance scoring
2. Add fallback search strategies
3. Consider implementing domain-specific search optimizations

### Priority 4: Documentation
1. Update CLAUDE.md with domain-specific limitations
2. Add troubleshooting guide for each domain
3. Document which domains work best for which time periods/topics

---

## Files Modified This Session

- ✅ `tools/extract.py` - Multi-domain routing, removed English Wikipedia
- ✅ `services/domains/dzieje.py` - Fixed title extraction, content extraction
- ✅ `services/domains/ipn.py` - Improved but still needs work
- ✅ `server.py` - Updated documentation, removed English references
- ✅ `tests/data/jadwiga-wikipedia-pl.md` - 3,845 words, working
- ✅ `tests/data/jadwiga-dzieje.md` - 744 words, working

## Files Still Needed

- ⚠️ `tests/data/solidarnosc-ipn.md` - BLOCKED by IPN service issues
- ⚠️ Test files for: Polona, SuperKid, Przystanek Historia, GWO

---

## Key Learnings

1. **Domain Specialization Matters:**
   - IPN = 20th century only
   - Wikipedia = general knowledge but works well
   - Dzieje.pl = popular history but search is broken

2. **Direct URLs Work Better Than Search:**
   - `https://dzieje.pl/postacie/jadwiga-andegawenska` ✅
   - Search for same topic ❌

3. **Site Structure Complexity:**
   - Modern educational sites use navigation pages, not content listings
   - May need manual exploration to find working content URLs
   - JavaScript/interactive elements may block simple HTTP access

---

## Session Statistics

- **Domains Implemented:** 7
- **Domains Fully Tested:** 2 (Wikipedia, Dzieje)
- **Domains Partially Working:** 1 (IPN - extraction works, search broken)
- **Domains Untested:** 4 (Polona, SuperKid, Przystanek Historia, GWO)
- **Test Files Generated:** 2
- **Bugs Fixed:** 3 (English Wikipedia removal, Dzieje title extraction, Dzieje content extraction)
- **Bugs Remaining:** Multiple (IPN search, content discovery for several domains)

---

## Commands for Next Session

```bash
# Continue IPN investigation
python -c "
import asyncio
from services.http_client import HTTPClient
http_client = HTTPClient()
response = await http_client.get('https://edukacja.ipn.gov.pl/edu/lekcje-i-warsztaty')
# Analyze response for actual content
"

# Test remaining domains
python -c "
from tools.search import search_polish_history
from tools.extract import extract_article
# Test Polona, SuperKid, etc.
"

# Generate missing test files
# Once working URLs are found for each domain
```

---

**Status:** Ready for next session - IPN service is the main blocker
**Estimated Time:** 1-2 hours to fix IPN and test remaining domains
**Success Criteria:** All 7 domains have working extraction with test files
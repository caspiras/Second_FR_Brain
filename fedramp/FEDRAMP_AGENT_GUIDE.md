# FedRAMP Rev5 Documentation Monitor - Agent Instructions

**🚨 CRITICAL: READ THIS FIRST WHEN STARTING ANY NEW SESSION**

## Mandatory First Steps for Every Agent Session

**Before doing ANYTHING else, you MUST:**

1. **Check the current date/time:**
   ```bash
   date -u +"%Y-%m-%dT%H%M%SZ"
   ```
   - Understand what TODAY is (e.g., if it's April 10th 2026, then today is April 10th)
   - DO NOT assume the date or act like it's a different day

2. **Read the specification file:**
   ```
   Read: /Users/christopherjcosby/Projects/claude-projects/git-projects/fr_scraper/spec.md
   ```
   - This contains ALL operational guidelines
   - Read it completely before answering user questions

3. **Read the latest snapshot baseline:**
   ```
   Read: /Users/christopherjcosby/Projects/claude-projects/git-projects/fr_scraper/snapshots/latest.json
   ```
   - This tells you the baseline directory to compare against
   - This tells you when the last check was performed

## What This Project Does

This project monitors TWO FedRAMP websites for changes:
1. **https://www.fedramp.gov/docs/rev5/** (Rev5 Documentation - 40-50+ pages)
2. **https://www.fedramp.gov/notices/** (Public Notices - single page)

## When User Asks About Changes

When the user asks ANY variation of "what has changed?" or "check for changes":

**🚨 YOU MUST DO A COMPLETE SITE SCRAPE - NOT JUST COMPARE FILES**

### Step-by-Step Process:

1. **Get current date/time** (see step 1 above)

2. **Load the baseline** from `snapshots/latest.json`:
   - Get the `baseline_directory` field
   - This is the previous snapshot you'll compare against
   - Example: `2026-04-09T151318Z-update`

3. **Create a NEW snapshot** with CURRENT timestamp:
   - Directory: `snapshots/YYYY-MM-DDTHHMMSSZ-update/`
   - Use the timestamp from step 1

4. **Crawl BOTH websites COMPLETELY**:
   - **Rev5 Docs**: Start at https://www.fedramp.gov/docs/rev5/
     - Extract all links under `/docs/rev5/`
     - Fetch EVERY page (40-50+ pages)
     - Save each page as `.html` file in snapshot directory
   - **Notices**: Fetch https://www.fedramp.gov/notices/
     - Extract all notice entries
     - Include in `_meta.json`

5. **Compare** new snapshot vs baseline snapshot:
   - Page count changes
   - New pages added
   - Pages removed
   - Content changes in existing pages
   - New notices added

6. **Update** `snapshots/latest.json`:
   - Set `baseline_directory` to your NEW snapshot
   - Set `checked_at` to current timestamp
   - Set page/notice counts
   - Set notes describing changes

7. **Report** findings to user:
   - "Changes since [baseline date] ([X days] ago)"
   - List specific pages that changed
   - List new notices
   - Be explicit about the temporal gap

## What NOT to Do

**❌ NEVER do these when asked about changes:**
- Run `git log` or `git status`
- Report on spec.md file changes
- Report on this repository's files
- Just compare files without crawling the website
- Use old snapshots without creating a new one
- Skip updating `latest.json`
- Act like today is a different date

**❌ NEVER just compare previously fetched files:**
- You MUST fetch fresh content from BOTH websites
- You MUST create a new timestamped snapshot
- You MUST do a complete crawl every time

## Critical Rules

### Rule 1: Check Current Date FIRST
Always run `date -u` before doing anything. Know what day TODAY is.

### Rule 2: Create NEW Snapshot Every Time
Never compare old snapshots without creating a new one with current data.

### Rule 3: Crawl BOTH Websites Completely
- ALL pages under /docs/rev5/ (40-50+ pages)
- The /notices/ page

### Rule 4: Update latest.json Every Time
After creating a new snapshot, ALWAYS update `snapshots/latest.json` to point to it.

### Rule 5: Report Temporal Context
Always say "Changes since [date] ([X days/hours] ago)" to make the time gap clear.

## Example Correct Workflow

```
User: "What has changed?"

Agent:
1. Runs: date -u → "2026-04-10T16:15:18Z" (understands today is April 10th)
2. Reads: snapshots/latest.json → baseline is "2026-04-09T151318Z-update" (April 9th)
3. Calculates: Today (April 10th) - Baseline (April 9th) = 1 day ago
4. Creates: snapshots/2026-04-10T161518Z-update/
5. Crawls: All pages from BOTH websites (fresh fetch from fedramp.gov)
6. Compares: New snapshot vs April 9th baseline
7. Updates: snapshots/latest.json → points to April 10th snapshot
8. Reports: "Changes since April 9th at 3:13 PM (1 day ago): [changes found]"
```

## Example WRONG Workflow (Don't Do This)

```
User: "What has changed?"

Agent:
❌ Doesn't check current date
❌ Assumes today is April 9th when it's actually April 10th
❌ Compares files already in snapshots/ directory without fetching new content
❌ Doesn't create a new snapshot
❌ Doesn't update latest.json
❌ Reports changes without temporal context
```

## File Locations

- Spec file: `/Users/christopherjcosby/Projects/claude-projects/git-projects/fr_scraper/spec.md`
- Latest pointer: `/Users/christopherjcosby/Projects/claude-projects/git-projects/fr_scraper/snapshots/latest.json`
- Snapshots: `/Users/christopherjcosby/Projects/claude-projects/git-projects/fr_scraper/snapshots/YYYY-MM-DDTHHMMSSZ-update/`

## Summary

**When user asks about changes:**
1. ✅ Check current date
2. ✅ Read spec.md and latest.json
3. ✅ Create NEW snapshot with CURRENT timestamp
4. ✅ Fetch fresh content from BOTH websites
5. ✅ Compare new vs baseline
6. ✅ Update latest.json
7. ✅ Report with temporal context

**DO NOT:**
- ❌ Skip checking current date
- ❌ Compare old files without new fetch
- ❌ Forget to update latest.json
- ❌ Report without temporal context

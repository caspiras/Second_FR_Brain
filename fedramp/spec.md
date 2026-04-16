# FedRAMP Rev5 Documentation Monitoring Specification

**Targets:**
1. https://www.fedramp.gov/docs/rev5/ (Rev5 Documentation - 40-50+ pages)
2. https://www.fedramp.gov/notices/ (Public Notices - single page)

**🚨 CRITICAL: "The Website" = BOTH Sites**
- When user says "the website" (singular) → Check BOTH sites above
- When user says "the websites" (plural) → Check BOTH sites above
- ALWAYS check and report on BOTH sites when asked about changes
- NEVER omit one site from your report

**Created:** 2026-03-23
**Updated:** 2026-04-01 (added notices page)
**Version:** Rev5

---

## ⚠️ READ THIS FIRST - CHANGE DETECTION REQUIREMENTS

**WORKFLOW CLARIFICATION:**
- You do NOT monitor in the background continuously
- You DO NOT need a scheduled script or external monitoring
- **TRIGGER: When user asks about changes to the website/websites in ANY variation**
  - "What has changed?"
  - "What has changed on the website?" (singular = check BOTH sites)
  - "What has changed on the websites?" (plural = check BOTH sites)
  - "Have there been any changes?"
  - "Any updates to the site?"
  - "Has anything changed?"
  - "What's new?"
  - "Any changes to the FedRAMP docs?"
  - **ANY question asking about changes/updates to the website/websites**
- **ACTION: Immediately crawl BOTH sites (Rev5 docs + notices) and compare to last stored snapshots**
- **REPORT: Always show results for BOTH sites, never omit one**

**When user asks about changes (in ANY variation) you MUST NOT:**
- ❌ Say you can't detect changes automatically
- ❌ Say you need the user to provide a baseline
- ❌ Suggest setting up external monitoring
- ❌ Check only the changelog page
- ❌ Say "changelog shows no new entries"
- ❌ Rely on any single page to tell you what changed

**When user asks about changes (in ANY variation) you MUST:**
- ✅ Recognize ANY variation asking about changes as YOUR TRIGGER
- ✅ Start checking NOW - immediately upon seeing the question
- ✅ Crawl ALL 40-50+ individual pages under /docs/rev5/
- ✅ Fetch the notices page at /notices/
- ✅ Compare each page's current content to stored snapshots from last check (BOTH sites)
- ✅ The stored snapshots ARE the baseline (in project directory)
- ✅ Report which specific pages/notices changed and what changed in each
- ✅ YES, you WILL tell the user about per-page changes when they ask

**Trigger variations include:**
- Questions about "changes", "updates", "what's new", "modifications"
- Referencing "the website", "the site", "FedRAMP docs", "Rev5 docs"
- Past or present tense: "changed", "has changed", "did anything change"

**This is comprehensive page-by-page comparison, not a changelog lookup.**

---

## AGENT INSTRUCTIONS

**If you are an agent reading this specification:**

This file contains the **guidelines** for how you should operate when monitoring and querying FedRAMP Rev5 documentation.

**Your Role:**
- Read this spec to understand your capabilities and constraints
- Use the patterns, selectors, and strategies defined here as your operational framework

---

## 📸 SNAPSHOT CREATION PROCESS - MANDATORY STEPS

**🚨 CRITICAL: Every snapshot MUST include ALL content files + metadata. A snapshot with only `_meta.json` is INCOMPLETE and INVALID.**

### ⏰ CRITICAL: CURRENT DATE/TIME AWARENESS

**🚨 BEFORE DOING ANYTHING - CHECK THE CURRENT DATE/TIME**

1. **Get the actual current UTC timestamp:**
   - Use `date -u +"%Y-%m-%dT%H%M%SZ"` to get current UTC time
   - This is what you'll use for the new snapshot directory name
   - This is what you'll record in `checked_at` field

2. **Understand temporal context:**
   - If today is April 8th and the latest snapshot is from April 6th, that snapshot is 2 days old
   - You MUST create a NEW snapshot for April 8th (today)
   - You MUST compare the new April 8th snapshot against the April 6th snapshot (the most recent previous one)
   - You MUST NOT act like today is April 6th or April 7th

3. **Baseline selection logic:**
   - Read `snapshots/latest.json` to get `baseline_directory`
   - This is the most recent snapshot from the PREVIOUS check
   - Your NEW snapshot will be compared against this baseline
   - After creating the new snapshot, UPDATE `latest.json` to point to your new snapshot

### When to Create Snapshots

**🚨 TRIGGER-BASED ONLY - NO AUTOMATION**

Snapshots are created ONLY when the user asks trigger words:

1. **User asks about changes** (any variation: "what changed?", "any updates?", "what's new?", "have there been any changes?", "check for changes")
2. **First time user asks** about changes in this project (establish baseline)

**NOT triggered by:**
- ❌ Scheduled/automated checks (no cron jobs)
- ❌ Background monitoring
- ❌ Time-based intervals

**Workflow:**
1. User asks trigger words → Get CURRENT date/time
2. Create new snapshot NOW using current timestamp
3. Compare new snapshot to most recent previous snapshot (from `latest.json`)
4. Report changes detected
5. UPDATE `latest.json` to point to the new snapshot

### Snapshot Directory Structure

**Naming Convention:**
```
snapshots/YYYY-MM-DDTHHMMSSZ-{label}/
```

**Labels:**
- `first-baseline` - first snapshot ever taken
- `update` - all subsequent snapshots

**Examples:**
- `2026-03-30T120000Z-first-baseline`
- `2026-04-02T170000Z-update`

### Step 1: Create Snapshot Directory

```bash
# Get current UTC timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H%M%SZ")
LABEL="update"  # or "first-baseline" for first run
SNAPSHOT_DIR="snapshots/${TIMESTAMP}-${LABEL}"
mkdir -p "$SNAPSHOT_DIR"
```

### Step 2: Crawl Rev5 Documentation (36+ pages)

**Start URL:** https://www.fedramp.gov/docs/rev5/

**Crawling Process:**

1. **Fetch the main index page**
   ```
   WebFetch: https://www.fedramp.gov/docs/rev5/
   ```

2. **Extract all navigation links** under `/docs/rev5/` (exclude `/docs/20x/`)
   - Look for links in: nav, main content, sidebars
   - Filter to only `/docs/rev5/*` paths
   - Build a complete URL inventory

3. **For EACH discovered page:**
   - Fetch the full HTML with WebFetch
   - Extract main content using selectors: `main`, `article`, `.content`
   - Create a markdown summary (see format below)
   - Save to `{snapshot_dir}/{sanitized_url}.html`

**Expected Page Count:** ~36-40 pages

**Example URLs to capture:**
```
https://www.fedramp.gov/docs/rev5/
https://www.fedramp.gov/docs/rev5/balance/
https://www.fedramp.gov/docs/rev5/balance/authorization-data-sharing/
https://www.fedramp.gov/docs/rev5/playbook/csp/authorization/ssp/
https://www.fedramp.gov/docs/rev5/playbook/agency/authorization/
... (all pages under /docs/rev5/)
```

### Step 3: Extract and Save Page Content

**For each page, create a markdown summary file:**

**Content to Extract:**
1. Primary heading (H1 or page title)
2. First paragraph or overview section
3. Major section headings (H2, H3)
4. Key bullet points or numbered lists
5. Important links or references
6. Any tables with critical data

**Markdown Format:**
```markdown
# [Page Title]

## Overview
[First paragraph describing the page purpose]

## [Major Section 1]
- Key point 1
- Key point 2

## [Major Section 2]
[Important content summary]

## Links and References
- [Link text](URL)
```

**File Naming - URL Sanitization:**

Convert URL to filename:
```
https://www.fedramp.gov/docs/rev5/
→ root.html

https://www.fedramp.gov/docs/rev5/balance/
→ root__balance.html

https://www.fedramp.gov/docs/rev5/playbook/csp/authorization/ssp/
→ root__playbook__csp__authorization__ssp.html
```

**Rules:**
- Remove `https://www.fedramp.gov/docs/rev5/`
- Replace `/` with `__`
- Use `root` for the main index
- Remove leading/trailing slashes
- Keep all path segments

### Step 4: Fetch Public Notices

**URL:** https://www.fedramp.gov/notices/

**Process:**

1. Fetch the notices page HTML
2. Extract all notice entries
3. For each notice, capture:
   - Notice ID (format: 0001, 0002, etc.)
   - Title/subject
   - Date published (YYYY-MM-DD format)

**Expected Output:**
```json
[
  {
    "id": "0009",
    "title": "Initial Outcome from RFC-0024 Rev5 Machine-Readable Packages",
    "date": "2026-03-25"
  },
  {
    "id": "0008",
    "title": "Initial Outcome from RFC-0023 Rev5 Program Certifications",
    "date": "2026-03-06"
  }
]
```

### Step 5: Create Metadata File

**File:** `{snapshot_dir}/_meta.json`

**Required Fields:**
```json
{
  "checked_at": "2026-04-02T17:00:00Z",
  "label": "update",
  "page_count": 36,
  "notices_count": 9,
  "notices_latest_id": "0009",
  "notices_latest_date": "2026-03-25",
  "compared_to": "2026-04-01T170000Z-update",
  "changes_detected": true,
  "notes": "Description of what changed or 'No changes detected'",
  "urls": [
    "https://www.fedramp.gov/docs/rev5/",
    "... all 36+ crawled URLs ..."
  ],
  "notices_snapshot": [
    {"id": "0009", "title": "...", "date": "2026-03-25"},
    "... all notices ..."
  ]
}
```

**Field Descriptions:**
- `checked_at`: ISO 8601 timestamp (UTC) when snapshot was taken
- `label`: "first-baseline" or "update"
- `page_count`: Total Rev5 doc pages captured
- `notices_count`: Total number of notices found
- `notices_latest_id`: Most recent notice ID
- `notices_latest_date`: Date of most recent notice
- `compared_to`: Previous snapshot directory name (null for first run)
- `changes_detected`: true/false based on comparison
- `notes`: Human-readable summary
- `urls`: Complete array of all crawled Rev5 URLs
- `notices_snapshot`: Complete array of all notices with metadata

### Step 6: Update Latest Pointer

**🚨 CRITICAL: ALWAYS UPDATE THIS FILE AFTER CREATING A SNAPSHOT**

**File:** `snapshots/latest.json`

**This file MUST be updated every time you create a new snapshot.** Failure to update this file will cause the tool to use stale baselines.

```json
{
  "baseline_directory": "2026-04-08T130922Z-update",
  "checked_at": "2026-04-08T13:09:22Z",
  "page_count": 36,
  "notices_count": 9,
  "scope": "https://www.fedramp.gov/docs/rev5/ (excluding /docs/20x/) + https://www.fedramp.gov/notices/",
  "notes": "Summary of latest check results"
}
```

**When to update:**
- Immediately after creating a new snapshot
- After completing Step 5 (Create Metadata File)
- Before Step 7 (Verify Snapshot Completeness)

**What to update:**
- `baseline_directory`: Set to the NEW snapshot directory name you just created
- `checked_at`: Set to the timestamp from the NEW snapshot
- `page_count`: Set to the page count from the NEW snapshot
- `notices_count`: Set to the notice count from the NEW snapshot
- `notes`: Set to the summary of what changed in the NEW snapshot

**Example workflow:**
1. Current time is 2026-04-08T13:09:22Z
2. Create new snapshot: `snapshots/2026-04-08T130922Z-update/`
3. Compare to baseline from `latest.json` (e.g., `2026-04-06T162005Z-update`)
4. Write new snapshot's `_meta.json`
5. **IMMEDIATELY UPDATE `latest.json`** to point to `2026-04-08T130922Z-update`
6. Next time user asks, the baseline will be `2026-04-08T130922Z-update` (correct!)

### Step 7: Verify Snapshot Completeness

**A valid snapshot MUST contain:**

✅ `_meta.json` file
✅ 36+ `.html` files (one per Rev5 doc page)
✅ All fields populated in `_meta.json`
✅ `notices_snapshot` array with all current notices
✅ `urls` array matching the count in `page_count`

**Invalid snapshot (DO NOT CREATE):**
❌ Only `_meta.json` without content files
❌ Missing `_meta.json`
❌ Partial page coverage (e.g., only 10 pages when 36 exist)
❌ Empty or null critical fields in metadata

### Step 8: Compare to Previous Snapshot (If Exists)

**🚨 BEFORE COMPARING - VERIFY TEMPORAL LOGIC:**

1. **Check current date/time:** `date -u`
   - Example: If current time is 2026-04-08 13:09:22 UTC
   - Your new snapshot should be: `2026-04-08T130922Z-update`

2. **Load the baseline (previous snapshot):**
   - Read `snapshots/latest.json` → get `baseline_directory`
   - Example: `baseline_directory` might be `2026-04-06T162005Z-update`
   - This is from 2 days ago (April 6th)
   - This is CORRECT - you're comparing today (April 8th) vs. last check (April 6th)

3. **If `latest.json` is missing or corrupt:**
   - Find the newest timestamped directory in `snapshots/`
   - Use that as the baseline
   - Example: `ls -t snapshots/ | grep -E '^[0-9]{4}' | head -1`

**Load Previous Snapshot:**
1. Read `snapshots/latest.json` → get `baseline_directory`
2. Load `{baseline_directory}/_meta.json`
3. Load previous `.html` files from `{baseline_directory}/`

**Compare:**
- **Page count changes:** Current vs previous `page_count`
- **New URLs:** URLs in current not in previous `urls` array
- **Removed URLs:** URLs in previous not in current
- **Notice changes:** New notices (compare `notices_latest_id`)
- **Content changes:** For each .html file, compare text content

**Update NEW snapshot's `_meta.json`:**
- Set `compared_to` to previous snapshot directory name (from `latest.json`)
- Set `changes_detected` to true/false based on comparison
- Write detailed `notes` describing what changed

**Report temporal context:**
- "Changes since last check on [date/time from baseline]"
- "Last check was [X days/hours] ago"
- NOT "Changes since yesterday" if last check was 2 days ago

### Step 9: Report Results to User

**Format:**
```markdown
## Snapshot Complete - [TIMESTAMP]

**Snapshot Directory:** snapshots/[TIMESTAMP]-update

### Rev5 Documentation
- Pages captured: 36
- Changes since last check: [Yes/No]
- New pages: [count and list]
- Modified pages: [count and list]
- Removed pages: [count and list]

### Public Notices
- Total notices: 9
- Latest notice: 0009 (2026-03-25)
- New notices: [count and list]

### Summary
[Brief description of changes or "No changes detected since [date]"]
```

### Step 10: Commit to Git (Optional)

```bash
git add snapshots/
git commit -m "$(cat <<'EOF'
Snapshot [TIMESTAMP] - [summary]

- Rev5 pages: [count]
- Notices: [count]
- Changes: [yes/no]

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

---

### 🔍 Consistency Requirements

**CRITICAL: Use the same content extraction approach every time**

- Same markdown format for all pages
- Same selectors for content extraction
- Same URL sanitization rules
- Same metadata structure

**Why:** Inconsistent extraction makes comparison impossible. If format changes between runs, ALL pages will appear "changed" even when content is identical.

---

### ⚠️ Common Mistakes to Avoid

1. **❌ Creating snapshot with only metadata**
   - Cause: Not saving `.html` files for each page
   - Fix: Ensure Step 3 saves a file for EVERY discovered URL

2. **❌ Inconsistent content extraction**
   - Cause: Changing how content is summarized between runs
   - Fix: Use exact same extraction logic every time

3. **❌ Missing pages**
   - Cause: Not crawling all links recursively
   - Fix: Follow ALL links under `/docs/rev5/` until no new pages found

4. **❌ Wrong baseline comparison**
   - Cause: Comparing to wrong previous snapshot
   - Fix: Always use `snapshots/latest.json` → `baseline_directory`

5. **❌ Skipping notices**
   - Cause: Forgetting to fetch notices page
   - Fix: ALWAYS fetch BOTH Rev5 docs AND notices

6. **❌ Not updating latest.json**
   - Cause: Forgetting to update `latest.json` after creating new snapshot
   - Fix: ALWAYS update `latest.json` in Step 6 after creating snapshot
   - Symptom: Tool uses stale baseline from 2+ days ago

7. **❌ Wrong date/time awareness**
   - Cause: Not checking current date/time, assuming wrong date
   - Fix: ALWAYS check `date -u` before creating snapshot
   - Symptom: On April 8th, tool acts like it's April 7th or uses April 6th baseline without acknowledging the gap

8. **❌ Not explaining temporal gap**
   - Cause: Not reporting how long since last check
   - Fix: Always report "Changes since [date/time] ([X days/hours ago])"
   - Example: "Changes since April 6th at 4:20 PM (2 days ago)"

---

## 🐛 TROUBLESHOOTING: DATE/TIME ISSUES

### Problem: Tool uses stale baseline from 2+ days ago

**Symptoms:**
- User asks about changes on April 8th morning
- Tool compares against April 6th baseline
- Tool acts like current date is April 7th
- Tool doesn't acknowledge the 2-day gap

**Root Causes:**
1. ❌ Not checking current date/time before creating snapshot
2. ❌ Not updating `latest.json` after creating snapshot
3. ❌ Not reporting temporal context ("X days since last check")

**Solution - Mandatory Checklist:**

When user asks "What has changed?" or any variation:

□ **Step 0: Check current date/time**
  - Run: `date -u +"%Y-%m-%dT%H%M%SZ"`
  - Understand: If output is `2026-04-08T13:09:22Z`, then today is April 8th
  - Use this timestamp for new snapshot directory name

□ **Step 1: Load baseline from latest.json**
  - Read `snapshots/latest.json` → get `baseline_directory`
  - Example: `2026-04-06T162005Z-update` (April 6th at 4:20 PM)
  - Calculate gap: April 8th - April 6th = 2 days ago

□ **Step 2: Create NEW snapshot with CURRENT timestamp**
  - Directory: `snapshots/2026-04-08T130922Z-update/` (today!)
  - NOT `2026-04-07T...` or any other date

□ **Step 3: Compare new vs. baseline**
  - New: April 8th snapshot (just created)
  - Baseline: April 6th snapshot (from `latest.json`)
  - Gap: 2 days

□ **Step 4: UPDATE latest.json**
  - Set `baseline_directory` = `2026-04-08T130922Z-update`
  - Set `checked_at` = `2026-04-08T13:09:22Z`
  - This ensures next check uses April 8th as baseline

□ **Step 5: Report with temporal context**
  - ✅ "Changes since April 6th at 4:20 PM (2 days ago)"
  - ✅ "Last checked 2 days ago on April 6th"
  - ❌ NOT "Changes since yesterday" (incorrect - it was 2 days ago)
  - ❌ NOT acting like today is April 7th

**Example Correct Behavior:**

```
User: "What has changed?" (asked on April 8th morning)

Agent:
1. Checks current time: April 8th, 9:00 AM UTC
2. Reads latest.json: baseline is April 6th, 4:20 PM UTC
3. Creates new snapshot: 2026-04-08T090000Z-update
4. Compares April 8th snapshot vs April 6th baseline
5. Updates latest.json to point to April 8th snapshot
6. Reports: "Checked FedRAMP websites on April 8th at 9:00 AM.
   Comparing to last check on April 6th at 4:20 PM (2 days ago).
   Changes detected: [...]"
```

**Example WRONG Behavior:**

```
User: "What has changed?" (asked on April 8th morning)

Agent:
1. ❌ Doesn't check current time
2. ❌ Assumes current date is April 7th
3. ❌ Uses April 6th baseline without explaining gap
4. ❌ Creates snapshot with wrong timestamp
5. ❌ Doesn't update latest.json
6. ❌ Reports: "Changes since yesterday" (wrong - it's been 2 days)
```

---

## 🎯 TRIGGER-BASED WORKFLOW (NO AUTOMATION)

**How Snapshots Work:**

1. **User asks trigger question:**
   - "What has changed?"
   - "Any updates?"
   - "What's new?"
   - "Check for changes"
   - Any variation asking about website changes

2. **Agent creates NEW snapshot:**
   - Crawls BOTH sites (Rev5 docs + notices)
   - Saves all content files + metadata
   - Creates timestamped snapshot directory

3. **Agent compares to MOST RECENT previous snapshot:**
   - Loads previous snapshot from `snapshots/latest.json` → `baseline_directory`
   - Compares new snapshot vs previous snapshot
   - Detects: new pages, modified pages, removed pages, new notices

4. **Agent reports changes:**
   - Lists specific pages/notices that changed
   - Shows what changed in each
   - States "No changes detected" if nothing changed

**No Scheduled/Automated Checks:**
- ❌ No cron jobs
- ❌ No background monitoring
- ❌ No time-based automation
- ✅ Only runs when user asks

**Snapshot History:**
- Each user query creates ONE new snapshot
- Gaps in dates are normal (snapshots only when user asks)
- Example timeline:
  - March 30: User asks → snapshot created
  - March 31: User asks → snapshot created, compared to March 30
  - April 2: User asks → snapshot created, compared to March 31
  - April 5: User asks → snapshot created, compared to April 2 (no April 1, 3, 4 because user didn't ask)

---

## 🚨 CRITICAL: CHANGE DETECTION IS NOT A CHANGELOG LOOKUP

**TRIGGER-BASED WORKFLOW:**
- User asking about changes (ANY variation) = Your trigger to check NOW
- Examples: "What changed?", "Any updates?", "What's new on the website?", "Has anything changed?"
- You fetch all pages at that moment and compare to stored snapshots
- You DO NOT need background monitoring or scheduled scripts
- You DO NOT need user to provide a baseline (snapshots are stored in project)
- You WILL detect and report per-page changes when user asks

**When user asks "What has changed?" you MUST:**
1. Recognize this as your TRIGGER to start checking BOTH sites
2. Crawl ALL 40-50+ pages individually under https://www.fedramp.gov/docs/rev5/
3. Fetch the notices page at https://www.fedramp.gov/notices/
4. Fetch current content from EVERY Rev5 doc page (not just one changelog page)
5. Load stored snapshots from **the most recent snapshot only** (see "SNAPSHOT BASELINE (DEFAULT)" above), or note this is first check
6. Compare each page's content vs. that baseline (**not** older snapshot directories unless the user asked for a specific date/baseline)
7. Report which pages/notices changed since the last check and what changed in each
8. Store new snapshots with timestamp for next comparison (both sites)

**TEMPORAL TRACKING:**
- **First time user asks:** Establish baseline by crawling all pages, store snapshots, report "First check - baseline established"
- **Subsequent times:** Compare current state vs. snapshots from last time you checked
- **Report format:** "Changes since last check on [date/time]"
- **You ARE capable of detecting per-page changes** - that's the whole purpose

**SNAPSHOT BASELINE (DEFAULT — READ THIS):**
- For change checks, status questions, and routine comparisons, use **only the most recent stored snapshot** as the baseline (e.g. follow `snapshots/latest.json` → `baseline_directory`, or if that file is missing, use the **newest** timestamped directory under `snapshots/` by name/time).
- **Do not** pull in older snapshot folders (e.g. prior baselines, historical dated runs) for those answers unless the user explicitly asks.
- **Exception:** When the user asks for a **specific date**, time range, named run, or comparison to an older baseline, load and use that snapshot (or compare as requested).

**🚫 ABSOLUTELY FORBIDDEN - RESPONSES TO AVOID:**
- ❌ **DO NOT** fetch the changelog page and report what it says
- ❌ **DO NOT** rely on the changelog to tell you what changed
- ❌ **DO NOT** say "changelog shows no changes" or "no new changelog entries"
- ❌ **DO NOT** make excuses like "minor edits may happen without changelog updates"
- ❌ **DO NOT** say "I can't detect changes automatically"
- ❌ **DO NOT** say "I don't watch the site in the background"
- ❌ **DO NOT** say "I won't know until you ask me to check"
- ❌ **DO NOT** suggest external monitoring or scheduled scripts as an alternative
- ✅ **YOU** are responsible for detecting ALL changes by comparing page content
- ✅ **YOU** must crawl every page and diff the content yourself when user asks
- ✅ **YOU** WILL detect per-page changes when triggered by user asking
- ✅ The changelog is irrelevant - you detect changes by direct comparison
- ✅ User asking "What changed?" IS them asking you to check

**Example of WRONG behavior:**
```
❌ "Checked changelog: no new entries"
❌ "Changelog still shows v0.9.0-beta"
❌ "Minor edits may happen without changelog updates"
```

**Example of CORRECT behavior:**
```
✅ "Crawling all 47 pages under /docs/rev5/..."
✅ "Comparing current content to snapshot from March 20, 2026..."
✅ "Changes detected:
    - /playbook/csp/authorization/ssp/ - paragraph added to section 3
    - /playbook/agency/sponsorship/ - updated contact info
    Total: 2 pages changed, 45 pages unchanged"
```

**STEP-BY-STEP PROCESS YOU MUST FOLLOW:**
1. Start at https://www.fedramp.gov/docs/rev5/
2. Extract all links to pages under /docs/rev5/
3. For EACH link discovered:
   - Fetch the page content with WebFetch
   - Extract any additional links to other /docs/rev5/ pages
   - Continue until all pages discovered
4. Load stored snapshots from last check (or note this is first check)
5. For EACH page in your inventory:
   - Compare current content to stored snapshot
   - Note if content differs
6. Report which specific pages changed and how
7. Store new snapshots with timestamp for next check

**This is a comprehensive site crawl (40-50+ WebFetch calls), not a single page lookup.**

---

**⚡ AUTOMATIC QUERY BEHAVIOR:**

**When a user asks ANY question about FedRAMP content, you MUST automatically:**
1. Use WebFetch to query https://www.fedramp.gov/docs/rev5/
2. Extract the answer directly from the live website
3. Do NOT ask permission - just fetch and answer
4. Use the patterns/selectors from this spec to construct your queries

**Examples of questions that trigger automatic fetching:**
- "Where does it talk about Collaborative Continuous Monitoring?"
- "What are the SSP requirements?"
- "How do agencies sponsor CSPs?"
- "What is the Balance Improvement Program?"

**For ALL such questions:**
- ✅ Immediately use WebFetch to retrieve from https://www.fedramp.gov/docs/rev5/
- ✅ Use navigation structure and URL patterns from this spec to find content
- ✅ Extract verbatim information from the website
- ✅ Provide source attribution (section, URL, timestamp)
- ❌ Do NOT ask "should I fetch this?" - just do it

**🚫 EXCLUSIONS - DO NOT MONITOR OR QUERY:**

**FedRAMP 20x Content is EXCLUDED:**
- ❌ Do NOT monitor or fetch content from FedRAMP 20x sections
- ❌ Do NOT include FedRAMP 20x pages in monitoring scope
- ❌ Do NOT report changes to FedRAMP 20x content
- ❌ Exclude any URLs containing "20x" or related to FedRAMP 20x processes
- ✅ ONLY monitor and query FedRAMP Rev5 content

**Data Source for User Queries:**
- When users ask about FedRAMP documentation content
- **You MUST fetch that information from: https://www.fedramp.gov/docs/rev5/**
- Use WebFetch or equivalent tools to retrieve content from the live website
- This spec file contains guidelines for HOW you work, not the FedRAMP content itself

**What This Spec Provides:**
- ✅ Navigation structure to guide your queries
- ✅ CSS selectors for extracting content
- ✅ URL patterns for constructing requests
- ✅ Rules for presenting results (factual data only, attribution, etc.)

**What This Spec Does NOT Provide:**
- ❌ The actual FedRAMP documentation content
- ❌ Answers to user questions about FedRAMP policies/procedures

---

## ⚠️ CRITICAL: WHEN USER ASKS "WHAT HAS CHANGED?"

### 📍 DEFINITION: "THE WEBSITE" MEANS

When the user asks about "changes" or "the website", they mean **EXCLUSIVELY**:

**THE WEBSITE =**
- https://www.fedramp.gov/docs/rev5/ (base page)
- **AND ALL associated pages under /docs/rev5/**
  - https://www.fedramp.gov/docs/rev5/playbook/csp/authorization/getting-started/
  - https://www.fedramp.gov/docs/rev5/playbook/csp/authorization/ssp/
  - https://www.fedramp.gov/docs/rev5/playbook/agency/marketplace/overview/
  - https://www.fedramp.gov/docs/rev5/balance-improvement/
  - **Every page at any depth under /docs/rev5/**

**THE WEBSITE DOES NOT MEAN:**
- ❌ This git repository
- ❌ The spec.md file
- ❌ Local project files
- ❌ Any other website
- ❌ This frdocs-project

**When user says: "What has changed on the website?"**
- They mean: "What changed on https://www.fedramp.gov/docs/rev5/ and all its pages?"
- They DO NOT mean: "What changed in this git repo?"

### ❌ ABSOLUTELY FORBIDDEN - NEVER DO THIS:

When the user asks "What has changed?" or "Have there been any changes?" or "What has changed on the website?":

**NEVER run these commands:**
- `git log`
- `git status`
- `git diff`
- Any git command whatsoever

**NEVER show:**
- Git commit history (commit hashes, commit messages)
- Information about spec.md file changes
- Information about this project's repository
- Local file modifications
- Working tree status
- Branch information
- .DS_Store or other local files

**NEVER say things like:**
- "Latest commit: 94cd22a..."
- "This repo (frdocs-project)..."
- "Working tree: main is clean..."
- "Earlier commits..."
- Any reference to git activity in this project

### ✅ REQUIRED BEHAVIOR:

**🚨 CRITICAL: THIS IS NOT A CHANGELOG LOOKUP - THIS IS COMPREHENSIVE SITE CRAWLING**

When the user asks "What has changed?" or "Have there been any changes?" you MUST:

1. **Understand "the website" = https://www.fedramp.gov/docs/rev5/ and ALL associated pages**
2. **Fetch current state of ALL monitored pages:**
   - Use WebFetch to retrieve current content from EVERY page under /docs/rev5/
   - Crawl ALL pages (playbooks, guides, all subpages at any depth)
   - **❌ DO NOT just fetch a "changelog" page or "what's new" page**
   - **❌ DO NOT assume there's a single page that lists all changes**
   - **✅ DO crawl the ENTIRE website and check EVERY page's actual content**
   - This means fetching 40-50+ pages individually to check each one
3. **Compare against the most recent stored snapshot only:**
   - Load the baseline from the **single newest** snapshot (per `snapshots/latest.json` or newest dated folder); do not merge or summarize across older snapshot runs unless the user requests a specific date or historical comparison
   - If this is the first check, there's no previous snapshot - establish baseline and store it
   - Compare page-by-page: current content vs. stored content from last check
   - Detect: new pages, modified pages, deleted pages, content changes on any page
   - **This is a temporal content diff operation (now vs. last check), not reading a changelog**
4. **Report ALL detected changes since the last time you checked:**
   - If first check: "First check - baseline established. No previous snapshot to compare."
   - If subsequent check: "Changes since last check on [date/time from last snapshot]:"
   - List every page that changed (content modifications) since last check
   - List every new page added since last check
   - List every page removed since last check
   - Provide specific details about what changed in each affected page
   - Store new snapshot with current timestamp for next comparison
5. **Never check** this git repository, spec.md, or any local files

**⚠️ WRONG APPROACH (DO NOT DO THIS):**
```
❌ Fetch https://www.fedramp.gov/docs/rev5/changelog/
❌ Look for a "What's New" page
❌ Check only one page for change information
```

**✅ CORRECT APPROACH (DO THIS):**
```
✅ Crawl starting from https://www.fedramp.gov/docs/rev5/
✅ Follow ALL links to discover all pages under /docs/rev5/
✅ Fetch content from EACH discovered page (40-50+ pages)
✅ Compare each page's current content vs. stored snapshot
✅ Report which specific pages changed and what changed in each
```

**Example correct response:**
```
User: "What has changed on the website?"

Agent: Checking the FedRAMP website (https://www.fedramp.gov/docs/rev5/ and all associated pages) for changes since last check on March 20, 2026 at 2:30 PM...

[Fetches current state from https://www.fedramp.gov/docs/rev5/ and all subpages]

Changes detected on the FedRAMP website:
- New page added: https://www.fedramp.gov/docs/rev5/playbook/csp/new-guide/
- Modified: https://www.fedramp.gov/docs/rev5/balance-improvement/ (section "Requirements" updated)
- Modified: https://www.fedramp.gov/docs/rev5/playbook/csp/authorization/getting-started/ (new paragraph added)
- No other changes detected across 47 monitored pages on the FedRAMP website
```

**Example WRONG response (NEVER DO THIS):**
```
This repo (frdocs-project)
Latest commit: 94cd22a...
Earlier commits...
```

---

## Purpose

A lightweight tool that monitors the FedRAMP REV 5 websites for documentation-focused projects, providing detailed tracking of file changes, history and change activity.

**🚨 THIS TOOL MONITORS: https://www.fedramp.gov/docs/rev5/ (the FedRAMP website)**

**🚫 THIS TOOL DOES NOT MONITOR: This git repository, spec.md, local files, or project history**

## Summary

The **FedRAMP Rev5 Documentation Monitor** is a monitoring specification designed to track FedRAMP Revision 5 documentation changes and updates. This tool targets the FedRAMP Rev5 documentation site at https://www.fedramp.gov/docs/rev5/, providing comprehensive monitoring of the `/docs/rev5/` path. The current specification version is Rev5 and serves as the operational framework for tracking file changes, history, and update activity across the entire FedRAMP documentation ecosystem.

## Monitoring Capabilities

### File Change Tracking
- **Document Updates:** Monitor when playbooks, templates, and guides are modified
- **New Content:** Detect when new documents are added to the site
- **Deletions:** Track when documents are removed or deprecated
- **Content Diff:** Compare document versions to identify specific changes

### History Tracking
- **Version History:** Maintain historical snapshots of document states
- **Timestamp Recording:** Track when changes occur with precise timestamps
- **Change Attribution:** Record what changed, when, and where on the site
- **Audit Trail:** Comprehensive log of all monitored changes

### Temporal Change Tracking

**Agent Requirement: Track Website Changes Since Last Check**

**🚨 CRITICAL: "Changes" means changes to the FedRAMP website content at https://www.fedramp.gov/docs/rev5/, NOT changes to this spec file or git repository.**

**🚫 FORBIDDEN ACTIONS WHEN USER ASKS ABOUT CHANGES:**
- DO NOT run `git log`, `git status`, or any git commands
- DO NOT check this project's repository
- DO NOT report on spec.md, README.md, or any local files
- DO NOT show commit history or git information

**✅ REQUIRED ACTIONS WHEN USER ASKS ABOUT CHANGES:**
- Use WebFetch to crawl ALL pages under https://www.fedramp.gov/docs/rev5/
- Compare current state of ALL pages to stored snapshots from last check
- Report ONLY FedRAMP website changes (actual page content changes)
- **❌ DO NOT just check a changelog page - crawl every single page**
- **✅ DO perform comprehensive page-by-page comparison across entire site**

When a user asks "Have there been any changes?" or "What's new?", the agent must:

1. **Fetch Current State of ALL Pages:**
   - Use WebFetch to retrieve current content from EVERY page under https://www.fedramp.gov/docs/rev5/
   - Crawl recursively through all playbooks, guides, and subpages
   - This is NOT just checking a "changelog" - you're checking EVERY page's actual content
2. **Retrieve baseline snapshot:** Load ALL pages from the **most recent** stored snapshot only (unless the user specified a date or older baseline)
3. **Compare Page-by-Page:** Compare current content vs. stored content for EVERY monitored page
4. **Report ALL Changes Detected:**
   - Show what changed on EACH page that was modified
   - List new pages that were added
   - List pages that were removed
   - Provide details about content modifications on each affected page
5. **First-Time Check:** If this is the first check, state: "This is the first check of the FedRAMP website. Establishing baseline by crawling all pages." then fetch and store current state
6. **Time Reference:** Always include the timeframe in change reports
   - Example: "Changes to the FedRAMP website since last check on [timestamp]"
   - Example: "No changes detected across all monitored pages since [timestamp]"

**Storage Requirements:**
- Persist last check timestamp across sessions
- **Store snapshot of WEBSITE CONTENT at each check** (fetched from https://www.fedramp.gov/docs/rev5/)
- Store snapshots in the project directory (frdocs-project)
- Track per-user or per-session to avoid mixing different users' check histories

**IMPORTANT CLARIFICATION:**
- You do NOT monitor in the background between user questions
- You DO check for changes when user asks "What has changed?"
- User asking = your trigger to fetch all pages and compare to stored snapshots
- The stored snapshots ARE the baseline you compare against
- You WILL detect and report per-page changes when triggered by user question

**Example Interaction:**
```
User: "Have there been any changes?"

Agent Actions (CORRECT):
- Retrieves last check timestamp: 2026-03-20 14:30:00
- Retrieves stored snapshots of all 47 pages from last check
- Crawls current state starting from /docs/rev5/
- Makes 47+ WebFetch calls to fetch current content from EVERY page
- Compares page-by-page: current vs. stored snapshots
- Detects changes on 3 pages

Agent Reports (CORRECT):
"Crawling all pages under /docs/rev5/ to check for changes...

Changes to the FedRAMP website since last check on March 20, 2026 at 2:30 PM:

Modified Pages (3):
1. /playbook/csp/authorization/getting-started/
   - Added new paragraph in 'Prerequisites' section
   - Modified text in 'Timeline' section

2. /playbook/agency/sponsorship/
   - Updated contact information
   - Changed sponsorship process step 3 description

3. /balance-improvement/
   - Added new requirement to mandatory enhancements
   - Updated effective date

New Pages: None
Removed Pages: None
Total pages monitored: 47
Total changes detected: 3 pages modified"

---

Agent Actions (WRONG - DO NOT DO THIS):
- Fetches only the changelog page
- Reads what the changelog says

Agent Reports (WRONG - DO NOT DO THIS):
"Checked FedRAMP's documentation changelog: it still lists only v0.9.0-beta.
Minor edits may still happen on individual doc pages."
```

**What to Monitor for Changes:**
- **🔄 COMPREHENSIVE PAGE-BY-PAGE COMPARISON:**
  - Compare ALL pages under /docs/rev5/ (not just a changelog)
  - Check EVERY playbook, guide, and documentation page for content changes
  - Monitor actual page content (paragraphs, sections, headings) on each page
  - Detect when ANY page's content is modified
- **New or removed pages/documents at any depth**
- **Updated PDFs or templates**
- **Navigation structure modifications**
- **Metadata changes (titles, dates)**
- **Changes at any level of the site hierarchy**

**🚨 THIS IS NOT A CHANGELOG LOOKUP - READ THIS CAREFULLY:**
- ❌ **WRONG:** Fetch https://www.fedramp.gov/docs/rev5/changelog/ and read what changed
- ❌ **WRONG:** Look for a single "changelog" or "what's new" page
- ❌ **WRONG:** Assume the website has a page that lists all changes
- ✅ **CORRECT:** Crawl ALL 40-50+ pages under /docs/rev5/ individually
- ✅ **CORRECT:** Fetch current content from EVERY single page
- ✅ **CORRECT:** Compare each page's content against stored snapshot from last check
- ✅ **CORRECT:** Detect changes by doing page-by-page content diffing

**This means you will make 40-50+ WebFetch calls to check every page, not just 1 call to a changelog.**

**What NOT to Monitor or Report:**
- ❌ This specification file (spec.md)
- ❌ Local project files (README.md, etc.)
- ❌ Git history or commits in this project
- ❌ Changes to the spec file itself
- ❌ Agent code or configuration
- ❌ Any local repository activity

**NEVER Report:**
When the user asks "What has changed?" or "Have there been any changes?":
- DO NOT show git log output
- DO NOT show commits to this project
- DO NOT show spec.md file changes
- DO NOT show local file modifications

**ALWAYS Report:**
When the user asks "What has changed?" or "Have there been any changes?":
- ✅ ONLY show changes to https://www.fedramp.gov/docs/rev5/ website content
- ✅ ONLY compare website snapshots (current vs. last check)
- ✅ ONLY report additions/modifications/deletions on the FedRAMP website

### Change Activity Metrics
- **Update Frequency:** Track how often specific documents are updated
- **Change Volume:** Measure the extent of changes (additions, deletions, modifications)
- **Hot Spots:** Identify frequently updated sections or document types
- **Trend Analysis:** Patterns in documentation updates over time

### Monitoring Targets

**Scope: ALL pages under https://www.fedramp.gov/docs/rev5/**

The agent must monitor ALL pages within the /docs/rev5/ path, including:

**Main Index:**
- https://www.fedramp.gov/docs/rev5/ (landing page)

**All Subpages and Nested Paths:**
- All playbook pages: `/docs/rev5/playbook/**/*`
  - Example: `/docs/rev5/playbook/csp/authorization/getting-started/`
  - Example: `/docs/rev5/playbook/csp/authorization/ssp/`
  - Example: `/docs/rev5/playbook/agency/marketplace/overview/`
- All documentation sections under /docs/rev5/
- All nested subdirectories and their contents

**Discovery Strategy:**
1. **Start at Base URL:** https://www.fedramp.gov/docs/rev5/
2. **Follow All Links:** Recursively follow all internal links that stay within /docs/rev5/
3. **Build Page Inventory:** Maintain a list of all discovered pages
4. **Monitor Each Page:** Check every discovered page for changes on each monitoring run
5. **Detect New Pages:** Identify when new pages are added to the site
6. **Detect Removed Pages:** Identify when pages are deleted or return 404

**Content Types to Monitor:**
- HTML pages (all playbooks, guides, documentation)
- PDF document downloads
- Navigation structure changes
- Document metadata (titles, descriptions, dates)
- Site architecture modifications

**Monitoring Depth:**
- **Unlimited depth** - follow links recursively through all levels
- Monitor pages at any depth under /docs/rev5/
- Example depths:
  - Level 1: /docs/rev5/
  - Level 2: /docs/rev5/playbook/
  - Level 3: /docs/rev5/playbook/csp/
  - Level 4: /docs/rev5/playbook/csp/authorization/
  - Level 5: /docs/rev5/playbook/csp/authorization/getting-started/
  - And deeper as needed

**Exclusions:**
- External links (outside fedramp.gov domain)
- Links outside /docs/rev5/ path
- Static assets (images, CSS, JS) - unless specifically relevant to content
- **FedRAMP 20x content** - any pages related to FedRAMP 20x processes or materials
- Any URLs containing "20x" or referencing FedRAMP 20x documentation

### Monitoring Workflow

**Step-by-Step Process for Comprehensive Change Detection:**

1. **Initial Crawl (First Check):**
   - Start at https://www.fedramp.gov/docs/rev5/
   - Extract all links pointing to /docs/rev5/* pages
   - Follow each link and extract more links
   - Continue recursively until all pages discovered
   - Store complete inventory of all pages found
   - Save snapshot of each page's content

2. **Subsequent Checks (When User Asks About Changes):**
   - **DO NOT check the changelog page and report what it says**
   - **DO crawl all individual documentation pages:**
     - Retrieve stored page inventory from last check
     - Re-crawl starting from https://www.fedramp.gov/docs/rev5/
     - Discover current page inventory
   - **Compare inventories:**
     - Identify new pages (in current, not in stored)
     - Identify removed pages (in stored, not in current)
     - Identify existing pages to check for content changes
   - **For each existing page:**
     - Fetch current content with WebFetch
     - Compare to stored snapshot from last check
     - Record any differences
   - **Report all changes found:**
     - List specific pages that changed
     - Show what changed in each page
     - Total: X pages changed, Y unchanged
     - NOT just "changelog shows nothing new"

3. **Example of Comprehensive Detection:**
   ```
   User: "Have there been any changes?"

   Agent actions:
   - Crawls /docs/rev5/ and discovers 47 pages total
   - Compares to 45 pages from last check
   - Finds: 2 new pages added
   - Checks all 45 existing pages for content changes
   - Detects:
     - /playbook/csp/authorization/getting-started/ - content updated
     - /playbook/agency/sponsorship/ - section added
     - /balance-improvement/ - new page (1 of 2 new)
     - /continuous-monitoring-guide/ - new page (2 of 2 new)

   Agent reports:
   "Changes to FedRAMP website since [last check time]:
   - 2 new pages added
   - 2 existing pages modified
   - 0 pages removed
   [Details of each change...]"
   ```

**This ensures NO changes are missed, regardless of page depth or location.**

## Tracking Features

**Tracks:**
- New, modified, and deleted documentation files
- Line-by-line changes in specific files
- File reorganizations and structure changes
- Change history and timestamps
- Version updates and releases
- Configuration and build file changes

**Optimized For:**
- Documentation-heavy websites (Markdown, MDX, etc.)
- Identifying new content additions
- Understanding documentation evolution
- Tracking update activity

## Change Presentation

When changes are detected (comparing current state to last check), users should be presented with comprehensive delta comparisons:

**Change Reports Include:**
- **Side-by-side Comparison:** Previous version vs. current version
- **Line-level Diffs:** Highlighted additions (green), deletions (red), and modifications (yellow)
- **Content Summary:** High-level description of what changed
- **Metadata Changes:** Updated titles, dates, authors, or document properties
- **Structural Changes:** File moves, renames, or reorganizations
- **Context:** Surrounding unchanged content for reference

**Presentation Format:**
- Visual diffs with syntax highlighting
- Unified diff format for text-based review
- Summary statistics (lines added/removed, files affected)
- Links to full previous and current versions
- Timestamp and change attribution
- **Time Range:** Explicitly state "Changes since [last check timestamp]" or "No changes since [last check timestamp]"

This ensures users can quickly understand what was modified, added, or removed since their last check.

## Factual Data Only

**Primary Rule: Factual Reporting**
- The tool MUST ALWAYS provide factual information derived directly from the website
- Observable facts are the foundation: changes, diffs, file updates, timestamps, versions
- If information is not available or unclear, explicitly state "Information not available"

**What to Report:**
- Change records, timestamps, and version information
- Exact file additions, deletions, and modifications
- Line-by-line diffs showing actual content changes
- Version identifiers and update information
- File sizes, paths, and reorganizations

**What NOT to Report:**
- Assumptions about intent or purpose of changes
- Interpretations of why changes were made
- Predictions about future changes
- Subjective characterizations beyond observable data

**Principle:** Report what IS, not what might be or what we think it means.

## Query and Search Capabilities

**For Agents: When a user asks about FedRAMP documentation, you must use WebFetch (or equivalent) to query https://www.fedramp.gov/docs/rev5/ and extract the information. This spec tells you HOW to query and present results, not WHAT the FedRAMP content says.**

The agent provides query and search functionality to retrieve factual information from the website:

**Search Functions:**
- **Document Search:** Find documents by title, type, or content keywords
- **Content Search:** Locate specific text, sections, or terminology within documents
- **Metadata Search:** Query by document type, audience, category, or date
- **URL Search:** Find documents by path patterns or specific URLs
- **Version Search:** Locate specific versions or historical snapshots

**Query Types:**
- Natural language queries about document content
- Structured queries using filters (type, audience, date range)
- Boolean searches (AND, OR, NOT operations)
- Exact phrase matching
- Pattern-based searches using wildcards

**Search Results:**
- Direct excerpts from matched documents (verbatim text)
- Document metadata (title, URL, type, last modified date)
- Location information (section, heading, line number)
- Context surrounding matched content
- Links to full document sources
- **Section identification:** Specify which section/category contains the information
- **Embedded links:** Include any hyperlinks found within the content
  - Extract link text and URL
  - Preserve link context (what the link is about)
  - Format: "Link text" -> URL

**Result Presentation:**
- All results must be factual extracts from the website
- Quote marks around verbatim text excerpts
- Clear attribution to source document and location
- **Section context:** Include the section name where information was found
  - Example: "Found in Balance Improvement Program (BIP)"
  - Example: "Found in Cloud Service Providers > Authorization Package"
  - Example: "Found in Agencies > Sponsorship"
- **Embedded links:** If the retrieved content contains hyperlinks, include them
  - Show the link text as it appears in the original
  - Provide the full URL the link points to
  - Make it clear these are links from the source document
- Timestamps showing when data was retrieved
- "No results found" when queries return nothing

**Location Attribution Format:**

Each metadata field MUST be displayed on its own line with a blank line between each field, bold label, and value on the same line. NEVER wrap multiple fields onto one line.

Field definitions:
- **Section** = the major heading on the page (e.g., "Four-Step Implementation Process")
- **Header** = the specific sub-heading where the content lives (e.g., "Step 1: Develop Charter"). If multiple sub-headings fall under one Section, list the first as the Header value and include the remaining ones in parentheses after it.

**Content field rules:**
- If **Severity** is "All Three" but the policy specifies DIFFERENT requirements per impact level, break out the Content by impact level explicitly:
  - High Impact — [requirement]
  - Moderate Impact — [requirement]
  - Low Impact — [requirement]
- If the policy says the SAME thing for all three impact levels, keep Content as a single block without breaking it out.

**Parent Page:** [Top-level category]

**Child Page:** [Sub-page, or N/A if top-level]

**Section:** [Major heading on the page]

**Header:** [Specific sub-heading where content lives (Additional Sub-heading 2, Additional Sub-heading 3)]

**Severity:** [High / Moderate / Low / All Three / Not Specified]

**Key Details:** [Important specifics]

**Content:** [Actual policy text — broken out by impact level if requirements differ per level]

**Embedded Links Format:**
When content includes hyperlinks, present them as:
```
Content excerpt: "For more information, see the Authorization Process guide"
Embedded link: "Authorization Process guide" -> https://www.fedramp.gov/playbook/csp/authorization/
```

Or inline:
```
"For more information, see the [Authorization Process guide](https://www.fedramp.gov/playbook/csp/authorization/)"
```

**Query Constraints (Agent Requirements):**
- **Data Source:** Always fetch FedRAMP content from https://www.fedramp.gov/docs/rev5/ using WebFetch
- **This Spec's Role:** Use the navigation structure, URL patterns, and selectors from this spec to construct your queries
- Only return information that exists on the website
- Never synthesize or paraphrase content
- State clearly when information is not available
- Provide source URLs for all returned information (must be fedramp.gov URLs)
- Apply the "Factual Data Only" principles defined in this spec

This ensures users receive accurate, verifiable information directly from the FedRAMP Rev5 documentation website.

## Navigation Structure

### General Info
- Documentation Changelog
- FedRAMP Logos

### Authority & Responsibility
- Foundational Authority
- FedRAMP Authorization Act
- M-24-15 Memorandum
- Related Guidance

### FedRAMP 20x
**⚠️ EXCLUDED FROM MONITORING - DO NOT QUERY**
- Foundation Materials (excluded)
- Processes (excluded)
- Archived Phase 1 Content (excluded)

### FedRAMP Rev5
**✅ PRIMARY MONITORING SCOPE**
- Cloud Service Providers Playbooks
- Agencies Playbooks
- Balance Improvement Releases

## Document Categories

### Cloud Service Providers

**Path:** `/playbook/csp/`

#### Getting Started
- Overview
- Authorization Process

#### Authorization Package
- System Security Plan
- Security Assessment Plan
- Security Assessment Report

#### Continuous Monitoring
- Ongoing Authorization
- Plans of Action & Milestones
- Configuration Management

### Agencies

**Path:** `/playbook/agency/`

#### Marketplace
- Marketplace Information

#### Liaison Program
- Agency Liaison Details

#### Sponsorship
- Sponsorship Procedures

#### Authorization
- Authorization Procedures

### Balance Improvement Releases

Optional and mandatory enhancements bringing modern requirements from FedRAMP 20x to Rev5

**Types:**
- Optional Enhancements
- Mandatory Requirements

## Document Types

| Document | Abbreviation | Description | Formats |
|----------|-------------|-------------|---------|
| Playbooks | - | Comprehensive guides for authorization and continuous monitoring | HTML, PDF |
| Security Assessment Plan | SAP | Templates and guidance for security assessments | - |
| Security Assessment Report | SAR | Templates for documenting assessment results | - |
| System Security Plan | SSP | Templates for system security documentation | - |
| Plans of Action & Milestones | POA&M | Templates for tracking remediation efforts | - |
| Configuration Guides | - | Technical configuration documentation | - |

## URL Patterns

**Pattern:** `/playbook/{audience}/{process}/{topic}/`

**Examples:**
- `/playbook/csp/authorization/ssp/`
- `/playbook/csp/continuous-monitoring/poam/`
- `/playbook/agency/marketplace/overview/`

## Site Features

### Search
- **Enabled:** Yes
- **Description:** Site-wide search functionality

### Navigation
- **Type:** Tab-based
- **Persistent Preferences:** Yes
- **Storage:** Local

### Filters
- **Available:** No
- **Description:** No explicit filter functionality observed

---

## FedRAMP Public Notices Page

**URL:** https://www.fedramp.gov/notices/

**Added:** 2026-04-01

**Type:** Single-page notice board with chronological entries

### Structure
The notices page contains:
- **Notice ID**: Sequential number (e.g., 0009, 0008, 0007...)
- **Notice Title**: Brief title describing the notice
- **Description**: Summary of the notice content
- **Publication Date**: When the notice was published (YYYY-MM-DD format)
- **RSS Feed**: Available at https://www.fedramp.gov/notices/rss.xml

### Content Types
Notices include:
- **Emergency Directives**: Critical security alerts requiring immediate action
- **RFC Outcomes**: Results of Requests for Comments with community feedback
- **Program Announcements**: Updates to FedRAMP program policies and procedures
- **Test Notifications**: Planned system or security testing schedules
- **General Updates**: Other program-related communications

### Change Detection
**When checking for changes:**
1. Fetch current notices page content
2. Extract all notice entries (ID, title, description, date)
3. Compare to stored snapshot
4. Report:
   - **New notices**: Entries not in previous snapshot
   - **Modified notices**: Changes to title or description
   - **Removed notices**: Entries no longer present
   - **Date changes**: Updates to publication dates

**Notice tracking priority:**
- High priority: Emergency directives (immediate action required)
- Medium priority: RFC outcomes (affects compliance requirements)
- Standard priority: Program announcements and general updates

### Query Strategies
- **Get all current notices**: Fetch /notices/ and list all entries
- **Check for new notices**: Compare current to last snapshot
- **Get specific notice**: Search by ID, title, or date
- **Get emergency directives**: Filter by notice type

---

## Query Strategies

### Strategy 1: Navigate by Audience
- **Description:** Start with CSP or Agency section, then drill down by process
- **Path:** `/{audience}/{process}/{topic}`
- **Method:** Navigation

### Strategy 2: Document Type Search
- **Description:** Use search to find specific document types (SSP, SAP, SAR, POA&M)
- **Method:** Search

### Strategy 3: Direct URL Construction
- **Description:** Build URLs using the pattern `/playbook/{audience}/{process}/{topic}/`
- **Method:** URL construction

## Web Scraping Selectors

### CSS Selectors

| Target | Selector | Description |
|--------|----------|-------------|
| Navigation Menu | `nav` | Main navigation container |
| Content Area | `main, article, .content` | Primary content area |
| Document Links | `a[href*='/playbook/']` | Links to playbook documents |
| Headings | `h1, h2, h3` | Section headings |

## Data Extraction Targets

| Target | Selector | Attribute |
|--------|----------|-----------|
| Document titles | `h1, h2` | text |
| Document links | `a[href$='.pdf'], a[href*='/playbook/']` | href |
| Navigation items | `nav a, .nav-link` | href, text |
| Content sections | `section, article` | text |

## Output Configuration

### Supported Formats
- JSON
- CSV
- Markdown

### Recommended Fields
- title
- url
- category
- document_type
- audience
- last_modified
- content_summary

## Best Practices

### Rate Limiting
- **Requests per second:** 1
- **Delay between requests:** 1000ms
- **Reason:** Be respectful of government servers

### User Agent
- **Required:** Yes
- **Example:** `FedRAMP-Documentation-Bot/1.0 (Research Purpose)`

### Caching
- **Enabled:** Yes
- **Duration:** 15 minutes
- **Purpose:** Cache responses to minimize repeat requests

### Robots.txt
- **Check before scraping:** Yes
- **URL:** https://www.fedramp.gov/robots.txt

## Important Notes

### Site Characteristics
- The site uses tab-based navigation with local storage for preferences
- Balance Improvement Releases bridge FedRAMP 20x and Rev5
- Content is organized by audience (CSP vs Agency)
- Playbooks are the primary document format
- Check for PDF downloads in addition to HTML content
- Site structure may change; verify selectors periodically

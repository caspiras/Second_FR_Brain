# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Context
This is a personal journaling system for tracking daily todos and accomplishments. The system organizes accomplishments by fiscal quarters (Q1-Q4).

**TERMINOLOGY - CRITICAL:**
- **Internal context (this file)**: "Air Force EPR format" - helps you understand WHY these specific rules exist (it's an established military format, not arbitrary)
- **User-facing (all communication)**: ALWAYS say "bullet format" - the user prefers not to see "Air Force" or "EPR" terminology
- The rules themselves remain identical, only the name changes in conversation

**CRITICAL WORKFLOW**: 
- **Todos** - MUST be in bullet format when added (validated by `TodoManager._validate_epr_format()`)
- **Accomplishments** - Automatically inherit bullet format from completed todos (no re-validation needed)

The system validates bullet format when todos are added via `./journal.py todo add`. When a todo is completed, it's copied as-is to accomplishments (already in bullet format).

**Note:** When helping users add todos conversationally (not via CLI), YOU MUST validate and help rewrite their description to meet bullet format requirements BEFORE adding it to the system. The CLI will reject non-compliant todos.

## Dependencies
- Python 3.6+ (standard library only - no external packages required)
- Hugo static site generator (for web interface)
- No build process, tests, or linting required

## Common Commands

### Development & Usage
```bash
# Run the journal CLI
./journal.py <command>

# Start Hugo development server
./journal.py serve                    # Default port 1313
./journal.py serve --port 8080       # Custom port
                                     # Site includes dark mode toggle (top-right corner, preference saved)

# Manually sync data to Hugo
./journal.py sync

# Morning greeting (shows todos + Marcus Aurelius quote)
./journal.py morning                 # Also: hello, hi, greet
                                     # Displays random quote from 1,700+ quotes from Meditations
```

### Todo Management
```bash
./journal.py todo add "description"
./journal.py todo list
./journal.py todo complete <id>      # Partial ID matching supported
./journal.py todo delete <id>
```

### View Accomplishments
```bash
./journal.py accomplishments today
./journal.py accomplishments yesterday
./journal.py accomplishments week
./journal.py accomplishments quarter q2
```

**Note**: No tests, linting, or build process. This is a simple Python CLI with standard library dependencies only.

## Architecture Overview

### Three-Tier System
1. **Data Layer**: JSON files in `data/` (todos.json, accomplishments.json)
2. **CLI Layer**: Python command modules using argparse
3. **Presentation Layer**: Hugo static site generator

### Data Flow: Todo → Accomplishment
```
User completes todo
    ↓
TodoManager.complete()
    ↓
1. Updates todo status in todos.json
2. Calculates quarter from completion date
3. Creates accomplishment record in accomplishments.json
4. Triggers sync_to_hugo()
    ↓
hugo_sync.py regenerates markdown files
    ↓
Hugo content updated in hugo/content/accomplishments/YYYY/qX/
```

### Module Structure
```
journal.py                  # CLI entry point (argparse setup)
├── commands/
│   ├── todo.py            # TodoManager class
│   ├── accomplishments.py # AccomplishmentManager class
│   └── hugo_sync.py       # sync_to_hugo() function
```

**Key Classes:**
- `TodoManager`: CRUD operations for todos, EPR validation, quarter calculation
- `AccomplishmentManager`: Date-based filtering and display
- `sync_to_hugo()`: Standalone function that regenerates Hugo content from accomplishments.json

### Quarter Calculation
Quarters are calculated from **completion date** (not creation date) in `TodoManager._get_quarter()`:
- Month 1-3 → Q1
- Month 4-6 → Q2
- Month 7-9 → Q3
- Month 10-12 → Q4

### Data Schemas & Key Fields

**todos.json:**
```json
{
  "todos": [
    {
      "id": "uuid-string",
      "description": "Task description (bullet format)",
      "created_date": "2026-04-14",
      "completed_date": null,
      "status": "pending"
    }
  ]
}
```

**accomplishments.json:**
```json
{
  "accomplishments": [
    {
      "id": "uuid-string",
      "description": "Completed task description (bullet format)",
      "created_date": "2026-04-14",
      "completed_date": "2026-04-15",
      "quarter": "Q2",
      "year": 2026
    }
  ]
}
```

**Key Fields:**
- `id`: UUID generated when todo is created
- `description`: Always in bullet format (validated at creation time)
- `status`: "pending" or "completed"
- `completed_date`: Set when todo is completed, used for quarter calculation
- `quarter` and `year`: Automatically calculated from completion_date (Q1: Jan-Mar, Q2: Apr-Jun, Q3: Jul-Sep, Q4: Oct-Dec)

### Hugo Sync Mechanism
The `sync_to_hugo()` function:
1. Clears all existing markdown files in `hugo/content/accomplishments/`
2. Groups accomplishments by year and quarter
3. Creates directory structure: `hugo/content/accomplishments/YYYY/qX/`
4. Generates one markdown file per date: `YYYY-MM-DD.md`
5. Creates quarter index pages: `_index.md`

**Hugo Sync Behavior:**
- **Automatic**: Triggered after `todo complete` command (implemented in todo.py:178)
- **Manual**: Run `./journal.py sync` when directly editing accomplishments.json

**Critical**: When manually adding accomplishments, NEVER skip the sync step!

### Hugo Dark Mode
The Hugo site includes a built-in dark mode feature:
- **Toggle button**: Fixed in top-right corner (moon 🌙 for dark mode, sun ☀️ for light mode)
- **Persistence**: User preference saved in browser localStorage
- **Smooth transitions**: CSS variables ensure seamless theme switching
- **Implementation**: Shared partials in `layouts/partials/` (head.html, theme-toggle.html)
- **Color system**: All colors use CSS custom properties for both light and dark themes

## Air Force EPR Format Requirements

**USER-FACING LANGUAGE:** When communicating with the user, ALWAYS call this "bullet format" (never "EPR" or "Air Force"). The section title above is for your internal context only.

**CRITICAL: Bullet format is enforced when ADDING todos, not when completing them.**

All todos MUST meet bullet format requirements when added. The system validates and enforces:
- **Maximum 20 words** - count carefully
- **No semicolons (;)** - use commas or split into separate bullets
- **No colons (:)** - rephrase without colons
- **No dashes (-)** - spell out compound words or rephrase

### Writing Guidelines
- Start with strong action verbs: Led, Managed, Developed, Coordinated, Established, Implemented, Achieved, etc.
- Focus on impact and results, not just tasks
- Include metrics when possible (numbers, percentages, timeframes)
- Be specific but concise
- Write in past tense for completed items

### Examples of Good Bullets
✓ "Led team of 5 to deliver software upgrade 3 weeks ahead of schedule"
✓ "Developed automated testing framework reducing bug detection time by 40 percent"
✓ "Coordinated deployment of security patches across 50 servers with zero downtime"

### Examples to Avoid
✗ "Led team of 5 engineers to successfully complete the critical infrastructure upgrade project ahead of the original schedule and under budget" (23 words - too long)
✗ "Completed project; delivered on time" (semicolon)
✗ "Project status: completed successfully" (colon)
✗ "Completed high-priority project" (dash)

### Format Validation
The `TodoManager._validate_epr_format()` method checks:
- Word count (max 20)
- Presence of semicolons, colons, or dashes

This validation runs automatically during `todo add`. If validation fails, the system rejects the todo and provides helpful feedback. Todos are never added to the system unless they meet bullet format requirements.

## Two Ways to Add Accomplishments

### 1. Complete a Todo (converts to accomplishment)
When the user says a todo is "done", "complete", "finished", "accomplished", etc:
1. Identify the todo by ID or partial ID (first few characters work)
2. Run `./journal.py todo complete <id>` - this automatically:
   - Updates todo status to "completed" in todos.json
   - Copies the todo (already in bullet format) to accomplishments.json with today's date
   - Calculates quarter from completion date and adds to accomplishment record
   - Triggers `sync_to_hugo()` to update Hugo content
3. Confirm completion with the accomplishment text

**Note:** The todo description is already in bullet format (validated when it was added via `_validate_epr_format()`), so no conversion or validation is needed when completing.

### 2. Directly Log an Accomplishment
When the user says "completed", "accomplished", "log accomplishment", "add accomplishment", "record accomplishment", etc, WITHOUT an existing todo:
1. Take the user's description and ensure it meets bullet format:
   - Maximum 20 words
   - No semicolons, colons, or dashes
   - Strong action verb (Led, Managed, Developed, etc.)
2. Directly edit accomplishments.json to add the entry with today's date
3. **CRITICAL: Run `./journal.py sync` to update Hugo content** (NEVER skip this step!)
4. Confirm the accomplishment was logged

**IMPORTANT: Accomplishments do NOT need to be associated with an existing todo. If the user states they completed or accomplished something that's not in their todo list, log it directly as an accomplishment.**

## Error Handling & Validation

### Partial ID Matching
The system supports partial ID matching for `todo complete` and `todo delete` commands:
- Users can provide just the first few characters of the UUID
- Example: `./journal.py todo complete abc123` will match todo with ID `abc123-4567-89de-...`
- If multiple todos match the partial ID, the system shows an error
- If no todos match, the system shows an error

### Bullet Format Validation
When adding a todo, the system validates bullet format in `TodoManager._validate_epr_format()`:
- **Word count check**: Counts words, rejects if > 20 words
- **Character check**: Rejects if contains semicolons (;), colons (:), or dashes (-)
- **Helpful feedback**: Provides specific error messages explaining what's wrong

Example validation errors (as shown to user):
- "✗ Bullet Format Validation Failed"
- "Too many words (23/20 max)"
- "Contains semicolon (;) - not allowed in bullet format"
- "Contains colon (:) - not allowed in bullet format"
- "Contains dash (-) - not allowed in bullet format"

### Emoji Handling
- **Storage**: Todos are stored WITH emojis in todos.json (user can add emojis if desired)
- **Display**: When displaying todos to user, emojis are stripped via `TodoManager._strip_emoji()`
- **Why**: Keeps display clean and professional while preserving user's original input
- **Important**: Never modify the emoji content in data files, only strip during display

## Critical Time/Date Awareness

### Always Be Date-Aware
- **Current Date**: Always check today's date before responding to user queries
- **User Forgetfulness**: Users may forget to close out their day, so completed todos from yesterday might still be in today's context
- **Previous Day Queries**: When a user asks about "yesterday" or "previous day" accomplishments, verify:
  1. What is today's date?
  2. What is yesterday's date?
  3. What accomplishments were completed on that specific date?
- **Late Night Edge Cases**: If it's late at night (after 10pm), the user might be referring to earlier today when they say "today's accomplishments"

### Handling Date Queries
When a user asks about accomplishments:
- **"Today's accomplishments"** → Check accomplishments.json for today's date
- **"Yesterday's accomplishments"** → Calculate yesterday's date and filter
- **"This week's accomplishments"** → Show last 7 days
- **"Previous day's accomplishments"** → Interpret as yesterday unless they specify a date

### Data Integrity
- Completion dates are stored in ISO format: YYYY-MM-DD
- Always verify dates match before reporting accomplishments
- If no accomplishments exist for a date, clearly state that
- Don't assume an empty list means the user didn't accomplish anything - they may have forgotten to log

## Communication Style
- **Use emojis in your responses** - The user likes emojis in greetings, headers, and conversational text
- Make the journal system engaging and visually friendly
- Be concise but warm

## FedRAMP Integration

The morning greeting includes checking for FedRAMP Rev 5 documentation changes. FedRAMP monitoring data is stored locally in the `fedramp/` directory.

### When to Run FedRAMP Check

**ALWAYS run the FedRAMP check when the user says:**
- "morning", "good morning", "hello", "hi", "greet", "start the day"

**NEVER run the FedRAMP check when the user:**
- Only asks for specific todos or accomplishments
- Runs specific commands like `./journal.py todo list`
- Is in the middle of another conversation without greeting

### How to Check for Changes

After running `./journal.py morning`, immediately delegate FedRAMP documentation check to a **background agent** (use `Agent` tool with `run_in_background=true`):

```
Check for FedRAMP Rev 5 documentation changes and report findings.

Read these files for complete workflow instructions:
- fedramp/FEDRAMP_AGENT_GUIDE.md (agent instructions and mandatory first steps)
- fedramp/spec.md (complete operational guidelines)

Execute the change detection workflow as specified in those files.
Report: time since last check, pages added/removed, content changes, new notices.
```

**Why background execution:** Crawling 40-50+ pages takes time; user can review todos while check runs.

## On-Demand FedRAMP Documentation Queries

**IMPORTANT: This is separate from the morning routine change detection.**

The user is a product security engineer who frequently needs to reference FedRAMP Rev 5 guidelines and policies.

### When to Trigger

Only when the user explicitly asks FedRAMP-related questions:
- "What does FedRAMP Rev 5 say about [topic]?"
- "Show me the Rev 5 guidance on [topic]"
- "What are the FedRAMP requirements for [topic]?"

### How to Query

1. Load `fedramp/snapshots/latest.json` to find the current baseline directory
2. Search through cached HTML files in `fedramp/snapshots/[baseline_directory]/`
   - **EXCLUDE RFC pages** - Only return FedRAMP Rev 5 policy/guidance pages
3. If needed, fetch fresh content from fedramp.gov

### Search Result Format Requirements

Display each metadata field on its own line (bold label, value on same line, blank line between fields):

- **Parent Page:** [page name]
- **Child Page:** [page name]
- **Section:** [major heading]
- **Header:** [sub-heading] (additional sub-headings in parentheses if applicable)
- **Severity:** [High/Moderate/Low/All Three]
- **Key Details:** [brief summary]
- **Content:** [full requirement text]
  - If Severity is "All Three" with DIFFERENT requirements per level, break out explicitly:
    - High Impact — [requirement]
    - Moderate Impact — [requirement]
    - Low Impact — [requirement]
  - If SAME requirement for all levels, keep as single block

**Note:** Complete formatting examples are in `fedramp/spec.md`

## Conversational Commands (Cursor Interface)
The user interacts with the journal through natural conversation. Recognize these intents:

**Morning greeting:**
- **Triggers:** "morning", "good morning", "hello", "hi", "greet", "start the day"
- **IMPORTANT:** When the user says ANY of these greetings, treat it as a full morning routine request
- **Two-step process:**
  1. First, run: `./journal.py morning` - Shows greeting, date, Marcus Aurelius quote, pending todos
  2. Then, spawn background agent for FedRAMP documentation check (see FedRAMP Integration section - use Agent tool with run_in_background=true)
- **Do NOT** treat "hello" or "hi" as casual greetings - they always trigger the full morning routine
- **Background execution:** FedRAMP check runs while user reviews todos, results shown when complete

**Todo management:**
- "add todo [description]" → **IMPORTANT:** Validate bullet format first (max 20 words, no semicolons/colons/dashes). If user's description doesn't meet requirements, help them rewrite it before adding to the system.
- "show todos", "list todos", "what are my todos" → Display pending todos (strip emojis, hide IDs, use checkbox format)
- "complete [todo-id or description]" → Mark done (supports partial ID matching), copy to accomplishments, sync Hugo (no conversion needed - already validated)

**Accomplishment management:**
- "log accomplishment [description]" → Validate/convert to bullet format, then add directly to accomplishments.json, sync Hugo
- "add accomplishment [description]" → Same as above
- "show today", "today's accomplishments" → Filter by today's date
- "show yesterday", "yesterday's accomplishments" → Filter by yesterday
- "show this week" → Last 7 days
- "show Q1/Q2/Q3/Q4" → Filter by quarter

## Display Format for Todos
When displaying todos in chat responses, ALWAYS:
- Strip any emojis from the todo description text
- Use simple checkbox format: `- [ ] Description text`
- Do NOT show the todo ID in the display
- Keep it clean and minimal

**Example:**
```
Your pending todos:
- [ ] Review documentation for MFA implementation status
- [ ] Coordinate plans with Andrew on AWS Bedrock documentation
- [ ] Update GW user account Jira ticket with new information
```

**Note:** Emojis and IDs remain stored in the data files (don't modify the data), but strip emojis and hide IDs when displaying to the user.

## Display Format for Accomplishments
When showing accomplishments (today, yesterday, week, quarter), always use bullet list format with `•` and a **blank line between each bullet** for readability:

```
Today's Accomplishments (April 14, 2026):

• [EPR-formatted accomplishment]

• [EPR-formatted accomplishment]

• [EPR-formatted accomplishment]
```

## Coding Preferences
- Use Python 3.6+
- Keep code simple and readable
- Use standard library when possible (datetime, json, pathlib)
- All dates in ISO format (YYYY-MM-DD)
- Command pattern: each major feature is a Manager class in `commands/`
- Modular design: separate CLI parsing (journal.py) from business logic (commands/)

## Privacy & Security
- This is personal data - never suggest cloud syncing or sharing features
- All data stays local on the user's machine
- Journal entries are private

## File Organization
- Todos: `data/todos.json`
- Accomplishments: `data/accomplishments.json`
- Marcus Aurelius Quotes: `data/marcus_aurelius_quotes.json` (1,700+ quotes from the full text of Meditations)
- Hugo content: `hugo/content/accomplishments/YYYY/qX/`
- Hugo layouts: `hugo/layouts/` (index.html, _default/list.html, _default/single.html)
- Hugo partials: `hugo/layouts/partials/` (head.html, theme-toggle.html - dark mode implementation)
- Scripts: `scripts/parse_meditations.py` (one-time utility used to extract quotes from Meditations text - only needed if quotes require updating)

## Git Workflow

This repository is used for personal journaling with GitHub as a remote backup.

**Committing Changes:**
- Commit after adding new features or fixing bugs
- Use descriptive commit messages in present tense (e.g., "Add FedRAMP change detection", "Fix bullet format validation")
- Group related changes together in a single commit

**Pushing to GitHub:**
- Push regularly to keep GitHub backup up to date
- Command: `git push origin main`
- Safe to push anytime - this is a personal repository

**Privacy Note:**
- `data/todos.json` and `data/accomplishments.json` are gitignored (personal data stays local)
- Only code, configuration, and documentation are version controlled

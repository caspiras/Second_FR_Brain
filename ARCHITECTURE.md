# Architecture

## Technology Stack
- **Hugo**: Static site generator for displaying journal content locally
- **Python**: CLI tool for managing todos and accomplishments
- **Markdown**: Content format for Hugo pages
- **YAML/JSON**: Data storage for todos and accomplishments

## Directory Structure
```
journal/
├── hugo/                      # Hugo site
│   ├── content/
│   │   ├── accomplishments/   # Accomplishments organized by quarter
│   │   │   ├── 2026/
│   │   │   │   ├── q1/       # Jan-Mar
│   │   │   │   ├── q2/       # Apr-Jun
│   │   │   │   ├── q3/       # Jul-Sep
│   │   │   │   └── q4/       # Oct-Dec
│   │   └── daily/            # Daily views
│   ├── layouts/
│   ├── static/
│   └── config.toml
├── data/
│   ├── todos.json                  # Active todos
│   ├── accomplishments.json        # Completed items
│   └── marcus_aurelius_quotes.json # 1,700+ quotes from Meditations
├── scripts/
│   └── parse_meditations.py        # Downloads and parses full text
├── journal.py                # Main CLI tool
├── commands/
│   ├── todo.py              # Todo management
│   └── hugo_sync.py         # Sync data to Hugo content
└── README.md
```

## Data Flow

### Adding a Todo
1. User runs `journal.py todo add "Task description"`
2. Todo is added to `data/todos.json` with status: "pending"
3. Assigned a unique ID and created_date

### Completing a Todo
1. User runs `journal.py todo complete <id>`
2. Todo status updated to "completed" in `todos.json`
3. Completion_date is set to current date
4. Todo is copied to `accomplishments.json`
5. Hugo content files are regenerated via `hugo_sync.py`
6. Accomplishment is categorized into appropriate quarter based on completion_date
7. Markdown file created in `hugo/content/accomplishments/YYYY/qX/`

### Viewing Accomplishments
1. User runs `hugo server` from `hugo/` directory
2. Hugo serves site on localhost (typically :1313)
3. Users can browse:
   - Quarterly views (all accomplishments per quarter)
   - Daily views (accomplishments by specific date)
   - Annual summaries

## Hugo Content Organization

### Quarter Pages
- Each quarter gets an index page: `hugo/content/accomplishments/2026/q1/_index.md`
- Lists all accomplishments completed in that quarter
- Sorted by completion date

### Daily Pages
- Individual accomplishments stored as: `hugo/content/accomplishments/2026/q1/YYYY-MM-DD.md`
- Can have multiple accomplishments per day
- Frontmatter includes: date, title, tags, quarter

### Hugo Frontmatter Example
```yaml
---
title: "Completed Project X"
date: 2026-04-14
quarter: "Q2"
year: 2026
tags: ["work", "project"]
---
Description of accomplishment
```

## CLI Commands Structure
```
journal.py morning                      # Start your day (greeting + pending todos)
journal.py hello/hi/greet              # Aliases for morning

journal.py todo add "description"       # Add new todo
journal.py todo list                    # Show all pending todos
journal.py todo complete <id>           # Mark todo as complete
journal.py todo delete <id>             # Delete a todo

journal.py accomplishments today        # Show today's accomplishments
journal.py accomplishments yesterday    # Show yesterday's accomplishments
journal.py accomplishments week         # Show last 7 days
journal.py accomplishments quarter q2   # Show Q2 accomplishments

journal.py serve                        # Start Hugo server
journal.py sync                         # Manually sync to Hugo
```

## Data Schema

### todos.json
```json
{
  "todos": [
    {
      "id": "uuid-string",
      "description": "Task description",
      "created_date": "2026-04-14",
      "completed_date": null,
      "status": "pending"
    }
  ]
}
```

### accomplishments.json
```json
{
  "accomplishments": [
    {
      "id": "uuid-string",
      "description": "Completed task description",
      "created_date": "2026-04-14",
      "completed_date": "2026-04-15",
      "quarter": "Q2",
      "year": 2026
    }
  ]
}
```

## Quarter Calculation Logic
- Read completion_date
- Extract month
- Calculate quarter:
  - Months 1-3 → Q1
  - Months 4-6 → Q2
  - Months 7-9 → Q3
  - Months 10-12 → Q4

## Hugo Theme & Layout
- Use simple, clean theme (or custom minimal theme)
- Layouts:
  - `layouts/_default/list.html` - For quarter index pages
  - `layouts/_default/single.html` - For individual accomplishment pages
  - `layouts/index.html` - Homepage with year/quarter navigation
- Partials:
  - `layouts/partials/quarter-nav.html` - Quarter navigation menu
  - `layouts/partials/accomplishment-list.html` - List rendering

## Configuration Management
- `config.toml` for Hugo configuration
- Python config could use environment variables or config file for:
  - Hugo directory path
  - Data directory path
  - Default Hugo server port

## Sync Strategy
- When a todo is completed, `hugo_sync.py`:
  1. Reads accomplishments.json
  2. Generates markdown files in appropriate quarter directory
  3. Creates/updates quarter index pages with all accomplishments
  4. Ensures proper frontmatter for Hugo processing

## Error Handling
- Validate todo ID exists before completing/deleting
- Handle missing Hugo directory gracefully
- Check for duplicate IDs
- Validate date formats
- Backup data files before modifications

## Date/Time Handling
- All dates stored in ISO 8601 format: YYYY-MM-DD
- Completion date captured when `todo complete` is executed
- Quarter calculated from completion_date, not created_date
- System timezone-aware (uses system's local time)
- Edge cases handled:
  - User forgets to close out day → accomplishments remain accurately dated
  - Late night completions → dated to the day they were completed
  - Viewing "yesterday" → calculates actual previous calendar day

## Time-Aware Features
- Daily greeting shows current date and time-appropriate greeting
- Accomplishment queries filter by exact dates
- Weekly view shows rolling 7-day window
- Quarter view filters by completion quarter and current year

## Future Enhancements (Not in MVP)
- Search across accomplishments
- Tags/categories for todos
- Priority levels
- Recurring todos
- Export to PDF/CSV
- Statistics dashboard (total accomplishments per quarter)


# Journal Project

A todo list and accomplishment tracking system with quarterly organization, powered by Hugo.

## Features

- ✅ **Integrated Todo & Accomplishment Tracking** - Completed todos automatically become accomplishments
- 📅 **Daily Tracking** - Track what you accomplish each day
- 📊 **Quarterly Organization** - View accomplishments by fiscal quarters (Q1-Q4)
- 🌐 **Local Hugo Site** - Beautiful web interface for browsing accomplishments

## Prerequisites

- Python 3.6+
- Hugo (install from https://gohugo.io/installation/)

## Installation

1. Clone or navigate to this directory
2. Ensure Hugo is installed: `hugo version`

## Usage

### Start Your Day

**Get a greeting with your pending todos:**
```bash
./journal.py morning
# or use: hello, hi, greet
```

This will show you:
- A time-appropriate greeting (Good morning/afternoon/evening)
- Today's date
- Random quote from Marcus Aurelius' "Meditations" (1,700+ quotes from the full text!)
- All your pending todos
- Motivation to get things done!

### Managing Todos

**Add a todo (Air Force EPR format):**
```bash
./journal.py todo add "Led team of 5 to complete project 2 weeks early"
```

**Important: EPR Format Requirements**
- Maximum 20 words
- No semicolons, colons, or dashes
- Start with action verb (Led, Managed, Developed, etc.)
- Be concise and impactful

The system will validate your todo and provide helpful feedback if it doesn't meet EPR format.

**List pending todos:**
```bash
./journal.py todo list
```

**Complete a todo (becomes an accomplishment):**
```bash
./journal.py todo complete <todo-id>
```
Note: You can use the first few characters of the ID

**Delete a todo:**
```bash
./journal.py todo delete <todo-id>
```

### Viewing Accomplishments

**View in the terminal:**
```bash
./journal.py accomplishments today       # Today's accomplishments
./journal.py accomplishments yesterday   # Yesterday's accomplishments
./journal.py accomplishments week        # Last 7 days
./journal.py accomplishments quarter q2  # Specific quarter (q1, q2, q3, q4)
```

**View in browser (Hugo server):**
```bash
./journal.py serve
```
Then visit http://localhost:1313 in your browser

**Manually sync to Hugo:**
```bash
./journal.py sync
```

### Quarterly Organization

Accomplishments are automatically organized by quarter:
- **Q1**: January 1 - March 31
- **Q2**: April 1 - June 30
- **Q3**: July 1 - September 30
- **Q4**: October 1 - December 31

Browse by year and quarter in the Hugo web interface!

## EPR Writing Guide

Need help writing in Air Force EPR format? Check out **EPR_GUIDE.md** for:
- Detailed formatting rules
- Strong action verbs to use
- Examples by category (development, project management, etc.)
- Common mistakes to avoid
- Quick tips and checklist

## Project Structure

```
journal/
├── data/                    # JSON data files
│   ├── todos.json          # Active todos
│   ├── accomplishments.json # Completed items
│   └── marcus_aurelius_quotes.json # 1,700+ quotes from Meditations
├── scripts/
│   └── parse_meditations.py # Parser for extracting quotes from full text
├── hugo/                    # Hugo static site
│   ├── content/            # Generated accomplishment pages
│   └── layouts/            # HTML templates
├── commands/               # Python modules
│   ├── todo.py            # Todo management
│   └── hugo_sync.py       # Hugo synchronization
└── journal.py             # Main CLI tool
```

## How It Works

1. Add todos throughout your day
2. When you complete a todo, it's automatically:
   - Marked as complete in your todo list
   - Added to accomplishments with the completion date (timestamped accurately)
   - Categorized into the appropriate quarter
   - Synced to Hugo for web viewing
3. Browse your accomplishments by quarter using the Hugo site or terminal commands

## Date Awareness

The system is fully date-aware:
- Accomplishments are timestamped with their **completion date** (YYYY-MM-DD)
- You can view accomplishments for specific dates (today, yesterday, this week)
- Quarter assignment is based on when you **completed** the todo, not when you created it
- If you forget to close out your day, accomplishments from previous days remain accurately dated

## Conversational Interface (Claude Code)

If using this system with Claude Code (claude.ai/code), you can use natural language instead of CLI commands:

### Morning Routine Triggers
Say any of these to start your day:
- `morning` / `good morning`
- `hello` / `hi`
- `greet` / `start the day`

This shows: greeting, date, Marcus Aurelius quote, pending todos, **and** FedRAMP documentation changes.

### Todo Management Triggers
- `add todo [description]` - Add a new todo (will help you format in EPR)
- `show todos` / `list todos` / `what are my todos` - Display pending todos
- `complete [todo-id or description]` - Mark todo as done (supports partial ID matching)

### Accomplishment Management Triggers
- `log accomplishment [description]` / `add accomplishment [description]` - Log directly (no existing todo needed)
- `show today` / `today's accomplishments` - View today's accomplishments
- `show yesterday` / `yesterday's accomplishments` - View yesterday
- `show this week` - Last 7 days
- `show Q1` / `show Q2` / `show Q3` / `show Q4` - View by quarter

**Note:** Claude Code will help you format descriptions to meet EPR requirements before adding them to the system.


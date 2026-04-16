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

**Add a todo (bullet formatting):**
```bash
./journal.py todo add "Led team of 5 to complete project 2 weeks early"
```

**Important: Bullet Format Requirements**
- Maximum 20 words
- No semicolons, colons, or dashes
- Start with action verb (Led, Managed, Developed, etc.)
- Be concise and impactful

The system will validate your todo and provide helpful feedback if it doesn't meet the format requirements.

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

## Bullet Writing Guide

Need help writing effective bullet points? Check out **EPR_GUIDE.md** for:
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

## Conversational Trigger Words (Claude Code)

When using this system with Claude Code, you can use natural language commands:

### Morning Routine
Trigger words: `morning`, `good morning`, `hello`, `hi`, `greet`, `start the day`

### Todo Management
- **Add**: "add todo [description]"
- **View**: "show todos", "list todos", "what are my todos"
- **Complete**: "complete [todo-id or description]", "mark [todo] done"
- **Delete**: "delete [todo-id]", "remove [todo]"

### Accomplishment Management
- **Log directly**: "log accomplishment [description]", "add accomplishment [description]"
- **View today**: "show today", "today's accomplishments"
- **View yesterday**: "show yesterday", "yesterday's accomplishments"
- **View week**: "show this week", "this week's accomplishments"
- **View quarter**: "show Q1", "show Q2", "show Q3", "show Q4"


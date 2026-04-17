# Quick Start Guide

Get started with your journaling system in 3 steps!

## Step 0: Start Your Day ☀️

```bash
./journal.py morning
# or: ./journal.py hello
```

Get a nice greeting, wisdom from Marcus Aurelius, and see all your pending todos!

**What you'll see:**
- Time-appropriate greeting
- Inspirational quote from "Meditations" (1,700+ different quotes!)
- Your pending todos list

## Step 1: Add Some Todos (Bullet Format!)

Remember: Max 20 words, no semicolons/colons/dashes, start with action verb!

```bash
./journal.py todo add "Led team meeting to finalize project proposal and timeline"
./journal.py todo add "Reviewed team feedback and incorporated 5 key suggestions"
./journal.py todo add "Updated documentation improving clarity by 40 percent"
```

**Not sure about bullet format?** Check **BULLET_GUIDE.md** for examples and tips!

## Step 2: Complete Todos (They Become Accomplishments!)

```bash
# List your todos first
./journal.py todo list

# Complete one using the ID shown (you can use just the first few characters)
./journal.py todo complete <id>
```

When you complete a todo, it automatically:
- Gets marked as complete
- Becomes an accomplishment
- Gets categorized into the current quarter
- Syncs to your Hugo site

## Step 3: View Your Accomplishments

```bash
# Start the Hugo server
./journal.py serve
```

Then open your browser to: **http://localhost:1313**

You'll see:
- Your accomplishments organized by year and quarter
- Daily breakdowns of what you accomplished
- A clean, browseable interface

## Tips

- **Partial IDs work**: Instead of typing the full UUID, just use the first few characters (e.g., `e04a09a0`)
- **Auto-sync**: Accomplishments sync to Hugo automatically when you complete a todo
- **Manual sync**: Run `./journal.py sync` if needed
- **Quarterly view**: Navigate through Q1, Q2, Q3, Q4 in the web interface

## Example Workflow

Morning:
```bash
# Start your day
./journal.py morning

# Add your todos (bullet format!)
./journal.py todo add "Authored blog post on microservices architecture for engineering team"
./journal.py todo add "Fixed critical authentication bug affecting 500 users"
./journal.py todo add "Coordinated client meeting to finalize project requirements and timeline"
```

Throughout the day, as you complete tasks:
```bash
./journal.py todo complete <id>
```

Check your progress:
```bash
# See what you've accomplished today
./journal.py accomplishments today

# See this week's accomplishments
./journal.py accomplishments week
```

End of day:
```bash
# View in the browser
./journal.py serve

# Or quickly check in terminal
./journal.py accomplishments today
```

Next morning:
```bash
# Start fresh
./journal.py morning

# Check what you did yesterday
./journal.py accomplishments yesterday
```

## Current Quarter Breakdown

- **Q1**: January 1 - March 31
- **Q2**: April 1 - June 30  ← You're here!
- **Q3**: July 1 - September 30
- **Q4**: October 1 - December 31

---

**Need help?** Check README.md for full documentation!

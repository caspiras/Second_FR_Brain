#!/usr/bin/env python3
"""
Journal CLI - Manage todos and accomplishments
"""
import argparse
import subprocess
import sys
import json
import random
from pathlib import Path
from datetime import datetime
from commands.todo import TodoManager
from commands.accomplishments import AccomplishmentManager
from commands.hugo_sync import sync_to_hugo


def get_greeting():
    """Get time-appropriate greeting"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 22:
        return "Good evening"
    else:
        return "Hello"


def get_random_marcus_quote():
    """Get a random quote from Marcus Aurelius"""
    quotes_file = Path("data/marcus_aurelius_quotes.json")
    try:
        with open(quotes_file, 'r') as f:
            data = json.load(f)
            return random.choice(data["quotes"])
    except FileNotFoundError:
        return "You have power over your mind, not outside events. Realize this, and you will find strength."


def show_daily_greeting():
    """Show greeting with Marcus Aurelius quote and pending todos"""
    greeting = get_greeting()
    today = datetime.now().strftime("%A, %B %d, %Y")

    print(f"\n{'='*60}")
    print(f"  {greeting}! ☀️")
    print(f"  {today}")
    print(f"{'='*60}\n")

    # Marcus Aurelius quote
    quote = get_random_marcus_quote()
    print(f"💭 Marcus Aurelius:\n")
    print(f'   "{quote}"\n')
    print(f"{'='*60}\n")

    manager = TodoManager()
    data = manager._load_todos()
    pending_todos = [t for t in data["todos"] if t["status"] == "pending"]

    if pending_todos:
        print(f"📋 You have {len(pending_todos)} pending todo(s):\n")
        for todo in pending_todos:
            description = manager._strip_emoji(todo['description'])
            print(f"  [ ] [{todo['id'][:8]}] {description}")
            print(f"      Created: {todo['created_date']}\n")
        print(f"{'='*60}")
        print("💪 Let's get things done today!")
    else:
        print("🎉 No pending todos! You're all caught up!")
        print(f"{'='*60}")
        print("✨ Start fresh with: ./journal.py todo add \"Your task\"")

    print()


def main():
    parser = argparse.ArgumentParser(
        description="Journal CLI - Track todos and accomplishments"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Todo commands
    todo_parser = subparsers.add_parser("todo", help="Manage todos")
    todo_subparsers = todo_parser.add_subparsers(dest="todo_command")

    # todo add
    add_parser = todo_subparsers.add_parser("add", help="Add a new todo")
    add_parser.add_argument("description", help="Todo description")

    # todo list
    todo_subparsers.add_parser("list", help="List all pending todos")

    # todo complete
    complete_parser = todo_subparsers.add_parser("complete", help="Mark todo as complete")
    complete_parser.add_argument("id", help="Todo ID (or first few characters)")

    # todo delete
    delete_parser = todo_subparsers.add_parser("delete", help="Delete a todo")
    delete_parser.add_argument("id", help="Todo ID (or first few characters)")

    # Accomplishments commands
    acc_parser = subparsers.add_parser("accomplishments", help="View accomplishments")
    acc_subparsers = acc_parser.add_subparsers(dest="acc_command")

    # accomplishments today
    acc_subparsers.add_parser("today", help="Show today's accomplishments")

    # accomplishments yesterday
    acc_subparsers.add_parser("yesterday", help="Show yesterday's accomplishments")

    # accomplishments week
    acc_subparsers.add_parser("week", help="Show this week's accomplishments")

    # accomplishments quarter
    quarter_parser = acc_subparsers.add_parser("quarter", help="Show quarter accomplishments")
    quarter_parser.add_argument("quarter", help="Quarter (q1, q2, q3, q4)")

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Start Hugo server")
    serve_parser.add_argument("--port", default=1313, type=int, help="Port number")

    # Sync command
    subparsers.add_parser("sync", help="Manually sync accomplishments to Hugo")

    # Greeting commands
    greet_parser = subparsers.add_parser("morning", help="Start your day with a greeting and todo list")
    subparsers.add_parser("hello", help="Greeting (alias for morning)")
    subparsers.add_parser("hi", help="Greeting (alias for morning)")
    subparsers.add_parser("greet", help="Greeting (alias for morning)")

    args = parser.parse_args()

    # Handle commands
    if args.command == "todo":
        manager = TodoManager()

        if args.todo_command == "add":
            manager.add(args.description)
        elif args.todo_command == "list":
            manager.list()
        elif args.todo_command == "complete":
            manager.complete(args.id)
        elif args.todo_command == "delete":
            manager.delete(args.id)
        else:
            todo_parser.print_help()

    elif args.command == "accomplishments":
        acc_manager = AccomplishmentManager()

        if args.acc_command == "today":
            acc_manager.show_today()
        elif args.acc_command == "yesterday":
            acc_manager.show_yesterday()
        elif args.acc_command == "week":
            acc_manager.show_week()
        elif args.acc_command == "quarter":
            acc_manager.show_quarter(args.quarter)
        else:
            acc_parser.print_help()

    elif args.command == "serve":
        hugo_dir = Path("hugo")
        if not hugo_dir.exists():
            print("✗ Hugo directory not found")
            sys.exit(1)

        print(f"🚀 Starting Hugo server on port {args.port}...")
        print(f"   Visit: http://localhost:{args.port}")
        print("   Press Ctrl+C to stop")

        try:
            subprocess.run(
                ["hugo", "server", "--port", str(args.port)],
                cwd=hugo_dir
            )
        except KeyboardInterrupt:
            print("\n✓ Server stopped")

    elif args.command == "sync":
        sync_to_hugo()

    elif args.command in ["morning", "hello", "hi", "greet"]:
        show_daily_greeting()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()

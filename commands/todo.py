"""Todo management commands"""
import json
import uuid
import re
from datetime import datetime
from pathlib import Path


class TodoManager:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.todos_file = self.data_dir / "todos.json"
        self.accomplishments_file = self.data_dir / "accomplishments.json"

    def _strip_emoji(self, text):
        """Remove emoji characters from text"""
        # Pattern to match emojis
        emoji_pattern = re.compile(
            "["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE
        )
        return emoji_pattern.sub('', text).strip()

    def _load_todos(self):
        """Load todos from JSON file"""
        with open(self.todos_file, 'r') as f:
            return json.load(f)

    def _save_todos(self, data):
        """Save todos to JSON file"""
        with open(self.todos_file, 'w') as f:
            json.dump(data, f, indent=2)

    def _load_accomplishments(self):
        """Load accomplishments from JSON file"""
        with open(self.accomplishments_file, 'r') as f:
            return json.load(f)

    def _save_accomplishments(self, data):
        """Save accomplishments to JSON file"""
        with open(self.accomplishments_file, 'w') as f:
            json.dump(data, f, indent=2)

    def _get_quarter(self, date_str):
        """Calculate quarter from date string (YYYY-MM-DD)"""
        date = datetime.strptime(date_str, "%Y-%m-%d")
        month = date.month
        if 1 <= month <= 3:
            return "Q1"
        elif 4 <= month <= 6:
            return "Q2"
        elif 7 <= month <= 9:
            return "Q3"
        else:
            return "Q4"

    def _validate_epr_format(self, description):
        """Validate bullet format constraints"""
        errors = []

        # Check word count (max 20 words)
        word_count = len(description.split())
        if word_count > 20:
            errors.append(f"Too many words ({word_count}/20 max)")

        # Check for prohibited punctuation
        if ';' in description:
            errors.append("Contains semicolon (;) - not allowed in bullet format")
        if ':' in description:
            errors.append("Contains colon (:) - not allowed in bullet format")
        if '--' in description or description.count('-') > 0:
            errors.append("Contains dash (-) - not allowed in bullet format")

        return errors

    def add(self, description):
        """Add a new todo"""
        # Validate bullet format
        errors = self._validate_epr_format(description)
        if errors:
            print("\n✗ Bullet Format Validation Failed:\n")
            for error in errors:
                print(f"  • {error}")
            print("\n📝 Bullet Format Tips:")
            print("  • Max 20 words")
            print("  • No semicolons, colons, or dashes")
            print("  • Start with action verb (Led, Managed, Developed, etc.)")
            print("  • Be concise and impactful")
            print("\n  Example: Led team of 5 to complete project 2 weeks early")
            print()
            return

        data = self._load_todos()

        todo = {
            "id": str(uuid.uuid4()),
            "description": description,
            "created_date": datetime.now().strftime("%Y-%m-%d"),
            "completed_date": None,
            "status": "pending"
        }

        data["todos"].append(todo)
        self._save_todos(data)

        word_count = len(description.split())
        print(f"✓ Todo added: {description}")
        print(f"  ID: {todo['id']}")
        print(f"  Words: {word_count}/20")

    def list(self):
        """List all pending todos"""
        data = self._load_todos()
        pending_todos = [t for t in data["todos"] if t["status"] == "pending"]

        if not pending_todos:
            print("No pending todos.")
            return

        print(f"\n📋 Pending Todos ({len(pending_todos)}):\n")
        for todo in pending_todos:
            description = self._strip_emoji(todo['description'])
            print(f"  [ ] [{todo['id'][:8]}] {description}")
            print(f"      Created: {todo['created_date']}\n")

    def complete(self, todo_id):
        """Mark a todo as complete"""
        data = self._load_todos()

        # Find the todo
        todo = None
        for t in data["todos"]:
            if t["id"].startswith(todo_id) and t["status"] == "pending":
                todo = t
                break

        if not todo:
            print(f"✗ Todo not found or already completed: {todo_id}")
            return

        # Mark as complete
        completed_date = datetime.now().strftime("%Y-%m-%d")
        todo["completed_date"] = completed_date
        todo["status"] = "completed"

        # Save updated todos
        self._save_todos(data)

        # Add to accomplishments
        accomplishments_data = self._load_accomplishments()
        year = datetime.now().year
        quarter = self._get_quarter(completed_date)

        accomplishment = {
            "id": todo["id"],
            "description": todo["description"],
            "created_date": todo["created_date"],
            "completed_date": completed_date,
            "quarter": quarter,
            "year": year
        }

        accomplishments_data["accomplishments"].append(accomplishment)
        self._save_accomplishments(accomplishments_data)

        print(f"✓ Todo completed: {todo['description']}")
        print(f"  Added to accomplishments ({year} {quarter})")

        # Trigger Hugo sync
        from commands.hugo_sync import sync_to_hugo
        sync_to_hugo()

    def delete(self, todo_id):
        """Delete a todo"""
        data = self._load_todos()

        # Find and remove the todo
        original_length = len(data["todos"])
        data["todos"] = [t for t in data["todos"] if not t["id"].startswith(todo_id)]

        if len(data["todos"]) == original_length:
            print(f"✗ Todo not found: {todo_id}")
            return

        self._save_todos(data)
        print(f"✓ Todo deleted: {todo_id}")

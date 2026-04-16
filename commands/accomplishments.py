"""Accomplishments viewing commands"""
import json
from datetime import datetime, timedelta
from pathlib import Path


class AccomplishmentManager:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.accomplishments_file = self.data_dir / "accomplishments.json"

    def _load_accomplishments(self):
        """Load accomplishments from JSON file"""
        with open(self.accomplishments_file, 'r') as f:
            return json.load(f)

    def show_today(self):
        """Show today's accomplishments"""
        today = datetime.now().strftime("%Y-%m-%d")
        self._show_for_date(today, "Today")

    def show_yesterday(self):
        """Show yesterday's accomplishments"""
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        self._show_for_date(yesterday, "Yesterday")

    def show_week(self):
        """Show this week's accomplishments"""
        today = datetime.now()
        week_ago = today - timedelta(days=7)

        data = self._load_accomplishments()
        accomplishments = data["accomplishments"]

        # Filter for last 7 days
        week_accs = [
            acc for acc in accomplishments
            if week_ago.strftime("%Y-%m-%d") <= acc["completed_date"] <= today.strftime("%Y-%m-%d")
        ]

        if not week_accs:
            print("\n📊 No accomplishments in the last 7 days.")
            return

        # Group by date
        by_date = {}
        for acc in week_accs:
            date = acc["completed_date"]
            if date not in by_date:
                by_date[date] = []
            by_date[date].append(acc)

        print(f"\n📊 Accomplishments - Last 7 Days ({len(week_accs)} total)\n")
        print("=" * 60)

        for date in sorted(by_date.keys(), reverse=True):
            dt = datetime.strptime(date, "%Y-%m-%d")
            formatted_date = dt.strftime("%A, %B %d, %Y")
            accs = by_date[date]

            print(f"\n{formatted_date} ({len(accs)} accomplishment{'s' if len(accs) > 1 else ''}):")
            for acc in accs:
                print(f"  ✓ {acc['description']}")

        print(f"\n{'=' * 60}\n")

    def show_quarter(self, quarter):
        """Show accomplishments for a specific quarter"""
        quarter = quarter.upper()
        if quarter not in ["Q1", "Q2", "Q3", "Q4"]:
            print(f"✗ Invalid quarter: {quarter}. Use Q1, Q2, Q3, or Q4")
            return

        year = datetime.now().year
        data = self._load_accomplishments()
        accomplishments = data["accomplishments"]

        # Filter for the quarter
        quarter_accs = [
            acc for acc in accomplishments
            if acc["quarter"] == quarter and acc["year"] == year
        ]

        if not quarter_accs:
            print(f"\n📊 No accomplishments for {year} {quarter}.")
            return

        # Get quarter date range
        quarter_ranges = {
            "Q1": "January - March",
            "Q2": "April - June",
            "Q3": "July - September",
            "Q4": "October - December"
        }

        print(f"\n📊 {year} {quarter} Accomplishments ({quarter_ranges[quarter]})")
        print(f"   Total: {len(quarter_accs)} accomplishment{'s' if len(quarter_accs) > 1 else ''}\n")
        print("=" * 60)

        # Group by date
        by_date = {}
        for acc in quarter_accs:
            date = acc["completed_date"]
            if date not in by_date:
                by_date[date] = []
            by_date[date].append(acc)

        for date in sorted(by_date.keys(), reverse=True):
            dt = datetime.strptime(date, "%Y-%m-%d")
            formatted_date = dt.strftime("%A, %B %d, %Y")
            accs = by_date[date]

            print(f"\n{formatted_date}:")
            for acc in accs:
                print(f"  ✓ {acc['description']}")

        print(f"\n{'=' * 60}\n")

    def _show_for_date(self, date_str, label):
        """Show accomplishments for a specific date"""
        data = self._load_accomplishments()
        accomplishments = data["accomplishments"]

        # Filter for the date
        date_accs = [
            acc for acc in accomplishments
            if acc["completed_date"] == date_str
        ]

        # Format the date nicely
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        formatted_date = dt.strftime("%A, %B %d, %Y")

        print(f"\n📊 {label}'s Accomplishments ({formatted_date})")
        print("=" * 60)

        if not date_accs:
            print("\n  No accomplishments recorded for this day.")
            print("\n  This could mean:")
            print("    • You didn't complete any todos on this day")
            print("    • You forgot to mark todos as complete")
            print("    • You took a well-deserved break! 🌴")
        else:
            print(f"\n  Total: {len(date_accs)} accomplishment{'s' if len(date_accs) > 1 else ''}\n")
            for idx, acc in enumerate(date_accs, 1):
                print(f"  {idx}. ✓ {acc['description']}")

        print(f"\n{'=' * 60}\n")

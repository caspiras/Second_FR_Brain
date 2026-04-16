"""Sync accomplishments to Hugo content"""
import json
from pathlib import Path
from datetime import datetime


def sync_to_hugo():
    """Sync accomplishments.json to Hugo markdown files"""

    # Load accomplishments
    accomplishments_file = Path("data/accomplishments.json")
    with open(accomplishments_file, 'r') as f:
        data = json.load(f)

    accomplishments = data["accomplishments"]

    # Group by year and quarter
    grouped = {}
    for acc in accomplishments:
        year = str(acc["year"])
        quarter = acc["quarter"].lower()

        if year not in grouped:
            grouped[year] = {}
        if quarter not in grouped[year]:
            grouped[year][quarter] = []

        grouped[year][quarter].append(acc)

    # Create Hugo content structure
    hugo_content = Path("hugo/content/accomplishments")

    # Clear existing content
    if hugo_content.exists():
        for item in hugo_content.rglob("*.md"):
            item.unlink()

    # Generate markdown files
    for year, quarters in grouped.items():
        for quarter, accs in quarters.items():
            # Create directory structure
            quarter_dir = hugo_content / year / quarter
            quarter_dir.mkdir(parents=True, exist_ok=True)

            # Create index page for quarter
            index_content = f"""---
title: "{year} {quarter.upper()}"
type: "accomplishments"
---

# {year} {quarter.upper()} Accomplishments

"""

            # Group by date
            by_date = {}
            for acc in accs:
                date = acc["completed_date"]
                if date not in by_date:
                    by_date[date] = []
                by_date[date].append(acc)

            # Create individual files per date
            for date, date_accs in sorted(by_date.items()):
                date_file = quarter_dir / f"{date}.md"

                # Format date for display
                dt = datetime.strptime(date, "%Y-%m-%d")
                formatted_date = dt.strftime("%B %d, %Y")

                content = f"""---
title: "Accomplishments - {formatted_date}"
date: {date}
quarter: "{quarter.upper()}"
year: {year}
type: "accomplishment"
---

"""
                for acc in date_accs:
                    content += f"- {acc['description']}\n"

                with open(date_file, 'w') as f:
                    f.write(content)

            # Write quarter index
            index_file = quarter_dir / "_index.md"
            with open(index_file, 'w') as f:
                f.write(index_content)

    print("✓ Hugo content synced successfully")

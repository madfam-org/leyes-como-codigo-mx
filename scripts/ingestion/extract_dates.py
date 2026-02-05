import json
import re
from datetime import datetime
from pathlib import Path


def extract_dates():
    registry_path = Path("data/law_registry.json")

    if not registry_path.exists():
        print("❌ Registry not found")
        return

    with open(registry_path, "r") as f:
        registry = json.load(f)

    updated_count = 0

    # Regex for date: dd/mm/yyyy
    date_pattern = re.compile(r"DOF\s+(\d{2}/\d{2}/\d{4})")

    for law in registry["federal_laws"]:
        # Only process if missing date or current date is invalid/placeholder
        if "publication_date" not in law or not law["publication_date"]:
            match = date_pattern.search(law["name"])
            if match:
                date_str = match.group(1)
                try:
                    # Parse dd/mm/yyyy
                    dt = datetime.strptime(date_str, "%d/%m/%Y")
                    # Format YYYY-MM-DD
                    iso_date = dt.strftime("%Y-%m-%d")

                    law["publication_date"] = iso_date

                    # Clean the name optionally? keeping it for context is fine
                    # But maybe remove the "DOF..." part for cleaner UI?
                    # law['name'] = law['name'].split('DOF')[0].strip()

                    updated_count += 1
                except ValueError:
                    print(f"⚠️ Invalid date format for {law['id']}: {date_str}")

    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=4, ensure_ascii=False)

    print(f"✅ Extracted dates for {updated_count} laws")


if __name__ == "__main__":
    extract_dates()

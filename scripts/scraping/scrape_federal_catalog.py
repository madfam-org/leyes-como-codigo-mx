#!/usr/bin/env python3
"""
Wrapper script: Scrape the federal legislative catalog.

Calls the catalog_spider to fetch the list of federal laws from
diputados.gob.mx and writes the result to data/discovered_laws.json.

Exit codes: 0 = success, 1 = failure.
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def main():
    from apps.scraper.federal.catalog_spider import fetch_catalog

    output_path = PROJECT_ROOT / "data" / "discovered_laws.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("Scraping federal catalog from diputados.gob.mx ...")

    # Use local dump if available (faster, avoids network)
    local_dump = PROJECT_ROOT / "leyes_fed_dump.html"
    local_file = str(local_dump) if local_dump.exists() else None

    laws = fetch_catalog(local_file)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(laws, f, indent=2, ensure_ascii=False)

    print(f"Found {len(laws)} federal laws. Saved to {output_path}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

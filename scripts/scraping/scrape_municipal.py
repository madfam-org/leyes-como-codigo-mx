#!/usr/bin/env python3
"""
Wrapper script: Scrape municipal law catalogs.

Currently supports CDMX. Each municipality is wrapped in try/except so
one failure doesn't block the rest.

Exit codes: 0 = success (possibly partial), 1 = all failed.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def scrape_cdmx(output_dir):
    """Scrape CDMX catalog and write results."""
    from apps.scraper.municipal.cdmx import CDMXScraper

    scraper = CDMXScraper()
    results = scraper.scrape_catalog()

    output_file = output_dir / "cdmx_catalog.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"  CDMX: {len(results)} laws found. Saved to {output_file}")
    return {"municipality": "cdmx", "count": len(results), "status": "success"}


MUNICIPALITIES = [
    ("cdmx", scrape_cdmx),
]


def main():
    output_dir = PROJECT_ROOT / "data" / "municipal"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Scraping municipal law catalogs ...")

    summary = {
        "started_at": datetime.now().isoformat(),
        "municipalities": [],
    }
    succeeded = 0

    for name, scrape_fn in MUNICIPALITIES:
        print(f"  Scraping {name} ...")
        try:
            result = scrape_fn(output_dir)
            summary["municipalities"].append(result)
            succeeded += 1
        except Exception as e:
            print(f"  ERROR scraping {name}: {e}")
            summary["municipalities"].append(
                {"municipality": name, "status": "error", "error": str(e)}
            )

    summary["completed_at"] = datetime.now().isoformat()
    summary["total"] = len(MUNICIPALITIES)
    summary["succeeded"] = succeeded
    summary["failed"] = len(MUNICIPALITIES) - succeeded

    summary_file = output_dir / "municipal_scraping_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"Municipal scraping done: {succeeded}/{len(MUNICIPALITIES)} succeeded.")
    return 0 if succeeded > 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

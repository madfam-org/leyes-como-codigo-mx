#!/usr/bin/env python3
"""
Bulk Municipal Law Scraper

Scrapes municipal-scope laws from OJN for all 32 Mexican states.
Similar structure to bulk_state_scraper.py but uses scrape_municipal_laws().

Only execute after probe_ojn_municipal.py confirms OJN has municipal data.

Output: data/municipal_laws/<state>/<state>_municipal_metadata.json
"""

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ojn_scraper import OJNScraper

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
REGISTRY_PATH = PROJECT_ROOT / "data" / "state_registry.json"
MUNICIPAL_DIR = PROJECT_ROOT / "data" / "municipal_laws"


def main():
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        registry = json.load(f)

    states = registry["states"]

    # Setup logging
    log_file = MUNICIPAL_DIR / "scraping_log.txt"
    log_file.parent.mkdir(parents=True, exist_ok=True)

    def log(message):
        print(message)
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} - {message}\n")

    # Initialize scraper with municipal output dir
    scraper = OJNScraper(output_dir=str(PROJECT_ROOT / "data" / "state_laws"))

    total_stats = {
        "states_completed": 0,
        "states_failed": 0,
        "total_laws_found": 0,
        "total_laws_downloaded": 0,
        "total_laws_failed": 0,
        "start_time": datetime.now().isoformat(),
        "state_results": [],
    }

    log("=" * 80)
    log("🏘️  BULK MUNICIPAL LAW SCRAPING - STARTING")
    log(f"Total states: {len(states)}")
    log(f"Start time: {total_stats['start_time']}")
    log("=" * 80)

    for i, state in enumerate(states, 1):
        state_id = state["id"]
        state_name = state["name"]

        # Skip CDMX (not in OJN)
        if state_id == 9:
            log(f"\n[{i}/{len(states)}] Skipping {state_name} (not in OJN)")
            continue

        log(f"\n[{i}/{len(states)}] Starting: {state_name} (ID: {state_id})")

        try:
            results = scraper.scrape_municipal_laws(state_id, state_name)

            total_stats["states_completed"] += 1
            total_stats["total_laws_found"] += results["total_found"]
            total_stats["total_laws_downloaded"] += results["successful"]
            total_stats["total_laws_failed"] += results["failed"]

            total_stats["state_results"].append(
                {
                    "state_id": state_id,
                    "state_name": state_name,
                    "found": results["total_found"],
                    "downloaded": results["successful"],
                    "failed": results["failed"],
                    "success_rate": (
                        f"{results['successful']/results['total_found']*100:.1f}%"
                        if results["total_found"] > 0
                        else "0%"
                    ),
                }
            )

            log(
                f"✅ {state_name}: {results['successful']}/{results['total_found']} municipal laws"
            )

        except Exception as e:
            log(f"❌ {state_name} FAILED: {e}")
            total_stats["states_failed"] += 1
            total_stats["state_results"].append(
                {"state_id": state_id, "state_name": state_name, "error": str(e)}
            )

        # Save progress after each state
        progress_file = MUNICIPAL_DIR / "scraping_progress.json"
        with open(progress_file, "w", encoding="utf-8") as f:
            json.dump(total_stats, f, indent=2, ensure_ascii=False)

    # Final summary
    total_stats["end_time"] = datetime.now().isoformat()

    log("\n" + "=" * 80)
    log("🎉 BULK MUNICIPAL SCRAPING COMPLETE")
    log("=" * 80)
    log(f"States completed: {total_stats['states_completed']}/{len(states)}")
    log(f"States failed: {total_stats['states_failed']}")
    log(f"Total laws found: {total_stats['total_laws_found']}")
    log(f"Total downloaded: {total_stats['total_laws_downloaded']}")
    log(f"Total failed: {total_stats['total_laws_failed']}")
    if total_stats["total_laws_found"] > 0:
        rate = (
            total_stats["total_laws_downloaded"] / total_stats["total_laws_found"] * 100
        )
        log(f"Success rate: {rate:.1f}%")
    log(f"End time: {total_stats['end_time']}")
    log("=" * 80)

    # Save final summary
    summary_file = MUNICIPAL_DIR / "scraping_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(total_stats, f, indent=2, ensure_ascii=False)

    log(f"\n📊 Summary: {summary_file}")
    log(f"📝 Log: {log_file}")


if __name__ == "__main__":
    main()

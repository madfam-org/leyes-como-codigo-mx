#!/usr/bin/env python3
"""
Re-scrape Orchestrator

Runs the full state law recovery + municipal expansion sequence:
1. Re-scrape problem states with failure tracking (comprehensive)
2. Scrape CDMX via CDMXScraper
3. Smart retry transient failures
4. Run tier-1 city scrapers (best effort)
5. Consolidate all metadata (state + municipal)
6. Print summary

Usage:
    python scripts/scraping/rescrape_and_expand.py
    python scripts/scraping/rescrape_and_expand.py --skip-cities
    python scripts/scraping/rescrape_and_expand.py --dry-run
"""

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts" / "scraping"

# Problem states that need comprehensive re-scraping
PROBLEM_STATES = [
    {"id": 16, "name": "Michoacán"},
    {"id": 15, "name": "Estado de México"},
    {"id": 24, "name": "San Luis Potosí"},
    {"id": 2, "name": "Baja California"},
    {"id": 10, "name": "Durango"},
    {"id": 23, "name": "Quintana Roo"},
]


def run_step(name, cmd, cwd=None):
    """Run a subprocess step, return (success, duration)."""
    cwd = cwd or str(PROJECT_ROOT)
    print(f"\n{'='*70}")
    print(f"▶️  {name}")
    print(f"   Command: {' '.join(cmd)}")
    print(f"{'='*70}")

    start = time.time()
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=False,
            timeout=7200,  # 2h max per step
        )
        duration = time.time() - start
        success = result.returncode == 0
        status = "✅" if success else "⚠️"
        print(
            f"\n{status} {name}: {'success' if success else 'failed'} ({duration:.0f}s)"
        )
        return success, duration
    except subprocess.TimeoutExpired:
        duration = time.time() - start
        print(f"\n⏰ {name}: timed out ({duration:.0f}s)")
        return False, duration
    except Exception as e:
        duration = time.time() - start
        print(f"\n❌ {name}: error: {e} ({duration:.0f}s)")
        return False, duration


def main():
    parser = argparse.ArgumentParser(description="Re-scrape and expand orchestrator")
    parser.add_argument("--skip-cities", action="store_true", help="Skip tier-1 cities")
    parser.add_argument("--skip-cdmx", action="store_true", help="Skip CDMX scraping")
    parser.add_argument("--skip-retry", action="store_true", help="Skip smart retry")
    parser.add_argument("--dry-run", action="store_true", help="Show plan only")
    args = parser.parse_args()

    started_at = datetime.now()

    print("🚀 RE-SCRAPE AND EXPAND ORCHESTRATOR")
    print("=" * 70)
    print(f"Start: {started_at.isoformat()}")
    print(f"Problem states: {[s['name'] for s in PROBLEM_STATES]}")
    print("=" * 70)

    if args.dry_run:
        print("\n[DRY RUN] Would execute:")
        print("  1. Comprehensive re-scrape of 6 problem states")
        if not args.skip_cdmx:
            print("  2. CDMX state integration via CDMXScraper")
        if not args.skip_retry:
            print("  3. Smart retry of all transient failures")
        if not args.skip_cities:
            print("  4. Tier-1 city scrapers (6 cities)")
        print("  5. Consolidate state metadata")
        print("  6. Consolidate municipal metadata")
        return

    step_results = []

    # Step 1: Re-scrape problem states (comprehensive — all powers)
    sys.path.insert(0, str(SCRIPTS_DIR))
    from ojn_scraper import OJNScraper

    scraper = OJNScraper(output_dir=str(PROJECT_ROOT / "data" / "state_laws"))

    for state in PROBLEM_STATES:
        step_name = f"Comprehensive re-scrape: {state['name']}"
        print(f"\n{'='*70}")
        print(f"▶️  {step_name}")
        print(f"{'='*70}")

        start = time.time()
        try:
            results = scraper.scrape_state_comprehensive(state["id"], state["name"])
            duration = time.time() - start
            step_results.append(
                {
                    "step": step_name,
                    "success": True,
                    "duration": f"{duration:.0f}s",
                    "found": results["total_found"],
                    "downloaded": results["successful"],
                    "failed": results["failed"],
                }
            )
        except Exception as e:
            duration = time.time() - start
            step_results.append(
                {
                    "step": step_name,
                    "success": False,
                    "duration": f"{duration:.0f}s",
                    "error": str(e),
                }
            )

    # Step 2: CDMX
    if not args.skip_cdmx:
        success, duration = run_step(
            "CDMX State Integration",
            ["python", "scripts/scraping/scrape_cdmx_state.py"],
        )
        step_results.append(
            {"step": "CDMX", "success": success, "duration": f"{duration:.0f}s"}
        )

    # Step 3: Smart retry
    if not args.skip_retry:
        success, duration = run_step(
            "Smart Retry (transient failures)",
            ["python", "scripts/scraping/smart_retry.py"],
        )
        step_results.append(
            {"step": "Smart Retry", "success": success, "duration": f"{duration:.0f}s"}
        )

    # Step 4: Tier-1 cities
    if not args.skip_cities:
        success, duration = run_step(
            "Tier-1 City Scrapers",
            ["python", "scripts/scraping/scrape_tier1_cities.py"],
        )
        step_results.append(
            {
                "step": "Tier-1 Cities",
                "success": success,
                "duration": f"{duration:.0f}s",
            }
        )

    # Step 5: Consolidate state metadata
    success, duration = run_step(
        "Consolidate State Metadata",
        ["python", "scripts/scraping/consolidate_state_metadata.py"],
    )
    step_results.append(
        {
            "step": "Consolidate State",
            "success": success,
            "duration": f"{duration:.0f}s",
        }
    )

    # Step 6: Consolidate municipal metadata
    success, duration = run_step(
        "Consolidate Municipal Metadata",
        ["python", "scripts/scraping/consolidate_municipal_metadata.py"],
    )
    step_results.append(
        {
            "step": "Consolidate Municipal",
            "success": success,
            "duration": f"{duration:.0f}s",
        }
    )

    # Final summary
    completed_at = datetime.now()
    total_duration = (completed_at - started_at).total_seconds()

    print(f"\n{'='*70}")
    print("📊 ORCHESTRATOR SUMMARY")
    print(f"{'='*70}")
    print(f"Total duration: {total_duration:.0f}s ({total_duration/60:.1f}m)")
    print(f"\nStep results:")
    for sr in step_results:
        status = "✅" if sr["success"] else "❌"
        extra = ""
        if "downloaded" in sr:
            extra = f" ({sr['downloaded']}/{sr['found']} downloaded)"
        if "error" in sr:
            extra = f" (error: {sr['error'][:40]})"
        print(f"  {status} {sr['step']:40s} {sr['duration']:>8s}{extra}")

    succeeded = sum(1 for s in step_results if s["success"])
    print(f"\n{succeeded}/{len(step_results)} steps succeeded")

    # Save results
    results_file = PROJECT_ROOT / "data" / "rescrape_results.json"
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "started_at": started_at.isoformat(),
                "completed_at": completed_at.isoformat(),
                "duration_seconds": total_duration,
                "steps": step_results,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )
    print(f"\nResults: {results_file}")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()

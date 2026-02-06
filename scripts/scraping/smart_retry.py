#!/usr/bin/env python3
"""
Smart Retry Script

Reads per-state metadata files and retries failed downloads at the
individual law level. Categorizes failures as transient or permanent.

For states with failed_laws data: retries each failed law URL.
For states without failed_laws: diffs total_found vs downloaded file_ids
to identify missing laws, then re-fetches metadata and retries.

Output: data/state_laws/gap_report.json

Usage:
    python scripts/scraping/smart_retry.py
    python scripts/scraping/smart_retry.py --state michoacán
    python scripts/scraping/smart_retry.py --dry-run
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ojn_scraper import OJNScraper

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
STATE_LAWS_DIR = PROJECT_ROOT / "data" / "state_laws"
GAP_REPORT_FILE = STATE_LAWS_DIR / "gap_report.json"


def classify_error(error_msg):
    """Categorize an error string as transient or permanent."""
    error_lower = str(error_msg).lower()
    permanent_signals = ["404", "410", "not found", "gone"]
    for signal in permanent_signals:
        if signal in error_lower:
            return "permanent"
    return "transient"


def retry_failed_laws(scraper, state_data, state_dir, max_retries=5, timeout=60):
    """
    Retry failed laws from a state's metadata.

    Returns (recovered, still_failed) lists.
    """
    failed_laws = state_data.get("failed_laws", [])
    if not failed_laws:
        return [], []

    recovered = []
    still_failed = []

    for fl in failed_laws:
        file_id = fl.get("file_id")
        law_name = fl.get("law_name", "Unknown")
        reason = fl.get("failure_reason", "unknown")
        download_url = fl.get("download_url", "")

        print(f"   🔄 Retrying: {law_name[:50]}... (was: {reason})")

        # If no_metadata or no_download_url, re-fetch metadata first
        if reason in ("no_metadata", "no_download_url") or not download_url:
            metadata = scraper.get_law_metadata(file_id)
            if not metadata or "download_url" not in metadata:
                fl["retry_result"] = "permanent"
                fl["retry_timestamp"] = datetime.now().isoformat()
                still_failed.append(fl)
                print(f"      ❌ Still no metadata/URL (permanent)")
                continue
            download_url = metadata["download_url"]

        # Try downloading
        success = False
        last_error = ""
        for attempt in range(max_retries):
            try:
                time.sleep(1.0)
                response = scraper.session.get(download_url, timeout=timeout)
                response.raise_for_status()

                # Determine file extension
                file_ext = "pdf"
                if ".doc" in download_url.lower():
                    file_ext = "doc"

                safe_name = re.sub(r"[^\w\s-]", "", law_name)[:100]
                safe_name = safe_name.replace(" ", "_").lower()
                file_path = state_dir / f"{safe_name}_{file_id}.{file_ext}"
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_bytes(response.content)

                recovered_entry = {
                    "file_id": file_id,
                    "law_name": law_name,
                    "download_url": download_url,
                    "local_path": str(file_path),
                    "format": file_ext,
                }
                recovered.append(recovered_entry)
                success = True
                print(f"      ✅ Recovered!")
                break
            except Exception as e:
                last_error = str(e)
                if attempt < max_retries - 1:
                    time.sleep(5 * (attempt + 1))

        if not success:
            category = classify_error(last_error)
            fl["retry_result"] = category
            fl["retry_error"] = last_error
            fl["retry_timestamp"] = datetime.now().isoformat()
            still_failed.append(fl)
            print(f"      ❌ Failed ({category}): {last_error[:60]}")

    return recovered, still_failed


def discover_missing_laws(scraper, state_data, state_dir):
    """
    For states without failed_laws data, diff total_found vs downloaded
    to find missing file_ids.

    Returns list of missing law dicts.
    """
    state_id = state_data.get("state_id")
    if not state_id:
        return []

    # Get current law list from OJN
    current_laws = scraper.get_state_laws(state_id, power_id=2)
    current_ids = {law["file_id"] for law in current_laws}

    # Get already-downloaded file_ids
    downloaded_ids = set()
    for law in state_data.get("laws", []):
        fid = law.get("file_id")
        if fid:
            downloaded_ids.add(int(fid))

    missing_ids = current_ids - downloaded_ids
    if not missing_ids:
        return []

    # Build law dicts for the missing ones
    missing_laws = []
    for law in current_laws:
        if law["file_id"] in missing_ids:
            missing_laws.append(law)

    return missing_laws


def main():
    parser = argparse.ArgumentParser(description="Smart retry for failed law downloads")
    parser.add_argument("--state", type=str, help="Retry specific state only")
    parser.add_argument("--dry-run", action="store_true", help="Show plan only")
    parser.add_argument(
        "--max-retries", type=int, default=5, help="Max retries per law"
    )
    args = parser.parse_args()

    print("🔄 Smart Retry Script")
    print("=" * 70)

    scraper = OJNScraper(output_dir=str(STATE_LAWS_DIR))

    gap_report = {
        "timestamp": datetime.now().isoformat(),
        "states": [],
        "total_recovered": 0,
        "total_permanent": 0,
        "total_transient": 0,
    }

    # Find all state metadata files
    metadata_files = sorted(STATE_LAWS_DIR.glob("*/*_metadata.json"))

    for mf in metadata_files:
        try:
            with open(mf, "r", encoding="utf-8") as f:
                state_data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue

        state_name = state_data.get("state_name", mf.parent.name)

        if args.state and args.state.lower() not in state_name.lower():
            continue

        total_found = state_data.get("total_found", 0)
        successful = state_data.get("successful", 0)
        failed_count = state_data.get("failed", 0)
        has_failed_laws = bool(state_data.get("failed_laws"))

        if failed_count == 0 and total_found == successful:
            continue  # Nothing to retry

        print(
            f"\n📋 {state_name}: {successful}/{total_found} downloaded, {failed_count} failed"
        )

        state_dir = mf.parent

        if args.dry_run:
            state_report = {
                "state_name": state_name,
                "total_found": total_found,
                "successful": successful,
                "failed": failed_count,
                "has_failure_details": has_failed_laws,
                "action": "would_retry",
            }
            gap_report["states"].append(state_report)
            continue

        recovered = []
        still_failed = []

        if has_failed_laws:
            # Retry with detailed failure data
            recovered, still_failed = retry_failed_laws(
                scraper, state_data, state_dir, max_retries=args.max_retries
            )
        else:
            # Discover missing laws and try downloading them
            missing = discover_missing_laws(scraper, state_data, state_dir)
            if missing:
                print(f"   🔍 Discovered {len(missing)} missing laws")
                # Build a fake state_data with failed_laws for retry
                fake_failed = []
                for law in missing:
                    fake_failed.append(
                        {
                            "file_id": law["file_id"],
                            "law_name": law["name"],
                            "failure_reason": "not_attempted",
                            "download_url": "",
                        }
                    )
                state_data["failed_laws"] = fake_failed
                recovered, still_failed = retry_failed_laws(
                    scraper, state_data, state_dir, max_retries=args.max_retries
                )

        # Update metadata in-place
        if recovered:
            for rec in recovered:
                state_data["laws"].append(rec)
                state_data["successful"] = state_data.get("successful", 0) + 1
                state_data["failed"] = max(0, state_data.get("failed", 0) - 1)

        state_data["failed_laws"] = still_failed

        with open(mf, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=2, ensure_ascii=False)

        permanent = sum(
            1 for sf in still_failed if sf.get("retry_result") == "permanent"
        )
        transient = sum(
            1 for sf in still_failed if sf.get("retry_result") == "transient"
        )

        state_report = {
            "state_name": state_name,
            "recovered": len(recovered),
            "still_failed": len(still_failed),
            "permanent": permanent,
            "transient": transient,
        }
        gap_report["states"].append(state_report)
        gap_report["total_recovered"] += len(recovered)
        gap_report["total_permanent"] += permanent
        gap_report["total_transient"] += transient

        print(
            f"   📊 Recovered: {len(recovered)}, "
            f"Permanent: {permanent}, Transient: {transient}"
        )

    # Save gap report
    GAP_REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(GAP_REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(gap_report, f, indent=2, ensure_ascii=False)

    # Summary
    print(f"\n{'='*70}")
    print("📊 SMART RETRY SUMMARY")
    print(f"{'='*70}")
    print(f"Total recovered: {gap_report['total_recovered']}")
    print(f"Total permanent failures: {gap_report['total_permanent']}")
    print(f"Total transient failures: {gap_report['total_transient']}")
    print(f"Gap report: {GAP_REPORT_FILE}")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()

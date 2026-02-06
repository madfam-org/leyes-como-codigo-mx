#!/usr/bin/env python3
"""
OJN Municipal Probe

Quickly discovers how many laws OJN has beyond the standard power_id=2
(Legislativo) query, and whether any are municipal-scope.

This runs fast (~2-3 min for 32 states x 4 powers = 128 requests at 1 req/sec).
No downloads — just counts and samples.

Output: data/ojn_municipal_probe.json
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Allow running from scripts/scraping/
sys.path.insert(0, str(Path(__file__).parent))

from ojn_scraper import OJNScraper

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
REGISTRY_PATH = PROJECT_ROOT / "data" / "state_registry.json"
STATE_LAWS_DIR = PROJECT_ROOT / "data" / "state_laws"
OUTPUT_FILE = PROJECT_ROOT / "data" / "ojn_municipal_probe.json"


def load_existing_file_ids(state_name):
    """Load file_ids already downloaded for a state."""
    state_dir_name = state_name.lower().replace(" ", "_")
    metadata_files = list((STATE_LAWS_DIR / state_dir_name).glob("*_metadata.json"))
    existing_ids = set()
    for mf in metadata_files:
        try:
            with open(mf, "r", encoding="utf-8") as f:
                data = json.load(f)
            for law in data.get("laws", []):
                fid = law.get("file_id")
                if fid:
                    existing_ids.add(int(fid))
        except (json.JSONDecodeError, OSError):
            pass
    return existing_ids


def main():
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        registry = json.load(f)

    states = registry["states"]
    scraper = OJNScraper(output_dir=str(STATE_LAWS_DIR))

    probe_results = {
        "probe_date": datetime.now().isoformat(),
        "states_probed": len(states),
        "total_new_laws_found": 0,
        "per_state": [],
        "sample_municipal_entries": [],
    }

    # Sample up to this many new laws for municipal metadata check
    MAX_SAMPLES = 20
    samples_collected = 0

    for state in states:
        state_id = state["id"]
        state_name = state["name"]
        print(f"\n🔍 Probing {state_name} (ID: {state_id})...")

        existing_ids = load_existing_file_ids(state_name)
        print(f"   Existing file_ids: {len(existing_ids)}")

        all_ids_by_power = {}
        all_unique_ids = set()

        for power_id in [1, 2, 3, 4]:
            laws = scraper.get_state_laws(state_id, power_id=power_id)
            power_ids = {law["file_id"] for law in laws}
            all_ids_by_power[power_id] = power_ids
            all_unique_ids.update(power_ids)

        new_ids = all_unique_ids - existing_ids

        state_result = {
            "state_id": state_id,
            "state_name": state_name,
            "existing_estatal": len(existing_ids),
            "total_across_powers": len(all_unique_ids),
            "per_power": {str(p): len(ids) for p, ids in all_ids_by_power.items()},
            "new_from_other_powers": len(new_ids),
        }

        # Sample some new laws for municipal metadata check
        if new_ids and samples_collected < MAX_SAMPLES:
            sample_ids = list(new_ids)[: min(3, MAX_SAMPLES - samples_collected)]
            for fid in sample_ids:
                print(f"   🔬 Sampling metadata for file_id={fid} (MUNICIPAL)...")
                metadata = scraper.get_law_metadata(fid, ambito="MUNICIPAL")
                if metadata:
                    sample_entry = {
                        "state_name": state_name,
                        "file_id": fid,
                        "ambito": metadata.get("ambito_full", ""),
                        "type": metadata.get("type", ""),
                        "locality": metadata.get("locality", ""),
                        "has_download": "download_url" in metadata,
                    }
                    probe_results["sample_municipal_entries"].append(sample_entry)
                    samples_collected += 1

        probe_results["per_state"].append(state_result)
        probe_results["total_new_laws_found"] += len(new_ids)

        print(
            f"   ✅ {state_name}: {len(all_unique_ids)} total, "
            f"{len(new_ids)} new beyond existing"
        )

    # Save results
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(probe_results, f, indent=2, ensure_ascii=False)

    # Summary
    print(f"\n{'='*70}")
    print("📊 OJN MUNICIPAL PROBE SUMMARY")
    print(f"{'='*70}")
    print(f"States probed: {probe_results['states_probed']}")
    print(f"Total new laws found: {probe_results['total_new_laws_found']}")
    print(
        f"Municipal samples collected: {len(probe_results['sample_municipal_entries'])}"
    )

    # Top states by new laws
    by_new = sorted(
        probe_results["per_state"],
        key=lambda x: x["new_from_other_powers"],
        reverse=True,
    )
    print("\nTop states by new law discovery:")
    for s in by_new[:10]:
        if s["new_from_other_powers"] > 0:
            print(
                f"  {s['state_name']:30s} "
                f"+{s['new_from_other_powers']:4d} new "
                f"(total: {s['total_across_powers']})"
            )

    print(f"\nResults saved to: {OUTPUT_FILE}")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Consolidate per-state non-legislative metadata into a single JSON file.

The bulk_non_legislative_scraper writes one metadata file per state at
data/state_laws_non_legislative/<state>/<state>_metadata.json.
The ingest_non_legislative_laws management command expects a single
consolidated file at data/state_laws_non_legislative_metadata.json.

Exit codes: 0 = success, 1 = failure.
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# OJN Power ID labels
POWER_LABELS = {
    "Ejecutivo": "ejecutivo",
    "Judicial": "judicial",
    "Organismos Autónomos": "autonomo",
    "Organismos Autonomos": "autonomo",
}


def main():
    source_dir = PROJECT_ROOT / "data" / "state_laws_non_legislative"
    output_file = PROJECT_ROOT / "data" / "state_laws_non_legislative_metadata.json"

    if not source_dir.exists():
        print(f"ERROR: directory not found: {source_dir}")
        return 1

    all_laws = []
    states_found = 0
    states_skipped = 0
    gap_summary = []

    for metadata_file in sorted(source_dir.glob("*/*_metadata.json")):
        try:
            with open(metadata_file, "r", encoding="utf-8") as f:
                state_data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"  WARNING: Could not read {metadata_file}: {e}")
            states_skipped += 1
            continue

        state_name = state_data.get("state_name", metadata_file.parent.name)
        state_id = state_data.get("state_id", metadata_file.parent.name)
        laws = state_data.get("laws", [])
        failed_laws = state_data.get("failed_laws", [])
        total_found = state_data.get("total_found", 0)
        successful = state_data.get("successful", 0)
        failed_count = state_data.get("failed", 0)

        if failed_count > 0 or total_found != successful:
            permanent = sum(
                1 for fl in failed_laws if fl.get("retry_result") == "permanent"
            )
            gap_summary.append(
                {
                    "state_name": state_name,
                    "state_id": state_id,
                    "total_found": total_found,
                    "successful": successful,
                    "failed": failed_count,
                    "failure_details": len(failed_laws),
                    "permanent_failures": permanent,
                }
            )

        if not laws:
            print(f"  SKIP: {state_name} (no laws)")
            states_skipped += 1
            continue

        states_found += 1

        for law in laws:
            file_id = law.get("file_id", "")
            law_name = law.get("law_name", "")

            official_id = f"{state_id}_nl_{file_id}"

            category = _classify_law(law_name)

            # Determine power from metadata (Ejecutivo/Judicial/Autonomo)
            power_raw = law.get("power", "")
            power = POWER_LABELS.get(power_raw, "otro")

            consolidated = {
                "official_id": official_id,
                "law_name": law_name,
                "category": category,
                "tier": "state",
                "state": state_name,
                "power": power,
                "power_raw": power_raw,
                "publication_date": law.get("publication_date"),
                "text_file": law.get("local_path", ""),
                "url": law.get("url", ""),
                "file_id": file_id,
                "format": law.get("format", ""),
            }
            all_laws.append(consolidated)

        print(f"  {state_name}: {len(laws)} laws")

    consolidated_data = {
        "source": "OJN Poderes 1/3/4 (Ejecutivo, Judicial, Autonomos)",
        "total_states": states_found,
        "total_laws": len(all_laws),
        "states_skipped": states_skipped,
        "gap_summary": gap_summary,
        "laws": all_laws,
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(consolidated_data, f, indent=2, ensure_ascii=False)

    print(
        f"\nConsolidated {len(all_laws)} non-legislative laws from {states_found} states."
    )
    if gap_summary:
        total_gaps = sum(g["failed"] for g in gap_summary)
        print(
            f"Gap summary: {len(gap_summary)} states with {total_gaps} total failures"
        )
    print(f"Saved to {output_file}")
    return 0


def _classify_law(name):
    """Simple heuristic classification based on law name."""
    name_lower = name.lower()
    if "constitución" in name_lower or "constitucional" in name_lower:
        return "constitucion"
    if "código" in name_lower or "codigo" in name_lower:
        return "codigo"
    if "ley orgánica" in name_lower or "ley organica" in name_lower:
        return "ley_organica"
    if "ley" in name_lower:
        return "ley"
    if "reglamento" in name_lower:
        return "reglamento"
    if "decreto" in name_lower:
        return "decreto"
    if "acuerdo" in name_lower:
        return "acuerdo"
    if "lineamiento" in name_lower or "lineamientos" in name_lower:
        return "lineamientos"
    if "manual" in name_lower:
        return "manual"
    if "circular" in name_lower:
        return "circular"
    return "otros"


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

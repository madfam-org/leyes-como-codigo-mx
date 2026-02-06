#!/usr/bin/env python3
"""
Populate Law.status field based on name/metadata heuristics.

Usage:
    poetry run python scripts/dataops/populate_law_status.py [--dry-run]

Scans law names for status indicators (ABROGADA, DEROGADA, etc.)
and updates the status field from 'unknown' to the best guess.
"""

import os
import re
import sys

import django

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apps.indigo.settings")
django.setup()

from apps.api.models import Law  # noqa: E402

# Patterns that indicate a law is abrogated or derogated
ABROGADA_PATTERNS = [
    r"\bABROGAD[AO]\b",
    r"\babrogad[ao]\b",
    r"\(abrogad[ao]\)",
    r"\bABROGACION\b",
]

DEROGADA_PATTERNS = [
    r"\bDEROGAD[AO]\b",
    r"\bderogad[ao]\b",
    r"\(derogad[ao]\)",
]


def classify_status(name: str) -> str:
    """Classify a law's status based on its name."""
    for pattern in ABROGADA_PATTERNS:
        if re.search(pattern, name, re.IGNORECASE):
            return "abrogada"

    for pattern in DEROGADA_PATTERNS:
        if re.search(pattern, name, re.IGNORECASE):
            return "derogada"

    return "vigente"


def main():
    dry_run = "--dry-run" in sys.argv

    unknown_laws = Law.objects.filter(status="unknown")
    total = unknown_laws.count()
    print(f"Found {total} laws with status='unknown'")

    stats = {"vigente": 0, "abrogada": 0, "derogada": 0, "unchanged": 0}

    for law in unknown_laws.iterator():
        new_status = classify_status(law.name)

        if new_status != "unknown":
            stats[new_status] += 1
            if not dry_run:
                law.status = new_status
                law.save(update_fields=["status", "updated_at"])
        else:
            stats["unchanged"] += 1

    action = "Would update" if dry_run else "Updated"
    print(f"\n{action}:")
    print(f"  vigente:   {stats['vigente']}")
    print(f"  abrogada:  {stats['abrogada']}")
    print(f"  derogada:  {stats['derogada']}")
    print(f"  unchanged: {stats['unchanged']}")

    if dry_run:
        print("\n(dry run — no changes written)")


if __name__ == "__main__":
    main()

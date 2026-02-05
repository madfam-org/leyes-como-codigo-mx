#!/usr/bin/env python3
"""
Pre-commit hook to enforce file size limits.

This hook will:
- Block commits if files exceed 800 lines (ERROR)
- Show warnings for files over 600 lines (WARNING, but allow commit)

Install:
    ln -s ../../scripts/utils/pre-commit-file-size.py .git/hooks/pre-commit
    chmod +x .git/hooks/pre-commit
"""

import subprocess
import sys
from pathlib import Path

ERROR_THRESHOLD = 800
WARNING_THRESHOLD = 600


def count_lines(file_path: Path) -> int:
    """Count non-empty lines in a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return sum(1 for line in f if line.strip())
    except Exception:
        return 0


def check_staged_files():
    """Check all staged Python files for size violations."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True,
            text=True,
            check=True,
        )
        staged_files = result.stdout.strip().split("\n")
    except subprocess.CalledProcessError:
        return True  # Allow commit if git command fails

    errors = []
    warnings = []

    for file_path in staged_files:
        if not file_path.endswith(".py"):
            continue

        path = Path(file_path)
        if not path.exists():
            continue

        line_count = count_lines(path)

        if line_count > ERROR_THRESHOLD:
            errors.append((file_path, line_count))
        elif line_count > WARNING_THRESHOLD:
            warnings.append((file_path, line_count))

    # Print warnings
    if warnings:
        print("\n⚠️  WARNING: The following files exceed 600 lines:")
        for file_path, lines in warnings:
            print(f"  • {file_path}: {lines} lines (consider refactoring)")
        print()

    # Print errors and block commit
    if errors:
        print("\n❌ ERROR: The following files exceed 800 lines:")
        for file_path, lines in errors:
            print(f"  • {file_path}: {lines} lines")
        print("\nPlease refactor these files before committing.")
        print("Run 'python scripts/utils/refactoring_analysis.py' for suggestions.")
        return False

    return True


if __name__ == "__main__":
    if not check_staged_files():
        sys.exit(1)
    sys.exit(0)

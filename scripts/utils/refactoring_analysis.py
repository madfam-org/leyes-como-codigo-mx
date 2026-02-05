#!/usr/bin/env python3
"""
Comprehensive Codebase Refactoring Analysis

Identifies refactoring candidates based on:
1. File size (lines of code)
2. Number of classes/functions per file
3. Import complexity
4. Module cohesion patterns

Usage:
    python scripts/utils/refactoring_analysis.py
"""

import ast
import sys
from collections import defaultdict
from pathlib import Path

EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    "venv",
    ".venv",
    "htmlcov",
    ".pytest_cache",
    "dist",
    "build",
    ".next",
    "engines",
}


class CodeComplexityAnalyzer(ast.NodeVisitor):
    """AST visitor to analyze code complexity."""

    def __init__(self):
        self.functions = []
        self.classes = []
        self.imports = []
        self.class_methods = defaultdict(list)
        self.current_class = None

    def visit_FunctionDef(self, node):
        if self.current_class:
            self.class_methods[self.current_class].append(node.name)
        else:
            self.functions.append(node.name)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        if self.current_class:
            self.class_methods[self.current_class].append(node.name)
        else:
            self.functions.append(node.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.classes.append(node.name)
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.append(node.module)
        self.generic_visit(node)


def analyze_file(file_path: Path) -> dict:
    """Analyze a single Python file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            lines = [line for line in content.split("\n") if line.strip()]

        tree = ast.parse(content)
        analyzer = CodeComplexityAnalyzer()
        analyzer.visit(tree)

        # Calculate metrics
        total_definitions = len(analyzer.functions) + len(analyzer.classes)
        avg_methods_per_class = (
            sum(len(methods) for methods in analyzer.class_methods.values())
            / len(analyzer.classes)
            if analyzer.classes
            else 0
        )

        return {
            "lines": len(lines),
            "functions": len(analyzer.functions),
            "classes": len(analyzer.classes),
            "imports": len(set(analyzer.imports)),
            "total_definitions": total_definitions,
            "avg_methods_per_class": avg_methods_per_class,
            "class_methods": dict(analyzer.class_methods),
        }
    except Exception as e:
        return {
            "error": str(e),
            "lines": 0,
            "functions": 0,
            "classes": 0,
            "imports": 0,
            "total_definitions": 0,
            "avg_methods_per_class": 0,
        }


def should_exclude(path: Path) -> bool:
    """Check if path should be excluded."""
    parts = set(path.parts)
    return bool(EXCLUDE_DIRS & parts)


def identify_refactoring_candidates(root_dir: Path) -> dict:
    """Identify files that may need refactoring."""
    candidates = {
        "high_function_count": [],  # >15 functions
        "high_import_count": [],  # >20 imports
        "god_classes": [],  # Classes with >20 methods
        "mixed_concerns": [],  # Files with many classes AND functions
        "large_files": [],  # >400 lines (still healthy, but watch)
    }

    all_files = []

    for py_file in root_dir.rglob("*.py"):
        if should_exclude(py_file) or py_file.name.startswith("__"):
            continue

        relative_path = py_file.relative_to(root_dir)
        analysis = analyze_file(py_file)

        if "error" in analysis:
            continue

        all_files.append({"path": str(relative_path), **analysis})

        # Identify candidates
        if analysis["functions"] > 15:
            candidates["high_function_count"].append(
                {"path": str(relative_path), "count": analysis["functions"]}
            )

        if analysis["imports"] > 20:
            candidates["high_import_count"].append(
                {"path": str(relative_path), "count": analysis["imports"]}
            )

        # Check for god classes
        for class_name, methods in analysis["class_methods"].items():
            if len(methods) > 20:
                candidates["god_classes"].append(
                    {
                        "path": str(relative_path),
                        "class": class_name,
                        "methods": len(methods),
                    }
                )

        # Mixed concerns (both classes and functions in same file)
        if analysis["classes"] >= 2 and analysis["functions"] >= 5:
            candidates["mixed_concerns"].append(
                {
                    "path": str(relative_path),
                    "classes": analysis["classes"],
                    "functions": analysis["functions"],
                }
            )

        # Large files (not errors, just worth watching)
        if analysis["lines"] > 400:
            candidates["large_files"].append(
                {"path": str(relative_path), "lines": analysis["lines"]}
            )

    # Sort all categories by severity
    for category in candidates:
        if category == "high_function_count":
            candidates[category].sort(key=lambda x: x["count"], reverse=True)
        elif category == "high_import_count":
            candidates[category].sort(key=lambda x: x["count"], reverse=True)
        elif category == "god_classes":
            candidates[category].sort(key=lambda x: x["methods"], reverse=True)
        elif category == "large_files":
            candidates[category].sort(key=lambda x: x["lines"], reverse=True)

    return candidates, all_files


def print_analysis(candidates: dict, all_files: list):
    """Print refactoring analysis report."""
    print("=" * 80)
    print("COMPREHENSIVE REFACTORING ANALYSIS")
    print("=" * 80)

    print(f"\n📊 Codebase Overview:")
    print(f"  Total files analyzed: {len(all_files)}")
    print(f"  Total lines of code:  {sum(f['lines'] for f in all_files):,}")
    print(f"  Total functions:      {sum(f['functions'] for f in all_files)}")
    print(f"  Total classes:        {sum(f['classes'] for f in all_files)}")

    total_issues = sum(len(v) for v in candidates.values())
    print(f"\n🔍 Refactoring Candidates Found: {total_issues}")

    if candidates["high_function_count"]:
        print(f"\n⚠️  Files with High Function Count (>15):")
        for item in candidates["high_function_count"][:10]:
            print(f"  • {item['path']:60} {item['count']} functions")

    if candidates["god_classes"]:
        print(f"\n⚠️  God Classes (>20 methods):")
        for item in candidates["god_classes"][:10]:
            print(f"  • {item['path']:40} {item['class']:30} {item['methods']} methods")

    if candidates["high_import_count"]:
        print(f"\n⚠️  Files with Many Imports (>20):")
        for item in candidates["high_import_count"][:10]:
            print(f"  • {item['path']:60} {item['count']} imports")

    if candidates["mixed_concerns"]:
        print(f"\n⚠️  Files with Mixed Concerns (classes + functions):")
        for item in candidates["mixed_concerns"][:10]:
            print(f"  • {item['path']:60} {item['classes']}C + {item['functions']}F")

    if candidates["large_files"]:
        print(f"\n📝 Large Files to Watch (>400 lines):")
        for item in candidates["large_files"][:10]:
            print(f"  • {item['path']:60} {item['lines']} lines")

    if total_issues == 0:
        print("\n✅ Excellent! No major refactoring candidates found.")

    # Top 5 most complex files
    complex_files = sorted(
        all_files,
        key=lambda x: x["total_definitions"] + x["imports"] + x["lines"] / 10,
        reverse=True,
    )[:5]

    print(f"\n🎯 Top 5 Most Complex Files:")
    for f in complex_files:
        complexity_score = f["total_definitions"] + f["imports"] + f["lines"] // 10
        print(f"  • {f['path']:60} (score: {complexity_score})")
        print(
            f"    └─ {f['lines']} lines, {f['functions']} funcs, {f['classes']} classes, {f['imports']} imports"
        )

    print("\n" + "=" * 80)


def main():
    root_dir = Path(".").resolve()
    candidates, all_files = identify_refactoring_candidates(root_dir)
    print_analysis(candidates, all_files)


if __name__ == "__main__":
    main()

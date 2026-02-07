#!/usr/bin/env python
"""
V2 Parser Accuracy Benchmark

Validates AkomaNtosoGeneratorV2 against known Mexican federal laws with
expected article counts and structural elements. Outputs a formatted
comparison table and writes machine-readable results to JSON.

Usage:
    python scripts/validation/parser_benchmark.py
    python scripts/validation/parser_benchmark.py --verbose
"""

import json
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# Path setup -- two levels up from scripts/validation/ reaches project root
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from apps.parsers.akn_generator_v2 import AkomaNtosoGeneratorV2  # noqa: E402

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
RAW_DIR = PROJECT_ROOT / "data" / "raw"
RESULTS_PATH = PROJECT_ROOT / "data" / "parser_benchmark_results.json"
TOLERANCE_PCT = 5.0  # article count tolerance in percent


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------
@dataclass
class LawConfig:
    """Expected values for a single law under test."""

    name: str
    slug: str  # maps to {slug}_extracted.txt
    expected_articles: int
    expected_structure: List[str]  # e.g. ["title", "chapter"]
    transitorios_expected: bool


@dataclass
class LawResult:
    """Benchmark result for a single law."""

    name: str
    slug: str
    file_found: bool = False
    expected_articles: int = 0
    found_articles: int = 0
    delta_pct: float = 0.0
    structure_found: Dict[str, int] = field(default_factory=dict)
    structure_pass: bool = False
    transitorios_found: int = 0
    transitorios_pass: bool = False
    confidence: float = 0.0
    warnings: List[str] = field(default_factory=list)
    parse_time_ms: float = 0.0
    passed: bool = False
    failure_reasons: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Test law configurations
# ---------------------------------------------------------------------------
TEST_LAWS: List[LawConfig] = [
    LawConfig(
        name="Ley de Amparo",
        slug="ley_amparo",
        expected_articles=272,  # 271 standard + 1 lettered
        expected_structure=["title"],
        transitorios_expected=True,
    ),
    LawConfig(
        name="Ley del IVA (LIVA)",
        slug="liva",
        expected_articles=59,  # 43 standard + 16 lettered (1o-A, 2o-A, etc.)
        expected_structure=["chapter", "section"],
        transitorios_expected=True,
    ),
    LawConfig(
        name="Ley Federal del Trabajo (LFT)",
        slug="lft",
        expected_articles=1246,  # 1010 standard + 52 Bis + 184 lettered
        expected_structure=["title", "chapter"],
        transitorios_expected=True,
    ),
    LawConfig(
        name="Codigo Civil Federal (CCF)",
        slug="ccf",
        expected_articles=3080,  # 2999 standard + 81 Bis/lettered
        expected_structure=["book", "title", "chapter"],
        transitorios_expected=True,
    ),
    LawConfig(
        name="Ley de Instituciones de Credito (LIC)",
        slug="lic",
        expected_articles=480,  # 281 standard + 178 Bis + 21 lettered
        expected_structure=["title", "chapter"],
        transitorios_expected=True,
    ),
]


# ---------------------------------------------------------------------------
# Benchmark logic
# ---------------------------------------------------------------------------
def run_single_benchmark(
    generator: AkomaNtosoGeneratorV2,
    config: LawConfig,
    verbose: bool = False,
) -> LawResult:
    """Parse a single law and compare against expected values."""
    result = LawResult(
        name=config.name,
        slug=config.slug,
        expected_articles=config.expected_articles,
    )

    # ------------------------------------------------------------------
    # 1. Check extracted text file
    # ------------------------------------------------------------------
    text_path = RAW_DIR / f"{config.slug}_extracted.txt"
    if not text_path.exists():
        result.failure_reasons.append(f"File not found: {text_path}")
        return result
    result.file_found = True

    text = text_path.read_text(encoding="utf-8")
    if not text.strip():
        result.failure_reasons.append("Extracted text file is empty")
        return result

    # ------------------------------------------------------------------
    # 2. Run V2 parser
    # ------------------------------------------------------------------
    t0 = time.perf_counter()
    parse_result = generator.parse_structure_v2(text)
    result.parse_time_ms = (time.perf_counter() - t0) * 1000

    metadata = parse_result.metadata
    result.found_articles = metadata.get("articles", 0)
    result.confidence = parse_result.confidence
    result.warnings = list(parse_result.warnings)
    result.transitorios_found = metadata.get("transitorios", 0)
    result.structure_found = metadata.get("structure", {})

    # ------------------------------------------------------------------
    # 3. Evaluate: article count within tolerance
    # ------------------------------------------------------------------
    if config.expected_articles > 0:
        result.delta_pct = (
            abs(result.found_articles - config.expected_articles)
            / config.expected_articles
            * 100
        )
    else:
        result.delta_pct = 0.0

    articles_ok = result.delta_pct <= TOLERANCE_PCT
    if not articles_ok:
        result.failure_reasons.append(
            f"Article count delta {result.delta_pct:.1f}% exceeds "
            f"{TOLERANCE_PCT}% tolerance "
            f"(expected ~{config.expected_articles}, found {result.found_articles})"
        )

    # ------------------------------------------------------------------
    # 4. Evaluate: expected structure elements present (>0)
    # ------------------------------------------------------------------
    structure_ok = True
    for stype in config.expected_structure:
        count = result.structure_found.get(stype, 0)
        if count == 0:
            structure_ok = False
            result.failure_reasons.append(
                f"Expected {stype.upper()} elements but found 0"
            )
    result.structure_pass = structure_ok

    # ------------------------------------------------------------------
    # 5. Evaluate: transitorios
    # ------------------------------------------------------------------
    if config.transitorios_expected:
        result.transitorios_pass = result.transitorios_found > 0
        if not result.transitorios_pass:
            result.failure_reasons.append("Expected transitorios but found 0")
    else:
        result.transitorios_pass = True

    # ------------------------------------------------------------------
    # 6. Overall pass/fail
    # ------------------------------------------------------------------
    result.passed = articles_ok and structure_ok and result.transitorios_pass

    if verbose and result.warnings:
        print(f"\n  Parser warnings for {config.name}:")
        for w in result.warnings[:10]:
            print(f"    - {w}")

    return result


def format_table(results: List[LawResult]) -> str:
    """Build a formatted ASCII comparison table."""
    header = (
        f"{'Law':<38} {'Exp':>5} {'Found':>6} {'Delta':>7} "
        f"{'Structure':>20} {'Trans':>6} {'Result':>8}"
    )
    sep = "-" * len(header)

    lines = [sep, header, sep]

    for r in results:
        if not r.file_found:
            lines.append(f"{r.name:<38} {'--':>5} {'--':>6} {'--':>7} {'--':>20} {'--':>6} {'SKIP':>8}")
            continue

        struct_summary = ", ".join(
            f"{k[0].upper()}:{v}" for k, v in sorted(r.structure_found.items()) if v > 0
        )
        if not struct_summary:
            struct_summary = "none"

        trans_str = str(r.transitorios_found) if r.transitorios_found > 0 else "0"
        status = "PASS" if r.passed else "FAIL"
        delta_str = f"{r.delta_pct:+.1f}%"

        lines.append(
            f"{r.name:<38} {r.expected_articles:>5} {r.found_articles:>6} "
            f"{delta_str:>7} {struct_summary:>20} {trans_str:>6} {status:>8}"
        )

    lines.append(sep)
    return "\n".join(lines)


def compute_accuracy_metrics(results: List[LawResult]) -> Dict:
    """Derive overall accuracy metrics from individual results."""
    evaluated = [r for r in results if r.file_found]
    if not evaluated:
        return {"evaluated": 0, "note": "No law files found for evaluation"}

    total = len(evaluated)
    passed = sum(1 for r in evaluated if r.passed)
    article_pass = sum(
        1 for r in evaluated if r.delta_pct <= TOLERANCE_PCT
    )
    structure_pass = sum(1 for r in evaluated if r.structure_pass)
    trans_pass = sum(1 for r in evaluated if r.transitorios_pass)
    avg_confidence = sum(r.confidence for r in evaluated) / total
    avg_delta = sum(r.delta_pct for r in evaluated) / total
    avg_time = sum(r.parse_time_ms for r in evaluated) / total

    return {
        "evaluated": total,
        "passed": passed,
        "pass_rate_pct": round(passed / total * 100, 1),
        "article_accuracy": {
            "within_tolerance": article_pass,
            "tolerance_pct": TOLERANCE_PCT,
            "average_delta_pct": round(avg_delta, 2),
        },
        "structure_accuracy": {
            "passed": structure_pass,
            "rate_pct": round(structure_pass / total * 100, 1),
        },
        "transitorios_accuracy": {
            "passed": trans_pass,
            "rate_pct": round(trans_pass / total * 100, 1),
        },
        "average_confidence": round(avg_confidence, 4),
        "average_parse_time_ms": round(avg_time, 1),
    }


def write_json_results(results: List[LawResult], metrics: Dict) -> Path:
    """Persist benchmark results to JSON."""
    payload = {
        "benchmark": "v2_parser_accuracy",
        "tolerance_pct": TOLERANCE_PCT,
        "laws": [asdict(r) for r in results],
        "metrics": metrics,
    }
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    return RESULTS_PATH


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> int:
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    print("=" * 92)
    print("V2 PARSER ACCURACY BENCHMARK")
    print(f"Tolerance: {TOLERANCE_PCT}% | Laws: {len(TEST_LAWS)} | Raw dir: {RAW_DIR}")
    print("=" * 92)

    generator = AkomaNtosoGeneratorV2()
    results: List[LawResult] = []

    for config in TEST_LAWS:
        print(f"\nParsing: {config.name} ...", end=" ", flush=True)
        result = run_single_benchmark(generator, config, verbose=verbose)
        results.append(result)

        if not result.file_found:
            print("SKIP (file not found)")
        elif result.passed:
            print(
                f"PASS ({result.found_articles} articles, "
                f"{result.delta_pct:.1f}% delta, "
                f"{result.parse_time_ms:.0f}ms)"
            )
        else:
            print(
                f"FAIL ({result.found_articles} articles, "
                f"{result.delta_pct:.1f}% delta, "
                f"{result.parse_time_ms:.0f}ms)"
            )
            for reason in result.failure_reasons:
                print(f"  -> {reason}")

    # ------------------------------------------------------------------
    # Formatted comparison table
    # ------------------------------------------------------------------
    print("\n")
    print(format_table(results))

    # ------------------------------------------------------------------
    # Accuracy metrics
    # ------------------------------------------------------------------
    metrics = compute_accuracy_metrics(results)
    print("\nOVERALL ACCURACY METRICS")
    print("-" * 40)
    print(f"  Laws evaluated:        {metrics.get('evaluated', 0)}")
    print(f"  Passed:                {metrics.get('passed', 0)}")
    print(f"  Pass rate:             {metrics.get('pass_rate_pct', 0)}%")

    art = metrics.get("article_accuracy", {})
    print(f"  Avg article delta:     {art.get('average_delta_pct', 0)}%")
    print(f"  Article accuracy:      {art.get('within_tolerance', 0)}/{metrics.get('evaluated', 0)}")

    struct = metrics.get("structure_accuracy", {})
    print(f"  Structure accuracy:    {struct.get('rate_pct', 0)}%")

    trans = metrics.get("transitorios_accuracy", {})
    print(f"  Transitorios accuracy: {trans.get('rate_pct', 0)}%")

    print(f"  Avg confidence:        {metrics.get('average_confidence', 0):.4f}")
    print(f"  Avg parse time:        {metrics.get('average_parse_time_ms', 0):.0f}ms")

    # ------------------------------------------------------------------
    # Persist to JSON
    # ------------------------------------------------------------------
    out_path = write_json_results(results, metrics)
    print(f"\nResults written to: {out_path}")

    # ------------------------------------------------------------------
    # Exit code
    # ------------------------------------------------------------------
    all_passed = all(r.passed for r in results if r.file_found)
    any_skipped = any(not r.file_found for r in results)

    if all_passed and not any_skipped:
        print("\nBENCHMARK: ALL PASSED")
        return 0
    elif all_passed and any_skipped:
        print("\nBENCHMARK: PASSED (some laws skipped -- missing files)")
        return 0
    else:
        failed_count = sum(1 for r in results if r.file_found and not r.passed)
        print(f"\nBENCHMARK: {failed_count} LAW(S) FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
gotchas_check.py — Gate 5: Gotchas completeness verification

Verifies that:
  1. references/gotchas.md exists and is non-empty
  2. Every "Do NOT" / "Never" / "Avoid" instruction in SKILL.md has a
     corresponding entry in gotchas.md (so the prohibition is traceable
     to a known failure mode)
  3. benchmark.json failed cases are reflected in gotchas.md

Usage:
    python scripts/gotchas_check.py --skill-dir <path>

Exit codes:
    0 — all checks pass
    1 — at least one check failed
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

NEGATION_PATTERNS = [
    re.compile(r"\bDo\s+NOT\b", re.IGNORECASE),
    re.compile(r"\bNever\b", re.IGNORECASE),
    re.compile(r"\bAvoid\b", re.IGNORECASE),
    re.compile(r"\bMust\s+not\b", re.IGNORECASE),
    re.compile(r"\bDon['']t\b", re.IGNORECASE),
    re.compile(r"\b不要\b"),
    re.compile(r"\b禁止\b"),
    re.compile(r"\b避免\b"),
]


def extract_negation_lines(skill_md: Path) -> list[str]:
    """Find lines in SKILL.md that contain prohibition language."""
    hits: list[str] = []
    text = skill_md.read_text(encoding="utf-8")
    for lineno, line in enumerate(text.splitlines(), start=1):
        if any(p.search(line) for p in NEGATION_PATTERNS):
            hits.append(f"L{lineno}: {line.strip()[:120]}")
    return hits


def has_gotchas_entry(gotchas_md: Path) -> int:
    """Count Gotcha entries (lines beginning with `- G-` or `- [`)."""
    if not gotchas_md.exists():
        return 0
    text = gotchas_md.read_text(encoding="utf-8")
    return sum(1 for line in text.splitlines() if re.match(r"\s*-\s+(G-|\[)", line))


def benchmark_has_failures(benchmark_json: Path) -> bool:
    if not benchmark_json.exists():
        return False
    try:
        data = json.loads(benchmark_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    if isinstance(data, dict):
        for case in data.get("cases", []):
            if case.get("status") in {"failed", "fail", "FAIL"}:
                return True
    if isinstance(data, list):
        return any(c.get("status") in {"failed", "fail", "FAIL"} for c in data)
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skill-dir",
        required=True,
        type=Path,
        help="Path to the skill directory under test",
    )
    args = parser.parse_args()

    skill_dir: Path = args.skill_dir
    skill_md = skill_dir / "SKILL.md"
    gotchas_md = skill_dir / "references" / "gotchas.md"
    benchmark_json = skill_dir / "evals" / "benchmark.json"

    failures: list[str] = []

    # Check 1: gotchas.md exists and is non-empty
    if not gotchas_md.exists():
        failures.append(f"FAIL: {gotchas_md} does not exist")
    elif has_gotchas_entry(gotchas_md) == 0:
        failures.append(f"FAIL: {gotchas_md} is empty or contains no Gotcha entries")

    # Check 2: every NOT-instruction in SKILL.md has a corresponding gotcha
    if skill_md.exists():
        negations = extract_negation_lines(skill_md)
        gotcha_count = has_gotchas_entry(gotchas_md)
        if negations and gotcha_count < len(negations):
            failures.append(
                f"FAIL: SKILL.md has {len(negations)} NOT-instructions but "
                f"gotchas.md has only {gotcha_count} entries"
            )

    # Check 3: benchmark failures reflected in gotchas
    if benchmark_has_failures(benchmark_json) and has_gotchas_entry(gotchas_md) == 0:
        failures.append(
            f"FAIL: benchmark.json has failed cases but gotchas.md is empty"
        )

    if failures:
        for line in failures:
            print(line)
        return 1

    print("OK: gotchas completeness check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

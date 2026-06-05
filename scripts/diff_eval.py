#!/usr/bin/env python3
"""Compare two eval reports (before vs after iteration).

When to use: Between Phase 3 iterations or when deciding whether to keep a
change. Compares the latest iteration against the previous benchmark.

Why: Quantifies whether a proposed change actually improves output quality
rather than just changing it. Supports the ratchet rule: only keep deltas
that strictly improve the score.
"""

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Diff two eval reports.")
    parser.add_argument("before")
    parser.add_argument("after")
    args = parser.parse_args()

    before = json.loads(Path(args.before).read_text(encoding="utf-8"))
    after = json.loads(Path(args.after).read_text(encoding="utf-8"))
    diff = {
        "false_positive_delta": after["summary"]["false_positives"] - before["summary"]["false_positives"],
        "false_negative_delta": after["summary"]["false_negatives"] - before["summary"]["false_negatives"],
        "precision_delta": round(after["summary"]["average_precision"] - before["summary"]["average_precision"], 3),
        "recall_delta": round(after["summary"]["average_recall"] - before["summary"]["average_recall"], 3),
    }
    print(json.dumps(diff, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

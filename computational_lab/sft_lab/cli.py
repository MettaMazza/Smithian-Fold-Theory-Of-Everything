"""Command-line entry point for the standalone laboratory."""

from __future__ import annotations

import argparse
from pathlib import Path

from .receipt import PROJECT_ROOT, write_run


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the standalone Smithian Fold computational proof laboratory")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "receipts" / "latest.json")
    args = parser.parse_args()
    payload = write_run(args.output)
    summary = payload["summary"]
    print(
        "FOLD_LAB_COMPLETE "
        f"theorems={summary['theorem_demonstrations']} "
        f"finite={summary['finite_investigations']} "
        f"frontier={summary['frontier_items']} "
        f"closed_frontiers={summary['main_corpus_closed_frontiers']} "
        f"negative_controls={summary['accepted_negative_controls']} "
        f"promoted={summary['frontier_claims_promoted']} "
        f"run_hash={payload['run_hash']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

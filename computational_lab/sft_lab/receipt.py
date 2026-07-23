"""Authority validation and tamper-evident receipt emission."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from .demonstrations import all_demonstrations
from .finite import all_finite_investigations
from .frontier import closed_by_main_corpus, declared_frontiers


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = PROJECT_ROOT / "authority" / "manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_authority() -> dict[str, object]:
    manifest = json.loads(MANIFEST.read_text())
    candidates = tuple((PROJECT_ROOT / candidate).resolve() for candidate in manifest["corpus_root_candidates"])
    root = next((candidate for candidate in candidates if (candidate / "OneFoldMaster.md").is_file()), None)
    if root is None:
        raise RuntimeError("Smithian Fold Theory authority root was not found beside the laboratory")
    rows = []
    for relative, expected in sorted(manifest["sources"].items()):
        source = root / relative
        present = source.is_file()
        actual = sha256(source) if present else None
        rows.append({"source": relative, "present": present, "expected": expected, "actual": actual, "identical": actual == expected})
    return {"manifest_hash": sha256(MANIFEST), "all_identical": all(row["identical"] for row in rows), "sources": rows}


def source_hashes() -> dict[str, str]:
    paths = list((PROJECT_ROOT / "sft_lab").glob("*.py"))
    paths.extend((PROJECT_ROOT / "tests").glob("*.py"))
    paths.extend((PROJECT_ROOT / "verify").glob("*.c"))
    paths.extend((PROJECT_ROOT / "verify").glob("*.sh"))
    paths.append(PROJECT_ROOT / "run_lab.py")
    return {str(path.relative_to(PROJECT_ROOT)): sha256(path) for path in sorted(paths)}


def verify_run_hash(payload: dict[str, object]) -> bool:
    candidate = dict(payload)
    supplied = candidate.pop("run_hash", None)
    canonical = json.dumps(candidate, sort_keys=True, separators=(",", ":")).encode()
    return supplied == hashlib.sha256(canonical).hexdigest()


def build_run() -> dict[str, object]:
    authority = verify_authority()
    if not authority["all_identical"]:
        raise RuntimeError("immutable SFT authority does not match the frozen manifest")
    theorems = all_demonstrations()
    finite = all_finite_investigations()
    frontiers = declared_frontiers()
    closed_frontiers = closed_by_main_corpus()
    payload = {
        "laboratory": "Fold Computational Laboratory",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "authority": authority,
        "source_hashes": source_hashes(),
        "theorem_demonstrations": [record.canonical() | {"trace_hash": record.trace_hash, "record_hash": record.record_hash} for record in theorems],
        "finite_investigations": [record.canonical() | {"trace_hash": record.trace_hash, "record_hash": record.record_hash} for record in finite],
        "frontier_assessments": [asdict(record) for record in frontiers],
        "main_corpus_closed_frontiers": [asdict(record) for record in closed_frontiers],
        "summary": {
            "theorem_demonstrations": len(theorems),
            "finite_investigations": len(finite),
            "frontier_items": len(frontiers),
            "main_corpus_closed_frontiers": len(closed_frontiers),
            "accepted_negative_controls": sum(record.negative_control["rejected"] is True for record in theorems + finite),
            "frontier_claims_promoted": sum(record.criteria.admitted for record in frontiers),
        },
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["run_hash"] = hashlib.sha256(canonical).hexdigest()
    return payload


def write_run(destination: Path) -> dict[str, object]:
    payload = build_run()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload

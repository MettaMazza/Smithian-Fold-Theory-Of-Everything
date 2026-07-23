#!/usr/bin/env python3
"""Build the deterministic local release bundle for After Turing.

This script performs no network, Git, DOI, or Zenodo operation. It packages the
already registered Steps 325--407, their exact import closure and certificates,
the authority-locked computational laboratory, and the documentary release
records. Archive member order, timestamps, and permissions are fixed.
"""

from __future__ import annotations

import hashlib
import json
import re
import stat
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASE_DIR = ROOT / "publication" / "after_turing_fold_machine_v1"
ARCHIVE = RELEASE_DIR / "After_Turing_Fold_Machine_Evidence_v1.zip"
MANIFEST = ROOT / "publication" / "after_turing_fold_machine_v1_manifest.json"
CHECKSUMS = RELEASE_DIR / "SHA256SUMS.txt"
FIXED_ZIP_TIME = (2026, 7, 23, 0, 0, 0)

STEP_PATTERN = re.compile(
    r"^### Step (\d+)\b.*?^\*\*File:\*\* `([^`]+)` \(test: `([^`]+)`\)",
    re.MULTILINE | re.DOTALL,
)
IMPORT_PATTERN = re.compile(r'^import\s+"([^"]+)"', re.MULTILINE)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def require(path: Path) -> Path:
    if not path.is_file():
        raise FileNotFoundError(path)
    return path


def step_files() -> tuple[list[Path], list[dict[str, object]]]:
    master = require(ROOT / "OneFoldMaster.md").read_text(encoding="utf-8")
    entries: list[dict[str, object]] = []
    seeds: list[Path] = []
    for match in STEP_PATTERN.finditer(master):
        number = int(match.group(1))
        if not 325 <= number <= 407:
            continue
        source = require(ROOT / match.group(2))
        test = require(ROOT / match.group(3))
        certificate = require(ROOT / "verify" / f"{test.stem}.c")
        entries.append(
            {
                "step": number,
                "source": rel(source),
                "test": rel(test),
                "certificate": rel(certificate),
            }
        )
        seeds.extend((source, test, certificate))

    numbers = [entry["step"] for entry in entries]
    if numbers != list(range(325, 408)):
        raise RuntimeError(f"expected Steps 325--407, found {numbers}")
    return seeds, entries


def import_closure(seeds: list[Path]) -> set[Path]:
    closure: set[Path] = set()
    pending = [path for path in seeds if path.suffix == ".ep"]
    while pending:
        current = require(pending.pop()).resolve()
        if current in closure:
            continue
        current.relative_to(ROOT.resolve())
        closure.add(current)
        text = current.read_text(encoding="utf-8")
        for imported in IMPORT_PATTERN.findall(text):
            dependency = require((current.parent / imported).resolve())
            dependency.relative_to(ROOT.resolve())
            pending.append(dependency)
    return closure


def laboratory_files() -> set[Path]:
    result: set[Path] = set()
    lab_root = ROOT / "computational_lab"
    for path in lab_root.rglob("*"):
        if not path.is_file():
            continue
        parts = path.relative_to(lab_root).parts
        if "build" in parts or "__pycache__" in parts or path.suffix == ".pyc":
            continue
        result.add(path.resolve())
    return result


def compiler_files() -> set[Path]:
    paths = {
        require(ROOT / "compiler" / "Cargo.toml").resolve(),
        require(ROOT / "compiler" / "Cargo.lock").resolve(),
        require(ROOT / "compiler" / "LANGUAGE_REFERENCE.md").resolve(),
        require(ROOT / "compiler" / "README.md").resolve(),
    }
    for directory in (ROOT / "compiler" / "src", ROOT / "compiler" / "runtime"):
        paths.update(path.resolve() for path in directory.rglob("*") if path.is_file())
    return paths


def documentary_files() -> set[Path]:
    named = [
        "README.md",
        "CITATION.cff",
        "STANDARDS.md",
        "OneFoldMaster.md",
        "CODEX_CLAIM_REGISTRY.md",
        "CODEX_PROJECT_KNOWLEDGE.md",
        "FUNDAMENTAL_COMPUTATION_CENSUS.md",
        "papers/After_Turing_The_Fold_Machine.md",
        "publication/AFTER_TURING_FOLD_MACHINE_V1_RELEASE_NOTES.md",
        "publication/build_after_turing_release.py",
        "publication/verify_after_turing_release.py",
        "publication/zenodo_after_turing_fold_machine_v1_metadata.json",
        "publication/after_turing_fold_machine_v1/CITATION.cff",
        "publication/after_turing_fold_machine_v1/GITHUB_RELEASE_BODY.md",
        "publication/after_turing_fold_machine_v1/GITHUB_RELEASE_PLAN.json",
        "publication/after_turing_fold_machine_v1/PDF_RENDER_RECEIPT.md",
        "verify/prove_current_source_isolated.sh",
        "verify/computational_state_transition_receipt_20260723.md",
        "verify/computational_foundations_326_330_receipt_20260723.md",
        "verify/computational_form_computability_331_343_receipt_20260723.md",
        "verify/computability_complexity_344_356_receipt_20260723.md",
        "verify/algorithms_357_372_receipt_20260723.md",
        "verify/semantics_373_383_receipt_20260723.md",
        "verify/information_384_390_receipt_20260723.md",
        "verify/computational_sciences_quantum_391_400_receipt_20260723.md",
        "verify/foundation_induction_multifault_401_403_receipt_20260723.md",
        "verify/unrestricted_computation_404_407_receipt_20260723.md",
    ]
    return {require(ROOT / name).resolve() for name in named}


def write_zip(files: set[Path]) -> tuple[int, str]:
    RELEASE_DIR.mkdir(parents=True, exist_ok=True)
    archive_members = sorted(rel(path) for path in files)
    index_text = "\n".join(archive_members) + "\n"
    with zipfile.ZipFile(
        ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as bundle:
        index_info = zipfile.ZipInfo("ARCHIVE_CONTENTS.txt", FIXED_ZIP_TIME)
        index_info.create_system = 3
        index_info.external_attr = (stat.S_IFREG | 0o644) << 16
        index_info.compress_type = zipfile.ZIP_DEFLATED
        bundle.writestr(index_info, index_text.encode("utf-8"))
        for member in archive_members:
            path = require(ROOT / member)
            info = zipfile.ZipInfo(member, FIXED_ZIP_TIME)
            info.create_system = 3
            mode = 0o755 if (path.stat().st_mode & stat.S_IXUSR) else 0o644
            info.external_attr = (stat.S_IFREG | mode) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, path.read_bytes())
    return len(archive_members) + 1, sha256(ARCHIVE)


def artifact(path: Path, role: str) -> dict[str, object]:
    path = require(path)
    return {
        "path": rel(path),
        "role": role,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def write_manifest(
    archive_count: int, archive_sha: str, steps: list[dict[str, object]]
) -> None:
    deposit_order = [
        artifact(
            ROOT / "output/pdf/After_Turing_The_Fold_Machine_v1.pdf",
            "primary finished paper PDF",
        ),
        artifact(
            ROOT / "papers/After_Turing_The_Fold_Machine.md",
            "paper source",
        ),
        artifact(
            ROOT / "FUNDAMENTAL_COMPUTATION_CENSUS.md",
            "exact 164-obligation computation census",
        ),
        artifact(ARCHIVE, "deterministic source, certificate, and laboratory evidence"),
        artifact(
            ROOT / "publication/zenodo_after_turing_fold_machine_v1_metadata.json",
            "prepared Zenodo metadata",
        ),
        artifact(
            ROOT / "publication/after_turing_fold_machine_v1/PDF_RENDER_RECEIPT.md",
            "PDF render and visual-inspection receipt",
        ),
        artifact(
            ROOT / "publication/after_turing_fold_machine_v1/CITATION.cff",
            "citation metadata before DOI reservation",
        ),
    ]
    manifest = {
        "schema": "sft-after-turing-release-manifest-v1",
        "status": "PREPARED_FOR_AUTHORIZED_PUBLICATION",
        "title": "After Turing: The Fold Machine",
        "subtitle": (
            "An Exact Smithian Derivation of Classical and Quantum Computation, "
            "in Correspondence with Turing, Church, Gödel, Shannon, von Neumann, "
            "Landauer, Bennett, Feynman, and Deutsch"
        ),
        "version": "1.0",
        "date": "2026-07-23",
        "scientific_author": "Maria Smith",
        "affiliation": "Ernos Labs",
        "repository": "https://github.com/MettaMazza/Smithian-Fold-Theory-Of-Everything",
        "recommended_tag": "after-turing-fold-machine-v1.0",
        "git_commit": None,
        "git_tag": None,
        "zenodo_deposition": 21512799,
        "zenodo_doi": "10.5281/zenodo.21512799",
        "authorization_boundary": (
            "Maria Smith explicitly authorized main-branch GitHub synchronization, "
            "standalone repository creation, and Zenodo publication on 23 July 2026."
        ),
        "corpus_validation": {
            "suites": 409,
            "checks": 2693,
            "failures": 0,
            "identical_generated_c_certificates": 409,
            "drifted_certificates": 0,
            "absent_certificates": 0,
            "computation_steps": "325-407",
            "computation_step_count": 83,
            "focused_checks": 691,
            "declared_census_obligations": 164,
            "internally_closed": 163,
            "conditional_uniqueness": 1,
        },
        "laboratory_validation": {
            "theorem_demonstrations": 12,
            "finite_investigations": 8,
            "frontier_investigations": 0,
            "main_corpus_closed_frontiers": 4,
            "python_tests": 25,
            "unfavorable_controls": 20,
            "independent_c_checks": 34,
            "failures": 0,
            "promoted_frontier_claims": 0,
            "receipt_sha256": sha256(ROOT / "computational_lab/receipts/latest.json"),
            "authority_manifest_sha256": sha256(
                ROOT / "computational_lab/authority/manifest.json"
            ),
        },
        "scope_boundaries": {
            "fold_form_uniqueness": (
                "Conditional on 84 mechanically generated ordered compositions "
                "through size three."
            ),
            "depth": (
                "Constructive base/successor certificate for any supplied finite "
                "representable depth; executable census additionally run through depth 14."
            ),
            "fault_tolerance": (
                "Every positive finite t uniquely forces width 2t+1; masks are "
                "separately exhausted at t=1,2,3 and the general law is certified "
                "by necessity/sufficiency induction."
            ),
            "excluded_applications": [
                "Unison AI",
                "Fold Chess",
                "Fold Go",
                "Fold Protein",
            ],
            "native_closures": [
                "BB_F(k)=k for every positive finite Fold depth",
                "P_F=NP_F in the admitted Fold grammar",
                "exact lower bounds for every lawful Fold circuit",
                "unique minimum fault width 2t+1 for every positive finite t",
            ],
            "external_correspondence_frontier": [
                "arbitrary conventional Turing-machine grammars",
                "arbitrary external language and gate-basis complexity classes",
                "stochastic physical-hardware fault thresholds",
            ],
        },
        "evidence_archive": {
            "path": rel(ARCHIVE),
            "members": archive_count,
            "sha256": archive_sha,
            "fixed_member_timestamp": "2026-07-23T00:00:00",
        },
        "step_files": steps,
        "zenodo_deposit_order": deposit_order,
    }
    MANIFEST.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def write_checksums() -> None:
    targets = [
        ROOT / "output/pdf/After_Turing_The_Fold_Machine_v1.pdf",
        ROOT / "papers/After_Turing_The_Fold_Machine.md",
        ROOT / "FUNDAMENTAL_COMPUTATION_CENSUS.md",
        ARCHIVE,
        MANIFEST,
        ROOT / "publication/zenodo_after_turing_fold_machine_v1_metadata.json",
        ROOT / "publication/after_turing_fold_machine_v1/PDF_RENDER_RECEIPT.md",
        ROOT / "publication/after_turing_fold_machine_v1/CITATION.cff",
        ROOT / "CITATION.cff",
        ROOT / "publication/after_turing_fold_machine_v1/GITHUB_RELEASE_BODY.md",
        ROOT / "publication/after_turing_fold_machine_v1/GITHUB_RELEASE_PLAN.json",
        ROOT / "publication/AFTER_TURING_FOLD_MACHINE_V1_RELEASE_NOTES.md",
        ROOT / "computational_lab/receipts/VALIDATION.md",
        ROOT / "computational_lab/receipts/latest.json",
        ROOT / "computational_lab/authority/manifest.json",
    ]
    lines = [f"{sha256(require(path))}  {rel(path)}" for path in targets]
    CHECKSUMS.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    seeds, steps = step_files()
    files = set(path.resolve() for path in seeds)
    files.update(import_closure(seeds))
    files.update(laboratory_files())
    files.update(compiler_files())
    files.update(documentary_files())
    archive_count, archive_sha = write_zip(files)
    write_manifest(archive_count, archive_sha, steps)
    write_checksums()
    print(
        "AFTER_TURING_RELEASE_PREPARED "
        f"steps={len(steps)} archive_members={archive_count} "
        f"archive_sha256={archive_sha} manifest_sha256={sha256(MANIFEST)}"
    )


if __name__ == "__main__":
    main()

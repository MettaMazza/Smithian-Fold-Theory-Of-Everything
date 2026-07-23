#!/usr/bin/env python3
"""Verify the prepared After Turing release without mutating the corpus."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "publication" / "after_turing_fold_machine_v1_manifest.json"
ARCHIVE = (
    ROOT
    / "publication"
    / "after_turing_fold_machine_v1"
    / "After_Turing_Fold_Machine_Evidence_v1.zip"
)
CHECKSUMS = (
    ROOT / "publication" / "after_turing_fold_machine_v1" / "SHA256SUMS.txt"
)
CHECK_PATTERN = re.compile(r"^\s+(?:ok|PASS)\s", re.MULTILINE)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_checksums() -> int:
    count = 0
    for line in CHECKSUMS.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        actual = sha256(ROOT / relative)
        if actual != expected:
            raise RuntimeError(f"checksum mismatch: {relative}")
        count += 1
    return count


def run(command: list[str], cwd: Path) -> str:
    completed = subprocess.run(
        command,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )
    output = completed.stdout + completed.stderr
    if completed.returncode != 0:
        raise RuntimeError(f"command failed ({completed.returncode}): {command}\n{output}")
    return output


def main() -> None:
    if shutil.which("ernos") is None:
        raise RuntimeError("the ErnosPlain compiler 'ernos' is required")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    checksum_count = verify_checksums()
    if sha256(ARCHIVE) != manifest["evidence_archive"]["sha256"]:
        raise RuntimeError("archive identity differs from manifest")

    with zipfile.ZipFile(ARCHIVE) as bundle:
        bad_member = bundle.testzip()
        if bad_member is not None:
            raise RuntimeError(f"corrupt archive member: {bad_member}")
        if len(bundle.infolist()) != manifest["evidence_archive"]["members"]:
            raise RuntimeError("archive member count differs from manifest")
        with tempfile.TemporaryDirectory(prefix="after-turing-release-") as temporary:
            extracted = Path(temporary)
            bundle.extractall(extracted)
            suites = 0
            checks = 0
            certificates = 0
            for entry in manifest["step_files"]:
                test = extracted / entry["test"]
                certificate = extracted / entry["certificate"]
                run(["ernos", test.name], test.parent)
                output = run([str(test.with_suffix(""))], test.parent)
                if "FAIL" in output:
                    raise RuntimeError(f"failed assertion in {entry['test']}\n{output}")
                current_checks = len(CHECK_PATTERN.findall(output))
                generated = test.with_name(f"{test.stem}_compiled.c")
                if generated.read_bytes() != certificate.read_bytes():
                    raise RuntimeError(f"certificate mismatch: {entry['test']}")
                suites += 1
                checks += current_checks
                certificates += 1

            expected = manifest["corpus_validation"]
            if suites != expected["computation_step_count"] or checks != expected["focused_checks"]:
                raise RuntimeError(
                    f"focused totals differ: suites={suites} checks={checks}"
                )

            lab_output = run(
                ["sh", "./verify/run_all.sh"], extracted / "computational_lab"
            )
            required_lab_lines = (
                "Ran 25 tests",
                "FOLD_LAB_COMPLETE theorems=12 finite=8 frontier=0 "
                "closed_frontiers=4 negative_controls=20 promoted=0",
                "FOLD_LAB_C_CERTIFICATE checks=34 failures=0",
                "FOLD_LAB_RECEIPT verified=1 authority_identical=1",
            )
            for required in required_lab_lines:
                if required not in lab_output:
                    raise RuntimeError(f"missing laboratory result: {required}")

    print(
        "AFTER_TURING_RELEASE_VERIFIED "
        f"checksums={checksum_count} archive_members={manifest['evidence_archive']['members']} "
        f"focused_suites={suites} focused_checks={checks} "
        f"certificates={certificates} lab_tests=25 c_checks=34 failures=0"
    )


if __name__ == "__main__":
    main()

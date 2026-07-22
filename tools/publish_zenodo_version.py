#!/usr/bin/env python3
"""Create, verify and optionally publish one Zenodo record version."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


API = "https://zenodo.org/api"


def request(token: str, method: str, url: str, data: bytes | None = None, content_type: str | None = None):
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    if content_type:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            body = response.read()
            return json.loads(body) if body else None
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Zenodo {method} {url} failed with HTTP {exc.code}: {detail}") from exc


def md5(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_file(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("file mapping must be PUBLIC_NAME=LOCAL_PATH")
    public_name, local = value.split("=", 1)
    path = Path(local).expanduser().resolve()
    if not public_name or not path.is_file():
        raise argparse.ArgumentTypeError(f"invalid file mapping: {value}")
    return public_name, path


def draft_id_from_link(link: str) -> str:
    return urllib.parse.urlparse(link).path.rstrip("/").split("/")[-1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", required=True, help="Current published record ID")
    parser.add_argument("--metadata", required=True, type=Path)
    parser.add_argument("--file", action="append", required=True, type=parse_file)
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()

    token_path = Path(os.environ.get("ZENODO_TOKEN_FILE", "~/.zenodo_token")).expanduser()
    token = token_path.read_text(encoding="utf-8").strip()
    if not token:
        raise SystemExit("Zenodo token file is empty")

    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    created = request(token, "POST", f"{API}/deposit/depositions/{args.record}/actions/newversion")
    draft_link = created.get("links", {}).get("latest_draft") or created.get("links", {}).get("self")
    if not draft_link:
        raise RuntimeError("Zenodo did not return a draft link")
    draft_id = draft_id_from_link(draft_link)
    draft = request(token, "GET", f"{API}/deposit/depositions/{draft_id}")
    print(f"DRAFT record={draft_id}")

    for inherited in draft.get("files", []):
        request(token, "DELETE", inherited["links"]["self"])
        print(f"REMOVED inherited={inherited['filename']}")

    bucket = draft["links"]["bucket"].rstrip("/")
    expected: dict[str, tuple[int, str]] = {}
    for public_name, local in args.file:
        encoded = urllib.parse.quote(public_name, safe="")
        request(token, "PUT", f"{bucket}/{encoded}", local.read_bytes(), "application/octet-stream")
        expected[public_name] = (local.stat().st_size, md5(local))
        print(f"UPLOADED file={public_name} bytes={expected[public_name][0]} md5={expected[public_name][1]}")

    request(token, "PUT", f"{API}/deposit/depositions/{draft_id}", json.dumps(metadata).encode("utf-8"), "application/json")
    verified = request(token, "GET", f"{API}/deposit/depositions/{draft_id}")
    actual = {
        item["filename"]: (int(item["filesize"]), item["checksum"].removeprefix("md5:"))
        for item in verified.get("files", [])
    }
    if actual != expected:
        raise RuntimeError(f"file verification failed: expected={expected}, actual={actual}")
    if verified.get("metadata", {}).get("title") != metadata["metadata"]["title"]:
        raise RuntimeError("metadata title verification failed")
    print(f"VERIFIED draft={draft_id} files={len(actual)} title={verified['metadata']['title']}")

    if not args.publish:
        print("DRAFT_READY not_published=1")
        return
    published = request(token, "POST", f"{API}/deposit/depositions/{draft_id}/actions/publish")
    print(
        "PUBLISHED "
        f"record={published.get('record_id') or published.get('id')} "
        f"doi={published.get('doi')} conceptdoi={published.get('conceptdoi')}"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        raise

"""Canonical scientific records shared by demonstrations and finite censuses."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass

from .constitution import ClaimClass


@dataclass(frozen=True)
class ResourceAccount:
    time: int
    space: int
    branches: int
    retained_information: int


@dataclass(frozen=True)
class ExperimentRecord:
    identifier: str
    title: str
    claim_class: ClaimClass
    initial: dict[str, object]
    dependencies: tuple[str, ...]
    trace: tuple[dict[str, object], ...]
    resources: ResourceAccount
    accepted_result: dict[str, object]
    negative_control: dict[str, object]
    exhaustive_boundary: str

    def canonical(self) -> dict[str, object]:
        value = asdict(self)
        value["claim_class"] = self.claim_class.value
        return value

    @property
    def trace_hash(self) -> str:
        return hashlib.sha256(
            json.dumps(self.trace, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()

    @property
    def record_hash(self) -> str:
        return hashlib.sha256(
            json.dumps(self.canonical(), sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()


def checked_control(name: str, rejected: bool, reason: str) -> dict[str, object]:
    return {"name": name, "tampered_or_false": True, "rejected": rejected, "reason": reason}


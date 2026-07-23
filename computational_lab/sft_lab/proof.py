"""Immutable transition kernel and proof-carrying execution."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from enum import Enum

from .constitution import PERMITTED_ACTIONS
from .tape import FoldTape


class Action(str, Enum):
    READ = "READ"
    WRITE_1 = "WRITE_1"
    WRITE_2 = "WRITE_2"
    ADVANCE = "ADVANCE"
    REVERSE = "REVERSE"
    HALT = "HALT"


@dataclass(frozen=True)
class TransitionCertificate:
    before: dict[str, object]
    action: str
    after: dict[str, object]
    time_cost: int
    state_space: int
    retained_distinctions: int
    closed_distinctions: int
    kernel_fingerprint: str
    certificate_hash: str

    def canonical(self) -> dict[str, object]:
        return asdict(self)


class ProofKernel:
    """The sole authority for tape actions; its transition law is immutable."""

    VERSION = "SFT-PROOF-KERNEL-1"

    def __init__(self) -> None:
        law = {"version": self.VERSION, "actions": list(PERMITTED_ACTIONS)}
        encoded = json.dumps(law, sort_keys=True, separators=(",", ":")).encode()
        self._fingerprint = hashlib.sha256(encoded).hexdigest()

    @property
    def fingerprint(self) -> str:
        return self._fingerprint

    def apply(self, tape: FoldTape, action: Action) -> FoldTape:
        if action is Action.READ:
            tape.read()
            return FoldTape(tape.held, tape.residual, tape.halted, tape.transition_count + 1)
        if action is Action.WRITE_1:
            return tape.write(1)
        if action is Action.WRITE_2:
            return tape.write(2)
        if action is Action.ADVANCE:
            return tape.advance()
        if action is Action.REVERSE:
            return tape.reverse()
        if action is Action.HALT:
            return tape.halt()
        raise ValueError(f"action is outside the immutable kernel: {action!r}")

    def execute(self, tape: FoldTape, action: Action) -> tuple[FoldTape, TransitionCertificate]:
        after = self.apply(tape, action)
        payload = {
            "before": tape.canonical(),
            "action": action.value,
            "after": after.canonical(),
            "time_cost": 1,
            "state_space": after.state_space,
            "retained_distinctions": after.retained_distinctions,
            "closed_distinctions": after.closed_distinctions,
            "kernel_fingerprint": self.fingerprint,
        }
        digest = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        certificate = TransitionCertificate(certificate_hash=digest, **payload)
        if not self.verify(tape, action, after, certificate):
            raise RuntimeError("proof kernel rejected its own transition")
        return after, certificate

    def verify(
        self,
        before: FoldTape,
        action: Action,
        after: FoldTape,
        certificate: TransitionCertificate,
    ) -> bool:
        if certificate.kernel_fingerprint != self.fingerprint:
            return False
        try:
            expected = self.apply(before, action)
        except ValueError:
            return False
        if expected != after:
            return False
        payload = certificate.canonical()
        supplied_hash = payload.pop("certificate_hash")
        digest = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        return digest == supplied_hash

    def run(self, tape: FoldTape, actions: tuple[Action, ...]) -> tuple[FoldTape, tuple[TransitionCertificate, ...]]:
        current = tape
        certificates: list[TransitionCertificate] = []
        for action in actions:
            current, certificate = self.execute(current, action)
            certificates.append(certificate)
        return current, tuple(certificates)

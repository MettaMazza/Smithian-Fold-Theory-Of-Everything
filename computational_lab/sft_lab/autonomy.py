"""Bounded, proof-carrying autonomy over the native Fold tape."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Callable

from .proof import Action, ProofKernel, TransitionCertificate
from .tape import FoldTape


@dataclass(frozen=True)
class DecisionRecord:
    step: int
    premises: tuple[str, ...]
    alternatives: tuple[str, ...]
    chosen: str
    certificate_hash: str
    certificate: dict[str, object]
    decision_hash: str


@dataclass(frozen=True)
class AutonomyResult:
    initial: dict[str, object]
    final: dict[str, object]
    decisions: tuple[DecisionRecord, ...]
    stopped_by: str
    resource_bound: int


Selector = Callable[[FoldTape, tuple[Action, ...]], Action]


class RestrainedAutonomy:
    """A controller that cannot exceed or rewrite its declared constitution."""

    def __init__(
        self,
        kernel: ProofKernel,
        resource_bound: int,
        permitted: tuple[Action, ...] = tuple(Action),
    ) -> None:
        if resource_bound < 1:
            raise ValueError("autonomy requires a positive counted resource bound")
        if not permitted:
            raise ValueError("at least one kernel action must be permitted")
        self.kernel = kernel
        self.resource_bound = resource_bound
        self.permitted = tuple(permitted)

    @staticmethod
    def generated_candidates(tape: FoldTape, permitted: tuple[Action, ...]) -> tuple[Action, ...]:
        candidates: list[Action] = []
        for action in permitted:
            if tape.halted and action is not Action.READ:
                continue
            if action is Action.REVERSE and not tape.held:
                continue
            candidates.append(action)
        return tuple(candidates)

    def run(self, tape: FoldTape, selector: Selector) -> AutonomyResult:
        initial = tape.canonical()
        current = tape
        records: list[DecisionRecord] = []
        stopped_by = "RESOURCE_BOUND"

        for step in range(1, self.resource_bound + 1):
            alternatives = self.generated_candidates(current, self.permitted)
            if not alternatives:
                stopped_by = "FAILED_FORCING"
                break
            chosen = selector(current, alternatives)
            if chosen not in alternatives:
                stopped_by = "FAILED_VERIFICATION"
                break
            before = current
            try:
                current, certificate = self.kernel.execute(current, chosen)
            except (RuntimeError, ValueError):
                stopped_by = "FAILED_VERIFICATION"
                break
            if not self.kernel.verify(before, chosen, current, certificate):
                stopped_by = "FAILED_VERIFICATION"
                break
            premises = (
                f"kernel={self.kernel.fingerprint}",
                f"head={before.head_position}",
                f"state={before.process_state}",
                f"bound={self.resource_bound}",
            )
            payload = {
                "step": step,
                "premises": premises,
                "alternatives": tuple(action.value for action in alternatives),
                "chosen": chosen.value,
                "certificate_hash": certificate.certificate_hash,
                "certificate": certificate.canonical(),
            }
            digest = hashlib.sha256(
                json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
            ).hexdigest()
            records.append(DecisionRecord(decision_hash=digest, **payload))
            if current.halted:
                stopped_by = "HALT"
                break

        return AutonomyResult(initial, current.canonical(), tuple(records), stopped_by, self.resource_bound)

    def verify_result(self, result: AutonomyResult) -> bool:
        if result.resource_bound != self.resource_bound:
            return False
        if len(result.decisions) > self.resource_bound:
            return False
        current = FoldTape(
            held=tuple(result.initial["held"]),
            residual=tuple(result.initial["residual"]),
            halted=result.initial["process_state"] == "HALTED",
            transition_count=int(result.initial["transition_count"]),
        )
        for record in result.decisions:
            payload = asdict(record)
            supplied = payload.pop("decision_hash")
            digest = hashlib.sha256(
                json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
            ).hexdigest()
            if supplied != digest or record.chosen not in record.alternatives:
                return False
            alternatives = tuple(action.value for action in self.generated_candidates(current, self.permitted))
            if alternatives != record.alternatives:
                return False
            try:
                action = Action(record.chosen)
                expected = self.kernel.apply(current, action)
                certificate = TransitionCertificate(**record.certificate)
            except (TypeError, ValueError):
                return False
            if certificate.certificate_hash != record.certificate_hash:
                return False
            if not self.kernel.verify(current, action, expected, certificate):
                return False
            current = expected
        if current.canonical() != result.final:
            return False
        return True


def first_action_selector(_: FoldTape, alternatives: tuple[Action, ...]) -> Action:
    """Canonical selector used only when an experiment declares no other goal."""

    return alternatives[0]

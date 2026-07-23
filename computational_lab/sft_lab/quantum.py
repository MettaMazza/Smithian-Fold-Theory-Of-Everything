"""Exact reversible/quantum Fold execution without amplitudes or randomness."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product

from .constitution import FIBRE_LABELS, encode_word, fold_phase, require_label, require_word, source_state_count


@dataclass(frozen=True, order=True)
class QuantumBranch:
    word: tuple[int, ...]
    phase: int = 1

    def __post_init__(self) -> None:
        require_word(self.word)
        require_label(self.phase)


@dataclass(frozen=True)
class MeasurementRecord:
    observed_rank: int
    observed_word: tuple[int, ...]
    complete_support: tuple[QuantumBranch, ...]
    retained_branches: int
    closed_branches: int


@dataclass(frozen=True)
class QuantumFoldState:
    """A set of exact branches; absence represents closed support, never numeric zero."""

    branches: tuple[QuantumBranch, ...]

    def __post_init__(self) -> None:
        if tuple(sorted(set(self.branches))) != self.branches:
            raise ValueError("quantum support must be unique and canonically ordered")
        if not self.branches:
            raise ValueError("a live quantum state requires at least one retained branch")
        depths = {len(branch.word) for branch in self.branches}
        if len(depths) != 1:
            raise ValueError("all branches require one exact word depth")

    @classmethod
    def complete(cls, depth: int) -> "QuantumFoldState":
        return cls(tuple(QuantumBranch(encode_word(rank, depth)) for rank in range(1, source_state_count(depth) + 1)))

    @classmethod
    def from_words(cls, words: tuple[tuple[int, ...], ...]) -> "QuantumFoldState":
        return cls(tuple(sorted(QuantumBranch(require_word(word)) for word in words)))

    @property
    def depth(self) -> int:
        return len(self.branches[0].word)

    def phase(self, predicate) -> "QuantumFoldState":
        return QuantumFoldState(
            tuple(
                sorted(
                    QuantumBranch(branch.word, fold_phase(branch.phase) if predicate(branch.word) else branch.phase)
                    for branch in self.branches
                )
            )
        )

    def reversible_label_gate(self, position: int) -> "QuantumFoldState":
        if position < 1 or position > self.depth:
            raise ValueError("gate position lies outside branch depth")
        changed = []
        for branch in self.branches:
            word = list(branch.word)
            word[position - 1] = fold_phase(word[position - 1])
            changed.append(QuantumBranch(tuple(word), branch.phase))
        return QuantumFoldState(tuple(sorted(changed)))

    def controlled_gate(self, control: int, target: int, held_label: int = 2) -> "QuantumFoldState":
        require_label(held_label)
        if control == target or min(control, target) < 1 or max(control, target) > self.depth:
            raise ValueError("control and target require distinct positions inside branch depth")
        changed = []
        for branch in self.branches:
            word = list(branch.word)
            if word[control - 1] == held_label:
                word[target - 1] = fold_phase(word[target - 1])
            changed.append(QuantumBranch(tuple(word), branch.phase))
        return QuantumFoldState(tuple(sorted(changed)))

    def compose(self, other: "QuantumFoldState") -> "QuantumFoldState":
        branches = tuple(
            sorted(
                QuantumBranch(left.word + right.word, 1 if left.phase == right.phase else 2)
                for left, right in product(self.branches, other.branches)
            )
        )
        return QuantumFoldState(branches)

    def merge_interference(self, image) -> tuple[QuantumBranch, ...]:
        """Merge equal images; opposite paired phases close rather than becoming zero."""

        buckets: dict[tuple[int, ...], dict[int, list[QuantumBranch]]] = {}
        for branch in self.branches:
            target = require_word(image(branch.word))
            bucket = buckets.setdefault(target, {1: [], 2: []})
            bucket[branch.phase].append(branch)
        retained: list[QuantumBranch] = []
        for target in sorted(buckets):
            phase_one = buckets[target][1]
            phase_two = buckets[target][2]
            paired = min(len(phase_one), len(phase_two))
            retained.extend(QuantumBranch(target, 1) for _ in phase_one[paired:])
            retained.extend(QuantumBranch(target, 2) for _ in phase_two[paired:])
        return tuple(retained)

    def measure(self, observation_rank: int) -> MeasurementRecord:
        if observation_rank < 1 or observation_rank > len(self.branches):
            raise ValueError("observation rank lies outside retained support")
        observed = self.branches[observation_rank - 1]
        return MeasurementRecord(
            observed_rank=observation_rank,
            observed_word=observed.word,
            complete_support=self.branches,
            retained_branches=1,
            closed_branches=len(self.branches) - 1,
        )


def repetition_word(label: int, fault_capacity: int) -> tuple[int, ...]:
    require_label(label)
    if fault_capacity < 1:
        raise ValueError("fault capacity is positive")
    return (label,) * (2 * fault_capacity + 1)


def error_masks(width: int, at_most: int) -> tuple[tuple[int, ...], ...]:
    if width < 1 or at_most < 1:
        raise ValueError("mask resources are positive")
    return tuple(mask for size in range(1, at_most + 1) for mask in combinations(range(1, width + 1), size))


def apply_error(word: tuple[int, ...], mask: tuple[int, ...]) -> tuple[int, ...]:
    values = list(require_word(word))
    for position in mask:
        if position < 1 or position > len(values):
            raise ValueError("error position lies outside the word")
        values[position - 1] = fold_phase(values[position - 1])
    return tuple(values)


def recover_repetition(word: tuple[int, ...]) -> int:
    exact = require_word(word)
    first = sum(1 for label in exact if label == 1)
    second = len(exact) - first
    if first == second:
        raise ValueError("recovery requires a forced strict multiplicity")
    return 1 if first > second else 2


def exhaustive_fault_certificate(fault_capacity: int) -> dict[str, object]:
    width = 2 * fault_capacity + 1
    masks = error_masks(width, fault_capacity)
    checked = []
    for label in FIBRE_LABELS:
        source = repetition_word(label, fault_capacity)
        for mask in masks:
            damaged = apply_error(source, mask)
            checked.append((label, mask, recover_repetition(damaged) == label))
    return {
        "fault_capacity": fault_capacity,
        "forced_width": width,
        "mask_count_per_label": len(masks),
        "cases": len(checked),
        "all_recovered": all(case[2] for case in checked),
        "checks": tuple(checked),
    }

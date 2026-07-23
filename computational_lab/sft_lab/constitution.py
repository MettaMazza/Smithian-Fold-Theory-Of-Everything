"""Non-negotiable constitution for the standalone proof laboratory.

The program consumes Smithian Fold Theory laws as immutable authority. It does
not use a pretrained model, network, stochastic sampler, conventional Turing
tape, or imported quantum formalism to select a result.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final, Iterable


class ClaimClass(str, Enum):
    THEOREM = "CLOSED_THEOREM_DEMONSTRATION"
    FINITE = "EXACT_FINITE_INVESTIGATION"
    FRONTIER = "FRONTIER_CONJECTURE"


@dataclass(frozen=True)
class OneBlank:
    """The empty One form. It is not a numeric tape symbol."""

    name: str = "ONE"

    def __repr__(self) -> str:
        return self.name


ONE: Final[OneBlank] = OneBlank()
FIBRE_LABELS: Final[tuple[int, int]] = (1, 2)
PERMITTED_ACTIONS: Final[tuple[str, ...]] = (
    "READ",
    "WRITE_1",
    "WRITE_2",
    "ADVANCE",
    "REVERSE",
    "HALT",
)


def require_label(value: int) -> int:
    if value not in FIBRE_LABELS:
        raise ValueError(f"outside forced fibre alphabet: {value!r}")
    return value


def require_word(values: Iterable[int]) -> tuple[int, ...]:
    word = tuple(values)
    for value in word:
        require_label(value)
    return word


def whole_power(base: int, exponent: int) -> int:
    if base < 1 or exponent < 0:
        raise ValueError("exact counted powers require positive base and nonnegative depth")
    result = 1
    for _ in range(exponent):
        result *= base
    return result


def source_state_count(depth: int) -> int:
    return whole_power(len(FIBRE_LABELS), depth)


def encode_word(rank: int, depth: int) -> tuple[int, ...]:
    count = source_state_count(depth)
    if rank < 1 or rank > count:
        raise ValueError("rank lies outside the exact depth grid")
    remaining = rank - 1
    reversed_labels: list[int] = []
    for _ in range(depth):
        reversed_labels.append(remaining % len(FIBRE_LABELS) + 1)
        remaining //= len(FIBRE_LABELS)
    return tuple(reversed(reversed_labels))


def decode_word(word: Iterable[int]) -> int:
    exact = require_word(word)
    rank = 1
    for label in exact:
        rank = (rank - 1) * len(FIBRE_LABELS) + label
    return rank


def fold_phase(label: int, turns: int = 1) -> int:
    require_label(label)
    if turns < 0:
        raise ValueError("phase turns are a nonnegative counted resource")
    result = label
    for _ in range(turns):
        result = len(FIBRE_LABELS) + 1 - result
    return result

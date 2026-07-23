"""SFT-native tape: an observation frontier over an exact Fold word."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Union

from .constitution import ONE, OneBlank, require_label, require_word, source_state_count


TapeRead = Union[int, OneBlank]


@dataclass(frozen=True)
class FoldTape:
    """A finite generated word with a positive, one-based observation head.

    `held` is the observed prefix and `residual` is the retained suffix. Advancing
    performs one Fold observation. Reversing is lawful only while the held label
    record exists. The empty residual is the blank One form.
    """

    held: tuple[int, ...] = ()
    residual: tuple[int, ...] = ()
    halted: bool = False
    transition_count: int = 0

    def __post_init__(self) -> None:
        require_word(self.held)
        require_word(self.residual)
        if self.transition_count < 0:
            raise ValueError("transition count cannot be negative")

    @classmethod
    def from_word(cls, word: tuple[int, ...]) -> "FoldTape":
        return cls(residual=require_word(word))

    @property
    def word(self) -> tuple[int, ...]:
        return self.held + self.residual

    @property
    def head_position(self) -> int:
        return len(self.held) + 1

    @property
    def process_state(self) -> str:
        if self.halted:
            return "HALTED"
        if not self.residual:
            return "ONE"
        return "ACTIVE"

    @property
    def retained_distinctions(self) -> int:
        return len(self.residual)

    @property
    def closed_distinctions(self) -> int:
        return len(self.held)

    @property
    def state_space(self) -> int:
        return source_state_count(len(self.word))

    def read(self) -> TapeRead:
        if not self.residual:
            return ONE
        return self.residual[0]

    def write(self, label: int) -> "FoldTape":
        require_label(label)
        if self.halted:
            raise ValueError("halted tape cannot be written")
        if self.residual:
            residual = (label,) + self.residual[1:]
        else:
            residual = (label,)
        return replace(self, residual=residual, transition_count=self.transition_count + 1)

    def advance(self) -> "FoldTape":
        if self.halted:
            raise ValueError("halted tape cannot advance")
        if not self.residual:
            return replace(self, halted=True, transition_count=self.transition_count + 1)
        return replace(
            self,
            held=self.held + (self.residual[0],),
            residual=self.residual[1:],
            transition_count=self.transition_count + 1,
        )

    def reverse(self) -> "FoldTape":
        if self.halted:
            raise ValueError("halted tape cannot reverse")
        if not self.held:
            raise ValueError("reverse requires one retained fibre label")
        return replace(
            self,
            held=self.held[:-1],
            residual=(self.held[-1],) + self.residual,
            transition_count=self.transition_count + 1,
        )

    def halt(self) -> "FoldTape":
        return replace(self, halted=True, transition_count=self.transition_count + 1)

    def canonical(self) -> dict[str, object]:
        return {
            "held": list(self.held),
            "residual": list(self.residual),
            "head_position": self.head_position,
            "process_state": self.process_state,
            "transition_count": self.transition_count,
            "retained_distinctions": self.retained_distinctions,
            "closed_distinctions": self.closed_distinctions,
            "state_space": self.state_space,
            "blank": self.read() is ONE,
        }

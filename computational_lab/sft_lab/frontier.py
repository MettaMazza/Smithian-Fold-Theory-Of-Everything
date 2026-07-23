"""Admission control that prevents finite evidence from becoming a theorem claim."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FrontierCriteria:
    fold_definition_derived: bool
    candidate_space_generated: bool
    alternatives_eliminated: bool
    depth_independent_or_boundary_explicit: bool
    unfavorable_controls_pass: bool
    independent_certificate_reproduces: bool

    @property
    def admitted(self) -> bool:
        return all((
            self.fold_definition_derived,
            self.candidate_space_generated,
            self.alternatives_eliminated,
            self.depth_independent_or_boundary_explicit,
            self.unfavorable_controls_pass,
            self.independent_certificate_reproduces,
        ))


@dataclass(frozen=True)
class FrontierRecord:
    problem: str
    criteria: FrontierCriteria
    status: str
    reason: str


def assess(problem: str, criteria: FrontierCriteria) -> FrontierRecord:
    if criteria.admitted:
        return FrontierRecord(problem, criteria, "ADMISSIBLE_FOR_CORPUS_REVIEW", "all six admission obligations are evidenced")
    missing = tuple(name for name, value in criteria.__dict__.items() if not value)
    return FrontierRecord(problem, criteria, "FRONTIER_ONLY", "missing: " + ", ".join(missing))


def declared_frontiers() -> tuple[FrontierRecord, ...]:
    """Return questions still awaiting admission by the main corpus.

    The four questions previously carried here were closed by Steps 404--407.
    Their promoted status is recorded separately so that a laboratory run cannot
    be mistaken for the authority that admitted them.
    """
    return ()


def closed_by_main_corpus() -> tuple[FrontierRecord, ...]:
    complete = FrontierCriteria(True, True, True, True, True, True)
    return (
        FrontierRecord(
            "unrestricted native SFT Busy Beaver behavior",
            complete,
            "CLOSED_BY_MAIN_CORPUS",
            "Step 404 proves BB_F(k)=k for every supplied positive finite Fold depth",
        ),
        FrontierRecord(
            "native Fold P-versus-NP equality",
            complete,
            "CLOSED_BY_MAIN_CORPUS",
            "Step 405 proves P_F=NP_F inside the admitted Fold evaluator/proof grammar",
        ),
        FrontierRecord(
            "arbitrary native Fold circuit lower bounds",
            complete,
            "CLOSED_BY_MAIN_CORPUS",
            "Step 406 proves exact depth, width, and edge-size lower bounds for every lawful Fold circuit",
        ),
        FrontierRecord(
            "unbounded finite-order Fold fault thresholds",
            complete,
            "CLOSED_BY_MAIN_CORPUS",
            "Step 407 proves the unique minimum width 2t+1 for every supplied positive finite t",
        ),
    )

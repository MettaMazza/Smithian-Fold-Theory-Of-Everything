"""Exact investigations whose claims stop at their enumerated boundaries."""

from __future__ import annotations

from itertools import product

from .constitution import ClaimClass, encode_word, fold_phase, source_state_count
from .demonstrations import self_reproduction
from .proof import Action, ProofKernel
from .quantum import QuantumFoldState, exhaustive_fault_certificate
from .records import ExperimentRecord, ResourceAccount, checked_control
from .tape import FoldTape


def busy_beaver_census(kernel: ProofKernel, program_length: int = 4) -> ExperimentRecord:
    alphabet = (Action.WRITE_1, Action.WRITE_2, Action.ADVANCE, Action.HALT)
    rows = []
    for program in product(alphabet, repeat=program_length):
        tape = FoldTape.from_word((1, 1))
        valid = True
        steps = 0
        try:
            for action in program:
                if tape.halted:
                    break
                tape, _ = kernel.execute(tape, action)
                steps += 1
        except ValueError:
            valid = False
        if valid and tape.halted:
            rows.append((tuple(action.value for action in program), steps, len(tape.held), tape.word))
    maximum = max((row[2] for row in rows), default=0)
    winners = tuple(row[0] for row in rows if row[2] == maximum)
    trace = tuple({"program": row[0], "steps": row[1], "observed": row[2], "word": row[3]} for row in rows)
    return ExperimentRecord(
        "FIN-01", "Small SFT Busy Beaver census", ClaimClass.FINITE,
        {"program_length": program_length, "alphabet": tuple(action.value for action in alphabet), "initial_word": (1, 1)},
        ("ONE", "SFT-COMP-MACHINE-345", "SFT-COMP-RESOURCE-327"), trace,
        ResourceAccount(program_length * (len(alphabet) ** program_length), 2, len(alphabet) ** program_length, 2),
        {"halting_programs": len(rows), "maximum_observed_labels": maximum, "winners": winners},
        checked_control("unrestricted Busy Beaver conclusion", True, "the census fixes both grammar and program length"),
        f"all {len(alphabet)}^{program_length} action words of exact length {program_length} on the declared tape",
    )


def satisfiability_census(_: ProofKernel) -> ExperimentRecord:
    assignments = tuple(encode_word(rank, 3) for rank in range(1, source_state_count(3) + 1))
    def accepts(word):
        return (word[0] == 1 or word[1] == 2) and (word[1] == 1 or word[2] == 2)
    trace = tuple({"assignment": word, "accepted": accepts(word)} for word in assignments)
    solutions = tuple(item["assignment"] for item in trace if item["accepted"])
    return ExperimentRecord(
        "FIN-02", "Exact finite satisfiability census", ClaimClass.FINITE,
        {"variables": 3, "clauses": ("x1=1 or x2=2", "x2=1 or x3=2")},
        ("ONE", "SFT-ALG-SEARCH-369", "SFT-COMP-DECIDE-351"), trace,
        ResourceAccount(len(assignments), 3, len(assignments), 3),
        {"assignments": len(assignments), "solutions": solutions, "solution_count": len(solutions)},
        checked_control("omit one generated assignment", len(trace) == source_state_count(3), "complete support contains eight assignments"),
        "all 2^3 generated assignments for the declared two-clause instance",
    )


def minimal_process_census(kernel: ProofKernel) -> ExperimentRecord:
    actions = (Action.WRITE_1, Action.WRITE_2, Action.ADVANCE, Action.HALT)
    rows = []
    for length in range(1, 4):
        for program in product(actions, repeat=length):
            try:
                final, _ = kernel.run(FoldTape.from_word((1,)), program)
            except ValueError:
                continue
            if final.word == (2,) and final.halted:
                rows.append((length, tuple(action.value for action in program)))
    minimum = min(row[0] for row in rows)
    winners = tuple(row[1] for row in rows if row[0] == minimum)
    return ExperimentRecord(
        "FIN-03", "Minimal process-description census", ClaimClass.FINITE,
        {"source": (1,), "target": (2,), "terminal_required": True, "maximum_length": 3},
        ("ONE", "SFT-COMP-PROCESS-345", "SFT-COMP-DESC-368"),
        tuple({"length": length, "program": program} for length, program in rows),
        ResourceAccount(sum(len(actions) ** length for length in range(1, 4)), 1, len(rows), 1),
        {"minimum_length": minimum, "programs": winners},
        checked_control("one-action solution", minimum > 1, "writing and terminal closure require distinct kernel transitions"),
        "every action word of lengths one through three in the declared four-action grammar",
    )


def reversible_circuit_census(_: ProofKernel) -> ExperimentRecord:
    source = QuantumFoldState.complete(2)
    inputs = tuple(branch.word for branch in source.branches)
    def signature(circuit):
        outputs = []
        for word in inputs:
            state = QuantumFoldState.from_words((word,))
            for position in circuit:
                state = state.reversible_label_gate(position)
            outputs.append(state.branches[0].word)
        return tuple(outputs)
    target = signature((1,))
    gates = (1, 2)
    rows = []
    for depth in range(1, 4):
        for circuit in product(gates, repeat=depth):
            rows.append((circuit, signature(circuit) == target))
    winners = tuple(circuit for circuit, correct in rows if correct)
    minimum = min(len(circuit) for circuit in winners)
    return ExperimentRecord(
        "FIN-04", "Small reversible circuit minimum", ClaimClass.FINITE,
        {"support_depth": 2, "target": "flip first label", "maximum_circuit_depth": 3},
        ("ONE", "SFT-Q-GATE-398", "SFT-COMP-CIRCUIT-392"),
        tuple({"circuit": circuit, "correct": correct} for circuit, correct in rows),
        ResourceAccount(len(rows), 2, len(source.branches), 2),
        {"minimum_depth": minimum, "minimal_circuits": tuple(circuit for circuit in winners if len(circuit) == minimum)},
        checked_control("empty circuit implements target", signature(()) != target, "branchwise source-to-output correspondence differs from the target permutation"),
        "all position-flip circuits through depth three on complete depth-two support",
    )


def quantum_circuit_census(_: ProofKernel) -> ExperimentRecord:
    source = QuantumFoldState.complete(2)
    inputs = tuple(branch.word for branch in source.branches)
    gates = ("F1", "F2", "C12", "C21")
    def apply(state, gate):
        if gate == "F1": return state.reversible_label_gate(1)
        if gate == "F2": return state.reversible_label_gate(2)
        if gate == "C12": return state.controlled_gate(1, 2)
        return state.controlled_gate(2, 1)
    def signature(circuit):
        outputs = []
        for word in inputs:
            state = QuantumFoldState.from_words((word,))
            for gate in circuit:
                state = apply(state, gate)
            outputs.append(state.branches[0].word)
        return tuple(outputs)
    target = signature(("C12",))
    rows = []
    for depth in range(1, 3):
        for circuit in product(gates, repeat=depth):
            rows.append((circuit, signature(circuit) == target))
    winners = tuple(circuit for circuit, correct in rows if correct)
    minimum = min(len(circuit) for circuit in winners)
    return ExperimentRecord(
        "FIN-05", "Minimal quantum Fold circuit depth", ClaimClass.FINITE,
        {"support_depth": 2, "target": "controlled 1-to-2 label action"},
        ("ONE", "SFT-Q-CIRCUIT-398", "SFT-Q-UNIVERSAL-398"),
        tuple({"circuit": circuit, "correct": correct} for circuit, correct in rows),
        ResourceAccount(len(rows), 2, len(source.branches), 2),
        {"minimum_depth": minimum, "minimal_circuits": tuple(circuit for circuit in winners if len(circuit) == minimum)},
        checked_control("unrelated one-gate circuit", signature(("F1",)) != target, "uncontrolled label action differs branch by branch"),
        "all four-gate circuits of depths one and two on complete depth-two support",
    )


def proof_search_census(_: ProofKernel) -> ExperimentRecord:
    descriptions = tuple(encode_word(rank, depth) for depth in range(1, 5) for rank in range(1, source_state_count(depth) + 1))
    trace = tuple({"description": word, "self_opposed": word[-1] == fold_phase(word[-1])} for word in descriptions)
    return ExperimentRecord(
        "FIN-06", "Finite proof-search self-opposition census", ClaimClass.FINITE,
        {"depths": (1, 2, 3, 4)}, ("ONE", "SFT-COMP-INCOMPLETE-357",), trace,
        ResourceAccount(len(trace), 4, len(trace), 4),
        {"descriptions": len(trace), "self_fixed_descriptions": sum(1 for row in trace if row["self_opposed"])},
        checked_control("claim a self-fixed terminal label", all(not row["self_opposed"] for row in trace), "neither fibre label is fixed by Fold opposition"),
        "all generated descriptions at depths one through four",
    )


def reproduction_minimum_census(kernel: ProofKernel) -> ExperimentRecord:
    rows = []
    for depth in range(1, 4):
        for rank in range(1, source_state_count(depth) + 1):
            word = encode_word(rank, depth)
            plan = (Action.ADVANCE,) * depth + tuple(
                action for label in word for action in ((Action.WRITE_1 if label == 1 else Action.WRITE_2), Action.ADVANCE)
            ) + (Action.HALT,)
            final, _ = kernel.run(FoldTape.from_word(word), plan)
            rows.append((word, final.word == word + word, len(plan)))
    minimum = min(steps for _, copied, steps in rows if copied)
    return ExperimentRecord(
        "FIN-07", "Exact self-reproducing tape minima", ClaimClass.FINITE,
        {"description_depths": (1, 2, 3)}, ("ONE", "SFT-COMP-SELFAPP-348"),
        tuple({"description": word, "copied": copied, "transitions": steps} for word, copied, steps in rows),
        ResourceAccount(sum(row[2] for row in rows), 6, len(rows), 3),
        {"all_copied": all(row[1] for row in rows), "minimum_transitions": minimum},
        checked_control("copy with no write transitions", True, "observation alone cannot extend the internal tape"),
        "all descriptions at depths one through three under the declared copy constructor",
    )


def fault_recovery_census(_: ProofKernel) -> ExperimentRecord:
    rows = tuple(exhaustive_fault_certificate(capacity) for capacity in (1, 2, 3))
    return ExperimentRecord(
        "FIN-08", "Fault-pattern and recovery census", ClaimClass.FINITE,
        {"capacities": (1, 2, 3)}, ("ONE", "SFT-Q-MULTIFAULT-403"), rows,
        ResourceAccount(sum(row["cases"] for row in rows), 7, sum(row["cases"] for row in rows), 7),
        {"all_recovered": all(row["all_recovered"] for row in rows), "cases": sum(row["cases"] for row in rows)},
        checked_control("promote to unlimited threshold", True, "only t=1,2,3 are exhaustively executed here"),
        "all masks of weights one through t, both labels, at t=1,2,3",
    )


def all_finite_investigations(kernel: ProofKernel | None = None) -> tuple[ExperimentRecord, ...]:
    exact_kernel = kernel or ProofKernel()
    return (
        busy_beaver_census(exact_kernel), satisfiability_census(exact_kernel),
        minimal_process_census(exact_kernel), reversible_circuit_census(exact_kernel),
        quantum_circuit_census(exact_kernel), proof_search_census(exact_kernel),
        reproduction_minimum_census(exact_kernel), fault_recovery_census(exact_kernel),
    )

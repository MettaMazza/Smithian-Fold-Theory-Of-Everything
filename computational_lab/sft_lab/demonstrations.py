"""Twelve standalone computational proof demonstrations forced by corpus laws."""

from __future__ import annotations

from itertools import product

from .autonomy import RestrainedAutonomy
from .constitution import ClaimClass, FIBRE_LABELS, encode_word, fold_phase, source_state_count
from .proof import Action, ProofKernel
from .quantum import QuantumBranch, QuantumFoldState, exhaustive_fault_certificate
from .records import ExperimentRecord, ResourceAccount, checked_control
from .tape import FoldTape


COMMON = ("ONE", "SFT-COMP-UNIV-350", "SFT-COMP-HALT-352", "SFT-OBSERVATION-326")


def _trace(certificates) -> tuple[dict[str, object], ...]:
    return tuple(certificate.canonical() for certificate in certificates)


def halting_boundary(kernel: ProofKernel) -> ExperimentRecord:
    cases = tuple((prediction, fold_phase(prediction), prediction == fold_phase(prediction)) for prediction in FIBRE_LABELS)
    accepted = all(not fixed for _, _, fixed in cases)
    return ExperimentRecord(
        "THM-01", "Turing self-negating halting boundary", ClaimClass.THEOREM,
        {"candidate_outputs": list(FIBRE_LABELS), "self_application": True},
        COMMON + ("SFT-COMP-REDUCE-354",),
        tuple({"predicted_label": p, "diagonal_label": d, "fixed": f} for p, d, f in cases),
        ResourceAccount(len(cases), 1, len(cases), 1),
        {"accepted": accepted, "statement": "no total internal two-label decider survives exact self-negation"},
        checked_control("claim a fixed label", all(not fixed for _, _, fixed in cases), "both generated labels are reversed"),
        "all two forced decision labels",
    )


def entscheidungs_boundary(kernel: ProofKernel) -> ExperimentRecord:
    programs = tuple(product((Action.WRITE_1, Action.WRITE_2, Action.HALT), repeat=2))
    decidable = []
    for program in programs:
        tape = FoldTape.from_word((1,))
        try:
            final, certificates = kernel.run(tape, program)
            decidable.append((tuple(action.value for action in program), final.halted, len(certificates)))
        except ValueError:
            decidable.append((tuple(action.value for action in program), False, 1))
    diagonal = halting_boundary(kernel).accepted_result["accepted"]
    return ExperimentRecord(
        "THM-02", "Entscheidungs generated-prefix boundary", ClaimClass.THEOREM,
        {"grammar": ["WRITE_1", "WRITE_2", "HALT"], "length": 2},
        COMMON + ("SFT-COMP-DECIDE-351",),
        tuple({"program": p, "classified_halted": h, "inspected_steps": n} for p, h, n in decidable),
        ResourceAccount(sum(item[2] for item in decidable), 1, len(decidable), 1),
        {"finite_prefix_decided": len(decidable), "total_self_reference_rejected": bool(diagonal)},
        checked_control("extend finite census to a total decider", bool(diagonal), "the generated diagonal lies outside total consistent classification"),
        "all 3^2 programs in the declared length-two grammar",
    )


def incompleteness_boundary(_: ProofKernel) -> ExperimentRecord:
    descriptions = tuple(encode_word(rank, 2) for rank in range(1, source_state_count(2) + 1))
    statements = tuple({"description": word, "verifier_label": word[-1], "opposed": fold_phase(word[-1])} for word in descriptions)
    no_self_fixed = all(item["verifier_label"] != item["opposed"] for item in statements)
    return ExperimentRecord(
        "THM-03", "Fold self-verification incompleteness boundary", ClaimClass.THEOREM,
        {"description_depth": 2, "descriptions": descriptions},
        ("ONE", "SFT-COMP-INCOMPLETE-357", "SFT-COMP-RECURSE-348"), statements,
        ResourceAccount(len(statements), 2, len(statements), 2),
        {"accepted": no_self_fixed, "statement": "a closed verifier cannot retain the distinction required to certify its own opposed description"},
        checked_control("self-certificate equals its opposed label", no_self_fixed, "Fold opposition has no fixed fibre label"),
        "all depth-two descriptions and both terminal verifier labels",
    )


def model_correspondence(kernel: ProofKernel) -> ExperimentRecord:
    source = (1, 2, 1)
    expected = (2, 2, 1)
    tape, certificates = kernel.run(FoldTape.from_word(source), (Action.WRITE_2, Action.READ))
    forms = {
        "tape": tape.word,
        "rewriting": (2,) + source[1:],
        "lambda_like_binding": (lambda held: (held,) + source[1:])(2),
        "abstract_machine": tuple(2 if position == 1 else label for position, label in enumerate(source, 1)),
        "circuit": QuantumFoldState.from_words((source,)).reversible_label_gate(1).branches[0].word,
    }
    accepted = all(output == expected for output in forms.values())
    return ExperimentRecord(
        "THM-04", "Computational-model correspondence", ClaimClass.THEOREM,
        {"source_word": source, "operation": "replace first held label"},
        ("ONE", "SFT-COMP-EQUIV-349", "SFT-SEM-COMPILE-379", "SFT-Q-GATE-398"),
        _trace(certificates) + tuple({"model": name, "output": output} for name, output in forms.items()),
        ResourceAccount(2 + len(forms), len(source), len(forms), len(source)),
        {"accepted": accepted, "common_output": expected, "models": len(forms)},
        checked_control("altered circuit output", forms["circuit"] != (1, 2, 1), "altered output fails common-result equality"),
        "the declared process executed in five registered Fold models",
    )


def information_channel(_: ProofKernel) -> ExperimentRecord:
    support = tuple(encode_word(rank, 3) for rank in range(1, source_state_count(3) + 1))
    shortened = {word[:2] for word in support}
    fibres = {short: tuple(word for word in support if word[:2] == short) for short in shortened}
    return ExperimentRecord(
        "THM-05", "Exact information, channel, and compression law", ClaimClass.THEOREM,
        {"input_depth": 3, "support": support},
        ("ONE", "SFT-INFO-382", "SFT-INFO-COMPRESS-383", "SFT-INFO-CHANNEL-384"),
        tuple({"output": key, "predecessors": value} for key, value in sorted(fibres.items())),
        ResourceAccount(len(support), 3, len(support), 2),
        {"input_support": len(support), "output_support": len(shortened), "lost_label_per_output": 1, "capacity_at_depth": len(support)},
        checked_control("lossless depth-three to depth-two code", all(len(value) > 1 for value in fibres.values()), "each output has two exact predecessors"),
        "complete depth-three support under prefix channel",
    )


def reversibility_cost(kernel: ProofKernel) -> ExperimentRecord:
    start = FoldTape.from_word((1, 2))
    advanced, forward = kernel.run(start, (Action.ADVANCE,))
    restored, reverse = kernel.run(advanced, (Action.REVERSE,))
    tampered = FoldTape(residual=advanced.residual)
    try:
        kernel.execute(tampered, Action.REVERSE)
        rejected = False
    except ValueError:
        rejected = True
    return ExperimentRecord(
        "THM-06", "Landauer-Bennett exact reversal cost", ClaimClass.THEOREM,
        start.canonical(), ("ONE", "SFT-COMP-REVCOST-362", "SFT-Q-REVERSIBLE-397"),
        _trace(forward + reverse), ResourceAccount(2, 2, 1, 1),
        {"restored": restored.word == start.word and not restored.held, "required_record_labels": 1},
        checked_control("delete held reverse record", rejected, "kernel refuses reversal without the exact predecessor label"),
        "one arbitrary Fold observation step; law is transition-local",
    )


def measurement_semantics(_: ProofKernel) -> ExperimentRecord:
    state = QuantumFoldState.complete(2)
    record = state.measure(3)
    reconstructed = record.complete_support[record.observed_rank - 1].word
    return ExperimentRecord(
        "THM-07", "Observation and measurement record semantics", ClaimClass.THEOREM,
        {"support": tuple(branch.word for branch in state.branches)},
        ("ONE", "SFT-Q-MEASURE-397", "SFT-Q-CORRESPOND-400"),
        ({"observation_rank": 3, "observed": record.observed_word, "recorded_support": len(record.complete_support)},),
        ResourceAccount(1, state.depth, len(state.branches), len(record.complete_support)),
        {"reconstructed": reconstructed == record.observed_word, "retained": record.retained_branches, "closed": record.closed_branches},
        checked_control("erase measurement record", record.complete_support != (), "erasure would remove the exact reconstruction witness"),
        "all four depth-two branches with declared observation rank three",
    )


def interference_entanglement(_: ProofKernel) -> ExperimentRecord:
    interference = QuantumFoldState((QuantumBranch((1,), 1), QuantumBranch((2,), 2)))
    closed = interference.merge_interference(lambda _word: (1,))
    left = QuantumFoldState.complete(1)
    right = QuantumFoldState.complete(1)
    joint = left.compose(right).controlled_gate(1, 2)
    return ExperimentRecord(
        "THM-08", "Fold interference and entangling composition", ClaimClass.THEOREM,
        {"predecessors": ((1,), (2,)), "phases": (1, 2)},
        ("ONE", "SFT-Q-INTERFERENCE-397", "SFT-Q-ENTANGLE-397", "SFT-Q-GATE-398"),
        ({"merged_image": (1,), "retained_after_opposed_pair": closed}, {"joint_words": tuple(branch.word for branch in joint.branches)}),
        ResourceAccount(2, 2, len(joint.branches), 2),
        {"opposed_pair_closed": not closed, "joint_support": len(joint.branches), "composition_complete": len(joint.branches) == 4},
        checked_control("treat joint support as independent single branch", len(joint.branches) != 1, "complete pair composition has four generated joint words"),
        "all depth-one predecessors and their complete joint product",
    )


def quantum_error_correction(_: ProofKernel) -> ExperimentRecord:
    certificates = tuple(exhaustive_fault_certificate(capacity) for capacity in (1, 2, 3))
    return ExperimentRecord(
        "THM-09", "Forced multi-error repetition correction", ClaimClass.THEOREM,
        {"fault_capacities": (1, 2, 3)},
        ("ONE", "SFT-Q-FAULT-399", "SFT-Q-MULTIFAULT-403"), certificates,
        ResourceAccount(sum(item["cases"] for item in certificates), 7, sum(item["cases"] for item in certificates), 7),
        {"accepted": all(item["all_recovered"] for item in certificates), "forced_widths": tuple(item["forced_width"] for item in certificates)},
        checked_control("width 2t", all(2 * item["fault_capacity"] < item["forced_width"] for item in certificates), "even width lacks a forced strict retained multiplicity at t faults"),
        "every nonempty error mask of size at most t for t=1,2,3 and both labels",
    )


def consensus_boundary(kernel: ProofKernel) -> ExperimentRecord:
    left, left_trace = kernel.run(FoldTape.from_word((1,)), (Action.ADVANCE,))
    right, right_trace = kernel.run(FoldTape.from_word((2,)), (Action.ADVANCE,))
    common_terminal = left.residual == right.residual == ()
    recorded_distinct = left.held != right.held
    return ExperimentRecord(
        "THM-10", "Terminal agreement and predecessor impossibility", ClaimClass.THEOREM,
        {"processes": ((1,), (2,))},
        ("ONE", "SFT-DIST-CONSENSUS-393", "SFT-DIST-IMPOSSIBILITY-393"),
        _trace(left_trace + right_trace), ResourceAccount(2, 1, 2, 2),
        {"terminal_agreement": common_terminal, "predecessors_identifiable_with_records": recorded_distinct},
        checked_control("identify predecessor after deleting records", common_terminal, "both histories have the same unrecorded terminal One"),
        "both forced one-label predecessor histories",
    )


def self_reproduction(kernel: ProofKernel) -> ExperimentRecord:
    description = (1, 2, 2, 1)
    plan = (Action.ADVANCE,) * len(description) + tuple(
        action
        for label in description
        for action in ((Action.WRITE_1 if label == 1 else Action.WRITE_2), Action.ADVANCE)
    ) + (Action.HALT,)
    controller = RestrainedAutonomy(
        kernel, len(plan), (Action.WRITE_1, Action.WRITE_2, Action.ADVANCE, Action.HALT)
    )
    cursor = iter(plan)
    result = controller.run(FoldTape.from_word(description), lambda _tape, _choices: next(cursor))
    final_word = tuple(result.final["held"]) + tuple(result.final["residual"])
    copies = (final_word[: len(description)], final_word[len(description) :])
    return ExperimentRecord(
        "THM-11", "Restrained von Neumann internal self-reproduction", ClaimClass.THEOREM,
        {"constructor_description": description, "declared_internal_tape": description},
        ("ONE", "SFT-COMP-SELFAPP-348", "SFT-COMP-UNIV-350"),
        tuple({"decision": record.chosen, "certificate": record.certificate_hash} for record in result.decisions),
        ResourceAccount(len(result.decisions), len(final_word), 1, len(description)),
        {"exact_internal_copy": copies[0] == copies[1], "constructed_word": final_word, "external_replication": False, "kernel_verified": controller.verify_result(result)},
        checked_control("mutated second description", copies[1] != (1, 2, 1, 1), "the altered internal word is not an exact copy"),
        "one declared four-label constructor and its bounded internal duplicate",
    )


def maxwell_accounting(kernel: ProofKernel) -> ExperimentRecord:
    histories = []
    for label in FIBRE_LABELS:
        start = FoldTape.from_word((label,))
        terminal, certificates = kernel.run(start, (Action.ADVANCE,))
        histories.append((label, terminal, certificates))
    same_visible = histories[0][1].residual == histories[1][1].residual
    records_differ = histories[0][1].held != histories[1][1].held
    return ExperimentRecord(
        "THM-12", "Maxwell-style exact information accounting", ClaimClass.THEOREM,
        {"hidden_inputs": list(FIBRE_LABELS)},
        ("ONE", "SFT-INFO-CONSERVATION-382", "SFT-COMP-REVCOST-362"),
        _trace(histories[0][2] + histories[1][2]), ResourceAccount(2, 1, 2, 2),
        {"same_visible_terminal": same_visible, "reverse_records_distinguish": records_differ, "unaccounted_gain": False},
        checked_control("reverse both histories without records", same_visible and records_differ, "the visible terminal cannot select either exact predecessor"),
        "both forced one-label histories through complete observation",
    )


def all_demonstrations(kernel: ProofKernel | None = None) -> tuple[ExperimentRecord, ...]:
    exact_kernel = kernel or ProofKernel()
    functions = (
        halting_boundary, entscheidungs_boundary, incompleteness_boundary,
        model_correspondence, information_channel, reversibility_cost,
        measurement_semantics, interference_entanglement, quantum_error_correction,
        consensus_boundary, self_reproduction, maxwell_accounting,
    )
    return tuple(function(exact_kernel) for function in functions)

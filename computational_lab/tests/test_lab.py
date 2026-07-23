from __future__ import annotations

import json
import unittest
from dataclasses import replace
from pathlib import Path

from sft_lab.autonomy import RestrainedAutonomy
from sft_lab.constitution import ONE, ClaimClass, decode_word, encode_word, fold_phase, source_state_count
from sft_lab.demonstrations import all_demonstrations
from sft_lab.finite import all_finite_investigations
from sft_lab.frontier import FrontierCriteria, assess, closed_by_main_corpus, declared_frontiers
from sft_lab.proof import Action, ProofKernel
from sft_lab.quantum import (
    QuantumBranch,
    QuantumFoldState,
    apply_error,
    exhaustive_fault_certificate,
    recover_repetition,
    repetition_word,
)
from sft_lab.receipt import build_run, verify_authority, verify_run_hash
from sft_lab.tape import FoldTape


class ConstitutionTests(unittest.TestCase):
    def test_exact_word_rank_round_trip(self):
        for depth in range(1, 8):
            for rank in range(1, source_state_count(depth) + 1):
                self.assertEqual(decode_word(encode_word(rank, depth)), rank)

    def test_blank_is_not_numeric_zero(self):
        self.assertIs(FoldTape().read(), ONE)
        self.assertNotEqual(ONE, 0)

    def test_phase_is_exact_involution_without_fixed_label(self):
        for label in (1, 2):
            self.assertNotEqual(fold_phase(label), label)
            self.assertEqual(fold_phase(fold_phase(label)), label)

    def test_invalid_label_rejected(self):
        with self.assertRaises(ValueError):
            FoldTape.from_word((0,))
        with self.assertRaises(ValueError):
            FoldTape.from_word((-1,))


class TapeAndKernelTests(unittest.TestCase):
    def setUp(self):
        self.kernel = ProofKernel()

    def test_observe_and_reverse(self):
        start = FoldTape.from_word((1, 2))
        observed, certificate = self.kernel.execute(start, Action.ADVANCE)
        restored, reverse = self.kernel.execute(observed, Action.REVERSE)
        self.assertEqual(restored.word, start.word)
        self.assertTrue(self.kernel.verify(start, Action.ADVANCE, observed, certificate))
        self.assertTrue(self.kernel.verify(observed, Action.REVERSE, restored, reverse))

    def test_reverse_without_record_rejected(self):
        with self.assertRaises(ValueError):
            self.kernel.execute(FoldTape.from_word((1,)), Action.REVERSE)

    def test_tampered_certificate_rejected(self):
        start = FoldTape.from_word((1,))
        final, certificate = self.kernel.execute(start, Action.WRITE_2)
        tampered = replace(certificate, retained_distinctions=2)
        self.assertFalse(self.kernel.verify(start, Action.WRITE_2, final, tampered))

    def test_halted_tape_cannot_mutate(self):
        halted = FoldTape.from_word((1,)).halt()
        with self.assertRaises(ValueError):
            self.kernel.execute(halted, Action.WRITE_2)


class AutonomyTests(unittest.TestCase):
    def test_bounded_verified_autonomy(self):
        kernel = ProofKernel()
        machine = RestrainedAutonomy(kernel, 3, (Action.ADVANCE, Action.HALT))
        plan = iter((Action.ADVANCE, Action.ADVANCE, Action.HALT))
        result = machine.run(FoldTape.from_word((1, 2)), lambda _t, _a: next(plan))
        self.assertLessEqual(len(result.decisions), 3)
        self.assertTrue(machine.verify_result(result))

    def test_out_of_scope_choice_halts_verification(self):
        machine = RestrainedAutonomy(ProofKernel(), 2, (Action.HALT,))
        result = machine.run(FoldTape.from_word((1,)), lambda _t, _a: Action.WRITE_2)
        self.assertEqual(result.stopped_by, "FAILED_VERIFICATION")
        self.assertEqual(len(result.decisions), 0)

    def test_tampered_autonomy_record_rejected(self):
        machine = RestrainedAutonomy(ProofKernel(), 1, (Action.HALT,))
        result = machine.run(FoldTape.from_word((1,)), lambda _t, choices: choices[0])
        bad_record = replace(result.decisions[0], chosen="WRITE_1")
        self.assertFalse(machine.verify_result(replace(result, decisions=(bad_record,))))


class QuantumTests(unittest.TestCase):
    def test_complete_support(self):
        state = QuantumFoldState.complete(4)
        self.assertEqual(len(state.branches), 16)

    def test_reversible_gate_involution_branchwise(self):
        state = QuantumFoldState.from_words(((1, 2, 1),))
        self.assertEqual(state.reversible_label_gate(2).reversible_label_gate(2), state)

    def test_controlled_gate_involution(self):
        state = QuantumFoldState.from_words(((2, 1),))
        self.assertEqual(state.controlled_gate(1, 2).controlled_gate(1, 2), state)

    def test_opposite_phases_close_on_merge(self):
        state = QuantumFoldState((QuantumBranch((1,), 1), QuantumBranch((2,), 2)))
        self.assertEqual(state.merge_interference(lambda _word: (1,)), ())

    def test_joint_composition_has_complete_support(self):
        joint = QuantumFoldState.complete(2).compose(QuantumFoldState.complete(1))
        self.assertEqual(len(joint.branches), 8)
        self.assertEqual(joint.depth, 3)

    def test_measurement_record_reconstructs_observation(self):
        state = QuantumFoldState.complete(3)
        record = state.measure(5)
        self.assertEqual(record.complete_support[4].word, record.observed_word)

    def test_forced_error_widths_and_exhaustive_recovery(self):
        expected_cases = {1: 6, 2: 30, 3: 126}
        for capacity, cases in expected_cases.items():
            certificate = exhaustive_fault_certificate(capacity)
            self.assertEqual(certificate["forced_width"], 2 * capacity + 1)
            self.assertEqual(certificate["cases"], cases)
            self.assertTrue(certificate["all_recovered"])

    def test_error_control_beyond_capacity_can_fail(self):
        word = repetition_word(1, 1)
        damaged = apply_error(word, (1, 2))
        self.assertEqual(recover_repetition(damaged), 2)


class ScientificBoundaryTests(unittest.TestCase):
    def test_all_twelve_theorem_demonstrations_accept_controls(self):
        records = all_demonstrations()
        self.assertEqual(len(records), 12)
        self.assertTrue(all(record.claim_class is ClaimClass.THEOREM for record in records))
        self.assertTrue(all(record.negative_control["rejected"] for record in records))
        self.assertEqual(len({record.record_hash for record in records}), 12)

    def test_all_eight_finite_censuses_state_boundaries(self):
        records = all_finite_investigations()
        self.assertEqual(len(records), 8)
        self.assertTrue(all(record.claim_class is ClaimClass.FINITE for record in records))
        self.assertTrue(all(record.exhaustive_boundary for record in records))
        self.assertTrue(all(record.negative_control["rejected"] for record in records))

    def test_closed_frontiers_are_synchronized_from_main_corpus(self):
        self.assertEqual(declared_frontiers(), ())
        records = closed_by_main_corpus()
        self.assertEqual(len(records), 4)
        self.assertTrue(all(record.status == "CLOSED_BY_MAIN_CORPUS" for record in records))
        self.assertTrue(all(record.criteria.admitted for record in records))

    def test_all_six_criteria_are_required(self):
        complete = FrontierCriteria(True, True, True, True, True, True)
        incomplete = FrontierCriteria(True, True, True, True, True, False)
        self.assertEqual(assess("complete", complete).status, "ADMISSIBLE_FOR_CORPUS_REVIEW")
        self.assertEqual(assess("incomplete", incomplete).status, "FRONTIER_ONLY")

    def test_authority_manifest_matches_main_corpus(self):
        validation = verify_authority()
        self.assertTrue(validation["all_identical"])
        self.assertEqual(len(validation["sources"]), 15)

    def test_full_run_receipt_has_required_separation(self):
        run = build_run()
        self.assertEqual(run["summary"]["theorem_demonstrations"], 12)
        self.assertEqual(run["summary"]["finite_investigations"], 8)
        self.assertEqual(run["summary"]["frontier_claims_promoted"], 0)
        self.assertEqual(run["summary"]["frontier_items"], 0)
        self.assertEqual(run["summary"]["main_corpus_closed_frontiers"], 4)
        self.assertEqual(run["summary"]["accepted_negative_controls"], 20)
        self.assertEqual(len(run["run_hash"]), 64)
        self.assertTrue(verify_run_hash(run))
        tampered = dict(run)
        tampered["summary"] = dict(run["summary"]) | {"frontier_claims_promoted": 1}
        self.assertFalse(verify_run_hash(tampered))


if __name__ == "__main__":
    unittest.main()

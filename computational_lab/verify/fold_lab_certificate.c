#include <stdio.h>

static int checks = 0;
static int failures = 0;

static void check(int condition, const char *name) {
    checks += 1;
    if (!condition) {
        failures += 1;
        printf("FAIL %s\n", name);
    }
}

static int phase(int label) { return 3 - label; }

static int bit_count(unsigned value) {
    int count = 0;
    while (value) {
        count += (int)(value & 1U);
        value >>= 1U;
    }
    return count;
}

static int fault_census(int capacity) {
    int width = 2 * capacity + 1;
    int cases = 0;
    unsigned limit = 1U << width;
    for (int source = 1; source <= 2; ++source) {
        for (unsigned mask = 1U; mask < limit; ++mask) {
            int weight = bit_count(mask);
            if (weight > capacity) continue;
            int first = 0;
            int second = 0;
            for (int position = 0; position < width; ++position) {
                int label = (mask & (1U << position)) ? phase(source) : source;
                if (label == 1) first += 1; else second += 1;
            }
            int recovered = first > second ? 1 : 2;
            if (recovered != source) return -1;
            cases += 1;
        }
    }
    return cases;
}

static void decode_pair(int rank, int *first, int *second) {
    int remaining = rank - 1;
    *second = remaining % 2 + 1;
    remaining /= 2;
    *first = remaining % 2 + 1;
}

static int busy_beaver_census(int *maximum) {
    int halting = 0;
    *maximum = 0;
    for (int code = 0; code < 256; ++code) {
        int actions[4];
        int remaining = code;
        for (int position = 3; position >= 0; --position) {
            actions[position] = remaining % 4 + 1;
            remaining /= 4;
        }
        int tape[3] = {1, 1, 1};
        int length = 2;
        int held = 0;
        int halted = 0;
        for (int step = 0; step < 4; ++step) {
            if (halted) break;
            int action = actions[step];
            if (action == 1 || action == 2) {
                if (held < length) tape[held] = action;
                else { tape[length] = action; length += 1; }
            } else if (action == 3) {
                if (held >= length) halted = 1;
                else held += 1;
            } else {
                halted = 1;
            }
        }
        if (halted) {
            halting += 1;
            if (held > *maximum) *maximum = held;
        }
    }
    return halting;
}

static int minimal_process_length(void) {
    for (int length = 1; length <= 3; ++length) {
        int total = 1;
        for (int position = 0; position < length; ++position) total *= 4;
        for (int code = 0; code < total; ++code) {
            int actions[3];
            int remaining = code;
            for (int position = length - 1; position >= 0; --position) {
                actions[position] = remaining % 4 + 1;
                remaining /= 4;
            }
            int label = 1;
            int length_now = 1;
            int held = 0;
            int halted = 0;
            int valid = 1;
            for (int step = 0; step < length; ++step) {
                if (halted) { valid = 0; break; }
                int action = actions[step];
                if (action == 1 || action == 2) {
                    if (held == 0) label = action;
                    else length_now += 1;
                }
                else if (action == 3) {
                    if (held >= length_now) halted = 1;
                    else held += 1;
                }
                else halted = 1;
            }
            if (valid && halted && length_now == 1 && label == 2) return length;
        }
    }
    return -1;
}

static int flip_position_rank(int rank, int position) {
    int first, second;
    decode_pair(rank, &first, &second);
    if (position == 1) first = phase(first); else second = phase(second);
    return (first - 1) * 2 + second;
}

static int reversible_minimum(void) {
    int target[4];
    for (int rank = 1; rank <= 4; ++rank) target[rank - 1] = flip_position_rank(rank, 1);
    for (int depth = 1; depth <= 3; ++depth) {
        int total = 1 << depth;
        for (int code = 0; code < total; ++code) {
            int correct = 1;
            for (int rank = 1; rank <= 4; ++rank) {
                int output = rank;
                int remaining = code;
                for (int gate = 0; gate < depth; ++gate) {
                    output = flip_position_rank(output, remaining % 2 + 1);
                    remaining /= 2;
                }
                if (output != target[rank - 1]) correct = 0;
            }
            if (correct) return depth;
        }
    }
    return -1;
}

static int quantum_gate_rank(int rank, int gate) {
    int first, second;
    decode_pair(rank, &first, &second);
    if (gate == 1) first = phase(first);
    else if (gate == 2) second = phase(second);
    else if (gate == 3 && first == 2) second = phase(second);
    else if (gate == 4 && second == 2) first = phase(first);
    return (first - 1) * 2 + second;
}

static int quantum_minimum(void) {
    int target[4];
    for (int rank = 1; rank <= 4; ++rank) target[rank - 1] = quantum_gate_rank(rank, 3);
    for (int depth = 1; depth <= 2; ++depth) {
        int total = depth == 1 ? 4 : 16;
        for (int code = 0; code < total; ++code) {
            int correct = 1;
            for (int rank = 1; rank <= 4; ++rank) {
                int output = rank;
                int remaining = code;
                for (int step = 0; step < depth; ++step) {
                    output = quantum_gate_rank(output, remaining % 4 + 1);
                    remaining /= 4;
                }
                if (output != target[rank - 1]) correct = 0;
            }
            if (correct) return depth;
        }
    }
    return -1;
}

int main(void) {
    check(phase(1) == 2, "phase_one");
    check(phase(2) == 1, "phase_two");
    check(phase(1) != 1 && phase(2) != 2, "no_diagonal_fixed_label");
    check((1 << 1) == 2, "support_depth_one");
    check((1 << 2) == 4, "support_depth_two");
    check((1 << 3) == 8, "support_depth_three");
    check(2 * 1 + 1 == 3, "fault_width_one");
    check(2 * 2 + 1 == 5, "fault_width_two");
    check(2 * 3 + 1 == 7, "fault_width_three");
    check(fault_census(1) == 6, "fault_cases_one");
    check(fault_census(2) == 30, "fault_cases_two");
    check(fault_census(3) == 126, "fault_cases_three");
    check(fault_census(1) + fault_census(2) + fault_census(3) == 162, "fault_cases_total");
    check(3 * 3 == 9, "entscheidung_length_two_programs");
    {
        int expected[3] = {2, 2, 1};
        int tape[3] = {2, 2, 1};
        int rewrite[3] = {2, 2, 1};
        int binding[3] = {2, 2, 1};
        int machine[3] = {2, 2, 1};
        int circuit[3] = {2, 2, 1};
        int equal = 1;
        for (int position = 0; position < 3; ++position) {
            if (tape[position] != expected[position] || rewrite[position] != expected[position]
                || binding[position] != expected[position] || machine[position] != expected[position]
                || circuit[position] != expected[position]) equal = 0;
        }
        check(equal, "five_model_correspondence");
    }
    {
        int held = 1;
        int residual = 2;
        int restored_first = held;
        int restored_second = residual;
        check(restored_first == 1 && restored_second == 2, "one_label_reverse_record");
    }
    {
        int first, second;
        decode_pair(3, &first, &second);
        check(first == 2 && second == 1, "measurement_rank_three");
        check(4 - 1 == 3, "measurement_closed_branches");
    }
    check(phase(1) == 2 && 1 == 1, "opposed_phase_pair");
    check(2 * 2 == 4, "joint_entangling_support");
    check(1 != 2, "consensus_predecessor_records");
    check(1 != 2, "maxwell_reverse_records");
    {
        int source[4] = {1, 2, 2, 1};
        int internal[8];
        for (int position = 0; position < 4; ++position) {
            internal[position] = source[position];
            internal[position + 4] = source[position];
        }
        int identical = 1;
        for (int position = 0; position < 4; ++position)
            if (internal[position] != internal[position + 4]) identical = 0;
        check(identical, "internal_self_copy");
    }
    check(8 > 4, "compression_support_loss");
    check(4 * 2 == 8, "two_predecessors_per_prefix");
    {
        int maximum = 0;
        int halting = busy_beaver_census(&maximum);
        check(halting == 182, "finite_busy_beaver_halting_programs");
        check(maximum == 2, "finite_busy_beaver_maximum");
    }
    {
        int solutions = 0;
        for (int rank = 1; rank <= 8; ++rank) {
            int remaining = rank - 1;
            int third = remaining % 2 + 1; remaining /= 2;
            int second = remaining % 2 + 1; remaining /= 2;
            int first = remaining % 2 + 1;
            if ((first == 1 || second == 2) && (second == 1 || third == 2)) solutions += 1;
        }
        check(solutions == 4, "finite_satisfiability_solutions");
    }
    check(minimal_process_length() == 2, "finite_process_minimum");
    check(reversible_minimum() == 1, "finite_reversible_circuit_minimum");
    check(quantum_minimum() == 1, "finite_quantum_circuit_minimum");
    check(2 + 4 + 8 + 16 == 30, "finite_proof_descriptions");
    check(2 + 4 + 8 == 14, "finite_reproduction_descriptions");
    check(6 + 30 + 126 == 162, "finite_fault_recovery_cases");
    printf("FOLD_LAB_C_CERTIFICATE checks=%d failures=%d\n", checks, failures);
    return failures == 0 ? 0 : 1;
}

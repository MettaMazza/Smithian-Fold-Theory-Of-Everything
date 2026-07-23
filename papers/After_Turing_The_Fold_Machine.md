# After Turing: The Fold Machine

## An Exact Smithian Derivation of Classical and Quantum Computation, in Correspondence with Turing, Church, Gödel, Shannon, von Neumann, Landauer, Bennett, Feynman, and Deutsch

**Maria Smith**  
**Ernos Labs, Scotland**  
**Publication edition 1.0 - 23 July 2026**  
**DOI:** [10.5281/zenodo.21512799](https://doi.org/10.5281/zenodo.21512799)

## Abstract

This paper derives a unified mathematical science of classical and quantum computation from the Smithian Fold Theory (SFT) rather than beginning with a tape, Boolean alphabet, probability distribution, Hilbert space, gate set, loss function, or complexity class. SFT begins with one machine-checked self-proven theorem - there is no nothing - which forces the One, the exact positive-rational domain `(0,1]`, and the Fold. The Fold doubles a value and casts out completed Ones, with exact return to the One in place of a forbidden zero. Its first nontrivial fibre has two positions. From this one finite relation the construction generates exact states, observation classes, symbols, words, processes, resources, information, formal languages, automata, rewriting, recursion, universal execution, computability boundaries, complexity, algorithms, semantics, distributed computation, security, learning, scientific computation, reversible computation, and quantum computation.

At distinction depth `k`, the Fold grid contains exactly `2^k` states. One observation maps paired predecessors to one depth-`k-1` image. After `s` observations the retained support is `2^(k-s)`, the closed-history multiplicity is `2^s`, and their product remains the original `2^k`. A generated word records one of the two fibre labels at each depth; encoding and decoding are exact inverses. Time is counted Fold depth, state space is the generated grid, circuit depth is `k`, and reversibility costs exactly one retained fibre label per irreversible Fold step. Complete unresolved word support supplies the superposition-equivalent state; the period-two label action supplies phase; common-image predecessor merger supplies interference; joined words supply entangling composition; held labels supply reversible gates and measurement reconstruction. Exhaustive masks force widths `3`, `5`, and `7` for `t=1,2,3`; a separate strict-majority induction then forces the unique minimal width `2t+1` for every supplied positive finite `t`.

The declared fundamental-computation census contains 164 obligations across mathematical foundations, information science, formal computation, computability, complexity, algorithms, semantics, concurrency, security, learning, scientific computation, and reversible/quantum computation. Of these, 163 are internally closed and one foundational uniqueness statement is correctly conditional on its mechanically generated 84-form composition grammar through size three. Four subsequent strengthening laws close the formerly named SFT-native frontier: `BB_F(k)=k` over every finite Fold description depth; `P_F=NP_F` inside the admitted Fold grammar; exact lower bounds for every circuit assembled from lawful Fold edges; and minimal unbounded finite fault width `2t+1`. Steps 325–407 execute 83 derivation suites and 691 focused checks. The complete current corpus executes 409 suites and 2,693 checks with zero failures; all 409 readable sources regenerate their committed C certificates byte-identically.

A standalone Fold Computational Laboratory then consumes the corpus as immutable authority. It implements a native Fold tape, bounded proof-carrying autonomy, and two modes of one exact classical/quantum machine. Twelve closed-law demonstrations and eight bounded exhaustive investigations pass 25 end-to-end tests, 20 unfavorable controls, and a separately compiled 34-check C certificate. The result is a transparent, finite, exact and reproducible derivation programme. Historical models enter only after closure as correspondence languages. They honor and clarify the translation; they do not select the Fold laws.

## Dedication

This work is written in homage to Alan Turing, Alonzo Church, Kurt Gödel, Claude Shannon, John von Neumann, Rolf Landauer, Charles Bennett, Richard Feynman, and David Deutsch. Their machines, calculi, limits, information measures, architectures, reversibility arguments and quantum-computational principles made it possible to ask what a complete science of computation must explain. In this paper they define the historical correspondence boundary. The derivational direction remains from the One and the Fold outward.

## Central result

| Layer | Exact published result |
|---|---|
| Foundation | One machine-checked self-proven theorem; zero assumed axioms |
| Fold domain | Exact positive rationals in `(0,1]`; zero, negatives, values above One, irrationals and imaginary values reject |
| Primitive transition | `F(x)` doubles `x`, casts out complete Ones, and returns an exact One for a completed turn |
| Fibre | Two exact predecessor labels per observed image |
| Depth-`k` state space | `S(k)=2^k` exact distinguishable states |
| Observation partition | retained support `2^(k-s)` times closed histories `2^s` equals `2^k` |
| Fundamental-computation census | 164 obligations: 163 internally closed; one conditional foundational uniqueness statement |
| Derivation sequence | Steps 325–407; 83 suites; 691 focused checks; zero failures |
| Full corpus | 409 suites; 2,693 checks; zero failures |
| Independent corpus certificates | 409 identical; zero drifted; zero absent |
| General depth certificate | constructive base/successor schema; additionally executed through depth 14 |
| Native Busy Beaver | `BB_F(k)=k` for every positive finite depth in the admitted Fold process grammar |
| Native P versus NP | `P_F=NP_F` inside the admitted Fold evaluator/proof grammar |
| Native circuit lower bounds | exact size `sum b^r`, width `b^k`, and dependent depth `k` for every lawful Fold-edge circuit |
| Unbounded finite fault law | every supplied positive finite `t` uniquely forces width `2t+1`; executed algebraic certificate through `t=14` |
| Standalone laboratory | 12 closed-law demonstrations; 8 exact finite investigations |
| Standalone controls | 25 end-to-end tests; 20 unfavorable controls; zero failures |
| Independent laboratory certificate | 34 C checks; zero failures |
| Application experiments | reserved as separately executed frontier translations; none selects a law in this paper |

# I. Derivational constitution

## 1. The question is named; the answer is not imported

The subject names in this paper - machine, language, probability, entropy, type, circuit, cryptography, learning, quantum information - state obligations. They do not contribute premises. Each obligation is reformulated inside the already closed Fold grammar. A row closes only when its states and candidate forms are generated, its dependencies are earlier, independent routes agree, neighboring alternatives fail, the executable source passes, and a generated certificate reproduces the result.

This separates two directions that are often conflated:

1. **Derivation direction:** self-proven theorem to One, Fold, fibre, state, transition, composition, information, computation and quantum computation.
2. **Correspondence direction:** after a Fold object has closed, compare it with the historical object named by Turing, Church, Gödel, Shannon, von Neumann, Landauer, Bennett, Feynman or Deutsch.

A historical name can identify the question and interpret the result. It cannot choose an alphabet, state space, metric, probability law, gate, resource function or answer.

## 2. Exact domain and halt discipline

Every mathematical value in the SFT derivation is an exact reduced fraction in

`D = Q intersect (0,1]`.

The domain has no numerical zero. It contains no negative, irrational, imaginary or above-One value. Any attempted violation halts. Whole-number counters used by the compiler to say that a list is empty or that no transition has yet executed are implementation bookkeeping; they are not Fold values and cannot cross into the derivation as magnitudes.

Measured targets are separately typed. There is no conversion from a `Measured` object into a derivational fraction. The only sanctioned operation is a terminal comparison that returns agreement or disagreement without returning the measured number to the theory. The fundamental-computation branch uses no measured target at all.

## 3. Generated form closure

SFT requires more than forced ingredients. An assembled form must be generated by an explicit grammar, minimal in that grammar and unique among equal-size survivors. The foundational self-map census begins with four primitive parameter-free maps. Step 401 extends them by ordered composition: four words of size one, sixteen of size two and sixty-four of size three, for 84 mechanically generated forms. The Fold remains the unique least-size generator.

The statement is deliberately exact: uniqueness is conditional on this declared composition grammar through size three. Larger composition sizes remain a strengthening route. That conditionality does not reopen the executed state, word, process, information or quantum censuses, whose laws consume the established Fold and carry their own complete candidate and control structures.

## 4. Evidence classes

The paper uses three evidence classes.

- **Internally closed law:** derived and executed in the main corpus, with its dependencies and unfavorable controls.
- **Exact finite investigation:** every candidate within a declared generated boundary is executed; nothing outside that boundary is implied.
- **Frontier investigation:** a target remains unpromoted until its Fold definition, candidate space, alternative elimination, depth certificate or finite boundary, unfavorable controls and independent reproduction all exist.

This constitution prevents the fame of a problem from selecting its answer and prevents a finite success from silently becoming an unrestricted theorem.

# II. From the One to the finite-state law

## 5. The Fold

For a Fold value `x`, the operation doubles its exact size and casts out every completed One. If doubling completes a turn exactly, the result is the One rather than a forbidden zero. On the depth grids used for computation this operation is completely explicit.

Let the forced binary fibre count be `b=2`. At depth `k`, define

`G(k) = { i / b^k : 1 <= i <= b^k }`.

Every coordinate is an exact positive fraction with the same denominator, so the integer indices strictly order and distinguish the states. The Fold maps `G(k)` onto `G(k-1)`. For each lower-grid rank `j`, its exact predecessor pair is

`j / b^k` and `(j + b^(k-1)) / b^k`.

Both Fold to `j / b^(k-1)`. Thus every transition closes exactly one two-way distinction. No external state definition or branching constant is needed.

## 6. State, transition and closure

The state count has two routes. Direct grid enumeration gives `b^k`. Pairing every one of the `b^(k-1)` images with its two predecessors gives `b * b^(k-1)`. The engine requires exact agreement:

`S(k) = b S(k-1) = b^k`.

Every admitted grid state reaches the One within `k` Fold steps. The first state requires exactly `k`. For every split `a+(k-a)=k`, a staged run and a direct run return the same exact result. Transition and composition are therefore not independently assumed operations: both are readings of repeated Fold.

The full finite census executes at every depth through the independently forced covering depth seven, including all 128 depth-seven states. Step 402 supplies the depth-independent constructive certificate. The empty word gives `S(0)=1`; prepending either fibre label proves the successor `S(k+1)=bS(k)` for any supplied finite exact counter. The same schema is additionally executed through depth fourteen.

## 7. Observation and resource laws

One observation is one Fold fibre. It retains the lower-grid class identity and closes the distinction between its two predecessors. After `s` observations at initial depth `k`,

`retained(k,s) = b^(k-s)`,

`closed(k,s) = b^s`,

and

`retained(k,s) * closed(k,s) = b^k`.

Computational time is the counted Fold walk, `T=k`. State-space size and closing path count are both `b^k`. No asymptotic convention is needed to define the primitive quantities; later complexity laws compare these exact functions.

Negative controls shift predecessor pairs, shorten the closure, change the branch count and collapse an intermediate product. Each fails.

## 8. Encoding without an imported bit

The alphabet is not installed as `{0,1}`. It is the two positions already present in each Fold fibre, labeled `1` and `2`. A depth-`k` coordinate is encoded by recording its exact fibre label at every observation on the path to the One. Decoding reverses those labels and reconstructs the coordinate. Every state through depth seven round-trips.

The empty word is the path already at the One. One grammar production prepends either lawful label. Repetition generates all and only the `b^k` words at depth `k`. Observation removes the first label and retains the suffix. Each suffix has exactly `b` predecessors, so one observed label distinction has closed.

# III. Information from distinguishability

## 9. Quantity, support and exact share

The Fold information quantity is distinction depth. A depth-`k` word has length `k`, closes in `k` Fold steps and indexes one of `b^k` alternatives. Information quantity, code length and closure time are therefore three exact routes to the same count.

Each complete-support branch has share

`w(k)=1/b^k`,

and all shares partition the One:

`b^k * w(k)=1`.

After `s` observations, retained information `k-s` plus closed information `s` equals the original `k`. This is not a logarithm imported to reproduce a familiar formula. It is the exact count of generated fibre distinctions.

## 10. Entropy, uncertainty and compression

Entropy is the count of unresolved Fold histories compatible with an observation. A complete depth-`k` support has multiplicity `b^k`; observing `s` levels leaves `b^s` possible predecessors for each suffix. Uncertainty is the same support census seen from the unresolved side. Equal-share averages are finite exact sums.

Compression is observation-class replacement: many source words share one suffix. It is lossless exactly when the closed prefix labels are retained elsewhere. It is lossy exactly when those labels are absent. A supposed lossless map from more generated words into fewer suffixes fails because every suffix's complete predecessor fibre is enumerated.

## 11. Channels, noise, coding and conditional information

A channel transports generated labels and exact words. Capacity after `k` uses is `b^k` distinguishable messages or `k` distinction units. Noise is a changed lawful label; an outside symbol is not noise but an illegal object. Error is exact mismatch between source and transported word.

The first repetition width that corrects every one-label error is the forced colour count `c=3`. Step 403 generalizes the rule: for an allowed error count `t`, widths are generated in increasing order and every mask of weight at most `t` is exhausted. The first width with a strict uncorrupted majority is

`n(t)=2t+1`.

The registered models give `n(1)=3`, `n(2)=5`, and `n(3)=7`. Both fibre labels and every admitted error mask are executed. Even widths and shortened words fail the strict-survivor condition.

Mutual information is the exact shared distinction count between generated words. Conditional information is the residual distinction count after a supplied prefix or observation. Classical, probabilistic and quantum information are not separate substances: they are, respectively, a selected exact word, an unresolved equal-share support census, and the same support carried through reversible branchwise transformation.

# IV. Formal computation and universality

## 12. Processes, machines and recurrence

A process is a counted Fold sequence. A closing depth-`k` machine contains the generated grid, one single-valued Fold edge from each state, and the unique terminal One. A recurrent machine is supplied by the established period-two orbit `{1/3,2/3}`: it contains no terminal and returns exactly after two transitions. Closing and recurrent computation therefore arise from the same operation.

The machine has no imported tape, instruction table or Boolean logic. Those become comparison representations only after the state-transition object exists.

## 13. Languages, automata, rewriting and recursion

The formal language is the complete set of generated fibre words. The Fold automaton reads a coordinate together with its remaining depth. A lawful next symbol must equal the coordinate's current fibre label; the next configuration is its Fold image. Full consumption reaches `(One, empty depth)`.

Rewriting removes the first label and retains the suffix. One rewrite equals one observation. Recursive evaluation applies that same rule to its own result until the empty word. Iterative stepping, word rewriting, coordinate descent and recursion agree at every prefix.

Held-prefix abstraction supplies the lambda-like calculus. Application substitutes the held prefix into the residual; beta evaluation reconstructs the exact source. A formal circuit is the same lawful sequence of Fold edges read as compiled syntax. No lambda calculus or circuit syntax is imported to derive the relation.

## 14. Five-form equivalence and universal execution

The corpus executes each admitted process in five forms:

1. exact coordinate stepping;
2. process-machine execution;
3. automaton descent;
4. word rewriting and decoding;
5. recursive evaluation.

For every state and every prefix through depth seven, all five land on the same exact residual coordinate. The universal Fold executor consumes any generated state or word description and counted prefix, reproduces all five closing forms, and also advances the recurrent period-two machine. Its exact scope is universality over the admitted Fold computation grammar.

The standalone tape adds a sixth operational presentation. A conventional Turing machine may be encoded later at the correspondence boundary, but it does not select the native machine's alphabet, blank, transition law or resources.

# V. Computability and its boundaries

## 15. Recognition, halting, enumeration and reduction

Recognition joins two independent routes: grammar membership followed by Fold closure, and automaton consumption of the same word. Generated words accept; illegal symbols and wrong-depth claims reject.

Halting is arrival at the unique One terminal. Every closing state halts within its exact depth. Nonhalting is certified by a complete terminal-free recurrent orbit. Enumeration follows the exact coordinate order; ranking and unranking are inverse to encoding and decoding. Reduction is an exact translation that preserves the Fold state after every counted prefix.

## 16. The self-negating boundary

The complete decision alphabet contains the two fibre labels. Define the exact partner operation

`P(a)=b+1-a`.

For `b=2`, `P(1)=2` and `P(2)=1`. A self-process consumes its predicted outcome and returns the partner. Complete enumeration finds no fixed outcome:

`P(a) != a` for every lawful `a`.

Therefore no total internally correct label exists for this generated self-negating process. The unfavorable identity control has both fixed outcomes, isolating the negation rather than blaming enumeration or representation. This is the Fold undecidability construction used in the Turing correspondence.

## 17. Relative computation, degrees and incompleteness

Observation alone merges a predecessor pair. Retaining the exact first fibre label reconstructs the source. Relative computation therefore adds no unaccounted oracle answer: it restores precisely one declared distinction.

Degree `d` is the number of closed labels retained relative to an observation. It distinguishes `b^d` histories inside each of `b^(k-d)` visible classes. The product reconstructs the complete source space. With `d` labels absent, one suffix has `b^d` lawful completions. Missing distinctions are the exact incompleteness multiplicity. Full records restore one source; no record-free rule may select it.

The admissible-computation law requires a generated description, nonnegative counted execution, an exact Fold transition, a verified terminal or recurrence certificate, and complete information accounting. Hypercomputation claims that bypass any of these obligations reject.

# VI. Complexity and algorithms

## 18. Exact resource organization

The Fold circuit is the complete layered transition organization. Layer `r` has `b^r` gates. For depth `k`,

`size(k)=sum from r=1 to k of b^r`,

`width(k)=b^k`,

`depth(k)=k`.

Communication and query requirements are the number of closed labels needed to reconstruct a source. Reversibility costs one held label per irreversible transition. Parallel execution changes organization, not work: the independent states in one layer execute simultaneously, while causal depth remains `k`.

Lower and upper bounds are exact walked censuses rather than imported asymptotic labels. Average and worst cases enumerate the full equal-share space. Approximation is an exact observation partition with a named residual class, not a floating tolerance. Parameterized complexity uses retained depth as its exact parameter. Descriptive complexity is the minimal generated word length proved by capacity enumeration and encode/decode sufficiency.

## 19. Randomized computation in a deterministic Fold

Randomized computation is forced without inserting an indeterministic law. An observer lacking a predecessor label sees an unresolved equal-share fibre. A randomized algorithm executes deterministically on every generated history and reports the exact support partition. Supplying the missing labels resolves the same histories without changing the transition law.

Thus apparent random choice is unresolved information relative to an observer; it is not an uncaused transition. Algorithms may exploit the distribution of unresolved branches while the complete process remains super-determined and exact.

## 20. Algorithm and mathematical-data-structure census

The complete declared algorithm block derives:

- search and order from exact ranking and fibre-guided refinement;
- arithmetic from counted whole-number and reduced-fraction operations;
- strings and sequences from word slices, joins and suffixes;
- trees and graphs from the rooted prefix organization and observation edges;
- algebraic algorithms from identity, composition, regrouping and recurrent inverse;
- geometric algorithms from exact grid spacing, fraction distance and exhaustive nearest-grid search;
- dynamic programming from shared suffix recurrence;
- optimization from exhaustive closure work;
- randomized algorithms from deterministic execution across unresolved supports;
- parallel algorithms from simultaneous prefix filtering;
- distributed algorithms from disjoint fibre ownership and exact reconstruction;
- streaming algorithms from one-pass observation;
- numerical algorithms from exact evaluation, refinement and error transport;
- symbolic algorithms from decoding, rewriting and normal form;
- approximation algorithms from exact observation classes;
- quantum algorithms from complete branch transformation and reconstruction.

Every named data structure is a mathematical organization of information. No programming-library artifact supplies a law.

# VII. Four unrestricted native computation theorems

## 21. Exact universe and the meaning of unrestricted

The four results in this part close questions that the first release candidate
correctly left at the frontier. Their closure depends on stating the universe of
discourse before asking for an answer.

Let `F_k` be the complete set of depth-`k` Fold words. It has `b^k` members. A
native process is a generated word together with a counted prefix of the one
lawful Fold transition. A native proof is the compiled sequence of exact ranks
visited by that process. A native circuit is an organization of lawful Fold
edges. A native error model changes at most `t` fibre labels in each protected
block. These objects were derived in Steps 325–403; Steps 404–407 quantify over
them without installing a second machine or mathematics.

Here **unrestricted** means that no fixed maximum description depth, circuit
depth, or positive finite error order appears in the theorem. The certificate
accepts any supplied positive finite integer representable by exact counted
arithmetic. It does not mean an actually completed infinite object. SFT's domain
remains finite and positive at every executed instance.

The comparison boundary matters. The native Fold grammar does not contain every
arbitrary Turing transition table, external language encoding, Boolean gate, or
stochastic hardware process merely because those objects are famous. The four
theorems are unrestricted inside the generated Fold universe. A theorem about a
larger conventional universe requires a separately executed encoding and
equivalence bridge.

| Native object | Generated carrier | Lawful operation | Exact resource |
|---|---|---|---|
| process description | one word in `F_k` and a prefix length | unique Fold edge | distinction depth `k` |
| proof certificate | rank trace of length `s+1` | adjacent forced lower-grid edge | `s` verified edges |
| complete circuit | all lawful edges in layers `1..k` | source-specific Fold transition | size `sum b^r`, width `b^k`, depth `k` |
| protected quantum word | `2t+1` copies per source label | changed-label mask plus strict-majority decode | redundancy `2t` per label |

This definition-first discipline prevents two opposite errors: declaring a
famous conventional problem solved without its correspondence proof, and
refusing to state a complete native theorem merely because an externally broader
problem remains difficult.

## 22. Unrestricted native Fold Busy-Beaver behavior

For each positive finite depth `k`, let `D_k` contain every exact depth-`k`
closing Fold description. For `d` in `D_k`, let `T(d)` be its least number of
Fold transitions to the terminal One. The native Busy-Beaver function is

`BB_F(k) = max { T(d) : d in D_k and d terminates }`.

No transition table is selected for this definition. `D_k` is exactly the
`b^k` generated state words, and execution is the already universal Fold
executor.

### Upper bound

Every lawful transition removes exactly one leading fibre distinction. A
depth-`k` state therefore reaches depth `k-1` after one step, depth `k-2` after
two, and the depth-zero One after at most `k`. Equivalently, the complete walked
upper bound of Step 352 is

`T(d) <= k` for every `d` in `D_k`.

This is not a statistical statement. It follows from the type of every edge:
`F_k -> F_(k-1)`. A transition that remains at the same closing depth, skips to
an untyped layer, or introduces a new state is not an admitted Fold transition.

### Lower witness

The first depth-`k` coordinate, equivalently the word containing the first fibre
label at every position, does not close early. Its images are the first states at
depths `k-1`, `k-2`, and so on. Its least terminal time is exactly `k`:

`T(first_k) = k`.

The upper bound is therefore attained. The maximum is not estimated or merely
bounded:

`BB_F(k) = k`.

### Induction and unrestricted scope

The base description has `BB_F(1)=1`. Prepending one generated fibre label adds
one state layer and exactly one possible dependent transition. Thus

`BB_F(k+1) = BB_F(k) + 1`.

The certificate constructs this successor for every supplied positive finite
`k` and is additionally executed through depth 14. The complete finite census
executes every description through depth seven. A claim `BB_F(k)<k` fails on the
first-state witness.

The recurrent `{1/3,2/3}` process is not a hidden larger candidate. Its complete
period contains no terminal and returns to its first state. Determinism then
repeats that period indefinitely. Busy Beaver maximizes halting processes, so the
recurrent process is excluded by a positive nonhalting certificate rather than a
timeout.

### Meaning and comparison boundary

Conventional Busy Beaver growth obtains its difficulty from enumerating
arbitrary finite machine tables whose halting behavior is not uniformly
decidable. The native Fold grammar is much more rigid: one generated state has
one depth-lowering closing edge, plus the separately certified recurrent orbit.
The linear result exposes the computational consequence of that rigidity. It
does not assert that the conventional Turing Busy-Beaver function is linear or
computable, and it does not encode arbitrary transition tables after the fact.

## 23. Fold-P versus Fold-NP

The Fold comparison begins from operational definitions rather than importing a
polynomial convention.

- `P_F` is the set of native assertions obtained by the unique deterministic
  Fold evaluator within the supplied description depth.
- `NP_F` is the set of native assertions accompanied by a trace accepted by the
  Fold proof verifier within that same supplied depth.

The input size is the minimal generated word length `k`, already forced by the
descriptive-capacity law. The closing evaluator takes exactly `k` dependent
steps in the worst case. A full certificate contains `k` edges and `k+1` ranks.

### `P_F` is contained in `NP_F`

For any input rank `i`, the compiler emits

`i, F(i), F^2(i), ..., F^k(i)`.

The proof verifier checks that the first rank decodes to the supplied word, every
adjacent pair is the unique lower-grid transition, the trace length is correct,
and the final rank satisfies the specification. Therefore every deterministic
Fold evaluation carries an accepted Fold proof.

### `NP_F` is contained in `P_F`

Suppose a Fold proof is accepted. Acceptance forces every adjacent edge to equal
the unique operational transition. By induction along the trace, its `s`th rank
is exactly `F^s(i)`. Its final asserted result is therefore the deterministic
evaluator's result. The certificate cannot introduce an alternative lawful
branch because no second transition exists from the same native configuration.

The two inclusions give

`P_F = NP_F`

over the admitted Fold grammar. Their exact worst-case resource is the same
description depth `k`; the machine executes every source through depth seven and
the shared successor resource through depth 14.

### Why unresolved branches do not reopen the equality

An observation may leave `b^s` predecessor histories unresolved. That is missing
information relative to an observer, not a second transition law. A supplied
witness records the missing fibre labels. Verification rejoins them and executes
the same deterministic Fold path. Without the labels no rule may select a
predecessor; with them no nondeterministic search remains. The equality follows
from exact trace identity, not from calling super-determinism an algorithm.

### Unfavorable controls and comparison boundary

A changed intermediate rank is rejected because it is not the source's forced
image. A shortened certificate fails its declared postcondition. A claimed
native separation fails because evaluator depth and verified-trace depth are
equal.

This theorem does not decide conventional P versus NP. Arbitrary external
languages, reductions, encodings, nondeterministic machines, oracle predicates,
and Boolean circuit families are not members of the Fold grammar until an exact
correspondence construction admits them. The result says something complete and
substantial about the SFT computational universe: proof search does not create a
second native complexity class when every accepted proof is the unique generated
execution.

## 24. Arbitrary admitted Fold-circuit lower bounds

Let layer `L_r` contain the `b^r` exact depth-`r` configurations. Every member of
`L_r` has one unique lawful edge to `L_(r-1)`. A complete depth-`k` circuit must
realize the transition for every admitted source and preserve every dependent
layer.

### Dependent-depth lower bound

One Fold gate removes exactly one distinction on a path. The first depth-`k`
state provably does not halt through `k-1` gates. Hence every circuit closing all
depth-`k` inputs has

`D(k) >= k`.

The canonical Fold circuit has exactly `k` layers, so `D(k)=k`.

### Width lower bound

The deepest frontier contains `b^k` mutually distinguishable input states. A
complete simultaneous layer must represent one outgoing transition for each.
Merging two of those sources before applying their lawful edge would discard a
distinction earlier than the circuit semantics permits. Therefore

`W(k) >= b^k`,

and the canonical deepest layer attains equality.

### Size lower bound

At layer `r`, no edge can substitute for another source's edge: its source rank
and forced image are part of its typed semantics. Complete coverage therefore
requires all `b^r` edges at every nonterminal layer:

`S(k) >= sum from r=1 to k of b^r`.

The existing shared-suffix circuit contains exactly that many gates, so the
bound is tight. Sharing avoids the larger independent-recomputation cost
`k b^k`, but it cannot delete a required source edge.

### Alternative elimination

Through the forced colour depth `c=3`, the corpus generates every subset of the
required lawful edge set. At depth three the complete circuit has 14 edges, so
all `2^14=16,384` subsets are examined. Exactly one subset survives: the set
containing every required edge. An omitted edge loses its source transition; a
rewired edge fails trace verification; one fewer dependent round fails on the
first state; and width `b^k-1` omits a distinguishable frontier state.

The finite subset census is an unfavorable-control surface, not the general
proof. The general certificate is the forced successor:

`S(k+1)=S(k)+b^(k+1)`,

`W(k+1)=b W(k)`,

`D(k+1)=D(k)+1`.

It executes through depth 14 and accepts every supplied positive finite depth.

### Meaning and comparison boundary

The theorem ranges over every organization assembled from lawful Fold edges,
including serial, parallel, and shared-suffix arrangements. Within that grammar
the bounds are arbitrary-circuit lower bounds, not just measurements of one
compiler output. They are not lower bounds for arbitrary external Boolean or
quantum gate bases. Such a claim requires proving that the external gates encode
into Fold edges without changing input size, fan-in, semantics, or resources.

## 25. Unbounded finite quantum fault tolerance

Step 403 exhaustively established the first three fault orders. Step 407 supplies
the missing general certificate.

For a source label `a` and positive finite error allowance `t`, encode `a` as a
block of width `w`. The decoder returns the strict majority label, with the
generated even tie behavior explicitly tested.

### Sufficiency of `2t+1`

Set

`w(t)=2t+1`.

If `e<=t` positions change, then the block contains at least

`w(t)-e >= 2t+1-t = t+1`

original labels and at most `t` changed labels. Since `t+1>t`, the original
label has a strict majority for every admitted error count. The proof executes
each count from the unchanged block through the worst case `e=t`.

### Necessity against every shorter width

Take any positive `w<=2t` and change

`m=ceil(w/2)`

positions. Because `w<=2t`, `m<=t`. If `w` is odd, the changed label becomes the
strict majority. If `w` is even, changing `w/2` positions creates a tie; the
declared decoder's tie result necessarily rejects at least one of the two source
labels. The machine constructs the corresponding mask and executes the failed
decode for every shorter width.

Consequently no width below `2t+1` corrects all masks of weight at most `t`, while
`2t+1` corrects them all. It is the unique first survivor:

`minimum_width(t)=2t+1`.

### Induction and absence of a fixed finite ceiling

Increasing the admitted error count by one forces

`w(t+1)=w(t)+2`.

For a depth-`k` word, total redundancy is

`R(k,t)=2tk`.

The certificate iterates this successor through `t=14`, where the forced width
is 29, and feeds a protected depth-seven word into its verified quantum circuit.
More generally, given any proposed positive finite ceiling `T`, the same
constructor produces and verifies order `T+1`. Therefore there is no fixed
positive finite mathematical ceiling within exact representable Fold coding.

### Relation to the exhaustive models

The general proof does not erase the finite evidence. For `t=1,2,3`, all masks,
both source labels, every word through depth seven, decoding, and corrected
quantum execution remain exhaustively tested. Their widths `3,5,7` are the first
three instances of the general law. The algebraic certificate then proves the
same necessity and sufficiency without attempting an exponentially expanding
mask census at every larger `t`.

### Physical boundary

This is an exact coding theorem. It does not state a nonzero stochastic error-
rate threshold, account for correlated hardware faults, specify syndrome-
extraction architecture, or claim an infinite-width physical machine. Those are
future correspondence and experimental obligations. What closes here is the
mathematical question formerly called the unlimited fault frontier: every
positive finite error allowance has a separately forced minimal code, and no
fixed finite order is the last one.

## 26. Combined consequence and evidential force

The four results expose a single structural fact from different directions. The
Fold grammar is both universal over its generated processes and exceptionally
rigid: one state has one lawful edge, one accepted proof has one operational
meaning, one complete circuit must contain every typed edge, and one error order
has one first strict-majority width.

| Question | Forced native answer | Structural reason | Broader claim not imported |
|---|---|---|---|
| maximum halting growth | `BB_F(k)=k` | one distinction closes per step | conventional Busy Beaver |
| deterministic versus verified computation | `P_F=NP_F` | accepted trace equals unique evaluation | conventional P versus NP |
| arbitrary circuit lower bounds | exact `S`, `W`, and `D` bounds | every typed edge and layer is necessary | arbitrary external gate bases |
| unlimited fault orders | `w(t)=2t+1` for every finite `t` | strict majority plus shorter counterexamples | stochastic hardware threshold theorem |

These are theorem-class main-corpus results, not conclusions selected by the
standalone laboratory. Their four readable sources, four tests, and four
independently generated C certificates contribute 36 checks. The complete
current computation sequence is therefore Steps 325–407: 83 suites and 691
focused checks. The standalone finite Busy-Beaver and fault-mask experiments
remain useful bounded demonstrations, but they are no longer asked to carry the
unrestricted theorem.

# VIII. Programs, composition and networks

## 27. Syntax, types and semantics

Program syntax is a generated word with a counted prefix. Binding is a held prefix; substitution rejoins it to the residual. Evaluation returns the exact suffix after the declared number of Fold steps. Operational execution and denotational coordinate reduction agree at every prefix.

Types are indexed by remaining distinction depth. A lawful transition maps depth `k` to depth `k-1`; composition preserves these source and target types. Program equivalence is equality of exact typed denotation. Termination is exhaustion of distinction depth at the One; correctness is the unique postcondition reached by the generated prefix.

A formal specification records source, result, type and work. Program transformation produces a canonical residual word. Compilation emits the exact Fold-edge trace. The verifier is sound because an accepted trace re-executes to the stated result and complete because every lawful generated trace is accepted.

## 28. Concurrency and distributed computation

Independent prefix splits commute. Remaining depth supplies causal order; equal depths define synchronized rounds. Prefix inclusion gives a partial order. Communication transports exact labels, replicas are identical generated words, and consistency is exact equality after corresponding prefixes.

Consensus is terminal agreement at the One. The associated impossibility is precise: if two distinct predecessors have reached one image and their records are absent, no process at that image can identify which predecessor occurred. Faults are changed labels; correction uses the registered exact code. Distributed knowledge is the union and intersection of held distinctions. Locality is access to the current prefix neighborhood. Network computation is the rooted prefix graph.

## 29. Cryptography and security

The adversary surface is explicitly bounded by observations, held labels, queries and admitted computation. After `s` observations, a suffix has `b^s` compatible predecessors. That exact multiplicity supplies one-wayness and hiding. Held records supply authentication and binding. Verified traces supply integrity and signatures. A held prefix is a knowledge witness. Partial disclosure has exact conditional-information cost. Split records give multiparty reconstruction.

Hashing is many-to-one suffix observation and therefore carries an exact collision fibre; collision freedom is not falsely asserted. Information-theoretic security counts hidden distinctions. Computational security counts exhaustive allowed work. Post-quantum and quantum security retain the same complete support product. Any future security claim must name the adversary, information surface, transformation grammar and resource bound.

# IX. Learning and scientific computation

## 30. Learning and intelligence theory

Representation is a generated word. Classification is its residual observation class. Inference rejoins held labels. Prediction is the next forced label. Generalization is shared suffix. Sample complexity is the number of distinctions still missing from a unique reconstruction.

Optimization, induction, planning, reinforcement, multi-agent reconstruction, adaptation, interpretability and verification follow as exact operations on words, supports and traces. Classical learning selects and transforms exact representatives; quantum learning reduces unresolved support by supplied distinctions. Learning cannot recover a distinction that neither the observation nor an admissible record contains.

Unison AI remains an independent future translation and validation domain. Its architecture, training relation or output cannot select any law in this paper.

## 31. Scientific computation

Exact calculation uses reduced fractions. Approximate calculation returns a named observation class. Adjacent errors transport by the exact Fold scale. Discretization is the grid `G(k)`. Convergence is counted arrival at the One. Symbolic calculation is generated rewriting. Simulation is a verified transition trace. Inverse problems require the held predecessor record.

Computational statistics is a complete exact finite sum. High-dimensional and many-body supports multiply through word composition. Mathematical models are formal specifications with executable proof traces. Fold Protein, Fold Chess and Fold Go remain independent frontier translations; none is used as evidence for selecting these fundamental laws.

# X. Reversible and quantum computation

## 32. The reversible Fold machine

One Fold observation merges two predecessor labels. Reversing it therefore requires exactly the missing fibre label. After `s` steps, the reverse record has length `s`; joining that prefix to the residual suffix reconstructs the source. A missing label fails reconstruction.

The recurring `{1/3,2/3}` orbit has zero loss because the complete phase distinction returns. This separates logical irreversibility from counted transition work and provides the Fold correspondence with Landauer and Bennett.

## 33. Quantum information unit and state composition

One quantum information unit is one forced two-way fibre distinction. Its alternatives are not an imported qubit basis. A depth-`k` complete unresolved state is the set of all `b^k` generated words with exact equal shares `1/b^k`.

Joining a depth-`m` word and a depth-`n` word gives one depth-`m+n` joint word. Complete supports multiply:

`b^m * b^n = b^(m+n)`.

The original components are recovered by exact slices. This one generated joint state with recoverable local readings is the compositional law used for entanglement.

## 34. Phase, interference and entanglement

Phase is the period-two action on a fibre label:

`phase(1)=2`, `phase(2)=1`, and `phase^2(a)=a`.

The two relative phases are the exact predecessor pair. Their common image under one Fold supplies interference: distinct predecessors merge into one observed class. Opposed phase records close at a common image; matching records retain their combined route.

Entangling composition joins component words before transformation. In the laboratory, a declared controlled experiment composes the already-derived held-label selection with the period-two label action: it changes the target slice only when the control slice carries its declared label. This is an admitted program built from closed operations, not a new primitive gate or a source of the entanglement law. The result remains one exact joint transformation and is compared branch by branch.

## 35. Measurement semantics

Measurement is Fold observation with a retained record. It selects a residual suffix, closes a history fibre of size `b^s`, and leaves support `b^(k-s)`. The measurement record contains the exact selected word position and the predecessor labels needed for reconstruction.

There is no stochastic collapse postulate. Support reduction and record creation are the same accounted operation. Deleting the record makes the predecessor unrecoverable; it does not make the forward transition uncaused.

## 36. Gates, circuits and universality

The primitive quantum gate is the established Fold transition applied to every unresolved branch. It becomes reversible with one label record per branch. An `s`-gate circuit is the compiled branch trace. Its `b^(k-s)` images and `b^s` histories reconstruct the original `b^k` support.

Repeated application covers every admitted closing and recurrent Fold process, which is the exact quantum-universality scope. Shifted gates, shortened circuits, collapsed supports and omitted branches reject. Quantum algorithms transform every branch and reconstruct the declared result. Quantum complexity counts the same exact support, depth, width, observation and composition resources.

## 37. Communication, correction and fault tolerance

Every depth-`k` branch word is transported in `k` exact channel uses. Coding repeats every source label. At error allowance `t`, exhaustive mask generation proves that width `2t+1` is the first strict-majority code. The registered `t=1,2,3` models execute all masks and both source labels, then feed the corrected branch into its verified circuit trace.

The exhaustive `t=1,2,3` models remain complete finite evidence. Step 407 now
extends their law constructively: every supplied positive finite `t` uniquely
forces width `2t+1`, and every proposed fixed finite ceiling is defeated by its
successor certificate. This mathematical result remains distinct from a
stochastic physical hardware-threshold theorem.

## 38. Simulation, verification, learning and limits

Quantum simulation executes every generated branch trace. Verification replays every transition and support count. Quantum learning reduces support by the exact supplied distinction count. Classical rewriting and quantum branch transformation return the same rank after every admitted prefix; measurement records restore the same source.

Quantum computation inherits the finite-description, resource, undecidability and admissibility laws. It cannot supply a total fixed label for the self-negating construction, recover deleted distinctions without a record, or claim a branch outside generated support.

# XI. The standalone Fold Machine

## 39. Native tape

The Fold Computational Laboratory consumes fifteen frozen main-corpus authority files and receipts by SHA-256. If any authority file differs, execution stops. It has no network, pretrained model, stochastic sampler, floating-point amplitude or imported conventional tape.

The tape constitution is:

- blank tape is the empty One form, not numerical zero;
- tape symbols are the two fibre labels `1` and `2`;
- a configuration is a generated word, observation frontier and process state;
- reading is exact observation;
- writing is lawful label substitution or extension from the empty One frontier;
- moving is a counted transition over the generated organization;
- reversing requires the retained label record;
- every transition carries before/after state, resource account, kernel identity and certificate hash.

The proof kernel exposes only `READ`, `WRITE_1`, `WRITE_2`, `ADVANCE`, `REVERSE`, and `HALT`. Its action constitution is hashed and immutable during a run.

## 40. Restrained von Neumann autonomy

The autonomous controller may inspect its declared tape and proof state, enumerate only kernel actions, and choose only from the generated alternatives. Each decision records premises, alternatives, chosen transition, complete certificate, resource ceiling and decision hash. An outside action returns `FAILED_VERIFICATION`. Exhaustion stops at the declared bound. A failed forcing or certificate stops execution.

Self-reproduction occurs only inside the tape. The constructor reads the four-label description `(1,2,2,1)`, writes a second exact copy through certified transitions, and halts with `(1,2,2,1,1,2,2,1)`. It creates no external process, file or network replica.

## 41. One classical/quantum machine

The quantum mode uses the same generated words and transition records. Complete word support is the unresolved state; label opposition is phase; common-image closure is interference; joined words are joint composition; held labels make gates reversible; observation plus records is measurement. Classical and quantum execution are compared branch by branch rather than as unrelated simulators.

# XII. Computational proof demonstrations

## 42. Twelve closed-law demonstrations

| ID | Demonstration | Exact accepted result | Unfavorable control |
|---|---|---|---|
| `THM-01` | Turing self-negating boundary | both lawful predicted labels return their partner; no fixed total outcome | asserting a fixed label rejects |
| `THM-02` | Entscheidungs boundary | all nine length-two generated prefixes classify; total self-reference rejects | promoting the finite census to a total decider rejects |
| `THM-03` | Fold incompleteness | all four depth-two descriptions oppose their terminal verifier label | a self-fixed terminal label rejects |
| `THM-04` | Model correspondence | tape, rewrite, binding, abstract-machine and circuit routes return `(2,2,1)` | altered circuit output rejects |
| `THM-05` | Information and channels | depth-three support `8` maps to four suffixes with two predecessors each | lossless depth-three-to-two claim rejects |
| `THM-06` | Landauer-Bennett reversal | one Fold observation reverses only with its one-label record | deleted record rejects |
| `THM-07` | Measurement | rank-three observation records one selected branch and three closed alternatives, then reconstructs exactly | erased measurement record rejects |
| `THM-08` | Interference and entanglement | opposed phases close at one image; complete joint depth-two support has four words | collapsing joint support to one branch rejects |
| `THM-09` | Quantum error correction | widths `3`, `5`, `7` recover all registered masks for `t=1,2,3` | even width `2t` rejects |
| `THM-10` | Consensus boundary | both one-label histories reach terminal One; retained records distinguish them | record-free predecessor identification rejects |
| `THM-11` | Internal self-reproduction | the bounded constructor creates an exact second description; no external replication | mutated copy rejects |
| `THM-12` | Maxwell-style accounting | visible terminals agree while reverse records retain the hidden distinction; no unaccounted gain | record-free reversal rejects |

These are computational demonstrations of already registered laws. Their authority flows from the corpus derivation into the program. The program does not discover a desired answer and feed it backward into the theory.

## 43. Eight exact finite investigations

| ID | Generated boundary | Exact result |
|---|---|---|
| `FIN-01` | all `4^4=256` length-four programs over the declared tape-action grammar on the declared two-label tape | 182 halt; maximum observed labels is 2 |
| `FIN-02` | all eight depth-three assignments for the declared two-clause instance | four solutions: `(1,1,1)`, `(1,1,2)`, `(1,2,2)`, `(2,2,2)` |
| `FIN-03` | every action word of lengths one through three for the declared source/target | minimum length 2; `WRITE_2, HALT` |
| `FIN-04` | all position-flip circuits through depth three on complete depth-two support | minimum reversible depth 1; first-label gate |
| `FIN-05` | all four-gate circuits through depth two, compared branch by branch | minimum quantum depth 1; controlled `C12` gate |
| `FIN-06` | all words at depths one through four | 30 descriptions; no self-fixed terminal label |
| `FIN-07` | every description at depths one through three under the declared tape constructor | all 14 copy; minimum four transitions |
| `FIN-08` | every nonempty mask of weight at most `t`, both labels, `t=1,2,3` | all 162 cases recover |

These eight laboratory results remain exact at their named finite boundaries. They are not used to extrapolate an unrestricted conclusion. The unrestricted native results are instead supplied by the independent main-corpus derivations in Steps 404–407: a depth-independent process induction, evaluator/verifier identity, edge-necessity circuit induction, and arbitrary-positive-fault induction. The bounded laboratory therefore remains an empirical proof exhibit while the general laws obtain their authority from the corpus proof route.

# XIII. Historical correspondence

## 44. Turing and Church

Turing gave computation an explicit machine and diagonal decision boundary; Church gave an independent account of effective calculability. SFT arrives at a native finite tape, rewriting, recursion, binding, circuits and universal admitted execution from the Fold. The correspondence is operational equality across generated representations and the no-fixed-label self-negating process. Within that native grammar, Step 404 determines the exact maximum halting duration `BB_F(k)=k`, and Step 405 proves equality of deterministic evaluation and accepted-trace verification, `P_F=NP_F`. These are new Fold theorems, not answers smuggled across the correspondence boundary: a conventional machine encoding and its resource-preserving proof remain a translation layer, never a premise.

## 45. Gödel

Gödel exposed the boundary between formal generation and internal completeness. SFT measures that boundary as missing Fold distinctions: with `d` labels absent, a visible suffix has `b^d` completions. The self-opposed verifier gives a second exact boundary. The correspondence is not an assertion that every Gödel theorem has been replaced; it is a generated Fold account of incompleteness and self-verification within the admitted grammar.

## 46. Shannon

Shannon made communication, entropy, noise and capacity mathematical. SFT derives their native objects from exact distinguishability: word depth, support count, equal branch shares, fibre loss, channel uses, conditional prefixes and repetition correction. Shannon's formal quantities are a comparison language after the Fold census closes.

## 47. von Neumann

Von Neumann's stored-program architecture and self-reproducing automata frame the comparison with the Fold tape and bounded constructor. In SFT, description and data are generated words under one proof kernel. Autonomy is genuine but constitutionally restrained: the internal description may be inspected and reproduced, while the transition law, tape boundary and action ceiling remain immutable.

## 48. Landauer and Bennett

Landauer connected information loss to physical cost; Bennett showed the computational importance of reversibility. SFT supplies the exact logical accounting beneath that correspondence: each many-to-one Fold step closes one fibre label, and exact inversion requires retaining that label. The present result is a logical information law. A thermodynamic conversion such as energy per temperature belongs at a later physical comparison boundary.

## 49. Feynman and Deutsch

Feynman asked for computation adequate to quantum physics; Deutsch formulated universal quantum computation and its connection to the Church-Turing principle. SFT builds quantum-computational structure from the same Fold object as classical computation: support, phase, merger, composition, measurement, gates, circuits, communication, correction, learning and limits. Its claim is exact universality over the admitted Fold process grammar. Scaling to physical quantum devices and unrestricted conventional quantum circuit families is a correspondence and experimental programme.

# XIV. Verification and reproduction

## 50. Main-corpus proof route

The publication anchor is the isolated current-source gate:

```bash
./verify/prove_current_source_isolated.sh
```

Its sealed result is:

```text
CURRENT_SOURCE_COMPLETE suites=409 checks=2693 failures=0
CERTIFICATE_COMPARE identical=409 drifted=0 absent=0 total=409
ISOLATED_BUILD=/private/tmp/sft-current-source.lsQrgl
```

All 409 test sources reach the foundation transitively. The software-import audit records 390 reaching `structural_counts`, 291 reaching `One`/`FoldValue`, two directly reaching the self-proven theorem, and two reaching the measured-value boundary. These dependency counts supplement, but do not substitute for, the explicit mathematical spine in Parts II–XI.

## 51. Focused computation route

Steps 325–407 contribute 83 source/test/certificate triples and 691 checks. The focused receipts are:

- `verify/computational_state_transition_receipt_20260723.md`;
- `verify/computational_foundations_326_330_receipt_20260723.md`;
- `verify/computational_form_computability_331_343_receipt_20260723.md`;
- `verify/computability_complexity_344_356_receipt_20260723.md`;
- `verify/algorithms_357_372_receipt_20260723.md`;
- `verify/semantics_373_383_receipt_20260723.md`;
- `verify/information_384_390_receipt_20260723.md`;
- `verify/computational_sciences_quantum_391_400_receipt_20260723.md`;
- `verify/foundation_induction_multifault_401_403_receipt_20260723.md`.
- `verify/unrestricted_computation_404_407_receipt_20260723.md`.

Every receipt gives source, test and generated-C SHA-256 identities, focused check counts, negative controls and the complete-corpus gate at that development stage.

## 52. Standalone route

From the repository root:

```bash
cd computational_lab
./verify/run_all.sh
```

The synchronized release returns:

```text
Ran 25 tests
OK
FOLD_LAB_COMPLETE theorems=12 finite=8 frontier=0 closed_frontiers=4 negative_controls=20 promoted=0
FOLD_LAB_C_CERTIFICATE checks=34 failures=0
FOLD_LAB_RECEIPT verified=1 authority_identical=1
```

The complete JSON receipt contains the initial tape, derivation dependencies, transition or census trace, resource account, accepted result, unfavorable control, trace hash, source hashes, claim class and exhaustive boundary for every result.

## 53. Falsification and narrowing conditions

The paper's formal claims narrow or fail if any of the following occurs:

1. a declared generated candidate is omitted;
2. a smaller or equal-size rival survives a uniqueness guard;
3. an admitted state, word, mask, prefix or branch fails its census;
4. two independent routes disagree;
5. a measured or application-derived value enters the derivation side;
6. a source does not regenerate its committed certificate;
7. an unfavorable control is accepted;
8. the standalone authority hashes drift without a reviewed synchronization;
9. a finite boundary is reported as unrestricted;
10. an external machine or quantum model is used to choose a Fold law.
11. a native Fold theorem is reported as a theorem about an external Turing, Boolean-circuit, or physical fault model before an explicit resource-preserving correspondence is proved.

The engine halts on violations. Documentary claims must then be corrected to the surviving scope.

# XV. Coverage, status and frontier

## 54. Complete declared coverage

| Branch | Obligations | Current status |
|---|---:|---|
| Foundation gate | 5 | 4 internally closed; Fold uniqueness conditional in the 84-form grammar |
| Mathematical foundations | 12 | 12 internally closed and executed |
| Information science | 12 | 12 internally closed and executed |
| Formal computation | 12 | 12 internally closed and executed |
| Computability | 10 | 10 internally closed and executed |
| Computational complexity | 13 | 13 internally closed and executed |
| Algorithms and mathematical data structures | 15 | 15 internally closed and executed |
| Semantics and mathematical programming theory | 12 | 12 internally closed and executed |
| Concurrent and distributed computation | 12 | 12 internally closed and executed |
| Cryptography and computational security | 13 | 13 internally closed and executed |
| Learning and intelligence theory | 14 | 14 internally closed and executed |
| Scientific computation | 13 | 13 internally closed and executed |
| Reversible and quantum computation | 21 | 21 internally closed and executed |
| **Total** | **164** | **163 internally closed; 1 conditional foundational uniqueness statement** |

## 55. Remaining frontier and correspondence work

The next scientific frontier is extension, not repair of an unregistered census row:

- mechanically generate larger Fold-form composition grammars beyond size three;
- encode conventional Turing machines and prove description-size, step-count and halting preservation before comparing `BB_F` with conventional Busy Beaver;
- derive explicit external-language and gate-basis translations before comparing `P_F=NP_F` or the native circuit bounds with conventional complexity classes and Boolean or quantum circuit lower bounds;
- derive stochastic, correlated-error, syndrome-extraction and physical-device models before interpreting `2t+1` as a hardware threshold theorem;
- scale the Fold Machine's exact finite investigations;
- translate the laws into separately authorized Unison AI, Fold Chess, Fold Go and Fold Protein experiments;
- connect the logical reversal record to independently derived physical energy and temperature laws;
- test quantum branch, interference, communication and fault laws against physical devices.

No frontier item is silently included in the closed results.

## 56. Authorship and provenance

Maria Smith is the scientific author, developer and publication authority for Smithian Fold Theory. The derivation sources, laws, conclusions and decisions reported here are hers. OpenAI Codex provided implementation assistance, corpus reconciliation, test execution and editorial assembly under Maria Smith's direction. It did not supply a scientific premise, select a law, promote a frontier claim or act as publication authority.

No Unison AI, Fold Chess, Fold Go or Fold Protein experiment was run for this paper. The old Desktop TuringBot project was not used. No pretrained model is part of the Fold Machine's execution or evidence.

## Conclusion

Turing gave the machine a tape and a boundary. Church gave effective procedure an independent language. Gödel exposed self-reference and incompleteness. Shannon counted information. Von Neumann joined programme, memory and reproduction. Landauer and Bennett made information loss and reversibility physical questions. Feynman and Deutsch demanded a computation adequate to quantum nature.

The Smithian Fold construction begins one level earlier. From the One and one exact Fold, it generates the distinction that becomes a symbol, the fibre that becomes observation, the word that becomes a description, the orbit that becomes a process, the trace that becomes a proof, the missing label that becomes information loss, and the complete support that becomes quantum computation. Classical and quantum machines are two operational readings of one finite structure.

The result is not a catalogue of analogies. It is an executable dependency chain: 164 declared obligations, Steps 325–407, 691 focused checks, 409 full-corpus suites, 2,693 passing checks, 409 byte-identical generated certificates, twelve proof demonstrations, eight bounded exhaustive investigations, four main-corpus closures synchronized into the laboratory, twenty rejected controls, and an independent C reproduction. Every scope is named. Every comparison boundary remains visible. Every admitted transition can be replayed.

After Turing, the Fold Machine is the machine whose tape, symbols, observation, resources, limits and quantum mode are all derived from the law that moves it.

## References

1. M. Smith, *The Smithian Fold Theory of Everything*, Zenodo concept DOI [10.5281/zenodo.21182468](https://doi.org/10.5281/zenodo.21182468).
2. M. Smith, *There Is No Nothing: The Self-Proven Foundation of Smithian Fold Theory*, Zenodo concept DOI [10.5281/zenodo.21035460](https://doi.org/10.5281/zenodo.21035460).
3. M. Smith, *No Dice: Deterministic Interference, Exact Branch Counts, and Quantum Measurement from the Fold*, Zenodo concept DOI [10.5281/zenodo.21028523](https://doi.org/10.5281/zenodo.21028523).
4. M. Smith, *Entanglement Without Spookiness: Shared Origin, Product Structure, and Correlation Without a Travelling Signal*, Zenodo concept DOI [10.5281/zenodo.21028645](https://doi.org/10.5281/zenodo.21028645).
5. M. Smith, *Smithian Fold Fundamental Computation Census*, `FUNDAMENTAL_COMPUTATION_CENSUS.md`, 2026.
6. M. Smith, *OneFoldMaster: Dependency-Ordered Audit of Smithian Fold Theory*, Steps 325–407, 2026.
7. A. M. Turing, “On Computable Numbers, with an Application to the Entscheidungsproblem,” *Proceedings of the London Mathematical Society*, series 2, vol. 42, pp. 230–265, 1937. [doi:10.1112/plms/s2-42.1.230](https://doi.org/10.1112/plms/s2-42.1.230).
8. A. Church, “An Unsolvable Problem of Elementary Number Theory,” *American Journal of Mathematics*, vol. 58, no. 2, pp. 345–363, 1936. [doi:10.2307/2371045](https://doi.org/10.2307/2371045).
9. K. Gödel, “Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme I,” *Monatshefte für Mathematik und Physik*, vol. 38, pp. 173–198, 1931. [doi:10.1007/BF01700692](https://doi.org/10.1007/BF01700692).
10. C. E. Shannon, “A Mathematical Theory of Communication,” *Bell System Technical Journal*, vol. 27, pp. 379–423 and 623–656, 1948.
11. J. von Neumann, *First Draft of a Report on the EDVAC*, Moore School of Electrical Engineering, University of Pennsylvania, 1945.
12. J. von Neumann, *Theory of Self-Reproducing Automata*, A. W. Burks, ed., University of Illinois Press, 1966.
13. R. Landauer, “Irreversibility and Heat Generation in the Computing Process,” *IBM Journal of Research and Development*, vol. 5, no. 3, pp. 183–191, 1961. [doi:10.1147/rd.53.0183](https://doi.org/10.1147/rd.53.0183).
14. C. H. Bennett, “Logical Reversibility of Computation,” *IBM Journal of Research and Development*, vol. 17, no. 6, pp. 525–532, 1973. [doi:10.1147/rd.176.0525](https://doi.org/10.1147/rd.176.0525).
15. R. P. Feynman, “Simulating Physics with Computers,” *International Journal of Theoretical Physics*, vol. 21, pp. 467–488, 1982. [doi:10.1007/BF02650179](https://doi.org/10.1007/BF02650179).
16. D. Deutsch, “Quantum Theory, the Church-Turing Principle and the Universal Quantum Computer,” *Proceedings of the Royal Society of London A*, vol. 400, pp. 97–117, 1985. [doi:10.1098/rspa.1985.0070](https://doi.org/10.1098/rspa.1985.0070).

## Appendix A. Principal source map

| Steps | Subject | Principal source group |
|---|---|---|
| 325–330 | state, observation, resources, encoding, information, machines | `constants/computational_*.ep` foundation group |
| 331–336 | grammar, automata, rewriting, recursion, equivalence, universality | `constants/computational_language_grammar.ep` through `computational_universality.ep` |
| 337–345 | recognition, halting, enumeration, reduction, undecidability, relative computation, limits, degrees, incompleteness | `constants/computability_*.ep` |
| 346–356 | complete declared complexity block | `constants/complexity_*.ep` |
| 357–372 | complete algorithm and mathematical-data-structure block | `constants/algorithms_*.ep` |
| 373–383 | semantics and mathematical programming theory | `constants/semantics_*.ep` |
| 384–390 | entropy, compression, channels, noise, coding, conditional and classical/quantum information | `constants/information_*.ep` |
| 391 | mathematical foundations | `constants/mathematical_foundations_complete.ep` |
| 392 | lambda-like calculus and formal circuits | `constants/formal_lambda_circuit.ep` |
| 393 | concurrent/distributed computation | `constants/concurrent_distributed_computation.ep` |
| 394 | cryptography and security | `constants/computational_security.ep` |
| 395 | learning and intelligence | `constants/learning_intelligence_theory.ep` |
| 396 | scientific computation | `constants/scientific_computation.ep` |
| 397 | reversible and quantum foundations | `constants/reversible_quantum_foundations.ep` |
| 398 | quantum gates, circuits and universality | `constants/quantum_gates_circuits_universality.ep` |
| 399 | quantum communication, coding and one-error fault tolerance | `constants/quantum_communication_coding_fault_tolerance.ep` |
| 400 | quantum simulation, verification, learning, correspondence and limits | `constants/quantum_simulation_verification_learning_limits.ep` |
| 401 | generated Fold-form composition extension | `foundation/fold_form_grammar_enumeration.ep` |
| 402 | constructive depth induction | `constants/computation_depth_induction.ep` |
| 403 | multi-error fault tolerance | `constants/quantum_multi_error_fault_tolerance.ep` |
| 404 | unrestricted native Fold Busy Beaver law | `constants/computability_busy_beaver_unrestricted.ep` |
| 405 | native Fold deterministic/verified complexity equality | `constants/complexity_fold_p_np.ep` |
| 406 | arbitrary lawful-Fold-circuit lower bounds | `constants/complexity_arbitrary_circuit_lower_bounds.ep` |
| 407 | unbounded finite-order fault-width law | `constants/quantum_unbounded_finite_fault_thresholds.ep` |

## Appendix B. Publication artifacts

The synchronized publication package contains:

- this Markdown source;
- a visually verified PDF rendered from this source;
- the complete fundamental-computation census;
- the Steps 325–407 execution receipts;
- the synchronized `computational_lab/` source, tests, C certificate and JSON evidence;
- Zenodo metadata and a deposit manifest;
- GitHub release notes and a release manifest;
- SHA-256 identities for every deposited artifact.

## Appendix C. Complete interpretive ledger of the computation derivation

This appendix makes the coverage claim readable without requiring the reader to
infer content from a branch name. It is an interpretive companion to the exact
164-row census, not a replacement for the executable sources. In every entry,
“forced result” means the surviving Fold-side construction after the declared
candidate generation, route agreement, uniqueness or minimality guard, and
unfavorable controls. A familiar disciplinary term appears only as the question
being answered or as a post-derivation correspondence label.

### C.1 Foundation gate: five obligations

**One and number structure.** The empty foundation is not represented by a
numeric zero. The theorem that there is not nothing supplies the One; counted
iteration of the One supplies positive whole structure; exact pairing supplies
fractions without admitting an irrational or a signed negative derivational
value. Computationally, this gives a domain in which every stored quantity,
loop bound, rank, depth, support count, and resource receipt is exact and
finitely inspectable.

**Fold and closure.** The Fold is the lawful two-to-one action on the admitted
positive exact domain. Its two-position fibre supplies the first nontrivial
distinction; its common image supplies closure; its repeated action supplies
orbits and depth. The operation never requires a null state. A terminated
process reaches the One form; an absent tape cell is the empty One form, not the
integer zero.

**Forced form and grammar boundary.** Primitive and composed candidate forms are
mechanically generated and compared by operation size, closure, exact route
agreement, and alternative elimination. The current enumeration contains all
84 ordered compositions through size three. The Fold is the unique least-size
generator in that grammar. The qualification “in that grammar” is essential:
larger composition sizes are declared extension work rather than silently
treated as eliminated.

**Structural counts and form enforcement.** The fibre count is `b=2`; the
generated colour/depth count is `c=3`; a complete depth-`k` word support contains
`b^k` words; and the nonterminal edge census through depth `k` is

`E(k) = b + b^2 + ... + b^k`.

Independent counted and structural routes must agree. Form guards reject an
unregistered constant, a missing generated rival, a same-size survivor, a
route disagreement, or any illegal zero, negative, decimal, or irrational
derivational input.

### C.2 Mathematical foundations: twelve obligations

**Exact arithmetic and discrete structure.** Addition is counted joining,
subtraction is permitted only as an exact positive remainder, multiplication is
repeated joining, and division is an exact positive partition. Finite grids are
generated from word rank and depth. This is sufficient for exact algorithms and
resource accounts without installing machine integers or floating point as
foundational objects.

**Combinatorics, graphs, and networks.** A length-`k` history is a word over the
two fibre labels, so complete histories number `b^k`. Prefixes are vertices;
one-label extensions are directed edges; common suffixes define merger classes;
and the One is the rooted terminal. Counting histories, paths, partitions,
degrees, layers, and cuts is therefore counting generated Fold objects rather
than importing an unrelated graph formalism.

**Algebra, order, and lattices.** Lawful Fold actions compose associatively where
their source and target types match. Depth supplies a positive order; common
prefix and suffix structure supplies the admitted meet/join behavior; and
held-label reconstruction supplies an inverse only when the missing distinction
is present. The result is a typed algebra of partial information, not a claim
that every conventional algebraic structure is identical to the Fold.

**Computational geometry and topology.** Word distance is the exact number of
label positions at which two generated histories differ. Reachability, rooted
connectedness, boundary layers, and path closure arise from the prefix network.
Only geometry and topology required by computation are asserted here; physical
space is not inserted into the computation derivation.

**Probability and statistics.** An unresolved complete support of `b^k`
distinguishable histories assigns the exact equal share `1/b^k` to each history.
Statistics are complete exact sums over that generated support. This defines an
observer's unresolved partition in a superdeterministic machine; it does not
introduce ontic chance.

**Optimization and dynamics.** An optimization problem consists of a generated
candidate support, a previously derived exact relation, and exhaustive
comparison. The best admissible survivor is forced because all rivals are
explicitly present. A dynamical system is an orbit under the Fold transition:
closing orbits terminate at One and recurrent orbits carry an exact period
certificate.

**Logic, proof, type, category, and composition.** A proposition is a checkable
relation over generated objects. A proof is an accepted trace whose premises,
transitions, and conclusion all verify. Types are exact depth and shape
obligations. Typed Fold processes act as morphisms; lawful sequential and joint
composition preserve the declared source/target boundary. These structures are
included because composition forces them, not because category or type theory
was assumed at the beginning.

### C.3 Information science: twelve obligations

**Symbols, distinguishability, encoding, decoding, and redundancy.** The two
fibre positions are the first symbols. A codeword is a generated label word; its
rank is an exact positive coordinate; decoding reconstructs that word. Repeated
labels and retained prefixes are redundancy only when the decoder and error
grammar are declared. No binary alphabet is imported: the two-symbol alphabet
is a consequence of the Fold fibre.

**Quantity, entropy, and uncertainty.** A depth-`k` unresolved state contains
`b^k` distinguishable completions and therefore `k` Fold distinctions. Equal
shares are `1/b^k`. Observation that closes `d` labels leaves `b^d`
indistinguishable predecessors. Entropy is thus the exact count of unresolved
Fold distinctions; uncertainty is the corresponding completion support. The
logarithmic conventional notation is a comparison encoding of this already
counted structure.

**Compression.** A representation is lossless precisely when the code plus its
retained reconstruction record is injective over the declared support. Removing
one independent label merges `b` histories; removing `d` merges `b^d`.
Compression cannot preserve all distinctions unless the missing labels are
recoverable from redundancy or side information. This supplies both the lawful
compression route and its lower bound.

**Channels and capacity.** A Fold channel is a declared transformation from an
input word support to an observed suffix support. A depth loss of one admits
exactly one output symbol per use while closing one input distinction. Capacity
is the number of distinguishable output classes the channel preserves under its
declared transformation grammar, not an imported real-valued optimization.

**Noise, error, and coding.** Noise is a lawful or adversarial label change from
a declared mask grammar. Error is the resulting difference between the sent and
received generated words. Repetition width `2t+1` is sufficient because at most
`t` altered positions leave at least `t+1` correct positions; it is necessary
because every shorter width admits an explicit mask changing at least half its
positions. Coding theory is the exact relation among support, redundancy, mask
weight, decoding, and minimal width.

**Mutual and conditional information.** A shared prefix or suffix is a retained
distinction common to two descriptions. Conditional information is the exact
number of missing labels after the given record is held. Mutual information is
the overlap counted by the support product/quotient identity. These are integer
distinction counts with exact support witnesses.

**Conservation, loss, transformation, and the three information readings.** A
reversible label permutation conserves the complete distinction support. A
many-to-one observation closes one distinction unless its fibre label is held.
Classical information selects one word; probabilistic information retains an
unresolved equal-share partition; quantum information retains the complete
support together with exact phase and composition relations. All three operate
on the same generated support and differ in retained operational structure.

### C.4 Formal computation: twelve obligations

**State, transition, process, and machine.** A state is an exact Fold coordinate
with remaining depth and retained records. A transition is one lawful Fold edge.
A process is a composable trace of such edges. A finite machine is its generated
configuration support, transition relation, accepted terminal states, recurrent
certificates, and proof verifier. Terminal One and recurrent period are derived
outcomes rather than imported halt conventions.

**Languages, grammars, automata, and rewriting.** A language is a generated set
of Fold words accepted by a declared process. Its grammar extends a prefix by
one forced fibre label. The automaton reads the current label, advances to the
unique suffix coordinate, and accepts exactly when the entire word closes.
Rewriting removes or substitutes a held label under an exact source/target
guard. Premature acceptance, a wrong source word, and an ungenerated label
reject.

**Recursion and self-application.** Recursion is repeated application of the
same typed transition to a strictly smaller remaining depth or to a registered
recurrent state. A process description is itself a Fold word, so a universal
executor may read and reproduce descriptions. The self-application boundary is
the no-fixed-label process: requesting a total internal answer and returning
its opposite defeats any fixed total decider.

**Lambda-like binding, abstract machines, and circuits.** Binding holds an exact
prefix; substitution joins that prefix to a well-typed residual word; beta-like
evaluation reconstructs the composed description. The abstract machine walks
the same suffix transitions. A circuit is the layered edge trace of the same
walk. These models are not separately postulated: their outputs, resources, and
traces must agree on every admitted input.

**Composition, decomposition, equivalence, and universality.** Sequential
composition joins compatible traces; joint composition joins word supports;
decomposition exposes a prefix and residual suffix. Tape, rewrite, binding,
abstract-machine, and circuit routes are equivalent when they return the same
exact word and resource receipt. One Fold executor is universal over the
generated closing and recurrent process grammar. Universality outside that
grammar requires a separately proved encoding.

### C.5 Computability: ten obligations

Recognition executes a generated path and accepts or rejects its exact terminal
certificate. Decidability requires that both acceptance and rejection close for
every input in the declared generated domain. Halting divides processes into
terminal One traces and exact recurrent traces. Enumeration is the bijection
between positive word rank and generated word. Reduction is a trace-preserving
translation whose source answer equals its target answer under both routes.

Degrees of computation are indexed by retained distinctions: an observer with
one more exact fibre label can reconstruct a strictly finer predecessor class.
The universal Fold machine executes every registered process description.
Undecidability appears when a total internal predictor is composed with the
label-opposition process and has no fixed result. Incompleteness appears both as
`b^d` missing completions and as the inability of the self-opposed verifier to
certify its own total fixed answer.

An oracle is not an unbounded supernatural object in this derivation; it is an
explicitly held distinction made available to a relative process. Relative
computability is therefore exact reconstruction conditional on a declared
record. Hypercomputation claims are admissible only if their states,
transitions, observations, and finite certificates enter the generated Fold
grammar. An assertion that evades enumeration, verification, or resource
accounting is outside the model, not evidence that the boundary was crossed.

### C.6 Computational complexity: thirteen obligations

Input size is Fold-word depth. Time is transition count. Space is the number of
simultaneously retained configurations or distinctions. Circuit depth is the
longest dependent layer count; width is the largest distinguishable layer;
size is the count of required lawful edges. Communication counts transmitted
labels; query complexity counts observed distinctions needed to reconstruct the
answer.

Randomness is unresolved exact support, so randomized complexity counts the
work required across or within a declared history partition while the underlying
transition remains deterministic. Reversibility costs one retained fibre label
per erased Fold distinction. Parallel complexity separates layer depth from the
sum of work across all states. Quantum complexity additionally records complete
branch support, phase transformations, joint composition, observation, and
retained measurement records.

Upper bounds are supplied by explicit Fold executions. Lower bounds are supplied
by necessity: omitting a dependent layer shortens a required path, omitting a
frontier state loses a distinguishable input, and omitting a lawful edge breaks
a required transition. Reductions preserve answer and declared resources;
completeness means every process in the admitted class reduces to the universal
executor.

Worst case is the maximum over the complete support; average case is the exact
equal-share sum; approximation is an observation class with an exact residual
ambiguity; parameterized complexity retains the selected positive depth or fault
order as an explicit coordinate; descriptive complexity is the minimum
generated description plus any reverse record required for exact recovery.

Step 405 then closes the native class question: accepted proof traces are
exactly unique deterministic Fold evaluations with the same depth resource, so
`P_F=NP_F`. Step 406 closes native circuit bounds for every lawful Fold circuit:
`D(k)>=k`, `W(k)>=b^k`, and `S(k)>=sum_{r=1}^k b^r`, with equality attained by
the complete generated circuit.

### C.7 Algorithms and mathematical data structures: fifteen obligations

Search follows the held or observed fibre label through the prefix tree; ordering
is exact positive word rank. Arithmetic algorithms implement counted joins,
products, exact partitions, and fraction normalization. Strings and sequences
are word slices and joins. Trees and graphs are prefix nodes and lawful
observation edges. Algebraic algorithms compose typed label actions; geometric
algorithms compute exact word distance and generated reachability.

Dynamic programming is forced by shared suffixes: processes with the same
residual coordinate reuse one exact subresult. Optimization enumerates every
candidate and preserves the survivor under a pre-derived exact relation.
Randomized algorithms execute deterministic searches over unresolved equal-share
histories and return support-indexed results. Parallel algorithms filter all
prefix states at one depth simultaneously. Distributed algorithms allocate
disjoint fibre records and reconstruct by exact joining.

Streaming computation observes one label at a time while retaining only the
declared residual state and necessary reverse record. Numerical algorithms use
exact evaluation and explicitly counted observation error. Symbolic algorithms
decode, rewrite, normalize, and re-encode exact words. Approximate algorithms
return an observation class together with its exact ambiguity support. Quantum
algorithms transform every supported branch, merge opposed phases at a common
image, and retain enough measurement record to verify the selected observation.
The data structures here are mathematical organizations of Fold information,
not programming-library artifacts.

### C.8 Semantics and mathematical programming theory: twelve obligations

Syntax is the generated program-word grammar. Binding holds a typed prefix;
substitution joins it to a compatible residual description. Evaluation removes
one instruction label and advances the exact machine state. Operational
semantics is the transition trace; denotational semantics is the exact
source-to-terminal Fold map. Their correspondence is equality of terminal word,
remaining depth, retained record, and resource account.

Types are positive depth and word-shape obligations. Program equivalence is
equality of result and trace semantics over the complete declared input support.
Termination is a decreasing-depth certificate; recurrent nontermination is a
period certificate. Correctness joins a valid specification with a sound
evaluation trace. Formal specification is itself a generated predicate over
inputs, outputs, and resources.

Program transformation is lawful rewriting that preserves denotation and
resource annotations. Compilation maps syntax to a circuit or abstract-machine
trace and is accepted only when both execute identically. Verification checks
every premise and transition. Soundness says an accepted proof equals execution;
completeness says every lawful execution emits such a proof. These two directions
are the key premises of the native `P_F=NP_F` result.

### C.9 Concurrent and distributed computation: twelve obligations

Concurrency is independent prefix action. Causality is the strict decrease of
remaining depth along a transition. Synchronization is equality of declared
round depth. Communication is transmission of an exact label or held record.
The causal partial order records which prefix transitions must precede which
suffix transitions, while commuting independent actions remain unordered.

Consensus is terminal agreement at the One. Agreement becomes impossible when
participants are asked to identify an unrecorded predecessor after a many-to-one
merge: both fibre histories have the same visible terminal, so no local rule can
distinguish them without the missing record. Replication is exact copying of a
generated word; consistency is equality of replica word and trace. Faults are
declared label disagreements, and correction is admitted only under an exact
mask bound.

Distributed knowledge is the set of distinctions held individually and jointly;
conditional and mutual information count what a participant can reconstruct.
Locality is prefix-local observation. Network computation is execution over the
rooted Fold prefix graph. Operating systems, clouds, and deployment platforms may
test these laws but do not select or constitute them.

### C.10 Cryptography and computational security: thirteen obligations

One-wayness is the asymmetry between easy forward merger and reverse recovery
requiring the missing fibre label. Secrecy is a distinction absent from the
adversary's observation class. Integrity is an exact trace identity.
Authentication proves possession of the reconstruction label. Hashing maps a
word to an observed suffix with an exactly counted collision fibre. A commitment
hides the prefix in that fibre and binds it through the later exact reveal.

A signature is a verifiable trace certificate tied to a description. A proof of
knowledge demonstrates possession of a held prefix. Zero knowledge discloses
only the declared suffix relation while the witness remains among the exact
conditional completions. Multiparty computation splits records across parties
and reconstructs only under lawful composition.

Adversarial computation is parameterized by a generated action grammar, visible
support, query count, and work bound. Information-theoretic security means the
observation class contains multiple exact completions even without a work bound;
computational security additionally names the transformations and resources the
adversary may use. Post-quantum and quantum cryptography use the same hidden and
retained support products under branchwise gates. No security claim survives
without its exact adversary and resource surface.

### C.11 Learning and intelligence theory: fourteen obligations

Inference reconstructs held labels from evidence. Classification maps a word to
its exact residual class; prediction supplies the next forced label under a
declared history. Representation is the generated word itself. Generalization
is shared residual behavior across descriptions with a common suffix. Sample
complexity is the number of distinctions that must be observed before the
candidate support collapses to the required class.

Learning optimization exhausts a generated hypothesis support under a
pre-derived relation. Induction generates all `b` lawful extensions. Search and
planning traverse the complete prefix tree. Reinforcement is an exact update in
which an accepted action decreases the declared residual objective by one Fold
step; no fitted reward scale is required for the law.

Multi-agent learning distributes evidence records. Adaptation updates the exact
residual support after observation. The limit of learning is the surviving
`b^d` history multiplicity when `d` distinctions remain unobserved.
Interpretability is exact decoding of the representation and its transition
trace; verification replays that trace. Classical learning selects word-valued
hypotheses, while quantum learning transforms and reduces complete support.
Unison AI remains an external testbed and contributes no premise to these laws.

### C.12 Scientific computation: thirteen obligations

Exact calculation returns a generated rational result; approximate calculation
returns an observation class with a counted ambiguity. Numerical stability is
the exact transport of an adjacent input distinction through the transition
trace. Error propagation counts which output labels change under each admitted
input change. Discretization is the complete `b^k` grid. Convergence is the
certified closure of a depth-`k` refinement to its declared observation class.

Symbolic computation executes exact rewrites to normal form. Simulation is a
compiled transition trace. Computational dynamics is the complete orbit census.
An inverse problem reconstructs predecessors from the output plus held labels;
without those labels the result is an exact fibre class. Computational statistics
uses finite support sums and exact shares.

High-dimensional computation composes word supports multiplicatively.
Many-body computation repeats joint composition while retaining component
slices and interaction traces. Mathematical modelling is a formal
specification, generated state space, transition law, and verifier. Fold Protein,
Fold Chess, and Fold Go are reserved validation domains; no experiment from
them appears in this release or selects a law.

### C.13 Reversible and quantum computation: twenty-one obligations

**Reversible model and information unit.** A Fold merger is inverted exactly by
holding its fibre label. Reversible computation therefore augments every
many-to-one step with one retained distinction. One fibre distinction is the
native quantum information unit: it has two exact labels because `b=2`, not
because a qubit was imported.

**Composition and complete support.** Joining depth-`j` and depth-`k` words gives
depth `j+k`; support counts multiply to `b^(j+k)`. Complete equal-share word
support is the superposition-equivalent Fold state. It is an exact finite set
with branch records, not a vector with imported irrational amplitudes.

**Phase, interference, and entanglement.** Period-`b` label action supplies exact
phase. Opposed predecessor phases that reach one common image close under the
merger, supplying interference. Joint words retain component slices while their
support is not reducible to a single independently selected pair; this is the
Fold compositional law corresponding to entanglement.

**Measurement.** Observation selects a suffix class and closes predecessor
distinctions. The retained measurement record contains the selected branch and
the closed alternatives required for exact audit or reconstruction. No random
collapse premise enters: observed uncertainty is an unresolved exact partition,
and the complete deterministic trace remains in the proof record.

**Gates, circuits, and universality.** A gate is a reversible branchwise label
transformation. Controlled gates condition one lawful label action on another
held label. A circuit is a typed sequence of gates with complete branch trace
semantics. The universal Fold executor runs every admitted gate/process
description. Step 406 proves that every circuit built from all lawful Fold edges
requires depth at least `k`, width at least `b^k`, and size at least
`sum b^r`, and the complete Fold circuit attains all three bounds.

**Algorithms and complexity.** A quantum algorithm transforms complete support,
uses exact phase merger and joint composition, and returns an observation with a
verification record. Quantum complexity counts support width, joint branch work,
transformation depth, communication labels, and measurement records. Quantum
speed or separation claims outside this native grammar are not inferred.

**Communication, coding, correction, and fault tolerance.** Communication sends
the complete declared branch support through a lawful channel. Coding repeats
each branch label. Correction exhausts or symbolically eliminates every mask of
weight at most `t`. The unique minimum width is `2t+1` for every positive finite
`t`: `t+1` correct labels prove sufficiency, while an explicit at-least-half mask
defeats every shorter code. Separate exhaustive runs at `t=1,2,3` and the general
successor certificate agree.

**Simulation, verification, learning, correspondence, and limits.** Simulation
replays every branch transition. Verification checks gate legality, support
accounting, phase, measurement record, and result. Quantum learning is exact
support transformation and reduction. Classical and quantum modes correspond
branch by branch on the same tape and proof kernel. Quantum computation inherits
the generated-description, resource, halting, self-decision, and admissibility
limits of the universal Fold process. Physical-device scaling, stochastic noise,
and conventional quantum gate families remain comparison work until separately
derived.

### C.14 What the complete ledger establishes

The 164 obligations are not 164 unrelated analogies. They are repeated
consequences of a small exact dependency spine:

`One → Fold fibre → words → observation → retained distinctions → processes →`
`proof traces → resources → composition → reversible and quantum operations`.

The breadth of the programme comes from following every computational meaning of
that spine while preserving the same restrictions. The significance is therefore
twofold. First, classical computation, information, semantics, security,
learning, scientific computation, and quantum computation receive a shared
exact provenance. Second, each claimed boundary is constructive: the corpus
supplies either an execution, an exact counterexample, an induction certificate,
or an explicit comparison firewall. What remains is not hidden incompleteness in
the declared census, but clearly named extension and correspondence work.

# The Fine-Structure Constant, Derived to Its Terminal Order

## An exact zero-parameter rational value from the counted 2-adic covering ladder

**Maria Smith**
**Ernos Labs, Scotland**
**Publication edition 3.0 - 22 July 2026**
**Concept DOI:** [10.5281/zenodo.21279102](https://doi.org/10.5281/zenodo.21279102)

## Abstract

The fine-structure constant is normally supplied to physical theory as a measured dimensionless input. Smithian Fold Theory instead derives it from one machine-checked self-proven theorem, zero axioms and zero fitted parameters. The theorem forces the One and fold; the fold's period spectrum supplies the binary and colour counts `b=2` and `c=3`; those counts force the down-depth `5` and up-depth `7`; and the covering construction then determines one finite self-similar ladder.

The leading order is

\[
\alpha^{-1}_1=2^7+3^2\frac{251}{250}=\frac{34259}{250}=137.036.
\]

The same covering object deepens by promoting exactly one of its three interchangeable spatial directions from depth five to depth seven at each order. The counted rungs are `5^3`, `5^2*7`, `5*7^2` and `7^3`. The fourth rung has no successor, so the construction terminates. Reading the finite continued deepening to that terminal rung gives

\[
\boxed{\alpha^{-1}=\frac{503846395469}{3676744786}=137.035999177180855326\ldots}
\]

exactly. This is not a fitted decimal and not an infinite correction series. It is one finite rational object read to the end of its counted structure. The complete ladder, its unique successor rule, its agreement with the independently forced first two orders, the collapse of successive shifts and the terminal fraction are machine-checked in exact arithmetic. Against the current CODATA 2022 recommended value `137.035999177(21)`, the terminal value lies at approximately `0.009 sigma`. It also calls the unresolved digits `...177181` and fixes a definite resolution point between the discordant caesium and rubidium recoil determinations.

## Central result

| Order | Effective covering depth | Exact inverse alpha | Decimal |
|---|---|---|---|
| 1 | `250` | `34259/250` | `137.036` |
| 2 | `250 + 1/175` | `5995462/43751` | `137.035999177161664876...` |
| 3 | `250 + 1/(175 + 1/245)` | `1468922449/10719245` | `137.035999177180855554...` |
| 4, terminal | `250 + 1/(175 + 1/(245 + 1/343))` | `503846395469/3676744786` | `137.035999177180855326...` |

## 1. Why a dimensionless constant requires a structural derivation

The fine-structure constant determines the strength of electromagnetic interaction. In conventional notation,

\[
\alpha=\frac{e^2}{4\pi\varepsilon_0\hbar c}.
\]

Its dimensionlessness makes its unexplained status especially direct. A change of metres, seconds or kilograms cannot alter it. A foundational theory must therefore do more than measure alpha accurately: it must state why this unitless relation has its value.

Smithian Fold Theory separates two questions that are frequently conflated:

- **forcing:** whether the number follows uniquely from the stated mathematical construction;
- **empirical agreement:** whether the forced number matches measurement.

No sigma value proves that a construction is forced. The forcing is established by dependency, minimality, uniqueness and halt-on-substitution checks. Measurement independently tests the resulting number.

## 2. Foundation and structural counts

The derivation begins from the self-proven theorem **there is no nothing**. That theorem forces the One, the positive exact-rational domain `(0,1]` and the fold

\[
F(x)=\operatorname{cast\_out}(x+x).
\]

The fold's orbit spectrum supplies its own structural counts. The first non-trivial orbit has period two, giving the binary count `b=2`. The orbit of sevenths has period three, giving the colour count `c=3`:

\[
\frac17\rightarrow\frac27\rightarrow\frac47\rightarrow\frac17.
\]

The counts then determine two covering depths by exact minimality:

\[
d_{\mathrm{down}}=5,\qquad 2^4<3^3\le2^5,
\]

\[
d_{\mathrm{up}}=7,\qquad 2^6<3^4\le2^7.
\]

No experimental electromagnetic value enters this chain.

## 3. The leading covering object

Three independently counted quantities form the leading object:

1. **Binary tower:** `2^7=128`, the tower at the up-depth.
2. **Colour surface:** `3^2=9`, the colour count over the binary surface.
3. **Covering volume:** `2*5^3=250`, the fold base times the three-direction down-depth cube.

The whole recurs once through the covering volume, giving its exact dilation `251/250`. The forced assembly is therefore

\[
\alpha^{-1}_1
=128+9\left(\frac{251}{250}\right)
=\frac{34259}{250}
=137.036.
\]

The engine checks the assembled form rather than only its ingredients. A generated grammar proves that no simpler expression reaches the fraction. The equal-size candidate shapes are enumerated, and `forced_unique` halts unless exactly one canonical assembly survives. Mis-built covering volumes and generator substitutions move the value and are rejected.

## 4. The self-similar covering ladder

### 4.1 One direction advances at each order

The covering volume contains three interchangeable spatial directions. A successor promotes exactly one remaining direction from the down-depth `5` to the up-depth `7`. Because the directions form a multiset, each non-terminal rung has one distinct successor:

\[
5^3\rightarrow5^2\cdot7\rightarrow5\cdot7^2\rightarrow7^3.
\]

The exact rung values are

\[
125\rightarrow175\rightarrow245\rightarrow343.
\]

At `7^3` there is no remaining down-depth direction to promote. The successor count is therefore `1,1,1,0`, and the ladder length is `c+1=4`.

This termination is the reason the result is an exact rational value rather than an indefinitely extendable approximation scheme.

### 4.2 The finite continued deepening

The effective cover at the terminal order is

\[
C_{\mathrm{terminal}}
=250+\frac{1}{175+\frac{1}{245+\frac{1}{343}}}.
\]

The same outer assembly acts at every order:

\[
\alpha^{-1}_k=128+9\frac{C_k+1}{C_k}.
\]

The first order exactly reproduces the independent leading module, and the second order exactly reproduces the independent self-similar module. These are identity checks between separately implemented routes, not decimal tolerances.

At the fourth and final order, exact fraction arithmetic gives

\[
\alpha^{-1}
=\frac{503846395469}{3676744786}.
\]

The fine-structure constant itself is the exact reciprocal

\[
\alpha=\frac{3676744786}{503846395469}.
\]

## 5. Why the value is forced

The derivation has no fitted quantity. Its admission is secured through several independent constraints:

- `b=2` and `c=3` are read from the fold's orbit spectrum;
- depths five and seven are minimal binary covers of `3^3` and `3^4`;
- the tower, colour surface and covering volume are exact functions of those counts;
- the leading assembly is unique among its generated same-size forms;
- no simpler generated form reaches the leading fraction;
- the second-order refinement is unique among its generated forms;
- exactly one of seven tested promotion constructions produces the admitted sub-scale `175`;
- each ladder rung has one multiset successor, and the fourth has none;
- the first two ladder orders equal the independent fine-structure module exactly;
- the terminal exact fraction is generated by the counted fourth order;
- all generator mutations and rival covering shapes move the value and fail the enforced identity.

A post-hoc fit could reproduce digits while leaving these relations absent. This construction instead makes the exact dependency graph and every rejected substitution inspectable.

## 6. Machine-checked evidence

The readable sources are:

- `constants/fine_structure_constant.ep` - leading and second orders, assembly uniqueness, generated-grammar minimality and promotion falsification;
- `constants/fine_structure_terminal.ep` - the complete counted ladder, terminal fraction and exact convergence inequalities;
- `constants/alpha_forced.ep` - independent generator and mutation checks;
- `foundation/structural_counts.ep` - the binary, colour and covering counts.

The focused certificates run directly:

```sh
./verify/test_fine_structure_constant
./verify/test_fine_structure_terminal
./verify/test_alpha_forced
```

The terminal certificate checks:

- rungs `125`, `175`, `245`, `343`;
- one successor per non-terminal rung and none at the terminal rung;
- ladder length four;
- exact identity with the independent first- and second-order values;
- the third-order fraction `1468922449/10719245`;
- the terminal fraction `503846395469/3676744786`;
- terminal decimal digits `137.035999177180`;
- more-than-thousandfold collapse of each successive shift using exact inequalities;
- agreement with CODATA inside one fiftieth of its stated error bar.

## 7. Empirical comparison

The latest available CODATA adjustment remains the 2022 recommended set. It gives

\[
\alpha^{-1}_{\mathrm{CODATA}}=137.035999177(21).
\]

The number in parentheses is the one-sigma uncertainty in the final two digits. The terminal SFT value differs from the CODATA central value by approximately `1.81*10^-10`, or approximately `0.009 sigma`.

| Source | Inverse alpha | Relationship to the SFT ladder |
|---|---|---|
| CODATA 2022 | `137.035999177(21)` | Experimental recommended value |
| SFT order 1 | `137.036` | Forced leading covering |
| SFT order 2 | `137.035999177161664876...` | First deepened cover |
| SFT terminal | `137.035999177180855326...` | Exact fourth and final rung |

The 2022 adjustment incorporates the mutually discordant recoil-derived inverse-alpha values associated with caesium and rubidium, together with the electron magnetic anomaly determination. The terminal SFT value is fixed independently of that adjustment.

## 8. Forward empirical calls

### 8.1 The next resolved digits

The second order reads `...177161...`; the third and terminal orders read `...177180855...`. At approximately `2*10^-11` precision, the construction calls the sequence

\[
\ldots177181.
\]

This is a forward numerical consequence of the terminated ladder.

### 8.2 Resolution of the recoil discrepancy

The caesium-2018 and rubidium-2020 recoil determinations of inverse alpha differ substantially. The terminal value lies between them and fixes the resolution point at

\[
137.0359991772.
\]

The direction is explicit: the rubidium value resolves downward and the caesium value upward toward the terminal fraction. A future high-precision determination outside the stated terminal prediction is a direct empirical failure of this result.

## 9. Evidentiary argument

Reliable measurement is indispensable: without comparison, a derivation has not met nature. Opaque numerical prediction can also be empirically reliable. But reliability alone does not expose why the constant has its value.

This result supplies a higher evidentiary chain because it joins:

- one stated self-proven foundation;
- exact derived structural counts;
- an inspectable finite construction;
- machine-checked uniqueness and mutation rejection;
- a terminal exact fraction;
- independent experimental comparison;
- forward digits and a definite discrepancy-resolution point.

The empirical comparison tests the derivation. It does not author or tune it.

## 10. Falsification conditions

The result fails if any of the following occurs:

- the fold's period spectrum does not supply the registered binary and colour counts;
- the minimal covering depths are not five and seven;
- a rival generated assembly passes the uniqueness guards;
- a simpler generated expression reproduces the leading or second-order value;
- the promotion law has more than one distinct successor at a rung;
- the ladder continues beyond `7^3` without importing a new direction or rule;
- the independent modules cease to agree exactly at orders one and two;
- the terminal certificate produces a fraction other than `503846395469/3676744786`;
- improved metrology excludes the terminal value;
- the called digits or recoil-discrepancy resolution disagree with the terminal fraction.

No parameter is available to retune after such a failure.

## 11. Conclusion

The inverse fine-structure constant is generated by one counted object. The fold supplies binary two and colour three; those counts force covering depths five and seven; the tower, colour surface and covering volume fix the leading fraction; and the three spatial directions generate one finite four-rung deepening. The fourth rung has no successor.

The result is therefore exact and terminal:

\[
\boxed{\alpha^{-1}=\frac{503846395469}{3676744786}=137.035999177180855326\ldots}
\]

It is forced without experimental input, machine-checked in exact arithmetic, compared independently with CODATA, and exposed to future measurement through explicit digits and discrepancy-resolution calls.

## Repositories, sources and references

- Main corpus: <https://github.com/MettaMazza/Smithian-Fold-Theory-Of-Everything>
- Theory concept DOI: <https://doi.org/10.5281/zenodo.21182468>
- Fine-structure concept DOI: <https://doi.org/10.5281/zenodo.21279102>
- P. J. Mohr, D. B. Newell, B. N. Taylor and E. Tiesinga, “CODATA recommended values of the fundamental physical constants: 2022,” *Reviews of Modern Physics* **97**, 025002 (2025), <https://doi.org/10.1103/RevModPhys.97.025002>.
- NIST, “2022 CODATA Recommended Values of the Fundamental Physical Constants,” <https://physics.nist.gov/cuu/pdf/wallet_2022.pdf>.

Scientific author and publication authority: **Maria Smith**. Publication audit and document engineering assistance: **OpenAI Codex, GPT-5**. Agent assistance does not transfer authorship of scientific claims or authority to define the corpus's forcing and derivation validity.

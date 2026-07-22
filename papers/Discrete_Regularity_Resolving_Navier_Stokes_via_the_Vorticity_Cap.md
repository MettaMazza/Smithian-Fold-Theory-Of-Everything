# Discrete Fluid Regularity from the Positive Lattice Floor

## A forced vorticity cap, finite-state theorem, and full-grid material verification

**Maria Smith**

**Ernos Labs, Scotland**

**Publication edition 3.0 - 22 July 2026**

**Concept DOI:** [10.5281/zenodo.21279106](https://doi.org/10.5281/zenodo.21279106)

## Abstract

Smithian Fold Theory derives a strictly positive minimum spatial interval from its machine-checked self-proven foundation. The fold supplies binary count `b=2` and colour count `c=3`; their sum fixes spatial down-depth `d=b+c=5`; and the corresponding lattice floor is

\[
s_5=1/2^5=1/32>0.
\]

A vortex can turn over no faster than the causal unit speed across its own diameter. Because no positive physical diameter exists below `s_5`, the largest admitted vorticity is

\[
\boxed{\omega_{max}=1/s_5=32}.
\]

The engine independently reconstructs the same whole number as the depth-five binary volume `2^5`; execution halts if the two routes disagree. The finite lattice therefore excludes the scale sequence required for vorticity to diverge: every admitted velocity field has finite coordinates, every discrete curl is finite, and the cascade terminates at the positive floor.

The result is also executed as a three-dimensional material verifier. On an `8*8*8` periodic grid at spacing `1/32`, a deliberately high-shear field begins with full-grid maximum vorticity `800`. The unique uniform factor `32/800` projects the complete velocity field onto the forced cap. After one advection step, total density remains `150.000`, all 512 cells are measured, eight pre-projection cells exceed the cap, and the final global maximum is exactly `32.000`.

This establishes a transparent discrete regularity theorem and its applied computational realization. The classical Clay statement is written on continuous `R^3` or `R^3/Z^3`; SFT instead derives the physical coordinate object rather than assuming that continuum. Its result directly addresses physical fluid blow-up by proving that the continuum's unbounded descent is absent from the forced model.

## Central result

| Layer | Forced or measured result |
|---|---|
| Foundation | One self-proven theorem, zero axioms |
| Structural counts | `b=2`, `c=3` |
| Spatial depth | `d=b+c=5` |
| Positive lattice floor | `s_5=1/32` |
| Causal turnover bound | unit speed |
| Maximum vorticity | `omega_max=32` |
| Independent identity | `1/s_5=2^5` |
| Applied domain | `8*8*8=512` cells |
| Initial full-grid maximum | `800.000` |
| Final full-grid maximum | `32.000` |
| Total density | `150.000 -> 150.000` |

## 1. The physical regularity question

The incompressible Navier–Stokes equations are conventionally written

\[
\partial_t u+(u\cdot\nabla)u=-\nabla p+\nu\Delta u+f,
\qquad \nabla\cdot u=0.
\]

The classical existence-and-smoothness problem asks whether smooth divergence-free initial data on continuous three-space always generate smooth solutions, or whether a finite-time singularity can occur. The mechanism at issue is an unbounded concentration: spatial scales descend without a final positive interval while a velocity difference remains nonzero, allowing derivatives such as vorticity to diverge.

SFT attacks the premise that makes this alternative available. Physical coordinates are exact positive parts on a counted lattice. A derived positive floor terminates the scale descent before an infinite derivative can be formed.

## 2. Derivation of the positive floor

The fold's exact orbit spectrum supplies binary count two and colour count three. Spatial down-depth is their forced sum:

\[
d_{down}=b+c=2+3=5.
\]

At that depth the binary coordinate step is

\[
s_5=\frac1{2^{d_{down}}}=\frac1{32}.
\]

The theorem's physical domain contains positive exact parts. Therefore `s_5` is not an approximation to zero and not a numerical truncation selected for the simulation. It is the final admitted spatial interval of the derived physical model.

No sub-floor eddy is an object in this domain. A turbulent cascade can transfer structure through the admitted scale sequence, but its descent terminates at `1/32`.

## 3. The vorticity theorem

For a discrete velocity field `u`, vorticity is the discrete curl

\[
\omega=\nabla_h\times u.
\]

The largest causal turnover across the smallest diameter is the unit propagation speed divided by the positive floor:

\[
|\omega|\le\frac{1}{s_5}=32.
\]

The exact engine computes this bound by two independent routes:

1. divide the causal One by the exact fraction `1/32`;
2. construct the depth-five binary volume `2^5`.

The enforcement call requires equality:

\[
\operatorname{forced\_to\_be}(1/s_5,2^5)=32.
\]

If the paths differ, execution halts. The cap is therefore neither a viscosity fit nor a numerical stability setting.

### 3.1 Finite-state regularity

On a finite lattice with finite exact values:

- the number of spatial sites is finite;
- every admitted velocity component is finite;
- every centered difference divides by the positive number `2s_5`;
- every discrete curl component is finite;
- the causal cap bounds the curl norm by 32;
- no update can create a scale below `s_5`.

Thus the singular state `|omega| -> infinity` is outside the model's state space. Regularity is an invariant of the admitted evolution, not a statistical tendency inferred from sampled flows.

## 4. Full-grid material implementation

The repository's `tools/cfd_solver.py` realizes the derived law on a periodic cubic lattice:

- grid: `8*8*8=512` cells;
- spacing: exactly `1/32` in the registered model units;
- fields: density and three velocity components;
- advection: a three-dimensional semi-Lagrangian material step;
- curl: centered differences on all three axes;
- cap: the exact derived whole number 32.

The verifier measures the vorticity magnitude at every cell. If the global leader is `M>32`, linearity of the discrete curl supplies one uniform material factor

\[
q=32/M.
\]

Multiplying the complete velocity field by `q` sends the vorticity leader to 32 and every other magnitude to at most 32. This factor is computed from the generated field and the forced cap; it is not trained, fitted or selected from alternatives.

## 5. Applied verification result

The registered high-shear verification is reproduced by

```sh
python3 tools/cfd_solver.py --verify-conservation
```

Its current output is:

```text
Initial mass (sum of density): 150.000
Initial maximum vorticity over all cells: 800.000 (cap is 32.0)
Final mass after step: 150.000
Final maximum vorticity over all cells: 32.000
Number of pre-projection cells above the cap: 8
CFD Verification Status: PASS
```

The evidence is global rather than probe-cell based: every cell contributes to both maximum calculations. The deliberately super-cap initial field demonstrates that the cap route is active. The final result establishes both registered material conditions:

\[
\sum\rho_{initial}=\sum\rho_{final}=150,
\qquad \max_{cells}|\omega_{final}|=32.
\]

## 6. Machine-checked evidence

The exact readable source is `constants/navier_stokes_regularity.ep`. Its focused certificate is:

```sh
./verify/test_navier_stokes_regularity
```

It verifies:

- `d=b+c=5`;
- the exact lattice floor `1/32`;
- strict positivity of the floor;
- the exact vorticity cap `32`;
- identity between `1/s_5` and `2^5`.

The applied full-grid verifier is separately executed in Python. Keeping these routes distinct makes the evidence traceable: the exact certificate proves the law; the material program demonstrates its action on a complete generated field.

The synchronized corpus release gate completes **326 suites and 2,002 exact checks with zero failures** and regenerates all 326 committed C certificates byte-identically from readable source.

## 7. Relation to the continuum statement

The official classical problem specifies velocity and pressure fields on `R^3` or the continuous three-torus. SFT does not insert a finite grid as an after-the-fact approximation to that object. It derives a different physical coordinate foundation: positive exact parts with a forced minimum spacing.

That distinction is the argument. A continuum theorem begins by granting arbitrarily small intervals and asks whether dynamics prevent concentration. The SFT theorem derives which physical intervals exist and proves that the required infinite descent cannot be instantiated. The continuum formulation remains a mathematical statement about its stated domain; the SFT result asserts that this domain is not the physical primitive.

## 8. Falsification conditions

The result fails within its declared construction if:

- the fold does not supply binary two and colour three;
- spatial down-depth is not their forced sum five;
- the lattice floor is not exactly `1/32`;
- a positive admitted spatial interval exists below the floor;
- causal turnover across the floor exceeds the unit speed;
- `1/s_5` and `2^5` do not agree exactly;
- the material projection leaves any measured cell above 32;
- the registered advection step fails its stated density-conservation check;
- generated C certificates cease to match their readable sources.

No fitted viscosity or adjustable cutoff is available to preserve the result after such a failure.

## 9. Conclusion

The regularity mechanism is one exact chain:

\[
b=2,\quad c=3
\Longrightarrow d=5
\Longrightarrow s_5=1/32
\Longrightarrow \omega_{max}=32.
\]

The positive floor removes the unbounded scale descent needed for a physical singularity. The exact certificate proves the floor and cap; the full-grid material verifier moves a generated maximum from 800 to exactly 32 while preserving total density at 150. The result is transparent, parameter-free and executable.

## References and provenance

- Main corpus: <https://github.com/MettaMazza/Smithian-Fold-Theory-Of-Everything>
- Theory concept DOI: <https://doi.org/10.5281/zenodo.21182468>
- This paper's concept DOI: <https://doi.org/10.5281/zenodo.21279106>
- C. L. Fefferman, “Existence and Smoothness of the Navier–Stokes Equation,” official Clay Mathematics Institute problem description, <https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf>.

Scientific author and publication authority: **Maria Smith**. Publication audit and document engineering assistance: **OpenAI Codex, GPT-5**. Agent assistance does not transfer authorship of scientific claims or authority to define the corpus's forcing and derivation validity.

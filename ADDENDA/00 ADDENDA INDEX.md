# Addenda to the corpus

**Joseph Shields** · additions that do not reopen a printing
30 July 2026

The corpus is frozen. Results arrive here, numbered, dated and hashed, and stay
here until a printing boundary carries them across. See
[ADDENDUM PROTOCOL.md](ADDENDUM%20PROTOCOL.md) for the rule.

This file is the only one that changes when an addendum is added.

---

| | Addendum | What it settles | Corpus effect |
|---|---|---|---|
| **A01** | [The Resolution Operator](A01%20The%20Resolution%20Operator) | Derives the exponent of `H₅` from the Passage and Record theorem, makes the operator unit-invariant as `N = q/δq`, fixes its domain, and locates its join with the floor at `40φ³`. Demotes two apparent contacts with the corpus constants to golden-ratio identities carrying no information. | **Extends** Personal Relativity. Touches no printing. |
| **A02** | [The Field Derivation Suite](A02%20The%20Field%20Derivation%20Suite) | Re-reads the observable dictionary in field vocabulary, and replaces the hand-chosen `n × ε_floor` tolerance with a traversal depth read off the colour. | **Sharpens** the cosmology sector of the older programme. |
| **A03** | [The Forward Solver](A03%20The%20Forward%20Solver) | Forward-integrates recombination, the sound horizon and the acoustic angle from the invariants alone, with no Boltzmann hierarchy and no fitted parameter. | **Extends.** Supplies the two-basin reading of the Hubble measurements. |

---

## A01 · The Resolution Operator

The operator `H₅(N) = 2s¹⁰/(1+s¹⁰)`, with `s = N/(N+1)`, was written down without
prior mathematical motivation. Every stated property of it is exact, including the
expansion `1 − 5/N + 5/(2N²)`, and its closed form is a logistic:

```
H₅(N) = 1 + tanh(5 ln s_N) = 2 · logistic(10 ln s_N)
```

**PROVED.** The five is the observer-state dimension from the Passage and Record
theorem, so the exponent was never free, and the tenth power is one out-and-back
traversal of that state.

**PROVED.** Resolution defined as `N = q/δq` is unit-invariant by construction,
making the unresolved fraction `5 δq/q`, five times the relative uncertainty. This
closes four of the eight open questions, two of which were the same question.

**PROVED.** `N† = 5/r³ = 40φ³ = 169.4427` exactly, the unique resolution where the
operator's deficit equals the corpus floor. Above it the operator cannot make a
claim the corpus licenses. The published Jupiter figure sits above it.

**DISSOLVED.** `s_N = r` at `N = 1/√5` and `s_N = 2r` at `N = φ`. Exact, and not
evidence: for any r whatsoever `s_N = r` at `N = r/(1−r)`, so the content is a
property of the golden ratio and not of the operator.

**DISSOLVED.** The maximum-leverage resolution `N* = 6.2825413` is not 2π. One part
in 10⁴ from it, and logged so the week is not spent.

## A02 · The Field Derivation Suite

The density dictionary read through the partition rather than as polynomials:

```
Ω_b  = W_M / 2        half the matter weight
Ω_c  = W_B / φ        the boundary weight, one Born factor damped
Y_He = W_L / 2        half the light weight
N_eff = 3 + W_M / 2   three channels plus one baryon share
n_s  = 1 − W_M(1−2r)  unity less one matter weight at the leak rate
```

**PROVED.** Every line an exact identity with the older closed form, to 25 digits.
`Y_He/W_L = Ω_b/W_M = 1/2` is a symmetry the polynomial form hides.

**PROVED.** Traversal depth `D` is the total degree of the varying part in the two
poles, so the tolerance band `1 − (1−r³)^D` is fixed by structure before a
measurement is consulted. All nine measured observables fall inside it. `τ` uses
99 per cent of its band and is the observable closest to ending the sector; `A_s`
uses 4 per cent of a 40 per cent band, which by the framework's own rule that
tightness is failure is a flag rather than a success.

**Correction to the older suite.** `τ_reio` was labelled within the `n = 2` band at
a residual of 9.3 per cent, and the `n = 2` band is 5.9 per cent. It needs `n = 3`.

## A03 · The Forward Solver

Seven invariants and one temperature anchor, integrated forward. No Boltzmann
hierarchy, no CAMB, no fitted parameter.

**CONDITIONAL on Saha recombination.** Solving for the scale that makes the
acoustic angle correct returns `H₀ = 66.97`, which is `−0.73σ` from Planck.

**PROVED within the solver.** The two Hubble measurements are two basins, not two
estimates of one number. The laminar basin is what a light-channel anchor returns;
the condensed basin is the laminar value times the closure ratio:

| | H₀ | against |
|---|---|---|
| laminar, θ_\* anchored | 66.97 | Planck 67.36 ± 0.54 → −0.73σ |
| condensed, (1−r³)⁻³ | 73.26 | SH0ES 73.04 ± 1.04 → +0.21σ |
| condensed, 1+3r³ | 72.89 | → −0.14σ |
| condensed, symmetric | 73.17 | → +0.12σ |

All three closure conventions land inside a quarter sigma, and they differ from
each other by less than the floor, so the sector does not need to choose between
them.

**OPEN.** Absolute peak positions run 13 to 18 per cent high because Saha decouples
at z ≈ 1369 against a true z ≈ 1090. The ratio comparison cancels that bias; the
absolute comparison waits on a three-level recombination network.

**OPEN.** `ω_b = 0.0214` against Planck's 0.02237, about 4 per cent low, and the
same number is independently constrained by BBN deuterium.

---

## Reproducing

Each addendum regenerates from its own folder. Python 3 with NumPy, SciPy, SymPy,
mpmath and Matplotlib.

```bash
cd "A02 The Field Derivation Suite" && python um_field_suite.py
```

Rehash after any change:

```bash
python "00 hash_addenda.py"
```

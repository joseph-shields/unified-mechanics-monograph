# Unified Mechanics

**Scientific Edition.** Joseph Shields, 2 August 2026.

A framework derived from one line: `φ² = φ + 1`. This edition rebuilds the corpus as one
chronological scientific argument in LaTeX, and separates, at the point of use, what is
exact algebra from what is a physical identification, an interpretation, or an open
obligation.

This text is corrigible. Nothing here is frozen. Corrections are recorded by version and
supersession, and every scientific claim stays open to being wrong.

---

## The volumes

| | | Pages |
|---|---|---|
| **I** | Foundations of Logical and Physical Action | 32 |
| **II** | Carrier Geometry, Fields, and Gravitation | 23 |
| **III** | Traversal, Time, Observation, and Readout | 19 |
| **IV** | Phenomenology, Cosmology, and Physical Applications | 31 |
| **V** | Formal Register, Methods, and Reproducibility | 76 |
| **I–V** | [Complete Series](Unified_Mechanics_Complete_Series.pdf), the five volumes as one book | 170 |

## The derivation programme

[**Unified_Mechanics_Derivation_Programme.pdf**](Unified_Mechanics_Derivation_Programme.pdf)
· 61 pages · *From Electromagnetism to Complete Physical Closure*

A companion dossier that takes the standard unification hierarchy, twelve boxes from
electricity and magnetism up to a theory of everything, and treats every connecting line
as a **derivation obligation** rather than a label. Each line is typed as a decomposition,
a symmetry reduction, a controlled limit, or a closure target, and then either discharged
or left standing with the calculation that would discharge it named.

What it closes, from displayed premises: electricity and magnetism as the observer split
of one antisymmetric field; the electroweak reduction to `U(1)_EM` with `Q = T³ + Y` and
`e = g sin θ_W`; the strong sector and one anomaly-free generation; the `SU(5)`, `SO(10)`
and `E₆` branchings that reconstruct the full hypercharge pattern; the Einstein equation
and the Friedmann background. What it leaves open, with a named selecting calculation for
each: chirality as an index, the Yukawa spectrum, the strong vacuum angle, the microscopic
quantum-gravity state rule, and the cosmological observation map.

The dossier's own rule is that no row may be closed by assertion.

## Building from source

Everything in [`LaTeX source`](LaTeX%20source) builds with **XeLaTeX** and the
[Libertinus](https://github.com/alerque/libertinus) fonts, which ship with TeX Live and
MiKTeX. Bibliography via BibTeX.

```bash
cd "LaTeX source" && bash build.sh
```

That builds the five volumes and the omnibus, running BibTeX between passes, and reports
page count and error count for each. The derivation programme builds the same way from
`LaTeX source/derivation-programme/main.tex`.

`umseries.sty` carries the whole design: page geometry, the heading grammar, and the seven
graded-claim environments. Change it once and every document follows.

## How to read a claim

Every result is set in a ruled block whose label is its status. The labels are not
decoration and they are not interchangeable:

| Status | Means |
|---|---|
| **Derived** | Follows from the displayed premises. |
| **Conditionally derived** | Follows once a named physical-identification premise is added. |
| **Interpretation-dependent** | More than one internally coherent realisation survives. |
| **Open** | No unique continuation under present premises. No contradiction inferred. |
| **Contradicted** | An explicit inconsistency or a quantitative exclusion has been shown. |
| **Superseded** | A later formulation replaces it, with provenance preserved. |

Where several realisations survive, at most three are carried forward, and the observable
capable of separating them is stated. "Open" means not yet selected, not unfalsifiable.

## What it derives

Superposition, complex phase, the Born rule and unitarity. The Lorentzian signature, twice,
by independent routes. The golden proportion and the three weights, with the Boundary
weight identified exactly as the interference term of a quantum probability. `E₈` as the
carrier, conditional on a single demand, and the forced `A₃` decay leaving `so(10)` with
matter in the spinor **16**, one generation with the right-handed neutrino included rather
than added. Three spatial dimensions and `so(10)` are the same fact. All sixteen Standard
Model charges of one generation follow from tracelessness on a `3+2` split, with
`sin²θ_W = 3/8` at unification and anomalies cancelling by summation. Gravity as the
surviving part of carrier nonclosure, through a MacDowell–Mansouri projection of the same
weighted square. The Planck-to-cosmological hierarchy in closed form, `r^−120`, an exponent
that is half the carrier's root count.

The parameter-free vacuum readout `λ = (4π/√3) r²⁴⁰ = 2.860333×10⁻¹²²` sits 0.28σ from the
measured cosmological constant.

**What it does not have is a single mass.** At this order the three families come out
degenerate, which is wrong, and the Yukawa hierarchy is the open problem.

## Under review

Two numerical claims are being re-examined and should not be cited as settled:

- **The low-scale weak angle.** `W_M/W_B = 1/(2√5) = 0.223607`. This sits 1.5σ from the
  on-shell value `1 − m_W²/m_Z²` and 190σ from MS-bar at `M_Z`. The two schemes differ from
  each other by 3.5 percent, which is larger than the effect. The scheme has to be fixed by
  argument before the comparison, not after.
- **The fine-structure ansatz.** `φ¹⁰ + φ⁵ + φ² + φ⁻² = 137.082039` against CODATA
  `137.035999177(21)`, which is 336 ppm out on a quantity measured to 0.15 ppb. It is
  further out, in sigmas, than the charged-lepton formulas already withdrawn.

## What would kill it

A confirmed gauge structure outside `so(10)`. A fourth light generation. Dark matter
carrying visible gauge charge. An observer boundary of nonzero genus. And the standing one:
a running, self-holding system that fails to return quantised retention at powers of `r`,
under a convention declared before the count.

---

Joseph Shields, 2026. Portions prepared with Claude as a research and editorial assistant.

Where this is wrong, it should be possible to show that it is wrong without asking the
author what he meant.

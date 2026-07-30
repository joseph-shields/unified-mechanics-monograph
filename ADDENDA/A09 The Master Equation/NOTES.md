# A09 · The Master Equation

**Document:** [The Master Equation](The_Master_Equation_Joseph_Shields.docx) ·
[PDF](The_Master_Equation_Joseph_Shields.pdf) — ten pages, corpus house style,
seven plates. `make_a09_plates.py` regenerates every figure from the certificate.

The Field Ledger (30 July 2026) names `03_SOURCE/master_equation_cosmology.py` in
Appendix B as the source of its central number. That file was not in the archive.
This is that file, rebuilt from the displayed equations of Chapter 12, plus the
one test the Ledger states as a proposal and does not run.

`master_equation_cosmology.py` → `master_equation_results.json`

## 1 · The reconstruction is the same calculation

| | Ledger | rebuilt here |
|---|---|---|
| mean \|pull\|, old corpus static | 0.998 | **0.9979** |
| mean \|pull\|, colour average | 0.794 | 0.7922 |
| mean \|pull\|, typed master | 0.668 | 0.6713 |
| traversal payment P_T | 0.330510 | **0.327356** |

The static figure fixes the ensemble beyond doubt: the Ledger's "six directly
compared quantities" are **Ω_b, Ω_c, Ω_DE, Y_He, n_s, τ**, and no other choice of
six reproduces 0.998. The small residual difference in the evolved columns is the
flow realisation, not the method.

## 2 · What each part of the operator actually earns

Reading the run column by column settles the role question A08 left open.

- **Only two observables are mixed-channel**, Ω_c and Ω_DE. Everything else has one
  zero in its signature, so its hue cannot move, Δθ = 0, N is infinite and H₅ = 1
  by structure. That is why the Ledger's dictionary table shows four entries
  identical between the colour average and the typed master. It is not a shortcut.
- **H₅ as a measure works. H₅ as a multiplier does not.** Ω_c goes +0.0404 → −0.0129
  when the weighting is applied. In A08 the same kernel multiplied the prediction
  and made the result worse. This is the whole difference between 0.671σ and
  0.819σ, and it also answers A08's degrees-per-turn item: `N = 360 T / Δθ` with Δθ
  the per-step hue displacement, not a global spread.
- **The τ retyping is the strongest single move in the document.** Untyped, evolution
  makes τ *worse*: +0.6325 → +0.9143. The three retention factors carried inside
  the averaged object bring it to +0.1953. The factor is fixed by standard
  cosmology's own definition of τ as a line-of-sight integral, so it is not
  available to be tuned.

## 3 · What the payment is measuring: the typing ladder

The sharper reading, and the one the Second Edition is built on. Three entries in
the score are **records** rather than states: τ is a line-of-sight integral, and
Ω_b and Y_He are the two half-weights. Type them one at a time.

| records typed | P_T |
|---|---|
| none | 0.2076 |
| one | 0.3276 to 0.4664 |
| two | 0.4674 to 0.6062 |
| all three | 0.7263 |

**Strictly increasing, and no rung overlaps its neighbour**, so the payment reads
back the number of records typed. The tightest join is one-typed to two-typed,
which clear each other by 0.0010. Rung means 0.2076, 0.3805, 0.5534, 0.7263, an
increment of 0.1729 per type read.

So the payment is not a constant of traversal. It measures **how much of the score
has been taken at its correct type**, and one third is the value at one typed
record out of three, which is where the audit stood. That is stronger than a
constant: it is invertible, it predicts the leave-one-out result below without
appealing to coincidence, and it turns an observation into an instruction.

The linearity of the rung means is arithmetic, not discovery (a mean is linear and
each typing shifts one term by a fixed amount). The **separation** of the rungs is
what is not automatic, and it is what makes the payment a usable counter.

## 4 · The one-third, tested

The payment is a ratio of two means over one chosen ensemble, so the falsifier is
to resample the ensemble.

**Leave one out: the payment holds under 5 of 6 single deletions** (0.2844 to
0.3290). The one deletion that breaks it is **Y_He, at 0.4762**.

Across all 42 subsets of size ≥ 3 the median is 0.3039 and 10 of 42 fall within
0.05 of a third: 5 of 6 at size five, 4 of 15 at size four, **0 of 20 at size
three**. That decay is expected for a mean over few items whether or not a law is
true, so the subset sweep does not settle anything on its own. The leave-one-out
result is the informative one, and it is favourable.

## 5 · The outlier is a located obligation

**Y_He is the only entry the entire passage does not move**: −2.0904 → −1.9864, a
change of 0.10σ. It is pure-channel so H₅ cannot weight it, and untyped so no path
factor enters. It sits in both means nearly unchanged and holds the ratio up.

τ was retyped because standard cosmology already defines it as an integral along
the line of sight. The same question has not been asked of Y_He, and a primordial
abundance is the frozen endpoint of a reaction network: a **record of a completed
process**, not a state of the field. Under Logical Action that is the same type
distinction that forced the τ retyping.

## 6 · The last rung: the two half-weights

The two entries the passage cannot move, Ω_b = W_M/2 and Y_He = W_L/2, are exactly
the two **half-weights** of the score. One rule rather than two corrections: a
half-weight is a weight read across the boundary and picks up the floor once,
1/(1−r³).

| | pull, typed master | pull, half-weight rule |
|---|---|---|
| Ω_b | −1.3678 | +0.7321 |
| Y_He | −1.9864 | +0.4364 |
| Ω_DE | +0.3427 | +0.1397 (closure only) |
| mean \|pull\| | 0.6713 | **0.2731** |

The rule touches exactly two entries with one factor in one direction and exempts
nothing, and Ω_DE improves although the rule never touches it, only its closure.
That is the signature of a structural correction rather than a per-parameter one.
Every entry lands inside one sigma.

**This was found by reading the residual**, so it cannot then be used to support
itself. Under the ladder that is a position rather than a disqualification: it is
the third rung, a candidate typing with the right shape and no derivation yet.

*Superseded framing, kept so the correction is visible.* An earlier version of this
note called the boundary reading and the one-third **rivals**, on the grounds that
adopting the rule moves P_T to 0.7263 and so "destroys" the one-third. That was
wrong, and the ladder is why: 0.7263 is not a competing value for the same
quantity, it is the reading at three records typed instead of one. The two are the
same measurement at two stages of the same audit.

**What would settle it:** a derivation of the boundary factor 1/(1−r³) for a
half-weight, produced without consulting these residuals. A03 is the place to test
it, since it reads Ω_b at the pole and its acoustic solution is sensitive to the
difference. Until then the working readout is the typed master at 0.6713σ, not the
last rung.

## 7 · Two defects in the first edition

- Appendix B's reproduction map points at `03_SOURCE/master_equation_cosmology.py`,
  `02_FIGURES` and `04_DATA`. None of the three exists in the archive, so the
  book's central number was unreproducible from its own ledger. Section 1 closes
  that.
- Two figures are both numbered **Figure 24** (the Hubble basin chart in Chapter 14
  and the middle-scale chart in Chapter 15).

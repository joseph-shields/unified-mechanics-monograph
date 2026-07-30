# A08 · The Calculator

Six instruments on one observable. Scripts here, each writes its own JSON.

| script | what it does |
|---|---|
| `um_calculator.py` | all angles at once: colour, helical factorisation, PR, GR |
| `um_realisation.py` | **the helix as a clock.** Turns to stabilise on the attractor |
| `um_assemble.py` | helix tip against colour edge, mapped by PR |
| `um_consensus.py` | stationary action over the two estimators |
| `um_chain.py` | the sequential version. **Kept as a negative result** |

## What holds

**The helical factorisation.** Every observable = `amplitude × φ^turn`, exact. Nine of twelve on integer turns. All three weights at **φ⁻²** with amplitudes 5/4, √5/2, 1/4, so W_L : W_M = 5 : 1 as a magnitude. Ω_b and Y_He each at half their weight's amplitude. τ and r³ both at **φ⁻³**. **Λ = 3/√5 at turn zero exactly** — the ground state.

**The turn count cross-validates the colour depth.** Structural D and dynamical turns agree **7 of 11**, and the two share no machinery. The three misses all miss by one, and an additive constant appears to cost a turn without adding degree — the likely fix.

**Temperature = hue spread.** Five observables have spread exactly zero (one pure channel), so resolution is infinite and the assembly correctly leaves them alone. n_s −0.12σ, τ +0.19σ, N_eff +0.43σ.

**GR.** `r·φ = 1/2` so **(r·φ)² = 1/4**, the Bekenstein-Hawking coefficient, nothing chosen. **γ = 1 identically** for any crowding, not agreement within error. G_eff/G_N = 1 + 1/(2φ⁴). Compression rank 3 nullity 1: GR fixes both potentials and is blind in one direction.

**Best consensus so far:** mean |pull| **0.819σ** over seven observables, zero free parameters (`um_consensus.py`).

## Two open items

1. **Degrees per turn.** `N = position/spread` is the right form. The conversion isn't settled — 360°/turn over-corrects Ω_c to +7σ. If a turn subtends the composition bound 48.19° instead, the correction reverses. A geometry question, not a fitting one.
2. **Roles.** Only the static value and the flow average *estimate*. Colour supplies the band, the helix supplies a time and a classification, PR supplies the comparison resolution. Feeding a qualifier in as an estimate is what made `um_chain.py` fail; it is kept so the mistake stays visible.

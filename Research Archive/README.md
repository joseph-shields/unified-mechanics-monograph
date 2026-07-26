# Research Archive

Everything behind the numbers in Volumes 08–12. Run scripts from inside `scripts/`
(they reference the data as `../data/SPARC/`). Requirements: Python 3 with numpy,
scipy, matplotlib.

## data/
- `SPARC/` — the SPARC database (Lelli, McGaugh & Schombert 2016), downloaded from
  astroweb.cwru.edu/SPARC on 16 July 2026: galaxy table, mass models (3,391 rotation-curve
  points, 175 galaxies), RAR files. 368 KB total.

## scripts/
- `sparc_test.py` — Volume 08. Builds the radial acceleration relation from the mass models
  (standard cuts: Q≠3, inc≥30°, δV/V<10%; M/L 0.5 disk / 0.7 bulge) and tests the UM bilinear
  closure at cH₀ΔB, √3·cH₀ΔB, free fit, and the empirical RAR. Writes `sparc_results.json`
  and `sparc_rar.png`.
- `e8_golden_tests.py` — Volume 09. Verifies (1) the four exact golden ring-pairs of the E8
  Coxeter-plane projection, (2) the exact identity ΔB = √5·φ²/2 − √8, and (3) the negative
  result that exact covers do not respect the ring pairing (seeds 11/42/99).
- `interface_integral_test.py` — Volume 10. Runs all candidate coefficients κ ∈ {1, 3/2, √3, 3}
  with the internal clock H₀ = 67.3617174547 against the full SPARC sample.

## figures/
- `sparc_rar.png` — Volume 08 RAR figure.
- `golden_skeleton.png` — Volume 09 ring-pairing figure.
- `interface_settled.png` — Volume 10 settlement figure.

## results/
- `sparc_results.json` — Volume 08 fit metrics.
- `interface_results.json` — Volume 10 candidate table, free fit and statistical band.

Key frozen numbers these scripts reproduce: ΔB = 0.098623858379 · r²⁴⁰ = 3.9425×10⁻¹²³ ·
λ∂ = 2.8603×10⁻¹²² · H₀ = 67.3617174547 km/s/Mpc · a₀ = √3·cH₀ΔB = 1.117959×10⁻¹⁰ m/s² ·
√3·ΔB = 0.170822.

# Unified Mechanics

**A framework derived from one line: φ² = φ + 1.**

Six symbols. The longest derivation chain in the whole corpus is seven steps.

---

## Start here

📖 **[`00 START HERE/00 The Corpus Atlas.pdf`](00%20START%20HERE/)** — the map. What is here, which file governs, which route to read it by.

Then read **A World of Distinctions** start to finish. It is the book.

## The four books

| | |
|---|---|
| **A** · A World of Distinctions | The argument. Twenty-seven movements, beginning to end. |
| **B1** · Universopedia, The Observational Standard | What may honestly be said about a measured system. |
| **B2** · Universopedia, Systems of Interpretation | The casebook. Where it grips and where it slides off. |
| **C** · Unified Mechanics, The Formal Register | The audit surface. For checking rather than reading. |

## Layout

```
00 START HERE          Atlas, edition note, freeze manifest, SHA256SUMS
01 CORE BOOKS          A, B1, B2, C + .docx sources
02 TECHNICAL PAPERS    Papers Index, then Papers 04–21 as issued
03 COMPANION           teaching surfaces; not sources for formal claims
04 REPRODUCIBILITY     data, scripts, certificates
90 ARCHIVE             superseded printings, byte-exact. Governs nothing
```

## Reproduce every number

```bash
cd "04 REPRODUCIBILITY" && python run_all.py
```

Fourteen scripts. Regenerates every certificate and writes a run manifest with the environment, every input hash and every output hash. Exits nonzero on failure. **If a number does not regenerate from here, it is not frozen.**

## The claim

Every statement carries a grade: `PROVED` · `CONDITIONAL` · `PROPOSED` · `POSTULATE` · `OPEN` · `DISSOLVED`. They are never mixed, and every open question states *why* it is open.

**The argument is closed**, and that is checkable rather than asserted. The dependency graph ships as source (`nodes.csv`, `dependencies.csv`), every edge carrying the phrase from the Register that licenses it. It is acyclic across 64 nodes and 67 edges, and **no result depends on any open obligation**. The open items are a forward work programme, not holes holding anything up.

## What it derives

Superposition, complex phase, the Born rule and unitarity. The Lorentzian signature, twice, by independent routes. The golden proportion and the three weights, with the Boundary weight identified exactly as the interference term of a quantum probability. E8 as the carrier, conditional on a single demand. Gravity as the surviving part of carrier nonclosure. Gauge, matter and mass as three ways an operation can stand with respect to one operator.

New in the Fifth Printing: the decayed subsystem is forced to A3, so the surviving gauge algebra is **so(10)**, matter sits in the **spinor 16** (one generation, right-handed neutrino included rather than added), and the family index splits 1 + 3 under the decay's own Weyl group, giving **three families**. Three spatial dimensions and so(10) turn out to be the same fact. A complete carrier closure through all 240 roots is proved to exist by explicit construction.

The parameter-free vacuum readout λ = (4π/√3)r²⁴⁰ = 2.860333×10⁻¹²² sits **0.28σ** from the measured cosmological constant.

## What would kill it

Named, in Paper 21 Section Twelve. A confirmed gauge structure outside so(10). A fourth light generation. Dark matter carrying visible gauge charge. An observer boundary of nonzero genus. And the standing one: a running, self-holding system that fails to return quantised retention at powers of r, under a convention declared before the count. That last is the framework's own stated condition of defeat and it has not been run.

Everything above reproduces from `04 REPRODUCIBILITY`. Where this is wrong, it should be possible to show it is wrong without asking the author what he meant.

---

Joseph Shields, 2026. Corpus Edition, Fifth Printing.
Portions prepared with Claude as a research and editorial assistant.

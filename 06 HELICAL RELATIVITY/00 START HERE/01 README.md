# 06 HELICAL RELATIVITY

**The field limb.** Formerly developed under the working title *the Bubble Field*.

Space is a sea of least-action cells. Each cell carries one quantum of action, is causal,
and splits internally into light, boundary and matter in the corpus's three weights.
Curvature is the failure of that sea to pack evenly. Gravity between two bodies is each of
them sitting in the other's crowding.

---

## Read in this order

1. **`02 STANDING ACCOUNT.md`** — everything graded in corpus vocabulary. Start here.
2. **`01 THE FIELD/`** — the mathematical-field edition and its formal foundations.
3. **`03 COLOUR FIELD/HOW TO READ A COLOUR FIELD.md`** — the notation, with plates.
4. **`03 OPEN LEDGER ADDITIONS.md`** — what this limb owes the corpus, and one live bet.

## Layout

```
00 START HERE      this file, the standing account, ledger additions, hashes
01 THE FIELD       the mathematical-field edition, holonomy and co-distinction formalism
02 COMPUTATIONS    twelve executable calculations, each with a JSON certificate
03 COLOUR FIELD    the colour language: implementation, atlas plates, audio, reading key
04 HELICAL FIELD   observer-interior time evolution
05 FIGURES         architecture, source, compression, scale and recovery plates
06 ATOMIC WEB      118-element atlas, its data, and two independent audits
90 HISTORY         milestone documents in order, retained rather than overwritten
```

## Reproduce

```bash
cd "02 COMPUTATIONS" && for f in *.py; do python "$f"; done
```

Twelve scripts. Each resolves its own paths and writes a JSON certificate beside itself.
The colour atlas is run separately from `03 COLOUR FIELD`, and the atomic web audits from
`06 ATOMIC WEB/05_Audit`. Every number in the standing account regenerates from these.

Python 3 with NumPy, SciPy, SymPy and Matplotlib.

---

## Why this is a separate limb and not folded into the books

The field reproduces the vacuum sector of general relativity from two counting variables
and derives several things the corpus wanted. It also carries a source sector that is not
finished, a forecast for Newton's constant that cosmology has not yet settled, and a colour
language whose objects are counted but not yet named.

Folding that wholesale into a closed argument would put weight on beams that are not yet
load bearing. The four results that *are* load bearing are listed in
`03 OPEN LEDGER ADDITIONS.md` as papers to be issued into `02 TECHNICAL PAPERS`, where the
corpus's own grading applies to them. Everything else stays here until it earns the move.

## The one-line version

The three weights are a perfect square. The least-action cell is the geometric mean of the
Planck and vacuum lengths, which makes Newton's constant and the cosmological constant
problem the same missing number. General relativity provably cannot see the difference
between the light mode and the density mode. And the composition bound of the colour field
is `arcsin(1/Λ)`, which selects eight, the carrier dimension.

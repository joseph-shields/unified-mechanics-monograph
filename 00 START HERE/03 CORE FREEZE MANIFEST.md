# Core Freeze Manifest
### Corpus Edition 2026, Fifth Printing · 27 July 2026

This manifest governs which objects constitute the printing. Where this file and any
other document disagree, this file governs.

## The frozen core

| file | what it carries | sha256 (first 16) |
|---|---|---|
| `00 The Corpus Atlas.pdf` | the map. Read first. | `bcbe3869d52312e5` |
| `A — A World of Distinctions.pdf` | the argument, 27 movements | `1947562888d1aabc` |
| `B1 — Universopedia, The Observational Standard.pdf` | the observational contract | `6b87313041c25f34` |
| `B2 — Universopedia, Systems of Interpretation.pdf` | the casebook, misses included | `6af28c33316b2fee` |
| `C — Unified Mechanics, The Formal Register.pdf` | the audit surface | `69f81ae51c847d2a` |
| `00 The Papers Index.pdf` | numbering, status, what supersedes what | `7b8268fd0686707d` |
| `20 The Forward Closure.pdf` | carrier, descent, one operator | `9c24c95a4ed78642` |
| `21 The Rank-Three Decay.pdf` | T29 to T32, new this printing | `11dc724074c96183` |
| `run_manifest.json` | proof that every number regenerates | `a236f2f1687db593` |
| `graph_certificate.json` | acyclicity and the obligation structure | `850342cfebde70f0` |

Full hashes for all 104 active files are in `04 SHA256SUMS.txt`. Verify with:

```bash
sha256sum -c "00 START HERE/04 SHA256SUMS.txt"
```

## What this printing changed

The argument was closed in the Fourth Printing. This printing attacked the proof
obligations and repaired the edition. Four results are added, T29 to T32, carried by
Paper 21. Five of the seven obligations are regraded. Seven edition defects are fixed.
The Edition Note lists all of them with the evidence.

## Graph certificate

64 nodes, 67 dependency edges, acyclic: True.
Longest chain: 7 steps. No result T1 to T32 depends on any open
obligation, so the obligations are terminal and the argument is closed. Regenerate with
`python run_all.py` from `04 REPRODUCIBILITY`.

## Preservation

Papers are preserved as issued. Corrections belong in new printings and in the Papers
Index, never in altered files. Paper 19's title page still reads *The Five Coordinates*
and that is deliberate. The Fourth Printing sits under `90 ARCHIVE/Printings/Fourth`,
byte-exact and verified by the release gate. Nothing under Archive governs a current claim.

## Movement numbering

Unchanged from the Fourth Printing. The concordance from the Third Printing numbering is
Part Nine of the Formal Register. Papers 18 and 19 cite the older numbering and are read
through that table.

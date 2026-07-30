# Addendum protocol

**The corpus is frozen. New work arrives here.**

Every printing of the corpus is a closed object. Reissuing one to carry a new
result means rebuilding the books, the papers, the manifests and the hashes, and
that cost is what stops results being published. So the corpus stops moving and
this folder moves instead.

---

## The rule

1. **Nothing in a corpus printing is edited to accommodate an addendum.** Not the
   books, not the papers as issued, not the reproducibility archive, not a
   manifest. A printing that has been frozen stays byte-identical.
2. **Each addendum is one folder, numbered `Ann`, self-contained.** It carries its
   own document, its own scripts, its own certificates and its own hashes. It can
   be read without any other addendum.
3. **Only `00 ADDENDA INDEX.md` changes when an addendum is added.** One line
   appended. That file is the single entry point, and it is the only thing a
   corpus README ever needs to point at.
4. **Every addendum states which corpus items it touches**, under one of three
   headings: it *extends* an item, it *sharpens* an item, or it *withdraws* an
   item. An addendum that touches nothing says so.
5. **Grades are the corpus grades.** PROVED, CONDITIONAL, PROPOSED, POSTULATE,
   OPEN, DISSOLVED. Never mixed, and every open item states why it is open.
6. **An addendum may demote its own claims.** Recording that something looked like
   a result and is not one is the main reason this folder exists. See A01 section
   six for the pattern.

## Promotion

An addendum is not a printing. Its results live here until they earn the move
into `02 TECHNICAL PAPERS`, and the move happens at a printing boundary, in a
batch, once. That is the only time the corpus reopens.

Until then the addendum is the citable source. It is dated, hashed and complete,
so citing it is not a promise of a future edition.

## Layout of an addendum

```
Ann <Title>/
    <Title>_Joseph_Shields.docx     the document, corpus house style
    <Title>_Joseph_Shields.pdf      the same, for reading
    *.py                            whatever regenerates the numbers
    *_results.json                  the certificate the scripts write
    SHA256SUMS.txt                  hashes of everything above
```

## Adding one

```bash
cd "C:/Users/joesh/Desktop/SCI/ADDENDA" && python "00 hash_addenda.py"
```

That rehashes every addendum folder and rewrites the per-folder `SHA256SUMS.txt`.
Append the index line by hand so the description is yours, not generated.

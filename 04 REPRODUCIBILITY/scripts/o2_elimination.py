"""O2, second half: eliminate candidates using results the corpus already proves.

Three rank-3 subsystems can be the decayed part: A1+A1+A1, A2+A1, A3.
Two tests are applied, each drawn from a PROVED result rather than from taste.

TEST ONE, from T10 (the minimal closed carrier history is triangular, PROVED).
  The decayed part is a part of the carrier, and anything that is a carrier history at
  all must be able to close. T10 proves the minimal closed history is a triangle: three
  roots with pairwise inner product -1 summing to zero. A subsystem containing no such
  triangle cannot host a closed history and therefore is not a carrier history that
  decays; it is a set of directions that were never a history.

TEST TWO, from T25 and Movement Twenty (sector classification by ONE operator).
  A reducible decayed subsystem is two mutually orthogonal decays with no operation
  connecting them, which is two independent decay operators. The corpus derives its
  sectors from one operator. A reducible candidate contradicts that.
"""

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
def _cert(n): return _os.path.join(_ROOT, "certificates", n)
def _csv(n):  return _os.path.join(_ROOT, n)
import itertools, json, os, datetime
import numpy as np



HERE = os.path.dirname(os.path.abspath(__file__))
R = []
for i, j in itertools.combinations(range(8), 2):
    for si, sj in itertools.product((2, -2), repeat=2):
        v = [0] * 8; v[i] = si; v[j] = sj
        R.append(tuple(v))
for s in itertools.product((1, -1), repeat=8):
    if s.count(-1) % 2 == 0:
        R.append(tuple(s))
R = np.array(sorted(set(R)), dtype=np.int64)
G = (R @ R.T) // 4

def span_roots(basis):
    B = R[basis].astype(float)
    P = B.T @ np.linalg.pinv(B @ B.T) @ B
    return np.where(np.abs(R.astype(float) @ P.T - R.astype(float)).max(axis=1) < 1e-8)[0]

def perp(basis):
    return np.where((G[np.ix_(np.arange(240), basis)] == 0).all(axis=1))[0]

def components(idx):
    idx = list(idx); seen, comps = set(), []
    for v in idx:
        if v in seen: continue
        st, c = [v], []; seen.add(v)
        while st:
            a = st.pop(); c.append(a)
            for b in idx:
                if b not in seen and G[a, b] != 0:
                    seen.add(b); st.append(b)
        comps.append(c)
    return comps

def has_closed_triangle(idx):
    """Three roots in the subsystem, pairwise inner product -1, summing to zero."""
    for a, b, c in itertools.combinations(idx, 3):
        if G[a, b] == -1 and G[a, c] == -1 and G[b, c] == -1:
            if not R[a].any() + 0 and False: pass
            if np.all(R[a] + R[b] + R[c] == 0):
                return True, (int(a), int(b), int(c))
    return False, None

# find one representative of each of the three rank-3 types
reps = {}
for j, k in itertools.combinations(range(1, 240), 2):
    tri = [0, j, k]
    if np.linalg.matrix_rank(R[tri]) != 3: continue
    S = sorted(span_roots(tri))
    n = len(S)
    key = {6: "A1+A1+A1", 8: "A2+A1", 12: "A3"}.get(n)
    if key and key not in reps:
        reps[key] = S
    if len(reps) == 3: break

results = []
for name in ("A1+A1+A1", "A2+A1", "A3"):
    S = reps[name]
    comps = components(S)
    tri_ok, witness = has_closed_triangle(S)
    P = sorted(perp(S))
    pc = components(P)
    surviving = {40: "D5 = so(10)", 30: "A5 = su(6)", 26: "D4+A1 = so(8) + su(2)"}[len(P)]
    results.append({
        "candidate": name,
        "roots": len(S),
        "irreducible_components": len(comps),
        "irreducible": len(comps) == 1,
        "contains_closed_triangle": tri_ok,
        "triangle_witness": [R[i].tolist() for i in witness] if witness else None,
        "surviving_symmetry": surviving,
        "surviving_rank": int(np.linalg.matrix_rank(R[P])),
        "surviving_roots": len(P),
        "surviving_components": len(pc),
        "passes_T10_closure_test": tri_ok,
        "passes_T25_one_operator_test": len(comps) == 1,
    })

print(f"{'candidate':<10} {'comps':>5} {'irred':>6} {'triangle':>9}   {'survivor':<22} {'verdict'}")
print("-" * 78)
for d in results:
    ok = d["passes_T10_closure_test"] and d["passes_T25_one_operator_test"]
    print(f"{d['candidate']:<10} {d['irreducible_components']:>5} "
          f"{str(d['irreducible']):>6} {str(d['contains_closed_triangle']):>9}   "
          f"{d['surviving_symmetry']:<22} {'SURVIVES' if ok else 'eliminated'}")

survivors = [d for d in results if d["passes_T10_closure_test"] and d["passes_T25_one_operator_test"]]
print()
if len(survivors) == 1:
    s = survivors[0]
    print(f"Unique candidate: decay on {s['candidate']}, surviving symmetry {s['surviving_symmetry']}.")
    print(f"Geometry block dimension {s['surviving_rank']}, which with T15 and T16 gives 3 + 1 + 1.")
    print(f"Triangle witness in the decayed part: {s['triangle_witness']} (in halves)")
else:
    print(f"{len(survivors)} candidates survive: {[s['candidate'] for s in survivors]}")

json.dump({"generated": datetime.datetime.now().isoformat(timespec="seconds"),
           "tests": {"T10": "decayed part must host a closed triangular history",
                     "T25": "decayed part must be irreducible, one operator"},
           "candidates": results,
           "survivors": [s["candidate"] for s in survivors]},
          open(_cert("o2_elimination_certificate.json"), "w"), indent=2)

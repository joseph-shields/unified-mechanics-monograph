"""O1 and O3, given T31 (the decay is on an A3 subsystem).

O1 asked for a concrete representation of the cluster projection C on the E8 carrier.
T31 supplies it. If the decayed part is the A3 subsystem, then the reduction is averaging
over the Weyl group of that A3, which is W(A3) = S4, of order 24:

        C(x) = (1/24) sum over w in W(A3) of  w x w^-1

All five conditions of A6 hold for group averaging and none of them is a choice:
unital because averaging fixes the identity; idempotent because averaging twice is
averaging once; completely positive because it is a convex combination of automorphisms;
bimodular over the fixed algebra because invariant elements pull out of the average;
covariant because the average is equivariant under the normalizer. So this is not a
candidate for C, it is the map A6 describes, once the subsystem is named.

O3 asked for the gauge algebra, the matter modules and the families. With the decayed
part fixed, E8 decomposes under A3 + D5 and T25 does the sorting: what commutes with the
decay is gauge, what connects distinct decay sectors is matter. The branching itself is
textbook; the framework's contribution is forcing which subsystem decays.

Everything below is verified from the root system rather than quoted.
"""

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
def _cert(n): return _os.path.join(_ROOT, "certificates", n)
def _csv(n):  return _os.path.join(_ROOT, n)
import itertools, json, os, datetime
from fractions import Fraction
import numpy as np



HERE = os.path.dirname(os.path.abspath(__file__))
R = []
for i, j in itertools.combinations(range(8), 2):
    for si, sj in itertools.product((2, -2), repeat=2):
        v = [0]*8; v[i] = si; v[j] = sj
        R.append(tuple(v))
for s in itertools.product((1, -1), repeat=8):
    if s.count(-1) % 2 == 0:
        R.append(tuple(s))
R = np.array(sorted(set(R)), dtype=np.int64)
G = (R @ R.T) // 4

# ---- pick an A3: three simple roots in a chain, inner products -1 -----------------
A3 = None
for a, b, c in itertools.combinations(range(240), 3):
    if G[a, b] == -1 and G[b, c] == -1 and G[a, c] == 0:
        if np.linalg.matrix_rank(R[[a, b, c]]) == 3:
            A3 = [a, b, c]; break
simple = R[A3].astype(float) / 2.0                 # back to true coordinates
span = simple.T @ np.linalg.pinv(simple @ simple.T) @ simple      # projector onto A3
perp = np.eye(8) - span

A3roots = [i for i in range(240) if np.allclose(R[i]/2.0 @ perp, 0)]
D5roots = [i for i in range(240) if np.allclose(R[i]/2.0 @ span, 0)]
mixed   = [i for i in range(240) if i not in A3roots and i not in D5roots]

# ---- O1: build W(A3) explicitly and confirm its fixed subspace --------------------
def refl(a):
    a = a / np.linalg.norm(a)
    return np.eye(8) - 2 * np.outer(a, a)

gens = [refl(R[i].astype(float)/2.0) for i in A3]
group, frontier = [np.eye(8)], [np.eye(8)]
while frontier:
    nxt = []
    for g in frontier:
        for s in gens:
            h = s @ g
            if not any(np.allclose(h, k) for k in group):
                group.append(h); nxt.append(h)
    frontier = nxt
C = sum(group) / len(group)                        # the averaging projector
eig = np.linalg.eigvalsh(C)
fixed_dim = int(round(sum(abs(e - 1) < 1e-9 for e in eig)))

# ---- O3: sort the 248 by how each piece stands with the decay (T25) ---------------
def a3norm2(i):  return Fraction(round(4 * float(R[i]/2.0 @ span @ (R[i]/2.0))), 4)
buckets = {}
for i in mixed:
    buckets.setdefault(a3norm2(i), []).append(i)

report = {
    "generated": datetime.datetime.now().isoformat(timespec="seconds"),
    "O1": {
        "reduction": "averaging over W(A3)",
        "group_order": len(group),
        "group_is_S4": len(group) == 24,
        "C_is_idempotent": bool(np.allclose(C @ C, C)),
        "C_is_symmetric": bool(np.allclose(C, C.T)),
        "fixed_subspace_dimension": fixed_dim,
        "decayed_dimension": 8 - fixed_dim,
    },
    "O3": {
        "A3_roots": len(A3roots), "D5_roots": len(D5roots), "mixed_roots": len(mixed),
        "dim_A3": len(A3roots) + 3, "dim_D5": len(D5roots) + 5,
        "total_dim": len(A3roots) + 3 + len(D5roots) + 5 + len(mixed),
    },
}

print("O1  the concrete reduction")
print(f"  W(A3) built from its reflections: order {len(group)}   S4: {len(group)==24}")
print(f"  averaging map C idempotent: {np.allclose(C@C, C)}   symmetric: {np.allclose(C, C.T)}")
print(f"  fixed subspace dimension: {fixed_dim}     decayed: {8-fixed_dim}")
print(f"  -> the geometry block is {fixed_dim}-dimensional, so 3 + 1 + 1 by T15 and T16")
print()
print("O3  the sorting of the 248 by T25")
print(f"  decayed sector   A3 = su(4):  {len(A3roots)} roots + 3 Cartan = {len(A3roots)+3}")
print(f"  commutes, GAUGE  D5 = so(10): {len(D5roots)} roots + 5 Cartan = {len(D5roots)+5}")
print(f"  connects sectors, MATTER:     {len(mixed)} roots")
print(f"  total: {len(A3roots)+3+len(D5roots)+5+len(mixed)}")
print()
print("  matter split by how far each root leans into the decayed sector:")
names = {Fraction(3,4): "(4, 16) + (4bar, 16bar)   spinor of so(10)",
         Fraction(1,1): "(6, 10)                   vector of so(10)"}
for k in sorted(buckets):
    print(f"    |proj_A3|^2 = {str(k):<4}  count {len(buckets[k]):>3}   {names.get(k,'?')}")
    report["O3"].setdefault("matter_buckets", {})[str(k)] = len(buckets[k])

json.dump(report, open(_cert("o1_o3_certificate.json"), "w"), indent=2)

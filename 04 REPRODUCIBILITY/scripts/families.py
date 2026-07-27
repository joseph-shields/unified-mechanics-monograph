"""How many families? The count is decided by the decay's own Weyl group.

Matter sits in (4,16) + (4bar,16bar). The 16 is one generation; the family index is the
4 of the decayed su(4). So the question "how many families" is the question "what is the
4, as a module for the group the reduction averages over".

W(A3) = S4 permutes the four weight spaces of the fundamental, so the family index space
is the permutation module on four points, and that module is never irreducible:

        C^4  =  trivial (1)  +  standard (3)

C averages over W(A3), so the trivial summand is exactly the direction the decay cannot
tell apart from itself. T25 admits an operation as matter when it "connects distinct
decay sectors" and "closes into a cycle reproducing their readable identity". The
invariant direction connects nothing, because the decay leaves it fixed; it produces no
readable identity distinct from the decayed sector. The three non-invariant directions
each do.

Everything is verified below by explicit character computation, not quoted.
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

A3 = None
for a, b, c in itertools.combinations(range(240), 3):
    if G[a,b] == -1 and G[b,c] == -1 and G[a,c] == 0 and np.linalg.matrix_rank(R[[a,b,c]]) == 3:
        A3 = [a, b, c]; break
S = R[A3].astype(float)/2.0
span = S.T @ np.linalg.pinv(S @ S.T) @ S

def refl(a):
    a = a/np.linalg.norm(a); return np.eye(8) - 2*np.outer(a, a)
gens = [refl(R[i].astype(float)/2.0) for i in A3]
W, frontier = [np.eye(8)], [np.eye(8)]
while frontier:
    nxt = []
    for g in frontier:
        for s in gens:
            h = s @ g
            if not any(np.allclose(h, k) for k in W):
                W.append(h); nxt.append(h)
    frontier = nxt
assert len(W) == 24, len(W)

# ---- the family index: A3-projections of the spinor-sector roots ------------------
spinor = [i for i in range(240)
          if abs(float(R[i]/2.0 @ span @ (R[i]/2.0)) - 0.75) < 1e-9]
weights = []
for i in spinor:
    w = span @ (R[i].astype(float)/2.0)
    if not any(np.allclose(w, v) for v in weights):
        weights.append(w)
weights = np.array(weights)

# split the distinct weights into W-orbits
orbits, seen = [], set()
for k in range(len(weights)):
    if k in seen: continue
    orb = set()
    for g in W:
        img = g @ weights[k]
        for m in range(len(weights)):
            if np.allclose(img, weights[m]):
                orb.add(m)
    seen |= orb
    orbits.append(sorted(orb))

# ---- character of the permutation module on one orbit of four --------------------
def perm_character(orbit):
    """chi(g) = number of weights in the orbit that g fixes."""
    chi = []
    for g in W:
        f = 0
        for m in orbit:
            if np.allclose(g @ weights[m], weights[m]): f += 1
        chi.append(f)
    return chi

report = {"generated": datetime.datetime.now().isoformat(timespec="seconds"),
          "spinor_sector_roots": len(spinor),
          "distinct_family_weights": len(weights),
          "orbits": [len(o) for o in orbits]}

print(f"spinor-sector roots (|proj_A3|^2 = 3/4): {len(spinor)}")
print(f"distinct family-index weights: {len(weights)}")
print(f"W(A3)-orbits on them: sizes {[len(o) for o in orbits]}  (the 4 and the 4bar)")
print()

for n, orb in enumerate(orbits):
    chi = perm_character(orb)
    mult_trivial = Fraction(sum(chi), len(W))
    # <chi,chi> tells us how many irreducible pieces there are
    self_ip = Fraction(sum(c*c for c in chi), len(W))
    print(f"orbit {n+1}: size {len(orb)}")
    print(f"   <chi, trivial> = {mult_trivial}      multiplicity of the invariant direction")
    print(f"   <chi, chi>     = {self_ip}      number of irreducible summands")
    print(f"   => the family index space splits as {mult_trivial} + {len(orb) - mult_trivial}")
    report[f"orbit_{n+1}"] = {"size": len(orb), "trivial_multiplicity": int(mult_trivial),
                              "irreducible_summands": int(self_ip),
                              "non_invariant_dimension": int(len(orb) - mult_trivial)}

k = report["orbit_1"]["non_invariant_dimension"]
print()
print(f"Families that connect distinct decay sectors and carry a distinct readable")
print(f"identity, per T25: {k}")
print(f"Families if the decay-invariant direction is also counted: {report['orbit_1']['size']}")

json.dump(report, open(_cert("families_certificate.json"), "w"), indent=2)

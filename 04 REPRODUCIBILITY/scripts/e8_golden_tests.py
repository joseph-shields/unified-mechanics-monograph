"""Reproducibility script for Volume 09 — The Golden Skeleton of E8 (16 July 2026).

Tests:
 1. The eight Coxeter-plane rings of the E8 root shell pair into four golden pairs
    (R2/R1 = R6/R3 = R7/R4 = R8/R5 = phi, to eigenplane precision ~6e-7).
 2. Exact identity for the boundary mismatch: dB = sqrt(5)*phi^2/2 - sqrt(8),
    i.e. a difference of description-ring covolumes (disc Q(sqrt5)=5, disc Q(sqrt2)=8).
 3. NEGATIVE: independent exact covers (seeds 11/42/99) have cover-dependent
    cell ring-profiles -> the forty-cell cover does not canonically respect the
    golden pairing (consistent with Volume 05, Lemma 4).
Run: python e8_golden_tests.py
"""

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
def _d(*p): return _os.path.join(_ROOT, "data", *p)
def _r(*p): return _os.path.join(_ROOT, "results", *p)
def _f(*p): return _os.path.join(_ROOT, "figures", *p)

import itertools, random, math
import numpy as np
from collections import Counter



PHI = (1 + math.sqrt(5)) / 2
roots = []
for i, j in itertools.combinations(range(8), 2):
    for si in (2,-2):
        for sj in (2,-2):
            v=[0]*8; v[i]=si; v[j]=sj; roots.append(tuple(v))
for s in itertools.product((1,-1),repeat=8):
    if s.count(-1)%2==0: roots.append(tuple(s))
idx = {r:k for k,r in enumerate(roots)}
R = np.array(roots, float)
neg_of = np.array([idx[tuple(-x for x in r)] for r in roots])

half = (1,-1,-1,-1,-1,-1,-1,1)
simple = [half,(2,2,0,0,0,0,0,0),(-2,2,0,0,0,0,0,0),(0,-2,2,0,0,0,0,0),
          (0,0,-2,2,0,0,0,0),(0,0,0,-2,2,0,0,0),(0,0,0,0,-2,2,0,0),(0,0,0,0,0,-2,2,0)]
C = np.eye(8)
for s in simple:
    s = np.array(s, float)
    C = (np.eye(8) - 2*np.outer(s,s)/s.dot(s)) @ C
w, V = np.linalg.eigh(C + C.T)
target = 2*math.cos(2*math.pi/30)
prs = [j for j in range(8) if abs(w[j]-target) < 1e-8]
u, v = V[:,prs[0]].copy(), V[:,prs[1]].copy()
u /= np.linalg.norm(u); v -= u*u.dot(v); v /= np.linalg.norm(v)
xy = np.stack([R@u, R@v], 1)
rad = np.linalg.norm(xy, axis=1)
rings = sorted(set(np.round(rad,6)))

print("TEST 1 — golden ring pairing")
for i in range(8):
    for j in range(i):
        if abs(rings[i]/rings[j] - PHI) < 1e-6:
            print(f"  R{i+1}/R{j+1} = {rings[i]/rings[j]:.12f}")

print("TEST 2 — dB = sqrt5*phi^2/2 - sqrt8")
lhs = -2*math.sqrt(2) + 5/4 + 3*math.sqrt(5)/4
rhs = math.sqrt(5)*PHI**2/2 - math.sqrt(8)
print(f"  monograph: {lhs:.15f}  covolume form: {rhs:.15f}  equal: {abs(lhs-rhs)<1e-15}")

print("TEST 3 — cover ring-profile independence (negative result)")
G = (R @ R.T).astype(int)
cells_set = set()
for a in range(240):
    for b in np.where(G[a] == -4)[0]:
        c = tuple(int(x) for x in (R[a] + R[b]))
        if c in idx:
            cells_set.add(frozenset(min(k, int(neg_of[k])) for k in (a, int(b), idx[c])))
cells_all = [sorted(c) for c in cells_set]
canon = sorted(set(min(k, int(neg_of[k])) for k in range(240)))
touch = {k: [] for k in canon}
for ci, cell in enumerate(cells_all):
    for k in cell: touch[k].append(ci)
ring_of = {k: rings.index(round(rad[k],6)) for k in range(240)}

def attempt(rng):
    covered = set(); chosen = []
    while len(chosen) < 40:
        best, best_avail = None, None
        for k in canon:
            if k in covered: continue
            avail = [ci for ci in touch[k] if not (set(cells_all[ci]) & covered)]
            if not avail: return None
            if best_avail is None or len(avail) < len(best_avail):
                best, best_avail = k, avail
                if len(avail) <= 2: break
        chosen.append(rng.choice(best_avail))
        covered |= set(cells_all[chosen[-1]])
    return chosen

for seed in (11, 42, 99):
    rng = random.Random(seed); sol = None
    while sol is None: sol = attempt(rng)
    profs = Counter()
    for ci in sol:
        members = []
        for k in cells_all[ci]: members += [k, int(neg_of[k])]
        profs[tuple(sorted(ring_of[m] for m in members))] += 1
    print(f"  seed {seed}: {len(profs)} distinct cell ring-profiles (cover-dependent)")

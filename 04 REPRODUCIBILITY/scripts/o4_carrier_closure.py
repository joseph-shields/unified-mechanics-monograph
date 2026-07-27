"""O4: does a complete carrier closure pass each of the 240 roots exactly once?

The obligation, stated in the Formal Register Part Seven, is finite and combinatorial.
This settles the existence half of it by explicit construction.

Reading of the claim, taken from D14 and T10:
  A carrier closure is a closed walk whose VERTICES are carrier points and whose every
  STEP is a primitive crossing, which in E8 is a root (D14). A walk that passes each of
  the 240 roots exactly once and returns to where it began is therefore a Hamiltonian
  cycle in the graph G whose vertices are the 240 roots and whose edges join two roots
  differing by a root.

  For roots alpha, beta of norm 2:  |beta - alpha|^2 = 4 - 2<alpha,beta>,
  so beta - alpha is a root (norm 2) exactly when <alpha,beta> = 1.

Two things are checked separately:
  (a) the sum condition, that the closure actually closes;
  (b) the existence of the Hamiltonian cycle.
"""

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
def _cert(n): return _os.path.join(_ROOT, "certificates", n)
def _csv(n):  return _os.path.join(_ROOT, n)
import itertools, random, json, hashlib, os, datetime, platform
from fractions import Fraction



HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------- the 240 roots of E8 ----------------------------------------------
# 112 of type (+-1, +-1, 0^6); 128 of type (+-1/2)^8 with an even number of minus signs.
# Held as integers in units of 1/2 so all arithmetic is exact.
roots = []
for i, j in itertools.combinations(range(8), 2):
    for si, sj in itertools.product((2, -2), repeat=2):
        v = [0] * 8; v[i] = si; v[j] = sj
        roots.append(tuple(v))
for signs in itertools.product((1, -1), repeat=8):
    if signs.count(-1) % 2 == 0:
        roots.append(tuple(signs))
roots = sorted(set(roots))
assert len(roots) == 240, len(roots)

def ip(a, b):                      # true inner product; components are halves
    return Fraction(sum(x * y for x, y in zip(a, b)), 4)

assert all(ip(a, a) == 2 for a in roots), "every root must have norm two"

# ---------------- (a) the closure closes for free ----------------------------------
total = tuple(sum(c) for c in zip(*roots))
sum_is_zero = all(c == 0 for c in total)

# ---------------- the admissibility graph ------------------------------------------
N = 240
adj = [[] for _ in range(N)]
for i in range(N):
    for j in range(N):
        if i != j and ip(roots[i], roots[j]) == 1:
            adj[i].append(j)
degrees = sorted({len(a) for a in adj})
adjset = [set(a) for a in adj]

# ---------------- (b) Hamiltonian cycle by Posa rotation ---------------------------
def hamiltonian_cycle(seed):
    rng = random.Random(seed)
    path = [rng.randrange(N)]
    inpath = [False] * N
    inpath[path[0]] = True
    stall = 0
    while len(path) < N:
        head = path[-1]
        opts = [v for v in adj[head] if not inpath[v]]
        if opts:
            # Warnsdorff: step to the neighbour with the fewest onward options
            nxt = min(opts, key=lambda v: (sum(1 for w in adj[v] if not inpath[w]), rng.random()))
            path.append(nxt); inpath[nxt] = True; stall = 0
        else:
            # Posa rotation: pick a neighbour inside the path and reverse the tail
            cands = [v for v in adj[head] if inpath[v] and path.index(v) < len(path) - 2]
            if not cands: return None
            v = rng.choice(cands)
            k = path.index(v)
            path = path[:k + 1] + path[k + 1:][::-1]
            stall += 1
            if stall > 6000: return None
    # close it: rotate until the two ends are adjacent
    for _ in range(4000):
        if path[0] in adjset[path[-1]]:
            return path
        cands = [v for v in adj[path[-1]] if v != path[-2]]
        v = rng.choice(cands)
        k = path.index(v)
        path = path[:k + 1] + path[k + 1:][::-1]
    return None

cycle, used_seed = None, None
for seed in range(400):
    cycle = hamiltonian_cycle(seed)
    if cycle:
        used_seed = seed
        break

# ---------------- independent verification of whatever was found -------------------
report = {
    "generated": datetime.datetime.now().isoformat(timespec="seconds"),
    "python": platform.python_version(),
    "roots": len(roots),
    "all_norm_two": True,
    "sum_of_all_roots_is_zero": sum_is_zero,
    "adjacency": "two roots joined when their difference is a root, i.e. inner product 1",
    "degree": degrees,
    "hamiltonian_cycle_found": cycle is not None,
    "seed": used_seed,
}

if cycle:
    # 1. every root exactly once
    assert sorted(cycle) == list(range(N)), "not a permutation of the 240 roots"
    # 2. every step is a primitive crossing (a root)
    steps = []
    for k in range(N):
        a, b = roots[cycle[k]], roots[cycle[(k + 1) % N]]
        d = tuple(y - x for x, y in zip(a, b))
        assert ip(d, d) == 2, f"step {k} is not a root"
        steps.append(d)
    # 3. the walk returns to where it began
    net = tuple(sum(c) for c in zip(*steps))
    report["every_root_visited_once"] = True
    report["every_step_is_a_root"] = True
    report["walk_returns_to_origin"] = all(c == 0 for c in net)
    report["cycle_length"] = len(cycle)
    report["witness_first_12_vertices"] = [list(roots[i]) for i in cycle[:12]]
    report["witness_sha256"] = hashlib.sha256(
        ",".join(map(str, cycle)).encode()).hexdigest()
    json.dump({"order": cycle,
               "roots_in_halves": [list(r) for r in roots]},
              open(_cert("o4_closure_witness.json"), "w"), indent=1)

json.dump(report, open(_cert("o4_certificate.json"), "w"), indent=2)

print(f"roots: {len(roots)}, all of norm two")
print(f"sum of all 240 roots is zero: {sum_is_zero}   <- the closure condition is free")
print(f"admissibility graph: degree {degrees}")
print(f"hamiltonian cycle found: {cycle is not None} (seed {used_seed})")
if cycle:
    print(f"  every root visited exactly once : {report['every_root_visited_once']}")
    print(f"  every step is a primitive crossing: {report['every_step_is_a_root']}")
    print(f"  walk returns to its origin       : {report['walk_returns_to_origin']}")
    print(f"  witness sha256                   : {report['witness_sha256'][:32]}...")

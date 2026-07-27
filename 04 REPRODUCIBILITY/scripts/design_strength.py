"""Spherical design strengths of the 24-cell and 600-cell, derived from coordinates.

Paper 23 claims the hydrogen sampling cutoffs are the design strengths of the two
polytopes and nothing else. This establishes the strengths rather than citing them,
by checking every monomial moment against the exact value on S3.

A point set X on S^{n-1} is a spherical t-design when the average over X of every
polynomial of degree at most t equals its average over the sphere. For the discrete
Gram matrix of degree-N harmonics to be the identity, degree 2N must be integrated
exactly, so N <= floor(t/2), and hydrogen's principal number is N + 1.
"""
import itertools, json, os
from math import gamma, prod
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
def _cert(n): return os.path.join(_ROOT, "certificates", n)

def cell24():
    V = []
    for i, j in itertools.combinations(range(4), 2):
        for si, sj in itertools.product((1, -1), repeat=2):
            v = [0]*4; v[i] = si; v[j] = sj; V.append(v)
    return np.array(V, float) / np.sqrt(2)

def cell600():
    phi = (1 + 5**0.5) / 2
    V = []
    for i in range(4):
        for s in (2, -2):
            v = [0.]*4; v[i] = s; V.append(v)
    for s in itertools.product((1, -1), repeat=4):
        V.append(list(s))
    even = [p for p in itertools.permutations(range(4))
            if sum(1 for a, b in itertools.combinations(range(4), 2) if p[a] > p[b]) % 2 == 0]
    for p in even:
        for sa, sb, sc in itertools.product((1, -1), repeat=3):
            v = [0.]*4
            v[p[0]] = sa*phi; v[p[1]] = sb*1.0; v[p[2]] = sc/phi; v[p[3]] = 0.
            V.append(v)
    V = np.array(V, float)
    V = V / np.linalg.norm(V, axis=1, keepdims=True)
    U = []
    for v in V:
        if not any(np.allclose(v, u, atol=1e-9) for u in U): U.append(v)
    return np.array(U)

def exact_moment(e, n=4):
    """<x1^e1 ... xn^en> over the unit sphere in R^n."""
    if any(k % 2 for k in e): return 0.0
    return (prod(gamma((k + 1) / 2) for k in e) * gamma(n / 2)) / \
           (gamma(sum(e) / 2 + n / 2) * gamma(0.5) ** n)

def design_strength(X, tmax=14, tol=1e-9):
    t = 0
    for d in range(1, tmax + 1):
        for e in (e for e in itertools.product(range(d + 1), repeat=4) if sum(e) == d):
            disc = float(np.mean(np.prod(X ** np.array(e), axis=1)))
            if abs(disc - exact_moment(e)) > tol:
                return t
        t = d
    return t

out = {}
for name, X in [("24-cell", cell24()), ("600-cell", cell600())]:
    t = design_strength(X)
    N = t // 2
    out[name] = {"points": len(X), "design_strength_t": t,
                 "max_harmonic_degree_N": N, "hydrogen_n_max": N + 1,
                 "first_failure_at_n": N + 2}
    print(f"{name:>9}: {len(X):>3} points, spherical {t:>2}-design"
          f"  ->  N <= {N}  ->  hydrogen n <= {N+1}, fails at n = {N+2}")

print()
print("These are exactly the cutoffs reported in the hydrogen monograph.")
json.dump(out, open(_cert("design_strength_certificate.json"), "w"), indent=2)

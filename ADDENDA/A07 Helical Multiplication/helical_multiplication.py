"""HELICAL MULTIPLICATION.

An operation, its algebra, and what it selects.

    x (*) y  =  x y / sqrt| N(x y) |

where N is the field norm of Q(sqrt d). Multiply, then normalise by the square
root of the absolute norm. That is the whole definition.

What it does:

  * On the shell |N| = 1 it is ORDINARY multiplication, because the divisor is 1.
  * Off the shell it is a RETRACTION onto the shell, in one step.
  * The shell is the unit group, so it is closed, and the operation never leaves it.

Why the sign does not matter, stated as structure rather than as permission: the
norm takes values +1 and -1 on the shell, so the shell carries a Z/2 grading. That
grading is the phase. phi sits at -1, phi^2 at +1, and one turn flips it while two
turns restore it. **Phase has period two and the exponent has none.** That is the
helix written in arithmetic: what comes back is the sign, what never comes back is
the height.

What it selects: every real quadratic field has a fundamental unit, so there is one
attractor per field and the family is infinite. The operation is therefore NOT
unique to phi. But the attractors are ordered by growth per turn, and phi is the
smallest of all of them. Minimal expansion picks it out with nothing else supplied.

Run:  PYTHONUTF8=1 python helical_multiplication.py
"""

import json, math, os, datetime
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "helical_multiplication_results.json")


def norm(x, d):
    """The field norm of Q(sqrt d): x times its conjugate."""
    return sp.simplify(sp.expand(x * x.subs(sp.sqrt(d), -sp.sqrt(d))))


def hmul(x, y, d):
    """Helical multiplication. Multiply, then land on the shell."""
    p = sp.expand(x * y)
    n = norm(p, d)
    if n == 0:
        raise ZeroDivisionError("norm zero has no helical image")
    return sp.radsimp(sp.simplify(p / sp.sqrt(sp.Abs(n))))


d = 5
s5 = sp.sqrt(5)
phi = (1 + s5) / 2
res = {"generated": datetime.datetime.now().isoformat(timespec="seconds")}

print("HELICAL MULTIPLICATION")
print("=" * 78)
print("   x (*) y = x y / sqrt|N(x y)|      N = the field norm of Q(sqrt5)")
print()

# ── 1. on the shell it is ordinary multiplication ──────────────────────────
print("1  ON THE SHELL IT IS ORDINARY MULTIPLICATION")
shell = [phi, phi**2, phi**3, phi**4, phi**6]
ok = True
for a in shell:
    for b in shell:
        h = hmul(a, b, d)
        p = sp.radsimp(sp.simplify(a * b))
        if sp.simplify(h - p) != 0:
            ok = False
print("   every pair of units: helical product equals the ordinary product ->", ok)
print("   because |N| = 1 makes the divisor 1. The operation adds nothing there.")
res["ordinary_on_shell"] = bool(ok)

# ── 2. off the shell it retracts, in one step ─────────────────────────────
print()
print("2  OFF THE SHELL IT RETRACTS IN ONE STEP")
print("   %-22s %-12s %-24s %s" % ("input x", "N(x)", "x (*) 1", "N of the image"))
tests = [sp.Integer(3) + s5, sp.Integer(7), sp.Integer(2) + 3 * s5,
         sp.Rational(1, 3) + s5 / 7, phi + 1, sp.Integer(9) + 4 * s5]
rows = []
for x in tests:
    h = hmul(x, sp.Integer(1), d)
    nx, nh = norm(x, d), norm(h, d)
    rows.append(dict(x=sp.sstr(x), N_x=sp.sstr(nx), image=sp.sstr(h), N_image=sp.sstr(nh)))
    print("   %-22s %-12s %-24s %s" % (sp.sstr(x), sp.sstr(nx), sp.sstr(h), sp.sstr(nh)))
print("   every image has |N| = 1. One application is enough, always, because")
print("   N(x/sqrt|N(x)|) = N(x)/|N(x)| = +-1 identically.")
res["retraction"] = rows

# ── 3. the phase is a Z/2 grading, and that is the helix ──────────────────
print()
print("3  THE SIGN IS A PHASE, NOT AN AMBIGUITY")
print("   %-10s %-26s %-8s %s" % ("power", "value", "N", "phase"))
ph = []
for k in range(1, 9):
    v = sp.radsimp(sp.simplify(phi**k))
    n = norm(v, d)
    ph.append(dict(k=k, value=sp.sstr(v), N=int(n)))
    print("   phi^%-6d %-26s %-8s %s" % (k, sp.sstr(v), sp.sstr(n),
                                         "contraction" if n < 0 else "expansion"))
res["phase_grading"] = ph
print()
print("   N alternates -1, +1, -1, +1 with period two. The exponent never returns.")
print("   Phase comes back and height does not: the helix, in arithmetic.")

# ── 4. non-uniqueness: one attractor per field ───────────────────────────
print()
print("4  NON-UNIQUENESS. Every real quadratic field has its own attractor.")


def fundamental_unit(dd):
    """Smallest unit > 1 of Q(sqrt dd), by the continued fraction of sqrt dd."""
    a0 = sp.Integer(int(math.isqrt(dd)))
    if a0 * a0 == dd:
        return None
    # solve x^2 - dd y^2 = +-1 by brute search on y, adequate for small dd
    best = None
    for y in range(1, 200000):
        for sgn in (-1, 1):
            v = dd * y * y + sgn
            x = math.isqrt(v)
            if x * x == v and x > 0:
                cand = sp.Integer(x) + sp.Integer(y) * sp.sqrt(dd)
                if dd % 4 == 1:  # half-integer units smaller
                    pass
                best = cand
                break
        if best is not None:
            break
    return best


SQFREE = [2, 3, 5, 6, 7, 10, 11, 13, 14, 15, 17, 19, 21, 22, 23, 26, 29, 30, 31]
print("   %-5s %-28s %14s" % ("d", "fundamental unit > 1", "growth per turn"))
units = []
for dd in SQFREE:
    if dd == 5:
        u, uv = phi, float(phi)
    elif dd == 13:
        u, uv = (3 + sp.sqrt(13)) / 2, float((3 + math.sqrt(13)) / 2)
    elif dd == 21:
        u, uv = (5 + sp.sqrt(21)) / 2, float((5 + math.sqrt(21)) / 2)
    elif dd == 29:
        u, uv = (5 + sp.sqrt(29)) / 2, float((5 + math.sqrt(29)) / 2)
    else:
        u = fundamental_unit(dd)
        uv = float(u) if u is not None else None
    if uv is None:
        continue
    units.append(dict(d=dd, unit=sp.sstr(u), value=uv))
    print("   %-5d %-28s %14.6f%s" % (dd, sp.sstr(u), uv,
                                      "   <- smallest" if dd == 5 else ""))
res["fundamental_units"] = units

mn = min(units, key=lambda z: z["value"])
print()
print("   the family is infinite, so the operation is NOT unique to phi.")
print("   but the attractors are ordered, and the minimum is at d = %d:" % mn["d"])
print("   **phi = %.9f is the least fundamental unit of any real quadratic field.**"
      % mn["value"])
print("   Minimal growth per turn selects it, with nothing else supplied.")
res["minimal"] = mn

# ── 5. bending an arbitrary quantity toward the attractor ────────────────
print()
print("5  BENDING A QUANTITY TOWARD THE ATTRACTOR")
print("   repeated helical multiplication by phi, from an arbitrary start:")
x = sp.Rational(17, 4) + sp.Rational(2, 3) * s5
print("   %-6s %-30s %-10s %s" % ("turn", "state", "N", "ratio to previous"))
prev = None
trace = []
for k in range(6):
    n = norm(x, d)
    rat = "" if prev is None else "%.9f" % (float(x) / prev)
    trace.append(dict(turn=k, state=sp.sstr(x), N=sp.sstr(n),
                      value=float(x), ratio=rat))
    print("   %-6d %-30s %-10s %s" % (k, sp.sstr(x), sp.sstr(n), rat))
    prev = float(x)
    x = hmul(x, phi, d)
print("   after the first turn the norm is fixed at +-1 and the ratio is exactly")
print("   phi = %.9f. The state is on the attractor and every further turn is one" % float(phi))
print("   step up the helix: same phase alternation, monotone height.")
res["bending"] = trace

json.dump(res, open(OUT, "w"), indent=2)
print()
print("written:", OUT)

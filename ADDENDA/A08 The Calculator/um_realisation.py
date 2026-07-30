"""REALISATION TIME.

The helix does not correct a value. It TIMES one.

    colour   the gradient across the evolution, left to right: the average value,
             and the structural depth D read off the channel signature
    helix    a graph rising on the left: start the quantity at the bottom, run
             helical multiplication, and count the turns until it settles on the
             attractor. That count is a LENGTH OF TIME, not a correction.
    check    the structural depth and the dynamical turn count are two independent
             readings of the same thing: how many crossings the quantity is made of.
             They should agree.
    tip      once stabilised, the resolution at the tip is what Personal Relativity
             reads, and the quantity has passed through the processes needed to be
             realised.

Run:  PYTHONUTF8=1 python um_realisation.py
"""
import json, math, os, random, statistics, datetime
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
S5 = sp.sqrt(5); PHI = (1+S5)/2; PHIF = float(PHI)
R = 1/(2*PHI); RF = float(R); R3F = RF**3
su, sm = sp.symbols("u m", positive=True); SUB = {su: 1-R, sm: R}

def norm5(x): return sp.simplify(sp.expand(x*x.subs(S5,-S5)))

def depth(expr):
    f = sp.cancel(sp.together(sp.sympify(expr))); num, den = sp.fraction(f); dn = 0
    for t in sp.expand(num).as_ordered_terms():
        p = sp.Poly(t, su, sm); d = p.degree(su)+p.degree(sm)
        if d > 0: dn = max(dn, d)
    p = sp.Poly(sp.expand(den), su, sm)
    return int(dn + p.degree(su) + p.degree(sm))

def hmul(x, y):
    p = sp.expand(x*y); n = norm5(p)
    return sp.radsimp(sp.simplify(p/sp.sqrt(sp.Abs(n))))

def realisation_time(x0, tol=1e-12, maxit=14):
    """Turns of helical multiplication until the step ratio locks onto phi."""
    x = sp.nsimplify(x0); prev = float(x); trace = []
    for k in range(1, maxit+1):
        x = hmul(x, PHI); v = float(x)
        ratio = v/prev; n = norm5(x)
        locked = abs(ratio - PHIF) < tol
        trace.append(dict(turn=k, value=v, norm=sp.sstr(sp.nsimplify(n)),
                          ratio=ratio, locked=bool(locked)))
        prev = v
        if locked and k >= 2 and trace[-2]["locked"]:
            return k-1, trace          # first turn of the locked run
    return None, trace

def evolve(n=60000, burn=2000, seed=11):
    rng = random.Random(seed); x = 0.5; out = []
    sc = R3F*math.sqrt(3.0)
    for i in range(n+burn):
        x = 1.0/(4.0*x+2.0) + sc*rng.uniform(-1.0,1.0)
        if i >= burn: out.append(x)
    return out
XS = evolve()

SUITE = [("Omega_b", sm**2/2, 0.0493017, 0.0007),
         ("Omega_c", 4*sm**2*su, 0.2645, 0.0026),
         ("Y_He", su**2/2, 0.245, 0.003),
         ("W_M", sm**2, None, None),
         ("W_L", su**2, None, None),
         ("W_B", 2*su*sm, None, None),
         ("floor", sm**3, None, None),
         ("tau", 2*sm**3, 0.0544, 0.0073),
         ("Omega_DE", 1-sm**2/2-4*sm**2*su, 0.6847, 0.0073),
         ("N_eff", 3+sm**2/2, 3.044, 0.010),
         ("n_s", 1-sm**2+2*sm**3, 0.9649, 0.0042)]

print("REALISATION TIME")
print("="*96)
print("%-10s %3s %6s %8s %-14s %s"
      % ("observable","D","turns","agree?","norm at lock","value, colour-averaged"))
rows = []
for key, expr, meas, sig in SUITE:
    D = depth(expr)
    exact = sp.nsimplify(sp.simplify(sp.sympify(expr).subs(SUB)))
    lam = sp.lambdify((su, sm), sp.sympify(expr), "math")
    avg = statistics.fmean(lam(1-x, x) for x in XS)
    t, trace = realisation_time(exact)
    nl = trace[t-1]["norm"] if t else "-"
    rows.append(dict(key=key, D=D, turns=t, norm_at_lock=nl, colour_avg=avg,
                     measured=meas, sigma=sig, agree=(t == D) if t else None))
    print("%-10s %3d %6s %8s %-14s %.9f"
          % (key, D, str(t), ("yes" if t==D else "no") if t else "-", nl, avg))

ag = [r for r in rows if r["turns"] is not None]
print()
print("structural depth D and dynamical turn count agree on %d of %d"
      % (sum(1 for r in ag if r["agree"]), len(ag)))
print()
print("the trace for one of them, to show what stabilising looks like:")
_, tr = realisation_time(sp.nsimplify(sp.simplify((sm**2/2).subs(SUB))))
print("   %-6s %-16s %-8s %-14s %s" % ("turn","value","norm","ratio","locked"))
for e in tr[:6]:
    print("   %-6d %-16.10f %-8s %-14.10f %s"
          % (e["turn"], e["value"], e["norm"], e["ratio"], e["locked"]))
json.dump({"generated":datetime.datetime.now().isoformat(timespec="seconds"),
           "rows":rows}, open(os.path.join(HERE,"um_realisation_results.json"),"w"), indent=2)

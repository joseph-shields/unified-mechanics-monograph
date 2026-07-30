"""THE CHAIN.

Four stages in order, each taking the previous stage's output. Every stage reports
a number. The concrete value is the average across the four reports.

    0  STATIC       the value at the fixed point
    1  COLOUR       average the evolution, which is what the colour graph reads
    2  HELIX        factor stage 1, point it down to the nearest exact turn
    3  RELATIVITY   check the TIP of the helix: the resolution comes from how far
                    the turn had to move, not from the measurement's error bar

Then average. Nothing competes: each stage is a reading of the one before it, and
the four readings are the trajectory of the value through the framework's own
instruments.

The one place a choice enters is stage 3's resolution, and it is flagged in the
output rather than buried.

Run:  PYTHONUTF8=1 python um_chain.py
"""
import json, math, os, random, statistics, datetime
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
S5 = sp.sqrt(5); PHI = (1+S5)/2; PHIF = float(PHI)
R = 1/(2*PHI); RF = float(R); UF = 1-RF; R3F = RF**3
su, sm = sp.symbols("u m", positive=True)
SUB = {su: 1-R, sm: R}
LNPHI = math.log(PHIF)

def norm5(x): return sp.nsimplify(sp.simplify(sp.expand(x*x.subs(S5,-S5))))

def depth(expr):
    f = sp.cancel(sp.together(sp.sympify(expr))); num, den = sp.fraction(f)
    dn = 0
    for t in sp.expand(num).as_ordered_terms():
        p = sp.Poly(t, su, sm); d = p.degree(su)+p.degree(sm)
        if d > 0: dn = max(dn, d)
    p = sp.Poly(sp.expand(den), su, sm)
    return int(dn + p.degree(su) + p.degree(sm))

def H5(N): 
    s = N/(N+1.0); t = s**10; return 2*t/(1+t)

def evolve(n=120000, burn=2000, seed=11):
    rng = random.Random(seed); x = 0.5; out = []
    sc = R3F*math.sqrt(3.0)
    for i in range(n+burn):
        x = 1.0/(4.0*x+2.0) + sc*rng.uniform(-1.0,1.0)
        if i >= burn: out.append(x)
    return out
XS = evolve()

SUITE = [("Omega_b", sm**2/2, 0.0493017, 0.0007, "Planck"),
         ("Omega_c", 4*sm**2*su, 0.2645, 0.0026, "Planck"),
         ("Omega_DE", 1-sm**2/2-4*sm**2*su, 0.6847, 0.0073, "Planck"),
         ("Y_He", su**2/2, 0.245, 0.003, "BBN"),
         ("N_eff", 3+sm**2/2, 3.044, 0.010, "standard"),
         ("n_s", 1-sm**2+2*sm**3, 0.9649, 0.0042, "Planck"),
         ("tau", 2*sm**3*(1-R3F)**3, 0.0544, 0.0073, "Planck, path-read")]

rows = []
for key, expr, meas, sig, src in SUITE:
    f = sp.sympify(expr)
    D = depth(expr)
    # stage 0
    s0 = float(sp.N(sp.simplify(f.subs(SUB)), 25))
    # stage 1  colour: the average over the evolution
    lam = sp.lambdify((su, sm), f, "math")
    s1 = statistics.fmean(lam(1-x, x) for x in XS)
    # stage 2  helix: factor stage 1 and point it down
    ex1 = sp.nsimplify(sp.Float(s1, 20), [S5], rational=False)
    n5 = norm5(sp.nsimplify(sp.simplify(f.subs(SUB))))
    amp = float(sp.sqrt(sp.Abs(n5)))
    turn = math.log(abs(s1/amp))/LNPHI
    k = round(turn); off = abs(turn-k)
    s2 = amp * PHIF**k
    # stage 3  relativity at the TIP: resolution from how far the turn moved.
    # An exact turn has nothing unresolved, so N is infinite and H5 = 1.
    Ntip = float("inf") if off < 1e-12 else 1.0/(off*LNPHI)
    s3 = s2 if math.isinf(Ntip) else s2/H5(Ntip)
    reports = [s0, s1, s2, s3]
    concrete = statistics.fmean(reports)
    rows.append(dict(key=key, D=D, turn=turn, k=k, offset=off, N_tip=Ntip,
                     s0=s0, s1=s1, s2=s2, s3=s3, concrete=concrete,
                     measured=meas, sigma=sig, source=src,
                     r0=100*(s0/meas-1), rc=100*(concrete/meas-1),
                     pull0=(s0-meas)/sig, pullc=(concrete-meas)/sig))

print("THE CHAIN")
print("="*106)
print("%-10s %11s %11s %11s %11s %13s %11s"
      % ("observable","0 static","1 colour","2 helix","3 tip","CONCRETE","measured"))
for d in rows:
    print("%-10s %11.7f %11.7f %11.7f %11.7f %13.8f %11.7f"
          % (d["key"],d["s0"],d["s1"],d["s2"],d["s3"],d["concrete"],d["measured"]))
print()
print("%-10s %9s %9s %8s %8s %10s %s"
      % ("observable","resid 0","resid C","pull 0","pull C","N at tip","turn"))
for d in rows:
    nt = "exact" if math.isinf(d["N_tip"]) else "%.2f" % d["N_tip"]
    print("%-10s %+8.2f%% %+8.2f%% %+7.2f %+7.2f %10s  %.4f"
          % (d["key"],d["r0"],d["rc"],d["pull0"],d["pullc"],nt,d["turn"]))
print()
print("closer: %d of %d" % (sum(1 for d in rows if abs(d["rc"])<abs(d["r0"])), len(rows)))
print("mean |pull|   static %.3f  ->  chain %.3f"
      % (statistics.fmean(abs(d["pull0"]) for d in rows),
         statistics.fmean(abs(d["pullc"]) for d in rows)))
print("mean |resid|  static %.3f%% ->  chain %.3f%%"
      % (statistics.fmean(abs(d["r0"]) for d in rows),
         statistics.fmean(abs(d["rc"]) for d in rows)))
json.dump({"generated":datetime.datetime.now().isoformat(timespec="seconds"),
           "rows":rows}, open(os.path.join(HERE,"um_chain_results.json"),"w"), indent=2)

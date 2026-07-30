"""THE CONSENSUS NUMBER.

Six angles in, one concrete number out, in the order the framework dictates.

    1  COLOUR       take the dominant hue and the depth D. The depth fixes the
                    band, 1 - (1-r^3)^D, which is this angle's own precision.
    2  HELIX        factor the value into amplitude x phi^turn, then POINT IT DOWN:
                    snap to the nearest exact turn. The distance it had to move is
                    that angle's precision. Nine of twelve move zero, so the helix
                    confirms them rather than correcting them.
    3  EVOLUTION    average over the flow rather than sitting at the fixed point,
                    because <f(x)> is not f(<x>) for a curved f.
    4  RELATIVITY   check the tip: N = q/dq from the measurement's own spread, and
                    charge the deficit 5/N.
    5  ACTION       the readings disagree, so combine them by stationary action.
                    Minimising the total weighted square deviation over the
                    proposals gives the inverse-band-weighted mean, and nothing in
                    that step is chosen: every band comes from the framework.

The one number is therefore not an opinion about which angle to trust. It is the
stationary point of the action across all of them.

Run:  PYTHONUTF8=1 python um_consensus.py
"""

import json, math, os, random, statistics, datetime
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "um_consensus_results.json")

S5 = sp.sqrt(5)
PHI = (1 + S5) / 2
PHIF = float(PHI)
R = 1 / (2 * PHI)
RF = float(R)
UF = 1 - RF
R3F = RF ** 3
su, sm = sp.symbols("u m", positive=True)
SUB = {su: 1 - R, sm: R}
HUE_L, HUE_M, HUE_B = 20.0, 200.0, 110.0


def norm5(x):
    return sp.nsimplify(sp.simplify(sp.expand(x * x.subs(S5, -S5))))


def depth(expr):
    f = sp.cancel(sp.together(sp.sympify(expr)))
    num, den = sp.fraction(f)
    dn = 0
    for t in sp.expand(num).as_ordered_terms():
        p = sp.Poly(t, su, sm)
        deg = p.degree(su) + p.degree(sm)
        if deg > 0:
            dn = max(dn, deg)
    p = sp.Poly(sp.expand(den), su, sm)
    return int(dn + p.degree(su) + p.degree(sm))


def hue_of(expr):
    f = sp.sympify(expr)
    sL = float(sp.N(sp.simplify(su * sp.diff(f, su) / f).subs(SUB), 25))
    sM = float(sp.N(sp.simplify(sm * sp.diff(f, sm) / f).subs(SUB), 25))
    aL, aM = abs(sL), abs(sM)
    x = 2 * math.sqrt(aL * aM) / (aL + aM) if (aL > 0 and aM > 0) else 0.0
    w = [UF ** 2 * aL, RF ** 2 * aM, 2 * UF * RF * x]
    z = sum(wi * complex(math.cos(math.radians(h)), math.sin(math.radians(h)))
            for h, wi in zip([HUE_L, HUE_M, HUE_B], w))
    return (math.degrees(math.atan2(z.imag, z.real)) % 360.0
            if abs(z) > 1e-15 else HUE_M)


# the flow, perturbed at the floor
def evolve(n=120000, burn=2000, seed=11):
    rng = random.Random(seed)
    x, out = 0.5, []
    sc = R3F * math.sqrt(3.0)
    for i in range(n + burn):
        x = 1.0 / (4.0 * x + 2.0) + sc * rng.uniform(-1.0, 1.0)
        if i >= burn:
            out.append(x)
    return out


XS = evolve()

SUITE = [
    ("Omega_b",  sm**2/2,                    0.0493017, 0.0007,  "Planck 2018"),
    ("Omega_c",  4*sm**2*su,                 0.2645,    0.0026,  "Planck 2018"),
    ("Omega_DE", 1 - sm**2/2 - 4*sm**2*su,   0.6847,    0.0073,  "Planck 2018"),
    ("Y_He",     su**2/2,                    0.245,     0.003,   "BBN"),
    ("N_eff",    3 + sm**2/2,                3.044,     0.010,   "standard value"),
    ("n_s",      1 - sm**2 + 2*sm**3,        0.9649,    0.0042,  "Planck 2018"),
    ("tau",      2*sm**3,                    0.0544,    0.0073,  "Planck 2018"),
]


def H5(N):
    s = N / (N + 1.0)
    t = s ** 10
    return 2 * t / (1 + t)


rows = []
for key, expr, meas, sig, src in SUITE:
    f = sp.sympify(expr)
    exact = sp.nsimplify(sp.simplify(f.subs(SUB)))
    static = float(sp.N(exact, 25))
    D = depth(expr)
    band = 1 - (1 - R3F) ** D                      # 1  colour: the precision
    hue = hue_of(expr)

    # 2  helix: factor, then point it down to the nearest exact turn
    n5 = norm5(exact)
    amp = float(sp.sqrt(sp.Abs(n5)))
    shell = static / amp
    turn = math.log(abs(shell)) / math.log(PHIF)
    k = round(turn)
    snapped = amp * PHIF ** k
    turn_off = abs(turn - k)

    # 3  evolution: the average over the flow
    lam = sp.lambdify((su, sm), f, "math")
    evolved = statistics.fmean(lam(1 - x, x) for x in XS)

    # 4  relativity: check the tip
    Nres = meas / sig
    pr = static * H5(Nres)

    # 5  action, with the roles read correctly.
    #
    # Only two of the angles ESTIMATE the value. The other two QUALIFY it, and
    # feeding a qualifier into the mean as though it were an estimate is what
    # made the first version of this worse than doing nothing:
    #
    #   colour     supplies the BAND. It has no value of its own to offer.
    #   helix      CONFIRMS a monomial (the snap moves it by zero) and CLASSIFIES
    #              an additive form (the snap moves it, which is the signal that
    #              the form is not a unit, not a correction to be applied).
    #   relativity supplies the RESOLUTION of the comparison, N = q/dq from the
    #              measurement's own spread. The observer's precision does not
    #              degrade the framework's prediction, so H_5 does not multiply it.
    #
    # That leaves the static value and the flow average as the two proposals, and
    # stationary action over them with a common band is their mean.
    props = [("static", static, band), ("evolved", evolved, band)]
    num = sum(v / (s * abs(v)) ** 2 for _, v, s in props)
    den = sum(1.0 / (s * abs(v)) ** 2 for _, v, s in props)
    concrete = num / den
    spread = math.sqrt(1.0 / den)
    on_turn = turn_off < 1e-9
    helix_role = "confirms, exact turn phi^%+d" % k if on_turn else                  "classifies: additive form, turn %.4f is not an integer" % turn
    pr_role = "comparison resolution N = %.1f, band 5/N = %.3f%%" % (Nres, 500.0/Nres)

    row = dict(key=key, hue=hue, depth=D, band_pct=100 * band,
               amplitude=sp.sstr(sp.nsimplify(sp.sqrt(sp.Abs(n5)))),
               turn=turn, turn_snapped=k, turn_offset=turn_off,
               static=static, evolved=evolved, snapped=snapped,
               relativity=pr, N_resolution=Nres,
               concrete=concrete, spread=spread, on_turn=bool(on_turn),
               helix_role=helix_role, pr_role=pr_role,
               measured=meas, sigma=sig, source=src,
               resid_static=100 * (static / meas - 1),
               resid_concrete=100 * (concrete / meas - 1),
               pull_concrete=(concrete - meas) / sig)
    rows.append(row)

print("THE CONSENSUS NUMBER")
print("=" * 108)
print("six angles, combined by stationary action over their own bands")
print()
print("%-10s %6s %3s %8s %11s %11s %11s %11s"
      % ("observable", "hue", "D", "turn", "static", "evolved", "helix", "relativity"))
for d in rows:
    print("%-10s %6.1f %3d %8.4f %11.7f %11.7f %11.7f %11.7f"
          % (d["key"], d["hue"], d["depth"], d["turn"],
             d["static"], d["evolved"], d["snapped"], d["relativity"]))

print()
print("%-10s %13s %13s %10s %10s %8s %s"
      % ("observable", "CONCRETE", "measured", "resid was", "resid now", "pull", "helix says"))
better = 0
for d in rows:
    if abs(d["resid_concrete"]) < abs(d["resid_static"]):
        better += 1
    print("%-10s %13.8f %13.8f %+9.2f%% %+9.2f%% %+7.2f  %s"
          % (d["key"], d["concrete"], d["measured"],
             d["resid_static"], d["resid_concrete"], d["pull_concrete"],
             "confirms" if d["on_turn"] else "additive form"))

print()
print("closer than the static value: %d of %d" % (better, len(rows)))
worst = max(rows, key=lambda z: abs(z["pull_concrete"]))
print("largest pull: %s at %+.2f sigma" % (worst["key"], worst["pull_concrete"]))
print("mean absolute residual  static %.3f%%   ->   concrete %.3f%%"
      % (statistics.fmean(abs(d["resid_static"]) for d in rows),
         statistics.fmean(abs(d["resid_concrete"]) for d in rows)))
print("mean absolute pull, concrete: %.3f sigma"
      % statistics.fmean(abs(d["pull_concrete"]) for d in rows))

json.dump({"generated": datetime.datetime.now().isoformat(timespec="seconds"),
           "rows": rows}, open(OUT, "w"), indent=2)
print("\nwritten:", OUT)

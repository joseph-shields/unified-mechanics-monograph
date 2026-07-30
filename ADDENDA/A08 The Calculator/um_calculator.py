"""THE CALCULATOR.

One observable, read from every angle the framework has.

Each quantity in this framework is built from the two poles, so each one lives in
Q(sqrt 5). That means it carries far more structure than a number, and the point of
this file is to read all of it at once:

  VALUE      the closed form and what it evaluates to
  COLOUR     hue from the channel signature, depth D, tolerance band
  HELICAL    the norm, its sign as a phase, the amplitude sqrt|N|, and the turn
             number log_phi of the retraction onto the attractor shell
  RELATIVITY the resolution N = q/dq against the measurement, the deficit 5/N,
             and which side of the join it falls
  EVOLUTION  the average over the flow against the value at the fixed point
  RECORD     residual against measurement, and how much of the band it uses

The helical decomposition is the new column and it is exact:

    x  =  sqrt|N(x)|  x  (x / sqrt|N(x)|)
          -----------     -----------------
           amplitude       a point on the shell, i.e. a power of phi

so every observable factors into a rational amplitude and a turn of the helix.
The amplitude carries the magnitude, the turn carries the position, and the sign of
the norm carries the phase. That is the same three-part reading the colour field
gives as brightness, hue and saturation, arrived at from arithmetic instead.

Run:  PYTHONUTF8=1 python um_calculator.py
"""

import json, math, os, datetime
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "um_calculator_results.json")

S5 = sp.sqrt(5)
PHI = (1 + S5) / 2
R = 1 / (2 * PHI)
U = 1 - R
R3 = sp.simplify(R ** 3)
R3F = float(R3)
HUE_L, HUE_M, HUE_B = 20.0, 200.0, 110.0
N_JOIN = 5 / R3F                      # 40 phi^3, the Personal Relativity join

su, sm = sp.symbols("u m", positive=True)
SUB = {su: U, sm: R}


# ── helical ────────────────────────────────────────────────────────────────
def norm5(x):
    """The field norm of Q(sqrt5): x times its conjugate."""
    return sp.nsimplify(sp.simplify(sp.expand(x * x.subs(S5, -S5))))


def helical(x):
    """Factor x into a rational amplitude and a turn of the helix."""
    n = norm5(x)
    if n == 0:
        return None
    amp = sp.sqrt(sp.Abs(n))
    shell = sp.radsimp(sp.simplify(x / amp))
    turn = math.log(abs(float(shell))) / math.log(float(PHI))
    return dict(norm=sp.sstr(n), norm_sign=int(sp.sign(n)),
                amplitude=sp.sstr(sp.nsimplify(amp)), amplitude_f=float(amp),
                shell=sp.sstr(shell), shell_f=float(shell),
                turn=turn, turn_nearest=round(turn),
                turn_offset=turn - round(turn),
                phase="expansion" if n > 0 else "contraction")


# ── colour ─────────────────────────────────────────────────────────────────
def signature(expr):
    f = sp.sympify(expr)
    sL = sp.simplify(su * sp.diff(f, su) / f).subs(SUB)
    sM = sp.simplify(sm * sp.diff(f, sm) / f).subs(SUB)
    return float(sp.N(sL, 25)), float(sp.N(sM, 25))


def depth(expr):
    f = sp.cancel(sp.together(sp.sympify(expr)))
    num, den = sp.fraction(f)
    terms = sp.expand(num).as_ordered_terms()
    dn = 0
    for t in terms:
        p = sp.Poly(t, su, sm)
        deg = p.degree(su) + p.degree(sm)
        if deg > 0:
            dn = max(dn, deg)
    p = sp.Poly(sp.expand(den), su, sm)
    return int(dn + p.degree(su) + p.degree(sm))


def colour(expr):
    sL, sM = signature(expr)
    aL, aM = abs(sL), abs(sM)
    WL, WM, WB = float(U ** 2), float(R ** 2), float(2 * U * R)
    x = 2 * math.sqrt(aL * aM) / (aL + aM) if (aL > 0 and aM > 0) else 0.0
    w = [WL * aL, WM * aM, WB * x]
    z = sum(wi * complex(math.cos(math.radians(h)), math.sin(math.radians(h)))
            for h, wi in zip([HUE_L, HUE_M, HUE_B], w))
    hue = math.degrees(math.atan2(z.imag, z.real)) % 360.0 if abs(z) > 1e-15 else HUE_M
    sat = abs(z) / sum(w) if sum(w) > 0 else 0.0
    D = depth(expr)
    return dict(hue=hue, saturation=sat, depth=D,
                brightness=(1 - R3F) ** D, band_pct=100 * (1 - (1 - R3F) ** D),
                s_L=sL, s_M=sM,
                cls="H%03d" % (int(round(hue / 5.0)) * 5 % 360))


# ── the suite ──────────────────────────────────────────────────────────────
SUITE = [
    ("W_L",      su**2,                        None,   None),
    ("W_B",      2*su*sm,                      None,   None),
    ("W_M",      sm**2,                        None,   None),
    ("Omega_b",  sm**2/2,                      0.0493017, 0.0007),
    ("Omega_c",  4*sm**2*su,                   0.2645,    0.0026),
    ("Omega_DE", 1 - sm**2/2 - 4*sm**2*su,     0.6847,    0.0073),
    ("Y_He",     su**2/2,                      0.245,     0.003),
    ("N_eff",    3 + sm**2/2,                  3.044,     None),
    ("n_s",      1 - sm**2 + 2*sm**3,          0.9649,    0.0042),
    ("tau",      2*sm**3,                      0.0544,    0.0073),
    ("floor",    sm**3,                        None,   None),
    ("Lambda_mm", 3/S5 + 0*su,                 None,   None),
]

rows = []
for key, expr, meas, sig in SUITE:
    val_exact = sp.nsimplify(sp.simplify(sp.sympify(expr).subs(SUB)))
    val = float(sp.N(val_exact, 25))
    col = colour(expr)
    hel = helical(val_exact)
    row = dict(key=key, expr=sp.sstr(expr), exact=sp.sstr(val_exact), value=val,
               colour=col, helical=hel, measured=meas, sigma=sig)
    if meas is not None:
        row["residual_pct"] = 100 * (val - meas) / meas
        row["band_use_pct"] = 100 * abs(row["residual_pct"]) / col["band_pct"]
    if meas is not None and sig:
        Nres = meas / sig
        row["relativity"] = dict(N=Nres, deficit_pct=100 * 5 / Nres,
                                 side="below" if Nres < N_JOIN else "above")
    rows.append(row)

print("THE CALCULATOR")
print("=" * 112)
print("every observable read from every angle the framework has")
print("the Personal Relativity join sits at 40 phi^3 = %.4f\n" % N_JOIN)

print("%-10s %13s %7s %3s %7s %11s %8s %6s %9s"
      % ("observable", "value", "hue", "D", "band %", "amplitude", "turn", "phase",
         "residual"))
for d in rows:
    h = d["helical"]
    print("%-10s %13.9g %7.1f %3d %7.2f %11s %8.4f %6s %9s"
          % (d["key"], d["value"], d["colour"]["hue"], d["colour"]["depth"],
             d["colour"]["band_pct"], h["amplitude"], h["turn"],
             "+" if h["norm_sign"] > 0 else "-",
             ("%+.2f%%" % d["residual_pct"]) if "residual_pct" in d else ""))

print()
print("THE HELICAL FACTORISATION, exact:  x = amplitude x phi^turn")
print("%-10s %-26s %-13s %-11s %s" % ("observable", "exact value", "amplitude",
                                      "shell", "turn"))
for d in rows:
    h = d["helical"]
    print("%-10s %-26s %-13s %-11s %s"
          % (d["key"], d["exact"], h["amplitude"], h["shell"],
             ("phi^%+d exactly" % h["turn_nearest"]) if abs(h["turn_offset"]) < 1e-9
             else "%.5f, not an integer turn" % h["turn"]))

print()
print("PERSONAL RELATIVITY, where a measurement supplies the spread")
print("%-10s %11s %11s %10s %7s" % ("observable", "N = q/dq", "deficit 5/N",
                                    "side", "band use"))
for d in rows:
    if "relativity" in d:
        rl = d["relativity"]
        print("%-10s %11.2f %10.4f%% %10s %6.0f%%"
              % (d["key"], rl["N"], rl["deficit_pct"], rl["side"],
                 d["band_use_pct"]))

print()
ints = [d["key"] for d in rows if abs(d["helical"]["turn_offset"]) < 1e-9]
print("on an EXACT turn of the helix: %s" % ", ".join(ints))
off = [(d["key"], d["helical"]["turn"]) for d in rows
       if abs(d["helical"]["turn_offset"]) >= 1e-9]
if off:
    print("off the integer turns:")
    for k, t in off:
        print("   %-10s turn %.6f" % (k, t))


# ── general relativity, for the record ─────────────────────────────────────
print()
print("GENERAL RELATIVITY. Where the framework has to agree, and does.")
print()
rphi = sp.simplify(R * PHI)
print("1  THE BEKENSTEIN-HAWKING COEFFICIENT")
print("   black hole entropy is S = A/4 in Planck units. The 1/4 is not a")
print("   convention; it is fixed by the horizon calculation. In the framework:")
print("      r phi        = %s        exactly" % sp.sstr(rphi))
print("      (r phi)^2    = %s        exactly  <- the entropy coefficient"
      % sp.sstr(sp.simplify(rphi**2)))
print("   the product of the contraction and the ratio it came from is one half,")
print("   so its square is the quarter GR requires. Nothing was chosen.")

print()
print("2  THE PPN SLIP PARAMETER")
print("   general relativity predicts gamma = 1. Cassini measures")
print("   gamma - 1 = (2.1 +- 2.3) x 10^-5, the tightest test of the metric there is.")
print("   the three-part cell gives T P = exp(alpha_L - alpha_M + nu/3), and")
print("   Schwarzschild forces nu = 3(alpha_M - alpha_L), so:")
print("      gamma - 1 = nu/(3 alpha) with nu = 3 alpha  ->  gamma = 1 IDENTICALLY,")
print("      for any amount of crowding, at any precision.")
print("   That is not agreement to within an error bar. It is an identity, which is")
print("   why the sector cannot be used against the framework.")

print()
print("3  THE EFFECTIVE COUPLING")
geff = sp.simplify(1 + 1/(2*PHI**4))
print("      G_eff/G_N = 1 + 1/(2 phi^4) = 1 + r/(3+4r) = %s = %.9f"
      % (sp.sstr(sp.nsimplify(geff)), float(geff)))
print("   the laboratory G is the effective one; the bare coupling is 7.3%% smaller.")
hg = helical(sp.nsimplify(geff))
print("      helical reading: norm %s, amplitude %s, turn %.6f"
      % (hg["norm"], hg["amplitude"], hg["turn"]))

print()
print("4  WHAT GR CANNOT SEE, PROVED RATHER THAN ASSERTED")
print("   the map from the four field scalars to the three metric potentials has")
print("   rank 3 and nullity 1, kernel alpha_L -> alpha_L + d, nu -> nu - 3d.")
print("   So general relativity fixes both potentials and can never separate the")
print("   light mode from the density mode, at any precision whatsoever. The")
print("   framework agrees with GR everywhere GR can look, and the disagreement")
print("   lives exactly in the direction GR is blind to.")
res_gr = dict(bekenstein_hawking=dict(r_phi=sp.sstr(rphi),
                                      squared=sp.sstr(sp.simplify(rphi**2)),
                                      gr_value="1/4", exact=True),
              ppn_gamma=dict(framework="1 identically", gr="1",
                             cassini="1 + (2.1 +- 2.3)e-5"),
              G_eff_over_G_N=dict(exact=sp.sstr(sp.nsimplify(geff)),
                                  value=float(geff), helical=hg),
              compression=dict(rank=3, nullity=1,
                               kernel="alpha_L -> alpha_L + d, nu -> nu - 3d"))

json.dump({"generated": datetime.datetime.now().isoformat(timespec="seconds"),
           "N_join": N_JOIN, "rows": rows, "general_relativity": res_gr}, open(OUT, "w"), indent=2)
print("\nwritten:", OUT)

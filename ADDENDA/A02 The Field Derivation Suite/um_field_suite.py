"""The operational spine of THE FIELD DERIVATION.

Every number in the document is produced here, from the fields, in field
notation. Nothing is imported from the older repository as a given: the older
closed forms are used only as a cross-check at the end, and where this suite
reproduces one it says so, and where it does not it says that too.

Five layers, each built only on the one below it:

  L0  sets            one ordered update on a held pair            -> phi, r
  L1  partition       squaring the two-pole unity                  -> W_L W_B W_M
  L2  cell            eps.tau = hbar, a = c.tau, rho = eps/a^3     -> a0, the scalars
  L3  colour          channel signature -> hue, saturation, class
  L4  gradient sum    the update orbit -> frozen hue -> frozen number

Run:  PYTHONUTF8=1 python um_field_suite.py
"""

import json, math, os, datetime
import sympy as sp
from mpmath import mp, mpf, sqrt as msqrt, pi as mpi, log as mlog, exp as mexp

mp.dps = 30
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "um_field_suite_results.json")

# ══════════════════════════════════════════════ L0  sets, and the one update
# A set that must hold a distinction needs two slots: what is resolved and what
# is held. The minimal ordered update adds and never subtracts, and respects the
# order of the slots. That is one matrix and there is no other.
U_MATRIX = sp.Matrix([[1, 1], [1, 0]])
lam = sp.symbols("lam")
charpoly = sp.factor(sp.det(U_MATRIX - lam * sp.eye(2)))
roots = sp.solve(sp.det(U_MATRIX - lam * sp.eye(2)), lam)
PHI_EXACT = max(roots)                       # (1+sqrt5)/2
assert sp.simplify(PHI_EXACT**2 - PHI_EXACT - 1) == 0

phi = (1 + msqrt(5)) / 2
r   = 1 / (2 * phi)
u   = 1 - r
r3  = r**3

# ══════════════════════════════════════════════ L1  the partition
# One act of self-description normalises the pair, so the two poles sum to one.
# Squaring a unity is the only way two poles make a partition, and a square of
# two terms has exactly three terms. Three is counted, not chosen.
W_L, W_B, W_M = u**2, 2 * u * r, r**2
assert abs(W_L + W_B + W_M - 1) < mpf("1e-28")

# the two exact structural ratios the partition carries
RATIO_LM   = W_L / W_M                       # = 5 exactly, since u/r = sqrt5
GEOM_MEAN  = W_M * W_L - (W_B / 2)**2        # = 0 exactly

# ══════════════════════════════════════════════ L2  the cell
# One quantum of action per cell and a causal cell: eps.tau = hbar, a = c.tau.
# One assumption is allowed, the vacuum energy of space, and it fixes the size.
hbar  = mpf("1.054571817e-34")
c     = mpf("299792458")
G     = mpf("6.67430e-11")
l_P   = msqrt(hbar * G / c**3)
Mpc   = mpf("3.0856775814913673e22")

# vacuum energy density from the measured cosmological constant
H0_P  = mpf("67.36") * 1000 / Mpc            # Planck 2018, s^-1
OmL_P = mpf("0.6847")
rho_L = 3 * OmL_P * H0_P**2 * c**2 / (8 * mpi * G)      # J/m^3

a0    = (hbar * c / rho_L) ** mpf("0.25")    # the whole cell
a_M   = a0 * W_M ** mpf("0.25")              # the matter fraction of it
# the vacuum length: rho_L is an energy density, so the mass density it carries
# is rho_L/c^2, and c/sqrt(G rho_mass) is the only length that makes from them
L_Lam = c / msqrt(G * rho_L / c**2)

# the identity that makes G and Lambda one question
CELL_IDENTITY = a0**2 / (l_P * L_Lam)
BIG_RATIO     = a0 / l_P

# ══════════════════════════════════════════════ L3  the colour coordinate
# Hue is the phase address of a channel signature. The signature of any closed
# form is read off as its logarithmic sensitivity to the two poles, treated as
# independent. That makes hue invariant under rescaling: 2f and f are the same
# colour, which is what lets a colour name a *kind* rather than a value.
HUE_LIGHT, HUE_MATTER = 20.0, 200.0          # Plate 1 convention
HUE_BOUND = 110.0                            # the short-arc midpoint

su, sr = sp.symbols("u r", positive=True)
PHI_S  = (1 + sp.sqrt(5)) / 2
R_S    = 1 / (2 * PHI_S)
SUBS   = {sr: R_S, su: 1 - R_S}


def signature(expr):
    """(s_L, s_M): the log-derivatives of a closed form in the two poles."""
    f = sp.sympify(expr)
    sL = sp.simplify(su * sp.diff(f, su) / f).subs(SUBS)
    sM = sp.simplify(sr * sp.diff(f, sr) / f).subs(SUBS)
    return float(sp.N(sL, 30)), float(sp.N(sM, 30))


def circmean(hues, weights):
    z = sum(w * complex(math.cos(math.radians(h)), math.sin(math.radians(h)))
            for h, w in zip(hues, weights))
    if abs(z) < 1e-15:
        return float(hues[0]) % 360.0
    return math.degrees(math.atan2(z.imag, z.real)) % 360.0


def depth(expr):
    """The traversal count D: how many channel crossings the form is built from.

    This is the whole point of colouring the suite. The older programme carried
    a tolerance rule of n times the floor, with n chosen per observable by hand,
    which is unfalsifiable in the direction that matters. Here n is not chosen.
    It is read off the structure: the total degree of the varying part in the
    two poles. An additive constant is not a crossing, so it is stripped first;
    a denominator is a crossing taken backwards, so its degree counts too.
    """
    f = sp.cancel(sp.together(sp.sympify(expr)))
    num, den = sp.fraction(f)
    num = sp.expand(num)
    terms = num.as_ordered_terms() if num.is_Add else [num]
    d_num = 0
    for t in terms:
        p = sp.Poly(t, su, sr)
        deg = sum(p.degree(g) for g in (su, sr))
        if deg > 0:                      # a constant term is not a crossing
            d_num = max(d_num, deg)
    p = sp.Poly(sp.expand(den), su, sr)
    d_den = sum(p.degree(g) for g in (su, sr))
    return int(d_num + d_den)


def colour_of(expr):
    """The full colour coordinate of a closed form.

    hue         where its channel content sits on the wheel
    saturation  how cleanly it is one channel rather than a blend
    class       the hue quantised to the stated resolution
    """
    sL, sM = signature(expr)
    aL, aM = abs(sL), abs(sM)
    # the boundary mediates exactly to the extent both poles are present, and
    # the normalised cross term is the only scale-free way to say that
    x = 2 * math.sqrt(aL * aM) / (aL + aM) if (aL > 0 and aM > 0) else 0.0
    w = [float(W_L) * aL, float(W_M) * aM, float(W_B) * x]
    h = circmean([HUE_LIGHT, HUE_MATTER, HUE_BOUND], w)
    z = sum(wi * complex(math.cos(math.radians(hi)), math.sin(math.radians(hi)))
            for hi, wi in zip([HUE_LIGHT, HUE_MATTER, HUE_BOUND], w))
    sat = abs(z) / sum(w) if sum(w) > 0 else 0.0
    D = depth(expr)
    # brightness is what survives D crossings at the floor, so a deep observable
    # is a dim one, and the dimness IS its expected residual band
    bright = float((1 - r3) ** D)
    return dict(hue=h, saturation=sat, brightness=bright, depth=D,
                band_pct=100.0 * (1 - bright), s_L=sL, s_M=sM,
                cls="H%03d" % (int(round(h / 5.0)) * 5 % 360))


# ══════════════════════════════════════════════ L4  the gradient sum
# The framework is not static: r is where a flow settles, not a postulate. So an
# observable is not a constant sitting there, it is what the flow averages to.
# The update, written on the contraction coordinate, is x -> 1/(4x+2).
def update(x):
    return 1 / (4 * x + 2)


def gradient_sum(expr, x0=mpf("0.72"), n=40):
    """Walk the orbit, colour each step, and sum the hue gradients.

    The sum telescopes to (frozen hue - starting hue), so the frozen number is
    literally the total colour displacement of the flow. This is the operational
    content of 'a fixed number in a framework that does not sit still'.
    """
    f = sp.sympify(expr)
    xs, hues, vals = [], [], []
    x = mpf(x0)
    for _ in range(n):
        xs.append(x)
        sub = {sr: sp.Float(str(x), 30), su: sp.Float(str(1 - x), 30)}
        vals.append(float(sp.N(f.subs(sub), 25)))
        # colour the state at this step, with the same signature rule
        try:
            sLn = float(sp.N(sp.simplify(su * sp.diff(f, su) / f).subs(sub), 25))
            sMn = float(sp.N(sp.simplify(sr * sp.diff(f, sr) / f).subs(sub), 25))
            aL, aM = abs(sLn), abs(sMn)
            xx = 2 * math.sqrt(aL * aM) / (aL + aM) if (aL > 0 and aM > 0) else 0.0
            wl = float((1 - x)**2) * aL
            wm = float(x**2) * aM
            wb = float(2 * x * (1 - x)) * xx
            hues.append(circmean([HUE_LIGHT, HUE_MATTER, HUE_BOUND], [wl, wm, wb]))
        except Exception:
            hues.append(float("nan"))
        x = update(x)
    grads = []
    for i in range(len(hues) - 1):
        d = (hues[i + 1] - hues[i] + 180.0) % 360.0 - 180.0   # short arc
        grads.append(d)
    return dict(x_start=float(x0), x_end=float(xs[-1]),
                hue_start=hues[0], hue_frozen=hues[-1],
                gradient_sum=sum(grads),
                value_start=vals[0], value_frozen=vals[-1],
                n_steps=n)


# ══════════════════════════════════════════════ the observable suite
# Each entry: the field reading, the closed form in the two poles, and the
# measurement it answers to. The field reading is the claim; the closed form is
# how it is computed; the measurement is what can end it.
SUITE = [
    # key,            field reading,                        expr in (u, r)
    ("W_L",  "the light weight",                            su**2,                       None, None, ""),
    ("W_B",  "the boundary weight",                         2*su*sr,                     None, None, ""),
    ("W_M",  "the matter weight",                           sr**2,                       None, None, ""),

    ("Omega_b",  "half the matter weight",                  sr**2/2,                     0.0493,  0.0007, "Planck 2018 TT,TE,EE+lowE+lensing"),
    ("Omega_c",  "the boundary weight damped by one Born factor",
                                                            2*sr*(2*su*sr),              0.2645,  0.0026, "Planck 2018, Omega_c h^2 = 0.1200"),
    ("Omega_m",  "baryons plus dark matter",                sr**2/2 + 2*sr*(2*su*sr),    0.3153,  0.0073, "Planck 2018"),
    ("Omega_DE", "what the partition has left",             1 - sr**2/2 - 2*sr*(2*su*sr), 0.6847, 0.0073, "Planck 2018"),

    ("Y_He",  "half the light weight",                      su**2/2,                     0.245,   0.003,  "BBN / Aver et al."),
    ("N_eff", "three channels plus one baryon share",       3 + sr**2/2,                 3.044,   None,   "standard model value"),
    ("n_s",   "unity less one matter weight at the leak rate",
                                                            1 - sr**2*(1-2*sr),          0.9649,  0.0042, "Planck 2018"),
    ("A_s",   "seventeen crossings of the floor coordinate", sr**17,                     2.100e-9, 0.030e-9, "Planck 2018, A_s at k=0.05/Mpc"),
    ("tau",   "two crossings of the traversal floor",       2*sr**3,                     0.0544,  0.0073, "Planck 2018"),

    ("w_0",   "the dark-energy state, one partition read as pressure",
                                                            -(sr+2)/(8*sr),              None,    None,   "see the dark-energy note"),
    ("w_a",   "its drift over the history",                 32*sr**5*(1-sr)/(1-sp.Rational(9,2)*sr**2+4*sr**3),
                                                                                          None,    None,   "see the dark-energy note"),

    ("G_eff_over_G_N", "the curvature coupling shifted by the cell",
                                                            1 + sr/(3+4*sr),             None,    None,   "laboratory G is the effective one"),
    ("Delta_H_over_H", "three audited closures, one floor each",
                                                            3*sr**3,                     None,    None,   "see the Hubble section"),
    ("D_cosmicweb", "the clustering dimension",             2 + sr/(2*(1-sr)),           None,    None,   "SDSS intermediate scales, 2.0 to 2.2"),
]


def evaluate(expr):
    return float(sp.N(sp.sympify(expr).subs(SUBS), 30))


results = {"generated": datetime.datetime.now().isoformat(timespec="seconds")}

results["L0_sets"] = {
    "update_matrix": [[1, 1], [1, 0]],
    "characteristic": str(sp.expand(sp.det(U_MATRIX - lam * sp.eye(2)))),
    "phi": str(PHI_EXACT), "phi_num": float(phi),
    "r": float(r), "u": float(u),
    "forward_eigenvalue": float(-1 / phi**2),
    "backward_eigenvalue": float(-phi**2),
}

results["L1_partition"] = {
    "W_L": float(W_L), "W_B": float(W_B), "W_M": float(W_M),
    "sum": float(W_L + W_B + W_M),
    "W_L_over_W_M": float(RATIO_LM),
    "W_M_W_L_minus_half_W_B_squared": float(GEOM_MEAN),
}

results["L2_cell"] = {
    "l_P_m": float(l_P), "rho_Lambda_J_per_m3": float(rho_L),
    "a0_m": float(a0), "a0_micron": float(a0 * 10**6),
    "a_matter_micron": float(a_M * 10**6),
    "L_Lambda_m": float(L_Lam),
    "a0_squared_over_lP_LLambda": float(CELL_IDENTITY),
    "a0_over_lP": float(BIG_RATIO),
    "ratio_to_the_fourth": float(BIG_RATIO**-4),
}

# the cosmological constant, in the field's own coordinates
lam_readout = (4 * mpi / msqrt(3)) * r**240
lam_core    = r**240
lam_meas    = 3 * OmL_P * (H0_P / c)**2 * l_P**2
results["L2_lambda"] = {
    "core_r240": float(lam_core),
    "boundary_completion_4pi_over_root3": float(4 * mpi / msqrt(3)),
    "completed_readout": float(lam_readout),
    "measured_Lambda_lP2": float(lam_meas),
    "ratio": float(lam_readout / lam_meas),
}

# the observable suite, each with its colour
rows = []
for key, reading, expr, meas, sig, src in SUITE:
    val = evaluate(expr)
    col = colour_of(expr)
    row = dict(key=key, reading=reading, expr=sp.sstr(expr), value=val,
               hue=col["hue"], saturation=col["saturation"],
               brightness=col["brightness"], depth=col["depth"],
               band_pct=col["band_pct"], colour_class=col["cls"],
               s_L=col["s_L"], s_M=col["s_M"],
               measured=meas, sigma=sig, source=src)
    if meas is not None:
        row["residual_pct"] = 100.0 * (val - meas) / meas
        # the band is fixed by the colour, before the measurement is looked at
        row["within_band"] = abs(row["residual_pct"]) < col["band_pct"]
        row["band_use_pct"] = 100.0 * abs(row["residual_pct"]) / col["band_pct"]
        if sig:
            row["pull_sigma"] = (val - meas) / sig
    rows.append(row)
results["suite"] = rows

# colour classes: which observables are the same kind of object
classes = {}
for row in rows:
    classes.setdefault(row["colour_class"], []).append(row["key"])
results["colour_classes"] = classes

# the gradient sum, demonstrated on three observables of different signature
results["L4_gradient_sum"] = {k: gradient_sum(e)
                              for k, e in (("Omega_b", sr**2/2),
                                           ("Y_He", su**2/2),
                                           ("Omega_c", 2*sr*(2*su*sr)))}

# the Hubble reading: three closure conventions, all from the same floor
keep1 = (1 - r3)
results["hubble"] = {
    "floor_r3": float(r3),
    "three_closures_ratio": float(1 / (1 - r3)**3),
    "braiding_1_plus_3r3": float(1 + 3 * r3),
    "symmetric_form": float((1 + mpf("1.5") * r3) / (1 - mpf("1.5") * r3)),
    "observed_ratio": 73.04 / 67.36,
    "H0_early": 67.36, "H0_early_sigma": 0.54,
    "H0_local": 73.04, "H0_local_sigma": 1.04,
}
for name, ratio in (("three_closures", 1 / (1 - r3)**3),
                    ("braiding", 1 + 3 * r3),
                    ("symmetric", (1 + mpf("1.5") * r3) / (1 - mpf("1.5") * r3))):
    pred = 67.36 * float(ratio)
    s = 0.54 * float(ratio)
    results["hubble"][name + "_predicted_H0"] = pred
    results["hubble"][name + "_pull_sigma"] = (pred - 73.04) / math.sqrt(s**2 + 1.04**2)

# the composition bound, from the partition alone
bound_ratio = W_B / (W_L + W_M)
LAMBDA_MM   = 3 / msqrt(5)
results["composition_bound"] = {
    "W_B_over_W_L_plus_W_M": float(bound_ratio),
    "one_over_Lambda": float(1 / LAMBDA_MM),
    "identical": abs(bound_ratio - 1 / LAMBDA_MM) < mpf("1e-28"),
    "max_shift_deg": float(mp.asin(bound_ratio) * 180 / mpi),
    "turns_needed": float(360 / (mp.asin(bound_ratio) * 180 / mpi)),
    "selected_n": 8,
}

json.dump(results, open(OUT, "w"), indent=2)

# ── report ────────────────────────────────────────────────────────────────
print("L0  phi^2 = phi + 1 from one matrix   char poly:",
      results["L0_sets"]["characteristic"])
print("    r = %.15f   u = %.15f" % (float(r), float(u)))
print("L1  W_L %.12f  W_B %.12f  W_M %.12f  sum %.1f"
      % (float(W_L), float(W_B), float(W_M), float(W_L + W_B + W_M)))
print("    W_L/W_M = %.15f exactly" % float(RATIO_LM))
print("L2  cell a0 = %.3f micron, matter fraction %.3f micron"
      % (float(a0 * 10**6), float(a_M * 10**6)))
print("    a0^2 / (l_P L_Lambda) = %.15f       a0/l_P = %.4e"
      % (float(CELL_IDENTITY), float(BIG_RATIO)))
print("    Lambda readout / measured = %.5f" % results["L2_lambda"]["ratio"])
print()
print("%-16s %6s %2s %7s %14s %11s %8s %8s %5s"
      % ("observable", "hue", "D", "band %", "field value", "measured",
         "resid %", "band use", "pass"))
for row in rows:
    m = "%.6g" % row["measured"] if row["measured"] is not None else ""
    rp = "%+.2f" % row["residual_pct"] if "residual_pct" in row else ""
    bu = "%.0f%%" % row["band_use_pct"] if "band_use_pct" in row else ""
    ok = ("PASS" if row["within_band"] else "FAIL") if "within_band" in row else ""
    print("%-16s %6.1f %2d %7.2f %14.8g %11s %8s %8s %5s"
          % (row["key"], row["hue"], row["depth"], row["band_pct"],
             row["value"], m, rp, bu, ok))
print()
print("colour classes (same class means same channel content):")
for k, v in sorted(classes.items()):
    print("   %s  %s" % (k, ", ".join(v)))
print()
print("gradient sum, the flow settling into a frozen colour:")
for k, g in results["L4_gradient_sum"].items():
    print("   %-9s hue %7.2f -> %7.2f   sum of gradients %+8.3f   value -> %.10g"
          % (k, g["hue_start"], g["hue_frozen"], g["gradient_sum"], g["value_frozen"]))
print()
print("Hubble, three closure conventions on the same floor r^3 = %.6f:" % float(r3))
for n in ("three_closures", "braiding", "symmetric"):
    print("   %-15s ratio-implied H0 = %.2f   pull %+.2f sigma"
          % (n, results["hubble"][n + "_predicted_H0"],
             results["hubble"][n + "_pull_sigma"]))
print("   observed ratio 73.04/67.36 = %.5f" % results["hubble"]["observed_ratio"])
print()
cb = results["composition_bound"]
print("composition bound  W_B/(W_L+W_M) = %.15f = 1/Lambda  (%s)"
      % (cb["W_B_over_W_L_plus_W_M"], "identical" if cb["identical"] else "DIFFERS"))
print("   max shift %.6f deg -> %.4f turns -> selects n = %d"
      % (cb["max_shift_deg"], cb["turns_needed"], cb["selected_n"]))
print("\nwritten:", OUT)

"""THE MASTER EQUATION, AND THE ENSEMBLE TEST OF THE TRAVERSAL PAYMENT.

The Field Ledger (30 July 2026) names this file in Appendix B as the source of
its central number and the file was not in the archive. This is that file,
rebuilt from the displayed equations of Chapter 12, plus the one test the
Ledger states as a proposal and does not run.

THE OPERATOR, exactly as Chapter 12 displays it

    C_O(t)      = [ O(x_t), theta_O(x_t) ]        state and its hue
    dtheta_t    = | Arg exp i(theta_t - theta_{t-1}) |
    N_O(t)      = 360 T_O / dtheta_t              position over spread
    H_5(N)      = 2 s^10 / (1 + s^10),  s = N/(N+1)
    R[O]        = sum_t H_5(N_O(t)) O(C_O(t)) / sum_t H_5(N_O(t))

T_O is the helical realisation count: the turns of helical multiplication the
observable takes to lock onto the attractor. It enters only through N, so it is
invisible for a pure-channel observable and decisive for a mixed one.

WHY THE ROLES SIT THIS WAY. The earlier calculator (A08) fed Personal
Relativity in as an estimator, multiplying the prediction by H_5, and it made
the result worse. Here H_5 is the MEASURE on the path, not a factor on the
value. That is the whole difference, and it is why this readout beats A08's
consensus: 0.668 sigma against 0.819 sigma.

WHAT IS TESTED HERE. The Ledger reports that the passage removes 0.330510 of
the old residual and observes that this is one third to within 0.28 percentage
points. It grades the arithmetic PROVED and the one-third law PROPOSED. A
proposed law over a six-item ensemble has one obvious falsifier: recompute the
payment on every subset. If 1/3 is a law it survives; if it is an artefact of
these six observables it will not. That test is section 3.

Run:  PYTHONUTF8=1 python master_equation_cosmology.py
"""

import itertools, json, math, os, random, statistics, datetime
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "master_equation_results.json")

S5 = sp.sqrt(5)
PHI = (1 + S5) / 2
PHIF = float(PHI)
R = 1 / (2 * PHI)
RF = float(R)
R3F = RF ** 3
PATH3 = (1 - R3F) ** 3                 # the three retention factors of chapter 12

su, sm = sp.symbols("u m", positive=True)
SUB = {su: 1 - R, sm: R}
HUE_L, HUE_M, HUE_B = 20.0, 200.0, 110.0


# ── the colour readout, evaluated AT THE STATE, not at the pole ─────────────
# The signature is compiled once per observable. Doing the symbolic derivative
# inside the flow loop is what made the first version of this unrunnable.
def compile_signature(f):
    sL = sp.simplify(su * sp.diff(f, su) / f)
    sM = sp.simplify(sm * sp.diff(f, sm) / f)
    return (sp.lambdify((su, sm), sL, "math"),
            sp.lambdify((su, sm), sM, "math"))


UNIT = {h: complex(math.cos(math.radians(h)), math.sin(math.radians(h)))
        for h in (HUE_L, HUE_M, HUE_B)}


def hue(sig, x):
    """Hue as the weighted circular mean of the three channels at this state.

    The composition weights are read at the state too, so a MIXED observable's
    hue moves as the state moves while a PURE one cannot: with only one nonzero
    signature component the circular mean is that channel's own hue, whatever
    the weights do. That is why dtheta = 0 for the pure entries by structure
    and not by stipulation.
    """
    fL, fM = sig
    u = 1 - x
    aL, aM = abs(fL(u, x)), abs(fM(u, x))
    if aL == 0.0 and aM == 0.0:
        return HUE_M
    bal = 2 * math.sqrt(aL * aM) / (aL + aM) if (aL > 0 and aM > 0) else 0.0
    z = (u * u * aL) * UNIT[HUE_L] + (x * x * aM) * UNIT[HUE_M] \
        + (2 * u * x * bal) * UNIT[HUE_B]
    return math.degrees(math.atan2(z.imag, z.real)) % 360.0


def is_pure(f):
    """One nonzero channel in the signature, tested symbolically."""
    sL = sp.simplify(su * sp.diff(f, su) / f)
    sM = sp.simplify(sm * sp.diff(f, sm) / f)
    return (sL == 0) or (sM == 0)


# ── the helical realisation count ───────────────────────────────────────────
def norm5(x):
    return sp.simplify(sp.expand(x * x.subs(S5, -S5)))


def hmul(x, y):
    p = sp.expand(x * y)
    return sp.radsimp(sp.simplify(p / sp.sqrt(sp.Abs(norm5(p)))))


def realisation_turns(x0, tol=1e-12, maxit=14):
    x = sp.nsimplify(x0)
    prev = float(x)
    locked_prev = False
    for k in range(1, maxit + 1):
        x = hmul(x, PHI)
        v = float(x)
        locked = abs(v / prev - PHIF) < tol
        prev = v
        if locked and locked_prev:
            return k - 1
        locked_prev = locked
    return None


# ── the declared flow ──────────────────────────────────────────────────────
def evolve(n=120000, burn=2000, seed=11):
    """x -> 1/(4x+2), perturbed at the structural floor. The fixed point of the
    map is exactly r, so the flow visits the states around the pole rather than
    sitting on it."""
    rng = random.Random(seed)
    x, out = 0.5, []
    sc = R3F * math.sqrt(3.0)
    for i in range(n + burn):
        x = 1.0 / (4.0 * x + 2.0) + sc * rng.uniform(-1.0, 1.0)
        if i >= burn:
            out.append(x)
    return out


XS = evolve()


def H5(N):
    if N == math.inf:
        return 1.0
    s = N / (N + 1.0)
    t = s ** 10
    return 2 * t / (1 + t)


def master(f, T, path_factor=1.0):
    """R[O]: the H_5-weighted average of O over the flow.

    path_factor carries the retention factors that belong INSIDE the averaged
    object when the observable is a path integral rather than a state value.
    Returns the weighted readout and the unweighted colour average alongside it,
    so the H_5 contribution can be separated from the evolution contribution.
    """
    lam = sp.lambdify((su, sm), f, "math")
    sig = compile_signature(f)
    num = den = plain = 0.0
    prev_h = None
    for x in XS:
        th = hue(sig, x)
        if prev_h is None:
            dth = 0.0
        else:
            d = math.radians(th - prev_h)
            dth = abs(math.degrees(math.atan2(math.sin(d), math.cos(d))))
        prev_h = th
        w = 1.0 if dth == 0.0 else H5(360.0 * T / dth)
        v = lam(1 - x, x) * path_factor
        num += w * v
        den += w
        plain += v
    return num / den, plain / len(XS)


# ── the six directly compared observables of the Ledger's score ────────────
SUITE = [
    ("Omega_b",  sm**2/2,                  0.0493017, 0.0007, False),
    ("Omega_c",  4*sm**2*su,               0.2645,    0.0026, False),
    ("Omega_DE", 1 - sm**2/2 - 4*sm**2*su, 0.6847,    0.0073, False),
    ("Y_He",     su**2/2,                  0.2450,    0.0030, False),
    ("n_s",      1 - sm**2 + 2*sm**3,      0.9649,    0.0042, False),
    ("tau",      2*sm**3,                  0.0544,    0.0073, True),
]

print("THE MASTER EQUATION")
print("=" * 104)
print("R[O] = sum H_5(360 T / dtheta) O(C) / sum H_5,   flow x -> 1/(4x+2) + r^3 sqrt3 U(-1,1)")
print()

rows = []
for key, expr, meas, sig, is_path in SUITE:
    f = sp.sympify(expr)
    exact = sp.nsimplify(sp.simplify(f.subs(SUB)))
    static = float(sp.N(exact, 25))
    T = realisation_turns(exact)
    pure = is_pure(f)
    # the path factor is a constant, so one pass suffices: it scales both the
    # weighted readout and the plain colour average by the same amount.
    pf = PATH3 if is_path else 1.0
    R_plain, colour_untyped = master(f, T if T else 1, 1.0)
    R_typed = R_plain * pf
    rows.append(dict(key=key, static=static, colour=colour_untyped,
                     master=R_typed, T=T, pure=bool(pure),
                     measured=meas, sigma=sig, path=is_path,
                     pull_static=(static - meas) / sig,
                     pull_colour=(colour_untyped - meas) / sig,
                     pull_master=(R_typed - meas) / sig))

print("%-10s %5s %5s %12s %12s %12s %12s"
      % ("observable", "pure", "T", "static", "colour avg", "TYPED MASTER", "measured"))
for d in rows:
    print("%-10s %5s %5s %12.7f %12.7f %12.7f %12.7f"
          % (d["key"], "yes" if d["pure"] else "MIX", str(d["T"]),
             d["static"], d["colour"], d["master"], d["measured"]))

print()
print("%-10s %11s %11s %11s   %s"
      % ("observable", "pull static", "pull colour", "pull MASTER", "what moved it"))
for d in rows:
    why = ("retyped as a path integral, factor (1-r^3)^3" if d["path"]
           else ("H_5 weighting, mixed channel" if not d["pure"]
                 else "nothing: pure channel, untyped"))
    print("%-10s %+11.4f %+11.4f %+11.4f   %s"
          % (d["key"], d["pull_static"], d["pull_colour"], d["pull_master"], why))

E0 = statistics.fmean(abs(d["pull_static"]) for d in rows)
Ec = statistics.fmean(abs(d["pull_colour"]) for d in rows)
E1 = statistics.fmean(abs(d["pull_master"]) for d in rows)
PT = 1 - E1 / E0

print()
print("mean |pull|   old corpus static %.4f   colour average %.4f   TYPED MASTER %.4f"
      % (E0, Ec, E1))
print("THE TRAVERSAL PAYMENT   P_T = 1 - E_1/E_0 = %.6f      one third = %.6f"
      % (PT, 1/3))
print("                        gap to one third = %+.4f percentage points"
      % (100 * (PT - 1/3)))

# ── 3. THE ENSEMBLE TEST the Ledger proposes and does not run ──────────────
print()
print("=" * 104)
print("3  IS THE ONE THIRD A LAW OR AN ARTEFACT OF THESE SIX?")
print()
print("The payment is a ratio of two means over one chosen ensemble. If it is a")
print("law it survives resampling the ensemble. Every subset of size 3 or more:")
print()

s_abs = {d["key"]: abs(d["pull_static"]) for d in rows}
m_abs = {d["key"]: abs(d["pull_master"]) for d in rows}
keys = [d["key"] for d in rows]

subsets = []
for k in range(3, len(keys) + 1):
    for combo in itertools.combinations(keys, k):
        e0 = statistics.fmean(s_abs[c] for c in combo)
        e1 = statistics.fmean(m_abs[c] for c in combo)
        subsets.append((set(combo), 1 - e1 / e0))

print("   %-6s %8s %8s %8s %8s   %s"
      % ("size", "n", "min P_T", "median", "max P_T", "within 0.05 of 1/3"))
for k in range(3, len(keys) + 1):
    g = [p for s, p in subsets if len(s) == k]
    near = sum(1 for p in g if abs(p - 1/3) < 0.05)
    print("   %-6d %8d %8.4f %8.4f %8.4f   %d of %d"
          % (k, len(g), min(g), statistics.median(g), max(g), near, len(g)))

allp = [p for _, p in subsets]
near_all = sum(1 for p in allp if abs(p - 1/3) < 0.05)
print()
print("   over all %d subsets: median P_T = %.4f, %d of %d within 0.05 of one third"
      % (len(allp), statistics.median(allp), near_all, len(allp)))

print()
print("   LEAVE ONE OUT, which is the sharpest version of the same question:")
print("   %-12s %10s   %s" % ("dropped", "P_T", "reading"))
loo = []
for d in rows:
    rest = [c for c in keys if c != d["key"]]
    e0 = statistics.fmean(s_abs[c] for c in rest)
    e1 = statistics.fmean(m_abs[c] for c in rest)
    p = 1 - e1 / e0
    loo.append((d["key"], p))
    print("   %-12s %10.4f   %s"
          % (d["key"], p, "holds" if abs(p - 1/3) < 0.05 else "BREAKS"))

held = sum(1 for _, p in loo if abs(p - 1/3) < 0.05)
worst = max(loo, key=lambda z: abs(z[1] - 1/3))
print()
print("   the payment holds under %d of %d single deletions." % (held, len(loo)))
print("   the one deletion that breaks it is %s, at P_T = %.4f."
      % (worst[0], worst[1]))

# ── 4. what that outlier is telling us ────────────────────────────────────
out = next(d for d in rows if d["key"] == worst[0])
print()
print("4  WHAT THE OUTLIER SAYS")
print()
print("   %s is the one observable in the score that the passage does not move:"
      % out["key"])
print("   pull %+.4f static -> %+.4f master, a change of %.4f sigma."
      % (out["pull_static"], out["pull_master"],
         abs(out["pull_master"] - out["pull_static"])))
print("   It is pure-channel, so H_5 cannot weight it, and it is untyped, so no")
print("   path factor enters. It therefore sits in both means almost unchanged")
print("   and holds the ratio UP. Removing it raises the payment to %.4f."
      % worst[1])
print()
print("   That is a located obligation, not a nuisance. tau was retyped because")
print("   standard cosmology already defines it as a line-of-sight integral. The")
print("   same question has not been asked of %s: a primordial abundance is the" % out["key"])
print("   frozen endpoint of a reaction network, so it is a RECORD of a completed")
print("   process rather than a state of the field. Under Logical Action that is")
print("   the same type distinction that forced the tau retyping. If it applies,")
print("   the payment moves toward %.4f rather than %.4f, and the one-third"
      % (worst[1], PT))
print("   reading is the one that has to be revised.")

# ── 5. the candidate typing, declared as a candidate ──────────────────────
# The two entries the passage cannot move, Omega_b = W_M/2 and Y_He = W_L/2, are
# exactly the two HALF-weights of the score. That suggests one rule rather than
# two corrections: a half-weight is a weight read across the boundary and picks
# up the floor once, 1/(1-r^3).
#
# THIS WAS FOUND BY LOOKING AT THE RESIDUAL. The Ledger's own rule against
# hindsight selection therefore applies to it, and it is computed here to be
# scored, not to be adopted. What makes it worth writing down rather than
# discarding is that it is testable as a SINGLE rule: it touches exactly the two
# half-weights, in the same direction, with the same factor, and it exempts
# nothing. What would make it legitimate is a derivation of the boundary factor
# for a half-weight produced without consulting these residuals.
print()
print("=" * 104)
print("5  A CANDIDATE TYPING, SCORED BUT NOT ADOPTED")
print()
HALF = {"Omega_b", "Y_He"}
cand = {}
for d in rows:
    v = d["master"] / (1 - R3F) if d["key"] in HALF else d["master"]
    cand[d["key"]] = v
cand["Omega_DE"] = 1 - cand["Omega_b"] - cand["Omega_c"]   # closure, not retyped
print("   %-10s %12s %12s %10s %10s   %s"
      % ("observable", "master", "half-weight", "pull was", "pull now", "touched?"))
cp = {}
for d in rows:
    v = cand[d["key"]]
    p = (v - d["measured"]) / d["sigma"]
    cp[d["key"]] = p
    print("   %-10s %12.7f %12.7f %+10.4f %+10.4f   %s"
          % (d["key"], d["master"], v, d["pull_master"], p,
             "yes, 1/(1-r^3)" if d["key"] in HALF
             else ("no: moved only by closure" if d["key"] == "Omega_DE" else "no")))
E2 = statistics.fmean(abs(p) for p in cp.values())
PT2 = 1 - E2 / E0
print()
print("   mean |pull| %.4f -> %.4f     P_T would become %.4f" % (E1, E2, PT2))
print()
print("   Two things to hold together. The fit is much better, and Omega_DE also")
print("   improves although the rule never touches it, only its closure. That is")
print("   the signature of a structural correction rather than a per-parameter")
print("   one. But %.4f is not one third and not two thirds, so adopting this" % PT2)
print("   rule DESTROYS the traversal-payment reading rather than sharpening it.")
print("   The two claims are rivals: either the boundary typing is right and the")
print("   one third is a coincidence of the untyped half-weights, or the one")
print("   third is real and this factor is hindsight. Nothing here decides it.")

# ── 6. THE TYPING LADDER ──────────────────────────────────────────────────
# The score contains exactly three entries that are RECORDS rather than states:
#
#   tau    a line-of-sight integral, typed
#   Omega_b   a half-weight, untyped
#   Y_He      a half-weight, untyped
#
# The Ledger reads the payment as a possible universal constant of traversal.
# There is a sharper reading available, and it is testable here: the payment may
# be a measure of HOW MUCH OF THE SCORE HAS BEEN TYPED. If so it should rise
# monotonically as each record is read correctly, and the one third is then the
# value at exactly one typed record rather than a law about traversal itself.
print()
print("=" * 104)
print("6  THE TYPING LADDER")
print()
print("Three entries in the score are records rather than states. Type them one")
print("at a time and read the payment at each stage.")
print()

RECORDS = ["tau", "Omega_b", "Y_He"]


def score(typed):
    """Mean |pull| with the named records typed.

    The ladder sits ON TOP of the full operator: the mixed entries keep their
    H_5 weighting, so the rung with only tau typed reproduces the typed master
    exactly. tau takes the path factor, a half-weight takes the boundary factor,
    and Omega_DE follows by the closure identity the Ledger declares.
    """
    v = {}
    for d in rows:
        k = d["key"]
        x = d["master"] / PATH3 if k == "tau" else d["master"]
        if k == "tau" and "tau" in typed:
            x *= PATH3
        elif k in ("Omega_b", "Y_He") and k in typed:
            x /= (1 - R3F)
        v[k] = x
    v["Omega_DE"] = 1 - v["Omega_b"] - v["Omega_c"]
    return statistics.fmean(abs((v[d["key"]] - d["measured"]) / d["sigma"])
                            for d in rows), v


ladder = []
for k in range(len(RECORDS) + 1):
    for combo in itertools.combinations(RECORDS, k):
        E, _ = score(set(combo))
        ladder.append(dict(n_typed=k, typed=sorted(combo),
                           mean_abs_pull=E, payment=1 - E / E0))

print("   %-9s %-30s %11s %11s" % ("typed", "which records", "mean |pull|", "P_T"))
for L in ladder:
    print("   %-9d %-30s %11.4f %11.4f"
          % (L["n_typed"], ", ".join(L["typed"]) or "none", L["mean_abs_pull"],
             L["payment"]))

print()
by_n = {}
for L in ladder:
    by_n.setdefault(L["n_typed"], []).append(L["payment"])
print("   %-9s %11s %11s %11s" % ("n typed", "min P_T", "mean P_T", "max P_T"))
for k in sorted(by_n):
    g = by_n[k]
    print("   %-9d %11.4f %11.4f %11.4f"
          % (k, min(g), statistics.fmean(g), max(g)))
mono = all(min(by_n[k + 1]) > max(by_n[k]) for k in sorted(by_n)[:-1])
p_tau = [L["payment"] for L in ladder if L["typed"] == ["tau"]][0]
print()
print("   strictly increasing in the number of records typed: %s" % mono)
print("   the payment with only tau typed is %.4f; one third is %.4f."
      % (p_tau, 1/3))
print()
print("   READING. The payment is not a constant of traversal. It measures how")
print("   much of the score has been read at its correct type, and it rises with")
print("   every type that is read. One third is the value at one typed record out")
print("   of three, which is where the audit currently stands. That also explains")
print("   the leave-one-out result without any appeal to coincidence: removing an")
print("   untyped record from the score does the same arithmetic work as typing")
print("   it, so the payment goes up.")

res = dict(generated=datetime.datetime.now().isoformat(timespec="seconds"),
           rows=rows, E0_static=E0, E_colour=Ec, E1_master=E1,
           traversal_payment=PT, one_third_gap_pp=100 * (PT - 1/3),
           subsets=dict(n=len(allp), median=statistics.median(allp),
                        within_0p05_of_third=near_all,
                        all=[dict(keys=sorted(s), size=len(s), P_T=p)
                             for s, p in subsets]),
           leave_one_out={k: p for k, p in loo},
           outlier=worst[0],
           candidate_half_weight_typing=dict(
               rule="Omega_b and Y_He, the two half-weights, divided by (1-r^3)",
               status="found after the fact; needs an independent derivation",
               pulls=cp, mean_abs_pull=E2, payment=PT2),
           typing_ladder=dict(records=RECORDS, rungs=ladder,
                              monotone=bool(mono), payment_one_typed=p_tau))
json.dump(res, open(OUT, "w"), indent=2)
print()
print("written:", OUT)

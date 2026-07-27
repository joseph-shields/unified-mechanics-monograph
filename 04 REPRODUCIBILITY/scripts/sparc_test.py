"""Test the Unified Mechanics gold-silver interface closure against SPARC.

UM closure (main monograph eq. 19.1-19.3):
    g * g_I = a* g_b,  g_I = g - g_b   =>   g = [g_b + sqrt(g_b^2 + 4 a* g_b)] / 2
with the zero-fit scale a* = c H0 dB, dB = -2*sqrt(2) + 5/4 + 3*sqrt(5)/4.

Compared against the standard RAR function (McGaugh, Lelli & Schombert 2016):
    g = g_b / (1 - exp(-sqrt(g_b/gd))),  gd = 1.2e-10 m/s^2.
"""

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
def _d(*p): return _os.path.join(_ROOT, "data", *p)
def _r(*p): return _os.path.join(_ROOT, "results", *p)
def _f(*p): return _os.path.join(_ROOT, "figures", *p)
import numpy as np
from scipy.optimize import minimize_scalar
import json, math

KPC = 3.0856775814913673e19   # m
KMS = 1e3

# ---------------- UM constants ----------------
dB = -2*math.sqrt(2) + 5/4 + 3*math.sqrt(5)/4
H0 = 72.1 * KMS / (KPC * 1e3)          # 72.1 km/s/Mpc in 1/s
C = 2.99792458e8
A_STAR = C * H0 * dB
print(f"dB = {dB:.12f}")
print(f"a* = c H0 dB = {A_STAR:.6e} m/s^2")
print(f"a* * sqrt(3) = {A_STAR*math.sqrt(3):.6e} m/s^2   (snowflake covolume check)")

# ---------------- parse SPARC ----------------
# galaxy table: quality flag Q (col), inclination
gal = {}
with open(_d("SPARC", "SPARC_Lelli2016c.mrt")) as f:
    lines = f.readlines()
start = next(i for i, l in enumerate(lines) if l.startswith("----"))
# find the last dashed line before data
dash = [i for i, l in enumerate(lines) if set(l.strip()) == {"-"}]
for l in lines[dash[-1]+1:]:
    if len(l.strip()) == 0: continue
    parts = l.split()
    if len(parts) < 18: continue
    ID = parts[0]
    inc = float(parts[5]); Q = int(parts[17])
    gal[ID] = dict(inc=inc, Q=Q)

pts = []
with open(_d("SPARC", "MassModels_Lelli2016c.mrt")) as f:
    lines = f.readlines()
dash = [i for i, l in enumerate(lines) if set(l.strip()) == {"-"}]
for l in lines[dash[-1]+1:]:
    if len(l.strip()) == 0: continue
    ID = l[0:11].strip()
    D, R, Vobs, eV, Vgas, Vdisk, Vbul = (float(x) for x in
        (l[12:18], l[19:25], l[26:32], l[33:38], l[39:45], l[46:52], l[53:59]))
    pts.append((ID, R, Vobs, eV, Vgas, Vdisk, Vbul))
print("galaxies:", len(gal), " points:", len(pts))

# standard RAR sample cuts (MLS16): Q != 3, inc >= 30, eV/Vobs < 0.10, Vbar^2 > 0
UD, UB = 0.5, 0.7   # M/L disk, bulge at 3.6um
g_obs, g_bar, w = [], [], []
used_gal = set()
for ID, R, Vobs, eV, Vgas, Vdisk, Vbul in pts:
    if ID not in gal: continue
    if gal[ID]["Q"] == 3 or gal[ID]["inc"] < 30: continue
    if Vobs <= 0 or eV / Vobs >= 0.10: continue
    v2bar = Vgas*abs(Vgas) + UD*Vdisk*abs(Vdisk) + UB*Vbul*abs(Vbul)
    if v2bar <= 0: continue
    go = (Vobs*KMS)**2 / (R*KPC)
    gb = v2bar*KMS**2 / (R*KPC)
    g_obs.append(go); g_bar.append(gb)
    # log-space inverse-variance weight. Retained and reported, not used in the
    # headline fit: the published claim is an unweighted rms comparison, and the
    # weighted variant is reported separately so the two are never conflated.
    w.append(1.0 / max(2*eV/Vobs/math.log(10), 1e-3)**2)
    used_gal.add(ID)
g_obs = np.array(g_obs); g_bar = np.array(g_bar); w = np.array(w)
print("sample:", len(g_obs), "points from", len(used_gal), "galaxies")

assert len(g_obs) == len(g_bar) == len(w), "sample arrays disagree"
lgo = np.log10(g_obs); lgb = np.log10(g_bar)

# ---------------- models ----------------
def um(gb, a):    # UM bilinear closure
    return (gb + np.sqrt(gb**2 + 4*a*gb)) / 2
def rar(gb, gd):  # MLS16 exponential family
    return gb / (1 - np.exp(-np.sqrt(gb/gd)))

def rms_log(model, *args):
    return float(np.sqrt(np.mean((lgo - np.log10(model(g_bar, *args)))**2)))
def med_bias(model, *args):
    return float(np.median(lgo - np.log10(model(g_bar, *args))))

def fit_scale(model):
    r = minimize_scalar(lambda la: rms_log(model, 10**la), bounds=(-12, -9), method="bounded")
    return 10**r.x, r.fun

a_fit, rms_a = fit_scale(um)
gd_fit, rms_g = fit_scale(rar)

results = {
  "sample_points": int(len(g_obs)),
  "sample_galaxies": int(len(used_gal)),
  "a_star_frozen": A_STAR,
  "a_star_sqrt3": A_STAR*math.sqrt(3),
  "UM_frozen":  {"a": A_STAR, "rms_dex": rms_log(um, A_STAR), "median_bias_dex": med_bias(um, A_STAR)},
  "UM_sqrt3":   {"a": A_STAR*math.sqrt(3), "rms_dex": rms_log(um, A_STAR*math.sqrt(3)), "median_bias_dex": med_bias(um, A_STAR*math.sqrt(3))},
  "UM_freefit": {"a": a_fit, "rms_dex": rms_a, "median_bias_dex": med_bias(um, a_fit)},
  "RAR_frozen": {"gdag": 1.2e-10, "rms_dex": rms_log(rar, 1.2e-10), "median_bias_dex": med_bias(rar, 1.2e-10)},
  "RAR_freefit":{"gdag": gd_fit, "rms_dex": rms_g, "median_bias_dex": med_bias(rar, gd_fit)},
  "UM_freefit_weighted": {"a": float(10**minimize_scalar(
        lambda la: float(np.sum(w*(lgo-np.log10(um(g_bar,10**la)))**2)/np.sum(w)),
        bounds=(-12,-9), method="bounded").x), "estimator": "inverse-variance weighted rms"},
  "ratio_afit_over_astar": a_fit / A_STAR,
  "sqrt3": math.sqrt(3),
}
print(json.dumps(results, indent=2))
json.dump(results, open(_r("sparc_results.json"), "w"), indent=2)

# ---------------- deep-MOND regime check: low-acceleration points ----------------
low = g_bar < 1e-11
if low.sum() > 30:
    for name, m, arg in [("UM frozen", um, A_STAR), ("UM sqrt3", um, A_STAR*math.sqrt(3)), ("RAR 1.2e-10", rar, 1.2e-10)]:
        r = np.sqrt(np.mean((lgo[low] - np.log10(m(g_bar[low], arg)))**2))
        b = np.median(lgo[low] - np.log10(m(g_bar[low], arg)))
        print(f"low-acc (n={low.sum()}): {name}: rms={r:.3f} dex, bias={b:+.3f} dex")

# ---------------- figure ----------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt



INK, GOLD, GOLD2, SLATE, BG = "#102A43", "#B48A2E", "#E6B655", "#5B6B7A", "#FBF8F1"
fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.4), dpi=150)
fig.patch.set_facecolor(BG)

ax = axes[0]
ax.set_facecolor(BG)
hb = ax.hexbin(lgb, lgo, gridsize=55, cmap="bone_r", mincnt=1, linewidths=0)
xs = np.logspace(-12.6, -8.4, 300)
ax.plot(np.log10(xs), np.log10(xs), ":", color=SLATE, lw=1, label="g = g_b (no interface)")
ax.plot(np.log10(xs), np.log10(rar(xs, 1.2e-10)), "-", color=SLATE, lw=1.6,
        label="RAR g† = 1.20e-10 (fitted, MLS16)")
ax.plot(np.log10(xs), np.log10(um(xs, A_STAR)), "--", color="#8A2E2E", lw=1.6,
        label=f"UM closure, a★ = cH₀ΔB = {A_STAR:.2e} (zero-fit)")
ax.plot(np.log10(xs), np.log10(um(xs, A_STAR*math.sqrt(3))), "-", color=GOLD, lw=2.2,
        label=f"UM closure, √3·a★ = {A_STAR*math.sqrt(3):.2e} (zero-fit)")
ax.set_xlabel("log₁₀ g_bar  [m s⁻²]"); ax.set_ylabel("log₁₀ g_obs  [m s⁻²]")
ax.set_title("Radial acceleration relation — SPARC vs the interface closure", color=INK)
ax.legend(fontsize=8, loc="upper left", framealpha=0.9)
ax.set_xlim(-12.6, -8.4); ax.set_ylim(-12.2, -8.4)

ax = axes[1]
ax.set_facecolor(BG)
for name, m, arg, col in [("UM a★", um, A_STAR, "#8A2E2E"),
                          ("UM √3a★", um, A_STAR*math.sqrt(3), GOLD),
                          ("RAR g†", rar, 1.2e-10, SLATE)]:
    res = lgo - np.log10(m(g_bar, arg))
    ax.hist(res, bins=np.linspace(-0.8, 0.8, 90), histtype="step", lw=1.8,
            color=col, label=f"{name}: rms {np.sqrt(np.mean(res**2)):.3f} dex")
ax.axvline(0, color=INK, lw=0.8)
ax.set_xlabel("log₁₀ g_obs − log₁₀ g_model  [dex]")
ax.set_ylabel("points")
ax.set_title(f"Residuals — {len(g_obs)}-point SPARC sample", color=INK)
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig(_f("sparc_rar.png"), facecolor=BG)
print("wrote sparc_rar.png")

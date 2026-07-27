"""O5 and O6, computed from published values with no fitting anywhere.

O5 asked for the integral joining record growth to the measured expansion history.
Paper 19 proved the zeroth-order clause H.t = 1 and left the residual open. But the
residual is not free: the corpus already carries a parameter-free vacuum readout,

        lambda = (4 pi / sqrt3) r^240

which Part Five of the Register computes and then declines to promote, on the stated
ground that numerical resemblance is not derivation. One reason it could not be promoted
is that it rested on O4, which was open. O4's existence half is now proved by explicit
construction, so lambda now stands on a proved lemma. This recomputes the comparison.

O6 is the Hubble stake. The framework's claim is that the two pipelines differ by three
audited closures, so the local reading exceeds the early-universe reading by exactly the
retained fraction over three crossings, (1 - r^3)^3. That is checked here against the
published pair with errors propagated.

Nothing below is fitted. Every framework number is closed-form.
"""

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
def _cert(n): return _os.path.join(_ROOT, "certificates", n)
def _csv(n):  return _os.path.join(_ROOT, n)
import math, json, os, datetime



HERE = os.path.dirname(os.path.abspath(__file__))

# ---- framework constants, closed form --------------------------------------------
phi   = (1 + math.sqrt(5)) / 2
r     = 1 / (2 * phi)
r3    = r ** 3
lam   = (4 * math.pi / math.sqrt(3)) * r ** 240
keep3 = (1 - r3) ** 3

# ---- physical constants (CODATA 2018) --------------------------------------------
c    = 2.99792458e8
l_P  = 1.616255e-35            # Planck length, m
Mpc  = 3.0856775814913673e22

def H_si(H_kms_Mpc):  return H_kms_Mpc * 1e3 / Mpc

def Lambda_planck_units(H0, OmL):
    """Lambda in Planck units, i.e. Lambda * l_P^2, from H0 and Omega_Lambda."""
    return 3 * OmL * (H_si(H0) / c) ** 2 * l_P ** 2

def rel_err(H0, sH0, OmL, sOmL):
    return math.sqrt((sOmL / OmL) ** 2 + (2 * sH0 / H0) ** 2)

datasets = {
    "Planck 2018 TT,TE,EE+lowE+lensing":        dict(H0=67.36, sH0=0.54, OmL=0.6847, sOmL=0.0073),
    "Planck 2018 TT,TE,EE+lowE+lensing+BAO":    dict(H0=67.66, sH0=0.42, OmL=0.6889, sOmL=0.0056),
}

print("O5   the standing vacuum readout against the measured cosmological constant")
print(f"     framework   lambda = (4pi/sqrt3) r^240 = {lam:.6e}   (no free parameter)")
print()
out5 = {}
for name, d in datasets.items():
    meas = Lambda_planck_units(d["H0"], d["OmL"])
    e    = rel_err(**d)
    ratio = lam / meas
    sigma = abs(ratio - 1) / e
    print(f"     {name}")
    print(f"       measured  Lambda l_P^2 = {meas:.6e}  +- {e*100:.2f}%")
    print(f"       framework / measured   = {ratio:.5f}      ({sigma:.2f} sigma)")
    out5[name] = {"measured": meas, "rel_err": e, "ratio": ratio, "sigma": sigma}
print()

# ---- what Omega_Lambda the framework implies, and then H0.t0 ----------------------
print("     turning that into the expansion history, still with no fitting:")
for name, d in datasets.items():
    OmL_pred = lam / (3 * (H_si(d["H0"]) / c) ** 2 * l_P ** 2)
    Om_m = 1 - OmL_pred
    # H0 t0 = integral from 0 to 1 of da / sqrt(Om_m/a + OmL a^2)
    N = 2_000_000
    s = 0.0
    for k in range(N):
        a = (k + 0.5) / N
        s += 1.0 / math.sqrt(Om_m / a + OmL_pred * a * a)
    H0t0 = s / N
    t0 = H0t0 / H_si(d["H0"]) / (365.25 * 24 * 3600 * 1e9)
    print(f"       {name.split('+lowE')[0]:<28} Omega_L = {OmL_pred:.4f} "
          f"(measured {d['OmL']:.4f} +- {d['sOmL']:.4f}),  H0.t0 = {H0t0:.4f},  t0 = {t0:.3f} Gyr")
    out5[name].update(OmL_pred=OmL_pred, H0t0=H0t0, t0_Gyr=t0)
print()
print("     the zeroth-order clause H.t = 1 is proved; the shortfall to 0.95 is the")
print("     integrated price, and it now follows from lambda rather than being fitted.")
print()

# ---- O6, the Hubble stake ---------------------------------------------------------
print("O6   the audited closure counts, tested on the Hubble pair")
early = dict(H0=67.36, s=0.54, src="Planck 2018")
local = dict(H0=73.04, s=1.04, src="SH0ES 2022 (Riess et al.)")
pred  = early["H0"] / keep3
spred = early["s"] / keep3
sigma_comb = math.sqrt(spred ** 2 + local["s"] ** 2)
pull = (pred - local["H0"]) / sigma_comb
print(f"     retained over three crossings (1-r^3)^3 = {keep3:.9f}   gap = {(1-keep3)*100:.3f}%")
print(f"     early  {early['src']:<26} H0 = {early['H0']:.2f} +- {early['s']:.2f}")
print(f"     framework predicts local          H0 = {pred:.2f} +- {spred:.2f}")
print(f"     local  {local['src']:<26} H0 = {local['H0']:.2f} +- {local['s']:.2f}")
print(f"     pull = {pull:+.2f} sigma      (the corpus states 'about half a standard deviation')")

json.dump({"generated": datetime.datetime.now().isoformat(timespec="seconds"),
           "framework": {"phi": phi, "r": r, "r_cubed": r3, "lambda": lam,
                         "retained_three_crossings": keep3},
           "O5": out5,
           "O6": {"predicted_local_H0": pred, "sigma": spred,
                  "measured_local_H0": local["H0"], "measured_sigma": local["s"],
                  "pull_sigma": pull}},
          open(_cert("o5_o6_certificate.json"), "w"), indent=2)

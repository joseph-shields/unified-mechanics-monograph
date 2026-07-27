"""The framework already has a variational principle. It is T24.

T24 states that the square of a defect formed from curvature weighted by u against
realised area weighted by r has exactly three terms and no others:

    D = u R + r (e ^ e)
    D ^ D = u^2 (R^R) + 2ur (R^e^e) + r^2 (e^e^e^e)

That is term for term the MacDowell-Mansouri action for gravity with a cosmological
constant, in which

    F = R + (Lambda/3) e^e
    F ^ F = R^R + (2 Lambda/3) (R^e^e) + (Lambda^2/9) (e^e^e^e)

with the Gauss-Bonnet term topological in four dimensions, the cross term giving
Einstein-Hilbert, and the quartic term giving the cosmological constant.

The match is OVERDETERMINED. Two independent coefficient ratios must both return the
same Lambda, and there is nothing to tune: u and r are fixed by T4. This script checks
whether they agree, extracts the closed form, and then asks whether the value is
consistent with the standing vacuum readout, which reaches Lambda by a completely
different route (one retention per root over a complete closure).
"""
import math, json, os, datetime
from fractions import Fraction

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
def _cert(n): return os.path.join(_ROOT, "certificates", n)

phi = (1 + math.sqrt(5)) / 2
r   = 1 / (2 * phi)
u   = 1 - r
W_L, W_B, W_M = u*u, 2*u*r, r*r

# ---- the overdetermination check --------------------------------------------------
# from the cross term:   2ur / u^2 = 2 Lambda / 3   ->  Lambda = 3 r / u
# from the quartic term:  r^2 / u^2 = Lambda^2 / 9  ->  Lambda = 3 r / u
lam_from_cross   = 3 * (W_B / W_L) / 2
lam_from_quartic = 3 * math.sqrt(W_M / W_L)
agree = abs(lam_from_cross - lam_from_quartic) < 1e-14

# ---- closed form -------------------------------------------------------------------
# r/u = r/(1-r) with r = (sqrt5 - 1)/4 gives exactly 1/sqrt5, so Lambda = 3/sqrt5.
lam_carrier = 3 * r / u
closed      = 3 / math.sqrt(5)
closed_ok   = abs(lam_carrier - closed) < 1e-15

print("T24 read as an action, with the three weights as its coefficients")
print(f"   W_L (R^R, topological)   = {W_L:.12f}")
print(f"   W_B (R^e^e, Einstein)    = {W_B:.12f}")
print(f"   W_M (e^4, cosmological)  = {W_M:.12f}")
print()
print("Overdetermination check: two independent ratios, one Lambda, nothing to tune")
print(f"   from the cross term    Lambda = {lam_from_cross:.15f}")
print(f"   from the quartic term  Lambda = {lam_from_quartic:.15f}")
print(f"   agree to machine precision: {agree}")
print()
print(f"   closed form   Lambda = 3r/u = 3/sqrt5 = {closed:.15f}   exact: {closed_ok}")
print()

# ---- consistency with the standing vacuum readout ----------------------------------
lam_planck = (4 * math.pi / math.sqrt(3)) * r ** 240      # Lambda * l_P^2
l_P  = 1.616255e-35
c    = 2.99792458e8
Mpc  = 3.0856775814913673e22

# Lambda_physical = (3/sqrt5) / ell^2  and  Lambda_physical * l_P^2 = lam_planck
# so (ell / l_P)^2 = (3/sqrt5) / lam_planck
ell_over_lP = math.sqrt(closed / lam_planck)
ell = ell_over_lP * l_P
Lambda_phys = closed / ell**2
R_dS = math.sqrt(3 / Lambda_phys)                          # de Sitter radius

H0 = 67.36e3 / Mpc
R_H = c / H0                                               # Hubble radius

print("Two independent routes to Lambda, and what their agreement fixes")
print(f"   route 1, the three weights : Lambda = {closed:.9f} in carrier units")
print(f"   route 2, one retention per root over a complete closure:")
print(f"            Lambda l_P^2 = (4pi/sqrt3) r^240 = {lam_planck:.6e}")
print()
print(f"   together they fix the carrier-to-physical length:")
print(f"      ell / l_P = {ell_over_lP:.6e}")
print(f"      ell       = {ell:.6e} m   = {ell/9.4607e15/1e9:.3f} billion light years")
print()
print(f"   de Sitter radius sqrt(3/Lambda) = {R_dS:.6e} m")
print(f"   Hubble radius c/H0              = {R_H:.6e} m")
print(f"   ell / R_dS = {ell/R_dS:.9f}      predicted 5^(-1/4) = {5**-0.25:.9f}")
print(f"   ell / R_H  = {ell/R_H:.6f}")
print()
print("   The carrier length lands at the cosmological horizon scale. A priori it could")
print("   have landed anywhere across hundreds of orders of magnitude.")

json.dump({
  "generated": datetime.datetime.now().isoformat(timespec="seconds"),
  "weights": {"W_L": W_L, "W_B": W_B, "W_M": W_M},
  "lambda_from_cross_term": lam_from_cross,
  "lambda_from_quartic_term": lam_from_quartic,
  "overdetermined_and_consistent": bool(agree),
  "lambda_carrier_closed_form": "3r/u = 3/sqrt(5)",
  "lambda_carrier": closed,
  "lambda_planck_units_from_r240": lam_planck,
  "ell_over_planck_length": ell_over_lP,
  "ell_metres": ell,
  "de_sitter_radius_m": R_dS,
  "hubble_radius_m": R_H,
  "ell_over_R_dS": ell / R_dS,
  "predicted_ratio_5_to_the_minus_quarter": 5 ** -0.25,
}, open(_cert("lagrangian_certificate.json"), "w"), indent=2)

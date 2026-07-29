#!/usr/bin/env python3
"""Bubble Field Closure Attack

A reproducible next-stage calculation for Joseph Shields' Universal Field of Least Action.

The script does five things:
1. Preserves the exact three-part cell partition.
2. Tests a registered two-leg vacuum-record bridge for G.
3. Writes and verifies the exact emergent-metric source equations in isotropic gauge.
4. Reconstructs an exact constant-density relativistic star in bubble variables.
5. Pushes the weak and charged-lepton scale candidates while grading every claim.

No numerical proximity is silently promoted to a derivation. Each output is tagged as
EXACT, CONDITIONAL, CANDIDATE, RECONSTRUCTION, NO-GO, or OPEN.
"""
from __future__ import annotations

import datetime as _dt
import json
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

HERE = Path(__file__).resolve().parent
OUT_JSON = HERE / "bubble_field_closure_attack_results.json"
PLOT_G = HERE / "bubble_field_G_bridge.png"
PLOT_SOURCE = HERE / "bubble_field_source_profiles.png"
PLOT_SCALE = HERE / "bubble_field_scale_ladder.png"
PLOT_LEPTON = HERE / "bubble_field_lepton_candidate.png"

# Exact SI constants
HBAR = 1.054571817e-34
C = 299_792_458.0
EV = 1.602176634e-19
MPC = 3.0856775814913673e22
G_CODATA = 6.67430e-11
G_CODATA_SIGMA = 0.00015e-11

# Comparison values only; not used to tune formulas.
V_EW_REF_GEV = 246.21965
LEPTON_REF_MEV = {
    "electron": 0.51099895069,
    "muon": 105.6583755,
    "tau": 1776.86,
}

# Golden fixed point and three-part weights
PHI = (1.0 + math.sqrt(5.0)) / 2.0
R = 1.0 / (2.0 * PHI)
U = 1.0 - R
W_L = U * U
W_B = 2.0 * U * R
W_M = R * R
TRAVERSAL_FLOOR = R**3
RETENTION = 1.0 - TRAVERSAL_FLOOR
AMPLITUDE_RESPONSE = R / U  # = 1/sqrt(5), registered reciprocal cross-channel candidate

# Two cosmological boundary records. The first reproduces the uploaded computation;
# the second is the Planck TT,TE,EE+lowE+lensing best-estimate pair.
COSMO_BOUNDARIES = {
    "uploaded_planck_chain": {
        "H0_km_s_Mpc": 67.66,
        "H0_sigma": 0.42,
        "Omega_Lambda": 0.6889,
        "Omega_Lambda_sigma": 0.0056,
        "role": "reproducibility boundary used in the uploaded scripts",
    },
    "planck_best_estimate": {
        "H0_km_s_Mpc": 67.36,
        "H0_sigma": 0.54,
        "Omega_Lambda": 0.6847,
        "Omega_Lambda_sigma": 0.0073,
        "role": "Planck 2018 TT,TE,EE+lowE+lensing central boundary",
    },
}


def geometric_lambda(H0_km_s_Mpc: float, omega_l: float) -> float:
    """Geometric cosmological constant in m^-2 under flat LambdaCDM."""
    H0 = H0_km_s_Mpc * 1000.0 / MPC
    return 3.0 * omega_l * H0**2 / C**2


def relative_lambda_sigma(H: float, sH: float, O: float, sO: float) -> float:
    """Indicative uncorrelated propagation; Planck parameters are actually correlated."""
    return math.sqrt((2.0 * sH / H) ** 2 + (sO / O) ** 2)


def q_from_G_lambda(G: float, lam: float) -> float:
    """Vacuum/Planck-density ratio in the unreduced Planck convention."""
    return lam * HBAR * G / (8.0 * math.pi * C**3)


def G_from_q_lambda(q: float, lam: float) -> float:
    return 8.0 * math.pi * C**3 * q / (HBAR * lam)


# --------------------------------------------------------------------------------------
# 1. Exact partition and candidate vacuum bridge
# --------------------------------------------------------------------------------------
q_models = {
    "r^240": R**240,
    "r^241": R**241,
    # Registered bridge: 240 internal root modes + one external readout, followed by
    # an emit/return interrogative loop. Each complete leg retains (1-r^3) in amplitude,
    # so the two-leg probability contributes (1-r^3)^2.
    "r^241 (1-r^3)^2": R**241 * RETENTION**2,
}
q_UF = q_models["r^241 (1-r^3)^2"]

cosmo_results: dict[str, dict] = {}
for name, b in COSMO_BOUNDARIES.items():
    lam = geometric_lambda(b["H0_km_s_Mpc"], b["Omega_Lambda"])
    rel_lam = relative_lambda_sigma(
        b["H0_km_s_Mpc"], b["H0_sigma"], b["Omega_Lambda"], b["Omega_Lambda_sigma"]
    )
    G_pred = G_from_q_lambda(q_UF, lam)
    q_obs = q_from_G_lambda(G_CODATA, lam)
    n_eff = math.log(q_obs) / math.log(R)
    cosmo_results[name] = {
        **b,
        "Lambda_m^-2": lam,
        "indicative_relative_Lambda_sigma_uncorrelated": rel_lam,
        "q_observed_using_CODATA_G": q_obs,
        "effective_r_exponent": n_eff,
        "G_candidate_SI": G_pred,
        "G_candidate_sigma_from_cosmo_only": abs(G_pred) * rel_lam,
        "relative_to_CODATA": G_pred / G_CODATA - 1.0,
        "q_obs_over_r241": q_obs / (R**241),
        "q_obs_over_two_leg_model": q_obs / q_UF,
    }

# Use the uploaded boundary as the reproducibility branch for downstream scale candidates.
base = cosmo_results["uploaded_planck_chain"]
G_UF = base["G_candidate_SI"]
LAMBDA_UF_BOUNDARY = base["Lambda_m^-2"]
L_PLANCK_UF = math.sqrt(HBAR * G_UF / C**3)
L_LAMBDA = math.sqrt(8.0 * math.pi / LAMBDA_UF_BOUNDARY)
A0 = math.sqrt(L_PLANCK_UF * L_LAMBDA)
A0_MATTER = W_M**0.25 * A0
E0 = HBAR * C / A0
E_PLANCK_UF = math.sqrt(HBAR * C**5 / G_UF)
E_BRIDGE = math.sqrt(E_PLANCK_UF * E0)

# Weak-scale candidate: routed localized matter fraction times the square root of the
# retained one-cycle probability, applied to the UV/IR geometric-mean energy.
OMEGA_B_ROUTE = W_M / 2.0
V_EW_CANDIDATE = OMEGA_B_ROUTE * math.sqrt(RETENTION) * E_BRIDGE
V_EW_CANDIDATE_GEV = V_EW_CANDIDATE / EV / 1e9

# Registered charged-lepton candidate. The depths 11 and 17 are pre-existing corpus
# candidates; this script does not search over integers. The absolute electron factor is
# the minimal 10-light-block + one-readout depth with the two-sided r/2 correction.
M_E_CAND = V_EW_CANDIDATE * R**11 * (1.0 - R / 2.0)
M_MU_CAND = M_E_CAND * PHI**11 * (1.0 + TRAVERSAL_FLOOR)
M_TAU_CAND = M_E_CAND * PHI**17 * (1.0 - TRAVERSAL_FLOOR)
LEPTON_CAND_MEV = {
    "electron": M_E_CAND / EV / 1e6,
    "muon": M_MU_CAND / EV / 1e6,
    "tau": M_TAU_CAND / EV / 1e6,
}

# --------------------------------------------------------------------------------------
# 2. Exact emergent-metric source equations
# --------------------------------------------------------------------------------------
# Isotropic scalar-sector metric:
# ds^2 = -exp(2A)c^2dt^2 + exp(2B)(d rho^2 + rho^2 dOmega^2)
# A = -alpha_M, B = alpha_L + nu/3.
# Orthonormal Einstein components:
# G_tt = -e^-2B (B'^2 + 2B'' + 4B'/rho)
# G_rr =  e^-2B (2A'B' + B'^2 + 2(A'+B')/rho)
# G_th =  e^-2B (A'^2 + A'' + B'' + (A'+B')/rho)

rho = sp.symbols("rho", positive=True)
m = sp.symbols("m", positive=True)
x = m / (2 * rho)
A_ext = sp.log((1 - x) / (1 + x))
B_ext = 2 * sp.log(1 + x)
Ap = sp.diff(A_ext, rho)
Bp = sp.diff(B_ext, rho)
App = sp.diff(A_ext, rho, 2)
Bpp = sp.diff(B_ext, rho, 2)
Gtt_ext = sp.simplify(-sp.exp(-2 * B_ext) * (Bp**2 + 2 * Bpp + 4 * Bp / rho))
Grr_ext = sp.simplify(sp.exp(-2 * B_ext) * (2 * Ap * Bp + Bp**2 + 2 * (Ap + Bp) / rho))
Gth_ext = sp.simplify(sp.exp(-2 * B_ext) * (Ap**2 + App + Bpp + (Ap + Bp) / rho))

# Exact relation between clock mode and spatial packing for Schwarzschild in isotropic gauge.
alpha = sp.symbols("alpha", real=True)
B_of_alpha = sp.simplify(alpha - 2 * sp.log(sp.cosh(alpha / 2)))

# --------------------------------------------------------------------------------------
# 3. Exact constant-density star reconstructed as bubble fields
# --------------------------------------------------------------------------------------
# Dimensionless R_star=1, compactness Cstar=2GM/(Rc^2). This is an exact GR source
# solution used as a toolkit boundary, then decoded into alpha_M, alpha_L and nu.
CSTAR = 0.30
RSTAR = 1.0
MGEO = CSTAR * RSTAR / 2.0
RHO_SURFACE = (RSTAR - MGEO + math.sqrt(RSTAR * (RSTAR - 2.0 * MGEO))) / 2.0

r_areal = np.geomspace(1e-4, RSTAR, 8000)
y = np.sqrt(1.0 - CSTAR * (r_areal / RSTAR) ** 2)
y_surface = math.sqrt(1.0 - CSTAR)
F = -np.arctanh(y)
F_surface = -math.atanh(y_surface)
rho_iso = RHO_SURFACE * np.exp(F - F_surface)
T_inside = 0.5 * (3.0 * y_surface - y)
A_inside = np.log(T_inside)
B_inside = np.log(r_areal / rho_iso)
alpha_M_inside = -A_inside
alpha_L_inside = AMPLITUDE_RESPONSE * alpha_M_inside
nu_inside = 3.0 * (B_inside - alpha_L_inside)
packing_inside = np.exp(B_inside)
number_ratio_inside = np.exp(nu_inside)
pressure_ratio = (y - y_surface) / (3.0 * y_surface - y)  # p/(epsilon)

# Numerical verification of Einstein source equations away from coordinate endpoints.
A1 = np.gradient(A_inside, rho_iso, edge_order=2)
B1 = np.gradient(B_inside, rho_iso, edge_order=2)
A2 = np.gradient(A1, rho_iso, edge_order=2)
B2 = np.gradient(B1, rho_iso, edge_order=2)
exp_m2B = np.exp(-2.0 * B_inside)
Gtt_num = -exp_m2B * (B1**2 + 2.0 * B2 + 4.0 * B1 / rho_iso)
Grr_num = exp_m2B * (2.0 * A1 * B1 + B1**2 + 2.0 * (A1 + B1) / rho_iso)
Gth_num = exp_m2B * (A1**2 + A2 + B2 + (A1 + B1) / rho_iso)
expected_Gtt = np.full_like(r_areal, 3.0 * CSTAR)
expected_Gp = 3.0 * CSTAR * pressure_ratio
mask = (r_areal > 0.03) & (r_areal < 0.995)
source_verification = {
    "Gtt_median_abs_error": float(np.median(np.abs(Gtt_num[mask] - expected_Gtt[mask]))),
    "Gtt_max_abs_error": float(np.max(np.abs(Gtt_num[mask] - expected_Gtt[mask]))),
    "Grr_median_abs_error": float(np.median(np.abs(Grr_num[mask] - expected_Gp[mask]))),
    "Grr_max_abs_error": float(np.max(np.abs(Grr_num[mask] - expected_Gp[mask]))),
    "Gtheta_median_abs_error": float(np.median(np.abs(Gth_num[mask] - expected_Gp[mask]))),
    "Gtheta_max_abs_error": float(np.max(np.abs(Gth_num[mask] - expected_Gp[mask]))),
}

# --------------------------------------------------------------------------------------
# 4. Range hierarchy and confinement scale inversion
# --------------------------------------------------------------------------------------
# The quadratic operators make the range classification exact:
# light:     -nabla^2                 -> 1/r, infinite range
# boundary:  -nabla^2 + m_B^2        -> exp(-m_B r)/r, finite range
# matter:     m_M^2 without gradient -> local algebraic/contact response
# The weak VEV fixes an energy scale, not the gauge normalization g_B.
L_WEAK_FROM_V = HBAR * C / V_EW_CANDIDATE

SIGMA_QCD_GEV2 = 0.18
SIGMA_QCD_SI = SIGMA_QCD_GEV2 * (1e9 * EV) ** 2 / (HBAR * C)
E_STRING = math.sqrt(SIGMA_QCD_SI * HBAR * C)
A_STRING = HBAR * C / E_STRING

# --------------------------------------------------------------------------------------
# 5. Plots
# --------------------------------------------------------------------------------------
plt.figure(figsize=(9, 5.5))
labels = list(q_models.keys())
xx = np.arange(len(labels))
width = 0.34
qobs_uploaded = cosmo_results["uploaded_planck_chain"]["q_observed_using_CODATA_G"]
qobs_planck = cosmo_results["planck_best_estimate"]["q_observed_using_CODATA_G"]
ratio_uploaded = [q_models[k] / qobs_uploaded for k in labels]
ratio_planck = [q_models[k] / qobs_planck for k in labels]
plt.bar(xx - width/2, ratio_uploaded, width=width, label="uploaded cosmology boundary")
plt.bar(xx + width/2, ratio_planck, width=width, label="Planck best-estimate boundary")
plt.axhline(1.0, linewidth=1.2, linestyle="--", label="CODATA-compatible target")
plt.xticks(xx, labels)
plt.ylabel("model q / q inferred with CODATA G")
plt.yscale("log")
plt.title("Vacuum-record bridge: hierarchy candidates against the observed target")
plt.legend()
plt.grid(axis="y", alpha=0.25)
plt.tight_layout()
plt.savefig(PLOT_G, dpi=190)
plt.close()

plt.figure(figsize=(9, 5.7))
xr = r_areal / RSTAR
plt.plot(xr, alpha_M_inside, label="matter clock alpha_M")
plt.plot(xr, alpha_L_inside, label="light barrier alpha_L")
plt.plot(xr, nu_inside, label="log number density nu")
plt.plot(xr, B_inside, label="spatial packing B")
plt.plot(xr, pressure_ratio, label="p / energy density", linestyle="--")
plt.xlabel("areal radius r / R")
plt.ylabel("dimensionless field value")
plt.title("Exact constant-density star decoded into bubble variables")
plt.legend()
plt.grid(alpha=0.25)
plt.tight_layout()
plt.savefig(PLOT_SOURCE, dpi=190)
plt.close()

scale_names = ["vacuum cell", "electron", "muon", "tau", "weak VEV", "UV/IR bridge", "Planck"]
scale_eV = [
    E0 / EV,
    LEPTON_CAND_MEV["electron"] * 1e6,
    LEPTON_CAND_MEV["muon"] * 1e6,
    LEPTON_CAND_MEV["tau"] * 1e6,
    V_EW_CANDIDATE / EV,
    E_BRIDGE / EV,
    E_PLANCK_UF / EV,
]
plt.figure(figsize=(9, 5.5))
plt.scatter(range(len(scale_names)), np.log10(scale_eV), s=70)
plt.plot(range(len(scale_names)), np.log10(scale_eV), alpha=0.55)
plt.xticks(range(len(scale_names)), scale_names, rotation=20, ha="right")
plt.ylabel("log10 energy / eV")
plt.title("Candidate scale ladder from the vacuum cell to the Planck scale")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.savefig(PLOT_SCALE, dpi=190)
plt.close()

plt.figure(figsize=(8.5, 5.2))
lep_names = ["electron", "muon", "tau"]
pred = [LEPTON_CAND_MEV[k] for k in lep_names]
obs = [LEPTON_REF_MEV[k] for k in lep_names]
xx = np.arange(3)
w = 0.36
plt.bar(xx - w / 2, pred, width=w, label="registered candidate")
plt.bar(xx + w / 2, obs, width=w, label="reference")
plt.yscale("log")
plt.xticks(xx, lep_names)
plt.ylabel("mass / MeV")
plt.title("Charged-lepton candidate spectrum (log scale)")
plt.legend()
plt.grid(axis="y", alpha=0.25)
plt.tight_layout()
plt.savefig(PLOT_LEPTON, dpi=190)
plt.close()

# --------------------------------------------------------------------------------------
# 6. Certificate
# --------------------------------------------------------------------------------------
result = {
    "generated": _dt.datetime.now().isoformat(timespec="seconds"),
    "framework": "Universal Field of Least Action / three-part Bubble Field",
    "exact_partition": {
        "phi": PHI,
        "r": R,
        "u": U,
        "W_L": W_L,
        "W_B": W_B,
        "W_M": W_M,
        "sum": W_L + W_B + W_M,
        "W_L_over_W_M": W_L / W_M,
        "traversal_floor_r3": TRAVERSAL_FLOOR,
        "retention_1_minus_r3": RETENTION,
        "amplitude_response_r_over_u": AMPLITUDE_RESPONSE,
        "status": "EXACT algebra; physical dictionary remains a realization bridge",
    },
    "G_bridge": {
        "definition_q": "q = Lambda l_P^2/(8 pi) = rho_Lambda/rho_Planck (unreduced Planck convention)",
        "registered_bridge": "q_UF = r^241 (1-r^3)^2",
        "bridge_reading": "240 internal modes + one external readout; two complete interrogative legs retain (1-r^3) in amplitude",
        "q_models": q_models,
        "cosmological_boundaries": cosmo_results,
        "status": "CONDITIONAL CLOSED CANDIDATE; the two-leg representation postulate is not yet a theorem",
        "falsifier": "a precise geometric Lambda boundary incompatible with the predicted G, or failure of the 241/readout/two-leg representation",
    },
    "scales_reproducibility_branch": {
        "G_candidate": G_UF,
        "Planck_length_m": L_PLANCK_UF,
        "Lambda_length_sqrt_8pi_over_Lambda_m": L_LAMBDA,
        "whole_cell_a0_m": A0,
        "matter_cell_WM_quarter_a0_m": A0_MATTER,
        "vacuum_cell_energy_eV": E0 / EV,
        "Planck_energy_eV": E_PLANCK_UF / EV,
        "UV_IR_bridge_energy_eV": E_BRIDGE / EV,
    },
    "emergent_metric_source_sector": {
        "metric": "ds^2=-exp(2A)c^2dt^2+exp(2B)(d rho^2+rho^2 dOmega^2)",
        "field_map": "A=-alpha_M; B=alpha_L+nu/3",
        "Einstein_orthonormal": {
            "G_tt": "-exp(-2B)[B'^2+2B''+4B'/rho]",
            "G_rr": "exp(-2B)[2A'B'+B'^2+2(A'+B')/rho]",
            "G_theta": "exp(-2B)[A'^2+A''+B''+(A'+B')/rho]",
        },
        "source_map": "epsilon=c^4 G_tt/(8 pi G); p_r=c^4 G_rr/(8 pi G); p_t=c^4 G_theta/(8 pi G)",
        "Schwarzschild_isotropic": {
            "A": "ln[(1-x)/(1+x)]",
            "B": "2 ln(1+x)",
            "x": "GM/(2 rho c^2)",
            "exact_vacuum_residuals": [str(Gtt_ext), str(Grr_ext), str(Gth_ext)],
            "exact_B_of_alphaM": str(B_of_alpha),
        },
        "constant_density_star": {
            "compactness_2GM_Rc2": CSTAR,
            "central_pressure_over_energy_density": float(pressure_ratio[0]),
            "surface_isotropic_radius_over_R": RHO_SURFACE,
            "constitutive_split": "alpha_L=(r/u) alpha_M; nu=3(B-alpha_L)",
            "center_number_density_ratio": float(number_ratio_inside[0]),
            "surface_number_density_ratio": float(number_ratio_inside[-1]),
            "numerical_equation_verification": source_verification,
        },
        "identifiability": "GR fixes A and B. It cannot separately identify alpha_L and nu without one constitutive response law.",
        "status": "EXACT macroscopic source sector in the represented scalar/spherical class; microscopic matter-to-cell law remains conditional",
    },
    "weak_scale": {
        "formula": "v_UF=(r^2/2)*sqrt(1-r^3)*sqrt(E_P E_0)",
        "candidate_GeV": V_EW_CANDIDATE_GEV,
        "reference_GeV": V_EW_REF_GEV,
        "relative_error": V_EW_CANDIDATE_GEV / V_EW_REF_GEV - 1.0,
        "Compton_length_if_mass_equals_v_m": L_WEAK_FROM_V,
        "remaining": "gauge normalization: mediator masses require m_B=g_B v/2 (and mixing for Z)",
        "status": "CONDITIONAL SCALE CANDIDATE, not yet an electroweak gauge derivation",
    },
    "charged_leptons": {
        "formulae": {
            "electron": "m_e=v r^11 (1-r/2)",
            "muon": "m_mu=m_e phi^11 (1+r^3)",
            "tau": "m_tau=m_e phi^17 (1-r^3)",
        },
        "candidate_MeV": LEPTON_CAND_MEV,
        "reference_MeV": LEPTON_REF_MEV,
        "relative_errors": {
            k: LEPTON_CAND_MEV[k] / LEPTON_REF_MEV[k] - 1.0 for k in LEPTON_REF_MEV
        },
        "status": "REGISTERED SPECTRAL CANDIDATE; integer depths require a mass-operator theorem and are not declared derived",
        "decisive_missing_step": "construct the localized phase/winding operator whose eigenvalue multiplicities force depths 11 and 17",
    },
    "range_hierarchy": {
        "light": "massless differential operator -> inverse-distance Green function -> infinite range",
        "boundary": "massive differential operator -> Yukawa Green function -> finite range",
        "matter": "no spatial kinetic term / infinite mass limit -> algebraic contact response -> zero range",
        "status": "EXACT for the stated quadratic operator block; assigning Standard Model fields remains a representation bridge",
    },
    "confinement": {
        "identity": "sigma=rho a^2=E^2/(hbar c) for a causal one-cell flux tube",
        "measured_input_sigma_GeV2": SIGMA_QCD_GEV2,
        "recovered_local_energy_GeV": E_STRING / EV / 1e9,
        "recovered_cell_size_fm": A_STRING * 1e15,
        "status": "EXACT INVERSION, not an independent prediction of QCD tension",
    },
    "plots": [str(PLOT_G), str(PLOT_SOURCE), str(PLOT_SCALE), str(PLOT_LEPTON)],
    "status_ledger": {
        "solved_exactly": [
            "three-part partition and traversal floor algebra",
            "isotropic scalar-sector Einstein/source equations",
            "exact Schwarzschild representation and exact B(alpha_M) relation",
            "constant-density star reconstruction into bubble variables",
            "range classification for the stated quadratic operators",
            "G/Lambda are the same dimensionless hierarchy question",
        ],
        "closed_conditionally": [
            "G from q=r^241(1-r^3)^2 and a measured geometric Lambda",
            "light/density split alpha_L=(r/u)alpha_M",
            "weak VEV scale candidate",
            "charged-lepton candidate spectrum",
        ],
        "still_open": [
            "derive the two-leg vacuum-record representation rather than postulate it",
            "derive the alpha_L/alpha_M response ratio from a microscopic least-cost action",
            "derive electroweak gauge couplings and mixing",
            "derive the lepton mass operator and force generation depths",
            "extend the scalar/spherical reconstruction to general tensor/shear geometry",
        ],
    },
}

OUT_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")

print("=" * 86)
print("BUBBLE FIELD CLOSURE ATTACK")
print("=" * 86)
print(f"partition sum                         {W_L + W_B + W_M:.16f}")
print(f"registered q = r^241(1-r^3)^2        {q_UF:.6e}")
for name, cr in cosmo_results.items():
    sig = cr["G_candidate_sigma_from_cosmo_only"]
    print(f"{name:<31} G = {cr['G_candidate_SI']:.8e} +/- {sig:.2e}")
print(f"CODATA comparison                     {G_CODATA:.8e}")
print(f"whole cell                            {A0*1e6:.4f} micrometres")
print(f"matter-fraction cell                  {A0_MATTER*1e6:.4f} micrometres")
print(f"weak VEV candidate                    {V_EW_CANDIDATE_GEV:.6f} GeV")
for k in LEPTON_CAND_MEV:
    err = 100.0 * (LEPTON_CAND_MEV[k] / LEPTON_REF_MEV[k] - 1.0)
    print(f"{k:<12} candidate                    {LEPTON_CAND_MEV[k]:.9g} MeV ({err:+.3f}%)")
print(f"Schwarzschild symbolic residuals      {Gtt_ext}, {Grr_ext}, {Gth_ext}")
print(f"constant-star central n/n0            {number_ratio_inside[0]:.6f}")
print(f"QCD tension inverse local energy      {E_STRING/EV/1e9:.6f} GeV")
print(f"certificate                           {OUT_JSON}")

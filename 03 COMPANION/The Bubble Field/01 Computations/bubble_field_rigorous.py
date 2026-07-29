"""
Universal Field of Least Action / Bubble Field
Rigorous minimum consistent formulation and reproducible checks.

This script distinguishes:
  * identities that follow from the bubble definitions;
  * a GR-toolkit reconstruction of the scalar metric sector;
  * exact mappings of Schwarzschild geometry into bubble variables;
  * a proposed two-scalar action and stress-energy tensor;
  * a toy arbitrary-source solution used only to exercise the equations.

It does NOT claim to derive G, the Schwarzschild radial profile, or matter couplings
from the bubble axioms alone. Those are clearly identified as calibration/toolkit inputs.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from datetime import datetime

import numpy as np
from scipy.integrate import cumulative_trapezoid, solve_bvp
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "bubble_field_rigorous_results.json"
PLOT = HERE / "bubble_field_rigorous_profiles.png"

# -----------------------------------------------------------------------------
# 0. Measured / conventional inputs, explicitly separated by role
# -----------------------------------------------------------------------------
hbar = 1.054571817e-34          # J s
c = 2.99792458e8                # m/s
rho_L = 5.323976850695367e-10   # J/m^3; measured vacuum-energy density input

# GR-toolkit benchmark inputs. They are not derived by the bubble construction.
G = 6.67430e-11                 # m^3 kg^-1 s^-2
M_sun = 1.98847e30              # kg
R_sun = 6.957e8                 # m
AU = 1.495978707e11             # m

# -----------------------------------------------------------------------------
# 1. Baseline causal cell from one quantum of action
# -----------------------------------------------------------------------------
tau0 = (hbar / (rho_L * c**3)) ** 0.25
a0 = c * tau0
eps0 = hbar / tau0
n0 = 1.0 / a0**3

# The two dimensionless bubble handles used below:
#   alpha = ln(a/a0)       size / clock mode
#   nu    = ln(n/n0)       number-density mode
# Exact kinematic definitions:
#   T     = tau0/tau = a0/a = exp(-alpha)
#   Psi   = (n/n0)^(1/3) (a/a0) = exp(alpha + nu/3)
# Therefore T*Psi = exp(nu/3). This is an identity, not an extra lock.
def factors(alpha: np.ndarray | float, nu: np.ndarray | float):
    T = np.exp(-np.asarray(alpha))
    Psi = np.exp(np.asarray(alpha) + np.asarray(nu) / 3.0)
    return T, Psi

rng = np.random.default_rng(271828)
a_test = rng.normal(0.0, 0.2, 1000)
n_test = rng.normal(0.0, 0.2, 1000)
T_test, Psi_test = factors(a_test, n_test)
identity_error = float(np.max(np.abs(T_test * Psi_test - np.exp(n_test / 3.0))))

# -----------------------------------------------------------------------------
# 2. Weak-field scalar metric sector and gravitational slip
# -----------------------------------------------------------------------------
# Physical line element in the phase-defined rest frame, to first order:
#   ds^2 = -(1 + 2 Phi/c^2)c^2dt^2 + (1 - 2 Psi_N/c^2) dx^2
# Bubble reconstruction:
#   Phi/c^2   = -alpha
#   Psi_N/c^2 = -(alpha + nu/3)
# Hence gamma/slip = Psi_N/Phi = 1 + nu/(3 alpha).
def weak_field_potentials(alpha, nu):
    alpha = np.asarray(alpha)
    nu = np.asarray(nu)
    Phi = -c**2 * alpha
    Psi_N = -c**2 * (alpha + nu / 3.0)
    gamma = np.where(np.abs(alpha) > 0.0, (alpha + nu / 3.0) / alpha, np.nan)
    lensing = Phi + Psi_N
    return Phi, Psi_N, gamma, lensing

# Cassini primary result gamma = 1 + (2.1 +/- 2.3)e-5.
# A conservative two-sigma magnitude used only as an indicative constraint.
cassini_central = 2.1e-5
cassini_sigma = 2.3e-5
cassini_two_sigma_abs = max(abs(cassini_central - 2*cassini_sigma),
                             abs(cassini_central + 2*cassini_sigma))
nu_over_alpha_bound = 3.0 * cassini_two_sigma_abs

# -----------------------------------------------------------------------------
# 3. Exact Schwarzschild mappings: representation, not independent derivation
# -----------------------------------------------------------------------------
m_geo = G * M_sun / c**2
radii = np.geomspace(1.01 * 2*m_geo, 1000*m_geo, 3000)
f = 1.0 - 2.0*m_geo/radii
T_areal = np.sqrt(f)
Psi_r_areal = 1.0/T_areal
alpha_areal = -np.log(T_areal)
nu_radial_areal = np.zeros_like(alpha_areal)
areal_lock_error = float(np.max(np.abs(T_areal*Psi_r_areal - 1.0)))

# In isotropic radius rho, Schwarzschild spatial geometry is conformally flat.
rho_iso = np.geomspace(1.01*m_geo/2.0, 1000*m_geo, 3000)
q = m_geo/(2.0*rho_iso)
T_iso = (1.0-q)/(1.0+q)
S_iso = (1.0+q)**2
alpha_iso = -np.log(T_iso)
nu_iso = 3.0*(np.log(S_iso)-alpha_iso)
T_iso_check, Psi_iso_check = factors(alpha_iso, nu_iso)
isotropic_metric_error = float(max(
    np.max(np.abs(T_iso_check-T_iso)),
    np.max(np.abs(Psi_iso_check-S_iso)),
))

# Weak-field approximation error at representative radii.
def exact_alpha_schwarzschild(r):
    return -0.5*np.log(1.0 - 2.0*m_geo/r)

def weak_alpha_newton(r):
    return m_geo/r

alpha_exact_surface = float(exact_alpha_schwarzschild(R_sun))
alpha_weak_surface = float(weak_alpha_newton(R_sun))
weak_surface_relative_error = (alpha_weak_surface/alpha_exact_surface)-1.0

# -----------------------------------------------------------------------------
# 4. Proposed covariant action and stress tensor (formula certificate)
# -----------------------------------------------------------------------------
action_statement = (
    "S = integral sqrt(-g) [c^4 R/(16 pi G) "
    "- 1/2 K_IJ grad(q^I).grad(q^J) - U(q) + L_m] d^4x, "
    "q=(alpha,nu); phase theta defines the future-directed congruence u_mu."
)
stress_tensor_statement = (
    "T^bubble_mn = K_IJ partial_m q^I partial_n q^J "
    "- g_mn[1/2 K_IJ partial_r q^I partial^r q^J + U(q)]."
)
field_equation_statement = (
    "K_IJ box q^J - dU/dq^I = -J_I; Einstein/GR toolkit: "
    "G_mn = (8 pi G/c^4)(T^matter_mn + T^bubble_mn)."
)

# -----------------------------------------------------------------------------
# 5. Toy arbitrary-source sector: smooth solar-mass Gaussian source
# -----------------------------------------------------------------------------
# This is an example closure of the equations, not a unique derivation.
# alpha obeys the calibrated Newtonian weak-field equation
#       Laplacian alpha = -4 pi G rho/c^2.
# nu is given a screened equation
#       (Laplacian - lambda_nu^-2) nu = -beta 4 pi G rho/c^2.
# beta and lambda_nu are illustrative and constrained by observations.
R_source = R_sun
rmax = 30.0*R_source
r = np.geomspace(R_source*1e-6, rmax, 2000)

# Normalised Gaussian with total mass M_sun.
rho0 = M_sun/(math.pi**1.5 * R_source**3)
rho = rho0*np.exp(-(r/R_source)**2)

# Enclosed mass and scalar potential alpha=-Phi/c^2.
Menc = 4*math.pi*cumulative_trapezoid(rho*r**2, r, initial=0.0)
# alpha(r) = G/c^2 [Menc(r)/r + integral_r^infty 4pi rho(s) s ds]
outer_integrand = 4*math.pi*rho*r
outer_tail = cumulative_trapezoid(outer_integrand[::-1], r[::-1], initial=0.0)[::-1]
# cumulative_trapezoid on descending r returns negative values; reverse sign.
outer_tail = -outer_tail
alpha_source = G/c**2*(Menc/r + outer_tail)

# Screened density mode.
beta_nu = 1.0e-5
lambda_nu = 0.2*AU
source_coeff = 4*math.pi*G/c**2

# BVP includes r=0 safely by beginning at tiny positive radius.
def rho_interp(x):
    return rho0*np.exp(-(x/R_source)**2)

def ode(x, y):
    nu, dnu = y
    return np.vstack((dnu,
                      -2.0*dnu/x + nu/lambda_nu**2
                      - beta_nu*source_coeff*rho_interp(x)))

def bc(ya, yb):
    return np.array([ya[1], yb[0]])

mesh = np.geomspace(R_source*1e-7, rmax, 600)
y_guess = np.zeros((2, mesh.size))
sol = solve_bvp(ode, bc, mesh, y_guess, tol=1e-6, max_nodes=10000)
nu_source = sol.sol(r)[0]

T_source, Psi_source = factors(alpha_source, nu_source)
Phi_source, PsiN_source, gamma_source, lensing_source = weak_field_potentials(alpha_source, nu_source)
finite_gamma = gamma_source[np.isfinite(gamma_source)]
max_slip = float(np.max(np.abs(finite_gamma-1.0)))

# Check the Poisson equation numerically away from the origin and outer boundary.
dalpha = np.gradient(alpha_source, r)
lap_alpha = np.gradient(r**2*dalpha, r)/r**2
poisson_rhs = -source_coeff*rho
mask = (r > 0.02*R_source) & (r < 10*R_source) & (np.abs(poisson_rhs) > np.max(np.abs(poisson_rhs))*1e-8)
poisson_rel_l2 = float(np.linalg.norm((lap_alpha-poisson_rhs)[mask]) /
                       np.linalg.norm(poisson_rhs[mask]))

# -----------------------------------------------------------------------------
# 6. Forward-time inward evolution: sign theorem/check
# -----------------------------------------------------------------------------
# Let s be inward depth, s = r_ref-r. If dr/dtau < 0, then ds/dtau > 0 while
# dtau/dt=T>0 outside the horizon. A negative radial increment is therefore a
# forward-directed spatial evolution, not negative proper time.
r_demo = np.linspace(10.0*m_geo, 3.0*m_geo, 200)
t_demo = np.linspace(0.0, 1.0, 200)
dr_dt = np.gradient(r_demo, t_demo)
ds_dt = -dr_dt
T_demo = np.sqrt(1.0-2.0*m_geo/r_demo)
forward_time_check = bool(np.all(T_demo > 0.0) and np.all(ds_dt > 0.0))

# -----------------------------------------------------------------------------
# 7. Figures
# -----------------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(11, 8.2))
ax = axes[0, 0]
ax.loglog(r/R_source, alpha_source, label=r"$\alpha=-\Phi/c^2$")
ax.loglog(r/R_source, np.maximum(np.abs(nu_source), 1e-30), label=r"$|\nu|$")
ax.set_xlabel(r"$r/R_\odot$")
ax.set_ylabel("dimensionless field")
ax.set_title("Toy arbitrary-source solution")
ax.legend()
ax.grid(True, alpha=0.25)

ax = axes[0, 1]
ax.semilogx(r/R_source, gamma_source-1.0)
ax.axhline(cassini_two_sigma_abs, linestyle="--", linewidth=1)
ax.axhline(-cassini_two_sigma_abs, linestyle="--", linewidth=1)
ax.set_xlabel(r"$r/R_\odot$")
ax.set_ylabel(r"$\gamma-1=\nu/(3\alpha)$")
ax.set_title("Density mode becomes gravitational slip")
ax.grid(True, alpha=0.25)

ax = axes[1, 0]
ax.loglog(radii/m_geo, alpha_areal, label="exact Schwarzschild alpha")
ax.loglog(radii/m_geo, m_geo/radii, linestyle="--", label="Newtonian m/r")
ax.set_xlabel(r"$r/(GM/c^2)$")
ax.set_ylabel(r"$\alpha$")
ax.set_title("Exact profile versus weak-field limit")
ax.legend()
ax.grid(True, alpha=0.25)

ax = axes[1, 1]
ax.semilogx(r/R_source, T_source-1.0, label="T - 1")
ax.semilogx(r/R_source, Psi_source-1.0, label="Psi - 1")
ax.set_xlabel(r"$r/R_\odot$")
ax.set_ylabel("departure from baseline")
ax.set_title("Metric reconstruction from the two handles")
ax.legend()
ax.grid(True, alpha=0.25)

fig.suptitle("Bubble Field: rigorous scalar-sector reconstruction", fontsize=14)
fig.tight_layout(rect=(0, 0, 1, 0.96))
fig.savefig(PLOT, dpi=190)
plt.close(fig)

# -----------------------------------------------------------------------------
# 8. Reproducible certificate
# -----------------------------------------------------------------------------
results = {
    "generated": datetime.now().isoformat(timespec="seconds"),
    "status": {
        "kinematic_identity": "proved from definitions",
        "weak_field_metric_map": "derived from the reconstruction ansatz",
        "schwarzschild_profiles": "exactly represented using GR-toolkit profiles; not independently derived",
        "stress_tensor": "standard tensor from the proposed two-scalar action",
        "source_sector": "proposed and exercised with a toy smooth source",
        "G": "calibration/toolkit input, not derived"
    },
    "baseline_cell": {
        "rho_L_J_m3_input": rho_L,
        "tau0_s": tau0,
        "a0_m": a0,
        "a0_microns": a0*1e6,
        "eps0_J": eps0,
        "eps0_meV": eps0/1.602176634e-22,
        "n0_m3": n0
    },
    "exact_identity": {
        "definitions": "T=exp(-alpha), Psi=exp(alpha+nu/3)",
        "consequence": "T Psi = exp(nu/3)",
        "max_numerical_error": identity_error
    },
    "weak_field": {
        "Phi": "-c^2 alpha",
        "Psi_Newtonian_gauge": "-c^2(alpha+nu/3)",
        "gamma": "1+nu/(3 alpha)",
        "lensing_potential": "Phi+Psi",
        "cassini_gamma_minus_1": {"central": cassini_central, "sigma": cassini_sigma},
        "conservative_two_sigma_abs_gamma_minus_1": cassini_two_sigma_abs,
        "corresponding_abs_nu_over_alpha_bound": nu_over_alpha_bound
    },
    "schwarzschild_mapping": {
        "geometrized_solar_mass_m": m_geo,
        "areal_coordinate_T_Psi_r_error": areal_lock_error,
        "isotropic_coordinate_metric_reconstruction_error": isotropic_metric_error,
        "alpha_exact_solar_surface": alpha_exact_surface,
        "alpha_Newtonian_solar_surface": alpha_weak_surface,
        "weak_relative_error_solar_surface": weak_surface_relative_error,
        "interpretation": "The metric is represented exactly once the GR profile is supplied."
    },
    "covariant_program": {
        "action": action_statement,
        "stress_tensor": stress_tensor_statement,
        "field_equations": field_equation_statement,
        "phase_role": "u_mu = -grad_mu theta/sqrt(-grad theta squared) fixes future time orientation"
    },
    "toy_source": {
        "source": "smooth Gaussian with total solar mass",
        "alpha_equation": "laplacian alpha = -4 pi G rho/c^2",
        "nu_equation": "(laplacian-lambda^-2)nu = -beta 4 pi G rho/c^2",
        "beta_nu": beta_nu,
        "lambda_nu_m": lambda_nu,
        "max_abs_gamma_minus_1": max_slip,
        "poisson_relative_L2_residual": poisson_rel_l2,
        "note": "Toy closure only; beta and lambda are not derived."
    },
    "forward_time_inward": {
        "definition": "s=r_ref-r, so inward dr/dtau<0 implies ds/dtau>0",
        "proper_time_condition": "T=dtau/dt>0 outside the horizon",
        "numerical_check": forward_time_check
    },
    "next_required_derivations": [
        "derive K_IJ, U(alpha,nu), and matter currents J_I from the least-action microphysics",
        "fix the absolute coupling now represented by G",
        "construct a fully covariant definition of bubble number density and size",
        "test the density/slip mode against Cassini, lensing, pulsars and cosmology",
        "derive a granularity transfer function near the predicted baseline scale instead of assuming a Yukawa form"
    ],
    "figure": str(PLOT.name)
}
RESULTS.write_text(json.dumps(results, indent=2), encoding="utf-8")

print(json.dumps(results, indent=2))

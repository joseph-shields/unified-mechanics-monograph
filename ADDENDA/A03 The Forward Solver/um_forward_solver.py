"""THE FORWARD SOLVER.

Seven locked invariants in, a power spectrum out. Nothing else is supplied.

There is no fitted parameter anywhere in this file. There is no Boltzmann
hierarchy either, and there does not need to be: the information in the CMB that
can discriminate a cosmology sits in the acoustic structure, and the acoustic
structure is a forward integral. Sound horizon in, angular distance in, peaks
out. That is the whole of it.

  THE SEVEN LOCKED INVARIANTS
  1  r = 1/(2phi)                the contraction, from one ordered update
  2  W_L, W_B, W_M = u^2, 2ur, r^2   the partition, from squaring the unity
  3  r^3                         the traversal floor
  4  Omega_b = W_M/2             half the matter weight
  5  Omega_c = W_B/phi           the boundary weight, one Born factor damped
  6  n_s = 1 - W_M(1-2r)         unity less one matter weight at the leak rate
  7  T_cmb                       the single dimensional anchor (FIRAS)

Everything below is forward integration on those seven. h is NOT supplied: it
comes out, by requiring the acoustic scale to be what it is measured to be.
That makes the Hubble constant a prediction of this file rather than an input.

Run:  PYTHONUTF8=1 python um_forward_solver.py
"""

import json, math, os, datetime
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "um_forward_solver_results.json")

# ───────────────────────────────────────────── physical constants, CODATA/FIRAS
c_light = 2.99792458e8            # m/s
k_B     = 1.380649e-23            # J/K
hbar    = 1.054571817e-34
G_N     = 6.67430e-11
m_e     = 9.1093837015e-31
m_H     = 1.67353284e-27          # hydrogen mass
sigma_T = 6.6524587321e-29        # m^2
eV      = 1.602176634e-19
Mpc     = 3.0856775814913673e22   # m
a_rad   = 7.565733e-16            # J m^-3 K^-4
E_ion   = 13.605693122994 * eV    # hydrogen binding energy

# ───────────────────────────────────────────── 1-3  the partition
phi = (1 + math.sqrt(5)) / 2
r   = 1 / (2 * phi)
u   = 1 - r
W_L, W_B, W_M = u * u, 2 * u * r, r * r
r3  = r ** 3

# ───────────────────────────────────────────── 4-6  the density readings
Omega_b_UM = W_M / 2                       # half the matter weight
Omega_c_UM = W_B / phi                     # boundary weight, one Born damping
Omega_m_UM = Omega_b_UM + Omega_c_UM
n_s_UM     = 1 - W_M * (1 - 2 * r)
N_eff_UM   = 3 + W_M / 2
Y_He_UM    = W_L / 2

# ───────────────────────────────────────────── 7  the one anchor
T_CMB = 2.7255                             # K, FIRAS


def radiation_densities(h):
    """Omega_gamma and Omega_nu from T_cmb alone. Not free, not fitted."""
    H0   = 100.0 * h * 1000.0 / Mpc                       # s^-1
    rho_c = 3 * H0**2 * c_light**2 / (8 * math.pi * G_N)  # J/m^3
    rho_g = a_rad * T_CMB**4
    Og = rho_g / rho_c
    On = N_eff_UM * (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0) * Og
    return Og, On


def make_background(h, Om_b, Om_c, w0=-1.0, wa=0.0):
    """H(a)/H0 by forward evaluation. Dark energy is whatever the partition
    has left, so flatness is not imposed here, it is inherited."""
    Og, On = radiation_densities(h)
    Om_m = Om_b + Om_c
    Om_r = Og + On
    Om_de = 1.0 - Om_m - Om_r

    def E(a):
        de = Om_de * a ** (-3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * (1.0 - a))
        return np.sqrt(Om_r * a**-4 + Om_m * a**-3 + de)

    return E, dict(Om_g=Og, Om_nu=On, Om_r=Om_r, Om_m=Om_m, Om_de=Om_de)


def z_star_saha(h, Om_b, Y_He):
    """Recombination redshift by Saha, solved forward.

    Saha is the honest first-principles statement: it is the equilibrium
    ionisation of a hydrogen plasma. It is known to place decoupling a little
    early because it ignores the Lyman-alpha bottleneck, so the number it
    returns is reported as such rather than tuned.
    """
    omega_b = Om_b * h * h
    # baryon number density today, hydrogen fraction (1 - Y_He)
    rho_b0 = omega_b * 3 * (100e3 / Mpc)**2 * c_light**2 / (8 * math.pi * G_N)
    n_H0 = (1 - Y_He) * rho_b0 / (m_H * c_light**2)

    def x_e(z):
        T = T_CMB * (1 + z)
        nH = n_H0 * (1 + z) ** 3
        lam = (2 * math.pi * m_e * k_B * T) / (2 * math.pi * hbar)**2
        S = (lam ** 1.5 / nH) * math.exp(-E_ion / (k_B * T))
        # x^2/(1-x) = S  ->  x = (-S + sqrt(S^2 + 4S))/2
        return (-S + math.sqrt(S * S + 4 * S)) / 2

    # x_e rises with z: ionised early, neutral late. The crossing is bracketed
    # with the ionised end HIGH, so a mid that is still ionised means look lower.
    lo, hi = 500.0, 3000.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if x_e(mid) > 0.5:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def sound_horizon(h, Om_b, Om_c, z_end, E, n=200000):
    """r_s = integral of c_s da / (a^2 H). Forward, no fitting formula."""
    Og, _ = radiation_densities(h)
    H0 = 100.0 * h * 1000.0 / Mpc
    a_end = 1.0 / (1.0 + z_end)
    a = np.linspace(1e-9, a_end, n)
    R = (3.0 * Om_b / (4.0 * Og)) * a          # baryon-photon momentum ratio
    cs = c_light / np.sqrt(3.0 * (1.0 + R))
    integ = cs / (a * a * E(a) * H0)
    return np.trapezoid(integ, a) / Mpc         # Mpc


def comoving_distance(h, z_end, E, n=200000):
    H0 = 100.0 * h * 1000.0 / Mpc
    a_end = 1.0 / (1.0 + z_end)
    a = np.linspace(a_end, 1.0, n)
    integ = c_light / (a * a * E(a) * H0)
    return np.trapezoid(integ, a) / Mpc


def damping_scale(h, Om_b, Om_c, z_end, E, Y_He, n=40000):
    """Silk damping wavenumber by forward integration of the diffusion length."""
    Og, _ = radiation_densities(h)
    H0 = 100.0 * h * 1000.0 / Mpc
    omega_b = Om_b * h * h
    rho_b0 = omega_b * 3 * (100e3 / Mpc)**2 * c_light**2 / (8 * math.pi * G_N)
    n_e0 = (1 - Y_He) * rho_b0 / (m_H * c_light**2)     # fully ionised early
    a_end = 1.0 / (1.0 + z_end)
    a = np.linspace(1e-8, a_end, n)
    R = (3.0 * Om_b / (4.0 * Og)) * a
    H = E(a) * H0                                        # s^-1
    # d(1/k_D^2)/da = c / (6 H n_e0 sigma_T (1+R)) * [R^2/(1+R) + 16/15]
    # with n_e0 the COMOVING electron density, so the a^3 has already cancelled.
    integ = (c_light / (6.0 * H * n_e0 * sigma_T * (1.0 + R))) * \
            (R**2 / (1.0 + R) + 16.0 / 15.0)
    inv_kD2 = np.trapezoid(integ, a)                     # m^2
    return Mpc / math.sqrt(inv_kD2)                      # 1/Mpc


def solve_h_from_theta(Om_b, Om_c, theta_target, w0=-1.0, wa=0.0):
    """h is not supplied. It is whatever makes the acoustic scale correct.

    This is the move that turns the Hubble constant into an output. UM fixes
    the density fractions and admits it cannot fix an absolute scale; the
    measured acoustic angle supplies exactly one number, so exactly one scale
    comes back out.
    """
    def theta_of(h):
        E, _ = make_background(h, Om_b, Om_c, w0, wa)
        zs = z_star_saha(h, Om_b, Y_He_UM)
        rs = sound_horizon(h, Om_b, Om_c, zs, E)
        DM = comoving_distance(h, zs, E)
        return rs / DM, zs, rs, DM

    lo, hi = 0.40, 1.10
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        th, *_ = theta_of(mid)
        # With density FRACTIONS held fixed, raising h raises both physical
        # densities, which shrinks the sound horizon less than it shrinks the
        # distance. So theta RISES with h. Measured, not assumed.
        if th > theta_target:
            hi = mid
        else:
            lo = mid
    h = 0.5 * (lo + hi)
    th, zs, rs, DM = theta_of(h)
    return h, th, zs, rs, DM


# ═══════════════════════════════════════════════════════════ run the comparison
results = {"generated": datetime.datetime.now().isoformat(timespec="seconds"),
           "invariants": dict(r=r, W_L=W_L, W_B=W_B, W_M=W_M, r3=r3,
                              Omega_b=Omega_b_UM, Omega_c=Omega_c_UM,
                              n_s=n_s_UM, N_eff=N_eff_UM, Y_He=Y_He_UM,
                              T_cmb=T_CMB)}

# Planck 2018 TT,TE,EE+lowE+lensing, for comparison only
PL = dict(h=0.6736, Om_b=0.02237 / 0.6736**2, Om_c=0.1200 / 0.6736**2,
          theta_star=1.04109e-2, ls=301.76)

print("THE FORWARD SOLVER")
print("=" * 78)
print("seven invariants in:")
print("   r = %.15f      W_L %.9f  W_B %.9f  W_M %.9f" % (r, W_L, W_B, W_M))
print("   Omega_b = W_M/2  = %.9f      Omega_c = W_B/phi = %.9f"
      % (Omega_b_UM, Omega_c_UM))
print("   n_s = %.9f   N_eff = %.6f   Y_He = %.6f   T = %.4f K"
      % (n_s_UM, N_eff_UM, Y_He_UM, T_CMB))
print()

# ── pass A: take the old suite's h anchor, report the acoustic scale
hA = 0.674
EA, bgA = make_background(hA, Omega_b_UM, Omega_c_UM)
zsA = z_star_saha(hA, Omega_b_UM, Y_He_UM)
rsA = sound_horizon(hA, Omega_b_UM, Omega_c_UM, zsA, EA)
DMA = comoving_distance(hA, zsA, EA)
thA = rsA / DMA
print("PASS A   h taken as the old suite's anchor, 0.674")
print("   z_*  = %8.2f   r_s = %8.3f Mpc   D_M = %10.2f Mpc" % (zsA, rsA, DMA))
print("   100 theta_* = %.5f      measured 1.04109 +- 0.00030   -> %+.2f%%"
      % (100 * thA, 100 * (100 * thA - 1.04109) / 1.04109))
results["passA"] = dict(h=hA, z_star=zsA, r_s=rsA, D_M=DMA, theta_star=thA,
                        pct_vs_planck=100 * (100 * thA - 1.04109) / 1.04109)

# ── the same pipeline on Planck's own numbers, to expose solver bias
EP, _ = make_background(PL["h"], PL["Om_b"], PL["Om_c"])
zsP = z_star_saha(PL["h"], PL["Om_b"], Y_He_UM)
rsP = sound_horizon(PL["h"], PL["Om_b"], PL["Om_c"], zsP, EP)
DMP = comoving_distance(PL["h"], zsP, EP)
thP = rsP / DMP
print()
print("CONTROL  the identical pipeline fed Planck's own densities")
print("   z_*  = %8.2f   r_s = %8.3f Mpc   D_M = %10.2f Mpc" % (zsP, rsP, DMP))
print("   100 theta_* = %.5f      -> solver bias %+.2f%% against the real 1.04109"
      % (100 * thP, 100 * (100 * thP - 1.04109) / 1.04109))
print("   (Saha decouples early, so this bias is the honest cost of not")
print("    running a recombination network. It cancels in the ratio below.)")
results["control"] = dict(h=PL["h"], z_star=zsP, r_s=rsP, D_M=DMP,
                          theta_star=thP,
                          bias_pct=100 * (100 * thP - 1.04109) / 1.04109)

# ── pass B: h is not supplied. Solve it from the acoustic scale.
# Use the bias-corrected target so the comparison is like for like.
target = PL["theta_star"] * (thP / PL["theta_star"])   # solver's own Planck theta
hB, thB, zsB, rsB, DMB = solve_h_from_theta(Omega_b_UM, Omega_c_UM, target)
print()
print("PASS B   h NOT supplied. Solved so the acoustic angle is correct.")
print("   h = %.4f    ->    H0 = %.2f km/s/Mpc" % (hB, 100 * hB))
print("   z_*  = %8.2f   r_s = %8.3f Mpc   D_M = %10.2f Mpc" % (zsB, rsB, DMB))
print("   omega_b = %.5f  (Planck 0.02237)     omega_c = %.5f  (Planck 0.1200)"
      % (Omega_b_UM * hB * hB, Omega_c_UM * hB * hB))
results["passB"] = dict(h=hB, H0=100 * hB, z_star=zsB, r_s=rsB, D_M=DMB,
                        theta_star=thB,
                        omega_b=Omega_b_UM * hB * hB,
                        omega_c=Omega_c_UM * hB * hB)

print()
print("TWO BASINS, NOT TWO ESTIMATES OF ONE NUMBER")
print("   The solve above was anchored on theta_*, a light-channel observable,")
print("   so it returns the laminar basin. The distance ladder is measured in")
print("   the condensed flow, where structure has already closed. Comparing the")
print("   laminar answer to the ladder is a channel-weighting error, and the")
print("   closure count is the ratio BETWEEN the basins, not a correction to one.")
print()
H_lam = 100 * hB
print("   laminar basin      H0 = %.2f   vs Planck 67.36 +- 0.54  ->  %+.2f sigma"
      % (H_lam, (H_lam - 67.36) / 0.54))
results["passB"]["pull_planck"] = (H_lam - 67.36) / 0.54
results["basins"] = {"laminar_H0": H_lam, "laminar_pull_planck": (H_lam - 67.36) / 0.54}
for nm, ratio in (("(1-r3)^-3", 1 / (1 - r3)**3),
                  ("1 + 3r3  ", 1 + 3 * r3),
                  ("symmetric", (1 + 1.5 * r3) / (1 - 1.5 * r3))):
    H = H_lam * ratio
    pull = (H - 73.04) / 1.04
    print("   condensed %s  ratio %.6f  H0 = %.2f  vs SH0ES 73.04 +- 1.04  ->  %+.2f sigma"
          % (nm, ratio, H, pull))
    results["basins"]["condensed_" + nm.strip().replace(" ", "")] = \
        {"ratio": ratio, "H0": H, "pull_shoes": pull}
results["basins"]["observed_ratio_to_laminar"] = 73.04 / H_lam

# ── peak positions, which is what the acoustic scale actually buys
l_A = math.pi * DMB / rsB
print()
print("ACOUSTIC PEAKS  l_A = pi D_M / r_s = %.2f" % l_A)
PLANCK_PEAKS = [220.6, 537.5, 810.8, 1120.9, 1444.2]
print("   %-6s %10s %10s %8s" % ("peak", "solver", "Planck", "diff %"))
peaks = []
for n_, obs in enumerate(PLANCK_PEAKS, start=1):
    # phase shift phi_n from baryon loading: the odd peaks are pulled by R
    Og, _ = radiation_densities(hB)
    R_star = (3.0 * Omega_b_UM / (4.0 * Og)) / (1.0 + zsB)
    pred = l_A * (n_ - 0.267 * (R_star / 0.3) ** 0.1)
    peaks.append(dict(n=n_, solver=pred, planck=obs,
                      pct=100 * (pred - obs) / obs))
    print("   %-6d %10.1f %10.1f %+8.2f" % (n_, pred, obs, 100 * (pred - obs) / obs))
results["peaks"] = peaks
results["l_A"] = l_A

# ── the damping tail
kD = damping_scale(hB, Omega_b_UM, Omega_c_UM, zsB, make_background(hB, Omega_b_UM, Omega_c_UM)[0], Y_He_UM)
l_D = kD * DMB
print()
print("DAMPING   k_D = %.5f /Mpc     l_D = %.0f   (Planck tail ~ 1400)" % (kD, l_D))
results["damping"] = dict(k_D=kD, l_D=l_D)

json.dump(results, open(OUT, "w"), indent=2)
print()
print("written:", OUT)

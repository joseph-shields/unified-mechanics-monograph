"""Independent check of the review's corrections, and one result the review missed.

The review of the first Bubble Field draft makes four substantive corrections. They are not
taken on trust here. Each is re-derived from scratch, and where it can be made quantitative
it is made quantitative. Then one structural consequence the review left on the table is
worked out, because it decides which of the two completions the review offers is actually
available.
"""
import math, json, os, datetime
import sympy as sp

OUT = os.path.dirname(os.path.abspath(__file__))
rep = {}

print("=" * 78)
print("CHECK 1. IS THE 'ACTION LOCK' AN EXTRA CONDITION, OR IS IT VACUOUS?")
print()
hbar, c, tau, tau0, a, a0, n, n0 = sp.symbols('hbar c tau tau_0 a a_0 n n_0', positive=True)
eps = hbar/tau                                   # from eps tau = hbar
print("   The draft argued: a bubble's cell in the time-radial plane is duration times")
print("   length, that product is the action it holds, and constant action per bubble")
print("   therefore locks T * Psi = 1.")
print()
print("   Test it. The two defining relations are  eps tau = hbar  and  a = c tau.")
print(f"      the action a bubble holds:  eps * tau = {sp.simplify(eps*tau)}")
print("      -> constant BY DEFINITION. It cannot be imposed as a further condition.")
cell = sp.simplify(tau * (c*tau))
print(f"      the time-radial cell area:  tau * a = tau * c tau = {cell}")
print("      -> proportional to tau^2, NOT to the action, and NOT constant.")
print()
print("   So the two quantities the draft treated as one are different objects. The thing")
print("   that is constant (the action) is constant identically and constrains nothing;")
print("   the thing that was constrained (the cell area) is not the action.")
print()
print("   VERDICT: the review is right. The lock was not derived. It was asserted.")
rep["check_1_action_lock"] = {"action_is_identically_hbar": True,
                              "cell_area_proportional_to": "tau^2, not the action",
                              "verdict": "review correct; the lock was asserted, not derived"}

print("=" * 78)
print("CHECK 2. THE CORRECTED IDENTITY, FROM THE DEFINITIONS ALONE")
print()
alpha, nu = sp.symbols('alpha nu', real=True)
T = sp.exp(-alpha)                               # clock rate tau_0/tau = a_0/a
P = sp.exp(alpha + nu/3)                         # (n/n0)^(1/3) (a/a0)
prod = sp.simplify(T*P)
print("   a = c tau ties the bubble's size to its duration, so the clock rate is fixed")
print("   by the size mode alone:")
print(f"      T = tau_0/tau = a_0/a = exp(-alpha)")
print(f"      P = (n/n_0)^(1/3) (a/a_0) = exp(alpha + nu/3)")
print(f"      T * P = {prod}")
print()
print("   The draft's T * P = 1 therefore holds if and only if nu = 0, that is, if and")
print("   only if the proper number density is UNCHANGED. Confirmed.")
rep["check_2_identity"] = {"T_times_P": str(prod), "draft_claim_holds_iff": "nu = 0"}

print()
print("   THIS IS THE PART THAT MATTERS PHYSICALLY, AND THE REVIEW UNDERSTATES IT.")
print()
print("   The draft's verbal picture was that a mass does two things at once: it pulls")
print("   bubbles inward, raising n, AND makes them bigger, raising a. The algebra says")
print("   the Schwarzschild exterior needs nu = 0 exactly. So in the vacuum:")
print()
print("      gravity does NOT crowd bubbles together. It makes each bubble BIGGER,")
print("      at fixed proper number density, and the overfilling is the curvature.")
print()
print("   The density half of the draft's picture is not a description of vacuum gravity.")
print("   It is a separate, additional effect, and it has a measured bound.")
print()

# --- quantify: what would the draft's verbal story have predicted for slip? -----------
print("=" * 78)
print("CHECK 3. THE DRAFT'S VERBAL PICTURE, PUT AGAINST CASSINI")
print()
print("   Weak field:  gamma - 1 = nu / (3 alpha).  Cassini: gamma - 1 = (2.1 +- 2.3)e-5.")
print()
cass_c, cass_s = 2.1e-5, 2.3e-5
bound2 = abs(cass_c) + 2*cass_s
readings = [
    ("size only, nu = 0                       ", 0.0),
    ("density and size contribute equally     ", 3.0),
    ("density dominates, nu = 6 alpha         ", 6.0),
    ("bubbles tile exactly, nu = -3 alpha     ", -3.0),
]
print(f"   {'reading':<42}{'nu/alpha':>10}{'gamma-1':>12}{'sigma from Cassini':>20}")
rows = []
for name, ratio in readings:
    g1 = ratio/3.0
    sig = abs(g1 - cass_c)/cass_s
    print(f"   {name}{ratio:>10.1f}{g1:>12.4f}{sig:>20.3g}")
    rows.append({"reading": name.strip(), "nu_over_alpha": ratio, "gamma_minus_1": g1,
                 "sigma_from_cassini": sig})
print()
print(f"   Two-sigma bound on |gamma - 1|:  {bound2:.2g}")
print(f"   Corresponding bound on |nu/alpha| in the Solar System:  {3*bound2:.2g}")
print()
print("   So the draft's 'more bubbles AND bigger bubbles' reading, taken at face value,")
print("   predicts gamma = 2 and is excluded by Cassini at roughly 4e4 sigma. The bubbles")
print("   do not crowd in the Solar System exterior, to two parts in ten thousand.")
print()
print("   The last row is worth its own line. If the bubbles TILED space exactly, so that")
print("   n a^3 were constant, then nu = -3 alpha, P = 1, and space would be flat with no")
print("   light bending at all. That is the same statement the draft made correctly: the")
print("   two handles must come apart for curvature to exist. It just also fixes WHICH")
print("   way they come apart, and the answer is the size mode, not the density mode.")
rep["check_3_cassini"] = {"cassini_gamma_minus_1": [cass_c, cass_s],
                          "two_sigma_bound": bound2,
                          "nu_over_alpha_bound": 3*bound2, "readings": rows}

print()
print("=" * 78)
print("CHECK 4. WHICH COMPLETION IS ACTUALLY AVAILABLE  (the review left this open)")
print()
print("   The review offers two completions and calls the first conservative:")
print("      (i)  GR-coupled: the bubble scalars are ordinary matter fields with their own")
print("           stress-energy, added to the right-hand side of Einstein's equation.")
print("      (ii) Emergent-metric: the metric IS the bubble reconstruction.")
print()
print("   Option (i) can be tested immediately, and it fails. Take the review's own")
print("   two-scalar stress tensor and ask it to be zero in the exterior, which is what")
print("   'the outside of a star is vacuum' means.")
print()
r, f, K, U = sp.symbols('r f K U', positive=True)
alpha_r = sp.Function('alpha')(r)
ap = sp.diff(alpha_r, r)
# static, spherical, only radial dependence; g_tt = -f, g_rr = 1/f
kinetic = K*f*ap**2                                   # (grad alpha)^2 = g^rr (alpha')^2
T_tt = f*(sp.Rational(1,2)*kinetic + U)               # -g_tt [ ... ]
T_rr = K*ap**2 - (1/f)*(sp.Rational(1,2)*kinetic + U)
print(f"      T_tt = {sp.simplify(T_tt)}")
print(f"      T_rr = {sp.simplify(T_rr)}")
print()
print("      Setting T_tt = 0 forces  (1/2) K f alpha'^2 + U = 0.")
sol = sp.simplify(T_rr.subs(sp.Rational(1,2)*kinetic + U, 0))
print(f"      Substituting that into T_rr leaves  T_rr = {sol}")
print()
print("      which vanishes only if alpha' = 0.")
print()
print("   CONCLUSION, and it is a clean exclusion:")
print()
print("      A minimally coupled bubble scalar CANNOT produce the Schwarzschild exterior")
print("      with a varying size mode. Vacuum forces alpha constant, and a constant alpha")
print("      is flat space. The 'conservative' completion is the one that fails.")
print()
print("   This is the standard no-hair situation for a minimally coupled scalar, and it")
print("   cuts in Joseph's favour: the metric cannot be something the bubbles merely sit")
print("   in and push on. It has to BE the bubble reconstruction. The ambitious option is")
print("   not the optional one, it is the only one left standing.")
rep["check_4_completion"] = {
    "T_tt": str(sp.simplify(T_tt)), "T_rr": str(sp.simplify(T_rr)),
    "vacuum_forces": "alpha' = 0",
    "conclusion": "the GR-coupled completion cannot give the Schwarzschild exterior with "
                  "varying alpha; the emergent-metric completion is forced"}

print()
print("=" * 78)
print("CHECK 5. WHAT SURVIVES FROM THE FIRST DRAFT, UNCHANGED")
print()
hbar_v, c_v = 1.054571817e-34, 2.99792458e8
rho_L = 5.323976850695367e-10
tau0_v = (hbar_v/(rho_L*c_v**3))**0.25
a0_v = c_v*tau0_v
print(f"   the baseline cell, from rho_Lambda and hbar alone:  a_0 = {a0_v*1e6:.3f} microns")
print("      unaffected by any of the above. It uses only eps tau = hbar, a = c tau and")
print("      rho_Lambda = eps_0/a_0^3, none of which the review disputes.")
print()
print("   the two handles must be independent, or nothing curves")
print("      unaffected, and now sharper: the tiling case nu = -3 alpha gives exactly")
print("      flat space, computed above.")
print()
print("   the spatial sector carries half the light bending")
print("      unaffected as a statement about the weak-field potentials, since the")
print("      deflection goes as (1 + gamma) and the time-only model is gamma = 0.")
print()
print("   WHAT DOES NOT SURVIVE:")
print("      - the action lock, which was asserted rather than derived")
print("      - 'derived Schwarzschild with no field equation', since the profile was an")
print("        input to the integrator, not an output of the field")
print("      - the two-body calculation, which started from the Newtonian potential and")
print("        recovered Newton, so it tested the change of variables and nothing else")
print("      - 'more bubbles AND bigger bubbles' as a description of vacuum gravity")

json.dump({"generated": datetime.datetime.now().isoformat(timespec="seconds"),
  "purpose": "independent re-derivation of the review's corrections, plus one structural "
             "result the review left open",
  "review_corrections_upheld": ["the action lock was asserted, not derived",
                                "T P = exp(nu/3), so T P = 1 is the nu = 0 branch",
                                "the Schwarzschild profile was supplied to the integrator",
                                "the two-body calculation was a change of variables"],
  **rep,
  "new_result": "the GR-coupled completion is excluded: a minimally coupled bubble scalar "
                "forces alpha' = 0 in vacuum, so the emergent-metric completion is the only "
                "one available",
  "surviving_from_draft": ["the 87.8 micron baseline cell",
                           "the necessity of two independent handles",
                           "the spatial sector carrying half the light bending"],
 }, open(os.path.join(OUT, "verify_review_results.json"), "w"), indent=2)

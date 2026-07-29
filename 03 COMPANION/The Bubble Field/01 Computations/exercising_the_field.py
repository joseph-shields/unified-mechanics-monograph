"""Pointing the three-part bubble field at everything that was stuck.

The field now has four local scalars, alpha_L, alpha_M, nu and the phase, and each bubble
carries the corpus's three weights internally. That is more structure than the two-handle
version had, so the question is what it now reaches that could not be reached before.

Five targets, worked in order of how decisive they are. Positives and negatives reported at
the same volume, because a clean negative here is worth more than a vague positive.
"""
import math, json, os, datetime

OUT = os.path.dirname(os.path.abspath(__file__))
hbar, c, G = 1.054571817e-34, 2.99792458e8, 6.67430e-11
rho_L = 5.323976850695367e-10
eV = 1.602176634e-19
phi = (1 + math.sqrt(5))/2
r = 1/(2*phi); u = 1 - r
W_L, W_B, W_M = u*u, 2*u*r, r*r
l_P = math.sqrt(hbar*G/c**3)
rep = {}

# =====================================================================================
print("=" * 78)
print("TARGET 1. IS NEWTON'S CONSTANT DERIVABLE, AND IF NOT, WHAT IS MISSING EXACTLY?")
print()
print("   From hbar, c and rho_Lambda one can build exactly ONE length:")
a0_full = (hbar*c/rho_L)**0.25
a0_M    = (W_M*hbar*c/rho_L)**0.25
print(f"      a_0 = (hbar c / rho_L)^(1/4) = {a0_full*1e6:.3f} microns   (whole bubble)")
print(f"      a_0 = (W_M hbar c / rho_L)^(1/4) = {a0_M*1e6:.3f} microns   (matter fraction)")
print()
print("   G is dimensionally independent of those three. Check what G supplies that they")
print("   cannot: the combination G rho_L / c^4 has units of one over length squared.")
L_lam = c**2/math.sqrt(G*rho_L)
L_dS  = math.sqrt(3/(8*math.pi))*L_lam
print(f"      L_Lambda = c^2 / sqrt(G rho_L) = {L_lam:.4e} m")
print(f"      (the de Sitter radius sqrt(3/Lambda) is sqrt(3/8pi) of it, {L_dS:.4e} m)")
print()
print("   So the entire content of G, given the vacuum energy, is ONE dimensionless ratio:")
N = L_lam/a0_full
print(f"      L_Lambda / a_0 = {N:.6e}")
print()
print("   That is the number the field has to produce. Nothing else about G is missing.")
print()
print("   AND IT APPEARS TWICE, WHICH IS NOT A COINCIDENCE. Compare it with the bubble")
print("   measured in Planck lengths:")
print(f"      a_0 / l_P      = {a0_full/l_P:.6e}")
print(f"      L_Lambda / a_0 = {N:.6e}")
print(f"      equal to machine precision: {abs(a0_full/l_P/N - 1) < 1e-12}")
print()
print("   That is an algebraic identity, not a numerical accident. Substituting the")
print("   definitions:")
print()
print("      l_P L_Lambda = sqrt(hbar G/c^3) . c^2/sqrt(G rho_L) = sqrt(hbar c/rho_L) = a_0^2")
print()
print("      +-------------------------------------------------------------+")
print("      |   a_0 = sqrt( l_P . L_Lambda )                              |")
print("      +-------------------------------------------------------------+")
print()
print(f"      check: sqrt(l_P L_Lambda) = {math.sqrt(l_P*L_lam):.6e} m")
print(f"             a_0                = {a0_full:.6e} m")
print()
print("   THE BUBBLE IS THE GEOMETRIC MEAN OF THE SMALLEST AND LARGEST LENGTHS IN PHYSICS.")
print()
print("   Stated at its true strength, which is less than it first looks and more useful.")
print("   The identity is DIMENSIONAL: given the four constants hbar, c, G and rho_Lambda")
print("   there are only three lengths to build, and the middle one is automatically the")
print("   geometric mean of the outer two. It holds in any theory, and no dynamics of this")
print("   field produced it.")
print()
print("   What the bubble field adds is the claim that the middle length is the SIZE OF AN")
print("   ACTUAL OBJECT rather than a dimensional curiosity. Granting that, the identity")
print("   does real work: it PROVES that Targets 1 and 2 are one question rather than two")
print("   similar ones, since the number G is missing and the number Lambda is missing are")
print("   provably the same number. Deriving either one derives the other, and that was")
print("   not obvious before the identity was written down.")
print()
print("   The framework already manufactures numbers of this size, and only one way: as a")
print("   power of r. Solving for the exponent rather than guessing it:")
n_exact = math.log(N)/math.log(1/r)
print(f"      log(L/a_0) / log(1/r) = {n_exact:.4f}")
print()
print(f"      nearest integer: 60.  r^-60 = {(1/r)**60:.6e}")
print(f"      ratio to target: {N/((1/r)**60):.6f}")
print()
print("   Sixty is not an arbitrary landing spot. The corpus's hierarchy result carries")
print("   r^-120, and 120 = 2 x 60, with the square being exactly what a length-to-length")
print("   ratio does when it appears inside an energy density. So the exponent matches")
print("   something already derived, and the residual is a prefactor of 1.37, not a power.")
print()
print("   PROTOCOL. Only integers 40 to 80 were examined, one expression, no free")
print("   parameters, and the exponent was SOLVED FOR rather than searched. A 37 per cent")
print("   residual is not a match and is not reported as one. What is reported is that the")
print("   missing content of G is a single dimensionless number, that the framework's only")
print("   generator of such numbers gives the right order with an exponent that is half")
print("   the corpus's own, and that the prefactor is the whole remaining gap.")
rep["G"] = {"missing_content": "one dimensionless ratio L_Lambda/a_0 = a_0/l_P", "L_Lambda_m": L_lam,
            "ratio": N, "identity": "a_0 = sqrt(l_P L_Lambda), exact", "solved_exponent": n_exact, "nearest_integer": 60,
            "residual_prefactor": N/((1/r)**60),
            "note": "corpus hierarchy carries r^-120 = (r^-60)^2"}

# =====================================================================================
print()
print("=" * 78)
print("TARGET 2. THE COSMOLOGICAL CONSTANT PROBLEM, RESTATED")
print()
ratio_lP = a0_full/l_P
print(f"      Planck length      l_P = {l_P:.4e} m")
print(f"      bubble size        a_0 = {a0_full:.4e} m")
print(f"      a_0 / l_P              = {ratio_lP:.6e}")
print()
print("   The famous discrepancy between the observed vacuum energy and its Planck-scale")
print("   estimate is the fourth power of that one ratio:")
print(f"      (a_0/l_P)^-4 = {ratio_lP**-4:.4e}")
print(f"      quoted discrepancy is of order 1e-122 to 1e-123.")
print()
print("   So in this field the cosmological constant problem is not a problem about energy")
print("   at all. It is the single statement that the least-action cell is 5.4e30 Planck")
print("   lengths across rather than one. The 122 orders are 4 x 30.5, and nothing else.")
print()
print("   That is a genuine reframing and it is exact, not an estimate. It also means")
print("   Target 1 and Target 2 are THE SAME QUESTION: both are the ratio L/a_0, once as")
print("   G and once as Lambda. Deriving the one derives the other.")
rep["cc_problem"] = {"a0_over_lP": ratio_lP, "fourth_power_inverse": ratio_lP**-4,
                     "statement": "the CC problem is the single ratio a_0/l_P, to the fourth",
                     "same_question_as": "Target 1"}

# =====================================================================================
print()
print("=" * 78)
print("TARGET 3. CONFINEMENT FROM THE FLOOR, WITH A NUMBER")
print()
print("   The named mechanism: a bubble cannot hold less than one quantum of action, so")
print("   the matter part has a floor. A response pinned at its floor cannot spread, so")
print("   the field is squeezed into a tube of fixed cross-section and its energy grows")
print("   linearly with length. String tension = (energy density) x (cross-section).")
print()
print("   FIRST, AT THE VACUUM SCALE. If the tube is one vacuum bubble across:")
sigma_vac = rho_L * a0_full**2
sigma_QCD = 0.18 * (1e9*eV)**2 / (hbar*c)      # 0.18 GeV^2 in J/m
print(f"      sigma = rho_L a_0^2 = {sigma_vac:.4e} J/m")
print(f"      measured QCD string tension ~ 0.18 GeV^2 = {sigma_QCD:.4e} J/m")
print(f"      short by a factor of {sigma_QCD/sigma_vac:.3e}")
print()
print("      NEGATIVE, and cleanly so: the QCD string is not the vacuum bubble at its")
print("      floor. Twenty-three orders is not a factor anyone talks their way out of.")
print()
print("   SECOND, AT THE SCALE THE FIELD ITSELF SETS INSIDE MATTER. The bubble scale is")
print("   not a_0 where matter is present; it is set by the local energy. Take the QCD")
print("   scale as the local bubble energy and let the same construction run:")
E_had = 0.2e9*eV
a_had = hbar*c/E_had
rho_had = E_had/a_had**3
sigma_had = rho_had*a_had**2
print(f"      local cell energy   {E_had/eV/1e6:.0f} MeV")
print(f"      local cell size     a = hbar c / E = {a_had:.4e} m = {a_had*1e15:.3f} fm")
print(f"      local density       {rho_had:.4e} J/m^3")
print(f"      sigma = rho a^2   = {sigma_had:.4e} J/m")
print(f"      measured          = {sigma_QCD:.4e} J/m")
print(f"      ratio             = {sigma_had/sigma_QCD:.3f}")
print()
print("      POSITIVE, within a factor of a few, from one line and no fitting. The")
print("      construction 'energy density times cross-section of one cell' reproduces the")
print("      string tension once the cell is the one the local energy defines.")
print()
print("      What that establishes is narrower than 'confinement derived' and wider than")
print("      nothing: the floor mechanism is SCALE CONSISTENT. The same rule that gives a")
print("      hopeless answer at the vacuum scale gives the right answer at the hadronic")
print("      one, which is what you want from a mechanism whose scale is set by its")
print("      surroundings rather than fixed in advance.")
rep["confinement"] = {"sigma_vacuum_scale_J_per_m": sigma_vac,
                      "sigma_measured_J_per_m": sigma_QCD,
                      "vacuum_scale_shortfall": sigma_QCD/sigma_vac,
                      "hadronic_cell_fm": a_had*1e15,
                      "sigma_hadronic_scale": sigma_had,
                      "hadronic_ratio_to_measured": sigma_had/sigma_QCD,
                      "verdict": "vacuum-scale reading excluded by 23 orders; local-scale "
                                 "reading lands within a factor of a few"}

# =====================================================================================
print()
print("=" * 78)
print("TARGET 4. DOES THE CROWDING ENERGY LOOK LIKE DARK MATTER?")
print()
print("   The crowding carries energy: extra bubbles are extra vacuum energy. On the")
print("   crowding branch nu = 2.4 alpha_M, so")
print()
print("      delta rho = rho_L (e^nu - 1) ~ 2.4 rho_L alpha_M = 2.4 rho_L |Phi|/c^2")
print()
print("   which is an energy density that tracks the potential and extends exactly as far")
print("   as the potential does. That is the right SHAPE for a dark matter halo, so it is")
print("   worth putting a number on rather than admiring.")
print()
cases = [("Solar System, Earth orbit", 9.871e-9, None),
         ("galaxy, v = 200 km/s",      (200e3/c)**2, 5e-22),
         ("cluster, v = 1000 km/s",    (1000e3/c)**2, 1e-24)]
print(f"   {'system':<28}{'alpha_M':>12}{'delta rho kg/m^3':>20}{'observed DM':>14}{'short by':>12}")
dm = []
for nm, al, obs in cases:
    drho = 2.4*rho_L*al/c**2
    s = f"{obs:.1e}" if obs else "n/a"
    sh = f"{obs/drho:.1e}" if obs else "n/a"
    print(f"   {nm:<28}{al:>12.3e}{drho:>20.3e}{s:>14}{sh:>12}")
    dm.append({"system": nm, "alpha_M": al, "delta_rho_kg_m3": drho, "observed": obs})
print()
print("   NEGATIVE, by eleven orders in galaxies. The crowding energy has the right shape")
print("   and hopelessly the wrong size, and the reason is structural rather than")
print("   adjustable: it is proportional to rho_Lambda, so it can never be larger than the")
print("   vacuum energy times a small potential. Dark matter is about five times the")
print("   ordinary matter density, not a part in 1e11 of the vacuum.")
print()
print("   This is worth stating because it closes a door that looked open. The density")
print("   mode is a real new degree of freedom, but it is not a dark matter candidate in")
print("   this form, and no choice of the response ratio rescues it: the fork moves the")
print("   coefficient 2.4, not the eleven orders.")
rep["dark_matter"] = {"cases": dm, "verdict": "excluded as a dark matter candidate by ~11 "
                      "orders in galaxies; the shortfall is structural, not a coefficient"}

# =====================================================================================
print()
print("=" * 78)
print("TARGET 5. THE THREE CHANNELS AND THEIR RANGES")
print()
print("   Each bubble carries three parts, so the sea has three response channels, and")
print("   the range of each is fixed by whether that part propagates:")
print()
print(f"   LIGHT     W_L = u^2  = {W_L:.6f}   Lambda^2(surviving) = the 10")
print("                the light barrier IS the causal cell boundary, so this channel")
print("                propagates at c by construction. Massless, infinite range.")
print()
print(f"   BOUNDARY  W_B = 2ur = {W_B:.6f}   the cross block = the 15")
print("                the only weight that is a product of two different things, so it")
print("                exists only as a relation. It is also the only block whose bracket")
print("                with itself generates the other two, [15,15] -> 10 + 3. This is the")
print("                channel that makes the other two out of itself.")
print()
print(f"   MATTER    W_M = r^2  = {W_M:.6f}   Lambda^2(decayed) = the 3")
print("                the decayed sector by definition does not propagate in the")
print("                surviving one. Zero range. A force carried here is contact or")
print("                confined, never long range, and that is not a choice.")
print()
print("   The range hierarchy is therefore forced by the block structure and needs no")
print("   parameters: one infinite-range channel, one relational channel, one channel")
print("   with no range at all. What is NOT forced by this alone is the middle case,")
print("   the finite range of the weak interaction, which needs the boundary block to")
print("   acquire a scale. That is the same fixed-point equation as the mass problem,")
print("   which is the point where these two lines meet.")
rep["channels"] = {"light": {"W": W_L, "block": 10, "range": "infinite, propagates at c"},
                   "boundary": {"W": W_B, "block": 15, "range": "relational; sets its own "
                                "scale via the fixed point"},
                   "matter": {"W": W_M, "block": 3, "range": "zero; the decayed sector does "
                              "not propagate in the surviving one"}}

print()
print("=" * 78)
print("SCORECARD")
print()
print("   REACHED, and new:")
print("     - G and Lambda are ONE question, not two: the single ratio L/a_0 = 5.4e30.")
print("       Deriving either derives the other, and the framework's only generator of")
print("       numbers that size gives an exponent of 60, half the corpus's own 120.")
print("     - the cosmological constant problem is exactly (a_0/l_P)^-4. Not an estimate.")
print("     - the string tension comes out within a factor of a few once the cell is the")
print("       one the local energy sets, from energy density times cell cross-section.")
print("     - the range hierarchy is forced by the block structure with no parameters.")
print()
print("   CLOSED OFF, which is the other half of the work:")
print("     - the QCD string is not the vacuum bubble at its floor. Short by 1e23.")
print("     - the crowding energy is not dark matter. Short by 1e11, structurally.")
print()
print("   THE ONE NUMBER EVERYTHING NOW WAITS ON:")
print()
print("      L / a_0 = 5.4e30,  equivalently a_0 / l_P,  equivalently G,  equivalently")
print("      the cosmological constant problem. Four names for one missing derivation.")

json.dump({"generated": datetime.datetime.now().isoformat(timespec="seconds"),
  "field": "three-part bubble: alpha_L, alpha_M, nu, phase; weights u^2, 2ur, r^2",
  **rep,
  "scorecard": {
    "reached": ["G and Lambda are one question: the ratio L/a_0",
                "the CC problem is exactly (a_0/l_P)^-4",
                "string tension within a factor of a few at the local cell scale",
                "the range hierarchy is forced by the block structure"],
    "closed_off": ["the QCD string is not the vacuum bubble at its floor, short by 1e23",
                   "the crowding energy is not dark matter, short by 1e11"],
    "everything_waits_on": "the single dimensionless ratio L/a_0 = 5.4e30"},
 }, open(os.path.join(OUT, "exercising_the_field_results.json"), "w"), indent=2)

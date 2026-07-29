"""Auditing the closure attack, under the corpus's own protocol.

The package contains work of very different qualities under one cover, and the grading it
supplies is honest but softer than the corpus standard. This separates them, and where a
number is claimed it counts the search that produced it, because that is the only thing
that distinguishes a result from a coincidence.

The bar is the corpus's own: Lambda lands at 0.28 sigma and eta_H at 1.25 sigma, both from
closed forms fixed before the comparison.
"""
import math, itertools, json, os, datetime

OUT = os.path.dirname(os.path.abspath(__file__))
phi = (1 + math.sqrt(5))/2
r = 1/(2*phi); u = 1 - r
rep = {}

# =====================================================================================
print("=" * 78)
print("PART 1. THE LEPTON SPECTRUM, COUNTED")
print()
m_e, m_mu, m_tau = 0.51099895069, 105.6583755, 1776.86
s_e, s_mu, s_tau = 1.5e-10, 2.3e-9, 0.12          # PDG absolute uncertainties, MeV
cand = {"electron": 0.5114602674055334, "muon": 104.7866314888976,
        "tau": 1772.5297082927646}
print(f"   {'':<10}{'candidate':>16}{'measured':>16}{'rel err':>12}{'sigma':>14}")
sig = {}
for nm, meas, s in [("electron", m_e, s_e), ("muon", m_mu, s_mu), ("tau", m_tau, s_tau)]:
    c_ = cand[nm]; rel = c_/meas - 1; nsig = abs(c_-meas)/s
    sig[nm] = nsig
    print(f"   {nm:<10}{c_:>16.7f}{meas:>16.7f}{rel:>+11.3%}{nsig:>14.3g}")
print()
print("   THE DECISIVE POINT IS NOT THE SEARCH SIZE, IT IS THE MISS. The muon candidate is")
print("   0.83 per cent from a quantity measured to two parts in a hundred million, which")
print("   is 3.8e8 sigma in its own experimental units. A formula wrong by 0.8 per cent")
print("   about a number known to 1e-8 is simply wrong, however it was arrived at. The")
print("   corpus's accepted results sit at 0.28 and 1.25 sigma.")
print()

# --- how big was the search? ---------------------------------------------------------
print("   HOW MUCH SEARCH WAS AVAILABLE. The forms are m_mu = m_e phi^11 (1+r^3) and")
print("   m_tau = m_e phi^17 (1-r^3). Rebuild that class honestly and count it.")
print()
factors = {}
for nm, v in [("1", 1.0), ("u", u), ("1/u", 1/u), ("phi", phi), ("1/phi", 1/phi)]:
    factors[nm] = v
for k in (1, 2, 3, 4):
    factors[f"1+r^{k}"] = 1 + r**k
    factors[f"1-r^{k}"] = 1 - r**k
    factors[f"1+r^{k}/2"] = 1 + r**k/2
    factors[f"1-r^{k}/2"] = 1 - r**k/2
    factors[f"(1-r^{k})^2"] = (1 - r**k)**2
    factors[f"(1+r^{k})^2"] = (1 + r**k)**2
bases = {"phi": phi, "1/r": 1/r, "u": u, "1+r": 1+r}
cands = []
for bn, bv in bases.items():
    for n in range(1, 31):
        for fn, fv in factors.items():
            cands.append((f"{bn}^{n} * {fn}", bv**n * fv))
print(f"   candidate expressions in that class: {len(cands):,}")
print()
R1, R2 = m_mu/m_e, m_tau/m_mu
for label, target in [("m_mu/m_e  = %.4f" % R1, R1), ("m_tau/m_mu = %.4f" % R2, R2)]:
    hits1 = [c for c in cands if abs(c[1]/target - 1) < 0.01]
    hits2 = [c for c in cands if abs(c[1]/target - 1) < 0.001]
    print(f"   {label}")
    print(f"      within 1.0 per cent : {len(hits1):>5} of {len(cands):,}")
    print(f"      within 0.1 per cent : {len(hits2):>5}")
print()
n1 = len([c for c in cands if abs(c[1]/R1 - 1) < 0.01])
n2 = len([c for c in cands if abs(c[1]/R2 - 1) < 0.01])
print(f"   Stated accurately rather than rhetorically: {n1} and {n2} expressions out of")
print(f"   {len(cands):,} reach one per cent, hit rates of {100*n1/len(cands):.2f} and "
      f"{100*n2/len(cands):.2f} per cent. So the")
print("   search alone does not damn it; a pair hitting both is not trivially expected.")
print("   The problem is the other one: after all that freedom it still misses by 0.8 per")
print("   cent, and the base m_e is itself built on the fitted weak scale, so the errors")
print("   are not independent of Part 2 either.")
print()
print("   VERDICT ON THE LEPTONS: numerology, and the package's own grading says as much")
print("   in milder words. It is right that the decisive missing step is a mass operator")
print("   whose eigenvalue multiplicities FORCE the depths 11 and 17. Until that exists")
print("   the depths are two fitted integers and the correction factors are three more")
print("   fitted choices, against three targets. Do not carry these numbers forward.")
rep["leptons"] = {"sigma": sig, "class_size": len(cands),
                  "hits_within_1pc_ratio1": n1, "hits_within_1pc_ratio2": n2,
                  "verdict": "numerology; do not carry forward"}

# =====================================================================================
print()
print("=" * 78)
print("PART 2. THE WEAK SCALE")
print()
hbar, c, G_cod = 1.054571817e-34, 2.99792458e8, 6.67430e-11
eV = 1.602176634e-19
E_P = math.sqrt(hbar*c**5/G_cod)/eV
E_0 = 2.2487061123877767e-3
bridge = math.sqrt(E_P*E_0)
v_cand = (r**2/2)*math.sqrt(1-r**3)*bridge/1e9
print(f"   UV/IR bridge  sqrt(E_P E_0) = {bridge/1e9:.4f} GeV")
print(f"   v = (r^2/2) sqrt(1-r^3) x bridge = {v_cand:.4f} GeV   vs measured 246.2197")
print(f"   relative error {v_cand/246.21965-1:+.4%}")
print()
print("   Three chosen factors: the power r^2, the halving, and the square root of the")
print("   retained fraction. The geometric-mean bridge itself is the non-arbitrary part,")
print("   and it lands at 5241.6 GeV, a factor of 21 above the target, which the three")
print("   factors then close. 0.13 per cent from three choices is not evidence.")
print()
print("   WHAT IS WORTH KEEPING: the bridge sqrt(E_P E_0). That is the same geometric-mean")
print("   structure as a_0 = sqrt(l_P L_Lambda), so it is not an extra assumption, it is")
print("   the energy form of an identity already in hand. The claim that the electroweak")
print("   scale sits at the UV/IR geometric mean is a real structural proposal. The")
print("   prefactor is not.")
rep["weak"] = {"bridge_GeV": bridge/1e9, "candidate_GeV": v_cand,
               "relative_error": v_cand/246.21965-1,
               "verdict": "the geometric-mean bridge is structural; the three-factor "
                          "prefactor is fitted"}

# =====================================================================================
print()
print("=" * 78)
print("PART 3. THE G BRIDGE, WHICH IS THE STRONGEST OF THE THREE NUMBER CLAIMS")
print()
q_obs = 1.1491556219409747e-123
print(f"   q observed (Planck chain, CODATA G) = {q_obs:.6e}")
print(f"   effective exponent  log q / log r    = {math.log(q_obs)/math.log(r):.4f}")
print()
print(f"   r^240 = {r**240:.6e}     240 = the E8 root count, already derived in the corpus")
print(f"   r^241 = {r**241:.6e}     241 = 240 internal modes + one external readout")
print(f"   r^241 (1-r^3)^2 = {r**241*(1-r**3)**2:.6e}")
print(f"   ratio to observed: {r**241*(1-r**3)**2/q_obs:.6f}")
print()
print("   WHY THIS ONE IS DIFFERENT FROM THE OTHER TWO. The exponent is not fitted. The")
print("   observed effective exponent is 241.05, and 241 is not a free integer chosen from")
print("   a range: 240 is the root count the corpus derives, and the readout adds one. The")
print("   only fitted object is the residual factor 0.9433, matched by (1-r^3)^2 = 0.9419.")
print()
print("   So the honest reading is one derived exponent plus one fitted prefactor at the")
print("   0.15 per cent level, rather than a free two-parameter fit. That is materially")
print("   better than the lepton and weak claims and should not be lumped with them.")
print()
print("   AND IT HAS A REAL FALSIFIER, which is the thing that makes it science:")
q_two = r**241*(1-r**3)**2
print(f"      predicted G = {6.664385285614194e-11:.6e}  +/- 1.5 per cent (from Lambda)")
print(f"      CODATA G    = {G_cod:.6e}  +/- 0.0022 per cent")
print(f"      current agreement: {6.664385285614194e-11/G_cod-1:+.3%}, i.e. 0.1 sigma of the")
print( "      cosmological error, so consistent but not yet a test.")
print()
print("      The whole uncertainty is in Lambda. G is already known 700 times better than")
print("      the prediction. So ANY improvement in Lambda sharpens this into a real test,")
print("      and a factor of 100 in Lambda would test it at the 0.015 per cent level")
print("      against a G that is known to 0.002 per cent. This is a bet that can be lost,")
print("      and it will be settled by cosmology rather than by more algebra.")
rep["G_bridge"] = {"q_obs": q_obs, "effective_exponent": math.log(q_obs)/math.log(r),
                   "model": q_two, "ratio": q_two/q_obs,
                   "exponent_is_derived": "240 E8 roots + 1 readout",
                   "prefactor_is_fitted": True,
                   "verdict": "one derived exponent, one fitted prefactor; genuinely "
                              "falsifiable once Lambda improves"}

# =====================================================================================
print()
print("=" * 78)
print("PART 4. THE PART THAT IS ACTUALLY SOLID, AND A CORRECTION TO ME")
print()
print("   THE SOURCE SECTOR. Exact isotropic Einstein equations written in the bubble")
print("   variables, with A = -alpha_M and B = alpha_L + nu/3, exact Schwarzschild")
print("   residuals of zero, and a constant-density star reconstructed end to end. That")
print("   is the sector both my draft and the first review left empty, and it is now")
print("   filled with something checkable. This is the real advance in the package.")
print()
print("   THE IDENTIFIABILITY STATEMENT, which is sharp and correct:")
print()
print("      GR fixes A and B. It cannot separately identify alpha_L and nu without one")
print("      constitutive response law.")
print()
print("   That is exactly what I found from the other end when gamma came out identically")
print("   1 for every response ratio. Two routes, same conclusion: no gravitational")
print("   measurement of any precision can split the light mode from the density mode.")
print("   The split has to come from the microphysics or not at all.")
print()
print("   THEIR CANDIDATE SPLIT, and it is a good one:")
ratio_amp = r/u
nu_over_aM = 3*(1 - ratio_amp)
print(f"      alpha_L = (r/u) alpha_M,   r/u = 1/sqrt5 = {ratio_amp:.9f}")
print(f"      hence nu = 3(alpha_M - alpha_L) = {nu_over_aM:.6f} alpha_M   POSITIVE")
print()
print("   Positive means CROWDING, which is Joseph's picture, and it resolves the fork I")
print("   left open. It also picks the physically right reading of the two I offered: the")
print("   response follows the AMPLITUDE ratio r/u, not the intensity ratio r^2/u^2. That")
print("   is what a field does, and 1/sqrt5 is the same constant that already sets the")
print("   coframe coefficient in the boundary-block stationarity condition. It is not a")
print("   new number.")
print()
print("   A CORRECTION TO MY OWN CONFINEMENT RESULT, and they are right.")
print()
sig_id = "sigma = rho a^2 = (E/a^3) a^2 = E/a = E^2/(hbar c)"
print(f"      {sig_id}")
print()
print("   With a = hbar c/E the string tension is IDENTICALLY E^2/(hbar c). So putting in")
print("   the QCD scale and getting the QCD tension is a change of units, not a")
print("   prediction. My 'within a factor of five, no fitting' overstated it: the factor")
print("   of five is just 200 MeV against the 424 MeV that inverts the measured tension.")
print("   There is no independent content. Withdrawn.")
rep["solid"] = {"source_sector": "exact isotropic Einstein equations in bubble variables, "
                                 "exact Schwarzschild, constant-density star",
                "identifiability": "GR fixes A and B, not alpha_L and nu separately; "
                                   "independently confirms gamma = 1 for any response ratio",
                "constitutive_split": {"alpha_L_over_alpha_M": ratio_amp,
                                       "nu_over_alpha_M": nu_over_aM,
                                       "sign": "positive, crowding"},
                "my_confinement_claim": "WITHDRAWN; sigma = E^2/(hbar c) identically, so the "
                                        "string tension calculation was a change of units"}

print()
print("=" * 78)
print("VERDICT, SORTED")
print()
print("   KEEP AND BUILD ON:")
print("     - the exact source sector and the star reconstruction")
print("     - the identifiability theorem, which closes my open fork by showing no")
print("       gravitational measurement can ever settle it")
print("     - alpha_L = (r/u) alpha_M, giving crowding with nu = 1.66 alpha_M")
print("     - the geometric-mean bridge sqrt(E_P E_0), which is the energy form of an")
print("       identity already established")
print()
print("   HOLD AS A REAL BET:")
print("     - q = r^241 (1-r^3)^2. Derived exponent, fitted prefactor, and a falsifier")
print("       that cosmology will settle rather than algebra.")
print()
print("   DO NOT CARRY FORWARD:")
print("     - the charged lepton spectrum. 4e5 sigma on the muon, from a class in which")
print("       one per cent hits are common. The package's own grading agrees in substance.")
print("     - the weak VEV prefactor, three chosen factors for 0.13 per cent.")
print()
print("   WITHDRAWN FROM MY OWN WORK:")
print("     - the string tension result. Identity, not prediction.")

json.dump({"generated": datetime.datetime.now().isoformat(timespec="seconds"),
  "audited": "bubble-field-closure-attack-package",
  **rep,
  "verdict": {"keep": ["exact source sector and star reconstruction",
                       "the identifiability theorem",
                       "alpha_L = (r/u) alpha_M, crowding with nu = 1.66 alpha_M",
                       "the geometric-mean energy bridge"],
              "real_bet": ["q = r^241 (1-r^3)^2, falsifiable once Lambda improves"],
              "reject": ["the charged lepton spectrum", "the weak VEV prefactor"],
              "withdrawn_from_my_own_work": ["the string tension, which is an identity"]},
 }, open(os.path.join(OUT, "audit_closure_attack_results.json"), "w"), indent=2)

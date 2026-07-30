# ═════════════════════════════════════════════════════════ PART IV
part("Part four", "The field",
     "Helical Relativity, gravity, equivalence and the dark sector.")

chap("Chapter eight", "Helical Relativity",
     "A four-scalar field with a three-component geometric readout.")
para("Helical Relativity is the working field realisation developed after the "
     "frozen corpus. Its objects are least-action cells carrying the three-way "
     "partition. Space is modelled as their relational packing, curvature is the "
     "failure of that packing to remain uniform, and phase retains future "
     "orientation. The field is governed by four local scalars.")
eq("α_L = ln(a_L/a_{L0})       α_M = ln(a_M/a_{M0})       ν = ln(n/n_0)       "
   "θ = cyclic phase", size=11)
eq("T = exp(−α_M)        P = exp(α_L + ν/3)")
figure("fl_f09_scalars.png",
       "The field-to-geometry map and its one-dimensional compression kernel. "
       "Both metric potentials are fixed and one combination of the field is "
       "not.")
para("Writing the isotropic metric potentials as A = −α_M and B = α_L + ν/3 "
     "makes the compression explicit. Geometry sees the matter and clock scalar, "
     "the combined spatial scalar and the phase. It does not independently "
     "recover α_L and ν.")
eq("α_L → α_L + δ ,        ν → ν − 3δ")
grade("PROVED",
      "The linear map from (α_L, α_M, ν, θ) to (A, B, θ) has rank three and "
      "nullity one. The displayed transformation is its kernel.")
para("That kernel is not a small numerical uncertainty. It is an exact "
     "non-identifiability: any geometry-only account using A and B cannot "
     "separate the light-packing contribution from the number-density "
     "contribution without additional matter or observational structure. This is "
     "precisely the kind of information loss the Crowley and Glorpnorp criterion "
     "detects, and it is where the framework and general relativity are able to "
     "differ without either being wrong about what the other can see.")
figure("js_plate_10.png",
       "Working architecture of the helical field: local cell structure, "
       "packing, phase and the observer-interior readout. Author's plate, "
       "carried across unchanged.", width=6.2)
para("Under a declared least-Euclidean response cost with the mixed Boundary "
     "constraint r α_L + u α_M = χ, stationarity fixes the response ratio rather "
     "than leaving it as a fit parameter.")
eq("α_L / α_M = r/u = 1/√5        ν = 3(α_M − α_L) = 3(1 − 1/√5) α_M")
grade("CONDITIONAL",
      "The ratio follows exactly from the stated cost metric and constraint. The "
      "physical choice of that metric and constraint remains the named "
      "condition.")

chap("Chapter nine", "The principle of equivalence",
     "Inertia and gravitation as two readouts of one persistence cost.")
figure("fl_f11_equivalence.png",
       "The proposed unification beneath inertial and gravitational mass, and "
       "the post-Newtonian identity that follows from the response ratio.")
para("The equivalence principle is usually introduced operationally: in a "
     "sufficiently small freely falling laboratory, nongravitational physics is "
     "locally special-relativistic, and test bodies with negligible self-gravity "
     "follow the same trajectories independent of composition. The field ledger "
     "asks what operation could make inertial resistance and gravitational "
     "sourcing coincide.")
eq("m_i = m_g        G_{μν} + Λ g_{μν} = (8πG/c⁴) T_{μν}")
grade("STANDARD",
      "The equality of inertial and gravitational response is a central "
      "empirical principle of relativistic gravity. Any new field must preserve "
      "universal free fall and the tested post-Newtonian limits.")
para("Unified Mechanics proposes that a self-holding system pays one retention "
     "cost. Viewed from the object side, the cost is resistance to changed "
     "motion. Viewed from the geometric side, the same retained operation "
     "contributes to stress-energy and curvature. That is a unification claim "
     "only if one generator can produce both readouts with no "
     "composition-dependent remainder.")
eq("γ = (α_L + ν/3) / α_M ,      with  ν = 3(α_M − α_L)   ⟹   γ = 1")
grade("PROVED",
      "Given ν = 3(α_M − α_L), the displayed substitution returns γ = 1 "
      "identically, for any amount of crowding, at any precision. That is an "
      "identity rather than agreement inside an error bar. Cassini measures "
      "γ − 1 = (2.1 ± 2.3) × 10⁻⁵.")
grade("CONDITIONAL",
      "What the identity establishes is that the declared mapping cannot "
      "produce a slip. The mapping itself, and the source action beneath it, are "
      "the conditions, and they are still owed. So the correct statement is that "
      "the framework has no free parameter to tune here, not that the sector is "
      "closed to challenge: a source action that failed to return the "
      "Schwarzschild relation would defeat the sector regardless of what the "
      "substitution does.")
para("Two further contacts with general relativity are exact, and both are worth "
     "stating because they are the first places a reader will look for a "
     "contradiction.")
eq("r φ = 1/2        so        (r φ)² = 1/4")
grade("PROVED",
      "The identity is exact. The product of the contraction and the ratio it "
      "came from is one half, so its square is a quarter, and nothing was chosen "
      "to make it so.")
grade("READING",
      "One quarter is also the Bekenstein-Hawking coefficient in S = A/4, which "
      "is fixed by the horizon calculation and is not a convention. That is a "
      "**contact and not a derivation of horizon entropy**: the framework has "
      "supplied a number that agrees, and it has not supplied the counting "
      "argument that produces it. The identification becomes a result when a "
      "bridge to the horizon calculation exists, and until then it is recorded "
      "as the agreement it is.")
para("The effective coupling is a small and definite offset from the bare one:")
eq("G_eff/G_N = 1 + 1/(2φ⁴) = 1 + r/(3+4r) = %.9f" % (1 + 1/(2*phi**4)))
grade("CONDITIONAL",
      "Recovering the Schwarzschild relation from the physical response sector "
      "depends on the helical field equations and the source conditions, not on "
      "the algebraic substitution alone.")
grade("OPEN",
      "The observable obligation is sharp: derive universal coupling, "
      "composition independence, gravitational redshift and light bending from "
      "one source action. A verbal statement that inertia and gravity are both "
      "retention is not enough; the common generator has to be explicit.")

chap("Chapter ten", "Dark matter",
     "An exact density readout, a proposed neutral mode, and a route the "
     "programme has withdrawn.")
figure("fl_f12_dark.png",
       "The dark-matter sector split into the three logical objects actually "
       "present in the work. Keeping them apart is what stops a number from "
       "being read as a particle.")
para("The cleanest dark-matter result in the framework is a density identity. It "
     "reads the Boundary weight through one factor of the fixed ratio.")
eq("Ω_c = W_B / φ = 4r²(1−r) = %.12f" % (4*r*r*(1-r)))
grade("PROVED", "The equality among the closed forms is exact inside the "
      "partition algebra.")
grade("PROPOSED",
      "Identifying this number with the cosmological cold-dark-matter fraction "
      "is an observable dictionary entry. Numerical agreement does not supply "
      "dark-matter microphysics.")
para("A viable mechanism has to satisfy the equations that make cold dark matter "
     "useful in cosmology. At background and linear order the target behaviour "
     "is approximately pressureless, weakly interacting clustering with "
     "negligible visible gauge charge.")
eq("ρ̇_c + 3H ρ_c = 0        δ̈_c + 2H δ̇_c − 4πG ρ_m δ_m = 0")
eq("p_c/ρ_c → 0 ,      c_s² → 0 ,      Q_visible(ψ_c) = 0")
para("The current mechanism proposal is that dark matter consists of "
     "self-holding modes of the carrier that are neutral under the surviving "
     "visible gauge projection. The idea has a useful structural consequence: "
     "dark matter should not carry ordinary visible gauge charge. The mode "
     "spectrum, abundance, stability, nonlinear halo behaviour and coupling to "
     "the helical metric have not yet been derived in one executable model.")
grade("PROPOSED",
      "Dark matter is the retained, self-holding sector that survives "
      "dynamically while projecting trivially onto visible gauge charge.")
grade("OPEN",
      "Construct the mode operator and the stress-energy tensor, derive "
      "pressureless background evolution and linear transfer functions, and "
      "confront lensing, growth and halo data.")
para("A separate attempt treated local cell-crowding energy as the missing "
     "galactic mass. That route is withdrawn: it is roughly eleven orders of "
     "magnitude too small in galaxies, and it is structurally proportional to "
     "vacuum density multiplied by a weak potential. The failed calculation is "
     "retained deliberately, because keeping it visible is what prevents the "
     "same mechanism from re-entering later under a new name.")
grade("WITHDRAWN",
      "Vacuum crowding energy is not the galactic dark-matter source in the "
      "tested form.")
table(["Observable arena", "What the proposed mode must produce",
       "Present status"],
      [["Microwave background peaks",
        "early gravitational wells and the correct baryon-loading pattern",
        "not yet calculated with a field transfer function"],
       ["Large-scale growth",
        "pressureless clustering and f σ_8 across redshift",
        "open perturbation closure"],
       ["Weak and strong lensing",
        "the same gravitational mass that the dynamics require",
        "open nonlinear stress-energy"],
       ["Galactic halos", "stable profiles, mergers and substructure",
        "crowding-energy route withdrawn; replacement open"],
       ["Laboratory visibility",
        "no ordinary visible gauge charge; a defined portal, or none",
        "structural proposal only"]],
      [1.62, 2.86, 2.46], size=8.8)


# ═════════════════════════════════════════════════════════ PART V
part("Part five", "Seeing the field",
     "The colour language as an operational graph, with the charts placed where "
     "the reader can actually inspect them.")

chap("Chapter eleven", "The Colour Field",
     "A visual and computable readout, not a substitute for mechanism.")
para("The Colour Field assigns each string a hue, a saturation, a brightness and "
     "an accessibility, together with phase, frequency, orientation, winding and "
     "retained history. The point is not to decorate equations. It is to put "
     "composition, phase displacement, closure depth and observational access on "
     "one inspectable surface.")
figure("js_plate_13.png",
       "The notation plate. Hue is phase address, saturation is coherence, "
       "brightness is weight or intensity, and accessibility marks how much of "
       "the state is available to the observer. Author's plate.", width=6.4)
para("Composition uses the same three weights as the partition. Light and Matter "
     "supply fixed poles and the Boundary term is the moving relational "
     "contribution. For parent phases θ_1 and θ_2 the object phase is a weighted "
     "circular mean rather than an arithmetic average.")
eq("Z = W_L e^{iθ_L} + W_B e^{iθ_B} + W_M e^{iθ_M}")
eq("θ_out = arg(Z) ,        coherence = |Z| / (W_L + W_B + W_M)")
grade("PROVED",
      "For the declared composition rule, the complex sum, the phase, the "
      "coherence and the rotational covariance are exact mathematical outputs.")
grade("PROPOSED",
      "The assignment of physical particles or cosmological components to "
      "particular hues is notation until a mass, charge and coupling operator "
      "derives the assignment.")
figure("js_plate_14.png",
       "The composition-bound plate. The maximum phase displacement is fixed by "
       "the ratio of the Boundary weight to the two pole weights. Author's "
       "plate.", width=6.4)
eq("W_B/(W_L + W_M) = 2ur/(u² + r²) = √5/3 = 1/Λ")
eq("|Δθ| ≤ arcsin(1/Λ) = 48.189685°")
grade("PROVED",
      "The bound and its identity with √5/3 are exact for the supplied "
      "composition map.")
para("There is a structural reading of that bound worth recording here, because "
     "it removes an apparent circularity elsewhere in the programme. On the pole "
     "ratio k = u/r the composition bound is 2k/(k²+1), and requiring it to "
     "equal 1/Λ gives k + 1/k = 2Λ identically. So")
eq("Λ = (k² + 1)/(2k) = AM(k², 1) / GM(k², 1)")
para("and at k² = W_L/W_M = 5 that is the arithmetic mean of five and one over "
     "their geometric mean, which is 3/√5 exactly. The three is what five and "
     "one average to, and the root five is what they multiply to. Λ is therefore "
     "a consequence of the partition rather than an input to it.")
grade("PROVED",
      "The identity k + 1/k = 2Λ holds for any k, so Λ = 3/√5 at k² = 5 is "
      "forced by the weight ratio alone.")
para("A wound string closes when n times the phase shift equals an integer "
     "number of turns. Seven traversals require more displacement than the bound "
     "allows, while eight traversals require forty-five degrees and are "
     "admitted, so eight is the first allowable closure depth under the rule.")
figure("js_plate_15.png",
       "The closure spectrum. The isolated points are candidate closed states "
       "ordered by traversal depth. Author's plate.", width=6.4)
grade("PROVED",
      "Under the declared closure rule, depth eight is the first admissible "
      "closure, and self-composition has fixed points only at relative phase 0 "
      "or π.")
grade("OPEN",
      "The closure spectrum counts and orders candidate states. It does not yet "
      "attach a derived mass or a visible charge to a closure depth.")
figure("js_plate_16.png",
       "The full composition atlas. This is the chart the earlier grammar-only "
       "monograph described without letting the reader inspect it. Author's "
       "plate.", width=6.4)
para("The atlas can be read as a physical ledger only with its type "
     "declarations intact. A colour can be a phase coordinate, a display "
     "convention, a spectral wavelength or a measured optical response, and "
     "those are not interchangeable. The magenta arc from 270 to 360 degrees is "
     "nonspectral in particular, and has to be treated as a phase address rather "
     "than a single physical wavelength.")
figure("js_plate_17.png",
       "The colour-frequency plate. The spectral segment maps log-linearly from "
       "700 nm to 400 nm; the closing magenta segment is an extrapolated phase "
       "address. Author's plate.", width=6.4)
figure("js_plate_18.png",
       "The mass-operator plate. It identifies the allowed algebraic location of "
       "a mass map, and the task of deriving the spectrum that is still "
       "outstanding. Author's plate.", width=6.4)
callout("Why the charts matter", [
    "A reader can now inspect the bound, the closure gaps, the phase motion and "
    "the candidate spectrum structure directly. The charts do not become "
    "evidence for a particle assignment until the mass and charge operators are "
    "supplied, and that is exactly what makes them useful rather than "
    "decorative.",
])

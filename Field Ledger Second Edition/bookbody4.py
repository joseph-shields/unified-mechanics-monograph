# ═════════════════════════════════════════════════════════ PART VI
part("Part six", "Running cosmology",
     "The forward solver, the Hubble basins and the vacuum hierarchy.")

chap("Chapter thirteen", "The microwave background",
     "What the solver reaches, what the diagnostic shows, and where the missing "
     "physics is located.")
para("The forward solver starts from seven invariant readouts and the measured "
     "background temperature. It uses Saha ionisation equilibrium to estimate "
     "recombination, integrates the sound horizon and the comoving distance, and "
     "adjusts the single overall Hubble scale so that a bias-corrected acoustic "
     "angle condition is met. It does not evolve the photon Boltzmann hierarchy.")
eq("θ_* = r_s(z_*) / D_M(z_*)")
eq("x_e²/(1−x_e) = (1/n_H) (m_e k_B T / 2πℏ²)^{3/2} exp(−χ_H/k_B T)")
eq("c_s = c / √[3(1+R)] ,        R = 3ρ_b/(4ρ_γ)")
table(["Quantity", "Value", "Comparison and meaning"],
      [["H_0", "%.3f" % A03["passB"]["H0"],
        "the laminar basin, %+.2f σ from Planck 67.36 ± 0.54"
        % A03["passB"]["pull_planck"]],
       ["z_*", "%.1f" % A03["passB"]["z_star"],
        "early; a realistic recombination network gives about 1090"],
       ["r_s", "%.3f Mpc" % A03["passB"]["r_s"], "the sound horizon integral"],
       ["D_M", "%.1f Mpc" % A03["passB"]["D_M"],
        "the background distance integral"],
       ["ω_b", "%.7f" % A03["passB"]["omega_b"],
        "against Planck 0.02237, about four per cent low"],
       ["ω_c", "%.7f" % A03["passB"]["omega_c"], "against Planck 0.1200"],
       ["ℓ_A", "%.3f" % A03["l_A"], "acoustic spacing in this solver"],
       ["ℓ_D", "%.1f" % A03["damping"]["l_D"], "approximate damping scale"]],
      [0.80, 1.34, 4.80], size=9.0, mono=(1,), centre=(0, 1))
figure("fl_f27_peaks.png",
       "The acoustic peak positions the solver returns, against Planck. The "
       "spacing is right and the absolute scale is uniformly high, which is the "
       "signature of a single cause rather than of five separate ones.")
grade("CONDITIONAL",
      "Within a Saha-recombination solver, seven invariants and one temperature "
      "anchor return H_0 = %.3f km s⁻¹ Mpc⁻¹ with no fitted parameter, from an "
      "acoustic-angle condition alone." % A03["passB"]["H0"])
grade("READING",
      "The absolute peak positions run %.0f to %.0f per cent high, and all five "
      "run high together. A uniform displacement in one direction is a located "
      "cause, not five failures: Saha decoupling puts last scattering at "
      "z_* = %.0f instead of about 1090, and every peak position inherits that "
      "one shift. The ratio structure, which does not depend on it, is available "
      "to inspect now."
      % (min(p["pct"] for p in A03["peaks"]),
         max(p["pct"] for p in A03["peaks"]), A03["passB"]["z_star"]))
grade("OPEN",
      "A multilevel recombination network and a full Boltzmann perturbation "
      "evolution are required before the framework can claim a spectrum. The "
      "next solver has to output temperature, cross and polarisation spectra and "
      "the lensing response, with residuals against public likelihoods and no "
      "borrowed cold-dark-matter transfer function unless that borrowing is "
      "declared.")
callout("The defeat condition for this sector", [
    "A full implementation that cannot reproduce the observed peak phases, "
    "relative heights, damping tail and lensing response with its declared "
    "matter mechanism defeats the cosmological realisation, even if the density "
    "percentages remain numerically attractive.",
])

chap("Chapter fourteen", "The two Hubble basins",
     "One anchored solve, the closure conventions that carry it, and the "
     "mechanism that is still owed.")
para("The forward solver returns a low value of H_0 from an acoustic and "
     "light-channel anchor. The framework then applies closure factors built "
     "from the floor r³ to obtain the local family. Three nearby conventions are "
     "evaluated because their differences fall below the framework's own "
     "structural floor.")
eq("H_0(laminar) = %.3f        H_0 × (1−r³)⁻³ = %.3f"
   % (A03["basins"]["laminar_H0"], A03["basins"]["condensed_(1-r3)^-3"]["H0"]))
eq("H_0 × (1+3r³) = %.3f        H_0(symmetric) = %.3f"
   % (A03["basins"]["condensed_1+3r3"]["H0"],
      A03["basins"]["condensed_symmetric"]["H0"]))
figure("fl_f28_basins.png",
       "The two basins, with the three closure conventions. All three land "
       "inside a quarter of a sigma of the local ladder and differ from each "
       "other by less than the floor.")
grade("PROVED",
      "The three high-basin numbers are exact outputs of the displayed closure "
      "conventions applied to the solver's laminar value. They differ from each "
      "other by less than r³ = %.7f, so the sector does not have to choose "
      "between them." % r3)
grade("READING",
      "The two measurements are two basins rather than two estimates of one "
      "number. A light-channel anchor reads the laminar flow at the bottom of "
      "the river; a local ladder reads the condensed flow nearer the surface. "
      "Comparing a laminar readout against a local ladder is comparing two "
      "different questions, and the closure factor is the framework's account of "
      "the difference between them.")
grade("PROPOSED",
      "That the early and local measurements sample distinct physical basins is "
      "not established by numerical agreement. It requires an explicit "
      "scale-dependent observable map.")
para("The decisive test is not whether both numbers can be made from r. It is "
     "whether one field equation predicts when an observational pipeline reads "
     "one basin, when it reads the other, and how intermediate probes behave. "
     "Strong-lens time delays, standard sirens, megamasers, tip-of-the-red-giant "
     "distances and inverse-distance-ladder results should then occupy calculable "
     "positions rather than being assigned after the fact.")
grade("OPEN",
      "Derive the basin-selection functional before consulting an additional "
      "H_0 dataset, then publish the resulting placements prospectively.")

chap("Chapter fifteen", "Dark energy and the vacuum hierarchy",
     "From a closure complement to a present-day observational challenge.")
para("At the simplest dictionary level, dark energy is the complement after the "
     "baryon and cold-dark-matter readouts are removed from unity.")
eq("Ω_{DE} = 1 − Ω_b − Ω_c = %.12f" % (1 - W_M/2 - W_B/phi))
grade("PROVED",
      "The complement is exact once the two density entries are declared.")
grade("PROPOSED",
      "Identifying the complement with a vacuum component of equation of state "
      "w = −1 is a separate physical claim.")
para("The helical field offers a conditional route to w = −1. If each cell "
     "carries fixed action, and expansion creates additional cells through a "
     "renewal law rather than diluting a conserved count, then constant energy "
     "density under expansion implies negative pressure.")
eq("∇·N = n Θ        ρ̇ + 3H(ρ + p) = 0 ,   ρ̇ = 0  ⟹  p = −ρ")
grade("CONDITIONAL",
      "The vacuum equation of state follows given the cell-renewal law and fixed "
      "action per cell.")
para("The corpus also contains a dimensionless vacuum readout whose exponent is "
     "tied to the 240-root carrier, and a length relation that is exact:")
eq("λ = (4π/√3) r^{240} = 2.860333 × 10⁻¹²²")
eq("ℓ_P L_Λ = a_0²        a_0 = (ℏc/ρ_Λ)^{1/4} = 88.11 μm")
figure("fl_f29_ladder.png",
       "The proposed middle scale between the Planck and vacuum lengths. The "
       "geometric mean is dimensional bookkeeping; reading the middle length as "
       "a physical cell is the claim.")
grade("FORECAST",
      "λ is parameter-free within the stated carrier construction and is "
      "compared with the observed dimensionless cosmological constant. The "
      "physical normalisation and the observational dictionary remain part of "
      "the test surface.")
grade("CONDITIONAL",
      "a_0(W) = (W ℏc/ρ_Λ)^{1/4} is an exact family. Choosing the whole-cell or "
      "the Matter branch as the physical scale is the declared condition. The "
      "branch assignment gives scales near tens of microns, close enough to "
      "short-range gravity tests to be scientifically exposed and not yet a "
      "detection.")
grade("OPEN",
      "DESI DR2 makes this chapter more urgent. Flat ΛCDM remains a successful "
      "description of the acoustic data, while combinations with the microwave "
      "background and supernovae give sample-dependent evidence for evolving "
      "dark energy. Derive H(z), w(z), f σ_8 and the lensing response from the "
      "renewal and retention field equation before using the preferred shape as "
      "a target.")


# ═════════════════════════════════════════════════════════ PART VII
part("Part seven", "The scientific ledger",
     "What is established, what is proposed, what has been withdrawn, and what "
     "would end the programme.")

chap("Chapter sixteen", "What the book has actually shown",
     "A compressed theory is useful only when the reader can tell the machine "
     "from its promises.")
figure("fl_f30_close.png",
       "The final accounting rule: every section terminates in an observable "
       "test or an explicitly named missing bridge.")
table(["Sector", "Strongest present result", "Observable ceiling"],
      [["Logical Action", "the dynamical sufficiency criterion π E = Ẽ π",
        "general theorem; application-specific state content still required"],
       ["Crowley and Glorpnorp",
        "relationally incomplete transcripts cannot preserve "
        "relation-conditioned evolution",
        "conceptual and formal; empirical use depends on the chosen field"],
       ["Minimal update",
        "the fixed golden ray and the exact three-way perfect square",
        "the physical channel names remain proposed"],
       ["Chiral split",
        "characteristic decomposition and an action representative",
        "particle spectrum and couplings open"],
       ["Gödel",
        "projection recurrence does not imply equality of a history-augmented "
        "state", "the physical record-retention premise is proposed"],
       ["Helical geometry",
        "the four-to-three map and its exact compression kernel",
        "source action and universal coupling incomplete"],
       ["Equivalence",
        "γ = 1 identically under the declared mapping; (rφ)² = 1/4 exactly",
        "the mapping and the common source action are conditional; the entropy "
        "coefficient is a contact, not a derivation of horizon entropy"],
       ["Dark matter", "the exact Ω_c dictionary value",
        "microphysics and transfer functions open"],
       ["Colour Field",
        "exact composition, bound and closure spectrum under declared rules; "
        "Λ = AM/GM of the weight ratio",
        "mass and charge assignment open"],
       ["The master readout",
        "all six entries move toward measurement, %.4f σ to %.4f σ, "
        "no fitted quantity" % (A09["E0_static"], A09["E1_master"]),
        "the flow and the hue map need a common field action"],
       ["The traversal payment",
        "a monotone, separated ladder in the number of records typed",
        "repetition in an independent sector, declared in advance"],
       ["Microwave background",
        "background integrals and a peak-location solver with a single located "
        "bias", "full recombination and Boltzmann spectra open"],
       ["Hubble basins",
        "exact closure transforms, all three inside a quarter sigma",
        "the basin-selection mechanism is proposed"],
       ["Dark energy",
        "exact complement and vacuum readout; conditional w = −1 renewal law",
        "redshift-dependent field dynamics open"]],
      [1.34, 3.00, 2.60], size=8.6)
para("The language has now done its intended job inside the science. It kept the "
     "exact dark-matter fraction from being confused with a dark-matter "
     "particle. It kept an acoustic-scale integration from being marketed as a "
     "Boltzmann spectrum. It kept a closed spacetime projection from being "
     "equated with a restored full state. It kept a colour address from becoming "
     "a mass assignment by prose. And in Chapter twelve it did something more "
     "than police the claims: **the type distinction it enforces turned out to "
     "be the thing being measured.**")
callout("The one-line version", [
    "**Every observable in the score moves toward measurement, and the amount "
    "by which the whole score moves is a reading of how much of it has been "
    "taken at its correct type.** The vocabulary is not the product and it is "
    "not decoration either. It is the instrument.",
])

chap("Chapter seventeen", "Defeat conditions and the next executable programme",
     "The book ends with experiments and calculations, not with a declaration of "
     "completeness.")
table(["Test", "Required output", "Defeat or revision condition"],
      [["Full spectrum solver",
        "temperature, cross, polarisation and lensing spectra with residual "
        "likelihoods",
        "cannot recover peak phases, heights and damping with the declared "
        "matter sector"],
       ["Dark-matter mechanism",
        "stress-energy, linear transfer, halo and lensing predictions",
        "requires visible gauge charge, or fails clustering and lensing jointly"],
       ["Equivalence",
        "one source action yielding inertia, curvature and universal coupling",
        "a composition-dependent residual above experimental bounds"],
       ["Hubble basins",
        "a prospective rule assigning probes to a basin",
        "new probes do not follow the predeclared placements"],
       ["Colour spectrum", "a mass and charge operator from closure data",
        "assignments require fitted particle labels, or fail the measured "
        "spectrum"],
       ["Vacuum scale",
        "short-range-gravity and cosmological forecasts",
        "the predicted cell-scale signal is excluded with no permitted branch"],
       ["Carrier and gauge sector",
        "the surviving gauge algebra and family structure",
        "a confirmed gauge structure outside the declared carrier, or a fourth "
        "light family"],
       ["The typing ladder",
        "the payment in a sector sharing no observables with this one, scored "
        "under the same rule declared in advance",
        "the payment does not rise monotonically with the number of records "
        "typed, or the rungs do not separate"],
       ["The half-weight boundary",
        "a derivation of the factor 1/(1−r³) for a half-weight that does not "
        "consult these residuals",
        "no derivation exists, in which case the last rung stays a candidate "
        "and the working readout stays the typed master"]],
      [1.34, 2.70, 2.90], size=8.6)
para("The next computational release should be organised in the order of that "
     "table. First, replace Saha recombination with a multilevel network and "
     "couple it to a Boltzmann solver interface. Second, specify the dark-sector "
     "stress-energy and perturbation closure. Third, derive the helical source "
     "action and calculate the equivalence-principle observables. Fourth, lock "
     "the basin-selection rule before adding new measurements. Fifth, connect the "
     "closure spectrum to an independently defined mass and charge operator. And "
     "running alongside all five, finish the type audit: the ladder says what "
     "each completed type is worth before the calculation is done.")
grade("OPEN",
      "The framework is not observationally closed. Its value now depends on "
      "converting the strongest structural identities into prospective, "
      "executable calculations with no target insertion.")
callout("The one-book standard", [
    "A physicist should be able to read this volume once, understand the "
    "operational spine, inspect the actual field charts, reproduce the displayed "
    "numerical readouts, locate every missing bridge, and know exactly what "
    "result would force the programme to change.",
])


# ═════════════════════════════════════════════════════════ APPENDICES
part("Appendices", "Equations, reproduction and references",
     "A compact audit surface for the reader who wants the formulas without "
     "rereading the argument.")

chap("Appendix A", "Compact equation ledger", None)
table(["Object", "Equation", "Grade"],
      [["Minimal update", "(a,b) → (a+b,a);  φ² = φ+1;  r = 1/(2φ);  u = 1−r",
        "PROVED"],
       ["Partition", "W_L = u²;  W_B = 2ur;  W_M = r²;  sum = 1", "PROVED"],
       ["Weight ratio", "W_L/W_M = 5;  W_M W_L − (W_B/2)² = 0", "PROVED"],
       ["Logical Action", "π ∘ E_t = Ẽ_t ∘ π", "PROVED criterion"],
       ["Chiral split", "∂_u ∂_v X = 0;  X = X_L(u) + X_R(v)", "STANDARD"],
       ["Finite mode", "dψ/dτ = −i Ω Γ ψ", "CONDITIONAL representation"],
       ["Traversal lift", "p(s) = exp(is);  H(s) = (R cos s, R sin s, hs)",
        "PROVED construction"],
       ["Helical geometry", "A = −α_M;  B = α_L + ν/3", "definition"],
       ["Compression kernel", "α_L → α_L + δ;  ν → ν − 3δ", "PROVED"],
       ["Post-Newtonian slip", "γ = (α_L + ν/3)/α_M = 1",
        "PROVED identity, CONDITIONAL mapping"],
       ["Entropy coefficient", "(rφ)² = 1/4",
        "PROVED identity, READING of the contact"],
       ["Effective coupling", "G_eff/G_N = 1 + 1/(2φ⁴)", "PROVED identity"],
       ["Response ratio", "α_L/α_M = r/u = 1/√5", "CONDITIONAL"],
       ["Dark matter fraction", "Ω_c = W_B/φ = 4r²u",
        "PROVED identity, PROPOSED map"],
       ["Baryons", "Ω_b = W_M/2", "PROVED identity, PROPOSED map"],
       ["Dark energy", "Ω_{DE} = 1 − Ω_b − Ω_c", "PROVED given the map"],
       ["Tilt, dictionary", "n_s = 1 − W_M(1−2r)", "PROVED given the map"],
       ["Tilt, flow", "n_s = 1 + ln(1−r³)", "PROPOSED route"],
       ["Colour composition", "Z = Σ_j W_j e^{iθ_j};  θ = arg Z", "PROVED rule"],
       ["Colour bound", "|Δθ| ≤ arcsin(√5/3) = 48.189685°", "PROVED rule"],
       ["Cosmological constant", "Λ = (k²+1)/(2k) = AM(k²,1)/GM(k²,1)",
        "PROVED identity"],
       ["Master readout", "R[O] = Σ H_5(N_t) O(C_t) / Σ H_5(N_t)",
        "CONDITIONAL operator"],
       ["Resolution", "N = 360 T/Δθ;  H_5(N) = 2s¹⁰/(1+s¹⁰),  s = N/(N+1)",
        "PROVED, from A01"],
       ["Optical depth, typed", "τ = R[2m³(1−r³)³]", "CONDITIONAL path readout"],
       ["Traversal payment", "P_T = 1 − E_1/E_0 = %.6f"
        % A09["traversal_payment"], "PROVED arithmetic"],
       ["Typing ladder", "P_T strictly increasing in records typed; rung means "
        "%s" % ", ".join("%.4f" % (sum(L["payment"] for L in LAD["rungs"]
                                       if L["n_typed"] == k)
                                   / max(1, sum(1 for L in LAD["rungs"]
                                                if L["n_typed"] == k)))
                         for k in range(4)),
        "PROVED, READING"],
       ["Half-weight boundary", "Ω_b, Y_{He} each divided by (1−r³)",
        "candidate; derivation OPEN"],
       ["Acoustic angle", "θ_* = r_s/D_M", "STANDARD"],
       ["Vacuum readout", "λ = (4π/√3) r^{240}", "FORECAST"],
       ["Cell scale", "ℓ_P L_Λ = a_0²;  a_0 = 88.11 μm", "PROVED, CONDITIONAL "
        "branch"]],
      [1.44, 3.62, 1.88], size=8.4, mono=(1,))

chap("Appendix B", "Reproduction map", None)
para("Every number in this book regenerates from a script in the addenda folder, "
     "and every script writes its own JSON certificate beside it. The figures of "
     "this edition are generated from those certificates by the two plate "
     "scripts in this folder.", raw=False)
table(["Output", "Source"],
      [["Partition and cosmological dictionary",
        "ADDENDA/A02 The Field Derivation Suite/um_field_suite.py"],
       ["Forward recombination and acoustic solver",
        "ADDENDA/A03 The Forward Solver/um_forward_solver.py"],
       ["Resolution operator and its join",
        "ADDENDA/A01 The Resolution Operator"],
       ["Internal state instrument",
        "ADDENDA/A04 The Internal State Instrument/internal_state_instrument.py"],
       ["Colour average readout",
        "ADDENDA/A05 Prediction From The Colour Average/"
        "colour_average_prediction.py"],
       ["Helical multiplication and the realisation count",
        "ADDENDA/A07 Helical Multiplication/helical_multiplication.py"],
       ["Master readout, payment, ensemble tests and typing ladder",
        "ADDENDA/A09 The Master Equation/master_equation_cosmology.py"],
       ["All figures of this edition except the author's plates",
        "Field Ledger Second Edition/fl_diagrams.py and fl_charts.py"],
       ["The author's Colour Field and Helical Relativity plates",
        "carried across unchanged from the working science archive"]],
      [2.60, 4.34], size=8.6, raw=True)
grade("PROVED",
      "The reproduction map of the first edition named three locations that were "
      "not in the archive, so the central number was not reproducible from the "
      "book's own ledger. Every path above resolves to a file that exists, and "
      "the master script regenerates the four reported statistics from the "
      "displayed equations of Chapter twelve alone.")

chap("Appendix C", "References", None)
refs = [
    "Aghanim, N. et al. (Planck Collaboration). Planck 2018 results. VI. "
    "Cosmological parameters. Astronomy and Astrophysics 641, A6 (2020); "
    "arXiv:1807.06209.",
    "Abdul-Karim, M. et al. (DESI Collaboration). DESI DR2 Results II: "
    "Measurements of Baryon Acoustic Oscillations and Cosmological Constraints. "
    "Physical Review D 112, 083515 (2025); arXiv:2503.14738.",
    "Riess, A. G. et al. A Comprehensive Measurement of the Local Value of the "
    "Hubble Constant. Astrophysical Journal Letters 934, L7 (2022); "
    "arXiv:2112.04510.",
    "Einstein, A. Die Grundlage der allgemeinen Relativitätstheorie. Annalen der "
    "Physik 49, 769 (1916).",
    "Friedmann, A. Über die Krümmung des Raumes. Zeitschrift für Physik 10, 377 "
    "(1922).",
    "Gödel, K. An Example of a New Type of Cosmological Solutions of Einstein's "
    "Field Equations of Gravitation. Reviews of Modern Physics 21, 447 (1949).",
    "Penzias, A. A. and Wilson, R. W. A Measurement of Excess Antenna "
    "Temperature at 4080 Mc/s. Astrophysical Journal 142, 419 (1965).",
    "Noether, E. Invariante Variationsprobleme. Nachrichten von der Gesellschaft "
    "der Wissenschaften zu Göttingen (1918).",
    "Helmholtz, H. von. Über die physikalische Bedeutung des Princips der "
    "kleinsten Wirkung. Journal für die reine und angewandte Mathematik 100 "
    "(1887).",
    "Bertotti, B., Iess, L. and Tortora, P. A test of general relativity using "
    "radio links with the Cassini spacecraft. Nature 425, 374 (2003).",
    "Shields, J. Unified Mechanics, Corpus Edition, Fifth Printing (2026): A "
    "World of Distinctions; Universopedia; Formal Register; Technical Papers 13 "
    "and 17.",
    "Shields, J. The Depth of Traversal; From Chiral Wave Evolution to the "
    "Principle of Logical Action; The Rate Across the Scale (working traversal "
    "papers, 2026).",
    "Shields, J. Helical Relativity: Standing Account; Observer-Interior Quantum "
    "Colour Field; Forward Closure and associated computational certificates "
    "(working science archive, 2026).",
    "Shields, J. Addenda A01 to A09 to the Unified Mechanics corpus (2026), with "
    "computational certificates.",
]
for i, t in enumerate(refs, 1):
    para("%d.  %s" % (i, t), size=9, color=INK, after=5, line=1.16,
         indent=0.24, align=WD_ALIGN_PARAGRAPH.LEFT)

para("", size=1, after=16)
p = para("", size=1, after=10, align=WD_ALIGN_PARAGRAPH.CENTER)
_border(p, color="D8D8D8", sz=4, space=1)
para("THE LEDGER REMAINS OPEN", size=12, color=NAVY, bold=True,
     align=WD_ALIGN_PARAGRAPH.CENTER, after=6)
para("The next advance is not another synonym for the theory. It is the next "
     "equation that survives its own observational chain.",
     size=10.5, color=SLATE, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER,
     after=18, indent=1.1)
para("PROVENANCE", size=9, color=GOLD, bold=True,
     align=WD_ALIGN_PARAGRAPH.LEFT, after=4)
para("The Field Ledger, second edition, 30 July 2026. Rebuilt in the corpus "
     "house style from the compressed field edition of the same date. Every "
     "numerical value is regenerated from a certificate in SCI/ADDENDA and no "
     "measured value is used as an input to any framework quantity. Twenty-three "
     "figures are generated at print width by the two plate scripts in this "
     "folder; the seven Colour Field and Helical Relativity plates are the "
     "author's own, carried across unchanged. The frozen corpus is not modified "
     "by this volume.", size=8.5, color=SLATE, italic=True, after=0, raw=True)

doc.save(OUT)
print("saved:", OUT)
print("paragraphs", len(doc.paragraphs), "tables", len(doc.tables),
      "figures", FIGN[0])

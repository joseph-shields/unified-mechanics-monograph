# ═════════════════════════════════════════════════════════ TITLE
para("", after=40)
para("A WORKING THEORY BOOK  ·  SECOND EDITION", size=10, color=GOLD,
     align=WD_ALIGN_PARAGRAPH.CENTER, after=16)
para("Unified Mechanics", size=17, color=SLATE,
     align=WD_ALIGN_PARAGRAPH.CENTER, after=4, line=1.0)
para("The Field Ledger", size=34, color=NAVY, bold=True,
     align=WD_ALIGN_PARAGRAPH.CENTER, after=12, line=1.0, style="Title")
para("Modern cosmology through Logical Action, Helical Relativity and the "
     "Colour Field", size=12.5, color=SLATE, italic=True,
     align=WD_ALIGN_PARAGRAPH.CENTER, after=20, line=1.25)
para("JOSEPH SHIELDS", size=11.5, color=NAVY,
     align=WD_ALIGN_PARAGRAPH.CENTER, after=3)
para("UNIFIED MECHANICS RESEARCH PROGRAMME  ·  30 JULY 2026", size=8.5,
     color=GOLD, align=WD_ALIGN_PARAGRAPH.CENTER, after=24)

callout("What this book is", [
    "One book in which the framework is required to calculate, to draw, to "
    "compare, to refuse and to expose itself to defeat. The grammar appears "
    "only where the physics needs it.",
    "This is not a replacement for the corpus and it is not a catalogue of "
    "every proof. It is the single application-led route through the "
    "programme: the reader meets a recognised physical problem, sees the "
    "standard equation, watches the Unified Mechanics operation enter, and is "
    "shown the result, the grade and the remaining obligation.",
])

sub("What the second edition adds")
para("The first edition reported that one passage through the Colour Field, the "
     "helix and Personal Relativity removed a third of the joint residual of "
     "six cosmological observables, and read the near-one-third as a possible "
     "constant of traversal. Everything in that calculation reproduces. What "
     "has changed is the reading of it.")
para("The payment is not a constant. **It is a measurement of how much of the "
     "score has been taken at its correct type**, and it climbs every time one "
     "more type is read: 0.2076 with none read, %.4f with one, %.4f with two on "
     "average, %.4f with all three. One third is the value at one typed record "
     "out of three, which is exactly where the audit stood when the first "
     "edition went out. That is a sharper statement than a constant, it "
     "explains the leave-one-out behaviour without appealing to coincidence, "
     "and it tells the programme what to do next."
     % (RUNG[("tau",)]["payment"],
        (RUNG[("Omega_b", "tau")]["payment"]
         + RUNG[("Y_He", "tau")]["payment"]
         + RUNG[("Omega_b", "Y_He")]["payment"]) / 3,
        RUNG[("Omega_b", "Y_He", "tau")]["payment"]))
para("Every figure has been redrawn from the certificates. The Colour Field and "
     "Helical Relativity plates are carried across unchanged, because they are "
     "the working science; everything else is generated at print width from the "
     "JSON in the addenda folder, and the reproduction map at the back now "
     "points at files that exist.")

figure("fl_f01_rule.png",
       "The grade chain that governs every worked section. A reader should be "
       "able to locate any equation in this chain and see exactly where "
       "interpretation enters.")

sub("Reading convention")
para("A displayed equation may be standard physics, an exact internal identity, "
     "a conditional bridge, a proposed mechanism, a forecast or an open target. "
     "The status box immediately following it governs. The prose is not "
     "permitted to promote it silently.")

table(["Grade", "Meaning"],
      [["STANDARD", "Accepted background mathematics or published observation, "
        "used as a comparison surface."],
       ["PROVED", "Forced from declared framework premises or exact algebra."],
       ["CONDITIONAL", "Forced only after the named physical or mathematical "
        "condition is granted."],
       ["PROPOSED", "A physical interpretation or mechanism not yet forced by "
        "the formal layer."],
       ["FORECAST", "A numerical output exposed to later measurement."],
       ["OPEN", "A missing derivation, mechanism, network or experiment."],
       ["WITHDRAWN", "An earlier route retained in the ledger precisely because "
        "it no longer supports the theory."],
       ["READING", "An interpretation of a result the book has already "
        "established, offered as the sharpest available account of it."]],
      [1.16, 5.78], size=9.2)

sub("Contents")
table(["Part", "Title", "Route"],
      [["I", "The cosmological problem",
        "1. The sky as a ledger  ·  2. What the standard model computes"],
       ["II", "Logical Action",
        "3. Why logical order must survive  ·  4. Crowley and Glorpnorp"],
       ["III", "The mechanics",
        "5. The minimal update  ·  6. Chiral wave splitting  ·  7. Gödel and "
        "traversal depth"],
       ["IV", "The field",
        "8. Helical Relativity  ·  9. Equivalence  ·  10. Dark matter"],
       ["V", "Seeing the field",
        "11. The Colour Field  ·  12. The dictionary and the master readout"],
       ["VI", "Running cosmology",
        "13. The microwave background  ·  14. The Hubble basins  ·  "
        "15. Dark energy and the vacuum"],
       ["VII", "The scientific ledger",
        "16. What stands  ·  17. What would defeat it  ·  appendices"]],
      [0.56, 2.10, 4.28], size=9.2)


# ═════════════════════════════════════════════════════════ PART I
part("Part one", "The cosmological problem",
     "What modern cosmology measures, what it calculates, and what it still "
     "leaves as a set of named inputs.")

chap("Chapter one", "The sky as a ledger",
     "Begin with the observations, not with the vocabulary.")
para("Modern cosmology is an extraordinarily successful compression system. A "
     "handful of parameters propagates through general relativity, plasma "
     "physics, nuclear physics and statistical field theory to describe the "
     "expansion history, the microwave background, the abundance of light "
     "elements, the clustering of galaxies and the weak lensing of intervening "
     "matter. The success is real. The conceptual question is what those "
     "parameters are records of.")

figure("fl_f02_timeline.png",
       "The problem any new framework inherits: preserve the successful "
       "geometry and the observations while supplying a sharper operational "
       "account of the parameters.")

para("The standard model does not claim that Ω_b, Ω_c, n_s, τ or the "
     "dark-energy equation of state are self-explanatory objects. They are "
     "compact coordinates on a successful fit. Unified Mechanics enters only "
     "where it can supply a logical dependency that the fit does not already "
     "contain.")
grade("STANDARD",
      "Planck 2018 reports a spatially flat six-parameter ΛCDM fit with "
      "Ω_c h² = 0.120 ± 0.001, Ω_b h² = 0.0224 ± 0.0001, n_s = 0.965 ± 0.004, "
      "τ = 0.054 ± 0.007 and H_0 = 67.4 ± 0.5 km s⁻¹ Mpc⁻¹.")
grade("STANDARD",
      "DESI DR2 baryon acoustic oscillations are well described by flat ΛCDM but "
      "sit in mild tension with the parameters the microwave background prefers. "
      "Combinations with the background and with supernovae currently give a "
      "sample-dependent preference for evolving dark energy.")
grade("STANDARD",
      "The SH0ES Cepheid and supernova ladder reports "
      "H_0 = 73.04 ± 1.04 km s⁻¹ Mpc⁻¹ in its baseline analysis.")

callout("The scientific rule", [
    "A new framework is not helped by calling these measurements wrong. It has "
    "to show which standard equations it retains, which inputs it derives, "
    "which physical mechanisms it changes, and where a different prediction "
    "appears.",
])

chap("Chapter two", "What the standard model actually computes",
     "The microwave background is a dynamical calculation, not a row of fitted "
     "percentages.")
figure("fl_f03_pipeline.png",
       "The standard pipeline an alternative has to meet rather than gesture "
       "around. A stage may be derived or replaced, and either way the "
       "replacement carries the same obligation.")
para("For a homogeneous and isotropic background the first accounting equation "
     "is the Friedmann equation. The expansion rate is sourced by the total "
     "energy density, while each component evolves according to its equation of "
     "state and its interactions.")
eq("H²(a) = (8πG/3) ρ(a) − k c²/a²")
eq("ρ̇_i + 3H(ρ_i + p_i/c²) = Q_i ,      Σ_i Q_i = 0")
eq("E²(a) = Ω_r a⁻⁴ + Ω_m a⁻³ + Ω_k a⁻² + Ω_{DE} f(a)")
grade("STANDARD",
      "These equations define the background bookkeeping. They do not by "
      "themselves specify recombination, perturbation transfer, dark-matter "
      "microphysics or the origin of the primordial spectrum.")
para("The angular scale of the acoustic peaks is a ratio of two independently "
     "integrated distances: the sound horizon at last scattering, and the "
     "comoving angular-diameter distance to that surface.")
eq("θ_* = r_s(z_*) / D_M(z_*)")
eq("r_s(a_*) = ∫₀^{a_*} c_s(a) da / [a² H(a)]        "
   "D_M(a_*) = ∫_{a_*}^{1} c da / [a² H(a)]")
para("The full temperature and polarisation spectra need more than those "
     "background integrals. A Boltzmann hierarchy propagates coupled photon, "
     "baryon, neutrino and metric perturbations, while a recombination network "
     "supplies the visibility function. That distinction matters later: the "
     "forward solver of Chapter thirteen reaches the acoustic scale and the "
     "peak-location structure, and it does not yet produce a full spectrum.")
callout("What this book demands of itself", [
    "Every time the framework outputs a number, the book states whether it is "
    "an algebraic readout, an evolved field average, a background integral, a "
    "perturbation prediction, or a proposed physical interpretation.",
])


# ═════════════════════════════════════════════════════════ PART II
part("Part two", "Logical Action",
     "Why a physically adequate description has to preserve the distinctions "
     "that determine later evolution.")

chap("Chapter three", "The Principle of Logical Action",
     "Why endpoint agreement is too weak for physics.")
para("The Principle of Equivalent Action begins from a familiar fact: different "
     "written actions can generate the same Euler-Lagrange equations. Total "
     "derivatives, gauge representatives and field redefinitions can leave the "
     "resolved bulk dynamics unchanged. The invariant object is therefore an "
     "equivalence class of descriptions, not one privileged inscription.")
eq("S_1 ∼_E S_2   iff   E(S_1) = E(S_2)        [S]_E = { S′ : E(S′) = E(S) }")
para("But physical equivalence is always relative to what has been preserved. "
     "Two descriptions may agree on the final Euler-Lagrange operator while "
     "differing in boundary data, causal order, gauge reduction, phase, "
     "topology, measure, or the architecture that makes a result observable. "
     "Those differences can change what happens next. Logical Action is the "
     "requirement that the compressed description remain a valid dynamical "
     "quotient.")
figure("fl_f04_square.png",
       "The formal necessity behind Logical Action. A reduced state is adequate "
       "only when reduction and evolution commute.")
eq("π ∘ E_t = Ẽ_t ∘ π")
grade("PROVED",
      "If there exist x_1 and x_2 with π(x_1) = π(x_2) but "
      "π(E_t x_1) ≠ π(E_t x_2), then no single-valued reduced evolution Ẽ_t "
      "exists on the transcript. The omitted distinction is dynamically active.")
para("This is why the principle has to be followed rather than admired. A "
     "description that does not commute with evolution is not a simpler form of "
     "the same theory. It is a different state space, in which some physically "
     "distinct futures have been identified with each other. That can still be "
     "a useful approximation. It cannot be called lossless.")
eq("L(S) = (H, ≺, C, boundary, gauge, topology, measure, phase, record)")
eq("S_1 ∼_L S_2   iff   E(S_1) = E(S_2)  and  L(S_1) ≅ L(S_2)")
grade("PROVED",
      "The Principle of Logical Action refines an action class by the ordered "
      "distinctions required to reproduce its admissible evolution, its "
      "boundary response and its observation chain.")

chap("Chapter four", "Crowley and Glorpnorp",
     "The simplest test of whether a field has really been translated.")
figure("fl_f05_hotel.png",
       "The transmission problem. The receiver has the algebra and no "
       "independent sensory access to the hotel.")
para("Mr Crowley maintains a twenty-room hotel whose rooms contain lights, "
     "doors, occluders and paths. Glorpnorp is an alien who cannot see or hear "
     "the hotel but can read an algebraic transmission. Crowley succeeds only "
     "when Glorpnorp can answer the relevant questions and evolve the hotel "
     "state without being given a second visual explanation.")
para("A list of brightness values is not enough. Two hotels can have the same "
     "room-by-room brightness while differing in which bulb produced the light, "
     "which door is blocked, which beam crosses a corridor, which switch is "
     "causally upstream, and what will happen after the same intervention. The "
     "local snapshot survives while the relational field is lost.")
eq("F = (V, C, K, H, Q, U)")
table(["Component", "Meaning in the hotel", "Physical analogue"],
      [["V", "room values: brightness, temperature, occupancy",
        "local field values"],
       ["C", "adjacency, beam path, phase and source relations",
        "connection and relational structure"],
       ["K", "locked doors, forbidden transitions, conservation rules",
        "constraints and boundary conditions"],
       ["H", "the retained sequence of prior changes",
        "history, winding and traversal depth"],
       ["Q", "the questions the receiver must be able to answer",
        "task-relative observables"],
       ["U", "the rule that advances the state", "dynamics"]],
      [0.80, 3.30, 2.84], size=9.2, centre=(0,))
grade("PROVED",
      "A relationally incomplete local transcript cannot uniquely reproduce a "
      "field whenever the omitted relations alter later evolution. Snapshot "
      "preservation is not evolution preservation.")
para("The experiment earns the language. Rationality names the distinctions an "
     "account must preserve; Realisation names the operation that carries them; "
     "Observation names the record that checks it. A translation that omits "
     "dynamically active relations has not translated the field.")


# ═════════════════════════════════════════════════════════ PART III
part("Part three", "The mechanics",
     "From the minimal update to chiral propagation and traversal depth.")

chap("Chapter five", "The minimal update and the three roles",
     "The smallest recurrent operation from which the framework begins.")
para("The algebraic engine is a two-channel update in which the new outward "
     "value is the sum of the previous channels and the new retained value is "
     "the previous outward channel.")
figure("fl_f06_update.png",
       "The fixed ratio and the perfect-square partition. The three weights are "
       "the exact expansion of a square, so they sum to one with nothing "
       "adjusted.")
eq("(a, b) → (a+b, a)        [a_{n+1}; b_{n+1}] = [[1,1],[1,0]] [a_n; b_n]")
eq("φ² = φ + 1 ,       r = 1/(2φ) ,       u = 1 − r")
grade("PROVED",
      "The positive projective fixed ray of the update is the golden ratio. "
      "Once the two-sided reading r = 1/(2φ) is declared, the three weights are "
      "the exact square (u+r)² = u² + 2ur + r² = 1.")
eq("W_L = u² = %.12f        W_B = 2ur = %.12f        W_M = r² = %.12f"
   % (W_L, W_B, W_M), size=10.5)
grade("PROPOSED",
      "Light, Boundary and Matter are names for the three algebraic roles. The "
      "names become physical only through a realisation map that reproduces "
      "propagation, relation and retention in an observable system.")
para("The middle term is structurally special. It exists only as the product of "
     "different poles and it carries both orderings. In the later field "
     "language that is why the Boundary channel is used for interference, "
     "connection, phase transport and closure. That interpretation is not "
     "imported back into the algebra as a proof.")
para("Two exact relations inside the partition are worth having in hand before "
     "the dictionary arrives, because they are what the polynomial forms hide:")
eq("W_L / W_M = 5        exactly, since u/r = √5")
eq("W_M · W_L − (W_B/2)² = 0        exactly")
para("The main cosmological dictionary will read baryon density from half the "
     "retained weight, cold dark matter from the Boundary weight damped by one "
     "golden factor, and dark energy as the complement. The logical order is "
     "already visible: the partition is exact first, and the observable "
     "dictionary is a later hypothesis tested against measurement.")

chap("Chapter six", "Chiral wave splitting",
     "Not supersymmetry: characteristic propagation, frozen phase and "
     "equivalent action.")
figure("fl_f07_chiral.png",
       "The chiral construction used in this book. It is a wave decomposition "
       "and an action reconstruction, with no superpartner anywhere in it.")
para("A two-dimensional wave equation factorises along characteristic "
     "coordinates. With u = τ + σ and v = τ − σ, the general solution separates "
     "into left-moving and right-moving components.")
eq("∂_u ∂_v X = 0        X(τ, σ) = X_L(τ+σ) + X_R(τ−σ)")
grade("STANDARD",
      "The left and right split follows from characteristic factorisation of "
      "the wave equation. No supersymmetry algebra, superpartner or "
      "fermion-boson pairing is involved.")
para("Unified Mechanics treats the split as an operational beginning rather "
     "than an endpoint. A spatial slice retains a phase relation between the "
     "counter-propagating sectors, and finite mode expansion turns that "
     "retained relation into a first-order evolution operator.")
eq("dψ/dτ = −i Ω Γ ψ        ψ(τ) = exp(−i Ω Γ τ) ψ(0)        G[q] = q̈ + Ω² q")
grade("PROVED",
      "Given the finite-mode linear generator and the standard inverse "
      "variational conditions, the quadratic action is a representative that "
      "returns the governing oscillator operator.")
grade("PROPOSED",
      "The further identification of chiral retention with the framework's "
      "Light, Boundary and Matter channels is a physical mapping. It has to be "
      "tested through the spectrum, the couplings and the observable handedness "
      "it produces.")
para("Logical Action matters here because a sum of endpoint amplitudes does not "
     "preserve which phase arrived from which characteristic branch. "
     "Interference, winding and later coupling depend on that ordered "
     "relation. Erasing the split after forming the sum is legitimate only for "
     "questions proved insensitive to chirality.")

chap("Chapter seven", "Gödel, recurrence and traversal depth",
     "How a path can close in projection without restoring the same complete "
     "state.")
para("Gödel spacetime is a legitimate solution of the Einstein equations "
     "containing closed timelike curves. Unified Mechanics does not remove that "
     "geometry by declaration, and the simply connected topology of the usual "
     "Gödel manifold means an ordinary universal-cover argument does not open "
     "the curves. The resolution attacks a different inference: that return to "
     "the same spacetime event is return to the same complete physical state.")
eq("γ : [0, T] → M ,       γ(T) = γ(0)")
eq("Δτ = ∫₀^T √(−g_{μν} γ̇^μ γ̇^ν) dλ  >  0")
figure("fl_f08_godel.png",
       "The circle is the spacetime projection; the helix is the lifted state, "
       "including the accumulated traversal or retained record.")
para("Event coincidence and elapsed proper time are different invariants. The "
     "same distinction is elementary in the covering map p(s) = exp(is): the "
     "images agree while the unwrapped parameters differ. Unified Mechanics "
     "adds a record coordinate, a traversal depth, to the state, so the return "
     "closes in the projection and does not close in the lifted account.")
eq("p(s) = exp(i s) ,     p(s + 2πn) = p(s) ,     H(s) = (R cos s, R sin s, h s)")
eq("complete state = (spacetime event, phase, retained history)")
grade("PROVED",
      "For any state description augmented by a strictly increasing traversal "
      "coordinate, equality of the spacetime projection does not imply equality "
      "of the augmented state.")
grade("PROPOSED",
      "Physical reality retains enough history that a closed timelike "
      "projection cannot count as literal restoration of the same total system. "
      "This is the framework's resolution of the paradox, and not a proof that "
      "the Gödel metric lacks closed timelike curves.")
callout("What is claimed here", [
    "The argument dissolves “same event, therefore same complete "
    "occurrence”. It does not alter the local solution of general "
    "relativity, and it does not pretend that topology alone opens Gödel "
    "curves.",
])

chap("Chapter twelve", "The dictionary and the master readout",
     "From a static partition to colour state, helical order, a "
     "Personal-Relativity average, and one number per observable.",
     brk=True)
para("The old corpus evaluates each cosmological dictionary entry at the fixed "
     "pole r. The Colour Average lets that pole move under the declared update. "
     "The master readout adds the two instruments that the earlier calculation "
     "left standing beside the average: helical realisation supplies an ordered "
     "turn scale, and Personal Relativity supplies the resolution weight. The "
     "result is one typed measurement pipeline rather than three neighbouring "
     "metaphors.")

table(["Observable", "Dictionary form", "Value", "Working interpretation"],
      [["Ω_b", "W_M / 2", "%.9f" % (W_M/2), "half the retained Matter weight"],
       ["Ω_c", "W_B / φ", "%.9f" % (W_B/phi),
        "the Boundary weight damped by one fixed ratio"],
       ["Y_{He}", "W_L / 2", "%.9f" % (W_L/2),
        "half the outward Light weight"],
       ["N_{eff}", "3 + W_M / 2", "%.9f" % (3 + W_M/2),
        "three channels plus one baryon share"],
       ["n_s", "1 − W_M(1−2r)", "%.9f" % (1 - W_M*(1-2*r)),
        "unity less the retained weight at the leak rate"],
       ["τ", "2 r³", "%.9f" % (2*r3), "the static optical-depth entry"],
       ["Ω_{DE}", "1 − Ω_b − Ω_c", "%.9f" % (1 - W_M/2 - W_B/phi),
        "the closure complement"]],
      [0.82, 1.42, 1.36, 3.34], size=9.0, mono=(1, 2), centre=(0, 1, 2))
grade("PROVED",
      "Each dictionary value follows exactly from r, u and the stated map. The "
      "symmetry Y_{He}/W_L = Ω_b/W_M = 1/2 is a relation the polynomial forms "
      "hide.")
grade("PROPOSED",
      "The dictionary map itself is the cosmological identification being "
      "tested. It is not forced by the partition theorem alone.")

sub("The operator, and what each algebra is permitted to supply")
para("The Colour Average asks whether a curved observable should be evaluated at "
     "one fixed point or averaged over the states the declared evolution "
     "actually visits. The master calculation keeps that evolution, colours "
     "every state, uses the helical realisation count as its ordered position "
     "scale, and lets Personal Relativity weight each local reading by how "
     "sharply that colour step is resolved.")
eq("C_O(t) = [ O(x_t), θ_O(x_t) ]        Δθ_t = | Arg exp i(θ_t − θ_{t−1}) |")
eq("N_O(t) = 360 T_O / Δθ_t        H_5(N) = 2s^{10}/(1+s^{10}) ,   s = N/(N+1)")
eq("R[O] = Σ_t H_5(N_O(t)) · O(C_O(t))  /  Σ_t H_5(N_O(t))")
figure("fl_f19_operator.png",
       "The master operator, with each algebra restricted to what it may supply. "
       "Three of the four qualify the reading and exactly one of them returns a "
       "value.")
callout("What each algebra contributes, and why the order matters", [
    "Colour supplies the instantaneous field condition and its angular "
    "temperature. The helix supplies ordered traversal and the discrete "
    "realisation count T. Personal Relativity turns position over spread into "
    "the resolution N and therefore into the averaging kernel H_5.",
    "This ordering was arrived at by getting it wrong first. An earlier version "
    "of the calculation treated all four instruments as competing estimators "
    "and let H_5 **multiply the prediction**, on the reading that a less "
    "resolved observer should see a degraded value. None of the observables came "
    "out closer. **Read instead as a measure on the path**, H_5 is the "
    "averaging kernel, and nothing in the combination step is chosen: every "
    "weight comes from the framework.",
])
grade("READING",
      "A resolution is a property of the comparison, not of the quantity being "
      "compared. So it belongs in the measure and not in the value, and the "
      "difference between those two placements is the difference between an "
      "instrument and a fudge factor.")

para("The conversion from turns to degrees follows from the same reading. The "
     "spread in N = 360 T / Δθ is the hue displacement across **one traversal**, "
     "not a global spread over the whole flow. Read globally it over-corrects; "
     "read per step it is the ratio of the total angle of the realisation to the "
     "angle moved in one step, which is what a resolution is.")

figure("fl_f20_reach.png",
       "Which entries the weighting can reach. One zero in the channel "
       "signature and the hue cannot move, so the weight is one by structure.")
para("Four of the six entries have a zero in their channel signature. A monomial "
     "in the two poles has a constant signature, and with one component zero the "
     "weighted circular mean is that channel's own hue whatever the composition "
     "weights do. So Δθ vanishes identically, N is unbounded, and the weight is "
     "one. Only Ω_c and Ω_{DE} are mixed, and only they are weighted.")
grade("PROVED",
      "The reduction of the master operator to the plain Colour Average on the "
      "pure entries is an identity, not an approximation. That is why four "
      "entries carry the same value in both evolved columns.")

sub("Optical depth is a different kind of object")
para("Optical depth is not a state variable of the same type as a density "
     "fraction. In standard cosmology it is already an accumulated "
     "line-of-sight integral. Logical Action therefore requires its three "
     "traversal-retention factors to stay **inside** the object being averaged, "
     "rather than comparing a static endpoint against a path measurement.")
eq("τ = ∫ n_e σ_T c dt        O_τ(C_t) = 2 m(t)³ (1 − r³)³")
para("Left untyped, the evolution moves τ the wrong way, from %+.4f σ to %+.4f σ, "
     "because all three matter-channel entries are convex so averaging raises "
     "them, and τ already sat above measurement. Carrying the retention factors "
     "inside brings it to %+.4f σ. The factor is fixed by the standard "
     "definition of the observable and by the three closures already fixed over "
     "the same interval by the Hubble basins, so there was nothing in it "
     "available to be tuned."
     % (BY["tau"]["pull_static"], BY["tau"]["pull_colour"],
        BY["tau"]["pull_master"]))
grade("READING",
      "A mechanism that improved every entry by the same device would be a free "
      "parameter in disguise. τ moved the wrong way under the plain average "
      "precisely because the plain average was being applied to the wrong kind "
      "of object, and that is how the type error announced itself.")

sub("One number per observable")
figure("fl_f21_pulls.png",
       "Every entry, read three ways. Each bar runs from the static dictionary "
       "value to the typed master reading; the gold pip is the plain Colour "
       "Average, which coincides with the master for the four pure entries.")
table(["Observable", "static", "Colour Average", "typed master", "measured",
       "pull now"],
      [[NAME[k], "%.7f" % BY[k]["static"], "%.7f" % BY[k]["colour"],
        "**%.7f**" % BY[k]["master"], "%.7f" % BY[k]["measured"],
        "**%+.4f**" % BY[k]["pull_master"]] for k in ORDER],
      [0.94, 1.22, 1.30, 1.30, 1.22, 0.96], size=9.0,
      mono=(1, 2, 3, 4, 5), centre=(0, 1, 2, 3, 4, 5),
      colours={(i, 5): TEAL for i in range(len(ORDER))})
para("**Every entry moves toward measurement.** Six of six. The mean absolute "
     "pull falls from %.4f σ to %.4f σ and the mean absolute percentage residual "
     "from %.3f to %.3f per cent, with one local resolution equation used "
     "throughout and no quantity fitted anywhere. The gain does not come from "
     "choosing a separate formula per parameter: τ receives a path factor "
     "because τ is a path integral by definition, and the two mixed entries "
     "receive a weight because they are the two entries whose colour moves."
     % (A09["E0_static"], A09["E1_master"],
        sum(abs(100*(BY[k]["static"]/BY[k]["measured"]-1)) for k in ORDER)/6,
        sum(abs(100*(BY[k]["master"]/BY[k]["measured"]-1)) for k in ORDER)/6))
grade("CONDITIONAL",
      "The physical status still depends on deriving the stochastic update and "
      "the colour-temperature map from a common field action. What is "
      "established here is that the typed operator regenerates deterministically "
      "from the certificate and that it moves every entry in the right "
      "direction.")

sub("The traversal payment")
para("Normalise the old static discrepancy to one whole unresolved record. After "
     "the complete passage from field state to realised record, the retained "
     "discrepancy is the ratio of the two mean absolute pulls, and what the "
     "traversal paid is its complement.")
eq("P_T = (E_0 − E_1)/E_0 = 1 − E_1/E_0")
eq("E_0 = %.4f σ        E_1 = %.4f σ        P_T = %.6f"
   % (A09["E0_static"], A09["E1_master"], A09["traversal_payment"]))
figure("fl_f22_payment.png",
       "What one complete traversal pays, with one third marked where it falls. "
       "The evolution alone reaches %.4f σ; correcting the type of the optical "
       "depth supplies the remainder." % A09["E_colour"])
grade("PROVED",
      "For the declared six-observable score the reduction is %.6f of the old "
      "residual, leaving %.6f. Both regenerate deterministically from the flow, "
      "the hue map, the turn counts and the operator."
      % (A09["traversal_payment"], 1 - A09["traversal_payment"]))
para("The first edition observed that %.6f sits within %.2f percentage points of "
     "one third, and read that as the payment of one complete traversal: a "
     "possible constant, pending repetition in independent sectors. The "
     "arithmetic was right. The reading was one step short, and the step is "
     "available on the ensemble already in hand."
     % (A09["traversal_payment"],
        abs(100*(A09["traversal_payment"] - 1/3))))

sub("What the payment is actually measuring")
para("Three of the six entries in the score are **records** rather than states. "
     "Optical depth is a line-of-sight integral. Ω_b and Y_{He} are the two "
     "half-weights, each a weight read across a boundary. At the time of the "
     "first edition exactly one of those three had been typed. Type them one at "
     "a time and read the payment at each stage.")
figure("fl_f23_ladder.png",
       "The payment measures how much of the score has been taken at its "
       "correct type. It rises with every type read, strictly, so it can be "
       "read back to the count.")
table(["Records typed", "Which", "mean |pull|", "P_T"],
      [[str(L["n_typed"]),
        ", ".join(NAME[t] for t in L["typed"]) or "nothing typed",
        "%.4f" % L["mean_abs_pull"], "**%.4f**" % L["payment"]]
       for L in LAD["rungs"]],
      [1.16, 2.10, 1.60, 2.08], size=9.0, centre=(0, 2, 3),
      colours={(i, 3): TEAL for i in range(len(LAD["rungs"]))})
grade("PROVED",
      "The payment is strictly increasing in the number of records typed and no "
      "rung overlaps its neighbour, so the payment determines the count. The "
      "tightest join is between one typed and two typed, which clear each other "
      "by 0.0010. The rung means are %s, an increment of %.4f per type read."
      % (", ".join("%.4f" % (sum(L["payment"] for L in LAD["rungs"]
                                 if L["n_typed"] == k)
                             / max(1, sum(1 for L in LAD["rungs"]
                                          if L["n_typed"] == k)))
                   for k in range(4)),
         (RUNG[("Omega_b", "Y_He", "tau")]["payment"]
          - RUNG[()]["payment"]) / 3))
callout("The reading", [
    "**The traversal payment is not a constant of traversal. It is a "
    "measurement of how much of the score has been read at its correct type.** "
    "One third is the value at one typed record out of three, which is where "
    "the audit stood when the first edition went out.",
    "That is a stronger statement than a constant, for three reasons. It is "
    "invertible, so the payment can be used to count how many types remain "
    "unread. It predicts the leave-one-out behaviour of the next section "
    "without any appeal to coincidence. And it converts an observation into an "
    "instruction: the way to raise the payment is to read a type, and the "
    "programme knows which types are left.",
])
grade("READING",
      "The linearity of the rung means is arithmetic rather than discovery: a "
      "mean is a linear functional and each typing shifts one term by a fixed "
      "amount. What is not automatic is the **separation** of the rungs, and "
      "that is what makes the payment a usable counter.")

sub("Varying the ensemble")
para("The payment is a ratio of two means over one chosen ensemble, so the "
     "ensemble is the thing to vary. The sharpest version removes one entry at a "
     "time.")
figure("fl_f24_loo.png",
       "Removing one entry at a time. Five of six deletions leave the payment "
       "inside the band; the sixth removes the untyped record, which does the "
       "same arithmetic work as typing it.")
table(["Removed", "P_T without it", "Distance from a third", "Reading"],
      [[NAME[k], "%.4f" % A09["leave_one_out"][k],
        "%.4f" % abs(A09["leave_one_out"][k] - 1/3),
        "inside the band" if abs(A09["leave_one_out"][k] - 1/3) < 0.05
        else "**the untyped record.** Removing it acts like typing it, so the "
             "payment rises, exactly as the ladder says"]
       for k in ORDER],
      [0.92, 1.30, 1.46, 3.26], size=8.8, centre=(0, 1, 2),
      colours={(i, 3): (TEAL if abs(A09["leave_one_out"][k] - 1/3) < 0.05
                        else GOLD) for i, k in enumerate(ORDER)})
figure("fl_f25_subsets.png",
       "Every subset of size three or more. The split at size three is by "
       "whether the subset contains an untyped record, which is the ladder read "
       "from a different direction.")
para("Across all %d subsets of size three or more the median is %.4f. Within "
     "0.05 of a third: five of six at size five, four of fifteen at size four, "
     "and none of twenty at size three, where the values split either side of "
     "the band and the median falls in the gap between the two groups. A mean "
     "over three items has that variance regardless, so the sweep does not "
     "settle anything by itself. What it does show is that the bimodality has a "
     "cause, and the cause is the same one: which records in the subset have "
     "been typed."
     % (A09["subsets"]["n"], A09["subsets"]["median"]))
grade("OPEN",
      "The decisive test is repetition in a sector that shares no observables "
      "with this one, scored under the same typing rule declared in advance. The "
      "ladder makes that test sharper than the first edition could: it predicts "
      "not one number but a monotone sequence, indexed by how many records the "
      "new sector has typed.")

sub("The two half-weights")
para("The ladder says what to do next, and the last rung is worth showing "
     "because it is where the score would stand once the audit is complete. The "
     "two entries the passage does not reach are exactly the two half-weights, "
     "Ω_b = W_M/2 and Y_{He} = W_L/2. One rule rather than two corrections: a "
     "half-weight is a weight read across the boundary and picks up the "
     "structural floor once.")
eq("Ω_b = W_M/2        Y_{He} = W_L/2        each divided by (1 − r³)")
figure("fl_f26_halfweight.png",
       "Reading the two half-weights at the boundary. The dark energy fraction "
       "also improves although the rule never touches it, only its closure.")
table(["Observable", "typed master", "with both half-weights read", "note"],
      [[NAME[k], "%+.4f" % BY[k]["pull_master"], "**%+.4f**" % CAND["pulls"][k],
        ("read at the boundary" if k in ("Omega_b", "Y_He")
         else ("moved only through the closure" if k == "Omega_DE"
               else "unchanged"))] for k in ORDER]
      + [["**mean |pull|**", "%.4f" % A09["E1_master"],
          "**%.4f**" % CAND["mean_abs_pull"], "every entry inside one sigma"],
         ["**payment P_T**", "%.4f" % A09["traversal_payment"],
          "**%.4f**" % CAND["payment"], "all three records typed"]],
      [1.24, 1.28, 1.72, 2.70], size=8.8, centre=(0, 1, 2))
para("The rule touches exactly two entries, with one factor, in one direction, "
     "and it exempts nothing. Ω_{DE} improves although the rule never touches "
     "it and reaches it only through the closure identity, which is what a "
     "structural correction looks like rather than a per-parameter one. Every "
     "entry lands inside one sigma and the mean absolute pull falls to %.4f."
     % CAND["mean_abs_pull"])
grade("READING",
      "This rung was found by reading the residual, which is the one way of "
      "finding a rule that cannot then be used to support it. Under the ladder "
      "that is not a disqualification but a position: it is a candidate typing "
      "with the right shape and no derivation yet.")
grade("OPEN",
      "Derive the boundary factor for a half-weight without consulting these "
      "residuals. The forward solver of Chapter thirteen is the natural place to "
      "test it, because it reads Ω_b at the pole and its acoustic-scale solution "
      "is sensitive to the difference. Until that derivation exists, the working "
      "readout of this book is the typed master at %.4f σ, not the last rung."
      % A09["E1_master"])
callout("Not a licence to select by hindsight", [
    "The typed rule is frozen for this edition. A later dataset has to be "
    "evaluated with the same state and path typing, the same turn counts and "
    "the same kernel. If it fails, the rule is revised openly or rejected. It "
    "is not switched parameter by parameter.",
    "The ladder makes that discipline easier rather than harder, because it "
    "separates the two questions that used to be one. **Whether the operator "
    "works** is settled by the six entries moving together. **How far the "
    "audit has got** is what the payment reports, and it is allowed to change "
    "as the audit proceeds.",
])
para("A second route to the scalar tilt appears in the traversal-rate work, "
     "n_s = 1 + ln(1−r³) = %.5f, and it is not algebraically identical to the "
     "dictionary value %.5f. The two routes stay separate until a theorem shows "
     "that they refer to different resolutions, or one of them is superseded."
     % (1 + math.log(1-r3), BY["n_s"]["master"]))
grade("OPEN",
      "Explain the relation between the master field-dictionary tilt and the "
      "constant-retention flow tilt. Numerical proximity is not a derivation.")

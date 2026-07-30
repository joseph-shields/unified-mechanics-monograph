"""The Field Ledger, second edition: the measured charts.

Every number here comes from a certificate in SCI/ADDENDA. Nothing is redrawn
from the earlier plates by eye.
"""
from fl_base import *

LAD = A09["typing_ladder"]


# ══════════════════════════════════════════════ F19 the operator's roles
def f19_operator():
    stages = [
        ("COLOUR", MATTER_C, "hue $\\theta$ at the state\nand its step "
         "$\\Delta\\theta$", "supplies the\nANGULAR SPREAD"),
        ("HELIX", GOLD, "turns $T$ to lock\non the attractor",
         "supplies the\nTRAVERSAL COUNT"),
        ("RELATIVITY", BOUND_C, "$N = 360\\,T/\\Delta\\theta$\n"
         "$H_5 = 2s^{10}/(1{+}s^{10})$", "supplies the\nWEIGHT"),
        ("ACTION", TEAL, "$R[O] = \\Sigma H_5 O \\,/\\, \\Sigma H_5$",
         "supplies the\nNUMBER"),
    ]
    GX = 0.13
    BW = (W - 0.36 - 3 * GX) / 4
    BH, RH = 1.00, 0.44
    H = 0.62 + BH + RH + 0.68
    fig, ax = canvas(W, H)
    head(ax, W, H, "THE MASTER OPERATOR AND WHAT EACH ALGEBRA SUPPLIES",
         "three of the four qualify the reading; exactly one of them returns a "
         "value")
    yb = H - 0.62 - BH
    for i, (nm, col, body, role) in enumerate(stages):
        x = 0.18 + i * (BW + GX)
        tint(ax, x, yb, BW, BH, col, a=0.09)
        box(ax, x, yb, BW, BH, col, fill="none", lw=1.0)
        ax.add_patch(FancyBboxPatch((x, yb + BH - 0.25), BW, 0.25,
                                    boxstyle="round,pad=0,rounding_size=0.03",
                                    linewidth=0, facecolor=col, alpha=0.88,
                                    zorder=3))
        ax.text(x + BW / 2, yb + BH - 0.125, nm, ha="center", va="center",
                fontsize=8.2, color="white", weight="bold", zorder=4)
        ax.text(x + BW / 2, yb + (BH - 0.25) / 2, body, ha="center",
                va="center", fontsize=7.6, color=INK, linespacing=1.65)
        ax.text(x + BW / 2, yb - RH / 2, role, ha="center", va="center",
                fontsize=6.9, color=col, weight="bold", linespacing=1.55)
        if i < 3:
            arrow(ax, x + BW + 0.018, yb + BH / 2, x + BW + GX - 0.018,
                  yb + BH / 2, lw=1.0)
    foot(ax, W, [
        ("Only one algebra estimates. The others qualify: a spread, a count and "
         "a weight.", None),
        ("Read as a measure on the path, $H_5$ is the averaging kernel, and "
         "nothing in the combination step is chosen.", GOLD),
    ], y=0.34)
    save(fig, "fl_f19_operator.png")


# ══════════════════════════════════════════════ F20 what the weighting reaches
def f20_reach():
    RH, gap = 0.21, 0.085
    n = len(ORDER)
    H = 0.62 + n * RH + (n - 1) * gap + 0.54
    fig, ax = canvas(W, H)
    head(ax, W, H, "WHICH ENTRIES THE WEIGHTING REACHES",
         "one zero in the channel signature and the hue cannot move, so "
         "$\\Delta\\theta = 0$ and $H_5 = 1$ by structure")
    x0, LW = 1.02, 1.34
    top = H - 0.62
    for i, k in enumerate(ORDER):
        d = BY[k]
        y = top - i * (RH + gap) - RH
        ax.text(0.92, y + RH / 2, M[k], ha="right", va="center", fontsize=9.4,
                color=NAVY)
        col = SLATE if d["pure"] else BOUND_C
        tint(ax, x0, y, LW, RH, col, a=0.13 if d["pure"] else 0.16)
        box(ax, x0, y, LW, RH, LINE if d["pure"] else BOUND_C, fill="none",
            lw=0.75)
        ax.text(x0 + LW / 2, y + RH / 2,
                "PURE  ·  one channel" if d["pure"]
                else "MIXED  ·  two channels", ha="center", va="center",
                fontsize=7.0, color=col, weight="bold")
        note = ("$\\Delta\\theta = 0$,  $N = \\infty$,  $H_5 = 1$   ·   the "
                "weighting has nothing to weight" if d["pure"] else
                "hue moves with the state   ·   $T = %d$ turns   ·   $H_5$ "
                "weights it" % d["T"])
        ax.text(x0 + LW + 0.13, y + RH / 2, note, ha="left", va="center",
                fontsize=7.0, color=SLATE if d["pure"] else INK)
    foot(ax, W, [
        ("This is why four entries in the dictionary carry the same value in "
         "both evolved columns. It is structure, not omission.", None),
        ("$\\tau$ is pure too. It moves because its TYPE is corrected, which is "
         "a different operation entirely.", GOLD),
    ], y=0.32)
    save(fig, "fl_f20_reach.png")


# ══════════════════════════════════════════════ F21 every entry, every reading
def f21_pulls():
    fig, ax = chart(2.30, "EVERY ENTRY MOVES TOWARD MEASUREMENT",
                    "hollow = the static dictionary   ·   gold pip = the "
                    "colour average   ·   filled = the typed master   ·   "
                    "band is one $\\sigma$",
                    ["All six improve. The mean absolute pull falls from "
                     "%.4f$\\sigma$ to %.4f$\\sigma$ with no fitted quantity "
                     "anywhere."
                     % (A09["E0_static"], A09["E1_master"]),
                     "$\\tau$ is the entry whose type is corrected; $Y_{He}$ is "
                     "the entry whose type has not yet been read."])
    n = len(ORDER)
    ys = np.arange(n)[::-1]
    ax.axvspan(-1, 1, color=TEAL, alpha=0.07, zorder=0)
    ax.axvline(0, color=SLATE, lw=0.9, zorder=1)
    for v in (-2, -1, 1):
        ax.axvline(v, color=LINE, lw=0.6, ls=(0, (3, 3)), zorder=1)
    for i, k in enumerate(ORDER):
        d = BY[k]
        y = ys[i]
        a, b, c = d["pull_static"], d["pull_colour"], d["pull_master"]
        ax.plot([a, c], [y, y], color=LINE, lw=5.0, solid_capstyle="round",
                zorder=2)
        ax.plot([a], [y], marker="o", ms=5.2, color="white", mec=SLATE,
                mew=1.1, zorder=4)
        ax.plot([c], [y], marker="o", ms=7.6, color=TEAL, mec="white", mew=1.0,
                zorder=5)
        ax.plot([b], [y], marker="s", ms=2.3, color=GOLD, zorder=6)
        ax.text(c, y + 0.32, "%+.2f" % c, ha="center", va="bottom",
                fontsize=6.9, color=TEAL, weight="bold")
    ax.set_yticks(ys)
    ax.set_yticklabels([M[k] for k in ORDER], fontsize=9.6, color=NAVY)
    ax.tick_params(axis="y", length=0, pad=6)
    ax.set_xlim(-2.68, 1.42)
    ax.set_ylim(-0.72, n - 0.22)
    ax.set_xlabel("pull against measurement, in $\\sigma$", fontsize=8,
                  color=SLATE, labelpad=5)
    save(fig, "fl_f21_pulls.png")


# ══════════════════════════════════════════════ F22 the payment
def f22_payment():
    E0, Ec, E1 = A09["E0_static"], A09["E_colour"], A09["E1_master"]
    PT = A09["traversal_payment"]
    BH = 0.42
    H = 0.62 + 0.26 + BH + 0.34 + 0.58
    fig, ax = canvas(W, H)
    head(ax, W, H, "WHAT ONE COMPLETE TRAVERSAL PAYS",
         "the fraction of the joint residual of six observables that the passage "
         "removes")
    x0, x1 = 0.66, W - 0.52
    span = x1 - x0
    yb = H - 0.62 - 0.26 - BH
    xt = x0 + span * THIRD
    ax.plot([xt, xt], [yb - 0.10, yb + BH + 0.10], color=GOLD, lw=1.5, zorder=6)
    ax.text(xt, yb + BH + 0.16, "one third", ha="center", va="bottom",
            fontsize=7.6, color=GOLD, weight="bold")
    tint(ax, x0, yb, span, BH, SLATE, a=0.10)
    box(ax, x0, yb, span, BH, LINE, fill="none", lw=0.8)
    wp = span * PT
    ax.add_patch(FancyBboxPatch((x0, yb), wp, BH,
                                boxstyle="round,pad=0,rounding_size=0.03",
                                linewidth=0, facecolor=TEAL, alpha=0.82,
                                zorder=3))
    ax.text(x0 + wp / 2, yb + BH / 2, "PAID  %.4f" % PT, ha="center",
            va="center", fontsize=8.8, color="white", weight="bold", zorder=4)
    ax.text(x0 + wp + (span - wp) / 2, yb + BH / 2,
            "RETAINED  %.4f" % (1 - PT), ha="center", va="center",
            fontsize=8.8, color=SLATE, weight="bold", zorder=4)
    ax.text(x0, yb - 0.20, "$E_0$ = %.4f $\\sigma$" % E0, ha="left",
            va="center", fontsize=7.8, color=SLATE)
    ax.text(x1, yb - 0.20, "$E_1$ = %.4f $\\sigma$" % E1, ha="right",
            va="center", fontsize=7.8, color=TEAL, weight="bold")
    foot(ax, W, [
        ("$P_T = 1 - E_1/E_0 = %.6f$, which is one third to within %.2f "
         "percentage points." % (PT, abs(100 * (PT - THIRD))), None),
        ("The evolution alone reaches %.4f $\\sigma$; correcting the type of "
         "$\\tau$ supplies the remainder." % Ec, GOLD),
    ], y=0.32)
    save(fig, "fl_f22_payment.png")


# ══════════════════════════════════════════════ F23 THE TYPING LADDER
def f23_ladder():
    """The centre of the second edition.

    The payment is not one number. It is a reading of how much of the score has
    been taken at its correct type, and it climbs every time one more is read.
    """
    fig, ax = chart(2.36, "THE PAYMENT MEASURES HOW MUCH HAS BEEN TYPED",
                    "three entries in the score are records rather than states; "
                    "type them one at a time and read the payment",
                    ["Strictly increasing, so the payment reads back the number "
                     "of records typed. The one-typed and two-typed rungs clear "
                     "each other",
                     "by only 0.0010, which is the tightest join in the ladder. "
                     "One third is the reading at one typed record out of three."],
                    left=0.90)
    rungs = LAD["rungs"]
    NM = {"tau": "$\\tau$", "Omega_b": "$\\Omega_b$", "Y_He": "$Y_{He}$"}
    ax.axhspan(THIRD - 0.006, THIRD + 0.006, color=GOLD, alpha=0.35, zorder=1)
    ax.axhline(THIRD, color=GOLD, lw=1.3, zorder=2)
    by_n = {}
    for L in rungs:
        by_n.setdefault(L["n_typed"], []).append(L)
    # the mean bars of the first pass ran straight through the points they were
    # summarising. The trend line alone carries the same information.
    means = [float(np.mean([L["payment"] for L in by_n[k]]))
             for k in sorted(by_n)]
    ax.plot(sorted(by_n), means, color=NAVY, lw=1.0, ls=(0, (4, 3)), zorder=3)
    for k in sorted(by_n):
        g = sorted(by_n[k], key=lambda L: L["payment"])
        for j, L in enumerate(g):
            off = 0.0 if len(g) == 1 else (j - (len(g) - 1) / 2) * 0.42
            x = k + off
            ax.plot([x], [L["payment"]], marker="o", ms=7.6, color=TEAL,
                    mec="white", mew=1.0, zorder=5)
            # neighbouring rungs come within 0.0010 of each other, so a label
            # placed by x offset alone still collides. Both labels for a point
            # go on ONE side, and the side alternates along the rung.
            up = (j % 2 == 0)
            v0 = 0.020 if up else -0.020
            v1 = 0.058 if up else -0.058
            va0 = "bottom" if up else "top"
            # and the two points either side of a rung join are anchored so
            # their text runs AWAY from the join, not into it
            ha = "center"
            if len(g) > 1:
                ha = "left" if j == 0 else ("right" if j == len(g) - 1
                                            else "center")
            ax.text(x, L["payment"] + v0, "%.4f" % L["payment"], ha=ha,
                    va=va0, fontsize=6.6, color=TEAL, weight="bold")
            lab = ", ".join(NM[t] for t in L["typed"]) or "nothing typed"
            ax.text(x, L["payment"] + v1, lab, ha=ha, va=va0,
                    fontsize=6.7, color=SLATE)
    step = means[1] - means[0]
    ax.text(0.16, 0.735,
            "the rung means are  %s,\nso each type read pays a further %.4f"
            % (",  ".join("%.4f" % m for m in means), step),
            ha="left", va="center", fontsize=7.0, color=NAVY, linespacing=1.6)
    ax.set_xticks(sorted(by_n))
    ax.set_xticklabels(["none typed", "one typed", "two typed", "all three"],
                       fontsize=7.8, color=NAVY)
    ax.tick_params(axis="x", length=0, pad=5)
    ax.set_xlim(-0.72, 3.72)
    ax.set_ylim(0.14, 0.80)
    ax.set_ylabel("traversal payment $P_T$", fontsize=8, color=SLATE, labelpad=4)
    ax.text(3.64, THIRD + 0.010, "one third", ha="right", va="bottom",
            fontsize=7.2, color=GOLD, weight="bold")
    save(fig, "fl_f23_ladder.png")


# ══════════════════════════════════════════════ F24 leave one out
def f24_loo():
    fig, ax = chart(2.05, "REMOVING ONE ENTRY AT A TIME",
                    "the payment is a ratio of two means over a chosen "
                    "ensemble, so the ensemble is the thing to vary",
                    ["Five of six deletions leave the payment inside the band. "
                     "The sixth removes the untyped record,",
                     "which does the same arithmetic work as typing it, so the "
                     "payment rises. The ladder predicts this."],
                    left=1.10)
    loo = A09["leave_one_out"]
    ys = np.arange(len(ORDER))[::-1]
    ax.axvspan(THIRD - 0.05, THIRD + 0.05, color=GOLD, alpha=0.12, zorder=0)
    ax.axvline(THIRD, color=GOLD, lw=1.4, zorder=2)
    ax.axvline(A09["traversal_payment"], color=SLATE, lw=0.9, ls=(0, (4, 3)),
               zorder=2)
    for i, k in enumerate(ORDER):
        y, p = ys[i], loo[k]
        inside = abs(p - THIRD) < 0.05
        col = TEAL if inside else GOLD
        ax.plot([THIRD, p], [y, y], color=col, lw=1.1, alpha=0.5, zorder=3)
        ax.plot([p], [y], marker="o", ms=7.6, color=col, mec="white", mew=1.0,
                zorder=5)
        ax.text(p, y + 0.30, "%.4f" % p, ha="center", va="bottom",
                fontsize=6.9, color=col, weight="bold")
        if not inside:
            ax.text(p + 0.008, y, "  the untyped record", ha="left",
                    va="center", fontsize=7.0, color=GOLD, weight="bold")
    ax.set_yticks(ys)
    ax.set_yticklabels(["without " + M[k] for k in ORDER], fontsize=8.6,
                       color=NAVY)
    ax.tick_params(axis="y", length=0, pad=6)
    ax.set_xlim(0.255, 0.560)
    ax.set_ylim(-0.72, len(ORDER) - 0.10)
    ax.set_xlabel("traversal payment $P_T$ with that entry removed",
                  fontsize=8, color=SLATE, labelpad=5)
    ax.text(THIRD + 0.049, len(ORDER) - 0.34, "one third, $\\pm$0.05",
            ha="right", va="center", fontsize=7.2, color=GOLD, weight="bold")
    ax.text(A09["traversal_payment"] - 0.004, -0.52, "all six", ha="right",
            va="center", fontsize=6.8, color=SLATE)
    save(fig, "fl_f24_loo.png")


# ══════════════════════════════════════════════ F25 the subset sweep
def f25_subsets():
    fig, ax = chart(2.05, "EVERY SUBSET OF THE SCORE",
                    "all %d subsets of size three or more, median %.4f"
                    % (A09["subsets"]["n"], A09["subsets"]["median"]),
                    ["At size three the values split either side of the band. "
                     "The split is by whether the subset contains an",
                     "untyped record, which is the ladder again, read from a "
                     "different direction."],
                    left=0.82)
    subs = A09["subsets"]["all"]
    sizes = sorted({s["size"] for s in subs})
    ax.axhspan(THIRD - 0.05, THIRD + 0.05, color=GOLD, alpha=0.12, zorder=0)
    ax.axhline(THIRD, color=GOLD, lw=1.4, zorder=2)
    rng = np.random.default_rng(4)
    for j, sz in enumerate(sizes):
        g = [s["P_T"] for s in subs if s["size"] == sz]
        xs = j + rng.uniform(-0.17, 0.17, len(g))
        near = [abs(p - THIRD) < 0.05 for p in g]
        ax.scatter([x for x, q in zip(xs, near) if q],
                   [p for p, q in zip(g, near) if q],
                   s=17, color=TEAL, alpha=0.82, linewidths=0, zorder=4)
        ax.scatter([x for x, q in zip(xs, near) if not q],
                   [p for p, q in zip(g, near) if not q],
                   s=17, color=SLATE, alpha=0.40, linewidths=0, zorder=3)
        med = float(np.median(g))
        ax.plot([j - 0.30, j + 0.30], [med, med], color=NAVY, lw=1.7, zorder=5)
        ax.text(j, 0.775, "%d of %d" % (sum(near), len(g)), ha="center",
                va="center", fontsize=7.4, color=TEAL, weight="bold")
        ax.text(j, 0.738, "inside the band", ha="center", va="center",
                fontsize=6.4, color=SLATE)
    ax.set_xticks(range(len(sizes)))
    ax.set_xticklabels(["size %d\n%d subset%s"
                        % (sz, sum(1 for s in subs if s["size"] == sz),
                           "" if sum(1 for s in subs if s["size"] == sz) == 1
                           else "s") for sz in sizes],
                       fontsize=7.6, color=NAVY)
    ax.tick_params(axis="x", length=0, pad=5)
    ax.set_xlim(-0.55, len(sizes) - 0.45)
    ax.set_ylim(0.10, 0.82)
    ax.set_ylabel("traversal payment $P_T$", fontsize=8, color=SLATE, labelpad=4)
    ax.text(len(sizes) - 0.50, THIRD + 0.013, "one third", ha="right",
            va="bottom", fontsize=7.2, color=GOLD, weight="bold")
    ax.text(-0.50, 0.128, "navy bar = the median of the group", ha="left", va="center",
            fontsize=6.8, color=NAVY)
    save(fig, "fl_f25_subsets.png")


# ══════════════════════════════════════════════ F26 the half-weight reading
def f26_halfweight():
    cand = A09["candidate_half_weight_typing"]["pulls"]
    HALF = {"Omega_b", "Y_He"}
    PROSE = ["Every entry lands inside one",
             "sigma and the mean falls to",
             "%.4f. The rule touches two"
             % A09["candidate_half_weight_typing"]["mean_abs_pull"],
             "entries with one factor and",
             "exempts nothing.",
             "",
             "It was found by reading the",
             "residual, so what it needs",
             "next is a derivation of the",
             "boundary factor that does",
             "not consult these numbers."]
    panel_h = 0.30 + 0.46 + len(PROSE) * 0.135 + 0.16
    plot_h = max(2.05, panel_h)
    caps = ["$\\Omega_{DE}$ also improves although the rule never touches it, "
            "only its closure.",
            "That is what a structural correction looks like rather than a "
            "per-parameter one."]
    ncap = len(caps)
    H = TOP + T_H + S_H + plot_h + XL_H + ncap * CAP_H + BOT
    fig = plt.figure(figsize=(W, H), dpi=DPI)
    fig.patch.set_facecolor("white")
    PANEL_W, PL, PR = 2.10, 0.94, 0.14
    plot_w = W - PL - PANEL_W - 0.22 - PR
    y_plot = BOT + ncap * CAP_H + XL_H
    ax = fig.add_axes([PL / W, y_plot / H, plot_w / W, plot_h / H])
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(LINE)
    ax.tick_params(axis="x", colors=SLATE, labelsize=7.5, length=3)
    cx = (PL + plot_w / 2) / W
    fig.text(0.5, 1 - (TOP + T_H * 0.62) / H,
             "READING THE TWO HALF-WEIGHTS AT THE BOUNDARY", ha="center",
             va="center", fontsize=12.0, color=NAVY, weight="bold")
    fig.text(0.5, 1 - (TOP + T_H + S_H * 0.48) / H,
             "$\\Omega_b = W_M/2$ and $Y_{He} = W_L/2$ are the two half-weights; "
             "each picks up the floor once, $1/(1-r^3)$",
             ha="center", va="center", fontsize=7.2, color=SLATE)
    for i, ln in enumerate(caps):
        yy = (BOT + (ncap - 1 - i) * CAP_H + CAP_H * 0.40) / H
        fig.text(cx, yy, ln, ha="center", va="center", fontsize=7.0,
                 color=SLATE, style="italic")
    ys = np.arange(len(ORDER))[::-1]
    ax.axvspan(-1, 1, color=TEAL, alpha=0.07, zorder=0)
    ax.axvline(0, color=SLATE, lw=0.9, zorder=1)
    for i, k in enumerate(ORDER):
        y = ys[i]
        a, b = BY[k]["pull_master"], cand[k]
        touched = k in HALF
        ax.plot([a, b], [y, y], color=LINE, lw=4.4, solid_capstyle="round",
                zorder=2)
        ax.plot([a], [y], marker="o", ms=5.0, color="white", mec=SLATE,
                mew=1.1, zorder=4)
        ax.plot([b], [y], marker="o", ms=7.0,
                color=BOUND_C if touched else SLATE, mec="white", mew=1.0,
                zorder=5)
    ax.set_yticks(ys)
    ax.set_yticklabels([M[k] + ("  ½" if k in HALF else "") for k in ORDER],
                       fontsize=9.0)
    for t, k in zip(ax.get_yticklabels(), ORDER):
        t.set_color(BOUND_C if k in HALF else NAVY)
    ax.tick_params(axis="y", length=0, pad=6)
    ax.set_xlim(-2.42, 1.18)
    ax.set_ylim(-0.72, len(ORDER) - 0.28)
    ax.set_xlabel("pull, in $\\sigma$", fontsize=8, color=SLATE, labelpad=5)
    ax.text(-2.36, len(ORDER) - 0.55, "hollow = typed master", ha="left",
            va="center", fontsize=6.8, color=SLATE)
    px = PL + plot_w + 0.22
    pan = fig.add_axes([px / W, y_plot / H, PANEL_W / W, plot_h / H])
    pan.set_xlim(0, PANEL_W); pan.set_ylim(0, plot_h); pan.axis("off")
    pan.add_patch(plt.Rectangle((0, 0), PANEL_W, plot_h, facecolor=PALE,
                                edgecolor=LINE, lw=0.8, zorder=0))
    IN = 0.14
    yy = plot_h - 0.18
    pan.text(IN, yy, "WHAT IT WOULD TAKE", fontsize=7.6, color=GOLD,
             weight="bold", va="center")
    yy -= 0.30
    pan.text(IN, yy, "payment $P_T$", fontsize=6.9, color=SLATE, va="center")
    pan.text(IN, yy - 0.18, "%.4f  →  %.4f"
             % (A09["traversal_payment"],
                A09["candidate_half_weight_typing"]["payment"]),
             fontsize=8.2, color=TEAL, weight="bold", va="center")
    yy -= 0.46
    for ln in PROSE:
        pan.text(IN, yy, ln, fontsize=6.8, color=INK, va="center")
        yy -= 0.135
    save(fig, "fl_f26_halfweight.png")


# ══════════════════════════════════════════════ F27 the acoustic peaks
def f27_peaks():
    peaks = A03["peaks"]
    fig, ax = chart(2.10, "THE ACOUSTIC PEAK POSITIONS THE SOLVER RETURNS",
                    "seven invariants and one temperature anchor, integrated "
                    "forward, with no Boltzmann hierarchy and no fitted "
                    "parameter",
                    ["The spacing is right and the absolute scale is high by "
                     "%.0f to %.0f per cent, all in the same direction."
                     % (min(p["pct"] for p in peaks),
                        max(p["pct"] for p in peaks)),
                     "A single cause displaces all five together: Saha "
                     "decoupling at $z_* = %.0f$ against a true $z_* \\approx "
                     "1090$." % A03["passB"]["z_star"]],
                    left=0.86)
    ns = [p["n"] for p in peaks]
    xs = np.arange(len(ns))
    wid = 0.34
    ax.bar(xs - wid / 2, [p["planck"] for p in peaks], wid, color=MATTER_C,
           alpha=0.85, label="Planck", zorder=3)
    ax.bar(xs + wid / 2, [p["solver"] for p in peaks], wid, color=GOLD,
           alpha=0.85, label="forward solver", zorder=3)
    for i, p in enumerate(peaks):
        ax.text(xs[i] + wid / 2, p["solver"] + 34, "+%.1f%%" % p["pct"],
                ha="center", va="bottom", fontsize=6.6, color=GOLD,
                weight="bold")
    ax.set_xticks(xs)
    ax.set_xticklabels(["peak %d" % n for n in ns], fontsize=7.8, color=NAVY)
    ax.tick_params(axis="x", length=0, pad=5)
    # headroom above the tallest bar plus its per cent label, then the summary
    ax.set_ylim(0, 2260)
    ax.set_ylabel("multipole  $\\ell$", fontsize=8, color=SLATE, labelpad=4)
    ax.legend(frameon=False, fontsize=7.2, loc="upper left", labelcolor=SLATE)
    ax.text(len(ns) - 0.5, 2180,
            "$\\ell_A = %.1f$   ·   $r_s = %.1f$ Mpc   ·   $D_M = %.0f$ Mpc"
            % (A03["l_A"], A03["passB"]["r_s"], A03["passB"]["D_M"]),
            ha="right", va="top", fontsize=7.0, color=NAVY)
    save(fig, "fl_f27_peaks.png")


# ══════════════════════════════════════════════ F28 the two basins
def f28_basins():
    b = A03["basins"]
    fig, ax = chart(2.20, "THE TWO HUBBLE BASINS",
                    "one anchored solve, and the closure conventions that carry "
                    "it to the local family",
                    ["The three closure conventions differ from each other by "
                     "less than the structural floor $r^3$,",
                     "so the sector does not have to choose between them."],
                    left=1.46)
    rows = [
        ("Planck 2018", 67.36, 0.54, MATTER_C, "measured"),
        ("laminar, $\\theta_*$ anchored", b["laminar_H0"], None, GOLD,
         "%+.2f$\\sigma$" % b["laminar_pull_planck"]),
        ("condensed, $(1-r^3)^{-3}$", b["condensed_(1-r3)^-3"]["H0"], None,
         TEAL, "%+.2f$\\sigma$" % b["condensed_(1-r3)^-3"]["pull_shoes"]),
        ("condensed, $1+3r^3$", b["condensed_1+3r3"]["H0"], None, TEAL,
         "%+.2f$\\sigma$" % b["condensed_1+3r3"]["pull_shoes"]),
        ("condensed, symmetric", b["condensed_symmetric"]["H0"], None, TEAL,
         "%+.2f$\\sigma$" % b["condensed_symmetric"]["pull_shoes"]),
        ("SH0ES 2022", 73.04, 1.04, MATTER_C, "measured"),
    ]
    ys = np.arange(len(rows))[::-1]
    ax.axvspan(67.36 - 0.54, 67.36 + 0.54, color=MATTER_C, alpha=0.10, zorder=0)
    ax.axvspan(73.04 - 1.04, 73.04 + 1.04, color=MATTER_C, alpha=0.10, zorder=0)
    for i, (nm, v, s, col, note) in enumerate(rows):
        y = ys[i]
        if s:
            ax.plot([v - s, v + s], [y, y], color=col, lw=2.4, alpha=0.55,
                    solid_capstyle="round", zorder=3)
            ax.plot([v], [y], marker="s", ms=6.4, color=col, mec="white",
                    mew=0.9, zorder=5)
        else:
            ax.plot([v], [y], marker="o", ms=7.4, color=col, mec="white",
                    mew=1.0, zorder=5)
        ax.text(v, y + 0.30, "%.2f" % v, ha="center", va="bottom",
                fontsize=6.9, color=col, weight="bold")
        # the note column lives outside the data range so it cannot sit on an
        # error bar
        ax.text(75.9, y, note, ha="right", va="center", fontsize=6.8,
                color=SLATE)
    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in rows], fontsize=8.2, color=NAVY)
    ax.tick_params(axis="y", length=0, pad=6)
    ax.set_xlim(65.4, 76.0)
    ax.set_ylim(-0.70, len(rows) - 0.15)
    ax.set_xlabel("$H_0$   km s$^{-1}$ Mpc$^{-1}$", fontsize=8, color=SLATE,
                  labelpad=5)
    save(fig, "fl_f28_basins.png")


if __name__ == "__main__":
    print("chart plates:")
    f19_operator(); f20_reach(); f21_pulls(); f22_payment(); f23_ladder()
    f24_loo(); f25_subsets(); f26_halfweight(); f27_peaks(); f28_basins()

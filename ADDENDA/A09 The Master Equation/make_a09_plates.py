"""Plates for A09, The Master Equation.

Same two rules as the earlier plate rebuild, and a third that the first pass of
these charts broke:

1. Author at the width the plate is printed at. Every canvas below is sized in
   final page inches, so a fontsize here is the point size on paper.
2. Reserve room before placing text. Every caption line is given explicitly; no
   automatic wrapping is trusted.
3. For anything with axes, lay the page out as a VERTICAL BUDGET in inches and
   derive the axes rectangle from it. Placing a figure-level caption at a guessed
   fraction is what put the first pass of these on top of their own axis labels.

Colour carries meaning or it is not used. Matter blue, Light gold and Boundary
magenta for the channels; navy and slate for structure; teal for a reading that
improved and rust for one that did not.
"""

import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "a09")
os.makedirs(IMG, exist_ok=True)
DPI = 400

NAVY, GOLD, SLATE, INK = "#102A43", "#B48A2E", "#5B6B7A", "#243040"
TEAL, RUST, PALE, LINE = "#14707D", "#A8442A", "#F4F7F9", "#C7D3DE"
LIGHT_C, BOUND_C, MATTER_C = "#B8811C", "#B8256B", "#1E6FB8"

plt.rcParams.update({
    "font.family": ["Constantia", "Cambria", "DejaVu Sans"],
    "mathtext.fontset": "cm",
    "text.color": INK,
    "savefig.facecolor": "white",
})

R = json.load(open(r"C:\Users\joesh\Desktop\SCI\ADDENDA\A09 The Master Equation"
                   r"\master_equation_results.json"))
ROWS = R["rows"]
BY = {d["key"]: d for d in ROWS}
ORDER = ["Omega_b", "Omega_c", "Omega_DE", "Y_He", "n_s", "tau"]
M = {"Omega_b": r"$\Omega_b$", "Omega_c": r"$\Omega_c$",
     "Omega_DE": r"$\Omega_{DE}$", "Y_He": r"$Y_{He}$",
     "n_s": r"$n_s$", "tau": r"$\tau$"}
THIRD = 1.0 / 3.0
W = 6.50


def canvas(w, h, bg="white"):
    fig = plt.figure(figsize=(w, h), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w); ax.set_ylim(0, h); ax.axis("off")
    fig.patch.set_facecolor(bg); ax.set_facecolor(bg)
    return fig, ax


def box(ax, x, y, w, h, edge, fill="white", lw=0.9, r=0.05, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=%f" % r,
                                linewidth=lw, edgecolor=edge, facecolor=fill,
                                zorder=z))


def tint(ax, x, y, w, h, col, a=0.10, r=0.05):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=%f" % r,
                                linewidth=0, facecolor=col, alpha=a, zorder=1))


def arrow(ax, x0, y0, x1, y1, color=SLATE, lw=1.0, ms=8):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>",
                                 mutation_scale=ms, linewidth=lw, color=color,
                                 zorder=3, shrinkA=0, shrinkB=0))


def save(fig, name):
    fig.savefig(os.path.join(IMG, name), dpi=DPI, facecolor="white")
    plt.close(fig)
    print("  ", name)


# ── the vertical budget, in inches, for every plate that carries axes ───────
TOP, T_H, S_H = 0.06, 0.26, 0.21
XL_H, CAP_H, BOT = 0.36, 0.155, 0.09


def chart(plot_h, title, sub, caption_lines, left=0.98, right=0.16):
    """Lay out a charted plate from an explicit budget and return (fig, ax).

    The axes rectangle is derived from the budget rather than guessed, so a
    caption can never land on an axis label however long the tick labels are.
    """
    ncap = len(caption_lines)
    H = TOP + T_H + S_H + plot_h + XL_H + ncap * CAP_H + BOT
    fig = plt.figure(figsize=(W, H), dpi=DPI)
    fig.patch.set_facecolor("white")
    y_plot = BOT + ncap * CAP_H + XL_H
    ax = fig.add_axes([left / W, y_plot / H, (W - left - right) / W, plot_h / H])
    fig.text(0.5, 1 - (TOP + T_H * 0.62) / H, title, ha="center", va="center",
             fontsize=12.0, color=NAVY, weight="bold")
    fig.text(0.5, 1 - (TOP + T_H + S_H * 0.48) / H, sub, ha="center",
             va="center", fontsize=7.2, color=SLATE)
    for i, ln in enumerate(caption_lines):
        yy = (BOT + (ncap - 1 - i) * CAP_H + CAP_H * 0.40) / H
        fig.text(0.5, yy, ln, ha="center", va="center", fontsize=7.0,
                 color=GOLD, style="italic")
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(LINE)
    ax.tick_params(axis="x", colors=SLATE, labelsize=7.5, length=3)
    return fig, ax


# ══════════════════════════════════════════ 1. the operator and its roles
def plate_operator():
    """Four stages, and what each one is ALLOWED to supply. The point of the
    plate is that only one of the four returns a value."""
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
    H = 0.60 + BH + RH + 0.66
    fig, ax = canvas(W, H)
    ax.text(W / 2, H - 0.21, "THE MASTER OPERATOR, AND WHAT EACH ALGEBRA MAY "
            "SUPPLY", ha="center", va="center", fontsize=12.0, color=NAVY,
            weight="bold")
    ax.text(W / 2, H - 0.43, "three of the four qualify the reading; exactly "
            "one of them returns a value", ha="center", va="center",
            fontsize=7.2, color=SLATE)

    yb = H - 0.60 - BH
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

    ax.plot([0.18, W - 0.18], [0.50, 0.50], color=LINE, lw=0.8)
    ax.text(0.18, 0.31, "The failure this ordering fixes: fed in as an "
            "estimator, $H_5$ multiplies the prediction and the result gets "
            "worse.", ha="left", va="center", fontsize=7.0, color=RUST,
            style="italic")
    ax.text(0.18, 0.14, "As a measure on the path it is the averaging kernel, "
            "and nothing in the combination step is chosen.", ha="left",
            va="center", fontsize=7.0, color=TEAL, style="italic")
    save(fig, "a09_f1_operator.png")


# ══════════════════════════════════════════ 2. which observables can move
def plate_channels():
    """The signature decides in advance whether an observable has a hue that can
    move. Four of six cannot, and that is structure, not a shortcut."""
    RH, gap = 0.21, 0.085
    n = len(ORDER)
    H = 0.62 + n * RH + (n - 1) * gap + 0.52
    fig, ax = canvas(W, H)
    ax.text(W / 2, H - 0.21, "WHICH OBSERVABLES THE WEIGHTING CAN REACH",
            ha="center", va="center", fontsize=12.0, color=NAVY, weight="bold")
    ax.text(W / 2, H - 0.43, "one zero in the channel signature and the hue "
            "cannot move, so $\\Delta\\theta = 0$ and $H_5 = 1$ by structure",
            ha="center", va="center", fontsize=7.2, color=SLATE)

    x0, x1 = 1.02, W - 0.26
    LW = 1.34
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
        ax.text(x0 + LW / 2, y + RH / 2, "PURE  ·  one channel" if d["pure"]
                else "MIXED  ·  two channels", ha="center", va="center",
                fontsize=7.0, color=col, weight="bold")
        note = ("$\\Delta\\theta = 0$,  $N = \\infty$,  $H_5 = 1$   ·   the "
                "weighting cannot reach it" if d["pure"] else
                "hue moves with the state   ·   $T = %d$ turns   ·   $H_5$ "
                "weights it" % d["T"])
        ax.text(x0 + LW + 0.13, y + RH / 2, note, ha="left", va="center",
                fontsize=7.0, color=SLATE if d["pure"] else INK)

    ax.plot([0.26, W - 0.26], [0.34, 0.34], color=LINE, lw=0.8)
    ax.text(W / 2, 0.16, "$\\tau$ is pure, so the weighting does not reach it "
            "either. It moves because its TYPE changes, not because it is "
            "weighted.", ha="center", va="center", fontsize=7.0, color=GOLD,
            style="italic")
    save(fig, "a09_f2_channels.png")


# ══════════════════════════════════════════ 3. the pull ladder
def plate_pulls():
    """The whole result on one axis. Three readings per observable, in sigma.

    The gold pip is drawn ON TOP of the master dot rather than beside it,
    because for four of the six the colour average and the master ARE the same
    number and the plate should show that rather than hide it.
    """
    fig, ax = chart(2.30, "EVERY OBSERVABLE, EVERY READING",
                    "hollow = old corpus static   ·   gold pip = colour average"
                    "   ·   filled = typed master   ·   shaded band is one "
                    "$\\sigma$",
                    ["$\\tau$ is the only entry the colour average makes worse, "
                     "and the only one whose type is corrected.",
                     "$Y_{He}$ is the only entry that nothing in the passage "
                     "reaches at all."])
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
        better = abs(c) < abs(a)
        col = TEAL if better else RUST
        ax.plot([a, c], [y, y], color=LINE, lw=5.0, solid_capstyle="round",
                zorder=2)
        ax.plot([a], [y], marker="o", ms=5.2, color="white", mec=SLATE,
                mew=1.1, zorder=4)
        ax.plot([c], [y], marker="o", ms=7.6, color=col, mec="white", mew=1.0,
                zorder=5)
        ax.plot([b], [y], marker="s", ms=2.3, color=GOLD, zorder=6)
        ax.text(c, y + 0.32, "%+.2f" % c, ha="center", va="bottom",
                fontsize=6.9, color=col, weight="bold")

    ax.set_yticks(ys)
    ax.set_yticklabels([M[k] for k in ORDER], fontsize=9.6, color=NAVY)
    ax.tick_params(axis="y", length=0, pad=6)
    ax.set_xlim(-2.68, 1.42)
    ax.set_ylim(-0.72, n - 0.22)
    ax.set_xlabel("pull against measurement, in $\\sigma$", fontsize=8,
                  color=SLATE, labelpad=5)
    save(fig, "a09_f3_pulls.png")


# ══════════════════════════════════════════ 4. the traversal payment
def plate_payment():
    """One bar, the two means, and the third marked where it falls."""
    E0, Ec, E1 = R["E0_static"], R["E_colour"], R["E1_master"]
    PT = R["traversal_payment"]
    BH = 0.42
    H = 0.62 + 0.26 + BH + 0.34 + 0.58
    fig, ax = canvas(W, H)
    ax.text(W / 2, H - 0.21, "THE TRAVERSAL PAYMENT", ha="center", va="center",
            fontsize=12.0, color=NAVY, weight="bold")
    ax.text(W / 2, H - 0.43, "the fraction of the joint residual of six "
            "observables that the passage removes", ha="center", va="center",
            fontsize=7.2, color=SLATE)

    x0, x1 = 0.66, W - 0.52
    span = x1 - x0
    yb = H - 0.62 - 0.26 - BH

    xt = x0 + span * THIRD
    ax.plot([xt, xt], [yb - 0.10, yb + BH + 0.10], color=GOLD, lw=1.5, zorder=6)
    ax.text(xt, yb + BH + 0.16, "one third", ha="center", va="bottom",
            fontsize=7.6, color=GOLD, weight="bold")

    tint(ax, x0, yb, span, BH, SLATE, a=0.10)
    box(ax, x0, yb, span, BH, LINE, fill="none", lw=0.8)
    wpaid = span * PT
    ax.add_patch(FancyBboxPatch((x0, yb), wpaid, BH,
                                boxstyle="round,pad=0,rounding_size=0.03",
                                linewidth=0, facecolor=TEAL, alpha=0.82,
                                zorder=3))
    ax.text(x0 + wpaid / 2, yb + BH / 2, "PAID  %.4f" % PT, ha="center",
            va="center", fontsize=8.8, color="white", weight="bold", zorder=4)
    ax.text(x0 + wpaid + (span - wpaid) / 2, yb + BH / 2,
            "RETAINED  %.4f" % (1 - PT), ha="center", va="center",
            fontsize=8.8, color=SLATE, weight="bold", zorder=4)
    ax.text(x0, yb - 0.20, "$E_0$ = %.4f $\\sigma$" % E0, ha="left",
            va="center", fontsize=7.8, color=SLATE)
    ax.text(x1, yb - 0.20, "$E_1$ = %.4f $\\sigma$" % E1, ha="right",
            va="center", fontsize=7.8, color=TEAL, weight="bold")

    ax.plot([0.26, W - 0.26], [0.40, 0.40], color=LINE, lw=0.8)
    ax.text(W / 2, 0.24, "$P_T = 1 - E_1/E_0$ = %.6f.    The gap to one third "
            "is %+.2f percentage points." % (PT, 100 * (PT - THIRD)),
            ha="center", va="center", fontsize=7.8, color=INK)
    ax.text(W / 2, 0.10, "The colour average alone reaches %.4f $\\sigma$; the "
            "typing of $\\tau$ supplies the rest." % Ec, ha="center",
            va="center", fontsize=7.0, color=SLATE, style="italic")
    save(fig, "a09_f4_payment.png")


# ══════════════════════════════════════════ 5. leave one out
def plate_loo():
    """The sharpest form of the ensemble question, one deletion at a time."""
    fig, ax = chart(2.05, "LEAVE ONE OUT",
                    "a ratio of two means over a chosen ensemble has one "
                    "obvious falsifier: delete a member and recompute",
                    ["The payment holds under five of six deletions. The one "
                     "that breaks it is the one observable",
                     "the passage never moved."],
                    left=1.10)
    loo = R["leave_one_out"]
    ys = np.arange(len(ORDER))[::-1]
    ax.axvspan(THIRD - 0.05, THIRD + 0.05, color=GOLD, alpha=0.12, zorder=0)
    ax.axvline(THIRD, color=GOLD, lw=1.4, zorder=2)
    ax.axvline(R["traversal_payment"], color=SLATE, lw=0.9, ls=(0, (4, 3)),
               zorder=2)

    for i, k in enumerate(ORDER):
        y, p = ys[i], loo[k]
        held = abs(p - THIRD) < 0.05
        col = TEAL if held else RUST
        ax.plot([THIRD, p], [y, y], color=col, lw=1.1, alpha=0.5, zorder=3)
        ax.plot([p], [y], marker="o", ms=7.6, color=col, mec="white", mew=1.0,
                zorder=5)
        ax.text(p, y + 0.30, "%.4f" % p, ha="center", va="bottom",
                fontsize=6.9, color=col, weight="bold")
        if not held:
            ax.text(p + 0.008, y, "  BREAKS", ha="left", va="center",
                    fontsize=7.2, color=RUST, weight="bold")

    ax.set_yticks(ys)
    ax.set_yticklabels(["drop " + M[k] for k in ORDER], fontsize=8.8,
                       color=NAVY)
    ax.tick_params(axis="y", length=0, pad=6)
    ax.set_xlim(0.255, 0.545)
    ax.set_ylim(-0.72, len(ORDER) - 0.10)
    ax.set_xlabel("traversal payment $P_T$ with that observable removed",
                  fontsize=8, color=SLATE, labelpad=5)
    # the band label goes at the far edge of the band, where no marker can be
    ax.text(THIRD + 0.049, len(ORDER) - 0.34, "one third, $\\pm$0.05",
            ha="right", va="center", fontsize=7.2, color=GOLD, weight="bold")
    ax.text(R["traversal_payment"] - 0.004, -0.52, "all six", ha="right",
            va="center", fontsize=6.8, color=SLATE)
    save(fig, "a09_f5_loo.png")


# ══════════════════════════════════════════ 6. the whole subset sweep
def plate_subsets():
    """Every subset of size three or more, so the reader can see the decay."""
    fig, ax = chart(2.05, "EVERY SUBSET OF THE SCORE",
                    "all %d subsets of size three or more, median %.4f"
                    % (R["subsets"]["n"], R["subsets"]["median"]),
                    ["At size three the values split either side of the band and "
                     "none lands inside it, though the median falls in the gap.",
                     "The count decays with subset size, which a mean over few "
                     "items does whether or not a law is true."],
                    left=0.82)
    subs = R["subsets"]["all"]
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
        ax.text(j, 0.738, "within 0.05", ha="center", va="center",
                fontsize=6.4, color=SLATE)

    ax.set_xticks(range(len(sizes)))
    ax.set_xticklabels(["size %d\n%d subset%s"
                        % (sz, sum(1 for s in subs if s["size"] == sz),
                           "" if sum(1 for s in subs if s["size"] == sz) == 1
                           else "s")
                        for sz in sizes], fontsize=7.6, color=NAVY)
    ax.tick_params(axis="x", length=0, pad=5)
    ax.tick_params(axis="y", colors=SLATE, labelsize=7.5, length=3)
    ax.set_xlim(-0.55, len(sizes) - 0.45)
    ax.set_ylim(0.10, 0.82)
    ax.set_ylabel("traversal payment $P_T$", fontsize=8, color=SLATE,
                  labelpad=4)
    ax.text(len(sizes) - 0.50, THIRD + 0.013, "one third", ha="right",
            va="bottom", fontsize=7.2, color=GOLD, weight="bold")
    ax.text(-0.50, 0.132, "navy bar = median", ha="left", va="center",
            fontsize=6.8, color=NAVY)
    save(fig, "a09_f6_subsets.png")


# ══════════════════════════════════════════ 7. the candidate typing
def plate_candidate():
    """The rival claim, drawn as a rival rather than as an improvement.

    The verdict panel is laid out in INCHES on an overlay axes, so its text can
    be counted against the box height instead of overflowing it.
    """
    cand = R["candidate_half_weight_typing"]["pulls"]
    HALF = {"Omega_b", "Y_He"}
    # the panel's own budget, in inches, decided BEFORE the height is fixed:
    #   title 0.30, two stat blocks at 0.46, six prose lines at 0.135, pad 0.16
    PROSE = ["The fit improves sharply, but",
             "the rule was found by looking",
             "at the residual. And it moves",
             "the payment to neither a third",
             "nor two thirds, so the two",
             "readings are RIVALS."]
    panel_h = 0.30 + 2 * 0.46 + len(PROSE) * 0.135 + 0.16
    plot_h = max(2.05, panel_h)
    ncap = 2
    H = TOP + T_H + S_H + plot_h + XL_H + ncap * CAP_H + BOT
    fig = plt.figure(figsize=(W, H), dpi=DPI)
    fig.patch.set_facecolor("white")

    PANEL_W, PL, PR = 2.16, 0.94, 0.14
    plot_w = W - PL - PANEL_W - 0.22 - PR
    y_plot = BOT + ncap * CAP_H + XL_H
    ax = fig.add_axes([PL / W, y_plot / H, plot_w / W, plot_h / H])
    cx = (PL + plot_w / 2) / W          # captions centre on the PLOT, not the page
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(LINE)
    ax.tick_params(axis="x", colors=SLATE, labelsize=7.5, length=3)

    fig.text(0.5, 1 - (TOP + T_H * 0.62) / H,
             "A CANDIDATE TYPING, SCORED AND NOT ADOPTED", ha="center",
             va="center", fontsize=12.0, color=NAVY, weight="bold")
    fig.text(0.5, 1 - (TOP + T_H + S_H * 0.48) / H,
             "read the two half-weights across the boundary: "
             "$\\Omega_b = W_M/2$ and $Y_{He} = W_L/2$, each divided by "
             "$(1-r^3)$", ha="center", va="center", fontsize=7.2, color=SLATE)
    for i, ln in enumerate([
            "$\\Omega_{DE}$ also improves although the rule never",
            "touches it, only its closure."]):
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
    ax.text(-2.36, len(ORDER) - 0.55, "hollow = typed master",
            ha="left", va="center", fontsize=6.8, color=SLATE)

    # verdict panel, budgeted in inches
    px = PL + plot_w + 0.22
    pan = fig.add_axes([px / W, y_plot / H, PANEL_W / W, plot_h / H])
    pan.set_xlim(0, PANEL_W); pan.set_ylim(0, plot_h); pan.axis("off")
    pan.add_patch(plt.Rectangle((0, 0), PANEL_W, plot_h, facecolor=PALE,
                                edgecolor=LINE, lw=0.8, zorder=0))
    IN = 0.14
    yy = plot_h - 0.18
    pan.text(IN, yy, "WHY IT IS NOT ADOPTED", fontsize=7.6, color=GOLD,
             weight="bold", va="center")
    yy -= 0.30
    for lab, val, col in [
            ("mean |pull|", "0.6713  \u2192  %.4f"
             % R["candidate_half_weight_typing"]["mean_abs_pull"], TEAL),
            ("payment $P_T$", "0.3274  \u2192  %.4f"
             % R["candidate_half_weight_typing"]["payment"], RUST)]:
        pan.text(IN, yy, lab, fontsize=6.9, color=SLATE, va="center")
        pan.text(IN, yy - 0.18, val, fontsize=8.2, color=col, weight="bold",
                 va="center")
        yy -= 0.46
    yy -= 0.02
    for ln in PROSE:
        pan.text(IN, yy, ln, fontsize=6.8, color=INK, va="center")
        yy -= 0.135
    save(fig, "a09_f7_candidate.png")


if __name__ == "__main__":
    print("plates:")
    plate_operator()
    plate_channels()
    plate_pulls()
    plate_payment()
    plate_loo()
    plate_subsets()
    plate_candidate()
    print("all in", IMG)

"""The Field Ledger, second edition: the twelve schematic plates, redrawn.

These replace the machine-drawn originals, which carried ASCII mathematics
(phi^2, W_L, alpha_L) in a sans face at the wrong width. Every glyph here is the
real one and every canvas is authored at print width.
"""
from fl_base import *


# ══════════════════════════════════════════════ F1  the editorial rule
def f1_rule():
    H = 0.62 + 0.66 + 0.30 + 0.56
    fig, ax = canvas(W, H)
    head(ax, W, H, "THE GRADE CHAIN THAT GOVERNS EVERY SECTION",
         "a reader must be able to locate any equation in this chain and see "
         "exactly where interpretation enters")
    y = H - 0.62 - 0.66
    chain(ax, y, [
        ("PROBLEM", "a recognised\nphysical question", NAVY),
        ("STANDARD", "the accepted\nequation", MATTER_C),
        ("OPERATION", "the Unified\nMechanics move", GOLD),
        ("READOUT", "the number\nit returns", BOUND_C),
        ("TEST", "the measurement\nit meets", TEAL),
        ("OBLIGATION", "what is still\nowed", MAUVE),
    ], W, bh=0.66, fs=6.9, capfs=7.4)
    foot(ax, W, [
        ("A displayed equation is STANDARD, PROVED, CONDITIONAL, PROPOSED, "
         "FORECAST, OPEN or WITHDRAWN.", None),
        ("The status box immediately after it governs, and the prose is not "
         "permitted to promote it silently.", GOLD),
    ], y=0.34)
    save(fig, "fl_f01_rule.png")


# ══════════════════════════════════════════════ F2  the inherited problem
def f2_timeline():
    # budget: head 0.62, year band 0.20, rule, what band 0.34, who band 0.18,
    # foot 0.56. Everything above the line is the year only, so nothing can
    # reach the subtitle.
    H = 0.62 + 0.24 + 0.36 + 0.20 + 0.56
    fig, ax = canvas(W, H)
    head(ax, W, H, "WHAT ANY NEW FRAMEWORK INHERITS",
         "the geometry and the observations are not in dispute; the mechanism "
         "behind the parameters is")
    y = H - 0.62 - 0.24
    x0, x1 = 0.44, W - 0.44
    ax.plot([x0, x1], [y, y], color=NAVY, lw=1.4, zorder=2)
    marks = [(0.00, "1915", "field\nequations", "Einstein"),
             (0.19, "1922", "expanding\nsolutions", "Friedmann"),
             (0.36, "1949", "closed timelike\ncurves", "Gödel"),
             (0.53, "1965", "the microwave\nbackground", "Penzias, Wilson"),
             (0.74, "1998", "acceleration", "supernovae"),
             (1.00, "2025", "BAO and evolving\ndark energy", "DESI DR2")]
    for t, yr, what, who in marks:
        x = x0 + t * (x1 - x0)
        ax.plot([x], [y], marker="o", ms=5.0, color=GOLD, mec="white", mew=0.9,
                zorder=4)
        ax.text(x, y + 0.10, yr, ha="center", va="bottom", fontsize=7.6,
                color=NAVY, weight="bold")
        ax.text(x, y - 0.10, what, ha="center", va="top", fontsize=6.5,
                color=INK, linespacing=1.5)
        ax.text(x, y - 0.44, who, ha="center", va="top", fontsize=6.3,
                color=SLATE, style="italic")
    foot(ax, W, [
        ("The standard model is observationally powerful. The ledger asks which "
         "operations its successful parameters compress,", None),
        ("and it enters only where it can supply a dependency the fit does not "
         "already contain.", GOLD),
    ], y=0.34)
    save(fig, "fl_f02_timeline.png")


# ══════════════════════════════════════════════ F3  the standard pipeline
def f3_pipeline():
    H = 0.62 + 0.70 + 0.30 + 0.56
    fig, ax = canvas(W, H)
    head(ax, W, H, "THE PIPELINE AN ALTERNATIVE HAS TO MEET",
         "the microwave background is a dynamical calculation, not a row of "
         "fitted percentages")
    y = H - 0.62 - 0.70
    chain(ax, y, [
        ("SPECTRUM", "$A_s$,  $n_s$", MATTER_C),
        ("PLASMA", "baryons\nand photons", BOUND_C),
        ("RECOMBINE", "the visibility\nfunction", GOLD),
        ("GEOMETRY", "$r_s / D_M$", NAVY),
        ("LATE TIME", "$\\Omega_m$,\n$\\Omega_{DE}$, growth", TEAL),
        ("FIT", "$C_\\ell$ against\nlikelihoods", MAUVE),
    ], W, bh=0.70, fs=6.9, capfs=7.2)
    foot(ax, W, [
        ("Unified Mechanics does not get to skip a stage. It must derive a "
         "stage's inputs or replace the stage,", None),
        ("and in either case the replacement carries the same testable "
         "obligation.", GOLD),
    ], y=0.34)
    save(fig, "fl_f03_pipeline.png")


# ══════════════════════════════════════════════ F4  the square must commute
def f4_square():
    # budget: head 0.72, two rows of 0.52 with a 0.96 pitch, the identity at
    # 0.40 below the lower row, then the foot. Summing it beats guessing it.
    H = 0.72 + 0.52 + 0.96 + 0.40 + 0.62
    fig, ax = canvas(W, H)
    head(ax, W, H, "THE SQUARE THAT LOGICAL ACTION REQUIRES",
         "a reduced description is adequate only when reduction and evolution "
         "commute")
    bw, bh = 1.72, 0.52
    xl, xr = 1.02, W - 1.02 - bw
    yt, yb = H - 0.72 - bh, H - 0.72 - bh - 0.96
    cells = [(xl, yt, "complete state  $x$", NAVY),
             (xr, yt, "transcript  $\\pi(x)$", MATTER_C),
             (xl, yb, "evolved  $E_t\\,x$", NAVY),
             (xr, yb, "$\\tilde{E}_t\\,\\pi(x)$", MATTER_C)]
    for x, y, t, col in cells:
        tint(ax, x, y, bw, bh, col, a=0.10)
        box(ax, x, y, bw, bh, col, fill="none", lw=1.0)
        ax.text(x + bw / 2, y + bh / 2, t, ha="center", va="center",
                fontsize=8.6, color=INK)
    arrow(ax, xl + bw + 0.04, yt + bh / 2, xr - 0.04, yt + bh / 2, lw=1.0)
    ax.text((xl + bw + xr) / 2, yt + bh / 2 + 0.14, "reduce  $\\pi$",
            ha="center", va="bottom", fontsize=7.2, color=GOLD, weight="bold")
    arrow(ax, xl + bw + 0.04, yb + bh / 2, xr - 0.04, yb + bh / 2, lw=1.0)
    ax.text((xl + bw + xr) / 2, yb + bh / 2 - 0.16, "reduce  $\\pi$",
            ha="center", va="top", fontsize=7.2, color=GOLD, weight="bold")
    arrow(ax, xl + bw / 2, yt - 0.04, xl + bw / 2, yb + bh + 0.04, lw=1.0)
    ax.text(xl + bw / 2 - 0.10, (yt + yb + bh) / 2, "evolve  $E_t$", ha="right",
            va="center", fontsize=7.2, color=SLATE, rotation=90)
    arrow(ax, xr + bw / 2, yt - 0.04, xr + bw / 2, yb + bh + 0.04, lw=1.0)
    ax.text(xr + bw / 2 + 0.10, (yt + yb + bh) / 2, "evolve  $\\tilde{E}_t$",
            ha="left", va="center", fontsize=7.2, color=SLATE, rotation=270)
    ax.text(W / 2, yb - 0.22, "$\\pi \\circ E_t \\;=\\; \\tilde{E}_t \\circ \\pi$",
            ha="center", va="center", fontsize=13.0, color=NAVY, weight="bold")
    foot(ax, W, [
        ("If the two routes disagree the reduced description has thrown away a "
         "distinction that changes the future.", None),
        ("That may still be a useful approximation. It cannot be called "
         "lossless.", GOLD),
    ], y=0.34)
    save(fig, "fl_f04_square.png")


# ══════════════════════════════════════════════ F5  Crowley and Glorpnorp
def f5_hotel():
    # the packet is the tallest object, not the room grid: six items at 0.20
    # plus a 0.44 header. Budget from that, or the packet lands on the caption.
    PH = 1.62
    H = 0.80 + PH + 0.22 + 0.56
    fig, ax = canvas(W, H)
    head(ax, W, H, "THE TRANSMISSION PROBLEM",
         "the receiver has the algebra and no independent sensory access to the "
         "thing described")
    # the twenty rooms
    gx, gy, cw, ch = 0.055, 0.055, 0.30, 0.24
    x0 = 0.34
    ytop = H - 0.80
    ax.text(x0, ytop + 0.20, "CROWLEY'S TWENTY ROOMS", ha="left", va="center",
            fontsize=7.4, color=NAVY, weight="bold")
    rng = np.random.default_rng(7)
    blocked = {4, 9, 13}
    for k in range(20):
        i, j = k // 5, k % 5
        x = x0 + j * (cw + gx)
        y = ytop - i * (ch + gy) - ch
        lit = rng.random()
        col = hsv_to_rgb((0.11, 0.55, 0.55 + 0.45 * lit))
        box(ax, x, y, cw, ch, LINE, fill=col, lw=0.6)
        if k in blocked:
            ax.plot([x + 0.04, x + cw - 0.04], [y + 0.04, y + ch - 0.04],
                    color=RUST, lw=1.1, zorder=5)
            ax.plot([x + 0.04, x + cw - 0.04], [y + ch - 0.04, y + 0.04],
                    color=RUST, lw=1.1, zorder=5)
    # four rows of five, so the note sits under row four and not under row five
    ax.text(x0, ytop - 4 * (ch + gy) - 0.04, "crosses are blocked doors",
            ha="left", va="center", fontsize=6.4, color=RUST, style="italic")

    # the packet
    px, pw = 2.62, 1.70
    ph = PH
    py = ytop - ph
    tint(ax, px, py, pw, ph, MATTER_C, a=0.09)
    box(ax, px, py, pw, ph, MATTER_C, fill="none", lw=1.0)
    ax.add_patch(FancyBboxPatch((px, py + ph - 0.24), pw, 0.24,
                                boxstyle="round,pad=0,rounding_size=0.03",
                                linewidth=0, facecolor=MATTER_C, alpha=0.88,
                                zorder=3))
    ax.text(px + pw / 2, py + ph - 0.12, "THE STATE PACKET  $F$", ha="center",
            va="center", fontsize=7.6, color="white", weight="bold", zorder=4)
    items = [("$V$", "room values"), ("$C$", "relations and phase"),
             ("$K$", "constraints"), ("$H$", "retained history"),
             ("$Q$", "the questions asked"), ("$U$", "the update rule")]
    for i, (sym, txt) in enumerate(items):
        yy = py + ph - 0.44 - i * 0.20
        ax.text(px + 0.14, yy, sym, ha="left", va="center", fontsize=8.0,
                color=MATTER_C, weight="bold")
        ax.text(px + 0.42, yy, txt, ha="left", va="center", fontsize=7.0,
                color=INK)
    arrow(ax, x0 + 5 * (cw + gx) - gx + 0.06, py + ph / 2, px - 0.06,
          py + ph / 2, lw=1.1, color=GOLD)

    # the receiver
    rx = px + pw + 0.34
    arrow(ax, px + pw + 0.04, py + ph / 2, rx + 0.14, py + ph / 2, lw=1.1,
          color=GOLD)
    ax.add_patch(Circle((rx + 0.42, py + ph / 2 + 0.10), 0.20,
                        facecolor=BOUND_C, alpha=0.20, edgecolor=BOUND_C,
                        lw=1.0, zorder=3))
    ax.text(rx + 0.42, py + ph / 2 + 0.10, "?", ha="center", va="center",
            fontsize=11, color=BOUND_C, weight="bold", zorder=4)
    ax.text(rx + 0.42, py + ph / 2 - 0.22, "GLORPNORP", ha="center", va="top",
            fontsize=7.2, color=BOUND_C, weight="bold")
    ax.text(rx + 0.42, py + ph / 2 - 0.40,
            "can evolve the field\nand answer the\nquestions, or cannot",
            ha="center", va="top", fontsize=6.4, color=SLATE, linespacing=1.5)

    foot(ax, W, [
        ("Two hotels can share every brightness value and differ in which bulb "
         "lit which room, which door is shut,", None),
        ("and what happens after the same intervention. Snapshot preservation is "
         "not evolution preservation.", GOLD),
    ], y=0.34)
    save(fig, "fl_f05_hotel.png")


# ══════════════════════════════════════════════ F6  the minimal update
def f6_update():
    # head 0.62, chain 0.72, a 0.50 gap, then a 0.62 value band, then the foot
    H = 0.62 + 0.72 + 0.50 + 0.62 + 0.56
    fig, ax = canvas(W, H)
    head(ax, W, H, "THE MINIMAL UPDATE AND THE PERFECT SQUARE",
         "one recurrent operation, its fixed ray, and the exact three-way "
         "partition that follows")
    y = H - 0.62 - 0.72
    chain(ax, y, [
        ("UPDATE", "$(a,b) \\rightarrow (a{+}b,\\,a)$", NAVY),
        ("FIXED RAY", "$\\varphi^2 = \\varphi + 1$", MATTER_C),
        ("TWO POLES", "$r = 1/2\\varphi$\n$u = 1 - r$", GOLD),
        ("SQUARE IT", "$(u+r)^2 = 1$", BOUND_C),
    ], W, bh=0.72, fs=8.0, capfs=7.8)

    yv = y - 0.50
    vals = [("$W_L = u^2$", "0.477457514063", LIGHT_C),
            ("$W_B = 2ur$", "0.427050983125", BOUND_C),
            ("$W_M = r^2$", "0.095491502813", MATTER_C)]
    xw = (W - 0.60) / 3
    for i, (sym, v, col) in enumerate(vals):
        x = 0.30 + i * xw
        ax.text(x + xw / 2, yv + 0.20, sym, ha="center", va="center",
                fontsize=9.0, color=col, weight="bold")
        ax.text(x + xw / 2, yv + 0.03, v, ha="center", va="center",
                fontsize=8.0, color=INK)
    ax.text(W / 2, yv - 0.20, "sum $= 1$ exactly", ha="center", va="center",
            fontsize=8.4, color=NAVY, weight="bold")
    foot(ax, W, [
        ("The partition is exact algebra. Light, Boundary and Matter are the "
         "names of the three roles, and the", None),
        ("physical reading of those names is a later hypothesis that the "
         "observable dictionary has to earn.", GOLD),
    ], y=0.30)
    save(fig, "fl_f06_update.png")


# ══════════════════════════════════════════════ F7  the chiral split
def f7_chiral():
    H = 0.62 + 0.74 + 0.34 + 0.50
    fig, ax = canvas(W, H)
    head(ax, W, H, "CHIRAL SPLIT, GOVERNING OPERATOR, ACTION CLASS",
         "a wave decomposition and an action reconstruction, with no "
         "supersymmetry anywhere in it")
    y = H - 0.62 - 0.74
    chain(ax, y, [
        ("WAVE", "$\\partial_u \\partial_v X = 0$", NAVY),
        ("SPLIT", "$X = X_L(u) + X_R(v)$", MATTER_C),
        ("FREEZE", "a slice retains the\nphase relation", GOLD),
        ("OPERATOR", "$\\dot\\psi = -i\\,\\Omega\\Gamma\\,\\psi$", BOUND_C),
        ("CLASS", "$[S]_E$", TEAL),
    ], W, bh=0.74, fs=7.0, capfs=7.4)
    ax.text(W / 2, y - 0.30,
            "$S[q] = \\int d\\tau \\;\\frac{1}{2}\\left[\\,\\dot q^2 - q\\cdot"
            "\\Omega^2 q\\,\\right]$   is one representative of the class, "
            "not the class",
            ha="center", va="center", fontsize=9.0, color=NAVY)
    foot(ax, W, [
        ("The left and right split follows from characteristic factorisation. "
         "No superpartner and no fermion-boson pairing enters.", None),
        ("A sum of endpoint amplitudes does not record which phase arrived from "
         "which branch, and later coupling depends on that.", GOLD),
    ], y=0.30)
    save(fig, "fl_f07_chiral.png")


# ══════════════════════════════════════════════ F8  Godel and the lift
def f8_godel():
    plot_h = 1.92
    caps = ["Event coincidence and elapsed proper time are different "
            "invariants. The projection closes; the lifted account does not.",
            "This dissolves \"same event, therefore same complete occurrence\". "
            "It does not alter the local solution."]
    ncap = len(caps)
    H = TOP + T_H + S_H + plot_h + 0.20 + ncap * CAP_H + BOT
    fig = plt.figure(figsize=(W, H), dpi=DPI)
    fig.patch.set_facecolor("white")
    y_plot = (BOT + ncap * CAP_H + 0.20) / H
    fig.text(0.5, 1 - (TOP + T_H * 0.62) / H,
             "RECURRENCE IN PROJECTION IS NOT RETURN OF THE STATE",
             ha="center", va="center", fontsize=12.0, color=NAVY, weight="bold")
    fig.text(0.5, 1 - (TOP + T_H + S_H * 0.48) / H,
             "the circle is the spacetime projection; the helix is the state "
             "with its retained record",
             ha="center", va="center", fontsize=7.2, color=SLATE)
    for i, ln in enumerate(caps):
        yy = (BOT + (ncap - 1 - i) * CAP_H + CAP_H * 0.40) / H
        fig.text(0.5, yy, ln, ha="center", va="center", fontsize=7.0,
                 color=GOLD if i else SLATE, style="italic")

    axl = fig.add_axes([0.06, y_plot, 0.40, plot_h / H])
    axl.set_aspect("equal"); axl.axis("off")
    th = np.linspace(0, 2 * np.pi, 400)
    axl.plot(np.cos(th), np.sin(th), color=MATTER_C, lw=1.6)
    axl.plot([1], [0], marker="o", ms=7, color=NAVY, mec="white", mew=1.0,
             zorder=4)
    axl.annotate("", xy=(np.cos(0.45), np.sin(0.45)), xytext=(1.0, 0.0),
                 arrowprops=dict(arrowstyle="-|>", mutation_scale=10,
                                 color=GOLD, lw=1.4))
    axl.text(1.14, 0.06, "$\\gamma(0) = \\gamma(T)$", ha="left", va="center",
             fontsize=8.0, color=NAVY)
    axl.set_xlim(-1.35, 1.75); axl.set_ylim(-1.35, 1.35)
    axl.text(0, -1.22, "the projection: same event", ha="center", va="center",
             fontsize=7.6, color=MATTER_C, weight="bold")

    axr = fig.add_axes([0.50, y_plot, 0.46, plot_h / H], projection="3d")
    t = np.linspace(0, 3 * 2 * np.pi, 700)
    axr.plot(np.cos(t), np.sin(t), t / (2 * np.pi), color=BOUND_C, lw=1.5)
    axr.scatter([1, 1, 1], [0, 0, 0], [0, 1, 2], color=NAVY, s=16, zorder=5)
    axr.set_xticks([]); axr.set_yticks([])
    axr.set_zticks([0, 1, 2, 3])
    axr.tick_params(axis="z", colors=SLATE, labelsize=6)
    axr.set_zlabel("retained record", fontsize=6.8, color=SLATE, labelpad=-6)
    axr.grid(False)
    for pane in (axr.xaxis, axr.yaxis, axr.zaxis):
        pane.pane.fill = False
        pane.pane.set_edgecolor(LINE)
    axr.view_init(elev=18, azim=-58)
    axr.text2D(0.5, -0.02, "the lift: the same three events, three records",
               transform=axr.transAxes, ha="center", fontsize=7.6,
               color=BOUND_C, weight="bold")
    save(fig, "fl_f08_godel.png")


# ══════════════════════════════════════════════ F9  four scalars, three readouts
def f9_scalars():
    """Four scalars in, three readouts out, and the fan of arrows deleted.

    The first version drew an arrow from every scalar to every readout, which
    said nothing except that the plate was busy. What the reader needs is which
    scalars COMBINE, so the two that combine are bracketed and the one direction
    the bracket cannot resolve is stated once underneath.
    """
    ROW, GAPR = 0.38, 0.13
    H = 0.66 + 4 * ROW + 3 * GAPR + 0.46 + 0.62
    fig, ax = canvas(W, H)
    head(ax, W, H, "FOUR FIELD SCALARS, THREE GEOMETRIC READOUTS",
         "the map has rank three, so exactly one direction of the field is "
         "invisible to geometry")
    bw = 1.62
    xl, xr = 0.30, W - 0.30 - bw
    ytop = H - 0.66
    lefts = [("$\\alpha_L$", "light packing", LIGHT_C),
             ("$\\nu$", "number density", TEAL),
             ("$\\alpha_M$", "matter scale, clock", MATTER_C),
             ("$\\theta$", "cyclic phase", BOUND_C)]
    ys = []
    for i, (sym, txt, col) in enumerate(lefts):
        y = ytop - i * (ROW + GAPR) - ROW
        ys.append(y)
        tint(ax, xl, y, bw, ROW, col, a=0.11)
        box(ax, xl, y, bw, ROW, col, fill="none", lw=0.9)
        ax.text(xl + 0.16, y + ROW / 2, sym, ha="left", va="center",
                fontsize=9.4, color=col, weight="bold")
        ax.text(xl + 0.58, y + ROW / 2, txt, ha="left", va="center",
                fontsize=7.0, color=INK)

    # the bracket over the two that combine
    xb = xl + bw + 0.13
    ytA, ytB = ys[0] + ROW - 0.04, ys[1] + 0.04
    ax.plot([xb, xb + 0.12, xb + 0.12, xb], [ytA, ytA, ytB, ytB], color=GOLD,
            lw=1.1, zorder=3)
    ax.text(xb + 0.20, (ytA + ytB) / 2, "combine", ha="left", va="center",
            fontsize=6.8, color=GOLD, weight="bold", rotation=90)

    rights = [("$B = \\alpha_L + \\nu/3$", "the spatial potential", TEAL,
               (ytA + ytB) / 2),
              ("$A = -\\alpha_M$", "the clock potential", MATTER_C,
               ys[2] + ROW / 2),
              ("$\\theta$", "carried through unchanged", BOUND_C,
               ys[3] + ROW / 2)]
    xa0 = xb + 0.40
    for sym, txt, col, yc in rights:
        y = yc - ROW / 2
        tint(ax, xr, y, bw, ROW, col, a=0.11)
        box(ax, xr, y, bw, ROW, col, fill="none", lw=0.9)
        ax.text(xr + bw / 2, y + ROW / 2 + 0.07, sym, ha="center", va="center",
                fontsize=8.6, color=col, weight="bold")
        ax.text(xr + bw / 2, y + ROW / 2 - 0.10, txt, ha="center", va="center",
                fontsize=6.5, color=SLATE)
        arrow(ax, xa0, yc, xr - 0.05, yc, color=SLATE, lw=0.9, ms=7)
    # the rank goes on the kernel line, not above the columns, where it would
    # have to fight the subtitle for the same band
    yk = ys[3] - 0.30
    ax.text(W / 2, yk,
            "rank 3,  nullity 1,  kernel    "
            "$\\alpha_L \\rightarrow \\alpha_L + \\delta$,     "
            "$\\nu \\rightarrow \\nu - 3\\delta$",
            ha="center", va="center", fontsize=9.6, color=NAVY, weight="bold")
    foot(ax, W, [
        ("Both potentials are fixed and one combination is not. That is exact "
         "non-identifiability, not a small uncertainty:", None),
        ("a geometry-only account can never separate light packing from number "
         "density without further structure.", GOLD),
    ], y=0.30)
    save(fig, "fl_f09_scalars.png")


# ══════════════════════════════════════════════ F11 equivalence
def f11_equivalence():
    H = 2.30
    fig, ax = canvas(W, H)
    head(ax, W, H, "INERTIA AND GRAVITATION AS TWO READINGS OF ONE COST",
         "a unification claim only if one generator produces both without a "
         "composition-dependent remainder")
    cy = 1.16
    rr = 0.50
    lx, rx = 1.24, W - 1.24
    for x, lab, sub, col in ((lx, "OBJECT SIDE", "resistance to\nchanged motion",
                             MATTER_C),
                             (rx, "GEOMETRY SIDE", "source of\ncurvature", TEAL)):
        ax.add_patch(Circle((x, cy), rr, facecolor=col, alpha=0.13,
                            edgecolor=col, lw=1.1, zorder=2))
        ax.text(x, cy + 0.13, lab, ha="center", va="center", fontsize=7.4,
                color=col, weight="bold")
        ax.text(x, cy - 0.13, sub, ha="center", va="center", fontsize=6.8,
                color=INK, linespacing=1.5)
    bw, bh = 1.42, 0.46
    bx = (lx + rx) / 2 - bw / 2
    tint(ax, bx, cy - bh / 2, bw, bh, GOLD, a=0.14)
    box(ax, bx, cy - bh / 2, bw, bh, GOLD, fill="none", lw=1.1)
    ax.text(bx + bw / 2, cy + 0.09, "ONE RETENTION COST", ha="center",
            va="center", fontsize=7.4, color=GOLD, weight="bold")
    ax.text(bx + bw / 2, cy - 0.10, "one operation, two readouts", ha="center",
            va="center", fontsize=6.6, color=SLATE)
    arrow(ax, bx - 0.04, cy, lx + rr + 0.04, cy, lw=1.1, color=SLATE)
    arrow(ax, bx + bw + 0.04, cy, rx - rr - 0.04, cy, lw=1.1, color=SLATE)
    ax.text(W / 2, 0.74,
            "$\\gamma = (\\alpha_L + \\nu/3)/\\alpha_M$   with   "
            "$\\nu = 3(\\alpha_M - \\alpha_L)$   $\\Rightarrow$   "
            "$\\gamma = 1$  identically",
            ha="center", va="center", fontsize=9.4, color=NAVY, weight="bold")
    foot(ax, W, [
        ("Not agreement inside an error bar. An identity, for any amount of "
         "crowding, at any precision.", None),
        ("The obligation that remains is one source action yielding universal "
         "free fall, redshift and light bending together.", GOLD),
    ], y=0.30)
    save(fig, "fl_f11_equivalence.png")


# ══════════════════════════════════════════════ F12 the dark sector
def f12_dark():
    H = 2.66
    fig, ax = canvas(W, H)
    head(ax, W, H, "THREE DIFFERENT LOGICAL OBJECTS IN THE DARK SECTOR",
         "an exact density identity, a proposed mechanism and a withdrawn "
         "energy estimate are not the same kind of thing")
    cards = [
        ("EXACT IDENTITY", MATTER_C,
         "$\\Omega_c = W_B/\\varphi = 4r^2(1-r)$",
         "0.263932022500",
         "An algebraic readout.\nIt does not identify\na particle."),
        ("PROPOSED MECHANISM", GOLD,
         "self-holding modes,",
         "neutral under the\nvisible projection",
         "Must reproduce cold\nclustering, lensing and\ngrowth. Not yet derived."),
        ("WITHDRAWN ROUTE", MAUVE,
         "vacuum crowding energy",
         "as galactic mass",
         "Short by about eleven\norders of magnitude.\nKept so it cannot\nreturn renamed."),
    ]
    gx = 0.16
    cw = (W - 0.60 - 2 * gx) / 3
    chh = 1.52
    y = H - 0.70 - chh
    for i, (cap, col, l1, l2, note) in enumerate(cards):
        x = 0.30 + i * (cw + gx)
        tint(ax, x, y, cw, chh, col, a=0.08)
        box(ax, x, y, cw, chh, col, fill="none", lw=1.0)
        ax.add_patch(FancyBboxPatch((x, y + chh - 0.26), cw, 0.26,
                                    boxstyle="round,pad=0,rounding_size=0.03",
                                    linewidth=0, facecolor=col, alpha=0.88,
                                    zorder=3))
        ax.text(x + cw / 2, y + chh - 0.13, cap, ha="center", va="center",
                fontsize=7.0, color="white", weight="bold", zorder=4)
        ax.text(x + cw / 2, y + chh - 0.50, l1, ha="center", va="center",
                fontsize=7.6, color=INK)
        ax.text(x + cw / 2, y + chh - 0.74, l2, ha="center", va="center",
                fontsize=7.6, color=col, weight="bold", linespacing=1.5)
        ax.text(x + cw / 2, y + 0.34, note, ha="center", va="center",
                fontsize=6.5, color=SLATE, linespacing=1.55)
    foot(ax, W, [
        ("The exact fraction is not evidence for the mechanism, and the "
         "withdrawn estimate is not evidence against it.", None),
        ("Keeping the three apart is what stops a number from being read as a "
         "particle.", GOLD),
    ], y=0.30)
    save(fig, "fl_f12_dark.png")


# ══════════════════════════════════════════════ F29 the vacuum ladder
def f29_ladder():
    H = 2.34
    fig, ax = canvas(W, H)
    head(ax, W, H, "THE MIDDLE LENGTH BETWEEN PLANCK AND VACUUM",
         "the geometric mean is dimensional bookkeeping; reading the middle "
         "length as a physical cell is the claim")
    cy = 1.28
    rr = 0.42
    xs = [1.06, W / 2, W - 1.06]
    labs = [("Planck length", "$\\ell_P$", MATTER_C),
            ("cell scale", "$a_0$", GOLD),
            ("vacuum length", "$L_\\Lambda$", TEAL)]
    for x, (nm, sym, col) in zip(xs, labs):
        ax.add_patch(Circle((x, cy), rr, facecolor=col, alpha=0.13,
                            edgecolor=col, lw=1.1, zorder=2))
        ax.text(x, cy + 0.10, sym, ha="center", va="center", fontsize=11.0,
                color=col, weight="bold")
        ax.text(x, cy - 0.17, nm, ha="center", va="center", fontsize=6.8,
                color=INK)
    for a, b in ((0, 1), (1, 2)):
        arrow(ax, xs[a] + rr + 0.05, cy, xs[b] - rr - 0.05, cy, lw=1.0,
              style="<|-|>", ms=7, color=SLATE)
        ax.text((xs[a] + xs[b]) / 2, cy + 0.16, "same ratio", ha="center",
                va="bottom", fontsize=7.0, color=GOLD, weight="bold")
    ax.text(W / 2, 0.80,
            "$\\ell_P\\, L_\\Lambda = a_0^{\\,2}$          "
            "$a_0 = 88.11\\;\\mu\\mathrm{m}$          "
            "$\\lambda = (4\\pi/\\sqrt{3})\\,r^{240} = 2.860\\times 10^{-122}$",
            ha="center", va="center", fontsize=8.8, color=NAVY, weight="bold")
    foot(ax, W, [
        ("The identity is exact to fifteen digits and it is dimensional. What is "
         "exposed to experiment is the branch choice:", None),
        ("tens of microns sits close enough to short-range gravity tests to be "
         "tested, and is not yet a detection.", GOLD),
    ], y=0.30)
    save(fig, "fl_f29_ladder.png")


# ══════════════════════════════════════════════ F30 the closing rule
def f30_close():
    H = 0.62 + 0.66 + 0.30 + 0.56
    fig, ax = canvas(W, H)
    head(ax, W, H, "WHERE EVERY SECTION HAS TO TERMINATE",
         "an observable test, or an explicitly named missing bridge")
    y = H - 0.62 - 0.66
    chain(ax, y, [
        ("IDENTITY", "exact inside\nthe algebra", MATTER_C),
        ("DICTIONARY", "the observable\nit is read as", GOLD),
        ("MECHANISM", "the field equation\nbehind it", BOUND_C),
        ("FORECAST", "a number\nexposed", TEAL),
        ("DEFEAT", "what would end\nthe programme", MAUVE),
    ], W, bh=0.66, fs=6.9, capfs=7.4)
    foot(ax, W, [
        ("The vocabulary is not the product. It is what lets a large programme "
         "stay readable without flattening", None),
        ("the status of its parts, and it is why an exact fraction never becomes "
         "a particle by prose alone.", GOLD),
    ], y=0.34)
    save(fig, "fl_f30_close.png")


if __name__ == "__main__":
    print("diagram plates:")
    f1_rule(); f2_timeline(); f3_pipeline(); f4_square(); f5_hotel()
    f6_update(); f7_chiral(); f8_godel(); f9_scalars(); f11_equivalence()
    f12_dark(); f29_ladder(); f30_close()

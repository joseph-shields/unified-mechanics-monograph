"""Shared plate machinery for the Field Ledger, second edition.

Three rules, all of them learned from breaking them:

1. Author at the width the plate is printed at. Every canvas is sized in final
   page inches, so a fontsize here is the point size on paper.
2. Reserve room before placing text. Caption lines are given explicitly; no
   automatic wrapping is trusted anywhere.
3. For anything with axes, lay the page out as a vertical budget in inches and
   derive the axes rectangle from it, so a caption can never land on an axis
   label however long the tick labels turn out to be.

Colour carries meaning or it is not used. Matter blue, Light gold and Boundary
magenta for the three channels; navy and slate for structure; teal for a reading
that moved toward measurement, rust for one that moved away, and mauve for an
object the book has withdrawn.
"""

import json, math, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Wedge
from matplotlib.colors import hsv_to_rgb

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "fl")
os.makedirs(IMG, exist_ok=True)
DPI = 400
W = 6.50

NAVY, GOLD, SLATE, INK = "#102A43", "#B48A2E", "#5B6B7A", "#243040"
TEAL, RUST, PALE, LINE = "#14707D", "#A8442A", "#F4F7F9", "#C7D3DE"
MAUVE = "#7B5A80"
LIGHT_C, BOUND_C, MATTER_C = "#B8811C", "#B8256B", "#1E6FB8"

plt.rcParams.update({
    "font.family": ["Constantia", "Cambria", "DejaVu Sans"],
    "mathtext.fontset": "cm",
    "text.color": INK,
    "savefig.facecolor": "white",
})

A09 = json.load(open(r"C:\Users\joesh\Desktop\SCI\ADDENDA\A09 The Master Equation"
                     r"\master_equation_results.json"))
A03 = json.load(open(r"C:\Users\joesh\Desktop\SCI\ADDENDA\A03 The Forward Solver"
                     r"\um_forward_solver_results.json"))
BY = {d["key"]: d for d in A09["rows"]}
ORDER = ["Omega_b", "Omega_c", "Omega_DE", "Y_He", "n_s", "tau"]
M = {"Omega_b": r"$\Omega_b$", "Omega_c": r"$\Omega_c$",
     "Omega_DE": r"$\Omega_{DE}$", "Y_He": r"$Y_{He}$",
     "n_s": r"$n_s$", "tau": r"$\tau$"}
THIRD = 1.0 / 3.0
PHI = (1 + math.sqrt(5)) / 2
Rr = 1 / (2 * PHI)


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


def arrow(ax, x0, y0, x1, y1, color=SLATE, lw=1.0, ms=8, style="-|>", rad=None):
    kw = dict(arrowstyle=style, mutation_scale=ms, linewidth=lw, color=color,
              zorder=3, shrinkA=0, shrinkB=0)
    if rad is not None:
        kw["connectionstyle"] = "arc3,rad=%f" % rad
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), **kw))


def head(ax, w, h, title, sub=None):
    ax.text(w / 2, h - 0.21, title, ha="center", va="center", fontsize=12.0,
            color=NAVY, weight="bold")
    if sub:
        ax.text(w / 2, h - 0.43, sub, ha="center", va="center", fontsize=7.2,
                color=SLATE)


def foot(ax, w, lines, y=0.30, col=SLATE, rule=True):
    """Caption lines under a rule, given explicitly, bottom-up."""
    if rule:
        ax.plot([0.26, w - 0.26], [y + 0.16, y + 0.16], color=LINE, lw=0.8)
    for i, (txt, c) in enumerate(lines):
        ax.text(w / 2, y - i * 0.155, txt, ha="center", va="center",
                fontsize=7.0, color=c or col, style="italic")


def save(fig, name):
    fig.savefig(os.path.join(IMG, name), dpi=DPI, facecolor="white")
    plt.close(fig)
    print("  ", name)


# ── the vertical budget for charted plates ─────────────────────────────────
TOP, T_H, S_H = 0.06, 0.26, 0.21
XL_H, CAP_H, BOT = 0.36, 0.155, 0.09


def chart(plot_h, title, sub, caption_lines, left=0.98, right=0.16,
          cap_col=GOLD):
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
                 color=cap_col, style="italic")
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(LINE)
    ax.tick_params(axis="x", colors=SLATE, labelsize=7.5, length=3)
    ax.tick_params(axis="y", colors=SLATE, labelsize=7.5, length=3)
    return fig, ax


def chain(ax, y, items, w, bh=0.66, gx=0.13, x0=0.18, fs=7.4, capfs=8.0):
    """A left-to-right chain of captioned boxes, the book's commonest diagram."""
    n = len(items)
    bw = (w - 2 * x0 - (n - 1) * gx) / n
    for i, (cap, body, col) in enumerate(items):
        x = x0 + i * (bw + gx)
        tint(ax, x, y, bw, bh, col, a=0.09)
        box(ax, x, y, bw, bh, col, fill="none", lw=1.0)
        ax.add_patch(FancyBboxPatch((x, y + bh - 0.24), bw, 0.24,
                                    boxstyle="round,pad=0,rounding_size=0.03",
                                    linewidth=0, facecolor=col, alpha=0.88,
                                    zorder=3))
        ax.text(x + bw / 2, y + bh - 0.12, cap, ha="center", va="center",
                fontsize=capfs * 0.92, color="white", weight="bold", zorder=4)
        ax.text(x + bw / 2, y + (bh - 0.24) / 2, body, ha="center", va="center",
                fontsize=fs, color=INK, linespacing=1.6)
        if i < n - 1:
            arrow(ax, x + bw + 0.016, y + bh / 2, x + bw + gx - 0.016,
                  y + bh / 2, lw=1.0)
    return bw

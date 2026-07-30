"""PREDICTION FROM THE COLOUR AVERAGE.

How a framework that does not sit still returns a number.

The complaint this answers is a fair one: if every quantity is the endpoint of a
flow rather than a constant, what use is a number? The answer is that the
prediction is not the fixed point. It is the average over the evolution, and
those are different numbers whenever the observable is curved, because

        < f(x) >  is not  f( <x> )

and the gap between them is the curvature of f against the spread of the flow.
Neither of those is adjustable. The map is the framework's own update, the spread
is the framework's own floor r^3, and the observables are the framework's own
closed forms. There is nothing here to tune.

The colour field is the instrument that reads it. Each step of the evolution
carries a channel signature, so it carries a hue. The evolution therefore traces
a path across the wheel, the path has a distribution, and the circular mean of
that distribution is the object's colour class. The number and the colour are two
readings of the same average.

    operation  ->  colour it  ->  evolve it  ->  average the colour  ->  the number

Run:  PYTHONUTF8=1 python colour_average_prediction.py
"""

import json, math, os, random, statistics, datetime
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb

HERE = os.path.dirname(os.path.abspath(__file__))
PHI = (1 + math.sqrt(5)) / 2
R = 1 / (2 * PHI)
R3 = R ** 3

HUE_L, HUE_M, HUE_B = 20.0, 200.0, 110.0        # Plate 1 convention

NAVY, GOLD, SLATE, INK = "#102A43", "#B48A2E", "#5B6B7A", "#243040"
LINE, PALE = "#C7D3DE", "#F4F7F9"
plt.rcParams.update({"font.family": ["Constantia", "Cambria", "DejaVu Sans"],
                     "text.color": INK})


def update(x):
    """The framework's own update, written on the contraction coordinate."""
    return 1.0 / (4.0 * x + 2.0)


# Each observable as an explicit function of the two poles, kept independent so
# the channel signature can be read off. u is the light pole, m the matter pole.
OBSERVABLES = [
    ("Omega_b",  "u,m -> m^2 / 2",          lambda u, m: m * m / 2,
     0.0493017, 0.0007,  "Planck 2018"),
    ("Y_He",     "u,m -> u^2 / 2",          lambda u, m: u * u / 2,
     0.245,     0.003,   "BBN"),
    ("Omega_c",  "u,m -> 4 m^2 u",          lambda u, m: 4 * m * m * u,
     0.2645,    0.0026,  "Planck 2018"),
    ("n_s",      "u,m -> 1 - m^2 + 2 m^3",  lambda u, m: 1 - m * m + 2 * m ** 3,
     0.9649,    0.0042,  "Planck 2018"),
    ("tau",      "u,m -> 2 m^3",            lambda u, m: 2 * m ** 3,
     0.0544,    0.0073,  "Planck 2018"),
    ("Omega_DE", "u,m -> 1 - m^2/2 - 4m^2 u",
     lambda u, m: 1 - m * m / 2 - 4 * m * m * u, 0.6847, 0.0073, "Planck 2018"),
]


def signature(f, x, h=1e-7):
    """(s_L, s_M): the log-sensitivity of f to each pole at this point of the flow."""
    u, m = 1.0 - x, x
    v = f(u, m)
    if v == 0:
        return 0.0, 0.0
    dL = (f(u + h, m) - f(u - h, m)) / (2 * h)
    dM = (f(u, m + h) - f(u, m - h)) / (2 * h)
    return u * dL / v, m * dM / v


def hue_of(f, x):
    """The channel address of f at this point of the flow."""
    sL, sM = signature(f, x)
    aL, aM = abs(sL), abs(sM)
    u, m = 1.0 - x, x
    WL, WM, WB = u * u, m * m, 2 * u * m
    cross = 2 * math.sqrt(aL * aM) / (aL + aM) if (aL > 0 and aM > 0) else 0.0
    w = [WL * aL, WM * aM, WB * cross]
    z = sum(wi * complex(math.cos(math.radians(hi)), math.sin(math.radians(hi)))
            for hi, wi in zip([HUE_L, HUE_M, HUE_B], w))
    if abs(z) < 1e-15:
        return HUE_M, 0.0
    return math.degrees(math.atan2(z.imag, z.real)) % 360.0, abs(z) / sum(w)


def evolve(n=200000, burn=2000, seed=11):
    """Run the flow. The state does not rest at r: the framework's own third-law
    statement is that exact r is unreachable in finitely many noisy cycles, and
    the recorded RMS fluctuation is the floor. So the spread is r^3, not a choice.
    The perturbation is applied to the coordinate itself, which is what the floor
    is a floor on."""
    rng = random.Random(seed)
    x = 0.5
    out = []
    scale = R3 * math.sqrt(3.0)          # uniform with standard deviation r^3
    for i in range(n + burn):
        x = update(x) + scale * rng.uniform(-1.0, 1.0)
        if i >= burn:
            out.append(x)
    return np.array(out)


def circular_mean(hues, weights=None):
    if weights is None:
        weights = np.ones_like(hues)
    z = np.sum(weights * np.exp(1j * np.radians(hues)))
    return math.degrees(math.atan2(z.imag, z.real)) % 360.0, abs(z) / np.sum(weights)


xs = evolve()
print("PREDICTION FROM THE COLOUR AVERAGE")
print("=" * 96)
print("the flow: x -> 1/(4x+2), perturbed at the floor r^3 = %.9f" % R3)
print("   <x> = %.9f      sd = %.9f      r = %.9f" % (xs.mean(), xs.std(), R))
print()

rows = []
print("%-10s %-26s %12s %12s %12s %9s %9s"
      % ("observable", "operation", "static f(r)", "<f> evolved", "measured",
         "static", "evolved"))
for key, expr, f, meas, sig, src in OBSERVABLES:
    static = f(1 - R, R)
    vals = np.array([f(1 - x, x) for x in xs])
    avg = vals.mean()
    hues = np.array([hue_of(f, x)[0] for x in xs[::37]])      # thinned, for the graph
    hbar, coh = circular_mean(hues)
    hue_static = hue_of(f, R)[0]
    rows.append(dict(key=key, expr=expr, static=static, evolved=avg, measured=meas,
                     sigma=sig, source=src,
                     static_pct=100 * (static / meas - 1),
                     evolved_pct=100 * (avg / meas - 1),
                     hue_static=hue_static, hue_mean=hbar, coherence=coh,
                     hue_spread=float(np.std(hues)),
                     pull_static=(static - meas) / sig,
                     pull_evolved=(avg - meas) / sig,
                     hues=hues.tolist()))
    print("%-10s %-26s %12.8f %12.8f %12.8f %+8.2f%% %+8.2f%%"
          % (key, expr, static, avg, meas,
             100 * (static / meas - 1), 100 * (avg / meas - 1)))

print()
print("moved toward measurement: %d of %d"
      % (sum(1 for d in rows if abs(d["evolved_pct"]) < abs(d["static_pct"])), len(rows)))
print()
print("%-10s %11s %11s %11s %11s" % ("observable", "hue static", "hue mean",
                                     "coherence", "hue spread"))
for d in rows:
    print("%-10s %11.3f %11.3f %11.4f %11.4f"
          % (d["key"], d["hue_static"], d["hue_mean"], d["coherence"], d["hue_spread"]))

json.dump({"generated": datetime.datetime.now().isoformat(timespec="seconds"),
           "r": R, "r3": R3, "x_mean": float(xs.mean()), "x_sd": float(xs.std()),
           "rows": [{k: v for k, v in d.items() if k != "hues"} for d in rows]},
          open(os.path.join(HERE, "colour_average_prediction_results.json"), "w"),
          indent=2)

# ─────────────────────────────────────────────────────── the plate
n = len(rows)
fig = plt.figure(figsize=(6.9, 0.80 * n + 1.30), dpi=400)
ax = fig.add_axes([0, 0, 1, 1])
W, H = 6.9, 0.80 * n + 1.30
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
fig.patch.set_facecolor("white")

ax.text(W / 2, H - 0.22, "PREDICTION FROM THE COLOUR AVERAGE",
        ha="center", va="center", fontsize=12.5, color=NAVY, weight="bold")
ax.text(W / 2, H - 0.45,
        "the operation, its evolution coloured, and the number the average returns",
        ha="center", va="center", fontsize=7.2, color=SLATE)

y = H - 0.78
ax.text(0.30, y, "operation", fontsize=6.6, color=SLATE, weight="bold")
ax.text(2.02, y, "the evolution, coloured", fontsize=6.6, color=SLATE, weight="bold")
ax.text(4.86, y, "static", fontsize=6.6, color=SLATE, weight="bold", ha="center")
ax.text(5.62, y, "evolved", fontsize=6.6, color=SLATE, weight="bold", ha="center")
ax.text(6.40, y, "measured", fontsize=6.6, color=SLATE, weight="bold", ha="center")
ax.plot([0.25, W - 0.25], [y - 0.10, y - 0.10], color=LINE, lw=0.7)

for i, d in enumerate(rows):
    yy = H - 1.10 - i * 0.80
    ax.text(0.30, yy + 0.20, d["key"], fontsize=8.2, color=NAVY, weight="bold")
    ax.text(0.30, yy - 0.02, d["expr"], fontsize=6.4, color=INK)
    better = abs(d["evolved_pct"]) < abs(d["static_pct"])
    ax.text(0.30, yy - 0.22,
            ("closer by %.2f pts" % (abs(d["static_pct"]) - abs(d["evolved_pct"])))
            if better else "moves away",
            fontsize=6.0, color=(GOLD if better else "#B8256B"), style="italic")

    # the colour graph. A single-channel observable has no hue to vary, so it
    # gets a solid swatch: the value still evolves, the colour class does not.
    hs = np.array(d["hues"])
    x0, x1, hgt = 2.02, 4.10, 0.30
    if d["hue_spread"] < 1e-6:
        col = hsv_to_rgb([(d["hue_mean"] / 360.0) % 1.0, 0.72, 0.98])
        ax.add_patch(plt.Rectangle((x0, yy - hgt / 2 + 0.02), x1 - x0, hgt,
                                   facecolor=col, edgecolor="none"))
        ax.text((x0 + x1) / 2, yy - hgt / 2 - 0.11,
                "one pure channel  ·  hue fixed at %.0f°  ·  no spread to average"
                % d["hue_mean"], fontsize=5.7, color=SLATE, ha="center", va="center")
    else:
        lo, hi = hs.min(), hs.max()
        pad = (hi - lo) * 0.10
        lo, hi = lo - pad, hi + pad
        grid = np.linspace(lo, hi, 420)
        counts, _ = np.histogram(hs, bins=grid)
        dens = counts / counts.max() if counts.max() else counts
        cols = hsv_to_rgb(np.stack([(grid[:-1] / 360.0) % 1.0,
                                    np.full(len(dens), 0.72),
                                    np.full(len(dens), 0.98)], axis=-1))
        for k in range(len(dens)):
            if dens[k] <= 0:
                continue
            xa = x0 + (x1 - x0) * k / len(dens)
            ax.add_patch(plt.Rectangle((xa, yy - hgt / 2 + 0.02),
                                       (x1 - x0) / len(dens) * 1.02,
                                       hgt * dens[k], facecolor=cols[k],
                                       edgecolor="none"))
        ax.plot([x0, x1], [yy - hgt / 2 + 0.02] * 2, color=LINE, lw=0.7)
        xm = x0 + (x1 - x0) * (d["hue_mean"] - lo) / (hi - lo)
        ax.plot([xm, xm], [yy - hgt / 2 - 0.03, yy + hgt / 2 + 0.05],
                color=NAVY, lw=1.1)
        ax.text((x0 + x1) / 2, yy - hgt / 2 - 0.11,
                "mean hue %.2f°   spread %.2f°   coherence %.4f"
                % (d["hue_mean"], d["hue_spread"], d["coherence"]),
                fontsize=5.7, color=SLATE, ha="center", va="center")

    ax.text(4.86, yy + 0.06, "%.6f" % d["static"], fontsize=6.6, color=INK, ha="center")
    ax.text(4.86, yy - 0.12, "%+.2f%%" % d["static_pct"], fontsize=6.2,
            color=SLATE, ha="center")
    ax.text(5.62, yy + 0.06, "%.6f" % d["evolved"], fontsize=6.6,
            color=NAVY, ha="center", weight="bold")
    ax.text(5.62, yy - 0.12, "%+.2f%%" % d["evolved_pct"], fontsize=6.2,
            color=(GOLD if better else "#B8256B"), ha="center", weight="bold")
    ax.text(6.40, yy + 0.06, "%.6f" % d["measured"], fontsize=6.6, color=INK, ha="center")
    ax.text(6.40, yy - 0.12, d["source"], fontsize=5.6, color=SLATE, ha="center")
    if i < n - 1:
        ax.plot([0.25, W - 0.25], [yy - 0.40] * 2, color="#E8EDF2", lw=0.6)

ax.plot([0.25, W - 0.25], [0.36, 0.36], color=LINE, lw=0.7)
ax.text(W / 2, 0.20,
        "flow  x → 1/(4x+2)  perturbed at the floor r³ = %.6f.   Nothing fitted: "
        "the map, the spread and the forms are all the framework's own." % R3,
        ha="center", va="center", fontsize=6.2, color=SLATE)

out = os.path.join(HERE, "colour_average_prediction.png")
fig.savefig(out, dpi=400)
plt.close(fig)
print("\nplate:", out)

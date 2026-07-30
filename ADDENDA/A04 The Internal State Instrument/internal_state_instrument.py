"""THE INTERNAL STATE INSTRUMENT.

What the resolution operator is for.

Once resolution is defined invariantly as N = q / dq, the operator stops asking
how well an observer measured something and starts asking how sharply the thing
defines itself. A body with one crisp value of a quantity has a large N. A body
whose quantity is smeared across its own surface has a small one, before anybody
measures anything.

That gives two readings of the same body:

    EXTERNAL   q          the single number that gets quoted
    INTERNAL   q H5(N)    what is left once the body's own spread is charged for

and the gap between them is the uncoupling. For surface gravity the spread is
not measurement error at all: an oblate rotating body genuinely has different g
at its equator and its pole, so g does not have one value to know.

Everything here is computed from M, R_eq, R_pol and the rotation period. No
value of g is looked up.

    g_pol = GM / R_pol^2
    g_eq  = GM / R_eq^2 - omega^2 R_eq

That neglects the quadrupole contribution to the potential, so it lands within
about a third of a per cent of published equatorial and polar values. It is the
right approximation here because the spread is dominated by the two radii and
the centrifugal term, and both are in it.

Run:  PYTHONUTF8=1 python internal_state_instrument.py
"""

import json, math, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "internal_state_instrument_results.json")

G = 6.67430e-11
c = 2.99792458e8
phi = (1 + math.sqrt(5)) / 2
r = 1 / (2 * phi)
r3 = r ** 3
N_JOIN = 5 / r3                      # 40 phi^3 = 169.4427, the corpus floor


def H5(N):
    s = N / (N + 1.0)
    t = s ** 10
    return 2 * t / (1 + t)


def deficit(N):
    return 1.0 - H5(N)


#  name              M (kg)        R_eq (m)     R_pol (m)    period (s)
BODIES = [
    ("Sun",          1.98847e30,   6.957e8,     6.957e8,     25.05 * 86400),
    ("Earth",        5.97219e24,   6.378137e6,  6.356752e6,  86164.0905),
    ("Moon",         7.342e22,     1.73814e6,   1.73598e6,   27.321661 * 86400),
    ("Mars",         6.4171e23,    3.396200e6,  3.376200e6,  88642.663),
    ("Jupiter",      1.89813e27,   7.1492e7,    6.6854e7,    9.9250 * 3600),
    ("Saturn",       5.68340e26,   6.0268e7,    5.4364e7,    10.656 * 3600),
    ("Uranus",       8.68130e25,   2.5559e7,    2.4973e7,    17.24 * 3600),
    ("Neptune",      1.02413e26,   2.4764e7,    2.4341e7,    16.11 * 3600),
    # Sirius B, a white dwarf: slow rotator, very nearly spherical
    ("Sirius B",     2.063e30,     5.8e6,       5.7994e6,    None),
    # a canonical millisecond pulsar, deformed by rotation at 641 Hz
    ("PSR B1937+21", 2.78e30,      1.20e4,      1.185e4,     1.0 / 641.9),
]


def body_row(name, M, Req, Rpol, period):
    GM = G * M
    omega = 0.0 if period is None else 2 * math.pi / period
    g_pol = GM / Rpol ** 2
    g_eq = GM / Req ** 2 - omega ** 2 * Req
    # The external value is the midpoint of the body's own spread, and dq is the
    # half-range about that same midpoint. Centring anywhere else makes N depend
    # on a convention rather than on the body, and shifts it a few per cent.
    g_ext = (g_eq + g_pol) / 2.0
    dg = abs(g_pol - g_eq) / 2.0                  # intrinsic half-spread
    N = g_ext / dg if dg > 0 else float("inf")
    h = H5(N)
    chi = 2 * GM / (((Req + Rpol) / 2) * c ** 2)  # compactness
    f = (Req - Rpol) / Req                        # flattening
    q_rot = omega ** 2 * Req ** 3 / GM            # rotational parameter
    return dict(name=name, g_external=g_ext, g_eq=g_eq, g_pol=g_pol,
                spread=dg, N=N, H5=h, g_internal=g_ext * h,
                deficit_pct=100 * deficit(N), asymptote_pct=100 * 5 / N,
                flattening=f, q_rot=q_rot, compactness=chi,
                side=("below" if N < N_JOIN else "above"))


rows = [body_row(*b) for b in BODIES]

print("THE INTERNAL STATE INSTRUMENT")
print("=" * 100)
print("resolution comes from the body, not the measurement:  N = g / dg,"
      "   dg = (g_pol - g_eq)/2")
print("the corpus floor sits at N = 5/r^3 = 40 phi^3 = %.4f\n" % N_JOIN)
print("%-13s %9s %9s %9s %10s %9s %8s %9s %6s"
      % ("body", "g_ext", "g_eq", "g_pol", "spread", "N", "deficit", "g_int", "side"))
for d in sorted(rows, key=lambda x: x["N"]):
    print("%-13s %9.4f %9.4f %9.4f %10.5f %9.2f %7.3f%% %9.4f %6s"
          % (d["name"], d["g_external"], d["g_eq"], d["g_pol"], d["spread"],
             d["N"], d["deficit_pct"], d["g_internal"], d["side"]))

print("\nthe deficit is 5/N to the precision the asymptote claims:")
print("%-13s %10s %10s %8s" % ("body", "exact", "5/N", "agree"))
for d in sorted(rows, key=lambda x: x["N"]):
    print("%-13s %9.4f%% %9.4f%% %8s"
          % (d["name"], d["deficit_pct"], d["asymptote_pct"],
             "yes" if abs(d["deficit_pct"] - d["asymptote_pct"]) < 0.02 * max(1, d["deficit_pct"]) else "-"))

print("\nN is independent of how strong the gravity is. It tracks shape, not mass:")
print("%-13s %11s %11s %11s %9s" % ("body", "compactness", "flattening", "q_rot", "N"))
for d in sorted(rows, key=lambda x: x["N"]):
    print("%-13s %11.3e %11.3e %11.3e %9.2f"
          % (d["name"], d["compactness"], d["flattening"], d["q_rot"], d["N"]))

# ─────────────────────────────────────────────── the invariance demonstration
print("\n" + "=" * 100)
print("UNIT INVARIANCE. Jupiter's g, in five unit systems, one N.")
J = [d for d in rows if d["name"] == "Jupiter"][0]
print("%-14s %14s %14s %12s %10s" % ("unit", "g_ext", "spread", "N", "deficit"))
for unit, k in (("m/s^2", 1.0), ("cm/s^2", 100.0), ("ft/s^2", 3.280839895),
                ("g (Earth)", 1 / 9.80665), ("furlong/fortnight^2", 1.0 / 1.3054e-6)):
    ge, sp = J["g_external"] * k, J["spread"] * k
    print("%-14s %14.5g %14.5g %12.5f %9.4f%%"
          % (unit, ge, sp, ge / sp, 100 * deficit(ge / sp)))
print("   the ratio cannot be moved by a unit, so neither can the reading.")

# ─────────────────────────────────────────────── distances
print("\n" + "=" * 100)
print("DISTANCES. Same instrument, spread is whatever genuinely smears the value.")
DIST = [
    ("Earth to Moon",    3.84400e8,  2.1000e7,  "perigee to apogee, a real excursion"),
    ("1 AU",             1.495979e11, 2.5000e9, "Earth's own orbital eccentricity"),
    ("Earth to Mars",    2.25e11,     1.00e11,  "opposition to conjunction"),
    ("Proxima Centauri", 4.0175e16,   2.8e12,   "Gaia DR3 parallax"),
    ("Galactic centre",  2.5567e20,   9.46e17,  "8.28 +- 0.031 kpc"),
    ("Andromeda",        2.3995e22,   6.62e20,  "2.537 +- 0.070 Mly"),
    ("Hubble length",    1.3700e26,   1.1e25,   "the H0 basins themselves"),
]
print("%-18s %12s %12s %11s %9s %6s  %s"
      % ("separation", "q (m)", "dq (m)", "N", "deficit", "side", "what smears it"))
drows = []
for name, q, dq, why in DIST:
    N = q / dq
    drows.append(dict(name=name, q=q, dq=dq, N=N, deficit_pct=100 * deficit(N),
                      side="below" if N < N_JOIN else "above", why=why))
    print("%-18s %12.4e %12.4e %11.3f %8.4f%% %6s  %s"
          % (name, q, dq, N, 100 * deficit(N),
             "below" if N < N_JOIN else "above", why))

json.dump({"generated": datetime.datetime.now().isoformat(timespec="seconds"),
           "N_join": N_JOIN, "bodies": rows, "distances": drows},
          open(OUT, "w"), indent=2)

print("\n" + "=" * 100)
below = [d["name"] for d in rows + drows if d["side"] == "below"]
print("below the join, so carrying a claim the corpus licenses:")
print("   " + ", ".join(below))
print("\nwritten:", OUT)

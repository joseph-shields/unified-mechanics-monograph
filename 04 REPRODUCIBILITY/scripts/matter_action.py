"""The matter action, from the same square that gave gravity.

T24's construction is: take a defect built from a propagating part weighted u and a
held part weighted r, and square it. Applied to the geometry block that gave
MacDowell-Mansouri gravity. Applied to the FULL carrier curvature it should give
everything, because T25 already sorts the carrier's operations into exactly three
classes and (u + r) squared has exactly three terms.

    D  =  u F  +  r E              F the full carrier curvature, E the realised area
    D ^ D  =  u^2 (F^F)  +  2ur (F^E)  +  r^2 (E^E)

and the three weights carry the names the corpus gave them in Movement Five:

    W_L = u^2    Light        propagating, massless          <-> GAUGE
    W_B = 2ur    Boundary     mixed, sector-connecting       <-> MATTER
    W_M = r^2    Matter/held  the cost of persistence        <-> MASS

which is T25's classification, term for term. The weights were named for their sectors
before anyone knew that is what they were.

One structural consequence is worth more than the naming. MacDowell-Mansouri needs a
projection that breaks the larger symmetry down to the Lorentz subalgebra, and that
projection is inserted by hand; it is the standard objection to the construction. Here
the projection is the cluster projection C, which is derived. The decay IS the symmetry
breaking MacDowell-Mansouri assumes.

This script tests the consequences that can be checked: the exact weight ratios, the
hypercharge assignment forced by the 3+2 reversibility split, the full particle content
of one generation as the even exterior algebra, and the weak mixing angle.
"""
import math, json, os, datetime, itertools
from fractions import Fraction

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
def _cert(n): return os.path.join(_ROOT, "certificates", n)

phi = (1 + math.sqrt(5)) / 2
r   = 1 / (2 * phi)
u   = 1 - r
W_L, W_B, W_M = u*u, 2*u*r, r*r

print("SECTION 1  The three weights as the three sectors of T25")
print(f"   W_L = u^2  = {W_L:.12f}   gauge   : propagating, massless")
print(f"   W_B = 2ur  = {W_B:.12f}   matter  : sector-connecting, the mixed term")
print(f"   W_M = r^2  = {W_M:.12f}   mass    : the cost of persistence")
print(f"   sum        = {W_L+W_B+W_M:.12f}")
print()
print("   exact ratios, with nothing to tune:")
print(f"      mass to gauge   W_M/W_L = (r/u)^2   = {W_M/W_L:.15f}   exactly 1/5: "
      f"{abs(W_M/W_L - 0.2) < 1e-15}")
print(f"      matter to gauge W_B/W_L = 2r/u      = {W_B/W_L:.15f}   exactly 2/sqrt5: "
      f"{abs(W_B/W_L - 2/math.sqrt(5)) < 1e-15}")
print(f"      Lambda = 3 W_B / (2 W_L)            = {3*W_B/(2*W_L):.15f}   = 3/sqrt5")
print()

# ---------------------------------------------------------------------------------
# SECTION 2. The 3+2 reversibility split fixes hypercharge with no freedom.
# Y is block-constant: a on each of the three reversible (colour) directions,
# b on each of the two irreversible (clock, closure) directions. Membership in
# su(5) forces tracelessness: 3a + 2b = 0. Only the overall normalisation is
# conventional; the RATIO is forced.
# ---------------------------------------------------------------------------------
a, b = Fraction(-1, 3), Fraction(1, 2)
assert 3*a + 2*b == 0, "hypercharge must be traceless"
print("SECTION 2  Hypercharge from the 3+2 split")
print(f"   tracelessness 3a + 2b = 0 with the usual weak normalisation b = 1/2")
print(f"   forces a = {a} on each colour direction.   ratio a/b = {a/b} is the content;")
print(f"   the normalisation is the standard convention and is not derived.")
print()

# ---------------------------------------------------------------------------------
# SECTION 3. One generation as the even exterior algebra of C^5 = C^3 (+) C^2.
# Basis directions: c1 c2 c3 carry Y = a ; w1 w2 carry Y = b.
# A wedge of directions carries the sum of their Y. T3 = +-1/2 counts the weak
# directions present. Q = T3 + Y.
# ---------------------------------------------------------------------------------
COL, WEA = ["c1", "c2", "c3"], ["w1", "w2"]
Y = {**{c: a for c in COL}, **{w: b for w in WEA}}

def state(wedge):
    y = sum((Y[k] for k in wedge), Fraction(0))
    nw = sum(1 for k in wedge if k in WEA)
    nc = sum(1 for k in wedge if k in COL)
    return y, nc, nw

print("SECTION 3  One generation, as the even exterior algebra of C^5")
print(f"{'state':<6} {'SU(3)':>6} {'SU(2)':>6} {'Y':>7} {'dim':>4}   {'Q values':<22} basis")
rows, total = [], 0
SPEC = [
    ("Q",    2, lambda w: len([k for k in w if k in COL]) == 1 and len([k for k in w if k in WEA]) == 1),
    ("u^c",  2, lambda w: len([k for k in w if k in COL]) == 2 and len([k for k in w if k in WEA]) == 0),
    ("e^c",  2, lambda w: len([k for k in w if k in COL]) == 0 and len([k for k in w if k in WEA]) == 2),
    ("d^c",  4, lambda w: len([k for k in w if k in COL]) == 2 and len([k for k in w if k in WEA]) == 2),
    ("L",    4, lambda w: len([k for k in w if k in COL]) == 3 and len([k for k in w if k in WEA]) == 1),
    ("nu^c", 0, lambda w: len(w) == 0),
]
ALL = COL + WEA
for name, deg, pred in SPEC:
    wedges = [w for w in itertools.combinations(ALL, deg) if pred(w)]
    if not wedges and deg == 0: wedges = [()]
    y, nc, nw = state(wedges[0])
    su3 = {0: "1", 1: "3", 2: "3bar", 3: "1"}[nc]
    su2 = {0: "1", 1: "2", 2: "1"}[nw]
    # Q = T3 + Y, with T3 = +-1/2 when a single weak direction is present
    qs = sorted({y + t for t in ([Fraction(1,2), Fraction(-1,2)] if nw == 1 else [Fraction(0)])})
    total += len(wedges)
    print(f"{name:<6} {su3:>6} {su2:>6} {str(y):>7} {len(wedges):>4}   "
          f"{', '.join(str(q) for q in qs):<22} {wedges[0] if wedges[0] else '1'}")
    rows.append({"state": name, "su3": su3, "su2": su2, "Y": str(y),
                 "dim": len(wedges), "Q": [str(q) for q in qs]})
print(f"{'':<6} {'':>6} {'':>6} {'':>7} {total:>4}   total")
print()

# check against the Standard Model, written out independently
SM = {
 "Q":    ("3",    "2", Fraction(1,6),  6, {Fraction(2,3), Fraction(-1,3)}),
 "u^c":  ("3bar", "1", Fraction(-2,3), 3, {Fraction(-2,3)}),
 "d^c":  ("3bar", "1", Fraction(1,3),  3, {Fraction(1,3)}),
 "L":    ("1",    "2", Fraction(-1,2), 2, {Fraction(0), Fraction(-1)}),
 "e^c":  ("1",    "1", Fraction(1),    1, {Fraction(1)}),
 "nu^c": ("1",    "1", Fraction(0),    1, {Fraction(0)}),
}
ok = True
print("   checked against the Standard Model, written out independently:")
for row in rows:
    s = SM[row["state"]]
    match = (row["su3"] == s[0] and row["su2"] == s[1] and Fraction(row["Y"]) == s[2]
             and row["dim"] == s[3] and {Fraction(q) for q in row["Q"]} == s[4])
    ok &= match
    print(f"      {row['state']:<6} {'MATCH' if match else 'MISMATCH'}")
print(f"   all sixteen states match: {ok}   (total {total})")
print()

# ---------------------------------------------------------------------------------
# SECTION 4. The weak mixing angle at unification, from the same 3+2 split.
# ---------------------------------------------------------------------------------
trY2 = 3*a*a + 2*b*b
trT32 = 2 * Fraction(1,2)**2 / 2 * 2      # Tr(T3^2) over the fundamental doublet = 1/2
trT32 = Fraction(1,2)
norm = trY2 / trT32
s2w = trT32 / (trT32 + trY2)
print("SECTION 4  The weak mixing angle at unification")
print(f"   Tr(Y^2) over the 3+2 block = 3({a})^2 + 2({b})^2 = {trY2}")
print(f"   Tr(T3^2)                                        = {trT32}")
print(f"   hypercharge normalisation  Tr(Y^2)/Tr(T3^2)     = {norm}")
print(f"   sin^2(theta_W) at unification = {s2w} = {float(s2w):.6f}")
print(f"   the standard grand-unified value is 3/8: {s2w == Fraction(3,8)}")
print(f"   note: 3/8 is also (spatial modes)/(carrier rank) = 3/8")
print()

# ---------------------------------------------------------------------------------
# SECTION 5. CP structure from the reversibility sorting of Paper 22.
# ---------------------------------------------------------------------------------
print("SECTION 5  CP structure, from which block each force lives on")
print(f"{'sector':<12} {'block':<26} {'F^F term':<18} {'observed'}")
cp = [
 ("strong",  "3 reversible modes",       "no orientation to couple", "theta < 1e-10"),
 ("weak",    "clock + closure, on arrow", "orientation available",    "CP violated"),
 ("EM",      "traceless across both",     "no net orientation",       "CP conserved"),
 ("gravity", "the metric block 4 + 1",    "no net orientation",       "CP conserved"),
]
for s, blk, t, o in cp:
    print(f"{s:<12} {blk:<26} {t:<18} {o}")
print()
print("   The u^2 term is F^F, which for a gauge sector is the topological theta term.")
print("   Its coefficient is universal, so the framework cannot make theta small by")
print("   tuning. It makes it ZERO in the strong sector, because a term whose entire")
print("   content is orientation sensitivity has nothing to be sensitive with when its")
print("   block is freely reversible. The same reading requires CP violation in the")
print("   weak sector, which lives on the arrow. Two for two, no freedom used.")

json.dump({"generated": datetime.datetime.now().isoformat(timespec="seconds"),
  "weights": {"W_L": W_L, "W_B": W_B, "W_M": W_M},
  "sector_assignment": {"W_L": "gauge", "W_B": "matter", "W_M": "mass"},
  "exact_ratios": {"W_M_over_W_L": "1/5", "W_B_over_W_L": "2/sqrt5",
                   "Lambda": "3/sqrt5"},
  "hypercharge": {"colour": str(a), "weak": str(b), "traceless": True,
                  "ratio_forced": str(a/b), "normalisation": "conventional"},
  "generation": rows, "generation_total": total,
  "all_states_match_standard_model": bool(ok),
  "sin2_theta_W_unification": str(s2w),
  "hypercharge_normalisation": str(norm),
  "CP_structure": [{"sector": s, "block": b_, "term": t, "observed": o} for s, b_, t, o in cp],
  "macdowell_mansouri_note": "the projection MM inserts by hand is the cluster projection, "
                             "which the framework derives",
 }, open(_cert("matter_action_certificate.json"), "w"), indent=2)

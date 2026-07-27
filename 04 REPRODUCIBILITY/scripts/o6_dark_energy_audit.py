"""O6 extended: the deed audit applied to the dark-energy comparison.

Paper 19's rule is stated and must be obeyed in this order: count the whole-body
closures each pipeline performs, DECLARE the difference, and only then consult the gap.
The counts below are read off pipeline architecture, not off the discrepancy.

    CMB       light forms in the plasma, is released through the last-scattering
              face, is carried across the whole structure era, and is closed through
              a model engine that converts spectra into parameters.   3 closures.

    BAO       a ruler fixed at the drag epoch, then read locally in matter tracers.
              The formation closure is inherited; no transmission through the
              structure era and no model-engine closure.              1 closure.

    SNe Ia    parallax to Cepheid to supernova, calibration against calibration.
              Local reads throughout, no whole-body traversal.        0 closures.

Each closure retains 1 - r^3, so a difference of n closures prices at (1-r^3)^n.

The framework's claim is NOT that w departs from -1. It is that w = -1 holds inside
any single-deed pipeline, and that summing deeds of different closure count forces an
apparent evolution that is present in none of them separately. The observable signature
is that the significance tracks WHICH pipelines were summed rather than converging.
"""
import math, json, os, datetime

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
def _cert(n): return os.path.join(_ROOT, "certificates", n)

phi = (1 + math.sqrt(5)) / 2
r   = 1 / (2 * phi)
r3  = r ** 3
keep = 1 - r3

DECLARED = {"CMB": 3, "BAO": 1, "SNe Ia": 0}

print("Declared closure counts, from architecture, before consulting any gap")
for k, v in DECLARED.items():
    print(f"   {k:<8} {v} whole-body closure(s)")
print(f"\n   retained per closure  1 - r^3 = {keep:.9f}")
print()
print("Priced deed differences between pipeline pairs")
print(f"{'pair':<18} {'dn':>3} {'(1-r^3)^dn':>12} {'gap':>9}")
pairs = []
for a in DECLARED:
    for b in DECLARED:
        if a >= b: continue
        dn = abs(DECLARED[a] - DECLARED[b])
        if dn == 0: continue
        f = keep ** dn
        print(f"{a+' vs '+b:<18} {dn:>3} {f:>12.9f} {100*(1-f):>8.3f}%")
        pairs.append({"pair": f"{a} vs {b}", "delta_closures": dn,
                      "retained": f, "gap_percent": 100*(1-f)})
print()

# --- the observed significances, as published ---------------------------------------
OBS = [
    ("DESI DR2 BAO alone",              None,  "consistent with w = -1"),
    ("DESI + CMB",                      3.1,   "BAO(1) summed with CMB(3), dn = 2"),
    ("DESI + CMB + Pantheon+",          2.8,   "three deeds summed"),
    ("DESI + CMB + Union3",             3.8,   "three deeds summed, different SN pipeline"),
    ("DESI + CMB + DESY5",              4.2,   "three deeds summed, different SN pipeline"),
]
print("Published significance for evolving dark energy, by combination")
print(f"{'combination':<28} {'sigma':>6}   note")
for name, s, note in OBS:
    print(f"{name:<28} {('%.1f' % s) if s else '  -  ':>6}   {note}")

sn = [s for _, s, _ in OBS if s]
print()
print(f"   single-deed pipeline (BAO alone)        : no preference for evolution")
print(f"   combined-deed fits                      : {min(sn):.1f} to {max(sn):.1f} sigma")
print(f"   spread across SN pipelines at fixed data: {max(sn)-min(sn):.1f} sigma")
print()
print("   The three-deed fits differ from one another by more than one and a half sigma")
print("   while using the same BAO and the same CMB. Only the supernova pipeline changed.")
print("   A physically evolving w cannot care which photon pipeline is attached to it.")
print("   A deed-price difference must.")
print()
print("VERDICT, stated as a test rather than a result:")
print("   Consistent with the framework's reading. NOT confirmation: the mapping from a")
print("   priced deed difference onto w0 and wa is not derived here and remains OPEN.")
print("   The framework dies if a single-deed pipeline alone returns w != -1 at high")
print("   significance, since no combination artifact would then be available.")

json.dump({"generated": datetime.datetime.now().isoformat(timespec="seconds"),
           "declared_closure_counts": DECLARED,
           "declared_before_consulting_gap": True,
           "retained_per_closure": keep,
           "priced_pairs": pairs,
           "published_significances": [{"combination": n, "sigma": s, "note": t} for n, s, t in OBS],
           "single_deed_BAO_alone": "consistent with w = -1",
           "spread_across_SN_pipelines_sigma": max(sn) - min(sn),
           "status": "consistent with the framework's reading; the map from priced deed "
                     "difference to w0 and wa is OPEN and is not claimed",
           "falsifier": "a single-deed pipeline alone returning w != -1 at high significance"},
          open(_cert("o6_dark_energy_certificate.json"), "w"), indent=2)

"""Applications 04 — balanced-turnover bridge test, adult mouse subgranular zone (16 July 2026).

FROZEN mapping (mitotic vs post-mitotic, declared before counts):
  A = mitotic precursors (Ki67+);  B = post-mitotic committed neuroblasts (DCX+, Ki67-);
  x = A/(A+B). Bridge: x=r=0.309, committed:mitotic = (1-r)/r = sqrt5 = 2.236. Rule: |x-r|<=r^3.
REAL DATUM: DCX+ (type 2b/3) ~ 4x Ki67+ per GCL-SGZ volume (adult mouse SGZ stereology).
RESULT: frozen mitotic cut x=0.20 -> FAIL (|x-r|=0.11). Straddles r across defensible cuts
  (fate cut 0.09; overlap-corrected 0.30 IN band). Deciding quantity = Ki67+/DCX+ overlap, unmeasured.
VERDICT: frozen-cut fail, mapping-limited; one triple-stain stereological count (Ki67/DCX/stem)
  in young-adult DG resolves it. Run: python sgz_balanced_turnover_test.py
"""

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
def _d(*p): return _os.path.join(_ROOT, "data", *p)
def _r(*p): return _os.path.join(_ROOT, "results", *p)
def _f(*p): return _os.path.join(_ROOT, "figures", *p)
import math


r=(math.sqrt(5)-1)/4; CEIL=r**3
cuts={"mitotic (frozen)":1/(1+4.0),
      "overlap-corrected":(1+0.5)/(1+0.5+3.5),
      "fate (uncommitted only)":0.4/(0.4+4.0)}
print(f"r={r:.4f}  band=[{r-CEIL:.3f},{r+CEIL:.3f}]  predicted committed:mitotic=sqrt5={(1-r)/r:.3f}")
for k,x in cuts.items():
    print(f"  {k:22s}: x={x:.3f}  ratio={(1-x)/x:.2f}:1  {'PASS' if abs(x-r)<=CEIL else 'FAIL'} (|x-r|={abs(x-r):.3f})")

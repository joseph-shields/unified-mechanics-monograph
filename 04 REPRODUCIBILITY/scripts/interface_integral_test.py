"""Volume 10 reproducibility — candidate interface coefficients vs SPARC (16 July 2026).

a = kappa * c * H0 * dB, with dB = sqrt(5)*phi^2/2 - sqrt(8) and the framework's
internal clock H0 = 67.3617174547 km/s/Mpc (Volume 05 sec 12.2).
Candidates: kappa in {1, 3/2, sqrt(3), 3}. Verdict on 2,696 SPARC points:
  kappa=1     rms 0.1577  bias +0.079  (excluded)
  kappa=3/2   rms 0.1349  bias +0.021  (disfavoured)
  kappa=sqrt3 rms 0.1327  bias -0.001  (equal to free fit, zero parameters)
  kappa=3     rms 0.1588  bias -0.079  (excluded)
Requires: data/ folder with SPARC .mrt files (see 'SPARC data' directory here).
"""

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
def _d(*p): return _os.path.join(_ROOT, "data", *p)
def _r(*p): return _os.path.join(_ROOT, "results", *p)
def _f(*p): return _os.path.join(_ROOT, "figures", *p)
import numpy as np, math, json
from scipy.optimize import minimize_scalar



KPC = 3.0856775814913673e19; KMS = 1e3; C = 2.99792458e8
dB = -2*math.sqrt(2) + 5/4 + 3*math.sqrt(5)/4
H_UM = 67.3617174547
A = C*(H_UM*KMS/(KPC*1e3))*dB

gal = {}
for l in open(_d("SPARC", "SPARC_Lelli2016c.mrt")):
    parts = l.split()
    if len(parts) >= 18 and parts[0][0].isalnum():
        try: gal[parts[0]] = (float(parts[5]), int(parts[17]))
        except ValueError: pass
g_obs, g_bar = [], []
dash = 0
for l in open(_d("SPARC", "MassModels_Lelli2016c.mrt")):
    if set(l.strip()) == {"-"}: dash += 1; continue
    if dash < 2 or not l.strip(): continue
    ID = l[0:11].strip()
    try:
        D,R,Vobs,eV,Vgas,Vdisk,Vbul = (float(x) for x in (l[12:18],l[19:25],l[26:32],l[33:38],l[39:45],l[46:52],l[53:59]))
    except ValueError: continue
    if ID not in gal: continue
    inc, Q = gal[ID]
    if Q == 3 or inc < 30 or Vobs <= 0 or eV/Vobs >= 0.10: continue
    v2 = Vgas*abs(Vgas) + 0.5*Vdisk*abs(Vdisk) + 0.7*Vbul*abs(Vbul)
    if v2 <= 0: continue
    g_obs.append((Vobs*KMS)**2/(R*KPC)); g_bar.append(v2*KMS**2/(R*KPC))
g_obs = np.array(g_obs); g_bar = np.array(g_bar); lgo = np.log10(g_obs)
def um(gb, a): return (gb + np.sqrt(gb**2 + 4*a*gb))/2
def rms(a): return float(np.sqrt(np.mean((lgo - np.log10(um(g_bar,a)))**2)))
def bias(a): return float(np.median(lgo - np.log10(um(g_bar,a))))
print(f"n = {len(g_obs)};  a* = cH0dB = {A:.4e}")
for k, name in [(1,"1"),(1.5,"3/2"),(math.sqrt(3),"sqrt3"),(3,"3")]:
    print(f"kappa={name:>5}: a={k*A:.4e}  rms={rms(k*A):.4f}  bias={bias(k*A):+.4f}")
r = minimize_scalar(lambda la: rms(10**la), bounds=(-11,-9), method="bounded")
print(f"free fit: a={10**r.x:.4e}  rms={rms(10**r.x):.4f}")

# Every frozen output must have a generator in the release. This writes the one this
# script is responsible for. The estimator is named in the file so it can never again
# stand for two different things.
_out = {
    "estimator": "unweighted rms in log10 g, minimised over a",
    "n": int(len(g_obs)),
    "H0_internal_km_s_Mpc": H_UM,
    "a_star_internal": A,
    "candidates": {name: {"kappa": float(k), "a": float(k*A),
                          "rms_dex": rms(k*A), "median_bias_dex": bias(k*A)}
                   for k, name in [(1,"1"),(1.5,"3/2"),(math.sqrt(3),"sqrt3"),(3,"3")]},
    "a_free": float(10**r.x),
    "rms_free_dex": rms(10**r.x),
}
json.dump(_out, open(_r("interface_results.json"), "w"), indent=2)
print("wrote", _r("interface_results.json"))

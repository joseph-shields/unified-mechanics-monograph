"""Applications 03 — bridge extraction on real cortical neurogenesis data (16 July 2026).

Data: Takahashi, Nowakowski & Caviness (J Neurosci 1996), murine neocortex.
  leaving fraction Q per embryonic day (Table 3) + cell-cycle length Tc (Table 2), E11-E17.
Mapping (FROZEN): currency=cells; progenitor A (retained) vs neuron B (terminal);
  per cycle A->2(1-Q)A, B->B+2Q A; x=A/(A+B); chi=[Q/(1-Q)]/x; beta=0.
Bridge: chi=1+4x, fixed point x=r, chi=sqrt5. Screen: |chi-sqrt5|<=r^3 at the x=r crossing.
RESULT: x=r at E15.4, chi=sqrt5 at E14.7 (0.7 days apart) -> FAIL; trajectory grazes the
bridge line at x=0.44 (E14.9). DIAGNOSIS: cortex ramps Q (sweep, not plateau); the fixed
point is never occupied. Next test: balanced-turnover neurogenesis (standing progenitor:neuron
ratio = r). Run: python dev_neurogenesis_test.py
"""
import numpy as np, math
r=(math.sqrt(5)-1)/4; CEIL=r**3; CHI=1+4*r
E_Q=[(11,0.08),(12,0.11),(13,0.19),(14,0.34),(15,0.59),(16,0.54),(17,0.90)]
E_Tc=[(11,9.0),(12,10.2),(13,11.4),(14,15.1),(15,17.5),(16,18.4),(17,18.4)]
Ed=np.array([e for e,_ in E_Q]); Qd=np.array([q for _,q in E_Q]); Td=np.array([t for _,t in E_Tc])
Qf=lambda e:float(np.interp(e,Ed,Qd)); Tf=lambda e:float(np.interp(e,Ed,Td))
E,A,B,tr=11.0,1.0,0.0,[]
while E<17.0:
    Q=min(max(Qf(E),1e-4),0.999); x=A/(A+B); chi=(Q/(1-Q))/x
    tr.append((E,Q,x,chi)); A,B=2*(1-Q)*A,B+2*Q*A; E+=Tf(E)/24.0
tr=np.array(tr); Ea,Qa,xa,ca=tr.T
cross=lambda y,t:next((Ea[i]+ (t-y[i])/(y[i+1]-y[i])*(Ea[i+1]-Ea[i]) for i in range(len(y)-1) if (y[i]-t)*(y[i+1]-t)<=0 and y[i]!=y[i+1]),None)
Ex,Ech=cross(xa,r),cross(ca,CHI); chi_xr=float(np.interp(Ex,Ea,ca))
print(f"x=r at E{Ex:.2f}; chi=sqrt5 at E{Ech:.2f}; separation {abs(Ex-Ech):.2f} days")
print(f"chi at x=r = {chi_xr:.2f} vs sqrt5={CHI:.2f}; |Δ|={abs(chi_xr-CHI):.2f} ceiling r^3={CEIL:.4f}")
print("VERDICT:", "PASS" if abs(chi_xr-CHI)<=CEIL else "FAIL")

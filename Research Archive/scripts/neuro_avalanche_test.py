"""Applications 02 — preregistered blind test of the interface bridge on a
self-organising branching network (16 July 2026).

FROZEN before measurement: pass iff branching ratio self-organises to sigma~1 AND
|chi - sqrt5| <= r^3 = 0.0295, with chi = K/(P x), x = Q/(Q+R).
RESULT: sigma -> 0.95 (self-organised), but x -> 0.994, chi -> 1.006 -> DECISIVE FAIL.
DIAGNOSIS: wrong Whole. The stationary sparse-avalanche regime is degenerate
(chi->1 is just sigma->1 restated). The bridge's sqrt5 requires an accumulating
processing history (development / learning / a single sustained cascade), not an
instantaneous state fraction of a recycling steady state.
Run: python neuro_avalanche_test.py
"""
import numpy as np, math, json
rng = np.random.default_rng(20260716)
r=(math.sqrt(5)-1)/4; CEIL=r**3; CHI=1+4*r
N,STEPS,WARM,refrac,sigma0,u,tau,drive = 4000,90000,30000,1,2.6,0.06,5000.0,1.2
state=np.zeros(N,np.int32); omega=1.0; fired=np.zeros(N,bool)
acc={k:0.0 for k in ("Q","R","K","P","anc","desc")}; n=0
for t in range(STEPS):
    quies=state==0; Q=int(quies.sum()); R=N-Q; nf=int(fired.sum())
    lam=sigma0*omega*nf
    k=min(Q,rng.poisson(lam)) if (Q>0 and lam>0) else 0
    newfire=np.zeros(N,bool)
    if k>0: newfire[rng.choice(np.flatnonzero(quies),size=k,replace=False)]=True
    nsp=rng.poisson(drive); driven=0
    if nsp>0:
        qi=np.flatnonzero(quies&~newfire)
        if len(qi)>0:
            s=rng.choice(qi,size=min(nsp,len(qi)),replace=False); newfire[s]=True; driven=len(s)
    nfire=int(newfire.sum()); primed=int(((state==1)&~newfire).sum())
    state[(state>0)&~newfire]-=1; state[newfire]=refrac
    omega+=(1-omega)/tau-u*omega*(nfire/N); omega=min(max(omega,1e-6),1.0); fired=newfire
    if t>=WARM:
        acc["Q"]+=Q;acc["R"]+=R;acc["K"]+=nfire;acc["P"]+=primed;acc["anc"]+=nf;acc["desc"]+=(nfire-driven);n+=1
x=(acc["Q"]/n)/((acc["Q"]/n)+(acc["R"]/n)); chi=(acc["K"]/acc["P"])/x; sig=acc["desc"]/max(acc["anc"],1)
print(f"sigma={sig:.3f}  x={x:.3f}  chi={chi:.3f}  target sqrt5={CHI:.3f}  ceiling r^3={CEIL:.4f}")
print("VERDICT:", "PASS" if abs(chi-CHI)<=CEIL else "FAIL", f"(|chi-sqrt5|={abs(chi-CHI):.2f})")

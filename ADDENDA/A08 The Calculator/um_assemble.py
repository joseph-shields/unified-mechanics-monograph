"""THE ASSEMBLY. Helix tip against colour edge, mapped by Personal Relativity.

  COLOUR  the graph: mean hue is its COLOUR, the spread of the hue distribution is
          its TEMPERATURE. A pure channel has zero spread, so it is cold.
  HELIX   the tip: the realisation turn count T is its POSITION.
  PR      the map: resolution is position over spread, which is exactly q/dq.
          N = 360 T / spread_deg, since a full turn is the whole wheel.
          Zero spread gives infinite resolution and therefore no correction.

Run:  PYTHONUTF8=1 python um_assemble.py
"""
import json, math, os, random, statistics, datetime
import sympy as sp
import numpy as np

HERE=os.path.dirname(os.path.abspath(__file__))
S5=sp.sqrt(5); PHI=(1+S5)/2; PHIF=float(PHI); R=1/(2*PHI); RF=float(R); UF=1-RF; R3F=RF**3
su,sm=sp.symbols("u m",positive=True); SUB={su:1-R,sm:R}; LN=math.log(PHIF)
HL,HM,HB=20.0,200.0,110.0

def norm5(x): return sp.simplify(sp.expand(x*x.subs(S5,-S5)))
def hmul(x,y):
    p=sp.expand(x*y); return sp.radsimp(sp.simplify(p/sp.sqrt(sp.Abs(norm5(p)))))
def H5(N):
    if math.isinf(N): return 1.0
    s=N/(N+1.0); t=s**10; return 2*t/(1+t)
def hue_at(f,x):
    u,m=1.0-x,x; v=f(u,m)
    if v==0: return HM
    h=1e-7
    sL=u*(f(u+h,m)-f(u-h,m))/(2*h)/v; sM=m*(f(u,m+h)-f(u,m-h))/(2*h)/v
    aL,aM=abs(sL),abs(sM)
    cx=2*math.sqrt(aL*aM)/(aL+aM) if (aL>0 and aM>0) else 0.0
    w=[u*u*aL,m*m*aM,2*u*m*cx]
    z=sum(wi*complex(math.cos(math.radians(hh)),math.sin(math.radians(hh))) for hh,wi in zip([HL,HM,HB],w))
    return math.degrees(math.atan2(z.imag,z.real))%360.0 if abs(z)>1e-15 else HM
def evolve(n=60000,burn=2000,seed=11):
    rng=random.Random(seed); x=0.5; out=[]; sc=R3F*math.sqrt(3.0)
    for i in range(n+burn):
        x=1.0/(4.0*x+2.0)+sc*rng.uniform(-1.0,1.0)
        if i>=burn: out.append(x)
    return out
XS=evolve()
def turns(x0,maxit=12):
    x=sp.nsimplify(x0); prev=float(x); lock=[]
    for k in range(1,maxit+1):
        x=hmul(x,PHI); v=float(x); r=v/prev; prev=v
        lock.append(abs(r-PHIF)<1e-12)
        if len(lock)>=2 and lock[-1] and lock[-2]: return k-1
    return None

SUITE=[("Omega_b",lambda u,m:m*m/2,sm**2/2,0.0493017,0.0007),
       ("Omega_c",lambda u,m:4*m*m*u,4*sm**2*su,0.2645,0.0026),
       ("Omega_DE",lambda u,m:1-m*m/2-4*m*m*u,1-sm**2/2-4*sm**2*su,0.6847,0.0073),
       ("Y_He",lambda u,m:u*u/2,su**2/2,0.245,0.003),
       ("N_eff",lambda u,m:3+m*m/2,3+sm**2/2,3.044,0.010),
       ("n_s",lambda u,m:1-m*m+2*m**3,1-sm**2+2*sm**3,0.9649,0.0042),
       ("tau",lambda u,m:2*m**3*(1-R3F)**3,2*sm**3*(1-R3F)**3,0.0544,0.0073)]

print("THE ASSEMBLY");print("="*104)
print("%-10s %8s %8s %5s %11s %13s %13s %9s %8s"
      % ("observable","colour","temp","pos","resolution","colour value","ASSEMBLED","measured","pull"))
rows=[]
for k,fn,expr,meas,sig in SUITE:
    hs=np.array([hue_at(fn,x) for x in XS[::29]])
    hue=float(np.mean(hs)); temp=float(np.std(hs))
    val=statistics.fmean(fn(1-x,x) for x in XS)
    T=turns(sp.nsimplify(sp.simplify(sp.sympify(expr).subs(SUB))))
    N=float("inf") if temp<1e-9 else 360.0*T/temp
    asm=val/H5(N)
    rows.append(dict(key=k,colour=hue,temperature=temp,position=T,resolution=N,
                     colour_value=val,assembled=asm,measured=meas,sigma=sig,
                     pull=(asm-meas)/sig,resid=100*(asm/meas-1)))
    print("%-10s %8.2f %8.4f %5s %11s %13.8f %13.8f %9.6f %+8.2f"
          % (k,hue,temp,str(T),"exact" if math.isinf(N) else "%.1f"%N,val,asm,meas,(asm-meas)/sig))
print()
print("mean |pull| assembled: %.3f" % statistics.fmean(abs(d["pull"]) for d in rows))
print("cold (pure channel, no correction): %s"
      % ", ".join(d["key"] for d in rows if math.isinf(d["resolution"])))
print("warm (mixed, corrected):            %s"
      % ", ".join(d["key"] for d in rows if not math.isinf(d["resolution"])))
json.dump({"generated":datetime.datetime.now().isoformat(timespec="seconds"),"rows":rows},
          open(os.path.join(HERE,"um_assemble_results.json"),"w"),indent=2)

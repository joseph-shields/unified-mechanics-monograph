#!/usr/bin/env python3
"""Universal Field of Least Action: compression-boundary closure audit.

This script formalizes exactly what the Bubble Field can recover from its compressed
variables, what requires a constitutive key, what is only a dimensional translation,
and what is outside the representation. It also closes the smallest least-action
constitutive branch for alpha_L/alpha_M as a conditional theorem.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parent   # was hardcoded to the build machine
OLD = json.loads((ROOT / 'bubble_field_closure_attack_results.json').read_text())
OUT_JSON = ROOT / 'bubble_field_compression_boundary_results.json'
FIG_MAP = ROOT / 'bubble_field_compression_boundary_map.png'
FIG_LEDGER = ROOT / 'bubble_field_recovery_ledger.png'

# Exact framework constants
PHI = (1.0 + math.sqrt(5.0)) / 2.0
R = 1.0 / (2.0 * PHI)
U = 1.0 - R
W_L, W_B, W_M = U * U, 2.0 * U * R, R * R
EPS = R**3
S = 1.0 - EPS
KAPPA = R / U

# -----------------------------------------------------------------------------
# 1. Exact local compression map and its kernel
# q = (alpha_M, alpha_L, nu, theta)
# y = (A, B, Theta) = (-alpha_M, alpha_L + nu/3, theta)
# -----------------------------------------------------------------------------
Cmat = sp.Matrix([
    [-1, 0, 0, 0],
    [ 0, 1, sp.Rational(1, 3), 0],
    [ 0, 0, 0, 1],
])
rank = int(Cmat.rank())
nullspace = Cmat.nullspace()
null_vector = [sp.simplify(v) for v in nullspace[0]]

# Recoverability test for representative linear targets.
target_gradients = {
    'alpha_M': sp.Matrix([1, 0, 0, 0]),
    'alpha_L': sp.Matrix([0, 1, 0, 0]),
    'nu': sp.Matrix([0, 0, 1, 0]),
    'theta': sp.Matrix([0, 0, 0, 1]),
    'A=-alpha_M': sp.Matrix([-1, 0, 0, 0]),
    'B=alpha_L+nu/3': sp.Matrix([0, 1, sp.Rational(1, 3), 0]),
    'hidden_split=alpha_L-nu/3': sp.Matrix([0, 1, -sp.Rational(1, 3), 0]),
}
recoverability = {}
for name, grad in target_gradients.items():
    directional = sp.simplify((grad.T * nullspace[0])[0])
    recoverability[name] = {
        'gradient_dot_kernel': str(directional),
        'recoverable_from_compression': bool(directional == 0),
    }

# -----------------------------------------------------------------------------
# 2. Conditional constitutive closure from a least-norm boundary response
# S_resp = 1/2(aL^2+aM^2) - lambda(r aL + u aM - chi)
# -----------------------------------------------------------------------------
aL, aM, lam, chi = sp.symbols('alpha_L alpha_M lambda chi', real=True)
r_sym, u_sym = sp.symbols('r u', positive=True)
S_resp = sp.Rational(1, 2) * (aL**2 + aM**2) - lam * (r_sym*aL + u_sym*aM - chi)
sol = sp.solve([
    sp.diff(S_resp, aL),
    sp.diff(S_resp, aM),
    sp.diff(S_resp, lam),
], [aL, aM, lam], dict=True)[0]
ratio_symbolic = sp.simplify(sol[aL] / sol[aM])
weak_nu_over_alphaM = 3.0 * (1.0 - KAPPA)

# -----------------------------------------------------------------------------
# 3. Freeze the G bridge and distinguish derivation status from evidence status
# -----------------------------------------------------------------------------
G_bridge = OLD['G_bridge']
q_uf = G_bridge['q_models']['r^241 (1-r^3)^2']
base = G_bridge['cosmological_boundaries']['uploaded_planck_chain']
G_pred = base['G_candidate_SI']
G_rel = base['relative_to_CODATA']

# -----------------------------------------------------------------------------
# 4. Exact structural scale versus calibrated low-energy matching
# -----------------------------------------------------------------------------
scales = OLD['scales_reproducibility_branch']
E_cross_GeV = scales['UV_IR_bridge_energy_eV'] / 1e9
v_ref = OLD['weak_scale']['reference_GeV']
matching_coeff_observed = v_ref / E_cross_GeV
matching_coeff_old_candidate = (W_M / 2.0) * math.sqrt(S)

# -----------------------------------------------------------------------------
# 5. Claim ledger: exact threshold, not rhetorical grading
# -----------------------------------------------------------------------------
claims = [
    {
        'claim': 'Golden fixed point, channel weights, traversal floor',
        'compression_status': 'INTERNAL INVARIANT',
        'evidence_status': 'RESULT',
        'closure': 'Exact algebra once the physical golden realization is admitted.',
    },
    {
        'claim': 'Cell scale a0(W)=(W hbar c/rho_Lambda)^(1/4)',
        'compression_status': 'DIMENSIONAL OUTPUT',
        'evidence_status': 'CONDITIONAL RESULT',
        'closure': 'Exact family; the branch W=1 or W=W_M is a declared vacuum-channel assignment.',
    },
    {
        'claim': 'w=-1',
        'compression_status': 'MACRO INVARIANT',
        'evidence_status': 'CONDITIONAL RESULT',
        'closure': 'Follows exactly from the continuity equation if cell renewal keeps rho_Lambda constant during expansion.',
    },
    {
        'claim': 'Metric/source sector in A and B',
        'compression_status': 'COMPRESSED FIELD',
        'evidence_status': 'EXACT REPRESENTATION',
        'closure': 'GR determines A and B; all metric observables factor through them.',
    },
    {
        'claim': 'Separate alpha_L and nu',
        'compression_status': 'KERNEL DEGREE',
        'evidence_status': 'NOT IDENTIFIABLE FROM METRIC',
        'closure': 'Requires a nonmetric observation or a constitutive section.',
    },
    {
        'claim': 'alpha_L/alpha_M = r/u = 1/sqrt(5)',
        'compression_status': 'CONSTITUTIVE SECTION',
        'evidence_status': 'CONDITIONAL THEOREM',
        'closure': 'Forced by least Euclidean response cost under the mixed-boundary constraint r alpha_L + u alpha_M = chi.',
    },
    {
        'claim': 'Schwarzschild, interior star, factor-two lensing',
        'compression_status': 'COMPRESSED FIELD',
        'evidence_status': 'EXACT GR RECONSTRUCTION',
        'closure': 'Exact in the spherical scalar sector; not an independent derivation of GR from cell microdynamics.',
    },
    {
        'claim': 'G from q=r^241(1-r^3)^2',
        'compression_status': 'DISCRETE BRIDGE',
        'evidence_status': 'POSTDICTIVE CONDITIONAL FORECAST',
        'closure': 'Conditional theorem under 240-mode factorization, one readout, and two retained interrogative legs; frozen for future Lambda tests.',
    },
    {
        'claim': 'UV/IR scale E_cross=sqrt(E_P E_0)',
        'compression_status': 'STRUCTURAL SCALE',
        'evidence_status': 'RESULT/IDENTITY',
        'closure': 'Exact energy form of a0=sqrt(l_P L_Lambda) after the G bridge is supplied.',
    },
    {
        'claim': 'Electroweak VEV 246 GeV',
        'compression_status': 'LOW-ENERGY MATCHING',
        'evidence_status': 'CALIBRATION, NOT DERIVATION',
        'closure': 'The field outputs E_cross; the coefficient v/E_cross is a matching datum until a symmetry-breaking operator fixes it.',
    },
    {
        'claim': 'Charged-lepton masses',
        'compression_status': 'ERASED SPECTRAL DETAIL',
        'evidence_status': 'PREVIOUS ANSATZ REJECTED',
        'closure': 'Exact masses require a Yukawa/mass operator; the prior e, mu, tau formulas are withdrawn.',
    },
    {
        'claim': 'QCD string tension',
        'compression_status': 'DIMENSIONAL TRANSLATOR',
        'evidence_status': 'IDENTITY, NOT PREDICTION',
        'closure': 'sigma=E^2/(hbar c) converts a supplied tension to a supplied local scale; it does not select the QCD scale.',
    },
    {
        'claim': 'Vacuum crowding energy as dark matter',
        'compression_status': 'CLAIMED MACRO OUTPUT',
        'evidence_status': 'EXCLUDED',
        'closure': 'Short by about 11 orders in the existing audit; geometric crowding is not the same claim as extra energy density.',
    },
    {
        'claim': 'Range hierarchy',
        'compression_status': 'OPERATOR CLASS',
        'evidence_status': 'CONDITIONAL RESULT',
        'closure': 'Green-function ranges follow exactly after kinetic/mass operator assignments; channel weights alone do not force those assignments.',
    },
]

# Formal gates used to classify future claims.
gates = {
    'fiber_gate': 'Q must be constant on every fiber C^{-1}(y); locally, dQ annihilates ker(DC).',
    'anchor_gate': 'The dimensional units of Q must be generated by declared measured anchors, with their provenance retained.',
    'bridge_gate': 'Every constitutive section or representation operator must be declared explicitly and used consistently.',
    'history_gate': 'A formula chosen after viewing the target is postdictive until frozen against new data.',
    'precision_gate': 'A quantity inside the declared output space that misses a precision observation is falsified; compression is not an escape clause.',
}

certificate = {
    'framework': 'Universal Field of Least Action / Bubble Field compression-boundary edition',
    'compression_map': {
        'domain': '(alpha_M, alpha_L, nu, theta)',
        'codomain': '(A, B, Theta)',
        'formula': '(A,B,Theta)=(-alpha_M, alpha_L+nu/3, theta)',
        'matrix': [[str(x) for x in row] for row in Cmat.tolist()],
        'rank': rank,
        'nullity': 4-rank,
        'kernel_basis': [str(x) for x in null_vector],
        'kernel_transformation': 'alpha_L -> alpha_L + delta; nu -> nu - 3 delta',
        'factorization_theorem': 'Q is recoverable iff Q=Q_tilde o C, equivalently Q is constant on compression fibers.',
        'recoverability_examples': recoverability,
    },
    'constitutive_closure': {
        'action': 'S_resp=1/2(alpha_L^2+alpha_M^2)-lambda(r alpha_L+u alpha_M-chi)',
        'stationary_solution': {str(k): str(v) for k,v in sol.items()},
        'ratio_symbolic': str(ratio_symbolic),
        'ratio_numeric': KAPPA,
        'weak_field_nu_over_alphaM_on_GR_branch': weak_nu_over_alphaM,
        'status': 'conditional theorem under the declared least-cost response metric and mixed-boundary constraint',
    },
    'G_bridge': {
        'formula': 'q=r^241(1-r^3)^2; G=8 pi c^3 q/(hbar Lambda)',
        'q': q_uf,
        'G_candidate_SI': G_pred,
        'relative_to_CODATA_on_uploaded_boundary': G_rel,
        'derivational_status': 'conditional theorem under registered representation postulates',
        'evidential_status': 'postdiction now frozen as a future Lambda forecast',
    },
    'scale_boundary': {
        'E_cross_GeV': E_cross_GeV,
        'observed_EW_matching_coefficient': matching_coeff_observed,
        'old_candidate_matching_coefficient': matching_coeff_old_candidate,
        'field_output_stops_at': 'E_cross unless a symmetry-breaking matching operator is supplied',
    },
    'gates': gates,
    'claim_ledger': claims,
}
OUT_JSON.write_text(json.dumps(certificate, indent=2))

# -----------------------------------------------------------------------------
# Figure 1: compression map, exact kernel, and constitutive section
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 7.2))
ax.set_xlim(0, 12)
ax.set_ylim(0, 7.2)
ax.axis('off')

def box(x, y, w, h, title, body, fc):
    p = FancyBboxPatch((x,y), w,h, boxstyle='round,pad=0.04,rounding_size=0.12',
                       linewidth=1.2, facecolor=fc, edgecolor='0.25')
    ax.add_patch(p)
    ax.text(x+w/2, y+h-0.35, title, ha='center', va='top', fontsize=12, weight='bold')
    ax.text(x+0.18, y+h-0.78, body, ha='left', va='top', fontsize=9.5, linespacing=1.35)

def arrow(x1,y1,x2,y2,label=''):
    a=FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=16,linewidth=1.4,color='0.25')
    ax.add_patch(a)
    if label:
        ax.text((x1+x2)/2,(y1+y2)/2+0.18,label,ha='center',fontsize=9,weight='bold')

box(0.4, 3.75, 3.0, 2.6, 'Full local cell state',
    r'$q=(\alpha_M,\alpha_L,\nu,\theta)$'+'\n\nclock, light barrier,\nnumber density, phase', '#eef4fa')
box(4.45, 3.75, 3.1, 2.6, 'Compressed field',
    r'$A=-\alpha_M$'+'\n'+r'$B=\alpha_L+\nu/3$'+'\n'+r'$\Theta=\theta$'+'\n\nrank 3, nullity 1', '#eff8f1')
box(8.6, 3.75, 3.0, 2.6, 'Observable/toolkit layer',
    'metric, curvature,\nclocks, lensing, orbits,\nradiative phase, source map', '#fff7e8')
arrow(3.4,5.05,4.45,5.05,'compression C')
arrow(7.55,5.05,8.6,5.05,'GR / field readout')

box(0.8, 0.45, 4.4, 2.1, 'Exact information lost by compression',
    r'$(0,1,-3,0)$'+'\n'+r'$\alpha_L\to\alpha_L+\delta$'+'\n'+r'$\nu\to\nu-3\delta$'+'\n\nThe metric is unchanged.', '#fff2f2')
box(6.45, 0.45, 4.7, 2.1, 'Constitutive key (conditional section)',
    r'$S_{resp}=\frac{1}{2}(\alpha_L^2+\alpha_M^2)$'+'\n'+r'$r\alpha_L+u\alpha_M=\chi$'+'\n'+r'$\Rightarrow\ \alpha_L/\alpha_M=r/u=1/\sqrt{5}$', '#f2f4f7')
arrow(5.2,1.5,6.45,1.5,'least-action key')
ax.text(6, 6.9, 'THE EXACT COMPRESSION BOUNDARY', ha='center', fontsize=17, weight='bold')
ax.text(6, 6.56, 'The field recovers everything invariant on the fibers - and nothing inside the hidden split without a key.',
        ha='center', fontsize=10.5)
fig.tight_layout()
fig.savefig(FIG_MAP, dpi=220, bbox_inches='tight')
plt.close(fig)

# -----------------------------------------------------------------------------
# Figure 2: compact recovery ledger
# -----------------------------------------------------------------------------
labels = [
    'Metric/source', 'Schwarzschild/star', 'Cell scale', 'w=-1', 'G bridge',
    'UV/IR scale', 'alpha split', 'EW VEV', 'Lepton masses', 'QCD tension', 'DM energy'
]
levels = [5,5,4,4,3,5,3,2,0,1,0]
level_names = {
    5:'exact/result', 4:'conditional result', 3:'frozen conditional bridge',
    2:'calibration', 1:'translator only', 0:'outside/rejected'
}
fig, ax = plt.subplots(figsize=(11.5, 6.2))
y = np.arange(len(labels))
ax.barh(y, levels)
ax.set_yticks(y, labels)
ax.set_xlim(0,5.25)
ax.set_xticks(range(6), [level_names[i] for i in range(6)], rotation=22, ha='right')
ax.invert_yaxis()
ax.set_title('Universal Field of Least Action - recovery threshold ledger', weight='bold')
ax.set_xlabel('Epistemic closure level (not numerical accuracy)')
for yi, lv in zip(y, levels):
    ax.text(lv+0.06, yi, level_names[lv], va='center', fontsize=8.8)
fig.tight_layout()
fig.savefig(FIG_LEDGER, dpi=220, bbox_inches='tight')
plt.close(fig)

print(OUT_JSON)
print(FIG_MAP)
print(FIG_LEDGER)

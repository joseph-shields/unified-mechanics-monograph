# Helical Relativity

## Standing account, and its position relative to the corpus

**Joseph Shields** · 29 July 2026
Held in `Desktop\SCI\Helical Relativity`. Nothing here has been written into the corpus.

> **Naming.** This field was developed under the working title *the Bubble Field* and is
> renamed **Helical Relativity** as of this account. The earlier name is retained inside
> `05 History`, in the file names of the computations, and in the documents that were
> issued under it, because those are the record. Where this account says Helical
> Relativity and a script says bubble field, they are the same object.

---

## What this is

A field whose only objects are cells of least action. Each cell carries one quantum of
action, is causal, and is internally split into light, boundary and matter in the corpus's
three weights. Space is the sea of them. Curvature is the failure of that sea to pack
evenly, and gravity between two bodies is each of them sitting in the other's crowding.

The field has four local scalars:

```
alpha_L = ln(a_L/a_L0)     the light barrier, which sets spatial packing
alpha_M = ln(a_M/a_M0)     the matter scale, which sets clock rate
nu      = ln(n/n_0)        the number-density mode
theta                      the cyclic phase, which fixes future orientation
```

and the geometry it produces is

```
T = exp(-alpha_M)        P = exp(alpha_L + nu/3)        T P = exp(alpha_L - alpha_M + nu/3)
```

with `A = -alpha_M` and `B = alpha_L + nu/3` the two metric potentials.

---

## Grades

Using the corpus's own vocabulary.

### PROVED

**The partition is a perfect square.** `u² + 2ur + r² = (u+r)² = 1`, exactly, and the three
parts are the same split as the carrier's antisymmetric square: `u²` on the 10, `2ur` on
the 15, `r²` on the 3. Each cell carries the whole block structure. The factor of 2 in
`2ur` is the two orderings of the cross term, which is why the boundary weight cannot be
defined except as a relation between two things.

**Two handles are necessary for curvature.** If density and size were locked so that `n a³`
were constant, then `nu = -3 alpha`, `P = 1`, and space would be exactly flat with no light
bending at all. The independence of the handles is a precondition, not a freedom.

**The cell is the geometric mean of the Planck and vacuum lengths.** `l_P L_Lambda = a_0²`,
exactly. The identity is dimensional and holds in any theory; what the field adds is the
claim that the middle length is the size of an object. Granting that, it proves that

> **Newton's constant and the cosmological constant problem are the same missing number.**

One ratio, `5.431e30`, appearing once as `a_0/l_P` and once as `L_Lambda/a_0`. The 122
orders of the cosmological constant problem are that ratio to the fourth power, exactly
rather than approximately.

**The compression map, and what geometry can never see.** The map from the four scalars to
the three geometric potentials has rank 3 and nullity 1, with kernel

```
alpha_L -> alpha_L + delta ,      nu -> nu - 3 delta
```

so `A`, `B` and `theta` are recoverable and the combination `alpha_L - nu/3` is not. General
relativity fixes the two potentials and cannot separate the light mode from the density
mode at any precision whatsoever. This was reached twice independently: once as a kernel
computation, once from the observation that the slip parameter comes out identically 1 for
every response ratio.

**The metric and source sector.** Exact isotropic Einstein equations in the bubble
variables, Schwarzschild residuals of exactly zero, the exact relation
`B = alpha - 2 ln cosh(alpha/2)`, and a constant-density star reconstructed end to end with
central `n/n_0 = 1.4766`.

**The spatial mode carries half the light bending.** Deflection goes as `(1 + gamma)`, and a
time-only model has `gamma = 0`. Integrated numerically: 0.87563 arcsec without the spatial
mode, 1.75125 with it, against 1.7512 measured; and 28.655 against 42.982 arcsec per
century for Mercury, measured 42.98 ± 0.04.

**The range hierarchy needs no parameters.** The light channel is the causal cell boundary
itself, so it propagates at c. The matter channel is the decayed sector, which by
definition does not propagate in the surviving one, so its range is zero and a force
carried there is contact or confined. The boundary channel is the only one that exists as
a relation, and the only block whose bracket with itself generates the other two.

**The composition bound is the reciprocal of the cosmological constant.** In the colour
field, joining two strings through the partition shifts the phase by
`arg((W_L + W_M) + W_B e^(i delta))`, and that shift is bounded by

```
    W_B / (W_L + W_M)  =  2ur / (u² + r²)  =  sqrt(5)/3  =  1/Lambda      exactly

    |shift|  <=  arcsin(1/Lambda)  =  48.189685 degrees
```

verified symbolically. `Lambda = 3/sqrt5` was derived years earlier from an entirely
separate argument and nothing was tuned to meet it.

**And it selects the carrier dimension.** A wound string closes when `n · shift = 360 m`
for coprime integers, so the tightest closed object needs `360/arcsin(1/Lambda) = 7.470`
traversals, hence **eight**. Seven is excluded because `360/7 = 51.43` degrees exceeds the
bound and eight is admitted because 45 does not, each by about three degrees, so the
selection is tight rather than generous. Eight is the carrier dimension.

**Self-composition has exactly two fixed points.** The phase shift vanishes only when
`sin(delta) = 0`, so a string reproduces itself under self-composition at relative phase 0
or π and nowhere else. Two classes, symmetric and antisymmetric, both restoring. Checked
against the supplied implementation to 4e-14 degrees, at several hues, which also confirms
the rotational invariance its certificate claims.

### CONDITIONAL

**The response ratio, which closes the last fork.** Under a least Euclidean response cost
with the mixed-boundary constraint `r alpha_L + u alpha_M = chi`, stationarity forces

```
alpha_L / alpha_M = r/u = 1/sqrt(5)        hence   nu = 1.658 alpha_M
```

Verified symbolically and independently. The sign is positive, which is **crowding**, so
the physical picture stands: bubbles are pulled toward mass. It also settles which of the
two readings was right, since the response follows the amplitude ratio `r/u` and not the
intensity ratio `r²/u²`, and `1/sqrt5` is not a new constant but the one already setting
the coframe coefficient in the boundary-block stationarity condition.

Conditional on the cost metric and the constraint, both of which are declared.

**The cell scale.** `a_0(W) = (W hbar c / rho_Lambda)^(1/4)`, an exact family. The branch is
a declared channel assignment: the whole cell gives 87.78 microns, the matter fraction
48.80. The matter branch sits just under the 52 micron torsion-balance limit.

**The vacuum equation of state.** `w = -1` follows exactly, given a cell renewal law
`div N = n Theta` rather than ordinary number conservation. Fixed action per cell means an
expanding region holds more cells rather than thinner ones, and constant density under
expansion is `p = -rho`.

### FORECAST, FROZEN

**Newton's constant from the vacuum record.** `q = r^241 (1-r³)²`, giving
`G = 6.6644e-11` against CODATA `6.6743e-11`, a difference of −0.149 per cent.

The exponent is not fitted: 240 is the root count the corpus derives, plus one for the
external readout, and the observed effective exponent is 241.0497. The fitted object is the
residual prefactor 0.9433, matched by `(1-r³)² = 0.9419`.

The whole uncertainty is in Λ, at 1.5 per cent, while G is already known to 0.002 per cent.
**So any improvement in Λ sharpens this into a real test, and a hundredfold improvement
would test it at 0.015 per cent against a G known 700 times better.** This is a bet that
can be lost, and cosmology settles it rather than algebra.

### RESULT, PENDING A MATCHING OPERATOR

**The UV/IR crossing scale.** `E_cross = sqrt(E_P E_0) = 5241.6 GeV`, the energy form of the
geometric-mean identity and therefore not an extra assumption. The field's output stops
there. The ratio to the electroweak scale, 0.0470, is a matching datum until a
symmetry-breaking operator is supplied.

### WITHDRAWN

Recorded because a folder like this is worth most when it says what has already been tried.

| | |
|---|---|
| the action lock `T·P = 1` | asserted, not derived. `ε·τ = ℏ` is constant by definition and constrains nothing; the cell area `τ·a = cτ²` is not the action. Superseded by `T·P = e^(ν/3)` and then by the three-scale form. |
| "Schwarzschild derived with no field equation" | the profile was supplied to the integrator. What stands is the exact *representation*. |
| the two-body force calculation | started from the Newtonian potential and recovered Newton. A change of variables. |
| the QCD string tension | `σ = ρa² = E²/(ℏc)` identically, so supplying a scale and recovering the tension is a unit conversion. |
| crowding energy as dark matter | short by 10¹¹ in galaxies, and structurally: it is proportional to `rho_Lambda`, so it cannot exceed the vacuum energy times a small potential. |
| the charged-lepton formulas | the muon candidate misses by 0.83 per cent against a quantity measured to two parts in 10⁸. Wrong however arrived at. |
| "more bubbles and bigger bubbles" as vacuum gravity | in the single-scale reading this needed `ν = 0`. Restored by the three-part cell, where crowding tracks the light-matter gap. |

---

---

## The colour field, and what it is

The colour language gives each string a hue, saturation, brightness and accessibility plus
phase, frequency, orientation and winding, and joins two of them through the same
light/boundary/matter partition. Held in `06 Colour Field`.

**As supplied it is a notation.** The proton is assigned hue 8 degrees and the electron
212, so the hydrogen colour that comes out is a deterministic function of inputs that carry
no physics. That is worth saying plainly because everything above it in this section is not
a notation.

**The composition rule is a different matter, because it is a circle map.** That turns "can
this derive particles" into a question with an answer: a particle is an object that
reproduces itself under composition, and fixed points are counted rather than named. Run
against the supplied implementation unmodified, iteration collapses the whole circle onto
one attractor per phase, so the rule as written is contracting and has no spectrum.

**Putting the winding through it produces one.** The string state already carries a winding
number and the composition does not use it; a wound string closes after a whole number of
traversals rather than one, which gives `n · shift = 360 m` and a discrete family indexed by
two coprime integers, bounded below at eight. Sixteen closed objects exist with `n <= 20`,
and exactly one at the minimum depth.

This is the step that converts the colour language from naming to counting, and it is one
line in the composition function. What it does not yet do is attach a mass or a charge to a
depth, which is the same missing mass operator the lepton work needed. **Two independent
lines now converge on one obligation.**

---

## What is corpus-ready

Three papers could be issued from this as it stands.

**One. The cell and the two lengths.** The partition as a perfect square, its identity with
the 10/15/3 blocks, the geometric-mean relation, and the resulting theorem that G and the
cosmological constant problem are one number. Entirely PROVED, short, and it connects
directly to material the corpus already carries.

**Two. The compression boundary.** The kernel theorem, the statement that no gravitational
measurement can separate the light mode from the density mode, and the exact source sector
with the star reconstruction. This is the strongest technical content and it is the part
that makes the field a field rather than a picture.

**Three. The response closure.** The least-cost derivation of `alpha_L/alpha_M = r/u`, the
resulting crowding `nu = 1.658 alpha_M`, and the connection to `1/sqrt5` already present in
the boundary-block condition. CONDITIONAL, and it should be issued as such.

**Four, and this one is new.** The composition bound `arcsin(1/Lambda)`, the two-fixed-point
theorem, and the eight-traversal selection. Short, exact, and it ties the colour field to
the cosmological constant through a channel nobody was looking down. The closure spectrum
itself is a proposal and should be marked as one.

The G forecast belongs in the open ledger as a live bet with a named falsifier, not in a
paper. The lepton work is withdrawn and belongs only in this account.

---

## The programme

1. **The microscopic matter-to-cell law.** The source sector is exact given `A` and `B`; what
   is missing is how matter sets the cells inside itself. This is the one step between a
   representation of general relativity and a derivation of it.
2. **The mass operator.** Charged lepton masses need an operator whose eigenvalue
   multiplicities force their depths. Without it there are no lepton masses here, and with
   it there may be. This is the same fixed-point problem as the boundary-block equation.
3. **Derive the two-leg representation.** The G bridge postulates 240 internal modes, one
   readout, and two retained interrogative legs. Deriving that turns the forecast into a
   theorem.
4. **Sub-millimetre gravity.** Compare 48.8 microns against the published apparatus
   response of the torsion-balance experiments, since the existing bounds are set for
   Yukawa deviations and a granularity signature is a different observable.
5. **Beyond spherical.** The reconstruction is exact in the spherical scalar sector. Vector
   and tensor modes need the phase congruence or a fuller tetrad construction.

---

## Provenance and reproducibility

The work has three hands in it and the folders keep them separate. `05 History` holds the
milestone documents in order, including the first draft and the two review passes, retained
rather than overwritten so the sequence stays legible.

All eight computations in `01 Computations` were run end to end and all eight complete.
One portability fault was repaired: `bubble_field_compression_boundary.py` had its input
path hardcoded to its build machine and could not run anywhere else. It now resolves
relative to itself.

Numerical faults found and fixed along the way, recorded because they were all large enough
to have changed a conclusion: a photon integration started at finite radius rather than
infinity, keeping its outbound tail and dropping its inbound one; a perihelion event that
fired at aphelion, half an orbit early; and `Psi³ − 1` evaluated literally, where with
`Psi − 1` of order 10⁻⁸ the subtraction consumed eight digits, which was the whole gradient
being measured.

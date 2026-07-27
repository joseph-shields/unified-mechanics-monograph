"""Certify the Unified Mechanics dependency graph.

Reads nodes.csv and dependencies.csv, both of which are transcriptions of the
Formal Register and carry the licensing phrase for every edge, so a reader can
check each edge against the Register's own wording.

Three edge kinds:
  dependency  X uses Y in its derivation. These edges form the graph tested for cycles.
  reference   X points the reader at Y for context. Not a dependency. Excluded, because
              treating a pointer as a dependency manufactures false cycles (D10 points at
              T6, which depends on D10).
  witness     Y corroborates X by an independent route. Excluded from the chain.

Emits graph_certificate.json.
"""

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
def _cert(n): return _os.path.join(_ROOT, "certificates", n)
def _csv(n):  return _os.path.join(_ROOT, n)
import csv, json, os, hashlib, sys, datetime, platform



HERE = os.path.dirname(os.path.abspath(__file__))
def path(n): return os.path.join(HERE, n)

nodes = {r["id"]: r for r in csv.DictReader(open(_csv("nodes.csv"), encoding="utf-8"))}
edges = list(csv.DictReader(open(_csv("dependencies.csv"), encoding="utf-8")))

dep = [(e["from"], e["to"]) for e in edges if e["kind"] == "dependency"]
excluded = [(e["from"], e["to"], e["kind"]) for e in edges if e["kind"] != "dependency"]

# --- integrity: every endpoint is a declared node -------------------------------
unknown = sorted({n for a, b in dep for n in (a, b)} - set(nodes))
if unknown:
    sys.exit(f"edge endpoints not declared in nodes.csv: {unknown}")

out = {}                      # X -> what X uses
inc = {}                      # Y -> what uses Y
for a, b in dep:
    out.setdefault(a, set()).add(b)
    inc.setdefault(b, set()).add(a)

# --- acyclicity by depth-first search, reporting the cycle if there is one -------
WHITE, GREY, BLACK = 0, 1, 2
colour = {n: WHITE for n in nodes}
cycle = []

def visit(n, stack):
    colour[n] = GREY
    for m in sorted(out.get(n, ())):
        if colour[m] == GREY:
            cycle.extend(stack[stack.index(m):] + [m]); return True
        if colour[m] == WHITE and visit(m, stack + [m]):
            return True
    colour[n] = BLACK
    return False

for n in sorted(nodes):
    if colour[n] == WHITE and visit(n, [n]):
        break

acyclic = not cycle

# --- structure -------------------------------------------------------------------
# A root stands on nothing: it has no outgoing dependency edge.
roots = sorted(n for n in nodes if not out.get(n))
# A leaf holds nothing up: nothing depends on it.
leaves = sorted(n for n in nodes if not inc.get(n))

results     = sorted(n for n in nodes if nodes[n]["type"] == "result")
obligations = sorted(n for n in nodes if nodes[n]["type"] == "obligation")

# THE LOAD-BEARING QUESTION: does any graded result stand on an open obligation?
# Walk every ancestor of every result and look for an obligation.
def ancestors(n, seen=None):
    seen = seen if seen is not None else set()
    for m in out.get(n, ()):
        if m not in seen:
            seen.add(m); ancestors(m, seen)
    return seen

results_on_obligations = {t: sorted(set(obligations) & ancestors(t)) for t in results}
results_on_obligations = {k: v for k, v in results_on_obligations.items() if v}

# What DOES rest on an obligation, whatever its type.
def descendants(n, seen=None):
    seen = seen if seen is not None else set()
    for m in inc.get(n, ()):
        if m not in seen:
            seen.add(m); descendants(m, seen)
    return seen

rests_on_obligation = {o: sorted(descendants(o)) for o in obligations}

# --- which commitments actually carry load ----------------------------------------
# An axiom or definition that nothing depends on is stated but not used. That is not
# automatically a fault (some are framing), but it should be visible rather than implied.
commitments = sorted(n for n in nodes if nodes[n]["type"] in ("axiom", "definition"))
load_bearing = sorted(n for n in commitments if inc.get(n))
stated_unused = sorted(n for n in commitments if not inc.get(n))

# --- longest chain, for the record ------------------------------------------------
memo = {}
def depth(n):
    if n in memo: return memo[n]
    memo[n] = 0 if not out.get(n) else 1 + max(depth(m) for m in out[n])
    return memo[n]
deepest = max(nodes, key=depth)

cert = {
    "generated": datetime.datetime.now().isoformat(timespec="seconds"),
    "python": platform.python_version(),
    "inputs": {_os.path.basename(f): hashlib.sha256(open(f, "rb").read()).hexdigest()
               for f in (_csv("nodes.csv"), _csv("dependencies.csv"))},
    "nodes": len(nodes),
    "nodes_by_type": {t: sum(1 for n in nodes.values() if n["type"] == t)
                      for t in sorted({n["type"] for n in nodes.values()})},
    "dependency_edges": len(dep),
    "excluded_edges": [{"from": a, "to": b, "kind": k} for a, b, k in excluded],
    "acyclic": acyclic,
    "cycle": cycle,
    "ungrounded_roots": roots,
    "leaves": leaves,
    "load_bearing_commitments": load_bearing,
    "stated_but_unused_commitments": stated_unused,
    "longest_chain_length": depth(deepest),
    "longest_chain_from": deepest,
    "results_standing_on_an_open_obligation": results_on_obligations,
    "what_rests_on_each_obligation": rests_on_obligation,
}
json.dump(cert, open(_cert("graph_certificate.json"), "w", encoding="utf-8"), indent=2)

print(f"nodes {len(nodes)}  dependency edges {len(dep)}  acyclic {acyclic}")
print(f"by type: {cert['nodes_by_type']}")
print(f"ungrounded roots ({len(roots)}): {', '.join(roots)}")
print(f"longest chain: {depth(deepest)} steps, deepest node {deepest}")
print(f"load-bearing commitments ({len(load_bearing)}): {', '.join(load_bearing)}")
print(f"stated but unused ({len(stated_unused)}): {', '.join(stated_unused)}")
print()
if results_on_obligations:
    print("RESULTS STANDING ON AN OPEN OBLIGATION:")
    for k, v in results_on_obligations.items(): print(f"  {k} <- {v}")
else:
    print("No result T1..T28 stands on any open obligation O1..O7.")
print()
print("What rests on each obligation:")
for o, d in rests_on_obligation.items():
    print(f"  {o}: {', '.join(d) if d else '(nothing)'}")

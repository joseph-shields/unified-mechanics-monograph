"""How far is the frontier from phi^2 = phi + 1?

T3 is the golden fixed point: six symbols. This measures, in the certified dependency
graph, how many derivation steps separate that one line from every result the corpus
now carries, and prints the actual chain to the newest ones.
"""

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
def _cert(n): return _os.path.join(_ROOT, "certificates", n)
def _csv(n):  return _os.path.join(_ROOT, n)
import csv, os
from collections import deque



HERE = os.path.dirname(os.path.abspath(__file__))
nodes = {r["id"]: r for r in csv.DictReader(open(_csv("nodes.csv"), encoding="utf-8"))}
edges = [e for e in csv.DictReader(open(_csv("dependencies.csv"), encoding="utf-8"))
         if e["kind"] == "dependency"]
out, why = {}, {}
for e in edges:
    out.setdefault(e["from"], []).append(e["to"])
    why[(e["from"], e["to"])] = e["licensing_phrase"]

ORIGIN = "T3"          # phi^2 = phi + 1

def path_to_origin(n):
    """Shortest dependency chain from n down to the golden fixed point."""
    prev, q = {n: None}, deque([n])
    while q:
        v = q.popleft()
        if v == ORIGIN:
            chain = []
            while v is not None:
                chain.append(v); v = prev[v]
            return chain[::-1]          # read from the result down to the line
        for m in out.get(v, ()):
            if m not in prev:
                prev[m] = v; q.append(m)
    return None

results = [n for n in nodes if nodes[n]["type"] == "result"]
reach = {n: path_to_origin(n) for n in results}
grounded = {n: p for n, p in reach.items() if p}

print(f"phi^2 = phi + 1  is node {ORIGIN}. Six symbols.")
print(f"Results whose chain reaches it: {len(grounded)} of {len(results)}")
print(f"Deepest such result is {max(grounded, key=lambda n: len(grounded[n]))} "
      f"at {max(len(p) for p in grounded.values()) - 1} steps.")
print()

for target in ("T31", "T32", "T23", "T7"):
    p = reach.get(target)
    if not p:
        print(f"{target}: {nodes[target]['title']}")
        print("   does not descend from the golden fixed point; it descends from the "
              "two-sided reading A3 by a separate branch.\n")
        continue
    print(f"{target}  {nodes[target]['title']}   [{len(p)-1} steps from the line]")
    for a, b in zip(p, p[1:]):
        print(f"     {a} <- {b:<4} {nodes[b]['title'][:52]}")
        print(f"            \"{why[(a,b)]}\"")
    print()

ungrounded = sorted(n for n in results if not reach[n])
print(f"Results not descending from T3 ({len(ungrounded)}): {', '.join(ungrounded)}")
print("These descend from the two-sided reading A3, the record D11, or the reduction A6.")

"""Rebuild the second edition end to end.

    python build.py

Figures first, then the document. The plate scripts read their numbers from the
certificates in SCI/ADDENDA, so a change to a solver propagates into the figures
and the prose together and nothing has to be retyped.
"""
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
for step in ("fl_diagrams.py", "fl_charts.py"):
    print("==", step)
    subprocess.run([sys.executable, os.path.join(HERE, step)], check=True,
                   cwd=HERE)
print("== document")
g = {}
for f in ("bookhead.py", "bookbody1.py", "bookbody2.py", "bookbody3.py",
          "bookbody4.py"):
    p = os.path.join(HERE, f)
    exec(compile(open(p, encoding="utf-8").read(), f, "exec"), g)

"""Rebuild every certificate in the corpus from the included code and data.

    python run_all.py

Runs each script from the layer root, hashes every input and output, and writes
certificates/run_manifest.json recording the command, the environment, the input and
output hashes, and pass or fail for each step. A number is not frozen until this
regenerates it.

Exit status is nonzero if any step fails, so this can gate a release.
"""
import hashlib, json, os, platform, subprocess, sys, time

ROOT = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(ROOT, "scripts")
for d in ("results", "figures", "certificates"):
    os.makedirs(os.path.join(ROOT, d), exist_ok=True)

# Ordered so that anything depending on an earlier certificate runs after it.
STEPS = [
    ("validate_dependencies.py",     "the dependency graph, acyclicity, and what rests on each obligation"),
    ("distance_from_the_line.py",    "derivation distance from phi^2 = phi + 1"),
    ("o4_carrier_closure.py",        "O4: explicit complete carrier closure through all 240 roots"),
    ("o2_surviving_block.py",        "O2: exhaustive rank-3 subsystems of E8 and their complements"),
    ("o2_elimination.py",            "O2: elimination of candidates by T10 and T25"),
    ("o1_o3_representation.py",      "O1 and O3: the reduction, the gauge algebra, the matter modules"),
    ("families.py",                  "O3: the family count from the decay's own Weyl group"),
    ("e8_golden_tests.py",           "T12: the golden ring pairing in the Coxeter plane"),
    ("interface_integral_test.py",   "candidate interface coefficients against SPARC"),
    ("sparc_test.py",                "the interface closure against the radial acceleration relation"),
    ("neuro_avalanche_test.py",      "negative screen: neuronal avalanche"),
    ("sgz_balanced_turnover_test.py","negative screen: subgranular zone balanced turnover"),
    ("dev_neurogenesis_test.py",     "cortical neurogenesis accumulating-history extraction"),
    ("o5_o6_cosmology.py",           "O5 and O6: the vacuum readout and the Hubble stake"),
]

def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def tree(d):
    out = {}
    for base, _, files in os.walk(os.path.join(ROOT, d)):
        for f in sorted(files):
            p = os.path.join(base, f)
            out[os.path.relpath(p, ROOT).replace("\\", "/")] = sha(p)
    return out

before = {d: tree(d) for d in ("results", "figures", "certificates")}
env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")

records, failed = [], []
for name, what in STEPS:
    path = os.path.join(SCRIPTS, name)
    if not os.path.exists(path):
        records.append({"script": name, "status": "missing"}); failed.append(name); continue
    t0 = time.time()
    p = subprocess.run([sys.executable, path], cwd=SCRIPTS, env=env,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    ok = p.returncode == 0
    if not ok: failed.append(name)
    records.append({
        "script": name, "purpose": what, "status": "ok" if ok else "FAILED",
        "returncode": p.returncode, "seconds": round(time.time() - t0, 2),
        "script_sha256": sha(path),
        "stdout_tail": p.stdout.strip().splitlines()[-12:],
        "stderr_tail": p.stderr.strip().splitlines()[-6:] if not ok else [],
    })
    print(f"[{'ok ' if ok else 'FAIL'}] {name:<32} {round(time.time()-t0,1):>6}s   {what}")

after = {d: tree(d) for d in ("results", "figures", "certificates")}
changed = {d: sorted(set(k for k in after[d] if before[d].get(k) != after[d][k]))
           for d in after}

manifest = {
    "command": "python run_all.py",
    "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
    "python": platform.python_version(),
    "platform": platform.platform(),
    "packages": {},
    "inputs": {p: sha(os.path.join(ROOT, p)) for p in
               ("nodes.csv", "dependencies.csv") if os.path.exists(os.path.join(ROOT, p))},
    "data": tree("data"),
    "steps": records,
    "outputs_written_or_changed": changed,
    "all_passed": not failed,
    "failed": failed,
}
for mod in ("numpy", "scipy", "matplotlib"):
    try:
        manifest["packages"][mod] = __import__(mod).__version__
    except Exception:
        manifest["packages"][mod] = "not installed"

with open(os.path.join(ROOT, "certificates", "run_manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

print()
print(f"{len(STEPS) - len(failed)}/{len(STEPS)} steps passed")
if failed:
    print("FAILED: " + ", ".join(failed))
print("wrote certificates/run_manifest.json")
sys.exit(1 if failed else 0)

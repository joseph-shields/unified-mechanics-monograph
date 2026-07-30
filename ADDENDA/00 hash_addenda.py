"""Rehash every addendum folder. Run from anywhere; it locates itself."""
import hashlib, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
MANIFEST = "SHA256SUMS.txt"

total = 0
for folder in sorted(p for p in HERE.iterdir() if p.is_dir()):
    files = sorted(p for p in folder.rglob("*")
                   if p.is_file() and p.name != MANIFEST)
    if not files:
        continue
    lines = []
    for p in files:
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        lines.append(f"{h}  ./{p.relative_to(folder).as_posix()}")
    (folder / MANIFEST).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{folder.name}: {len(files)} files hashed")
    total += len(files)
print(f"\n{total} files across {len([p for p in HERE.iterdir() if p.is_dir()])} addenda")

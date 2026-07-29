# Lean build note

This is the lean variant of Volume E, cut for the repository. **Eleven files were removed,
26.7 MB, all of them renders. No data, no computation, no plate that any result depends on.**

## What was removed

| | |
|---|---|
| 7.37 MB | `03 COLOUR FIELD/03 Visuals/observer_inside_colour_field_evolution.gif` |
| 3.03 MB | `03 COLOUR FIELD/03 Visuals/concept_arctangent_umbrella_field.png` |
| 3.01 MB | `03 COLOUR FIELD/03 Visuals/concept_observer_inside_solid_wall_of_light.png` |
| 2.88 MB | `04 HELICAL FIELD/03_Visuals/umbrella_observer_concept.png` |
| 2.14 MB | `04 HELICAL FIELD/03_Visuals/helical_bubble_field_time_evolution.gif` |
| 1.59 MB | `05 FIGURES/interactive_scalar_field_map_visualization.png` |
| 1.45 MB | `05 FIGURES/universal_field_of_least_action_diagram.png` |
| 1.44 MB | `03 COLOUR FIELD/03 Visuals/observer_inside_quantum_colour_field.png` |
| 1.36 MB | `05 FIGURES/visual_scalar_field_system_diagram.png` |
| 1.28 MB | `04 HELICAL FIELD/03_Visuals/observer_inside_helical_field.png` |
| 1.11 MB | `03 COLOUR FIELD/02 Interactive/...web_preview.png` |

Concept art, two animations, three system diagrams and a browser screenshot. They are
illustrations of the picture, not evidence for it.

## What was kept, deliberately

- **every computation and every JSON certificate**, so all ten scripts still run
- **the seven atlas plates** in `03 COLOUR FIELD/07 Atlas Plates`, which carry the
  composition bound, the closure spectrum and the mass operator result
- **the two audio files**, since they are small and they are the sonification
- **the complete Quantum Colour Dictionary**, JSON and presets CSV. These are *data*, 5.7 MB
  of it, holding 7,301 presets. They were briefly cut from an earlier attempt at this
  variant and put back: the dictionary is the field's vocabulary, not a render of it.
- **the entire Atomic Web**, all 118 element cards, six master plates, four atlas boards,
  the CSV, the JSON and both audits. It is 43 MB of the 79 and it is the most
  independently checkable thing in the volume.

## Recovering the full set

The removed renders are in the complete build. Nothing references them by path, so the
lean variant is self-contained and every script, hash and cross-link resolves.

Regenerate the hashes after any further trimming:

```bash
cd "06 HELICAL RELATIVITY" && python - <<'EOF'
import hashlib, pathlib
d = pathlib.Path('.')
files = sorted(p for p in d.rglob('*') if p.is_file() and p.name != '04 SHA256SUMS.txt')
lines = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  ./{p.relative_to(d).as_posix()}"
         for p in files]
(d/'00 START HERE'/'04 SHA256SUMS.txt').write_text("\n".join(lines)+"\n", encoding='utf-8')
print(len(lines), "files hashed")
EOF
```

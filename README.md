Unified Mechanics is an independent research programme exploring whether many familiar structures in mathematics and physics can be understood through one shared systems-level framework.

The project distinguishes between:

- the abstract rules used to describe systems,
- the physical systems that realise those rules,
- the local conditions that shape their behaviour,
- and the records through which those systems become observable.

The framework does not claim that mathematics alone creates a universe from nothing. Its aim is to describe how real systems retain identity, interact with their surroundings, transform over time, and leave measurable records.

## What this repository contains

This repository includes:

- the main Unified Mechanics monograph,
- a compact edition of the monograph,
- formal appendices and supporting arguments,
- Universopedia, the observational and language framework,
- the Realisation and Self-Description Principle,
- research notes, tests, and open problems.

## Universopedia

Universopedia is the bridge between the observed world and the abstract framework.

It begins with familiar physical systems such as atoms, stars, galaxies, black holes, and living systems. It records what is directly observed, what is inferred, which local conditions matter, and how each system can be compressed into a common systems description.

The Familiarity Kernel identifies recorded structure that has not yet been placed into a stable and validated physical class.

## Current status

Unified Mechanics is an active research programme.

Some parts are formal mathematical results. Others are conditional constructions, interpretations, conjectures, or open problems. The documents aim to label those differences clearly.

The main current goal is not to replace successful physical theories with a single fitting formula. It is to investigate whether their structures can be connected through a shared account of systems, boundaries, local conditions, transformation, and observation.

## How to read the repository

A useful reading order is:

1. The main monograph
2. The compact monograph
3. Universopedia
4. The Realisation and Self-Description Principle
5. Supporting appendices, tests, and research notes

## Feedback

The most useful feedback concerns:

- mathematical gaps,
- hidden assumptions,
- unclear definitions,
- circular reasoning,
- conflicts with established results,
- related mathematical work,
- and ways to make the framework more precise.

This repository is intended to make the programme inspectable, testable, and open to correction.
"""

path = Path("/mnt/data/README.md")
path.write_text(readme, encoding="utf-8")
print(path)

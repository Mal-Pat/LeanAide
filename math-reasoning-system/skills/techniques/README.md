# Mathematical Techniques Library

This directory contains specialized proof techniques organized by mathematical field.

## Directory Structure
- `generic_arguments/`: Multi-disciplinary techniques for "almost all" reasoning (Topology, Measure, Baire, Algebraic Geometry).
- `invariants/`: General techniques for finding invariants and monovariants.
- `geometry/`: Differential and Riemannian geometry techniques (e.g., Bochner technique).

## Adding a Technique
1. Create a subfolder with the technique name.
2. Add `SKILL.md` containing the step-by-step instructions.
3. Add `manifest.json` with metadata for the dispatcher.
4. Register the technique in `skills/04_strategy_gen/registry.md`.

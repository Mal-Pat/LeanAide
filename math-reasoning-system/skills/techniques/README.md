# Mathematical Techniques Library

This directory contains specialized proof techniques organized by mathematical field
and by reusable proof structure.

## Directory Structure
- `core/`: General logical structures such as direct proof, contradiction, cases, equivalence, and reduction.
- `construction/`: Existence, explicit construction, and uniqueness arguments.
- `induction/`: Ordinary induction, strong induction, structural induction, minimal counterexamples, and descent.
- `combinatorics/`: Counting, double counting, pigeonhole, and finite enumeration arguments.
- `order/`: Bounding, monotonicity, squeeze, and extremal object arguments.
- `analysis/`: Epsilon-delta, density, and approximation arguments.
- `local_global/`: Compactness and gluing arguments.
- `algebra/`: Universal property arguments and related algebra/category-theory techniques.
- `algorithms/`: Termination and correctness arguments.
- `diagrammatic/`: Diagram chase and geometric/diagrammatic reasoning.
- `generic_arguments/`: Multi-disciplinary techniques for "almost all" reasoning (Topology, Measure, Baire, Algebraic Geometry).
- `invariants/`: General techniques for finding invariants and monovariants.
- `geometry/`: Differential and Riemannian geometry techniques (e.g., Bochner technique).

## Adding a Technique
1. Create a subfolder with the technique name.
2. Add `SKILL.md` containing the step-by-step instructions.
3. Add `manifest.json` with metadata for the dispatcher.
4. Register the technique in `skills/04_strategy_gen/registry.md`.

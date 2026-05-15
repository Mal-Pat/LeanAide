# Advanced Technique Registry

This registry lists specialized mathematical proof techniques available to the Strategy Generation dispatcher.

| Technique | Area | Keywords | Path |
| :--- | :--- | :--- | :--- |
| **Direct, Contrapositive, and Contradiction Proofs** | Core Logic | implication, contrapositive, contradiction, negation | `techniques/core/direct_contrapositive_contradiction/SKILL.md` |
| **Cases and Exhaustion** | Core Logic | cases, finite cases, parity, residues, signs | `techniques/core/cases_exhaustion/SKILL.md` |
| **Equivalence and Reduction** | Core Logic | iff, equivalent conditions, reduction, known theorem | `techniques/core/equivalence_reduction/SKILL.md` |
| **Existence, Construction, and Uniqueness** | Construction | exists, witness, construction, unique, canonical object | `techniques/construction/existence_uniqueness/SKILL.md` |
| **Induction, Minimal Counterexample, and Descent** | Induction | induction, strong induction, structural induction, minimal counterexample, descent | `techniques/induction/induction_and_descent/SKILL.md` |
| **Counting, Double Counting, and Pigeonhole** | Combinatorics | counting, double counting, pigeonhole, finite set, incidence | `techniques/combinatorics/counting_pigeonhole/SKILL.md` |
| **Invariant Construction** | General | combinatorics, group actions, game theory | `techniques/invariants/SKILL.md` |
| **Bounding, Monotonicity, and Extremal Objects** | Order/Analysis/Combinatorics | bounds, monotonicity, squeeze, maximal, minimal, extremal | `techniques/order/bounding_extremal/SKILL.md` |
| **Epsilon-Delta Proofs** | Analysis | limit, continuity, convergence, epsilon delta, metric space | `techniques/analysis/epsilon_delta/SKILL.md` |
| **Density and Approximation** | Analysis/Topology | density, approximation, dense subset, continuity, limit passage | `techniques/analysis/density_approximation/SKILL.md` |
| **Compactness and Local-to-Global Gluing** | Topology/Geometry/Logic | compactness, local-to-global, gluing, open cover, finite subcover | `techniques/local_global/compactness_gluing/SKILL.md` |
| **Universal Property Arguments** | Algebra/Category Theory | universal property, product, coproduct, quotient, tensor product, adjunction | `techniques/algebra/universal_property/SKILL.md` |
| **Algorithmic Correctness** | Algorithms/Logic/Discrete Math | algorithm, termination, correctness, loop invariant, recursion | `techniques/algorithms/correctness/SKILL.md` |
| **Diagram Chase and Diagrammatic Reasoning** | Algebra/Topology/Geometry | diagram chase, commutative diagram, exact sequence, geometric diagram | `techniques/diagrammatic/diagram_chase/SKILL.md` |
| **Bochner Technique** | Geometry | riemannian geometry, manifolds, curvature | `techniques/geometry/bochner_technique/SKILL.md` |
| **Generic Arguments** | General | baire category, measure theory, zariski, dense open | `techniques/generic_arguments/SKILL.md` |

## Hierarchy
- **Core Logical Techniques:** Nested under `techniques/core/`.
- **Reusable Structural Techniques:** Nested under `techniques/construction/`, `techniques/induction/`, `techniques/order/`, `techniques/local_global/`, and `techniques/algorithms/`.
- **Field-Specific Techniques:** Nested within `techniques/<field>/`, such as `analysis/`, `algebra/`, `combinatorics/`, and `geometry/`.

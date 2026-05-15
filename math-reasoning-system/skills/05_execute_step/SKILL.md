# Skill: Execution
Perform the next logical deduction from the current proof plan.
1. **Justification:** State exactly which theorem/axiom justifies the move.
2. **Example Sanity Check:** If the deduction introduces a new lemma, equality case, claimed equivalence, or strengthened statement, test it against the examples already recorded in `artifacts/02_examples.md` or request `skills/12_example_counterexample/SKILL.md`.
3. **Recursive Trigger:** If the step requires its own strategy and deconstruction, label as 'hard' and signal the Orchestrator to spawn a sub-loop.

**Scope:** This skill is for proof execution. In exploratory research mode, execute probes with `skills/09_exploratory_probe/SKILL.md` instead, unless the current probe has been converted into a precise theorem-proving subproblem.

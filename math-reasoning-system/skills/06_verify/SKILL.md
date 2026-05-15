# Skill: Verification

## Path A: INFORMAL_ONLY
- **The Skeptic's Hat:** Act as a critical peer reviewer. Find gaps in topological/algebraic assumptions.
- **Counter-examples:** Test result against edge cases.
- **Research Mode:** If checking a conjecture or proposed extension, label it as `supported`, `refuted`, `needs_hypotheses`, or `open`; do not upgrade it to a theorem without proof.
- Use `schema_informal.json`.

## Path B: WITH_LEAN
- **Drafting:** Formalize the step in Lean 4.
- **Style:** Use declarative proof style (`have`, `show`, `calc`).
- **Preference:** For even numbers, use $n = r + r$.
- Use `schema_lean.json` and `lean_boilerplate.lean`.

*Rule: If verification fails, stop the loop.*

**Regression Rule:** In problem-solving mode, verification remains binary for the current proof step: sound steps continue, unsound steps stop or force a pivot. Research-mode labels are only for exploratory conjectures.

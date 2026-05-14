# Skill: Verification

## Path A: INFORMAL_ONLY
- **The Skeptic's Hat:** Act as a critical peer reviewer. Find gaps in topological/algebraic assumptions.
- **Counter-examples:** Test result against edge cases.
- Use `schema_informal.json`.

## Path B: WITH_LEAN
- **Drafting:** Formalize the step in Lean 4.
- **Style:** Use declarative proof style (`have`, `show`, `calc`).
- **Preference:** For even numbers, use $n = r + r$.
- Use `schema_lean.json` and `lean_boilerplate.lean`.

*Rule: If verification fails, stop the loop.*

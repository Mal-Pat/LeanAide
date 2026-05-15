# Skill: Problem Deconstruction
Analyze the input LaTeX problem or research prompt. Generate `artifacts/01_problem_formalization.md`.
1. **Components:** Extract Givens, Hypotheses, and Goal.
   - If the input is exploratory and has no fixed theorem to prove, write the best current research aim in `goal` and mark it as provisional.
2. **Definitions:** Define all terms formally. Resolve ambiguities.
3. **Intuition:** Provide a 3-sentence undergraduate-level summary.
4. **Objective Classification:** Mark whether this is a `well_stated_problem`, `research_seed`, `extension_request`, or `ambiguous`.
5. **Question Seeds:** For exploratory inputs, list 3-5 possible precise questions or theorem candidates without pretending they are already true.
6. **Example Seeds:** List 2-5 natural examples, boundary cases, or possible counterexample families suggested by the definitions. If the statement is a fixed theorem, these are sanity checks, not evidence of proof.
Output must match `schema.json`.

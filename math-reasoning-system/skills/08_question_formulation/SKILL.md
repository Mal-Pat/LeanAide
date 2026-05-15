# Skill: Research Question Formulation

**Goal:** Convert an open-ended mathematical prompt into precise, ranked research questions without pretending they are already proven.

**Instructions:**
1. **Read Context:** Review `artifacts/01_problem_formalization.md` and, if present, `artifacts/02_literature_review.md`.
2. **Extract Axes of Variation:**
   - hypotheses to weaken or strengthen;
   - conclusions to sharpen, quantify, or replace;
   - ambient categories, dimensions, regularity classes, or finiteness assumptions to vary;
   - examples and counterexamples suggested by the definitions.
3. **Generate Questions:** Produce 5-10 precise questions. Each question must have:
   - a mathematical statement or objective;
   - motivation;
   - expected difficulty;
   - first probes to try.
4. **Generate Test Objects:** For each primary question candidate, list representative examples and likely counterexample families to examine.
5. **Rank:** Choose 2-3 primary questions by balancing plausibility, novelty, tractability, and relevance to the user's prompt.
6. **Guardrails:** Mark speculative claims as questions or conjectures, not theorems.

**Output:** Save to `artifacts/02_research_questions.md`. If structured output is requested, use `schema.json`.

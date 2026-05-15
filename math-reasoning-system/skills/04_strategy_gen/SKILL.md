# Skill: Strategy Generation (Dispatcher)

**Goal:** Formulate concrete, step-by-step proof plans by selecting and applying appropriate mathematical techniques.

**Scope:** Use this skill for `PROBLEM_SOLVING`. For `EXPLORATORY_RESEARCH`, use `skills/09_exploratory_probe/SKILL.md` unless a precise theorem has already been selected as the current target.

**Instructions:**
1. **Analyze Formalization:** Review `artifacts/01_problem_formalization.md`.
   - If `artifacts/02_examples.md` exists, use it to avoid strategies already refuted by counterexamples.
2. **Technique Selection:**
   - Scan `skills/04_strategy_gen/registry.md` and `skills/techniques/` for any skill whose manifest matches the problem context.
   - If a match is found (e.g., Riemannian manifolds -> `bochner_technique`), invoke that specific skill to generate strategy fragments.
3. **Reasoning Synthesis:**
   - **Forward Reasoning:** List 3-5 deductions from hypotheses.
   - **Backward Reasoning:** List 2-3 conditions implying the goal.
   - **Simplification:** Propose 2 special cases.
   - **Example Check:** List 2-3 examples or boundary cases that the plan should explain. If any counterexample appears valid, stop and recommend revising the statement instead of drafting a proof.
4. **Draft Plans:**
   - Generate Plan A and Plan B, incorporating selected technique fragments.
   - **CRITICAL:** Label every step's difficulty as `easy`, `standard`, or `hard`.
5. **Output:** Save to `artifacts/03_strategy_plans.md`.

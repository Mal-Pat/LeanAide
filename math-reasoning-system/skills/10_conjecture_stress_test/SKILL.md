# Skill: Conjecture Stress Test

**Goal:** Test a candidate conjecture or extension before treating it as a theorem.

**Instructions:**
1. **State the Candidate Precisely:** Include all hypotheses, definitions, and the proposed conclusion.
2. **Boundary Checks:** Test degenerate, small, low-dimensional, finite, singular, noncompact, noncommutative, or non-Noetherian cases as appropriate.
3. **Hypothesis Stress-Testing:** Remove or weaken one hypothesis at a time and look for failure.
4. **Known-Theorem Alignment:** Compare the candidate with known theorems. Decide whether it is a corollary, strengthening, variant, or likely false.
5. **Proof Skeleton:** If the candidate survives, outline the most plausible proof technique and identify the hardest lemma.
6. **Classification:** Label the candidate as `plausible`, `refuted`, `needs_extra_hypotheses`, `known_or_near_known`, or `open`.

**Output:** Append to `artifacts/04_research_trace.md`. If structured output is requested, use `schema.json`.

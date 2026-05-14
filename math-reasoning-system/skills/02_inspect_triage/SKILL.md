# Skill: Problem Inspection & Triage

**Goal:** Decide if the agent should immediately begin strategizing or if it must study literature first.

**Instructions:**
1. Review `artifacts/01_problem_formalization.md`.
2. Assess complexity: Is this a standard textbook problem, or does it invoke advanced, highly specific machinery (e.g., specific theorems from recent literature)?
3. **Decision:** 
   - Return `DIRECT_PROOF` if the hypotheses and goal use standard definitions that can be manipulated directly.
   - Return `SOURCE_STUDY` if the problem requires adapting a complex known theorem. Suggest keywords or specific papers to search.

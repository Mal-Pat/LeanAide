# Skill: Problem Inspection & Triage

**Goal:** Decide if the agent should begin proof strategizing, study literature, or branch into exploratory research.

**Instructions:**
1. Review `artifacts/01_problem_formalization.md`.
2. Assess objective type and complexity:
   - Is there a precise claim with fixed hypotheses and a fixed goal?
   - Is the request instead to extend, generalize, formulate questions, or look for conjectures?
   - Does it invoke advanced, highly specific machinery requiring source study?
3. **Decision:** 
   - Return `DIRECT_PROOF` if the hypotheses and goal use standard definitions that can be manipulated directly.
   - Return `SOURCE_STUDY` if the problem requires adapting a complex known theorem. Suggest keywords or specific papers to search.
   - Return `EXPLORATORY_RESEARCH` if there is no fixed theorem to prove, or the user asks for extensions, questions, conjectures, examples, or research directions.

**Regression Rule:** If the input is a normal theorem/exercise with an explicit goal, do not route to exploratory research merely because generalizations might be interesting.

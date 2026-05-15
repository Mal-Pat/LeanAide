# Skill: Meta-Cognition & Loop Control

**Goal:** Analyze the current proof or research trace and decide what the Orchestrator should do next.

**Instructions:**
1. In problem-solving mode, read `artifacts/04_execution_trace.md` and the current sub-goal.
   In exploratory research mode, read `artifacts/04_research_trace.md`, `artifacts/02_research_questions.md`, and any current conjecture.
2. **Progress Analysis:** Score viability from 1-10. Are we caught in a circular argument? Is the algebra exploding in complexity?
3. **Bottleneck Identification:** If stuck, formulate the exact obstacle as a precise mathematical question.
4. **Problem-Solving Next Step Decision:** In `PROBLEM_SOLVING`, output exactly one of the following commands:
   - `REFINE`: Proceed with the current plan, with minor adjustments.
   - `PIVOT`: Abandon the current plan. Switch to Plan B from the strategy artifact.
   - `ABANDON`: All plans exhausted. Trigger the generation of `artifacts/05_failure_report.md`.
5. **Research Next Step Decision:** In `EXPLORATORY_RESEARCH`, output exactly one of the following commands:
   - `PROBE`: Run another example, counterexample, specialization, or analogy probe.
   - `FORMULATE`: Convert evidence into a precise conjecture or question.
   - `STRESS_TEST`: Test a conjecture against edge cases and hypothesis weakening.
   - `SOURCE_STUDY`: Gather or revisit literature for the current obstacle.
   - `THEOREM_MODE`: A precise, plausible theorem has emerged; switch to `PROBLEM_SOLVING`.
   - `SYNTHESIZE`: Enough progress has accumulated; generate a research brief.
   - `ABANDON`: Exploration is exhausted; generate `artifacts/05_research_obstacles.md`.

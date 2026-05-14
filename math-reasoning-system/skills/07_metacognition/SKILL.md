# Skill: Meta-Cognition & Loop Control

**Goal:** Analyze the current execution trace and decide what the Orchestrator should do next.

**Instructions:**
1. Read `artifacts/04_execution_trace.md` and the current sub-goal.
2. **Progress Analysis:** Score viability from 1-10. Are we caught in a circular argument? Is the algebra exploding in complexity?
3. **Bottleneck Identification:** If stuck, formulate the exact obstacle as a precise mathematical question.
4. **Next Step Decision:** Output exactly one of the following commands:
   - `REFINE`: Proceed with the current plan, with minor adjustments.
   - `PIVOT`: Abandon the current plan. Switch to Plan B from the strategy artifact.
   - `ABANDON`: All plans exhausted. Trigger the generation of `artifacts/05_failure_report.md`.

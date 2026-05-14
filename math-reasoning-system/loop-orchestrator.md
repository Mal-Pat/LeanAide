# Master Orchestrator

## 1. Configuration
- **Execution Mode:** [User Specified: AUTONOMOUS | INTERACTIVE]
- **Verification Mode:** [User Specified: WITH_LEAN | INFORMAL_ONLY]

## 2. The Loop
Follow these phases strictly. Generate artifacts in `artifacts/` at each milestone.

**Phase 1: Formalization & Triage**
- Run `skills/01_deconstruct/SKILL.md`. Save to `artifacts/01_problem_formalization.md`.
- Run `skills/02_inspect_triage/SKILL.md`.
  - If `Source Study`: Run `skills/03_source_study/SKILL.md`. Save to `artifacts/02_literature_review.md`.
  - If `Direct Proof`: Proceed.

**Phase 2: Strategy**
- Run `skills/04_strategy_gen/SKILL.md`. Save to `artifacts/03_strategy_plans.md`.
- Classify steps as `easy`, `standard`, or `hard`.

**Phase 3: Execution Engine**
- Select a plan and loop:
  1. **Execute:** Run `skills/05_execute_step/SKILL.md`.
     - *Recursion:* If step is 'hard', pause and restart this loop on the sub-lemma.
  2. **Verify:** Run `skills/06_verify/SKILL.md` using the active Verification Mode.
  3. **Assess:** Run `skills/07_metacognition/SKILL.md`. 
  - Update `artifacts/04_execution_trace.md`.

**Phase 4: Termination**
- **Success:** Generate `artifacts/05_final_manuscript.md`.
- **Stuck:** Generate `artifacts/05_failure_report.md`.

*Protocol: If INTERACTIVE, pause after every Phase.*

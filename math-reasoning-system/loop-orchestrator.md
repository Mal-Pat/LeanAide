# Master Orchestrator

## 1. Configuration
- **Execution Mode:** [User Specified: AUTONOMOUS | INTERACTIVE]
- **Verification Mode:** [User Specified: WITH_LEAN | INFORMAL_ONLY]
- **Objective Mode:** [User Specified or AUTO: PROBLEM_SOLVING | EXPLORATORY_RESEARCH | AUTO]

`PROBLEM_SOLVING` is for a well-stated theorem, exercise, or lemma with fixed
hypotheses and a fixed goal. `EXPLORATORY_RESEARCH` is for open-ended requests:
extend a theorem, find variants, formulate questions, search for conjectures, or
map a research direction. In `AUTO`, keep the legacy proof-solving path whenever
the input contains a precise claim to prove; branch to exploratory research only
when no fixed target theorem is present or the user explicitly asks for
question/conjecture generation.

## 2. The Loop
Follow these phases strictly. Generate artifacts in `artifacts/` at each milestone.

**Phase 1: Formalization & Triage**
- Run `skills/01_deconstruct/SKILL.md`. Save to `artifacts/01_problem_formalization.md`.
- Run `skills/02_inspect_triage/SKILL.md`.
  - If definitions are unfamiliar, hypotheses look sharp, or the statement may be false, run `skills/12_example_counterexample/SKILL.md`. Save to `artifacts/02_examples.md`.
  - In `PROBLEM_SOLVING`, example generation is a sanity check only; it must not replace a proof.
  - If `Source Study`: Run `skills/03_source_study/SKILL.md`. Save to `artifacts/02_literature_review.md`.
  - If `Direct Proof`: Proceed.
  - If `Exploratory Research`: Run `skills/08_question_formulation/SKILL.md`. Save to `artifacts/02_research_questions.md`.
  - If exploratory work requires background, also run `skills/03_source_study/SKILL.md`. Save to `artifacts/02_literature_review.md`.

**Phase 2: Strategy**
- For `PROBLEM_SOLVING`: Run `skills/04_strategy_gen/SKILL.md`. Save to `artifacts/03_strategy_plans.md`.
- Classify steps as `easy`, `standard`, or `hard`.
- Use `artifacts/02_examples.md`, if present, to eliminate false plans and identify likely sharp hypotheses.
- For `EXPLORATORY_RESEARCH`: Run `skills/09_exploratory_probe/SKILL.md`. Save to `artifacts/03_exploration_plan.md`.
  - Classify probes as `low_cost`, `medium_cost`, or `high_cost`.
  - Mark each probe as `example_search`, `counterexample_search`, `generalization`, `specialization`, `analogy`, or `source_check`.
  - Use `skills/12_example_counterexample/SKILL.md` for concrete example and counterexample probes.

**Phase 3: Execution Engine**
- In `PROBLEM_SOLVING`, select a proof plan and loop:
  1. **Execute:** Run `skills/05_execute_step/SKILL.md`.
     - *Recursion:* If step is 'hard', pause and restart this loop on the sub-lemma.
     - If a new lemma or subclaim looks doubtful, run `skills/12_example_counterexample/SKILL.md` before investing in a long proof.
  2. **Verify:** Run `skills/06_verify/SKILL.md` using the active Verification Mode.
  3. **Assess:** Run `skills/07_metacognition/SKILL.md`. 
  - Update `artifacts/04_execution_trace.md`.
- In `EXPLORATORY_RESEARCH`, select an exploration plan and loop:
  1. **Probe:** Run `skills/09_exploratory_probe/SKILL.md` for the next concrete probe; for example or counterexample construction, run `skills/12_example_counterexample/SKILL.md`.
  2. **Stress-Test:** Run `skills/10_conjecture_stress_test/SKILL.md` on any emerging conjecture or candidate extension.
  3. **Assess:** Run `skills/07_metacognition/SKILL.md` in research mode.
  - Update `artifacts/04_research_trace.md`.
  - If a precise theorem emerges and the user wants a proof, switch to `PROBLEM_SOLVING` with that theorem as the new goal.

**Phase 4: Termination**
- **Problem-Solving Success:** Generate `artifacts/05_final_manuscript.md`.
- **Problem-Solving Stuck:** Generate `artifacts/05_failure_report.md`.
- **Research Consolidation:** Run `skills/11_research_synthesis/SKILL.md` and generate `artifacts/05_research_brief.md`.
- **Research Stuck:** Generate `artifacts/05_research_obstacles.md` with precise blockers, failed conjectures, and promising next probes.

*Protocol: If INTERACTIVE, pause after every Phase.*

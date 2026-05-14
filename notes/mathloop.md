# Meta-Prompt: Constructing the Mathematical Reasoning System

**To the Coding Agent:**
Act as a system architect. Create a directory named `math-reasoning-system/` and populate it with the following structure and file contents. This system is designed to allow an LLM to perform high-level mathematical research autonomously or interactively, with support for both formal (Lean 4) and informal (Peer-Review style) verification.

---

## 1. Directory Structure

```text
math-reasoning-system/
├── README.md                      # Setup and usage instructions
├── loop-orchestrator.md           # The Master State Machine
├── artifacts/                     # (Dir) Persistent mathematical artifacts
├── logs/                          # (Dir) Execution traces and failure logs
└── skills/                        # (Dir) Folder-based skill architecture
    ├── 01_deconstruct/
    │   ├── SKILL.md
    │   └── schema.json
    ├── 02_inspect_triage/
    │   └── SKILL.md
    ├── 03_source_study/
    │   ├── SKILL.md
    │   └── schema.json
    ├── 04_strategy_gen/
    │   ├── SKILL.md
    │   └── examples.md
    ├── 05_execute_step/
    │   └── SKILL.md
    ├── 06_verify/
    │   ├── SKILL.md
    │   ├── schema_informal.json
    │   ├── schema_lean.json
    │   └── lean_boilerplate.lean
    └── 07_metacognition/
        └── SKILL.md

```

---

## 2. File Contents

### 2.1. README.md

```markdown
# Mathematical Reasoning System

An agentic framework for solving complex mathematical problems through recursive deconstruction, strategic planning, and dual-mode verification.

## Modes of Operation
Before starting, specify your modes:

**Execution Modes:**
- `AUTONOMOUS`: Agent runs the full loop until success or failure.
- `INTERACTIVE`: Agent pauses after each phase for user feedback.

**Verification Modes:**
- `WITH_LEAN`: Logic is formalized and checked in Lean 4 (Declarative style).
- `INFORMAL_ONLY`: Logic is verified via "The Skeptic's Hat" (Peer-review style).

## Quick Start
1. Open your agentic CLI in this directory.
2. Provide the problem and set the modes.
3. Prompt: "Read `loop-orchestrator.md`. Problem: [LaTeX]. Mode: [AUTONOMOUS/WITH_LEAN]. Start."

```

### 2.2. loop-orchestrator.md

```markdown
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

```

### 2.3. skills/01_deconstruct/SKILL.md

```markdown
# Skill: Problem Deconstruction
Analyze the input LaTeX problem. Generate `artifacts/01_problem_formalization.md`.
1. **Components:** Extract Givens, Hypotheses, and Goal.
2. **Definitions:** Define all terms formally. Resolve ambiguities.
3. **Intuition:** Provide a 3-sentence undergraduate-level summary.
Output must match `schema.json`.

```

### 2.4. skills/06_verify/SKILL.md

```markdown
# Skill: Verification

## Path A: INFORMAL_ONLY
- **The Skeptic's Hat:** Act as a critical peer reviewer. Find gaps in topological/algebraic assumptions.
- **Counter-examples:** Test result against edge cases.
- Use `schema_informal.json`.

## Path B: WITH_LEAN
- **Drafting:** Formalize the step in Lean 4.
- **Style:** Use declarative proof style (`have`, `show`, `calc`).
- **Preference:** For even numbers, use $n = r + r$.
- Use `schema_lean.json` and `lean_boilerplate.lean`.

*Rule: If verification fails, stop the loop.*

```

### 2.5. skills/05_execute_step/SKILL.md

```markdown
# Skill: Execution
Perform the next logical deduction from the current proof plan.
1. **Justification:** State exactly which theorem/axiom justifies the move.
2. **Recursive Trigger:** If the step requires its own strategy and deconstruction, label as 'hard' and signal the Orchestrator to spawn a sub-loop.

```


### 2.6. skills/04_strategy_gen/SKILL.md

```markdown
# Skill: Strategy Generation

**Goal:** Formulate concrete, step-by-step plans to solve the problem formalized in `artifacts/01_problem_formalization.md`. Save the output to `artifacts/03_strategy_plans.md`.

**Instructions:**
1. **Forward Reasoning:** List 3-5 immediate, non-trivial deductions from the hypotheses.
2. **Backward Reasoning:** List 2-3 conditions that would directly imply the final goal.
3. **Simplification:** Propose 2 special, simplified cases (e.g., $n=1$, finite dimension, Abelian group) and state what insight they might yield.
4. **Proof Sketches:** Generate at least two distinct proof sketches (Plan A and Plan B). 
   - Break each plan down into logical steps/lemmas.
   - **CRITICAL:** Label every step's difficulty as `easy`, `standard`, or `hard`. A step must be labeled `hard` if it requires its own multi-step proof (this will trigger a recursive loop).

**Output format:** Generate the content in Markdown format suitable for the artifacts directory.

```

### 2.7. skills/04_strategy_gen/examples.md

```markdown
# Examples of Good Strategy Generation

## Forward Reasoning Example
*   *Hypothesis:* $G$ is a finite group of order $p^n$.
*   *Deduction:* By Sylow's Theorems, $G$ has a non-trivial center $Z(G)$.

## Proof Sketch Example
**Plan A: Proof by Contradiction**
*   **Step 1 (easy):** Assume for contradiction that $\sqrt{2} = a/b$ where $a,b$ are coprime.
*   **Step 2 (standard):** Deduce that $a^2 = 2b^2$, hence $a^2$ is even.
*   **Step 3 (hard):** Lemma: Prove that if $a^2$ is even, then $a$ is even. *(Note: Requires recursive loop).*
*   **Step 4 (standard):** Substitute $a=2k$ to show $b^2$ is even, implying $b$ is even, contradicting coprimality.

```

### 2.8. skills/02_inspect_triage/SKILL.md

```markdown
# Skill: Problem Inspection & Triage

**Goal:** Decide if the agent should immediately begin strategizing or if it must study literature first.

**Instructions:**
1. Review `artifacts/01_problem_formalization.md`.
2. Assess complexity: Is this a standard textbook problem, or does it invoke advanced, highly specific machinery (e.g., specific theorems from recent literature)?
3. **Decision:** 
   - Return `DIRECT_PROOF` if the hypotheses and goal use standard definitions that can be manipulated directly.
   - Return `SOURCE_STUDY` if the problem requires adapting a complex known theorem. Suggest keywords or specific papers to search.

```

### 2.9. skills/03_source_study/SKILL.md

```markdown
# Skill: Source Material Analysis

**Goal:** Dissect relevant mathematical literature to extract techniques. Write findings to `artifacts/02_literature_review.md`.

**Instructions:**
For each provided proof or theorem snippet:
1. **Structural Mapping:** Map which original hypothesis is used to justify which line in the proof.
2. **Hypothesis Stress-Testing:** Identify what specifically breaks in the proof if a key hypothesis is dropped.
3. **Generalization:** Can the hypotheses be weakened? (e.g., from compact to locally compact).
4. **Aha! Moment:** Distill the core trick of the paper into 1-3 sentences.

```

### 2.10. skills/07_metacognition/SKILL.md

```markdown
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

```

### 2.11. skills/06_verify/schema_informal.json

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "InformalVerification",
  "type": "object",
  "properties": {
    "is_sound": { "type": "boolean" },
    "flaws_found": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "potential_flaw": { "type": "string" },
          "severity": { "type": "string", "enum": ["minor", "major", "fatal"] },
          "recommendation": { "type": "string" }
        },
        "required": ["potential_flaw", "severity"]
      }
    },
    "sanity_check_passed": { "type": "boolean" }
  },
  "required": ["is_sound", "sanity_check_passed"]
}

```

### 2.12. skills/06_verify/schema_lean.json

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "LeanVerification",
  "type": "object",
  "properties": {
    "lean_code": { 
      "type": "string", 
      "description": "The generated Lean 4 code block using declarative style." 
    },
    "compiler_status": { 
      "type": "string", 
      "enum": ["success", "error", "not_run"] 
    },
    "error_analysis": { 
      "type": "string" 
    },
    "is_sound": { 
      "type": "boolean" 
    }
  },
  "required": ["lean_code", "compiler_status", "is_sound"]
}

```

### 2.13. skills/06_verify/lean_boilerplate.lean

```lean
import Mathlib

/-!
# Verification Boilerplate
This file contains specific definitional preferences and imports.
Always use declarative proof structures (`have`, `show`) rather than imperative tactics where possible.
-/

-- Specific definition preference for Even numbers
def MyEven (n : ℕ) : Prop := ∃ r, n = r + r

```

### 2.14. skills/01_deconstruct/schema.json

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ProblemFormalization",
  "type": "object",
  "properties": {
    "givens": { "type": "array", "items": { "type": "string" } },
    "hypotheses": { "type": "array", "items": { "type": "string" } },
    "goal": { "type": "string" },
    "problem_type": { "type": "string" },
    "definition_dictionary": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "term": { "type": "string" },
          "definition": { "type": "string" }
        }
      }
    },
    "intuitive_summary": { "type": "string" }
  },
  "required": ["givens", "hypotheses", "goal", "definition_dictionary"]
}

```

---

## 3. Implementation Instructions for the Agent

1. **Initialize Folders:** Create all directories listed in the structure.
2. **Generate Skills:** For each skill folder, create the `SKILL.md` file as defined.
3. **Create Schemas:** Create simple `.json` schemas for each skill to ensure the Orchestrator receives structured data.
4. **Boilerplate:** In `skills/06_verify/lean_boilerplate.lean`, add standard imports (e.g., `import Mathlib.Tactic`) and the user's specific mathematical definitions.
5. **Verification:** Once created, verify that `loop-orchestrator.md` correctly references the folder-based paths.

**End of Specification.**
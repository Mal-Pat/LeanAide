### The Best Way to Integrate: A "Registry" Approach

As you add specialized mathematical machinery (Bochner technique, invariants, etc.), you shouldn't just dump them into the general `skills/` folder. Instead, you should implement a **Hierarchical Skill Selection** system.

Instead of the `Strategy Generation` skill trying to know everything, it acts as a **Dispatcher**.

1. **The Technique Library:** Create a new directory `skills/techniques/`. Each sub-folder (e.g., `skills/techniques/bochner_technique/`) contains a `SKILL.md` and a `manifest.json` describing when to use it.
2. **The Registry:** Create a file `skills/strategy_gen/technique_registry.json`. This contains a mapping of "Mathematical Context" to "Technique Skill."

#### Updated `skills/strategy_gen/SKILL.md` Logic:

> "Analyze the problem deconstruction. Scan `skills/techniques/` for any skill whose manifest matches our problem context (e.g., if the problem involves Riemannian manifolds and curvature, select the `bochner_technique` skill). If a match is found, invoke that specific skill to help generate Plan A or B."

---

### Will too many skills cause regressions?

The short answer is **No, provided you maintain "Domain Isolation."**

Here is the breakdown of why this works and where the risks lie:

#### 1. The Benefit of Precise Descriptions

Unlike a single massive prompt (where every new instruction competes for attention and "dilutes" the others), a folder-based skill architecture uses **Explicit Invocation**. The agent only reads the "Bochner Technique" instructions when it is actually at that step of the loop.

* **Precision:** If the `SKILL.md` for Bochner is hyper-specific to Laplacian-on-forms and curvature, it won't "pollute" the agent's logic when it's doing basic group theory.

#### 2. The Risk of "Model Drift"

The only real regression occurs if the **Dispatcher** (the Strategy Gen skill) becomes overwhelmed. If there are 500 techniques, the LLM might struggle to pick the right one.

* **Fix:** Use a **Multi-Level Dispatcher**. Group techniques by field (e.g., `techniques/geometry/`, `techniques/algebra/`). The agent first picks the field, then the sub-field, then the specific technique.

#### 3. Standardizing the "Interface"

To prevent regressions, every specialized skill must follow a strict **Input/Output contract**.

* **Input:** Always `artifacts/01_problem_formalization.md`.
* **Output:** Must be a "Strategy Fragment" that the main `strategy_gen` skill can stitch into the final `artifacts/03_strategy_plans.md`.

---

### Suggested Directory Modification for Specialized Skills

Update your structure to look like this:

```text
skills/
├── strategy_gen/
│   ├── SKILL.md            # The Dispatcher
│   └── registry.md         # A list of available advanced techniques
└── techniques/
    ├── invariant_construction/
    │   ├── SKILL.md
    │   └── manifest.json   # Keywords: [combinatorics, group actions, knot theory]
    ├── bochner_technique/
    │   ├── SKILL.md
    │   └── manifest.json   # Keywords: [differential geometry, manifolds, curvature]
    └── generic_point/
        ├── SKILL.md
        └── manifest.json   # Keywords: [algebraic geometry, scheme theory]

```

### Integration Guidelines for your coding agent:

* **Precise Guardrails:** In each `techniques/*/SKILL.md`, start with a "Pre-condition" block: *"Do not apply this skill unless the problem involves [X]. If unsure, return 'NOT_APPLICABLE'."*
* **Staged Loading:** Teach the Orchestrator to only load the "Toolbox" (specialized skills) *after* Phase 1 is complete. This keeps the early "Deconstruction" phase clean and fast.

This approach mimics a mathematician walking through a library: you don't carry every book at once; you identify the subject matter first, then go to the specific shelf for the advanced tools.

**Would you like me to draft a `manifest.json` template for these specialized techniques?**
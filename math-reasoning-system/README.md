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

**Objective Modes:**
- `PROBLEM_SOLVING`: Prove a well-stated theorem or solve a fixed problem.
- `EXPLORATORY_RESEARCH`: Extend results, formulate questions, generate conjectures, and map promising directions.
- `AUTO`: Use problem solving when a precise target theorem is present; otherwise use exploratory research.

## Quick Start
1. Open your agentic CLI in this directory.
2. Provide the problem and set the modes.
3. Prompt: "Read `loop-orchestrator.md`. Problem: [LaTeX]. Mode: [AUTONOMOUS/WITH_LEAN/AUTO]. Start."

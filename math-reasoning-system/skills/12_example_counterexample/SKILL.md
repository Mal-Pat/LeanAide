# Skill: Example and Counterexample Construction

**Goal:** Construct useful examples, test examples, boundary cases, and counterexamples that clarify a problem, stress-test a conjecture, or guide a proof strategy.

**Scope:** This skill supports both `PROBLEM_SOLVING` and `EXPLORATORY_RESEARCH`.
Examples are evidence and diagnostic tools. They do not prove universal claims
unless the domain has been reduced to a finite exhaustive list and exhaustion is
explicitly justified.

**Instructions:**
1. **Classify the Target:**
   - theorem sanity check;
   - conjecture testing;
   - hypothesis necessity;
   - boundary/degenerate case;
   - model/example for definitions;
   - counterexample search.
2. **Extract Constraints:** List the hypotheses that examples must satisfy and the conclusion or behavior to test.
3. **Choose Construction Families:**
   - Small finite objects: sets of size `0, 1, 2, 3`, finite groups, small graphs, small categories.
   - Degenerate objects: empty set, zero object, identity map, constant function, discrete/indiscrete topology.
   - Extremal objects: maximal/minimal examples, equality cases, sharpness examples.
   - Standard pathological objects: non-Hausdorff spaces, non-Noetherian rings, nonmeasurable sets, discontinuous functions, singular spaces.
   - Free or universal examples: free groups, polynomial rings, quotient objects, products/coproducts.
4. **Compute Explicitly:** Verify each hypothesis and conclusion directly. For candidate counterexamples, state exactly which hypothesis holds and which conclusion fails.
5. **Compare Variants:** If no counterexample appears, try weakening one hypothesis at a time.
6. **Record Outcome:** Label each constructed object as:
   - `supporting_example`;
   - `counterexample`;
   - `boundary_case`;
   - `sharpness_example`;
   - `inconclusive_test`.
7. **Feed Back Into Workflow:**
   - In proof mode, a valid counterexample should stop the proof attempt and trigger a correction or failure report.
   - In research mode, examples and counterexamples should update conjectures, hypotheses, and next probes.

**Output:** Save to `artifacts/02_examples.md` for early examples or append to `artifacts/04_research_trace.md` / `artifacts/04_execution_trace.md` when used inside a loop. If structured output is requested, use `schema.json`.

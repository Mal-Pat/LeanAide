# Codegen TODO for `mathdoc_agent`

This note compares the compact JSON emitted by `mathdoc_agent` with the
handlers currently available through `LeanAide/PaperCodes.lean` and
`LeanAideCore/LeanAideCore/PaperCodes.lean`.

The Python exporter should continue to emit PaperStructure-style objects with a
`type` field. Lean dispatches through `type`, so generated JSON should not use
`kind` in saved outputs.

## Currently Matched Structures

These structures are already supported by Lean codegen and are emitted with
matching field names.

### `document`

- `body`: array of document nodes.
- `title`: optional metadata, currently ignored by Lean codegen.

### `Theorem`

- `claim`: theorem statement translated by Lean.
- `hypothesis`: optional array of hypotheses.
- `proof`: optional proof object.
- `label`: optional theorem label.
- `header`, `id`, `status`: metadata, currently ignored by Lean codegen.

### `Proof`

- `proof_steps`: array of proof steps.
- `claim_label`: optional label used when generating standalone command
  sequences.

### `assert_statement`

- `claim`: asserted proposition.
- `proof_method`: optional metadata, currently ignored by Lean codegen.
- `results_used`: optional references, currently ignored by Lean codegen.

### `calculation`

- `inline_calculation`: single calculation string, or
- `calculation_sequence`: array of calculation strings.

### `induction_proof`

- `on`: induction variable or expression.
- `prev_var`: optional previous variable name.
- `base_case_proof`: proof object for the base case.
- `induction_step_proof`: proof object for the induction step.

### `multi-condition_cases_proof`

- `proof_cases`: array of case objects.
- Each case has:
  - `condition`: case condition.
  - `proof`: proof object for that case.
- `exhaustiveness`: optional proof of case coverage. The Python exporter
  currently omits this unless it has a formal proof object; prose text here is
  not useful to Lean.

### `bi-implication_cases_proof`

- `if_proof`: forward implication proof.
- `only_if_proof`: reverse implication proof.

### `contradiction_statement`

- `assumption`: assumption to contradict.
- `proof`: proof object deriving the contradiction.

The Python exporter now emits `proof` here as a `Proof` object with
`proof_steps`, not as a raw array.

## Python Field Adjustments Already Made

- Contradiction proofs now use `proof : { type := "Proof", proof_steps := ... }`.
- Case proofs no longer emit prose-only `exhaustiveness`.
- Theorem nodes emit `claim`, not `statement`.
- Proof nodes do not repeat the theorem statement inside the proof.
- Saved JSON examples use `type`; `kind` is only used internally in Python.

## Lean Field Mismatches To Watch

### `general_induction_proof`

Lean's schema comment mentions `induction_hypotheses`, but the implementation
reads `induction_hyps` inside each case.

Recommended Lean-side fix: accept both names, with `induction_hyps` as the
current compatibility spelling.

Case fields:

- `condition`: case condition.
- `proof`: proof object.
- `induction_hyps` or `induction_hypotheses`: induction hypotheses.

### `bi-implication_cases_proof`

The schema comment mentions `antecedent` and `consequent`, but the codegen
implementation only requires `if_proof` and `only_if_proof`.

Recommended action: keep Python as-is unless Lean codegen starts using the
extra fields.

## New `@[codegen]` Handlers Needed

The following proof types are generated or recognized by `mathdoc_agent` but
currently degrade to generic `Proof` or `assert_statement` structures when Lean
does not have a dedicated handler. Dedicated handlers would preserve proof
intent and produce better Lean tactics.

### `contrapositive_proof`

JSON type to match: `contrapositive_proof`.

Fields:

- `assumption`: negated conclusion or contrapositive assumption.
- `proof`: proof deriving the negated hypothesis.
- `conclusion`: optional final contrapositive conclusion.

Expected Lean behavior: introduce the contrapositive assumption, derive the
negated hypothesis, and close using the contrapositive form of the theorem.

### `existence_proof`

JSON type to match: `existence_proof`.

Fields:

- `witness`: constructed witness.
- `proof`: verification that the witness satisfies the predicate.
- `claim`: optional existential claim.

Expected Lean behavior: use the witness, then generate tactics for the
verification proof.

### `uniqueness_proof`

JSON type to match: `uniqueness_proof`.

Fields:

- `existence_proof`: proof that at least one object exists.
- `uniqueness_proof`: proof that any two candidates are equal.
- `candidate_variables`: optional names for arbitrary candidates.
- `claim`: optional uniqueness or `exists unique` statement.

Expected Lean behavior: split existence and uniqueness goals, then prove the
equality of arbitrary candidates.

### `construction_proof`

JSON type to match: `construction_proof`.

Fields:

- `construction`: constructed object or definition.
- `verification`: proof that the construction has the required property.
- `claim`: optional target statement.

Expected Lean behavior: define or refine the constructed object, then discharge
the verification goals.

### `generic_element_proof`

JSON type to match: `generic_element_proof`.

Fields:

- `element`: arbitrary element introduced for the proof.
- `target_relation`: relation being proved, such as set equality or inclusion.
- `proof`: proof for the arbitrary element.
- `direction_proofs`: optional directional proofs for equality-style goals.

Expected Lean behavior: use extensionality or inclusion introduction, introduce
the generic element, and generate the elementwise proof.

### `epsilon_delta_proof`

JSON type to match: `epsilon_delta_proof`.

Fields:

- `epsilon_var`: epsilon variable name.
- `epsilon_positive`: positivity hypothesis for epsilon.
- `delta`: chosen delta expression.
- `delta_positive_proof`: proof that delta is positive.
- `bound_proof`: proof of the required bound.

Expected Lean behavior: introduce epsilon and its positivity hypothesis, use
the proposed delta, prove positivity, then prove the implication/bound.

### `invariant_proof`

JSON type to match: `invariant_proof`.

Fields:

- `invariant`: invariant predicate.
- `initial_proof`: proof that the invariant holds initially.
- `preservation_proof`: proof that every step preserves the invariant.
- `conclusion`: result obtained from the invariant.

Expected Lean behavior: prove initialization and preservation, then apply the
invariant to the target state.

### `reduction_proof`

JSON type to match: `reduction_proof`.

Fields:

- `reduced_to`: target result or previously proved theorem.
- `reduction_steps`: steps reducing the current claim to the known result.
- `result_used`: optional named theorem/result.
- `proof`: optional proof object for the reduced goal.

Expected Lean behavior: transform the goal through the reduction steps and
apply the known result.

### `counting_proof`

JSON type to match: `counting_proof`.

Fields:

- `counted_object`: finite type, set, or combinatorial object being counted.
- `first_count`: first counting argument.
- `second_count`: second counting argument.
- `equality_proof`: proof that the two counts are equal.

Expected Lean behavior: produce a finite-cardinality equality from two
cardinality computations.

### `pigeonhole_proof`

JSON type to match: `pigeonhole_proof`.

Fields:

- `objects`: objects being assigned.
- `boxes`: boxes or target classes.
- `assignment`: map from objects to boxes.
- `cardinality_proof`: proof that there are more objects than boxes.
- `conclusion`: collision or repeated-box conclusion.

Expected Lean behavior: apply an appropriate finite pigeonhole theorem.

### `minimal_counterexample_proof`

JSON type to match: `minimal_counterexample_proof`.

Fields:

- `counterexample_property`: property defining counterexamples.
- `minimal_element`: chosen minimal counterexample.
- `minimality_proof`: proof of minimality.
- `contradiction_proof`: proof contradicting minimality or counterexamplehood.

Expected Lean behavior: obtain a minimal counterexample by well-foundedness,
then derive a contradiction.

### `infinite_descent_proof`

JSON type to match: `infinite_descent_proof`.

Fields:

- `initial_counterexample`: starting counterexample.
- `descent_step`: construction of a smaller counterexample.
- `well_founded_relation`: relation used for descent.
- `contradiction_proof`: final contradiction from well-foundedness.

Expected Lean behavior: use well-founded descent or `Nat` minimality to rule
out the initial counterexample.

### `compactness_proof`

JSON type to match: `compactness_proof`.

Fields:

- `cover_or_family`: open cover or closed family.
- `finite_subcover_proof`: proof extracting a finite subcover/subfamily.
- `local_proof`: optional proof on finite data.
- `conclusion`: target compactness consequence.

Expected Lean behavior: apply the compactness theorem and pass to finite data.

### `density_proof`

JSON type to match: `density_proof`.

Fields:

- `dense_subset`: subset known or proved dense.
- `dense_proof`: proof of density.
- `extension_or_limit_step`: proof transferring the result by density.
- `conclusion`: target conclusion.

Expected Lean behavior: apply density or closure lemmas, then close by
continuity/order/topological transfer.

### `approximation_proof`

JSON type to match: `approximation_proof`.

Fields:

- `approximants`: approximating sequence, net, or family.
- `approximation_error`: bound or convergence statement.
- `limit_passage`: proof passing to the limit.
- `conclusion`: target result.

Expected Lean behavior: introduce approximants, prove estimates, and use a
limit theorem.

### `universal_property_proof`

JSON type to match: `universal_property_proof`.

Fields:

- `universal_property`: property being invoked.
- `existence_part`: proof constructing the comparison map/object.
- `uniqueness_part`: proof of uniqueness.
- `comparison_map`: optional explicit map.

Expected Lean behavior: use the universal property constructor or eliminator,
then prove existence and uniqueness subgoals.

### `algorithmic_proof`

JSON type to match: `algorithmic_proof`.

Fields:

- `algorithm`: algorithm or recursive procedure.
- `termination_proof`: proof of termination.
- `partial_correctness_proof`: proof that the result is correct if returned.
- `conclusion`: target correctness theorem.

Expected Lean behavior: define/refine the algorithm, prove termination, then
prove correctness.

### `probabilistic_proof`

JSON type to match: `probabilistic_proof`.

Fields:

- `probability_space`: probability space or measure context.
- `bad_event_bound`: bound on undesirable events.
- `positive_probability_proof`: proof that a good event has positive
  probability.
- `witness_conclusion`: deterministic existence conclusion.

Expected Lean behavior: prove the probability bound and extract existence from
positive probability.

### `local_to_global_proof`

JSON type to match: `local_to_global_proof`.

Fields:

- `cover`: local cover or localization data.
- `local_proofs`: proofs on each local piece.
- `compatibility_proof`: proof that local data agree on overlaps.
- `gluing_step`: construction of the global object/proof.

Expected Lean behavior: use a gluing or sheaf-style theorem after local and
compatibility goals are solved.

### `diagram_chase_proof`

JSON type to match: `diagram_chase_proof`.

Fields:

- `diagram`: named diagram or maps.
- `start_element`: element introduced at the start of the chase.
- `map_steps`: sequence of element images or preimages.
- `exactness_or_commutativity_uses`: facts used in the chase.
- `conclusion`: final element relation.

Expected Lean behavior: introduce elements, rewrite by commutativity, and use
exactness lemmas.

### `maximal_minimal_proof`

JSON type to match: `maximal_minimal_proof`.

Fields:

- `object`: extremal object.
- `ordering`: relation used for maximality/minimality.
- `extremal_property`: proof that the object is extremal.
- `improvement_contradiction`: proof that any improvement contradicts
  extremality.

Expected Lean behavior: choose an extremal object, assume an improving object,
and contradict maximality/minimality.

### `genericity_ae_proof`

JSON type to match: `genericity_ae_proof`.

Fields:

- `bad_set`: exceptional set.
- `smallness_proof`: proof the bad set is meagre/null/finite.
- `generic_condition`: condition holding outside the bad set.
- `conclusion`: almost-everywhere or generic conclusion.

Expected Lean behavior: prove smallness of the exceptional set, then apply the
corresponding almost-everywhere or genericity theorem.

### `diagrammatic_geometric_proof`

JSON type to match: `diagrammatic_geometric_proof`.

Fields:

- `configuration`: geometric objects and incidence data.
- `construction_steps`: auxiliary points, lines, or maps.
- `geometric_facts`: lemmas used in the diagrammatic argument.
- `conclusion`: target geometric statement.

Expected Lean behavior: introduce the configuration, construct auxiliaries, and
apply geometric lemmas to close the conclusion.

## Recommended Order

1. Add `contrapositive_proof`, `existence_proof`, `generic_element_proof`, and
   `epsilon_delta_proof`; these appear in the current example corpus and are
   the most useful next targets.
2. Add `uniqueness_proof`, `construction_proof`, `invariant_proof`, and
   `reduction_proof`; these are common enough to justify specialized
   generation.
3. Keep less common proof types degrading to supported core structures until
   there are examples that require more precise Lean behavior.

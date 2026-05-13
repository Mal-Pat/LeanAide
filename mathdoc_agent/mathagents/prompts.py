DOCUMENT_PARSER_INSTRUCTIONS = """
Decompose mathematical document text into a structured document tree.
Preserve the author's structure and do not invent mathematical content.
Classify sections, definitions, structure-definition items, instance-definition
items, inductive-type-definition items, theorem-like statements, proofs,
remarks, examples, and paragraphs. If unsure, use kind='unknown' and add a note.
Use kind='paragraph' only for genuinely non-mathematical prose, such as
motivation, exposition, history, transitions, or commentary that makes no
mathematical assertion and introduces no mathematical object. Any paragraph
containing mathematical content must be classified as a mathematical node:
definition, structure-definition, instance-definition,
inductive-type-definition, theorem/lemma/proposition/corollary/local_claim,
calculation_block, proof, example, remark, or unknown. Do not put mathematical
definitions, claims, constructions, hypotheses, examples, equations, or
properties in JSON type "Paragraph".
For theorem-like children, put the mathematical claim in the `statement` field.
If a proof immediately follows a theorem-like statement, attach the proof text
to that theorem-like child in `proof_text`. Do not emit the proof as a separate
paragraph. A text beginning with "Proof." or "Proof:" is never a paragraph.
For structure-definition children, set `name`, `is_class`, parameters, extends,
and fields. Use `is_class=true` for class-like structures such as groups.
For instance-definition children, set `class_name`, `target`, optional `name`,
parameters, fields, and value when present.
For inductive-type-definition children, set `name`, `is_prop`, parameters, and
constructors. Each constructor should include its name, when stated, and its
arguments.
Use `data_entries` only for small string metadata as key/value pairs.
"""

PROOF_CLASSIFIER_INSTRUCTIONS = """
Classify one proof fragment by its outermost proof structure.
Do not deeply refine the proof. If unsure, use kind='unknown' and explain why.
"""

INDUCTION_INSTRUCTIONS = """
Refine one induction proof fragment. Extract the induction variable, principle,
induction hypotheses, base cases, step cases, and child proof fragments.
Do not deeply refine child proofs or invent missing arguments.
"""

CASES_INSTRUCTIONS = """
Refine one case split proof fragment. Extract what is split on, the cases, case
assumptions, and an exhaustiveness reason when stated. Do not invent missing cases.
"""

SIMPLE_PROOF_INSTRUCTIONS = """
Refine a simple proof fragment by extracting method, hints, referenced lemmas,
referenced hypotheses, intermediate proof steps, and unresolved details. Do not
collapse a multi-sentence proof into a single assertion. Preserve each explicit
mathematical step as a `proof_steps` entry:
- use `let_statement` for introduced objects;
- use `assume_statement` for fixed arbitrary variables or assumptions;
- use `assert_statement` for equations, inequalities, derived claims, and final
  conclusions, with `proof_method` explaining the local justification.
Do not expand omitted arguments, but do keep all intermediate equations and
algebraic rewrites that are present in the source text.
"""

CALCULATION_INSTRUCTIONS = """
Refine a calculational proof fragment into calculation steps with lhs, relation,
rhs, justification, and side conditions. Do not invent omitted steps.
"""

STRUCTURED_PROOF_INSTRUCTIONS = """
Refine one proof fragment whose proof kind is supplied in the input.

Extract only the main logical components needed by that proof kind. Examples:
- contradiction: negated assumption and derivation of contradiction;
- contrapositive: assumption of the negated conclusion and proof of negated hypothesis;
- existence/construction: witness or construction and verification;
- uniqueness: existence part and uniqueness part;
- equivalence: one child per implication direction;
- reduction: current claim, reduced goal, proof of the reduction, and proof of
  the reduced goal;
- invariant: invariant definition, preservation proof, contradiction/conclusion;
- epsilon-delta: epsilon choice, delta choice, verification;
- generic element: arbitrary element setup and inclusion/member proof.

Do not deeply refine child proofs. Use child proof specs for components and mark
unresolved details when the source omits essential information. Use `metadata`
only for small string metadata as key/value pairs.
"""

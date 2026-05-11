DOCUMENT_PARSER_INSTRUCTIONS = """
Decompose mathematical document text into a structured document tree.
Preserve the author's structure and do not invent mathematical content.
Classify sections, definitions, theorem-like statements, proofs, remarks,
examples, and paragraphs. If unsure, use kind='unknown' and add a note.
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
referenced hypotheses, and unresolved details. Do not expand omitted arguments.
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
- reduction: target statement reduced to a known result or easier subgoal;
- invariant: invariant definition, preservation proof, contradiction/conclusion;
- epsilon-delta: epsilon choice, delta choice, verification;
- generic element: arbitrary element setup and inclusion/member proof.

Do not deeply refine child proofs. Use child proof specs for components and mark
unresolved details when the source omits essential information.
"""

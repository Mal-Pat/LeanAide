from __future__ import annotations

from enum import Enum


class NodeStatus(str, Enum):
    raw = "raw"
    classified = "classified"
    decomposed = "decomposed"
    locally_refined = "locally_refined"
    validated = "validated"
    resolved = "resolved"
    opaque = "opaque"


class DocumentKind(str, Enum):
    unknown = "unknown"
    document = "document"
    section = "section"
    subsection = "subsection"
    paragraph = "paragraph"
    definition = "definition"
    theorem = "theorem"
    lemma = "lemma"
    proposition = "proposition"
    corollary = "corollary"
    example = "example"
    remark = "remark"
    proof = "proof"
    local_claim = "local_claim"
    calculation_block = "calculation_block"
    opaque = "opaque"


class ProofKind(str, Enum):
    unknown = "unknown"
    simple = "simple"
    calculation = "calculation"
    cases = "cases"
    induction = "induction"
    contradiction = "contradiction"
    contrapositive = "contrapositive"
    extensionality = "extensionality"
    existence = "existence"
    uniqueness = "uniqueness"
    equivalence = "equivalence"
    local_claim = "local_claim"
    theorem_application = "theorem_application"
    definition_unfolding = "definition_unfolding"
    opaque = "opaque"

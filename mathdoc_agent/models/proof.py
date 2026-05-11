from __future__ import annotations

from typing import Any, Optional, Union

from pydantic import BaseModel, Field, computed_field

from mathdoc_agent.models.base import NodeStatus, ProofKind
from mathdoc_agent.models.references import Reference


class ProofNode(BaseModel):
    id: str
    kind: Union[ProofKind, str] = ProofKind.unknown
    status: NodeStatus = NodeStatus.raw

    text: str
    goal: Optional[str] = None
    hypotheses: list[str] = Field(default_factory=list)

    children: list["ProofNode"] = Field(default_factory=list)
    data: dict[str, Any] = Field(default_factory=dict)
    references: list[Reference] = Field(default_factory=list)

    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    notes: list[str] = Field(default_factory=list)
    unresolved_details: list[str] = Field(default_factory=list)

    @computed_field(return_type=str)
    @property
    def type(self) -> str:
        kind = self.kind.value if hasattr(self.kind, "value") else str(self.kind)
        return {
            ProofKind.unknown.value: "Proof",
            ProofKind.simple.value: "assert_statement",
            ProofKind.calculation.value: "calculation",
            ProofKind.cases.value: "multi-condition_cases_proof",
            ProofKind.induction.value: "induction_proof",
            ProofKind.contradiction.value: "contradiction_statement",
            ProofKind.contrapositive.value: "Proof",
            ProofKind.extensionality.value: "Proof",
            ProofKind.existence.value: "Proof",
            ProofKind.uniqueness.value: "Proof",
            ProofKind.equivalence.value: "bi-implication_cases_proof",
            ProofKind.local_claim.value: "Theorem",
            ProofKind.theorem_application.value: "assert_statement",
            ProofKind.definition_unfolding.value: "assert_statement",
            ProofKind.opaque.value: "opaque",
        }.get(kind, kind)


class ProofTree(BaseModel):
    id: str
    theorem_statement: Optional[str] = None
    root: ProofNode

    @computed_field(return_type=str)
    @property
    def type(self) -> str:
        return "ProofDetails"


ProofNode.model_rebuild()

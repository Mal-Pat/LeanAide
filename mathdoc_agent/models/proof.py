from __future__ import annotations

from typing import Any, Optional, Union

from pydantic import BaseModel, Field

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


class ProofTree(BaseModel):
    id: str
    theorem_statement: Optional[str] = None
    root: ProofNode


ProofNode.model_rebuild()

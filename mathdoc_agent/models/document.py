from __future__ import annotations

from typing import Any, Optional, Union

from pydantic import BaseModel, Field

from mathdoc_agent.models.base import DocumentKind, NodeStatus
from mathdoc_agent.models.proof import ProofTree
from mathdoc_agent.models.references import Reference
from mathdoc_agent.models.runs import AgentRunRecord


class DocumentNode(BaseModel):
    id: str
    kind: Union[DocumentKind, str] = DocumentKind.unknown
    status: NodeStatus = NodeStatus.raw

    title: Optional[str] = None
    label: Optional[str] = None
    text: str = ""

    children: list["DocumentNode"] = Field(default_factory=list)
    proof: Optional[ProofTree] = None
    data: dict[str, Any] = Field(default_factory=dict)
    references: list[Reference] = Field(default_factory=list)

    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    notes: list[str] = Field(default_factory=list)
    unresolved_details: list[str] = Field(default_factory=list)


class MathDocument(BaseModel):
    id: str
    title: Optional[str] = None
    root: DocumentNode
    run_log: list[AgentRunRecord] = Field(default_factory=list)


DocumentNode.model_rebuild()

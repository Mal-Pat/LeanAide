from __future__ import annotations

from pydantic import BaseModel

from mathdoc_agent.models.proof import ProofNode
from mathdoc_agent.models.validation import ValidationIssue
from mathdoc_agent.orchestration.context import ProofContext


class RepairRequest(BaseModel):
    old_node: ProofNode
    candidate: ProofNode
    context: ProofContext
    issues: list[ValidationIssue]


class RepairSpec(BaseModel):
    replacement: ProofNode
    explanation: str

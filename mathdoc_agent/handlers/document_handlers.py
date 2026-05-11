from __future__ import annotations

from mathdoc_agent.agents.runner import run_agent_typed
from mathdoc_agent.handlers.base import DocumentRefinementHandler
from mathdoc_agent.models.base import DocumentKind, NodeStatus, ProofKind
from mathdoc_agent.models.document import DocumentNode
from mathdoc_agent.models.proof import ProofNode, ProofTree
from mathdoc_agent.models.refinement_specs import DocumentRefinementSpec
from mathdoc_agent.models.validation import ValidationIssue, ValidationReport
from mathdoc_agent.orchestration.context import DocumentContext
from mathdoc_agent.orchestration.worklist import kind_key


class UnknownDocumentHandler(DocumentRefinementHandler[DocumentRefinementSpec]):
    kind = DocumentKind.unknown.value
    output_model = DocumentRefinementSpec

    def __init__(self, agent) -> None:
        self.agent = agent

    async def refine(self, node: DocumentNode, context: DocumentContext) -> DocumentNode:
        spec = await run_agent_typed(
            self.agent,
            {
                "node": node.model_dump(),
                "context": context.model_dump(),
                "task": "Decompose this mathematical document node into local child nodes.",
            },
            DocumentRefinementSpec,
        )
        children: list[DocumentNode] = []
        for child in spec.children:
            child_id = f"{node.id}.{child.id_suffix}"
            proof = None
            if child.proof_text:
                statement = str(child.data.get("statement") or child.text)
                proof = ProofTree(
                    id=f"{child_id}.proof",
                    theorem_statement=statement,
                    root=ProofNode(
                        id=f"{child_id}.proof.root",
                        kind=ProofKind.unknown,
                        status=NodeStatus.raw,
                        text=child.proof_text,
                        goal=statement,
                    ),
                )
            children.append(
                DocumentNode(
                    id=child_id,
                    kind=child.kind,
                    status=NodeStatus.decomposed if proof else NodeStatus.classified,
                    title=child.title,
                    label=child.label,
                    text=child.text,
                    data=child.data,
                    proof=proof,
                    notes=child.notes,
                )
            )
        return node.model_copy(
            update={
                "status": NodeStatus.decomposed,
                "children": children,
                "notes": node.notes + spec.notes,
            }
        )

    def validate(self, node: DocumentNode, context: DocumentContext) -> ValidationReport:
        issues: list[ValidationIssue] = []
        if not node.children:
            issues.append(ValidationIssue(severity="warning", path="children", message="Document node has no children after refinement."))
        return ValidationReport(ok=True, issues=issues)

    def is_resolved(self, node: DocumentNode, context: DocumentContext) -> bool:
        return bool(node.children) and all(
            child.status in {NodeStatus.resolved, NodeStatus.opaque, NodeStatus.classified}
            for child in node.children
        )


class PassthroughDocumentHandler(DocumentRefinementHandler[None]):
    def __init__(self, kind: DocumentKind | str) -> None:
        self.kind = kind_key(kind)

    async def refine(self, node: DocumentNode, context: DocumentContext) -> DocumentNode:
        return node.model_copy(update={"status": NodeStatus.resolved})

    def is_resolved(self, node: DocumentNode, context: DocumentContext) -> bool:
        return not node.children and node.proof is None

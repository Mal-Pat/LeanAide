from __future__ import annotations

from mathdoc_agent.models.base import DocumentKind, NodeStatus, ProofKind
from mathdoc_agent.models.document import DocumentNode
from mathdoc_agent.models.payloads import DefinitionData, StatementData
from mathdoc_agent.models.proof import ProofNode, ProofTree


class DocumentBuilder:
    @staticmethod
    def theorem_like(
        *,
        id: str,
        kind: DocumentKind,
        text: str,
        statement: str,
        proof_text: str | None = None,
        label: str | None = None,
        assumptions: list[str] | None = None,
        conclusion: str | None = None,
    ) -> DocumentNode:
        proof = None
        if proof_text:
            proof = ProofTree(
                id=f"{id}.proof",
                theorem_statement=statement,
                root=ProofNode(
                    id=f"{id}.proof.root",
                    kind=ProofKind.unknown,
                    status=NodeStatus.raw,
                    text=proof_text,
                    goal=statement,
                ),
            )
        return DocumentNode(
            id=id,
            kind=kind,
            status=NodeStatus.decomposed if proof else NodeStatus.classified,
            label=label,
            text=text,
            data=StatementData(
                statement=statement,
                assumptions=assumptions or [],
                conclusion=conclusion,
            ).model_dump(),
            proof=proof,
        )

    @staticmethod
    def definition(
        *,
        id: str,
        text: str,
        term: str | None = None,
        definiens: str | None = None,
        notation: str | None = None,
        label: str | None = None,
    ) -> DocumentNode:
        return DocumentNode(
            id=id,
            kind=DocumentKind.definition,
            status=NodeStatus.classified,
            label=label,
            text=text,
            data=DefinitionData(term=term, definiens=definiens, notation=notation).model_dump(),
        )

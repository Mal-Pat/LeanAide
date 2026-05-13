from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from mathdoc_agent.models.document import DocumentNode
from mathdoc_agent.models.proof import ProofNode
from mathdoc_agent.models.validation import ValidationReport
from mathdoc_agent.orchestration.context import DocumentContext, ProofContext

SpecT = TypeVar("SpecT")


class ProofRefinementHandler(ABC, Generic[SpecT]):
    kind: str
    output_model: type[SpecT] | None = None

    @abstractmethod
    async def refine(self, node: ProofNode, context: ProofContext) -> ProofNode:
        ...

    def validate(self, node: ProofNode, context: ProofContext) -> ValidationReport:
        return ValidationReport.ok_report()

    def is_resolved(self, node: ProofNode, context: ProofContext) -> bool:
        return False

    def child_context(
        self,
        parent: ProofNode,
        child: ProofNode,
        context: ProofContext,
    ) -> ProofContext:
        return context


class DocumentRefinementHandler(ABC, Generic[SpecT]):
    kind: str
    output_model: type[SpecT] | None = None

    @abstractmethod
    async def refine(self, node: DocumentNode, context: DocumentContext) -> DocumentNode:
        ...

    def validate(self, node: DocumentNode, context: DocumentContext) -> ValidationReport:
        return ValidationReport.ok_report()

    def is_resolved(self, node: DocumentNode, context: DocumentContext) -> bool:
        return False

    def child_context(
        self,
        parent: DocumentNode,
        child: DocumentNode,
        context: DocumentContext,
    ) -> DocumentContext:
        return context

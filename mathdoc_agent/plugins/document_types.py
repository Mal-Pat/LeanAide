from __future__ import annotations

from mathdoc_agent.agents import definitions
from mathdoc_agent.handlers.document_handlers import PassthroughDocumentHandler, UnknownDocumentHandler
from mathdoc_agent.models.base import DocumentKind
from mathdoc_agent.registries.document_handlers import DocumentHandlerRegistry


def default_document_handler_registry(
    *,
    parser_agent=definitions.document_parser_agent,
) -> DocumentHandlerRegistry:
    registry = DocumentHandlerRegistry()
    registry.register(DocumentKind.unknown.value, UnknownDocumentHandler(parser_agent))
    for kind in (
        DocumentKind.document,
        DocumentKind.section,
        DocumentKind.subsection,
        DocumentKind.paragraph,
        DocumentKind.definition,
        DocumentKind.theorem,
        DocumentKind.lemma,
        DocumentKind.proposition,
        DocumentKind.corollary,
        DocumentKind.example,
        DocumentKind.remark,
        DocumentKind.proof,
        DocumentKind.local_claim,
        DocumentKind.calculation_block,
        DocumentKind.opaque,
    ):
        registry.register(kind.value, PassthroughDocumentHandler(kind))
    return registry

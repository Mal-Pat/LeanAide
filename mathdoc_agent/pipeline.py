from __future__ import annotations

import asyncio

from mathdoc_agent.export.json import to_json
from mathdoc_agent.models.document import MathDocument
from mathdoc_agent.orchestration.document_orchestrator import document_from_text, refine_math_document
from mathdoc_agent.plugins.document_types import default_document_handler_registry
from mathdoc_agent.plugins.proof_types import default_proof_handler_registry
from mathdoc_agent.registries.document_handlers import DocumentHandlerRegistry
from mathdoc_agent.registries.proof_handlers import ProofHandlerRegistry


async def generate_math_document(
    source_text: str,
    *,
    id: str = "doc",
    title: str | None = None,
    document_registry: DocumentHandlerRegistry | None = None,
    proof_registry: ProofHandlerRegistry | None = None,
    document_iterations: int = 20,
    proof_iterations: int = 100,
) -> MathDocument:
    document = document_from_text(source_text, id=id, title=title)
    return await refine_math_document(
        document,
        document_registry or default_document_handler_registry(),
        proof_registry or default_proof_handler_registry(),
        document_iterations=document_iterations,
        proof_iterations=proof_iterations,
    )


async def generate_math_document_json(
    source_text: str,
    *,
    id: str = "doc",
    title: str | None = None,
    document_registry: DocumentHandlerRegistry | None = None,
    proof_registry: ProofHandlerRegistry | None = None,
    indent: int = 2,
) -> str:
    document = await generate_math_document(
        source_text,
        id=id,
        title=title,
        document_registry=document_registry,
        proof_registry=proof_registry,
    )
    return to_json(document, indent=indent)


def generate_math_document_json_sync(
    source_text: str,
    *,
    id: str = "doc",
    title: str | None = None,
    document_registry: DocumentHandlerRegistry | None = None,
    proof_registry: ProofHandlerRegistry | None = None,
    indent: int = 2,
) -> str:
    return asyncio.run(
        generate_math_document_json(
            source_text,
            id=id,
            title=title,
            document_registry=document_registry,
            proof_registry=proof_registry,
            indent=indent,
        )
    )

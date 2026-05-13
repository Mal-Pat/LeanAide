from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

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
    document_iterations: int = 20,
    proof_iterations: int = 100,
    indent: int = 2,
) -> str:
    document = await generate_math_document(
        source_text,
        id=id,
        title=title,
        document_registry=document_registry,
        proof_registry=proof_registry,
        document_iterations=document_iterations,
        proof_iterations=proof_iterations,
    )
    return to_json(document, indent=indent)


def generate_math_document_json_sync(
    source_text: str,
    *,
    id: str = "doc",
    title: str | None = None,
    document_registry: DocumentHandlerRegistry | None = None,
    proof_registry: ProofHandlerRegistry | None = None,
    document_iterations: int = 20,
    proof_iterations: int = 100,
    indent: int = 2,
) -> str:
    return asyncio.run(
        generate_math_document_json(
            source_text,
            id=id,
            title=title,
            document_registry=document_registry,
            proof_registry=proof_registry,
            document_iterations=document_iterations,
            proof_iterations=proof_iterations,
            indent=indent,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate mathdoc_agent JSON from a mathematical source text file."
    )
    parser.add_argument("source", type=Path, help="Source text/Markdown file to parse.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="JSON output path. If omitted, write JSON to stdout.",
    )
    parser.add_argument(
        "--id",
        help="Document id. Defaults to the source file stem.",
    )
    parser.add_argument("--title", help="Optional document title.")
    parser.add_argument(
        "--document-iterations",
        type=int,
        default=20,
        help="Maximum document refinement iterations.",
    )
    parser.add_argument(
        "--proof-iterations",
        type=int,
        default=100,
        help="Maximum proof refinement iterations per proof.",
    )
    parser.add_argument("--indent", type=int, default=2, help="JSON indentation.")
    args = parser.parse_args()

    source_text = args.source.read_text(encoding="utf-8")
    json_text = generate_math_document_json_sync(
        source_text,
        id=args.id or args.source.stem,
        title=args.title,
        document_iterations=args.document_iterations,
        proof_iterations=args.proof_iterations,
        indent=args.indent,
    )
    if args.output is None:
        print(json_text)
    else:
        args.output.write_text(json_text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

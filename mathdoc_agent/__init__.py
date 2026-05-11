"""Agentic mathematical document decomposition package."""

from mathdoc_agent.models.document import DocumentNode, MathDocument
from mathdoc_agent.models.proof import ProofNode, ProofTree
from mathdoc_agent.pipeline import (
    generate_math_document,
    generate_math_document_json,
    generate_math_document_json_sync,
)

__all__ = [
    "DocumentNode",
    "MathDocument",
    "ProofNode",
    "ProofTree",
    "generate_math_document",
    "generate_math_document_json",
    "generate_math_document_json_sync",
]

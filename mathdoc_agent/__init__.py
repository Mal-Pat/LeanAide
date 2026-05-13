"""Agentic mathematical document decomposition package."""

from mathdoc_agent.models.document import DocumentNode, MathDocument
from mathdoc_agent.models.proof import ProofNode, ProofTree

__all__ = [
    "DocumentNode",
    "MathDocument",
    "ProofNode",
    "ProofTree",
    "generate_math_document",
    "generate_math_document_json",
    "generate_math_document_json_sync",
]


def __getattr__(name: str):
    if name in {
        "generate_math_document",
        "generate_math_document_json",
        "generate_math_document_json_sync",
    }:
        from mathdoc_agent import pipeline

        return getattr(pipeline, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

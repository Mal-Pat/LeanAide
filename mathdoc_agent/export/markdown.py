from __future__ import annotations

from mathdoc_agent.models.document import DocumentNode, MathDocument
from mathdoc_agent.models.proof import ProofNode
from mathdoc_agent.orchestration.worklist import kind_key


def render_proof_node_md(node: ProofNode, indent: int = 0) -> str:
    pad = "  " * indent
    lines = [f"{pad}- **{kind_key(node.kind)}** `{node.id}` [{node.status.value}]"]
    if node.goal:
        lines.append(f"{pad}  - Goal: `{node.goal}`")
    if node.hypotheses:
        lines.append(f"{pad}  - Hypotheses: {', '.join(node.hypotheses)}")
    if node.notes:
        lines.append(f"{pad}  - Notes: {'; '.join(node.notes)}")
    if node.unresolved_details:
        lines.append(f"{pad}  - Unresolved: {'; '.join(node.unresolved_details)}")
    for child in node.children:
        lines.append(render_proof_node_md(child, indent + 1))
    return "\n".join(lines)


def render_document_node_md(node: DocumentNode, indent: int = 0) -> str:
    pad = "  " * indent
    title = f" {node.title}" if node.title else ""
    label = f" `{node.label}`" if node.label else ""
    lines = [f"{pad}- **{kind_key(node.kind)}** `{node.id}`{label}{title} [{node.status.value}]"]
    if node.text:
        lines.append(f"{pad}  - Text: {node.text[:160]}")
    if node.proof is not None:
        lines.append(f"{pad}  - Proof:")
        lines.append(render_proof_node_md(node.proof.root, indent + 2))
    for child in node.children:
        lines.append(render_document_node_md(child, indent + 1))
    return "\n".join(lines)


def render_math_document_md(document: MathDocument) -> str:
    lines = []
    if document.title:
        lines.append(f"# {document.title}")
        lines.append("")
    lines.append(render_document_node_md(document.root))
    return "\n".join(lines)

from __future__ import annotations

import sys

from mathdoc_agent.models.base import NodeStatus, ProofKind
from mathdoc_agent.models.proof import ProofNode, ProofTree
from mathdoc_agent.orchestration.context import build_proof_context
from mathdoc_agent.orchestration.worklist import (
    choose_next_proof_node,
    kind_key,
    replace_proof_node,
)
from mathdoc_agent.registries.proof_handlers import ProofHandlerRegistry


def mark_opaque(node: ProofNode, reason: str) -> ProofNode:
    return node.model_copy(
        update={
            "kind": ProofKind.opaque,
            "status": NodeStatus.opaque,
            "notes": node.notes + [reason],
        }
    )


async def refine_one_proof_node(
    proof_tree: ProofTree,
    node: ProofNode,
    registry: ProofHandlerRegistry,
    available_document_results: list[str] | None = None,
) -> ProofTree:
    context = build_proof_context(
        proof_tree,
        node.id,
        available_document_results=available_document_results,
    )
    handler = registry.get(kind_key(node.kind))

    try:
        candidate = await handler.refine(node, context)
        report = handler.validate(candidate, context)
    except Exception as exc:
        print(
            f"[mathdoc_agent] proof handler error node={node.id} kind={kind_key(node.kind)!r}: {exc}",
            file=sys.stderr,
            flush=True,
        )
        candidate = mark_opaque(node, f"Marked opaque after handler exception: {exc}")
    else:
        if not report.ok:
            print(
                "[mathdoc_agent] proof validation error "
                f"node={node.id} kind={kind_key(node.kind)!r}: "
                + "; ".join(issue.message for issue in report.issues),
                file=sys.stderr,
                flush=True,
            )
            candidate = mark_opaque(
                node,
                "Marked opaque after failed validation: "
                + "; ".join(issue.message for issue in report.issues),
            )

    new_root = replace_proof_node(proof_tree.root, node.id, candidate)
    new_tree = proof_tree.model_copy(update={"root": new_root})
    return recompute_proof_statuses(new_tree, registry)


async def refine_proof_tree(
    proof_tree: ProofTree,
    registry: ProofHandlerRegistry,
    available_document_results: list[str] | None = None,
    max_iterations: int = 100,
) -> ProofTree:
    tree = recompute_proof_statuses(proof_tree, registry)

    for _ in range(max_iterations):
        node = choose_next_proof_node(tree.root)
        if node is None:
            break
        tree = await refine_one_proof_node(
            tree,
            node,
            registry,
            available_document_results=available_document_results,
        )

    return recompute_proof_statuses(tree, registry)


def recompute_proof_node_status(
    node: ProofNode,
    proof_tree: ProofTree,
    registry: ProofHandlerRegistry,
) -> ProofNode:
    children = [
        recompute_proof_node_status(child, proof_tree, registry)
        for child in node.children
    ]
    node = node.model_copy(update={"children": children})

    if kind_key(node.kind) == ProofKind.opaque.value:
        return node.model_copy(update={"status": NodeStatus.opaque})

    context = build_proof_context(proof_tree, node.id)
    handler = registry.get(kind_key(node.kind))

    try:
        resolved = handler.is_resolved(node, context)
    except Exception:
        resolved = False

    if resolved:
        return node.model_copy(update={"status": NodeStatus.resolved})
    if node.children:
        return node.model_copy(update={"status": NodeStatus.decomposed})
    if kind_key(node.kind) != ProofKind.unknown.value:
        return node.model_copy(update={"status": NodeStatus.classified})
    return node.model_copy(update={"status": NodeStatus.raw})


def recompute_proof_statuses(
    proof_tree: ProofTree,
    registry: ProofHandlerRegistry,
) -> ProofTree:
    root = recompute_proof_node_status(proof_tree.root, proof_tree, registry)
    return proof_tree.model_copy(update={"root": root})

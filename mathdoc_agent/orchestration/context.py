from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from mathdoc_agent.models.base import ProofKind
from mathdoc_agent.models.payloads import CasesData, InductionData, LocalClaimData
from mathdoc_agent.models.proof import ProofNode, ProofTree
from mathdoc_agent.orchestration.worklist import kind_key


class DocumentContext(BaseModel):
    document_title: Optional[str] = None
    ancestor_titles: list[str] = Field(default_factory=list)
    available_labels: list[str] = Field(default_factory=list)
    nearby_statements: list[str] = Field(default_factory=list)


class ProofContext(BaseModel):
    theorem_statement: Optional[str] = None
    ancestor_goals: list[str] = Field(default_factory=list)
    inherited_hypotheses: list[str] = Field(default_factory=list)
    active_inductions: list[str] = Field(default_factory=list)
    active_cases: list[str] = Field(default_factory=list)
    local_claims: list[str] = Field(default_factory=list)
    available_document_results: list[str] = Field(default_factory=list)


def path_to_proof_node(root: ProofNode, node_id: str) -> list[ProofNode] | None:
    if root.id == node_id:
        return [root]
    for child in root.children:
        subpath = path_to_proof_node(child, node_id)
        if subpath is not None:
            return [root] + subpath
    return None


def _local_claim_statement(node: ProofNode) -> str | None:
    if kind_key(node.kind) != ProofKind.local_claim.value:
        return None
    try:
        return LocalClaimData.model_validate(node.data).statement
    except Exception:
        return node.goal


def earlier_sibling_local_claims(proof_tree: ProofTree, node_id: str) -> list[str]:
    claims: list[str] = []

    def visit(parent: ProofNode) -> bool:
        for index, child in enumerate(parent.children):
            if child.id == node_id:
                for sibling in parent.children[:index]:
                    statement = _local_claim_statement(sibling)
                    if statement:
                        claims.append(statement)
                return True
            if visit(child):
                return True
        return False

    visit(proof_tree.root)
    return claims


def build_proof_context(
    proof_tree: ProofTree,
    node_id: str,
    available_document_results: list[str] | None = None,
) -> ProofContext:
    path = path_to_proof_node(proof_tree.root, node_id)
    if path is None:
        return ProofContext(
            theorem_statement=proof_tree.theorem_statement,
            available_document_results=available_document_results or [],
        )

    ancestor_goals: list[str] = []
    inherited_hypotheses: list[str] = []
    active_inductions: list[str] = []
    active_cases: list[str] = []
    local_claims: list[str] = []

    for ancestor in path[:-1]:
        if ancestor.goal:
            ancestor_goals.append(ancestor.goal)
        inherited_hypotheses.extend(ancestor.hypotheses)

        if kind_key(ancestor.kind) == ProofKind.induction.value:
            try:
                data = InductionData.model_validate(ancestor.data)
                active_inductions.append(
                    f"Induction on {data.variable}; IHs: {data.induction_hypotheses}"
                )
            except Exception:
                pass

        if kind_key(ancestor.kind) == ProofKind.cases.value:
            try:
                data = CasesData.model_validate(ancestor.data)
                active_cases.append(f"Case split on {data.split_on}")
            except Exception:
                pass

        statement = _local_claim_statement(ancestor)
        if statement:
            local_claims.append(statement)

    local_claims.extend(earlier_sibling_local_claims(proof_tree, node_id))

    return ProofContext(
        theorem_statement=proof_tree.theorem_statement,
        ancestor_goals=ancestor_goals,
        inherited_hypotheses=inherited_hypotheses,
        active_inductions=active_inductions,
        active_cases=active_cases,
        local_claims=local_claims,
        available_document_results=available_document_results or [],
    )

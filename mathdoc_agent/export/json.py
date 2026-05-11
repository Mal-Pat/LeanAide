from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel

from mathdoc_agent.models.base import DocumentKind, ProofKind
from mathdoc_agent.models.document import DocumentNode, MathDocument
from mathdoc_agent.models.payloads import (
    CalculationData,
    CasesData,
    InductionData,
    SimpleProofData,
    StatementData,
    StructuredProofData,
)
from mathdoc_agent.models.proof import ProofNode, ProofTree
from mathdoc_agent.orchestration.worklist import kind_key


def _without_none(value: dict[str, Any]) -> dict[str, Any]:
    return {key: item for key, item in value.items() if item is not None}


def _statement_data(node: DocumentNode) -> StatementData | None:
    try:
        return StatementData.model_validate(node.data)
    except Exception:
        return None


def _theorem_header(kind: str) -> str:
    return {
        DocumentKind.lemma.value: "Lemma",
        DocumentKind.proposition.value: "Proposition",
        DocumentKind.corollary.value: "Corollary",
        DocumentKind.local_claim.value: "Claim",
    }.get(kind, "Theorem")


def _assumption_steps(assumptions: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "type": "assume_statement",
            "assumption": assumption,
        }
        for assumption in assumptions
    ]


def _proof_details_data(proof: ProofTree | None) -> Any:
    if proof is None:
        return None
    return _proof_node_data(proof.root)


def _document_node_data(node: DocumentNode) -> dict[str, Any]:
    kind = kind_key(node.kind)
    if kind in {
        DocumentKind.theorem.value,
        DocumentKind.lemma.value,
        DocumentKind.proposition.value,
        DocumentKind.corollary.value,
        DocumentKind.local_claim.value,
    }:
        statement = _statement_data(node)
        proof = _proof_details_data(node.proof)
        return _without_none(
            {
                "type": "Theorem",
                "label": node.label or node.id,
                "header": _theorem_header(kind),
                "claim": statement.statement if statement else node.text,
                "hypothesis": _assumption_steps(statement.assumptions) if statement and statement.assumptions else None,
                "proof": proof,
                "id": node.id,
                "status": node.status.value,
            }
        )

    if kind == DocumentKind.definition.value:
        return _without_none(
            {
                "type": "Definition",
                "label": node.label or node.id,
                "header": "Definition",
                "definition": node.data.get("definiens") or node.text,
                "name": node.data.get("term") or node.title or node.label or node.id,
                "id": node.id,
                "status": node.status.value,
            }
        )

    if kind in {DocumentKind.section.value, DocumentKind.subsection.value, DocumentKind.document.value}:
        return _without_none(
            {
                "type": "Section" if kind != DocumentKind.document.value else "document",
                "label": node.label or node.id,
                "level": 2 if kind == DocumentKind.subsection.value else 1,
                "header": node.title or node.label or node.id,
                "content": [_document_node_data(child) for child in node.children],
                "id": node.id,
                "status": node.status.value,
            }
        )

    return _without_none(
        {
            "type": "Paragraph",
            "text": node.text,
            "id": node.id,
            "status": node.status.value,
        }
    )


def _simple_proof_data(node: ProofNode) -> dict[str, Any]:
    try:
        data = SimpleProofData.model_validate(node.data)
    except Exception:
        data = SimpleProofData()
    return _without_none(
        {
            "type": "assert_statement",
            "claim": node.goal or node.text,
            "proof_method": data.method,
            "id": node.id,
            "status": node.status.value,
            "text": node.text,
        }
    )


def _structured_data(node: ProofNode) -> StructuredProofData:
    try:
        return StructuredProofData.model_validate(node.data)
    except Exception:
        return StructuredProofData()


def _proof_node_data(node: ProofNode) -> Any:
    kind = kind_key(node.kind)
    if kind in {
        ProofKind.simple.value,
        ProofKind.theorem_application.value,
        ProofKind.definition_unfolding.value,
    }:
        return _simple_proof_data(node)

    if kind == ProofKind.calculation.value:
        try:
            data = CalculationData.model_validate(node.data)
        except Exception:
            data = CalculationData()
        sequence = [
            f"{step.lhs} {step.relation.value} {step.rhs}"
            + (f" ({step.justification})" if step.justification else "")
            for step in data.steps
        ]
        return _without_none(
            {
                "type": "calculation",
                "calculation_sequence": sequence or None,
                "inline_calculation": node.text if not sequence else None,
                "id": node.id,
                "status": node.status.value,
            }
        )

    if kind == ProofKind.induction.value:
        data = InductionData.model_validate(node.data)
        children = {child.id: child for child in node.children}
        base = [_proof_node_data(children[child_id]) for child_id in data.base_case_ids if child_id in children]
        steps = [_proof_node_data(children[child_id]) for child_id in data.step_case_ids if child_id in children]
        return _without_none(
            {
                "type": "induction_proof",
                "on": data.variable,
                "prev_var": data.metadata.get("prev_var") if hasattr(data, "metadata") else None,
                "base_case_proof": base[0] if len(base) == 1 else base,
                "induction_step_proof": steps[0] if len(steps) == 1 else steps,
                "id": node.id,
                "status": node.status.value,
                "text": node.text,
            }
        )

    if kind == ProofKind.cases.value:
        data = CasesData.model_validate(node.data)
        proof_cases = []
        for child in node.children:
            condition = child.hypotheses[0] if child.hypotheses else child.goal or child.text
            proof_cases.append(
                {
                    "type": "case",
                    "condition": condition,
                    "proof": _proof_node_data(child),
                }
            )
        return _without_none(
            {
                "type": "multi-condition_cases_proof",
                "proof_cases": proof_cases,
                "exhaustiveness": {
                    "type": "assert_statement",
                    "claim": data.exhaustive_reason,
                }
                if data.exhaustive_reason
                else None,
                "id": node.id,
                "status": node.status.value,
            }
        )

    if kind == ProofKind.contradiction.value:
        data = _structured_data(node)
        return _without_none(
            {
                "type": "contradiction_statement",
                "assumption": data.contradiction_assumption or (data.assumptions[0] if data.assumptions else None),
                "proof": [_proof_node_data(child) for child in node.children],
                "id": node.id,
                "status": node.status.value,
            }
        )

    if kind == ProofKind.equivalence.value and len(node.children) >= 2:
        return _without_none(
            {
                "type": "bi-implication_cases_proof",
                "if_proof": _proof_node_data(node.children[0]),
                "only_if_proof": _proof_node_data(node.children[1]),
                "id": node.id,
                "status": node.status.value,
            }
        )

    structured = _structured_data(node)
    proof_steps = [_proof_node_data(child) for child in node.children]
    if not proof_steps and structured.summary:
        proof_steps = [{"type": "assert_statement", "claim": structured.summary}]
    if not proof_steps:
        proof_steps = [{"type": "assert_statement", "claim": node.goal or node.text}]
    return _without_none(
        {
            "type": "Proof",
            "claim_label": node.goal or node.id,
            "proof_steps": proof_steps,
            "id": node.id,
            "status": node.status.value,
        }
    )


def paper_structure_data(model: BaseModel) -> dict[str, Any]:
    """Return a compact PaperStructure-style document for Lean codegen."""
    if isinstance(model, MathDocument):
        document = {
            "type": "document",
            "body": [_document_node_data(child) for child in model.root.children],
        }
        if model.title is not None:
            document["title"] = model.title
        return {"document": document}
    if isinstance(model, DocumentNode):
        return _document_node_data(model)
    if isinstance(model, ProofTree):
        return _proof_details_data(model)
    if isinstance(model, ProofNode):
        return _proof_node_data(model)
    return _debug_data(model)


def _debug_data(value: Any) -> Any:
    """Return JSON-ready data with public `type` discriminators, not internal `kind`.

    The orchestration layer keeps `kind` as an internal dispatch key. Exported JSON is
    intended for downstream Lean processing and should look closer to
    `resources/PaperStructure.json`, where `type` is the discriminator.
    """
    if isinstance(value, BaseModel):
        value = value.model_dump(mode="json")
    if isinstance(value, list):
        return [_debug_data(item) for item in value]
    if not isinstance(value, dict):
        return value

    cleaned_items = []
    for key, item in value.items():
        if key == "kind":
            continue
        cleaned_items.append((key, _debug_data(item)))

    if "type" not in value:
        return dict(cleaned_items)

    result: dict[str, Any] = {"type": value["type"]}
    for key, item in cleaned_items:
        if key != "type":
            result[key] = item
    return result


def to_json(model: BaseModel, *, indent: int = 2) -> str:
    return json.dumps(paper_structure_data(model), indent=indent, ensure_ascii=False)


def to_debug_json(model: BaseModel, *, indent: int = 2) -> str:
    return json.dumps(_debug_data(model), indent=indent, ensure_ascii=False)

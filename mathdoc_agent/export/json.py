from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel

from mathdoc_agent.models.base import DocumentKind, ProofKind
from mathdoc_agent.models.document import DocumentNode, MathDocument
from mathdoc_agent.models.payloads import (
    CalcStep,
    CalculationData,
    CasesData,
    InductionData,
    InductiveTypeDefinitionData,
    InstanceDefinitionData,
    SimpleProofData,
    StatementData,
    StructureDefinitionData,
    StructuredProofData,
)
from mathdoc_agent.models.proof import ProofNode, ProofTree
from mathdoc_agent.orchestration.worklist import kind_key
from mathdoc_agent.plugins.calculation_types import CORE_CALCULATION_SCHEMAS


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


def _logical_step_data(step) -> dict[str, Any]:
    return _without_none(step.model_dump(exclude_none=True))


def _calculation_step_data(step: CalcStep) -> dict[str, Any]:
    return _without_none(
        {
            "from": step.lhs,
            "relation": step.relation.value,
            "to": step.rhs,
            "justification": step.justification,
            "side_conditions": step.side_conditions or None,
        }
    )


def _goal_relation(data: CalculationData) -> str | None:
    if not data.steps:
        return None
    relations = {step.relation.value for step in data.steps}
    if len(relations) == 1:
        return data.steps[0].relation.value
    return "mixed"


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

    if kind == DocumentKind.structure_definition.value:
        data = StructureDefinitionData.model_validate(node.data)
        return _without_none(
            {
                "type": "structure-definition",
                "label": node.label or node.id,
                "name": data.name,
                "is_class": data.is_class,
                "parameters": data.parameters or None,
                "extends": data.extends or None,
                "fields": [field.model_dump(exclude_none=True) for field in data.fields] or None,
                "text": node.text or None,
                "id": node.id,
                "status": node.status.value,
            }
        )

    if kind == DocumentKind.instance_definition.value:
        data = InstanceDefinitionData.model_validate(node.data)
        return _without_none(
            {
                "type": "instance-definition",
                "label": node.label or node.id,
                "name": data.name,
                "class_name": data.class_name,
                "target": data.target,
                "parameters": data.parameters or None,
                "fields": data.fields or None,
                "value": data.value,
                "text": node.text or None,
                "id": node.id,
                "status": node.status.value,
            }
        )

    if kind == DocumentKind.inductive_type_definition.value:
        data = InductiveTypeDefinitionData.model_validate(node.data)
        return _without_none(
            {
                "type": "inductive-type-definition",
                "label": node.label or node.id,
                "name": data.name,
                "is_prop": data.is_prop,
                "parameters": data.parameters or None,
                "constructors": [
                    constructor.model_dump(exclude_none=True)
                    for constructor in data.constructors
                ],
                "text": node.text or None,
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
    if data.proof_steps:
        return _without_none(
            {
                "type": "Proof",
                "claim_label": node.goal or node.id,
                "proof_steps": [_logical_step_data(step) for step in data.proof_steps],
                "id": node.id,
                "status": node.status.value,
                "text": node.text,
            }
        )
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
        if data.calculation_kind in CORE_CALCULATION_SCHEMAS:
            return _without_none(
                {
                    "type": data.calculation_kind,
                    "start": data.start,
                    "target": data.target,
                    "goal_relation": _goal_relation(data),
                    "steps": [_calculation_step_data(step) for step in data.steps],
                    "inline_calculation": node.text if not data.steps else None,
                    "id": node.id,
                    "status": node.status.value,
                    "text": node.text,
                }
            )
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
                "proof": {
                    "type": "Proof",
                    "proof_steps": [_proof_node_data(child) for child in node.children],
                },
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

    if kind == ProofKind.reduction.value:
        data = _structured_data(node)
        children = {child.id: child for child in node.children}
        proof_of_reduction = (
            children.get(data.proof_of_reduction_id)
            if data.proof_of_reduction_id
            else (node.children[0] if node.children else None)
        )
        reduced_goal_proof = (
            children.get(data.proof_id)
            if data.proof_id
            else (node.children[1] if len(node.children) > 1 else None)
        )
        return _without_none(
            {
                "type": "reduction_proof",
                "claim": data.claim or node.goal,
                "reduced_to": data.reduced_to,
                "proof_of_reduction": (
                    _proof_node_data(proof_of_reduction)
                    if proof_of_reduction is not None
                    else None
                ),
                "proof": (
                    _proof_node_data(reduced_goal_proof)
                    if reduced_goal_proof is not None
                    else None
                ),
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

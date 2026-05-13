from __future__ import annotations

import re
from typing import Union

from pydantic import BaseModel, Field

from mathdoc_agent.mathagents.runner import run_agent_typed
from mathdoc_agent.builders.proof_builder import ProofBuilder
from mathdoc_agent.handlers.base import ProofRefinementHandler
from mathdoc_agent.models.base import NodeStatus, ProofKind
from mathdoc_agent.models.payloads import (
    CalculationData,
    CasesData,
    InductionData,
    LocalClaimData,
    LogicalProofStepData,
    SimpleProofData,
    StructuredProofData,
)
from mathdoc_agent.models.proof import ProofNode
from mathdoc_agent.models.refinement_specs import (
    CalculationRefinementSpec,
    CasesRefinementSpec,
    InductionRefinementSpec,
    LocalClaimRefinementSpec,
    metadata_entries_to_dict,
    SimpleProofRefinementSpec,
    StructuredProofRefinementSpec,
)
from mathdoc_agent.models.validation import ValidationIssue, ValidationReport
from mathdoc_agent.orchestration.context import ProofContext
from mathdoc_agent.orchestration.worklist import kind_key
from mathdoc_agent.validation.deterministic import validate_calculation_adjacency


class ClassificationSpec(BaseModel):
    kind: Union[ProofKind, str]
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    notes: list[str] = Field(default_factory=list)


class UnknownProofHandler(ProofRefinementHandler[ClassificationSpec]):
    kind = ProofKind.unknown.value
    output_model = ClassificationSpec

    def __init__(self, agent) -> None:
        self.agent = agent

    async def refine(self, node: ProofNode, context: ProofContext) -> ProofNode:
        spec = await run_agent_typed(
            self.agent,
            {
                "node": node.model_dump(),
                "context": context.model_dump(),
                "task": "Classify this proof node by outermost proof structure.",
            },
            ClassificationSpec,
        )
        if kind_key(spec.kind) == ProofKind.unknown.value:
            return node.model_copy(
                update={
                    "kind": ProofKind.opaque,
                    "status": NodeStatus.opaque,
                    "confidence": spec.confidence,
                    "notes": node.notes + spec.notes + ["Classifier could not identify proof structure."],
                }
            )
        return node.model_copy(
            update={
                "kind": spec.kind,
                "status": NodeStatus.classified,
                "confidence": spec.confidence,
                "notes": node.notes + spec.notes,
            }
        )


class OpaqueProofHandler(ProofRefinementHandler[None]):
    kind = ProofKind.opaque.value

    async def refine(self, node: ProofNode, context: ProofContext) -> ProofNode:
        return node.model_copy(update={"status": NodeStatus.opaque})

    def is_resolved(self, node: ProofNode, context: ProofContext) -> bool:
        return True


class InductionHandler(ProofRefinementHandler[InductionRefinementSpec]):
    kind = ProofKind.induction.value
    output_model = InductionRefinementSpec

    def __init__(self, agent) -> None:
        self.agent = agent

    async def refine(self, node: ProofNode, context: ProofContext) -> ProofNode:
        spec = await run_agent_typed(
            self.agent,
            {"node": node.model_dump(), "context": context.model_dump()},
            InductionRefinementSpec,
        )
        base_nodes = [
            ProofNode(
                id=f"{node.id}.{child.id_suffix}",
                kind=child.kind,
                status=NodeStatus.raw,
                text=child.text,
                goal=child.goal,
                hypotheses=child.hypotheses,
                notes=child.notes,
            )
            for child in spec.base_cases
        ]
        step_nodes = [
            ProofNode(
                id=f"{node.id}.{child.id_suffix}",
                kind=child.kind,
                status=NodeStatus.raw,
                text=child.text,
                goal=child.goal,
                hypotheses=child.hypotheses,
                notes=child.notes,
            )
            for child in spec.step_cases
        ]
        replacement = ProofBuilder.induction(
            id=node.id,
            text=node.text,
            variable=spec.variable,
            principle=spec.principle,
            induction_hypotheses=spec.induction_hypotheses,
            base_cases=base_nodes,
            step_cases=step_nodes,
            goal=node.goal,
            hypotheses=node.hypotheses,
        )
        return replacement.model_copy(update={"notes": node.notes + spec.notes})

    def validate(self, node: ProofNode, context: ProofContext) -> ValidationReport:
        issues: list[ValidationIssue] = []
        data = InductionData.model_validate(node.data)
        if not data.variable:
            issues.append(ValidationIssue(severity="error", path="data.variable", message="Induction node has no induction variable."))
        if not data.base_case_ids:
            issues.append(ValidationIssue(severity="error", path="data.base_case_ids", message="Induction node has no base cases."))
        if not data.step_case_ids:
            issues.append(ValidationIssue(severity="error", path="data.step_case_ids", message="Induction node has no step cases."))
        child_ids = {child.id for child in node.children}
        for child_id in data.base_case_ids + data.step_case_ids:
            if child_id not in child_ids:
                issues.append(ValidationIssue(severity="error", path="data", message=f"Referenced child id {child_id!r} is missing."))
        return ValidationReport.from_issues(issues)

    def is_resolved(self, node: ProofNode, context: ProofContext) -> bool:
        return bool(node.children) and all(
            child.status in {NodeStatus.resolved, NodeStatus.opaque}
            for child in node.children
        )


class CasesHandler(ProofRefinementHandler[CasesRefinementSpec]):
    kind = ProofKind.cases.value
    output_model = CasesRefinementSpec

    def __init__(self, agent) -> None:
        self.agent = agent

    async def refine(self, node: ProofNode, context: ProofContext) -> ProofNode:
        spec = await run_agent_typed(
            self.agent,
            {"node": node.model_dump(), "context": context.model_dump()},
            CasesRefinementSpec,
        )
        case_nodes = [
            ProofNode(
                id=f"{node.id}.{child.id_suffix}",
                kind=child.kind,
                status=NodeStatus.raw,
                text=child.text,
                goal=child.goal,
                hypotheses=child.hypotheses,
                notes=child.notes,
            )
            for child in spec.cases
        ]
        replacement = ProofBuilder.cases(
            id=node.id,
            text=node.text,
            split_on=spec.split_on,
            exhaustive_reason=spec.exhaustive_reason,
            cases=case_nodes,
            goal=node.goal,
            hypotheses=node.hypotheses,
        )
        return replacement.model_copy(update={"notes": node.notes + spec.notes})

    def validate(self, node: ProofNode, context: ProofContext) -> ValidationReport:
        issues: list[ValidationIssue] = []
        data = CasesData.model_validate(node.data)
        if not data.case_ids:
            issues.append(ValidationIssue(severity="error", path="data.case_ids", message="Cases node has no cases."))
        child_ids = {child.id for child in node.children}
        for child_id in data.case_ids:
            if child_id not in child_ids:
                issues.append(ValidationIssue(severity="error", path="data", message=f"Referenced child id {child_id!r} is missing."))
        return ValidationReport.from_issues(issues)

    def is_resolved(self, node: ProofNode, context: ProofContext) -> bool:
        return bool(node.children) and all(
            child.status in {NodeStatus.resolved, NodeStatus.opaque}
            for child in node.children
        )


class SimpleProofHandler(ProofRefinementHandler[SimpleProofRefinementSpec]):
    kind = ProofKind.simple.value
    output_model = SimpleProofRefinementSpec

    def __init__(self, agent) -> None:
        self.agent = agent

    def _fallback_proof_steps(self, text: str) -> list[LogicalProofStepData]:
        steps: list[LogicalProofStepData] = []
        pending_method: str | None = None
        parts = re.split(r"(\\\[.*?\\\])", text, flags=re.DOTALL)
        for part in parts:
            if not part.strip():
                continue
            match = re.fullmatch(r"\\\[(.*?)\\\]", part.strip(), flags=re.DOTALL)
            if match:
                equation = " ".join(match.group(1).split())
                steps.append(
                    LogicalProofStepData(
                        type="assert_statement",
                        claim=equation,
                        proof_method=pending_method or "displayed equation from the proof text",
                    )
                )
                pending_method = None
                continue
            sentences = [
                sentence.strip()
                for sentence in re.split(r"(?<=[.!?])\s+", " ".join(part.split()))
                if sentence.strip()
            ]
            for sentence in sentences:
                lowered = sentence.lower()
                if lowered.startswith("let "):
                    steps.append(
                        LogicalProofStepData(
                            type="let_statement",
                            variable_name="<anonymous>",
                            statement=sentence,
                        )
                    )
                    pending_method = sentence
                elif lowered.startswith("fix ") or lowered.startswith("assume "):
                    steps.append(
                        LogicalProofStepData(
                            type="assume_statement",
                            assumption=sentence,
                        )
                    )
                    pending_method = sentence
                elif any(marker in lowered for marker in ("we want to prove", "this shows", "therefore")):
                    steps.append(
                        LogicalProofStepData(
                            type="assert_statement",
                            claim=sentence,
                            proof_method="stated in the proof text",
                        )
                    )
                elif lowered.startswith(
                    ("by ", "since ", "using ", "rewriting ", "first,", "next,", "because ", "so")
                ):
                    pending_method = sentence
        if len(steps) < 2:
            return []
        return steps

    async def refine(self, node: ProofNode, context: ProofContext) -> ProofNode:
        spec = await run_agent_typed(
            self.agent,
            {"node": node.model_dump(), "context": context.model_dump()},
            SimpleProofRefinementSpec,
        )
        proof_steps = spec.proof_steps or self._fallback_proof_steps(node.text)
        data = SimpleProofData(
            method=spec.method,
            hints=spec.hints,
            referenced_lemmas=spec.referenced_lemmas,
            referenced_hypotheses=spec.referenced_hypotheses,
            proof_steps=proof_steps,
        )
        unresolved = node.unresolved_details + spec.unresolved_details
        status = NodeStatus.resolved if (data.hints or data.referenced_lemmas or data.referenced_hypotheses or data.proof_steps or unresolved) else NodeStatus.locally_refined
        return node.model_copy(
            update={
                "kind": ProofKind.simple,
                "status": status,
                "data": data.model_dump(),
                "unresolved_details": unresolved,
            }
        )

    def is_resolved(self, node: ProofNode, context: ProofContext) -> bool:
        data = SimpleProofData.model_validate(node.data)
        return bool(
            data.hints
            or data.referenced_lemmas
            or data.referenced_hypotheses
            or data.proof_steps
            or node.unresolved_details
        )


class CalculationHandler(ProofRefinementHandler[CalculationRefinementSpec]):
    kind = ProofKind.calculation.value
    output_model = CalculationRefinementSpec

    def __init__(self, agent) -> None:
        self.agent = agent

    async def refine(self, node: ProofNode, context: ProofContext) -> ProofNode:
        spec = await run_agent_typed(
            self.agent,
            {"node": node.model_dump(), "context": context.model_dump()},
            CalculationRefinementSpec,
        )
        replacement = ProofBuilder.calculation(
            id=node.id,
            text=node.text,
            steps=spec.steps,
            goal=node.goal,
            hypotheses=node.hypotheses,
            calculation_kind=spec.calculation_kind,
        )
        return replacement.model_copy(
            update={"unresolved_details": node.unresolved_details + spec.unresolved_details}
        )

    def validate(self, node: ProofNode, context: ProofContext) -> ValidationReport:
        data = CalculationData.model_validate(node.data)
        return validate_calculation_adjacency(data)

    def is_resolved(self, node: ProofNode, context: ProofContext) -> bool:
        data = CalculationData.model_validate(node.data)
        return bool(data.steps or node.unresolved_details)


class LocalClaimHandler(ProofRefinementHandler[LocalClaimRefinementSpec]):
    kind = ProofKind.local_claim.value
    output_model = LocalClaimRefinementSpec

    def __init__(self, agent=None) -> None:
        self.agent = agent

    async def refine(self, node: ProofNode, context: ProofContext) -> ProofNode:
        if self.agent is None:
            return node.model_copy(update={"status": NodeStatus.decomposed if node.children else NodeStatus.resolved})
        spec = await run_agent_typed(
            self.agent,
            {"node": node.model_dump(), "context": context.model_dump()},
            LocalClaimRefinementSpec,
        )
        proof_node = None
        if spec.proof is not None:
            proof_node = ProofNode(
                id=f"{node.id}.{spec.proof.id_suffix}",
                kind=spec.proof.kind,
                status=NodeStatus.raw,
                text=spec.proof.text,
                goal=spec.proof.goal or spec.statement,
                hypotheses=spec.proof.hypotheses,
                notes=spec.proof.notes,
            )
        return ProofBuilder.local_claim(
            id=node.id,
            text=node.text,
            statement=spec.statement,
            proof_node=proof_node,
            label=spec.label,
        ).model_copy(update={"notes": node.notes + spec.notes})

    def validate(self, node: ProofNode, context: ProofContext) -> ValidationReport:
        issues: list[ValidationIssue] = []
        data = LocalClaimData.model_validate(node.data)
        if not data.statement:
            issues.append(ValidationIssue(severity="error", path="data.statement", message="Local claim has no statement."))
        if data.proof_node_id and data.proof_node_id not in {child.id for child in node.children}:
            issues.append(ValidationIssue(severity="error", path="data.proof_node_id", message="Local claim proof_node_id is not a child."))
        return ValidationReport.from_issues(issues)

    def is_resolved(self, node: ProofNode, context: ProofContext) -> bool:
        if not node.children:
            return True
        return all(child.status in {NodeStatus.resolved, NodeStatus.opaque} for child in node.children)


class StructuredProofHandler(ProofRefinementHandler[StructuredProofRefinementSpec]):
    """Generic handler for proof families whose structure is a list of subproofs.

    This covers the reasonably decomposable proof types in `notes/proof_types.md`
    without adding duplicate orchestration code for every taxonomy entry.
    """

    output_model = StructuredProofRefinementSpec

    def __init__(self, kind: ProofKind | str, agent) -> None:
        self.kind = kind_key(kind)
        self.agent = agent

    async def refine(self, node: ProofNode, context: ProofContext) -> ProofNode:
        spec = await run_agent_typed(
            self.agent,
            {
                "node": node.model_dump(),
                "context": context.model_dump(),
                "proof_kind": self.kind,
                "task": "Refine this proof into its main logical components without expanding child proofs deeply.",
            },
            StructuredProofRefinementSpec,
        )
        def child_node(child) -> ProofNode:
            return ProofNode(
                id=f"{node.id}.{child.id_suffix}",
                kind=child.kind,
                status=NodeStatus.raw,
                text=child.text,
                goal=child.goal,
                hypotheses=child.hypotheses,
                notes=child.notes,
            )

        children = [child_node(child) for child in spec.components]
        proof_of_reduction = child_node(spec.proof_of_reduction) if spec.proof_of_reduction else None
        reduced_goal_proof = child_node(spec.proof) if spec.proof else None
        for child in (proof_of_reduction, reduced_goal_proof):
            if child is not None and child.id not in {existing.id for existing in children}:
                children.append(child)
        data = StructuredProofData(
            strategy=spec.strategy,
            summary=spec.summary,
            component_ids=[child.id for child in children],
            assumptions=spec.assumptions,
            conclusions=spec.conclusions,
            witness=spec.witness,
            contradiction_assumption=spec.contradiction_assumption,
            claim=spec.claim,
            reduced_to=spec.reduced_to,
            proof_of_reduction_id=proof_of_reduction.id if proof_of_reduction else None,
            proof_id=reduced_goal_proof.id if reduced_goal_proof else None,
            invariant=spec.invariant,
            construction=spec.construction,
            metadata=metadata_entries_to_dict(spec.metadata),
        )
        status = NodeStatus.decomposed if children else NodeStatus.resolved
        if spec.unresolved_details and not children:
            status = NodeStatus.resolved
        return node.model_copy(
            update={
                "kind": self.kind,
                "status": status,
                "children": children,
                "data": data.model_dump(),
                "unresolved_details": node.unresolved_details + spec.unresolved_details,
                "notes": node.notes + spec.notes,
            }
        )

    def validate(self, node: ProofNode, context: ProofContext) -> ValidationReport:
        issues: list[ValidationIssue] = []
        data = StructuredProofData.model_validate(node.data)
        child_ids = {child.id for child in node.children}
        for component_id in data.component_ids:
            if component_id not in child_ids:
                issues.append(
                    ValidationIssue(
                        severity="error",
                        path="data.component_ids",
                        message=f"Referenced component id {component_id!r} is missing.",
                    )
                )
        if self.kind == ProofKind.existence.value and not (data.witness or node.children):
            issues.append(
                ValidationIssue(
                    severity="warning",
                    path="data.witness",
                    message="Existence proof has no explicit witness or witness subproof.",
                )
            )
        if self.kind == ProofKind.contradiction.value and not (data.contradiction_assumption or node.children):
            issues.append(
                ValidationIssue(
                    severity="warning",
                    path="data.contradiction_assumption",
                    message="Contradiction proof has no negated assumption or contradiction subproof.",
                )
            )
        return ValidationReport.from_issues(issues)

    def is_resolved(self, node: ProofNode, context: ProofContext) -> bool:
        if node.children:
            return all(
                child.status in {NodeStatus.resolved, NodeStatus.opaque}
                for child in node.children
            )
        return bool(node.data or node.unresolved_details)

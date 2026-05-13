from __future__ import annotations

from mathdoc_agent.models.payloads import CalculationData
from mathdoc_agent.models.proof import ProofNode
from mathdoc_agent.models.validation import ValidationIssue, ValidationReport
from mathdoc_agent.orchestration.worklist import walk_proof_nodes


def validate_unique_proof_ids(root: ProofNode) -> ValidationReport:
    seen: set[str] = set()
    issues: list[ValidationIssue] = []
    for node in walk_proof_nodes(root):
        if node.id in seen:
            issues.append(
                ValidationIssue(
                    severity="error",
                    path=node.id,
                    message=f"Duplicate proof node id {node.id!r}.",
                )
            )
        seen.add(node.id)
    return ValidationReport.from_issues(issues)


def validate_calculation_adjacency(data: CalculationData) -> ValidationReport:
    issues: list[ValidationIssue] = []
    for index in range(1, len(data.steps)):
        prev_rhs = data.steps[index - 1].rhs.strip()
        curr_lhs = data.steps[index].lhs.strip()
        if curr_lhs != "_" and curr_lhs != prev_rhs:
            issues.append(
                ValidationIssue(
                    severity="warning",
                    path=f"steps[{index}].lhs",
                    message=f"Expected lhs to be {prev_rhs!r}, got {curr_lhs!r}.",
                )
            )
    return ValidationReport(ok=True, issues=issues)

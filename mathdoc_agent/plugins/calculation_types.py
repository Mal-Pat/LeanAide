from __future__ import annotations

from mathdoc_agent.models.payloads import CalculationData
from mathdoc_agent.models.validation import ValidationReport


CORE_CALCULATION_SCHEMAS = {
    "equality_chain",
    "inequality_chain",
    "mixed_relation_chain",
    "rewrite_by_hypothesis",
    "rewrite_by_lemma",
    "definition_unfolding",
    "normalization",
    "positivity_side_goal",
    "monotonicity_step",
    "triangle_inequality_estimate",
    "add_subtract_intermediate",
    "casewise_calculation",
    "inductive_step_calculation",
    "extensionality_then_pointwise_calculation",
    "calculation_to_contradiction",
}


class CalculationKindValidator:
    calculation_kind: str

    def validate(self, data: CalculationData) -> ValidationReport:
        return ValidationReport.ok_report()


class CalculationKindRegistry:
    def __init__(self) -> None:
        self._validators: dict[str, CalculationKindValidator] = {}

    def register(self, kind: str, validator: CalculationKindValidator) -> None:
        self._validators[kind] = validator

    def validate(self, data: CalculationData) -> ValidationReport:
        if data.calculation_kind in self._validators:
            return self._validators[data.calculation_kind].validate(data)
        return ValidationReport.ok_report()


calculation_kind_registry = CalculationKindRegistry()

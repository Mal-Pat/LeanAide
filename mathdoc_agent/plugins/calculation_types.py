from __future__ import annotations

from mathdoc_agent.models.payloads import CalculationData
from mathdoc_agent.models.validation import ValidationReport


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

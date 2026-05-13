from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ValidationIssue(BaseModel):
    severity: Literal["error", "warning", "info"]
    path: str
    message: str


class ValidationReport(BaseModel):
    ok: bool
    issues: list[ValidationIssue] = Field(default_factory=list)

    @classmethod
    def ok_report(cls) -> "ValidationReport":
        return cls(ok=True, issues=[])

    def has_errors(self) -> bool:
        return any(issue.severity == "error" for issue in self.issues)

    @classmethod
    def from_issues(cls, issues: list[ValidationIssue]) -> "ValidationReport":
        return cls(ok=not any(issue.severity == "error" for issue in issues), issues=issues)

from __future__ import annotations

from typing import Optional, Union

from pydantic import BaseModel, Field

from mathdoc_agent.models.base import DocumentKind, ProofKind
from mathdoc_agent.models.payloads import CalcStep


class ChildProofSpec(BaseModel):
    id_suffix: str
    kind: Union[ProofKind, str] = ProofKind.unknown
    text: str
    goal: Optional[str] = None
    hypotheses: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class InductionRefinementSpec(BaseModel):
    variable: str
    principle: Optional[str] = None
    induction_hypotheses: list[str] = Field(default_factory=list)
    base_cases: list[ChildProofSpec]
    step_cases: list[ChildProofSpec]
    notes: list[str] = Field(default_factory=list)


class CasesRefinementSpec(BaseModel):
    split_on: Optional[str] = None
    exhaustive_reason: Optional[str] = None
    cases: list[ChildProofSpec]
    notes: list[str] = Field(default_factory=list)


class SimpleProofRefinementSpec(BaseModel):
    method: Optional[str] = None
    hints: list[str] = Field(default_factory=list)
    referenced_lemmas: list[str] = Field(default_factory=list)
    referenced_hypotheses: list[str] = Field(default_factory=list)
    unresolved_details: list[str] = Field(default_factory=list)


class CalculationRefinementSpec(BaseModel):
    calculation_kind: Optional[str] = None
    steps: list[CalcStep] = Field(default_factory=list)
    unresolved_details: list[str] = Field(default_factory=list)


class LocalClaimRefinementSpec(BaseModel):
    statement: str
    label: Optional[str] = None
    proof: Optional[ChildProofSpec] = None
    notes: list[str] = Field(default_factory=list)


class DocumentChildSpec(BaseModel):
    id_suffix: str
    kind: Union[DocumentKind, str] = DocumentKind.unknown
    title: Optional[str] = None
    label: Optional[str] = None
    text: str
    notes: list[str] = Field(default_factory=list)
    data: dict = Field(default_factory=dict)
    proof_text: Optional[str] = None


class DocumentRefinementSpec(BaseModel):
    children: list[DocumentChildSpec]
    notes: list[str] = Field(default_factory=list)

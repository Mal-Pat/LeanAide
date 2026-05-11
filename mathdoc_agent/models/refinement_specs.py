from __future__ import annotations

from typing import Optional, Union

from pydantic import BaseModel, Field

from mathdoc_agent.models.base import DocumentKind, ProofKind
from mathdoc_agent.models.payloads import CalcStep


class MetadataEntry(BaseModel):
    key: str
    value: str


def metadata_entries_to_dict(entries: list[MetadataEntry]) -> dict[str, str]:
    return {entry.key: entry.value for entry in entries}


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


class StructuredProofRefinementSpec(BaseModel):
    strategy: Optional[str] = None
    summary: Optional[str] = None
    components: list[ChildProofSpec] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    conclusions: list[str] = Field(default_factory=list)
    witness: Optional[str] = None
    contradiction_assumption: Optional[str] = None
    reduced_to: Optional[str] = None
    invariant: Optional[str] = None
    construction: Optional[str] = None
    metadata: list[MetadataEntry] = Field(default_factory=list)
    unresolved_details: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class DocumentChildSpec(BaseModel):
    id_suffix: str
    kind: Union[DocumentKind, str] = DocumentKind.unknown
    title: Optional[str] = None
    label: Optional[str] = None
    text: str
    statement: Optional[str] = None
    notes: list[str] = Field(default_factory=list)
    data_entries: list[MetadataEntry] = Field(default_factory=list)
    proof_text: Optional[str] = None


class DocumentRefinementSpec(BaseModel):
    children: list[DocumentChildSpec]
    notes: list[str] = Field(default_factory=list)

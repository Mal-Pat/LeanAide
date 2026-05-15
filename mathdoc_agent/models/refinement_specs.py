from __future__ import annotations

from pydantic import BaseModel, Field

from mathdoc_agent.models.base import DocumentKind, ProofKind
from mathdoc_agent.models.payloads import (
    CalcStep,
    DeducedFromTheoremData,
    InductiveConstructorData,
    LogicalProofStepData,
    StructureFieldData,
)


class MetadataEntry(BaseModel):
    key: str
    value: str


def metadata_entries_to_dict(entries: list[MetadataEntry]) -> dict[str, str]:
    return {entry.key: entry.value for entry in entries}


class ChildProofSpec(BaseModel):
    id_suffix: str
    kind: ProofKind | str = ProofKind.unknown
    text: str
    goal: str | None = None
    hypotheses: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class InductionRefinementSpec(BaseModel):
    variable: str
    principle: str | None = None
    induction_hypotheses: list[str] = Field(default_factory=list)
    base_cases: list[ChildProofSpec]
    step_cases: list[ChildProofSpec]
    notes: list[str] = Field(default_factory=list)


class CasesRefinementSpec(BaseModel):
    split_on: str | None = None
    exhaustive_reason: str | None = None
    cases: list[ChildProofSpec]
    notes: list[str] = Field(default_factory=list)


class SimpleProofRefinementSpec(BaseModel):
    method: str | None = None
    hints: list[str] = Field(default_factory=list)
    referenced_lemmas: list[str] = Field(default_factory=list)
    referenced_hypotheses: list[str] = Field(default_factory=list)
    deduced_from_claim: list[str] = Field(default_factory=list)
    deduced_from_theorem: list[DeducedFromTheoremData] = Field(default_factory=list)
    proof_steps: list[LogicalProofStepData] = Field(default_factory=list)
    unresolved_details: list[str] = Field(default_factory=list)


class CalculationRefinementSpec(BaseModel):
    calculation_kind: str | None = None
    steps: list[CalcStep] = Field(default_factory=list)
    unresolved_details: list[str] = Field(default_factory=list)


class LocalClaimRefinementSpec(BaseModel):
    statement: str
    label: str | None = None
    proof: ChildProofSpec | None = None
    notes: list[str] = Field(default_factory=list)


class StructuredProofRefinementSpec(BaseModel):
    strategy: str | None = None
    summary: str | None = None
    components: list[ChildProofSpec] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    conclusions: list[str] = Field(default_factory=list)
    witness: str | None = None
    contradiction_assumption: str | None = None
    claim: str | None = None
    reduced_to: str | None = None
    proof_of_reduction: ChildProofSpec | None = None
    proof: ChildProofSpec | None = None
    invariant: str | None = None
    construction: str | None = None
    metadata: list[MetadataEntry] = Field(default_factory=list)
    unresolved_details: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class DocumentChildSpec(BaseModel):
    id_suffix: str
    kind: DocumentKind | str = DocumentKind.unknown
    title: str | None = None
    label: str | None = None
    text: str
    statement: str | None = None
    notes: list[str] = Field(default_factory=list)
    data_entries: list[MetadataEntry] = Field(default_factory=list)
    proof_text: str | None = None
    name: str | None = None
    is_class: bool | None = None
    is_prop: bool | None = None
    parameters: list[str] = Field(default_factory=list)
    extends: list[str] = Field(default_factory=list)
    fields: list[StructureFieldData] = Field(default_factory=list)
    class_name: str | None = None
    target: str | None = None
    value: str | None = None
    constructors: list[InductiveConstructorData] = Field(default_factory=list)


class DocumentRefinementSpec(BaseModel):
    children: list[DocumentChildSpec]
    notes: list[str] = Field(default_factory=list)

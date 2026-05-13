from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ProofKindData(BaseModel):
    pass


class DocumentKindData(BaseModel):
    pass


class StatementData(DocumentKindData):
    statement: str
    assumptions: list[str] = Field(default_factory=list)
    conclusion: Optional[str] = None


class DefinitionData(DocumentKindData):
    term: Optional[str] = None
    definiens: Optional[str] = None
    notation: Optional[str] = None


class SimpleProofData(ProofKindData):
    method: Optional[str] = None
    hints: list[str] = Field(default_factory=list)
    referenced_lemmas: list[str] = Field(default_factory=list)
    referenced_hypotheses: list[str] = Field(default_factory=list)


class InductionData(ProofKindData):
    variable: Optional[str] = None
    principle: Optional[str] = None
    base_case_ids: list[str] = Field(default_factory=list)
    step_case_ids: list[str] = Field(default_factory=list)
    induction_hypotheses: list[str] = Field(default_factory=list)


class CasesData(ProofKindData):
    split_on: Optional[str] = None
    exhaustive_reason: Optional[str] = None
    case_ids: list[str] = Field(default_factory=list)


class CalcRelation(str, Enum):
    eq = "="
    le = "<="
    lt = "<"
    ge = ">="
    gt = ">"
    iff = "<->"
    implies = "->"
    equiv_mod = "equiv_mod"


class CalcStep(BaseModel):
    lhs: str
    relation: CalcRelation
    rhs: str
    justification: Optional[str] = None
    side_conditions: list[str] = Field(default_factory=list)


class CalculationData(ProofKindData):
    calculation_kind: Optional[str] = None
    start: Optional[str] = None
    target: Optional[str] = None
    steps: list[CalcStep] = Field(default_factory=list)


class LocalClaimData(ProofKindData):
    statement: str
    proof_node_id: Optional[str] = None
    label: Optional[str] = None


class StructuredProofData(ProofKindData):
    strategy: Optional[str] = None
    summary: Optional[str] = None
    component_ids: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    conclusions: list[str] = Field(default_factory=list)
    witness: Optional[str] = None
    contradiction_assumption: Optional[str] = None
    reduced_to: Optional[str] = None
    invariant: Optional[str] = None
    construction: Optional[str] = None
    metadata: dict[str, str] = Field(default_factory=dict)

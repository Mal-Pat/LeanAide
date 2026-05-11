from __future__ import annotations

from mathdoc_agent.agents import definitions
from mathdoc_agent.handlers.proof_handlers import (
    CalculationHandler,
    CasesHandler,
    InductionHandler,
    LocalClaimHandler,
    OpaqueProofHandler,
    SimpleProofHandler,
    UnknownProofHandler,
)
from mathdoc_agent.models.base import ProofKind
from mathdoc_agent.registries.proof_handlers import ProofHandlerRegistry


def default_proof_handler_registry(
    *,
    classifier_agent=definitions.proof_classifier_agent,
    induction_agent=definitions.induction_agent,
    cases_agent=definitions.cases_agent,
    simple_agent=definitions.simple_proof_agent,
    calculation_agent=definitions.calculation_agent,
    local_claim_agent=None,
) -> ProofHandlerRegistry:
    registry = ProofHandlerRegistry()
    registry.register(ProofKind.unknown.value, UnknownProofHandler(classifier_agent))
    registry.register(ProofKind.opaque.value, OpaqueProofHandler())
    registry.register(ProofKind.induction.value, InductionHandler(induction_agent))
    registry.register(ProofKind.cases.value, CasesHandler(cases_agent))
    registry.register(ProofKind.simple.value, SimpleProofHandler(simple_agent))
    registry.register(ProofKind.calculation.value, CalculationHandler(calculation_agent))
    registry.register(ProofKind.local_claim.value, LocalClaimHandler(local_claim_agent))
    return registry

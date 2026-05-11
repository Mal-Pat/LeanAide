from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from mathdoc_agent.agents import prompts
from mathdoc_agent.models.refinement_specs import (
    CalculationRefinementSpec,
    CasesRefinementSpec,
    DocumentRefinementSpec,
    InductionRefinementSpec,
    SimpleProofRefinementSpec,
)

MODEL = os.environ.get("MATHDOC_AGENT_MODEL", "gpt-5.4")


@dataclass
class MissingAgentsSDKAgent:
    name: str
    model: str
    instructions: str
    output_type: type[Any] | None = None


def _agent(name: str, instructions: str, output_type: type[Any] | None = None) -> Any:
    try:
        from agents import Agent
    except ImportError:
        return MissingAgentsSDKAgent(
            name=name,
            model=MODEL,
            instructions=instructions,
            output_type=output_type,
        )
    return Agent(
        name=name,
        model=MODEL,
        instructions=instructions,
        output_type=output_type,
    )


document_parser_agent = _agent(
    "Document parser",
    prompts.DOCUMENT_PARSER_INSTRUCTIONS,
    DocumentRefinementSpec,
)
proof_classifier_agent = _agent(
    "Proof classifier",
    prompts.PROOF_CLASSIFIER_INSTRUCTIONS,
)
induction_agent = _agent(
    "Induction proof refiner",
    prompts.INDUCTION_INSTRUCTIONS,
    InductionRefinementSpec,
)
cases_agent = _agent(
    "Cases proof refiner",
    prompts.CASES_INSTRUCTIONS,
    CasesRefinementSpec,
)
simple_proof_agent = _agent(
    "Simple proof refiner",
    prompts.SIMPLE_PROOF_INSTRUCTIONS,
    SimpleProofRefinementSpec,
)
calculation_agent = _agent(
    "Calculation proof refiner",
    prompts.CALCULATION_INSTRUCTIONS,
    CalculationRefinementSpec,
)

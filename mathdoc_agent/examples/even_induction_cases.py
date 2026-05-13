from __future__ import annotations

import asyncio
from pathlib import Path

from mathdoc_agent.export.json import to_json
from mathdoc_agent.models.base import DocumentKind, ProofKind
from mathdoc_agent.models.refinement_specs import (
    CasesRefinementSpec,
    ChildProofSpec,
    DocumentChildSpec,
    DocumentRefinementSpec,
    InductionRefinementSpec,
    SimpleProofRefinementSpec,
)
from mathdoc_agent.orchestration.document_orchestrator import document_from_text, refine_math_document
from mathdoc_agent.plugins.document_types import default_document_handler_registry
from mathdoc_agent.plugins.proof_types import default_proof_handler_registry


SOURCE_TEXT = """Theorem. For every natural number n, either n is even or n+1 is even.

Proof. We prove this by induction on n. For n=0, n is even. For the induction
step, assume that either n is even or n+1 is even. We split into cases. If n is
even, then n=2k for some natural number k, hence n+2=2(k+1) is even, so the
right side of the desired disjunction holds. If n+1 is even, then the left side
of the desired disjunction holds."""


class DocumentParserAgent:
    def __call__(self, payload):
        return DocumentRefinementSpec(
            children=[
                DocumentChildSpec(
                    id_suffix="thm_even_or_next_even",
                    kind=DocumentKind.theorem,
                    label="thm:even_or_next_even",
                    text=SOURCE_TEXT,
                    statement="For every natural number n, either n is even or n+1 is even.",
                    proof_text=(
                        "We prove this by induction on n. For n=0, n is even. "
                        "For the induction step, assume that either n is even or n+1 is even. "
                        "We split into cases. If n is even, then n=2k for some natural number k, "
                        "hence n+2=2(k+1) is even, so the right side of the desired disjunction holds. "
                        "If n+1 is even, then the left side of the desired disjunction holds."
                    ),
                )
            ]
        )


class ProofClassifierAgent:
    def __call__(self, payload):
        text = payload["node"]["text"].lower()
        if "induction" in text:
            return {
                "kind": ProofKind.induction,
                "confidence": 0.99,
                "notes": ["Classified by explicit phrase: prove this by induction on n."],
            }
        if "split into cases" in text or "if n is even" in text:
            return {
                "kind": ProofKind.cases,
                "confidence": 0.99,
                "notes": ["Classified by explicit case split."],
            }
        return {
            "kind": ProofKind.simple,
            "confidence": 0.9,
            "notes": ["Leaf proof fragment."],
        }


class InductionAgent:
    def __call__(self, payload):
        return InductionRefinementSpec(
            variable="n",
            principle="ordinary induction on natural numbers starting at 0",
            induction_hypotheses=["Either n is even or n+1 is even."],
            base_cases=[
                ChildProofSpec(
                    id_suffix="base_n_eq_0",
                    kind=ProofKind.simple,
                    text="Base case n=0: 0 is even, so either 0 is even or 1 is even.",
                    goal="Either 0 is even or 0+1 is even.",
                    hypotheses=["n = 0"],
                )
            ],
            step_cases=[
                ChildProofSpec(
                    id_suffix="step_cases",
                    kind=ProofKind.cases,
                    text=(
                        "Induction step: assume either n is even or n+1 is even. "
                        "Split into the case that n is even and the case that n+1 is even."
                    ),
                    goal="Either n+1 is even or n+2 is even.",
                    hypotheses=["Either n is even or n+1 is even."],
                )
            ],
            notes=["The induction handler creates one base child and one step child."],
        )


class CasesAgent:
    def __call__(self, payload):
        return CasesRefinementSpec(
            split_on="the induction hypothesis: either n is even or n+1 is even",
            exhaustive_reason="The induction hypothesis is exactly a disjunction with these two cases.",
            cases=[
                ChildProofSpec(
                    id_suffix="case_n_even",
                    kind=ProofKind.simple,
                    text=(
                        "Case 1: n is even. Then n=2k for some k, so n+2=2(k+1) is even. "
                        "Thus the right disjunct of the goal, n+2 is even, holds."
                    ),
                    goal="Either n+1 is even or n+2 is even.",
                    hypotheses=["n is even"],
                ),
                ChildProofSpec(
                    id_suffix="case_next_even",
                    kind=ProofKind.simple,
                    text=(
                        "Case 2: n+1 is even. This is exactly the left disjunct of the goal, "
                        "so either n+1 is even or n+2 is even."
                    ),
                    goal="Either n+1 is even or n+2 is even.",
                    hypotheses=["n+1 is even"],
                ),
            ],
            notes=["The cases handler splits the induction step into the two IH alternatives."],
        )


class SimpleProofAgent:
    def __call__(self, payload):
        node = payload["node"]
        return SimpleProofRefinementSpec(
            method="direct proof",
            hints=[node["text"]],
            referenced_hypotheses=node.get("hypotheses", []),
        )


def build_registries():
    document_registry = default_document_handler_registry(parser_agent=DocumentParserAgent())
    proof_registry = default_proof_handler_registry(
        classifier_agent=ProofClassifierAgent(),
        induction_agent=InductionAgent(),
        cases_agent=CasesAgent(),
        simple_agent=SimpleProofAgent(),
    )
    return document_registry, proof_registry


async def build_document_json() -> str:
    document_registry, proof_registry = build_registries()
    document = document_from_text(
        SOURCE_TEXT,
        id="even_induction_cases",
        title="Evenness Alternates for Natural Numbers",
    )
    refined = await refine_math_document(
        document,
        document_registry,
        proof_registry,
        document_iterations=5,
        proof_iterations=20,
    )
    return to_json(refined, indent=2)


def main() -> None:
    output_path = Path(__file__).with_name("even_induction_cases.json")
    output_path.write_text(asyncio.run(build_document_json()), encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()

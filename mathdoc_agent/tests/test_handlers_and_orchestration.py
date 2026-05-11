from __future__ import annotations

import unittest
import json

from mathdoc_agent.export.json import to_json
from mathdoc_agent.models.base import DocumentKind, NodeStatus, ProofKind
from mathdoc_agent.models.payloads import CalcRelation, CalcStep, LocalClaimData
from mathdoc_agent.models.proof import ProofNode, ProofTree
from mathdoc_agent.models.refinement_specs import (
    CalculationRefinementSpec,
    CasesRefinementSpec,
    ChildProofSpec,
    DocumentChildSpec,
    DocumentRefinementSpec,
    InductionRefinementSpec,
    SimpleProofRefinementSpec,
)
from mathdoc_agent.orchestration.context import build_proof_context
from mathdoc_agent.orchestration.document_orchestrator import document_from_text, refine_math_document
from mathdoc_agent.orchestration.proof_orchestrator import refine_proof_tree
from mathdoc_agent.orchestration.worklist import walk_proof_nodes
from mathdoc_agent.plugins.document_types import default_document_handler_registry
from mathdoc_agent.plugins.proof_types import default_proof_handler_registry
from mathdoc_agent.validation.deterministic import validate_unique_proof_ids


class ClassifierAgent:
    def __call__(self, payload):
        text = payload["node"]["text"]
        if "induction" in text:
            return {"kind": "induction", "confidence": 0.9}
        if "cases" in text:
            return {"kind": "cases", "confidence": 0.9}
        if "calc" in text:
            return {"kind": "calculation", "confidence": 0.9}
        return {"kind": "simple", "confidence": 0.9}


class InductionAgent:
    def __call__(self, payload):
        text = payload["node"]["text"]
        if "nested induction" in text:
            return InductionRefinementSpec(
                variable="m",
                base_cases=[ChildProofSpec(id_suffix="base", kind=ProofKind.simple, text="nested base")],
                step_cases=[ChildProofSpec(id_suffix="step", kind=ProofKind.simple, text="nested step")],
            )
        return InductionRefinementSpec(
            variable="n",
            induction_hypotheses=["P n"],
            base_cases=[ChildProofSpec(id_suffix="base", kind=ProofKind.simple, text="base follows from L0")],
            step_cases=[ChildProofSpec(id_suffix="step", kind=ProofKind.cases, text="step cases")],
        )


class CasesAgent:
    def __call__(self, payload):
        text = payload["node"]["text"]
        if "nested cases" in text:
            return CasesRefinementSpec(
                split_on="R",
                cases=[
                    ChildProofSpec(id_suffix="r", kind=ProofKind.simple, text="R case"),
                    ChildProofSpec(id_suffix="not_r", kind=ProofKind.simple, text="not R case"),
                ],
            )
        return CasesRefinementSpec(
            split_on="Q(n)",
            cases=[
                ChildProofSpec(id_suffix="nested_induction", kind=ProofKind.induction, text="nested induction"),
                ChildProofSpec(id_suffix="nested_cases", kind=ProofKind.cases, text="nested cases"),
                ChildProofSpec(id_suffix="easy", kind=ProofKind.simple, text="easy case"),
            ],
        )


class SimpleAgent:
    def __call__(self, payload):
        return SimpleProofRefinementSpec(hints=[f"refine {payload['node']['id']}"])


class CalculationAgent:
    def __call__(self, payload):
        return CalculationRefinementSpec(
            calculation_kind="equality_chain",
            steps=[
                CalcStep(lhs="a", relation=CalcRelation.eq, rhs="b"),
                CalcStep(lhs="b", relation=CalcRelation.eq, rhs="c"),
            ],
        )


class DocumentParserAgent:
    def __call__(self, payload):
        return DocumentRefinementSpec(
            children=[
                DocumentChildSpec(
                    id_suffix="thm1",
                    kind=DocumentKind.theorem,
                    label="thm:p",
                    text="Theorem. P. Proof. simple proof.",
                    data={"statement": "P"},
                    proof_text="simple proof.",
                )
            ]
        )


def proof_registry():
    return default_proof_handler_registry(
        classifier_agent=ClassifierAgent(),
        induction_agent=InductionAgent(),
        cases_agent=CasesAgent(),
        simple_agent=SimpleAgent(),
        calculation_agent=CalculationAgent(),
    )


class HandlerAndOrchestrationTests(unittest.IsolatedAsyncioTestCase):
    async def test_nested_proof_orchestration_resolves_tree(self) -> None:
        tree = ProofTree(
            id="p",
            theorem_statement="forall n, P n",
            root=ProofNode(
                id="p.root",
                kind=ProofKind.unknown,
                status=NodeStatus.raw,
                text="outer induction",
            ),
        )
        refined = await refine_proof_tree(tree, proof_registry(), max_iterations=30)
        self.assertEqual(refined.root.status, NodeStatus.resolved)
        self.assertTrue(all(node.status == NodeStatus.resolved for node in walk_proof_nodes(refined.root)))
        self.assertTrue(validate_unique_proof_ids(refined.root).ok)

        nested_case = next(node for node in walk_proof_nodes(refined.root) if node.id.endswith("nested_cases.r"))
        context = build_proof_context(refined, nested_case.id)
        self.assertTrue(any("Induction on n" in item for item in context.active_inductions))
        self.assertTrue(any("Case split on Q(n)" in item for item in context.active_cases))

    async def test_document_orchestrator_refines_attached_proof(self) -> None:
        document = document_from_text("Theorem. P. Proof. simple proof.", title="Tiny")
        refined = await refine_math_document(
            document,
            default_document_handler_registry(parser_agent=DocumentParserAgent()),
            proof_registry(),
        )
        theorem = refined.root.children[0]
        self.assertEqual(refined.root.status, NodeStatus.resolved)
        dumped = refined.model_dump()
        self.assertEqual(dumped["type"], "document")
        self.assertEqual(dumped["document"]["type"], "document")
        self.assertEqual(dumped["document"]["body"][0]["type"], "Theorem")
        self.assertEqual(refined.root.model_dump()["type"], "document")
        self.assertEqual(theorem.model_dump()["type"], "Theorem")
        self.assertIsNotNone(theorem.proof)
        self.assertEqual(theorem.proof.model_dump()["type"], "ProofDetails")
        self.assertEqual(theorem.proof.root.status, NodeStatus.resolved)
        self.assertEqual(theorem.proof.root.model_dump()["type"], "assert_statement")
        self.assertEqual(len(refined.run_log), 1)
        exported = json.loads(to_json(refined))
        self.assertEqual(exported["type"], "document")
        self.assertEqual(exported["document"]["body"][0]["type"], "Theorem")
        self.assertNotIn("kind", exported["root"])
        self.assertNotIn("kind", exported["document"]["body"][0])

    def test_earlier_sibling_local_claim_is_in_context(self) -> None:
        claim = ProofNode(
            id="p.claim",
            kind=ProofKind.local_claim,
            status=NodeStatus.resolved,
            text="Claim. Q.",
            data=LocalClaimData(statement="Q").model_dump(),
        )
        later = ProofNode(
            id="p.later",
            kind=ProofKind.simple,
            status=NodeStatus.classified,
            text="Using the claim, finish.",
        )
        tree = ProofTree(
            id="p",
            theorem_statement="P",
            root=ProofNode(
                id="p.root",
                kind=ProofKind.cases,
                status=NodeStatus.decomposed,
                text="proof",
                children=[claim, later],
            ),
        )
        context = build_proof_context(tree, "p.later")
        self.assertIn("Q", context.local_claims)


if __name__ == "__main__":
    unittest.main()

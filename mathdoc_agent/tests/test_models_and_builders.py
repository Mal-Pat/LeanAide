from __future__ import annotations

import unittest

from mathdoc_agent.builders.document_builder import DocumentBuilder
from mathdoc_agent.builders.proof_builder import ProofBuilder
from mathdoc_agent.models.base import DocumentKind, NodeStatus, ProofKind
from mathdoc_agent.models.document import DocumentNode
from mathdoc_agent.models.payloads import CalcRelation, CalcStep, InductionData
from mathdoc_agent.models.proof import ProofNode, ProofTree
from mathdoc_agent.registries.proof_registry import proof_payload_registry


class ModelAndBuilderTests(unittest.TestCase):
    def test_proof_node_json_round_trip(self) -> None:
        node = ProofBuilder.simple(
            id="p.root",
            text="The result follows from L.",
            hints=["use L"],
        )
        tree = ProofTree(id="p", theorem_statement="P", root=node)
        round_trip = ProofTree.model_validate_json(tree.model_dump_json())
        self.assertEqual(round_trip.root.id, "p.root")
        self.assertEqual(round_trip.root.status, NodeStatus.resolved)

    def test_document_node_with_proof_round_trip(self) -> None:
        node = DocumentBuilder.theorem_like(
            id="doc.thm1",
            kind=DocumentKind.theorem,
            text="Theorem. P. Proof. Trivial.",
            statement="P",
            proof_text="Trivial.",
            label="thm:p",
        )
        round_trip = DocumentNode.model_validate_json(node.model_dump_json())
        self.assertIsNotNone(round_trip.proof)
        self.assertEqual(round_trip.proof.root.kind, ProofKind.unknown)

    def test_payload_registry_validates_known_and_ignores_unknown(self) -> None:
        data = proof_payload_registry.validate_data(
            ProofKind.induction,
            {"variable": "n", "base_case_ids": ["b"], "step_case_ids": ["s"]},
        )
        self.assertIsInstance(data, InductionData)
        self.assertIsNone(proof_payload_registry.validate_data("custom_kind", {}))

    def test_builders_create_expected_payloads(self) -> None:
        base = ProofNode(id="p.base", kind=ProofKind.simple, text="base")
        step = ProofNode(id="p.step", kind=ProofKind.simple, text="step")
        induction = ProofBuilder.induction(
            id="p",
            text="induct on n",
            variable="n",
            base_cases=[base],
            step_cases=[step],
        )
        data = InductionData.model_validate(induction.data)
        self.assertEqual(data.base_case_ids, ["p.base"])
        self.assertEqual(data.step_case_ids, ["p.step"])

        calc = ProofBuilder.calculation(
            id="c",
            text="a = b = c",
            steps=[
                CalcStep(lhs="a", relation=CalcRelation.eq, rhs="b"),
                CalcStep(lhs="b", relation=CalcRelation.eq, rhs="c"),
            ],
        )
        self.assertEqual(calc.data["start"], "a")
        self.assertEqual(calc.data["target"], "c")


if __name__ == "__main__":
    unittest.main()

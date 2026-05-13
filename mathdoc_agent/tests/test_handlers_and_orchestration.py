from __future__ import annotations

import io
import json
import unittest
from contextlib import redirect_stderr

from mathdoc_agent.export.json import to_json
from mathdoc_agent.mathagents.runner import run_agent_typed
from mathdoc_agent.models.base import DocumentKind, NodeStatus, ProofKind
from mathdoc_agent.models.payloads import (
    CalcRelation,
    CalcStep,
    InductiveConstructorData,
    LocalClaimData,
    StructuredProofData,
    StructureFieldData,
)
from mathdoc_agent.models.proof import ProofNode, ProofTree
from mathdoc_agent.models.refinement_specs import (
    CalculationRefinementSpec,
    CasesRefinementSpec,
    ChildProofSpec,
    DocumentChildSpec,
    DocumentRefinementSpec,
    InductionRefinementSpec,
    SimpleProofRefinementSpec,
    StructuredProofRefinementSpec,
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


class NamedLoggingAgent:
    name = "Named logging agent"

    def __call__(self, payload):
        return SimpleProofRefinementSpec(hints=["logged"])


class CalculationAgent:
    def __call__(self, payload):
        return CalculationRefinementSpec(
            calculation_kind="equality_chain",
            steps=[
                CalcStep(lhs="a", relation=CalcRelation.eq, rhs="b"),
                CalcStep(lhs="b", relation=CalcRelation.eq, rhs="c"),
            ],
        )


class StructuredAgent:
    def __call__(self, payload):
        proof_kind = payload["proof_kind"]
        if proof_kind == ProofKind.equivalence.value:
            return StructuredProofRefinementSpec(
                strategy="prove both implications",
                summary="Split the equivalence into forward and reverse directions.",
                components=[
                    ChildProofSpec(
                        id_suffix="forward",
                        kind=ProofKind.simple,
                        text="Assume P and prove Q.",
                        goal="P implies Q",
                        hypotheses=["P"],
                    ),
                    ChildProofSpec(
                        id_suffix="reverse",
                        kind=ProofKind.simple,
                        text="Assume Q and prove P.",
                        goal="Q implies P",
                        hypotheses=["Q"],
                    ),
                ],
            )
        return StructuredProofRefinementSpec(
            strategy=f"structured {proof_kind} proof",
            summary="Single unresolved structured proof.",
            unresolved_details=["No decomposition supplied by fake agent."],
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
                    statement="P",
                    proof_text="simple proof.",
                )
            ]
        )


class ProofParagraphDocumentParserAgent:
    def __call__(self, payload):
        return DocumentRefinementSpec(
            children=[
                DocumentChildSpec(
                    id_suffix="theorem",
                    kind=DocumentKind.theorem,
                    label="thm:p",
                    text="Theorem. P.",
                    statement="P",
                ),
                DocumentChildSpec(
                    id_suffix="proof",
                    kind=DocumentKind.paragraph,
                    text="Proof. This follows directly.",
                ),
            ]
        )


class DefinitionDocumentParserAgent:
    def __call__(self, payload):
        return DocumentRefinementSpec(
            children=[
                DocumentChildSpec(
                    id_suffix="group",
                    kind=DocumentKind.structure_definition,
                    text="A group is a type with multiplication, identity, and inverses.",
                    name="Group",
                    is_class=True,
                    fields=[
                        StructureFieldData(name="mul", type="G -> G -> G"),
                        StructureFieldData(name="one", type="G"),
                    ],
                ),
                DocumentChildSpec(
                    id_suffix="int_group",
                    kind=DocumentKind.instance_definition,
                    text="The integers form a group under addition.",
                    name="instIntGroup",
                    class_name="Group",
                    target="Int",
                    fields=[StructureFieldData(name="mul", type="Int.add")],
                    value="integer addition group structure",
                ),
                DocumentChildSpec(
                    id_suffix="even",
                    kind=DocumentKind.inductive_type_definition,
                    text="Even is generated by zero and adding two.",
                    name="Even",
                    is_prop=True,
                    parameters=["n : Nat"],
                    constructors=[
                        InductiveConstructorData(name="zero", arguments=[]),
                        InductiveConstructorData(name="step", arguments=["Even n"]),
                    ],
                ),
            ]
        )


def proof_registry():
    return default_proof_handler_registry(
        classifier_agent=ClassifierAgent(),
        induction_agent=InductionAgent(),
        cases_agent=CasesAgent(),
        simple_agent=SimpleAgent(),
        calculation_agent=CalculationAgent(),
        structured_agent=StructuredAgent(),
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

    async def test_structured_equivalence_handler_decomposes_directions(self) -> None:
        tree = ProofTree(
            id="iff",
            theorem_statement="P iff Q",
            root=ProofNode(
                id="iff.root",
                kind=ProofKind.equivalence,
                status=NodeStatus.classified,
                text="We prove both directions.",
                goal="P iff Q",
            ),
        )
        refined = await refine_proof_tree(tree, proof_registry(), max_iterations=10)
        self.assertEqual(refined.root.status, NodeStatus.resolved)
        self.assertEqual(refined.root.kind, ProofKind.equivalence)
        self.assertEqual(refined.root.model_dump()["type"], "bi-implication_cases_proof")
        self.assertEqual([child.id for child in refined.root.children], ["iff.root.forward", "iff.root.reverse"])
        self.assertTrue(all(child.status == NodeStatus.resolved for child in refined.root.children))

    async def test_simple_proof_preserves_intermediate_steps(self) -> None:
        tree = ProofTree(
            id="group",
            theorem_statement="G is Abelian",
            root=ProofNode(
                id="group.root",
                kind=ProofKind.simple,
                status=NodeStatus.classified,
                goal="G is Abelian",
                text=(
                    "Let G be a group satisfying the square identity. "
                    "Fix arbitrary elements a,b in G. We want to prove that ab = ba. "
                    "\\[abab = aabb\\] "
                    "\\[bab = abb\\] "
                    "\\[ba = ab\\] "
                    "Therefore G is Abelian."
                ),
            ),
        )
        refined = await refine_proof_tree(tree, proof_registry(), max_iterations=5)
        exported = json.loads(to_json(refined))
        self.assertEqual(exported["type"], "Proof")
        self.assertGreaterEqual(len(exported["proof_steps"]), 5)
        self.assertTrue(any(step["type"] == "let_statement" for step in exported["proof_steps"]))
        self.assertTrue(any(step["type"] == "assume_statement" for step in exported["proof_steps"]))
        self.assertTrue(any(step.get("claim") == "ba = ab" for step in exported["proof_steps"]))

    async def test_agent_runner_logs_to_stderr(self) -> None:
        stderr = io.StringIO()
        payload = {"node": {"id": "p.root", "kind": "simple"}}
        with redirect_stderr(stderr):
            result = await run_agent_typed(NamedLoggingAgent(), payload, SimpleProofRefinementSpec)

        self.assertEqual(result.hints, ["logged"])
        logs = stderr.getvalue()
        self.assertIn("calling Named logging agent -> SimpleProofRefinementSpec", logs)
        self.assertIn("completed Named logging agent -> SimpleProofRefinementSpec", logs)
        self.assertIn("node=p.root", logs)

    def test_default_registry_has_reasonable_taxonomy_handlers(self) -> None:
        registry = proof_registry()
        for kind in (
            ProofKind.contradiction,
            ProofKind.contrapositive,
            ProofKind.existence,
            ProofKind.uniqueness,
            ProofKind.equivalence,
            ProofKind.construction,
            ProofKind.minimal_counterexample,
            ProofKind.infinite_descent,
            ProofKind.exhaustion,
            ProofKind.counting,
            ProofKind.pigeonhole,
            ProofKind.invariant,
            ProofKind.reduction,
            ProofKind.epsilon_delta,
            ProofKind.generic_element,
            ProofKind.local_to_global,
            ProofKind.compactness,
            ProofKind.density,
            ProofKind.approximation,
            ProofKind.universal_property,
            ProofKind.algorithmic,
            ProofKind.probabilistic,
        ):
            self.assertEqual(registry.get(kind.value).kind, kind.value)

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
        self.assertEqual(set(exported.keys()), {"document"})
        self.assertEqual(exported["document"]["type"], "document")
        self.assertEqual(exported["document"]["body"][0]["type"], "Theorem")
        self.assertEqual(exported["document"]["body"][0]["claim"], "P")
        self.assertNotIn("root", exported)
        self.assertNotIn("run_log", exported)
        self.assertNotIn("kind", exported["document"]["body"][0])

    async def test_document_parser_supports_lean_definition_kinds(self) -> None:
        document = document_from_text("Definitions for algebraic structures.", title="Defs")
        refined = await refine_math_document(
            document,
            default_document_handler_registry(parser_agent=DefinitionDocumentParserAgent()),
            proof_registry(),
        )
        body = json.loads(to_json(refined))["document"]["body"]
        self.assertEqual(body[0]["type"], "structure-definition")
        self.assertEqual(body[0]["name"], "Group")
        self.assertTrue(body[0]["is_class"])
        self.assertEqual(body[0]["fields"][0]["name"], "mul")
        self.assertEqual(body[1]["type"], "instance-definition")
        self.assertEqual(body[1]["class_name"], "Group")
        self.assertEqual(body[1]["target"], "Int")
        self.assertEqual(body[1]["fields"]["mul"], "Int.add")
        self.assertEqual(body[2]["type"], "inductive-type-definition")
        self.assertEqual(body[2]["name"], "Even")
        self.assertTrue(body[2]["is_prop"])
        self.assertEqual(body[2]["constructors"][1]["arguments"], ["Even n"])

    async def test_proof_paragraph_attaches_to_preceding_theorem(self) -> None:
        document = document_from_text("Theorem. P.\n\nProof. This follows directly.", title="Proof Paragraph")
        refined = await refine_math_document(
            document,
            default_document_handler_registry(parser_agent=ProofParagraphDocumentParserAgent()),
            proof_registry(),
        )
        self.assertEqual(len(refined.root.children), 1)
        theorem = refined.root.children[0]
        self.assertIsNotNone(theorem.proof)
        self.assertEqual(theorem.proof.root.status, NodeStatus.resolved)
        body = json.loads(to_json(refined))["document"]["body"]
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]["type"], "Theorem")
        self.assertIn("proof", body[0])

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

    def test_export_flattens_instructional_proof_wrappers(self) -> None:
        root = ProofNode(
            id="metric.root",
            kind=ProofKind.contradiction,
            status=NodeStatus.resolved,
            text="Proof by contradiction.",
            data=StructuredProofData(
                contradiction_assumption="There exists z in the intersection.",
            ).model_dump(),
            children=[
                ProofNode(
                    id="metric.root.setup",
                    kind=ProofKind.existence,
                    status=NodeStatus.resolved,
                    goal="Set up the negation of the desired disjointness claim.",
                    text="Assume a point lies in both balls.",
                    children=[
                        ProofNode(
                            id="metric.root.setup.obtain",
                            kind=ProofKind.construction,
                            status=NodeStatus.resolved,
                            goal="Obtain a witness point in the intersection.",
                            text="Choose z in the intersection.",
                            children=[
                                ProofNode(
                                    id="metric.root.setup.obtain.verify",
                                    kind=ProofKind.simple,
                                    status=NodeStatus.resolved,
                                    goal="Verify that the witness lies in the required intersection.",
                                    text="The chosen point z lies in both balls.",
                                )
                            ],
                        )
                    ],
                )
            ],
        )
        exported = json.loads(to_json(ProofTree(id="metric", theorem_statement="P", root=root)))
        proof_steps = exported["proof"]["proof_steps"]
        self.assertEqual(len(proof_steps), 1)
        self.assertEqual(proof_steps[0]["type"], "assert_statement")
        self.assertEqual(proof_steps[0]["claim"], "The chosen point z lies in both balls.")
        self.assertNotIn("Set up", json.dumps(exported))
        self.assertNotIn("Obtain a witness", json.dumps(exported))
        self.assertNotIn("Verify that", json.dumps(exported))

    def test_export_removes_metric_style_instructional_claims(self) -> None:
        root = ProofNode(
            id="metric.root",
            kind=ProofKind.contradiction,
            status=NodeStatus.resolved,
            text="Proof by contradiction.",
            data=StructuredProofData(
                contradiction_assumption="\\(B(x,\\varepsilon/3)\\cap B(y,\\varepsilon/3)\\ne\\varnothing\\)",
            ).model_dump(),
            children=[
                ProofNode(
                    id="metric.root.assumption",
                    kind=ProofKind.contradiction,
                    status=NodeStatus.resolved,
                    text="Assume the balls intersect and derive consequences.",
                    data=StructuredProofData(
                        contradiction_assumption="\\(B(x,\\varepsilon/3)\\cap B(y,\\varepsilon/3)\\ne\\varnothing\\)",
                    ).model_dump(),
                    children=[
                        ProofNode(
                            id="metric.root.assumption.negated_assumption",
                            kind=ProofKind.simple,
                            status=NodeStatus.resolved,
                            goal="Negate the desired disjointness conclusion.",
                            text="Assume for contradiction that \\(B(x,\\varepsilon/3)\\cap B(y,\\varepsilon/3)\\ne\\varnothing\\).",
                        ),
                        ProofNode(
                            id="metric.root.assumption.witness",
                            kind=ProofKind.construction,
                            status=NodeStatus.resolved,
                            goal="Produce a witness in the intersection.",
                            text="Produce a witness in the intersection.",
                            children=[
                                ProofNode(
                                    id="metric.root.assumption.witness.task",
                                    kind=ProofKind.simple,
                                    status=NodeStatus.resolved,
                                    goal="Produce a witness in the intersection.",
                                    text="Produce a witness in the intersection.",
                                ),
                                ProofNode(
                                    id="metric.root.assumption.witness.membership",
                                    kind=ProofKind.simple,
                                    status=NodeStatus.resolved,
                                    goal="\\(z\\in B(x,\\varepsilon/3)\\cap B(y,\\varepsilon/3)\\)",
                                    text="\\(z\\in B(x,\\varepsilon/3)\\cap B(y,\\varepsilon/3)\\)",
                                ),
                            ],
                        ),
                    ],
                ),
                ProofNode(
                    id="metric.root.conclusion",
                    kind=ProofKind.construction,
                    status=NodeStatus.resolved,
                    goal="Conclude the desired disjointness statement.",
                    text="Therefore the balls are disjoint.",
                    children=[
                        ProofNode(
                            id="metric.root.conclusion.final",
                            kind=ProofKind.simple,
                            status=NodeStatus.resolved,
                            goal="\\(B(x,\\varepsilon/3)\\cap B(y,\\varepsilon/3)=\\varnothing\\)",
                            text="\\(B(x,\\varepsilon/3)\\cap B(y,\\varepsilon/3)=\\varnothing\\)",
                        )
                    ],
                ),
            ],
        )
        exported = json.loads(to_json(ProofTree(id="metric", theorem_statement="P", root=root)))
        dumped = json.dumps(exported)
        self.assertNotIn("Negate the desired", dumped)
        self.assertNotIn("Produce a witness", dumped)
        self.assertNotIn("Conclude the desired", dumped)

        nested_steps = exported["proof"]["proof_steps"][0]["proof"]["proof_steps"]
        self.assertEqual(nested_steps[0]["type"], "assume_statement")
        self.assertEqual(
            nested_steps[0]["assumption"],
            "\\(B(x,\\varepsilon/3)\\cap B(y,\\varepsilon/3)\\ne\\varnothing\\)",
        )
        self.assertEqual(nested_steps[1]["claim"], "\\(z\\in B(x,\\varepsilon/3)\\cap B(y,\\varepsilon/3)\\)")
        self.assertEqual(
            exported["proof"]["proof_steps"][1]["claim"],
            "\\(B(x,\\varepsilon/3)\\cap B(y,\\varepsilon/3)=\\varnothing\\)",
        )

    def test_export_turns_mathematical_proof_wrappers_into_claims(self) -> None:
        root = ProofNode(
            id="metric.root",
            kind=ProofKind.contradiction,
            status=NodeStatus.resolved,
            text="Proof by contradiction.",
            data=StructuredProofData(
                contradiction_assumption="B(x,ε/3)∩B(y,ε/3)≠∅",
            ).model_dump(),
            children=[
                ProofNode(
                    id="metric.root.assumption",
                    kind=ProofKind.construction,
                    status=NodeStatus.resolved,
                    goal="B(x,ε/3)∩B(y,ε/3)≠∅",
                    text="Assume the intersection is nonempty.",
                    children=[
                        ProofNode(
                            id="metric.root.witness",
                            kind=ProofKind.construction,
                            status=NodeStatus.resolved,
                            goal="∃z∈X, z∈B(x,ε/3) ∧ z∈B(y,ε/3)",
                            text="Choose a witness in the intersection.",
                            children=[
                                ProofNode(
                                    id="metric.root.witness.duplicate",
                                    kind=ProofKind.construction,
                                    status=NodeStatus.resolved,
                                    goal="∃z∈X, z∈B(x,ε/3) ∧ z∈B(y,ε/3)",
                                    text="Choose a witness in the intersection.",
                                    children=[
                                        ProofNode(
                                            id="metric.root.witness.membership",
                                            kind=ProofKind.simple,
                                            status=NodeStatus.resolved,
                                            goal="z∈B(x,ε/3)∩B(y,ε/3)",
                                            text="z∈B(x,ε/3)∩B(y,ε/3)",
                                        )
                                    ],
                                )
                            ],
                        )
                    ],
                )
            ],
        )
        exported = json.loads(to_json(ProofTree(id="metric", theorem_statement="P", root=root)))
        dumped = json.dumps(exported)
        self.assertNotIn("claim_label", dumped)

        proof_step = exported["proof"]["proof_steps"][0]
        self.assertEqual(proof_step["type"], "Theorem")
        self.assertEqual(proof_step["header"], "Claim")
        self.assertEqual(proof_step["claim"], "∃z∈X, z∈B(x,ε/3) ∧ z∈B(y,ε/3)")
        self.assertEqual(len(proof_step["proof"]["proof_steps"]), 1)
        self.assertEqual(proof_step["proof"]["proof_steps"][0]["claim"], "z∈B(x,ε/3)∩B(y,ε/3)")


if __name__ == "__main__":
    unittest.main()

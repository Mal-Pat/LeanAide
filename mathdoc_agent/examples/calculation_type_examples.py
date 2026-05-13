from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path

from mathdoc_agent.builders.proof_builder import ProofBuilder
from mathdoc_agent.export.json import to_json
from mathdoc_agent.models.base import DocumentKind, NodeStatus
from mathdoc_agent.models.document import DocumentNode, MathDocument
from mathdoc_agent.models.payloads import CalcRelation, CalcStep, StatementData
from mathdoc_agent.models.proof import ProofTree


@dataclass(frozen=True)
class CalculationExample:
    slug: str
    title: str
    label: str
    statement: str
    calculation_kind: str
    proof_text: str
    steps: tuple[CalcStep, ...]

    @property
    def source_text(self) -> str:
        return f"Theorem. {self.statement}\n\nProof. {self.proof_text}"


EXAMPLES: tuple[CalculationExample, ...] = (
    CalculationExample(
        slug="equality_chain_square_sum",
        title="Equality Chain",
        label="calc:equality_chain",
        statement="The expression (x+1)^2 equals x^2+2*x+1.",
        calculation_kind="equality_chain",
        proof_text="Expand the square and collect terms.",
        steps=(
            CalcStep(lhs="(x+1)^2", relation=CalcRelation.eq, rhs="x^2 + 2*x + 1", justification="ring"),
        ),
    ),
    CalculationExample(
        slug="inequality_chain_order_bound",
        title="Inequality Chain",
        label="calc:inequality_chain",
        statement="If a ≤ b and b ≤ c, then a ≤ c.",
        calculation_kind="inequality_chain",
        proof_text="Chain the two inequalities.",
        steps=(
            CalcStep(lhs="a", relation=CalcRelation.le, rhs="b", justification="hypothesis hab"),
            CalcStep(lhs="b", relation=CalcRelation.le, rhs="c", justification="hypothesis hbc"),
        ),
    ),
    CalculationExample(
        slug="mixed_relation_chain_nonnegative",
        title="Mixed Relation Chain",
        label="calc:mixed_relation_chain",
        statement="If x= y and y < z, then x < z.",
        calculation_kind="mixed_relation_chain",
        proof_text="Rewrite by x=y and then use y<z.",
        steps=(
            CalcStep(lhs="x", relation=CalcRelation.eq, rhs="y", justification="hypothesis hxy"),
            CalcStep(lhs="y", relation=CalcRelation.lt, rhs="z", justification="hypothesis hyz"),
        ),
    ),
    CalculationExample(
        slug="rewrite_by_hypothesis",
        title="Rewrite by Hypothesis",
        label="calc:rewrite_by_hypothesis",
        statement="If x=y, then f x = f y.",
        calculation_kind="rewrite_by_hypothesis",
        proof_text="Rewrite x to y using the hypothesis.",
        steps=(
            CalcStep(lhs="f x", relation=CalcRelation.eq, rhs="f y", justification="rewrite by hxy"),
        ),
    ),
    CalculationExample(
        slug="rewrite_by_lemma",
        title="Rewrite by Lemma",
        label="calc:rewrite_by_lemma",
        statement="x+0 = x.",
        calculation_kind="rewrite_by_lemma",
        proof_text="Rewrite using the add_zero lemma.",
        steps=(
            CalcStep(lhs="x + 0", relation=CalcRelation.eq, rhs="x", justification="add_zero"),
        ),
    ),
    CalculationExample(
        slug="definition_unfolding",
        title="Definition Unfolding",
        label="calc:definition_unfolding",
        statement="double x = x+x.",
        calculation_kind="definition_unfolding",
        proof_text="Unfold the definition of double.",
        steps=(
            CalcStep(lhs="double x", relation=CalcRelation.eq, rhs="x + x", justification="unfold double"),
        ),
    ),
    CalculationExample(
        slug="normalization",
        title="Normalization",
        label="calc:normalization",
        statement="(x+y)^2 normalizes to x^2+2*x*y+y^2.",
        calculation_kind="normalization",
        proof_text="Normalize the polynomial expression.",
        steps=(
            CalcStep(lhs="(x+y)^2", relation=CalcRelation.eq, rhs="x^2 + 2*x*y + y^2", justification="ring_nf"),
        ),
    ),
    CalculationExample(
        slug="positivity_side_goal",
        title="Positivity Side Goal",
        label="calc:positivity_side_goal",
        statement="If 0<x and 0<y, then 0<x*y.",
        calculation_kind="positivity_side_goal",
        proof_text="Use positivity of the factors as side conditions.",
        steps=(
            CalcStep(
                lhs="0",
                relation=CalcRelation.lt,
                rhs="x*y",
                justification="positivity",
                side_conditions=["0 < x", "0 < y"],
            ),
        ),
    ),
    CalculationExample(
        slug="monotonicity_step",
        title="Monotonicity Step",
        label="calc:monotonicity_step",
        statement="If a≤b, then a+c≤b+c.",
        calculation_kind="monotonicity_step",
        proof_text="Apply monotonicity of adding c.",
        steps=(
            CalcStep(lhs="a + c", relation=CalcRelation.le, rhs="b + c", justification="add_le_add_right hab c"),
        ),
    ),
    CalculationExample(
        slug="triangle_inequality_estimate",
        title="Triangle Inequality Estimate",
        label="calc:triangle_inequality_estimate",
        statement="|x+z|≤|x|+|z|.",
        calculation_kind="triangle_inequality_estimate",
        proof_text="Apply the triangle inequality.",
        steps=(
            CalcStep(lhs="|x+z|", relation=CalcRelation.le, rhs="|x| + |z|", justification="abs_add"),
        ),
    ),
    CalculationExample(
        slug="add_subtract_intermediate",
        title="Add-Subtract Intermediate",
        label="calc:add_subtract_intermediate",
        statement="f x - f y can be split through an intermediate z.",
        calculation_kind="add_subtract_intermediate",
        proof_text="Insert and subtract f z.",
        steps=(
            CalcStep(lhs="f x - f y", relation=CalcRelation.eq, rhs="(f x - f z) + (f z - f y)", justification="ring"),
        ),
    ),
    CalculationExample(
        slug="casewise_calculation",
        title="Casewise Calculation",
        label="calc:casewise_calculation",
        statement="|x| equals x when x is nonnegative and -x otherwise.",
        calculation_kind="casewise_calculation",
        proof_text="Split on whether x is nonnegative and simplify in each case.",
        steps=(
            CalcStep(lhs="|x|", relation=CalcRelation.eq, rhs="if 0 ≤ x then x else -x", justification="by_cases hx : 0 ≤ x"),
        ),
    ),
    CalculationExample(
        slug="inductive_step_calculation",
        title="Inductive Step Calculation",
        label="calc:inductive_step_calculation",
        statement="The successor step for the sum of the first n natural numbers follows by arithmetic.",
        calculation_kind="inductive_step_calculation",
        proof_text="Use the induction hypothesis and normalize the successor expression.",
        steps=(
            CalcStep(lhs="sum (n+1)", relation=CalcRelation.eq, rhs="sum n + (n+1)", justification="definition of sum"),
            CalcStep(lhs="sum n + (n+1)", relation=CalcRelation.eq, rhs="n*(n+1)/2 + (n+1)", justification="induction hypothesis"),
        ),
    ),
    CalculationExample(
        slug="extensionality_then_pointwise_calculation",
        title="Extensionality Then Pointwise Calculation",
        label="calc:extensionality_then_pointwise_calculation",
        statement="Two functions are equal when their values agree pointwise.",
        calculation_kind="extensionality_then_pointwise_calculation",
        proof_text="Apply function extensionality and calculate at an arbitrary point.",
        steps=(
            CalcStep(lhs="f x", relation=CalcRelation.eq, rhs="g x", justification="pointwise calculation after funext x"),
        ),
    ),
    CalculationExample(
        slug="calculation_to_contradiction",
        title="Calculation to Contradiction",
        label="calc:calculation_to_contradiction",
        statement="The assumptions a<b and b<a lead to a contradiction.",
        calculation_kind="calculation_to_contradiction",
        proof_text="Chain the strict inequalities to obtain a<a.",
        steps=(
            CalcStep(lhs="a", relation=CalcRelation.lt, rhs="b", justification="hypothesis hab"),
            CalcStep(lhs="b", relation=CalcRelation.lt, rhs="a", justification="hypothesis hba"),
        ),
    ),
)


async def build_example_json(example: CalculationExample) -> str:
    proof_root = ProofBuilder.calculation(
        id=f"{example.slug}.root.calculation",
        text=example.proof_text,
        goal=example.statement,
        calculation_kind=example.calculation_kind,
        steps=list(example.steps),
    )
    theorem = DocumentNode(
        id=f"{example.slug}.root.theorem",
        kind=DocumentKind.theorem,
        status=NodeStatus.resolved,
        label=example.label,
        text=example.source_text,
        data=StatementData(statement=example.statement).model_dump(),
        proof=ProofTree(
            id=f"{example.slug}.root.theorem.proof",
            theorem_statement=example.statement,
            root=proof_root,
        ),
    )
    document = MathDocument(
        id=example.slug,
        title=example.title,
        root=DocumentNode(
            id=f"{example.slug}.root",
            kind=DocumentKind.document,
            status=NodeStatus.resolved,
            children=[theorem],
        ),
    )
    return to_json(document, indent=2)


async def write_all_examples(output_dir: Path | None = None) -> list[Path]:
    target_dir = output_dir or Path(__file__).with_name("calculation_type_examples")
    target_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for example in EXAMPLES:
        source_path = target_dir / f"{example.slug}.md"
        json_path = target_dir / f"{example.slug}.json"
        source_path.write_text(example.source_text + "\n", encoding="utf-8")
        json_path.write_text(await build_example_json(example), encoding="utf-8")
        written.extend([source_path, json_path])
    return written


def main() -> None:
    for path in asyncio.run(write_all_examples()):
        print(path)


if __name__ == "__main__":
    main()

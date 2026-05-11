from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from mathdoc_agent.examples.proof_type_examples import EXAMPLES, write_all_examples
from mathdoc_agent.models.base import ProofKind


EXPECTED_PROOF_TYPES = {
    ProofKind.contradiction: "contradiction_statement",
    ProofKind.contrapositive: "Proof",
    ProofKind.existence: "Proof",
    ProofKind.uniqueness: "Proof",
    ProofKind.equivalence: "bi-implication_cases_proof",
    ProofKind.generic_element: "Proof",
    ProofKind.epsilon_delta: "Proof",
    ProofKind.invariant: "Proof",
    ProofKind.reduction: "Proof",
}


def contains_key(value, key: str) -> bool:
    if isinstance(value, dict):
        return key in value or any(contains_key(item, key) for item in value.values())
    if isinstance(value, list):
        return any(contains_key(item, key) for item in value)
    return False


class ProofTypeExampleTests(unittest.IsolatedAsyncioTestCase):
    async def test_examples_generate_paper_structure_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp)
            written = await write_all_examples(output_dir)
            self.assertEqual(len(written), 2 * len(EXAMPLES))

            for example in EXAMPLES:
                source_path = output_dir / f"{example.slug}.md"
                json_path = output_dir / f"{example.slug}.json"
                self.assertTrue(source_path.exists())
                self.assertTrue(json_path.exists())

                data = json.loads(json_path.read_text(encoding="utf-8"))
                self.assertFalse(contains_key(data, "kind"))
                self.assertEqual(data["type"], "document")
                theorem = data["document"]["body"][0]
                self.assertEqual(theorem["type"], "Theorem")
                proof_root = theorem["proof"]["root"]
                self.assertEqual(proof_root["type"], EXPECTED_PROOF_TYPES[example.proof_kind])
                self.assertEqual(proof_root["status"], "resolved")
                self.assertTrue(proof_root["data"]["strategy"])

    def test_saved_example_outputs_exist(self) -> None:
        output_dir = Path("mathdoc_agent/examples/proof_type_examples")
        for example in EXAMPLES:
            self.assertTrue((output_dir / f"{example.slug}.md").exists())
            self.assertTrue((output_dir / f"{example.slug}.json").exists())


if __name__ == "__main__":
    unittest.main()

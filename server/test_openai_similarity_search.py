from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from server.openai_similarity_search import run_similarity_search_payload


def write_jsonl(path: Path, records: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as output:
        for record in records:
            output.write(json.dumps(record, ensure_ascii=False) + "\n")


class OpenAISimilaritySearchTests(unittest.TestCase):
    def test_docstring_search_uses_doc_field_and_removes_embedding(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rawdata = Path(tmp)
            write_jsonl(
                rawdata / "mathlib4-prompts-embeddings-small.jsonl",
                [
                    {"name": "near", "doc": "near doc", "embedding": [1.0, 0.0]},
                    {"name": "far", "doc": "far doc", "embedding": [0.0, 1.0]},
                ],
            )

            result = run_similarity_search_payload(
                {"num": 1, "query": "q", "descField": "docString"},
                query_embedder=lambda _: [0.9, 0.1],
                rawdata_dir=rawdata,
            )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "near")
        self.assertEqual(result[0]["docString"], "near doc")
        self.assertNotIn("doc", result[0])
        self.assertNotIn("embedding", result[0])
        self.assertIn("distance", result[0])

    def test_description_search_removes_both_description_embeddings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rawdata = Path(tmp)
            write_jsonl(
                rawdata / "mathlib4-descs-embeddings-small.jsonl",
                [
                    {
                        "name": "desc",
                        "docString": "original docstring",
                        "description": "long description",
                        "concise-description": "short description",
                        "description-embedding": [1.0, 0.0],
                        "concise-description-embedding": [0.0, 1.0],
                    }
                ],
            )

            result = run_similarity_search_payload(
                {"num": 1, "query": "q", "descField": "description"},
                query_embedder=lambda _: [1.0, 0.0],
                rawdata_dir=rawdata,
            )

        self.assertEqual(result[0]["docString"], "long description")
        self.assertEqual(result[0]["concise-description"], "short description")
        self.assertNotIn("description", result[0])
        self.assertNotIn("description-embedding", result[0])
        self.assertNotIn("concise-description-embedding", result[0])


if __name__ == "__main__":
    unittest.main()

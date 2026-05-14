from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from server.openai_similarity_search import (
    _CACHE,
    embedding_file,
    pickle_file,
    run_similarity_search_payload,
)


def write_jsonl(path: Path, records: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as output:
        for record in records:
            output.write(json.dumps(record, ensure_ascii=False) + "\n")


class OpenAISimilaritySearchTests(unittest.TestCase):
    def setUp(self) -> None:
        _CACHE.clear()

    def test_docstring_search_uses_doc_field_and_removes_embedding(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rawdata = Path(tmp)
            embeddings_path = rawdata / "mathlib4-prompts-embeddings-small.jsonl"
            write_jsonl(
                embeddings_path,
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
            self.assertTrue(pickle_file(embeddings_path, "docString").exists())

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

    def test_numpy_search_returns_ranked_results(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rawdata = Path(tmp)
            write_jsonl(
                rawdata / "mathlib4-prompts-embeddings-small.jsonl",
                [
                    {"name": "first", "doc": "first doc", "embedding": [0.8, 0.2]},
                    {"name": "second", "doc": "second doc", "embedding": [1.0, 0.0]},
                    {"name": "third", "doc": "third doc", "embedding": [0.0, 1.0]},
                ],
            )

            result = run_similarity_search_payload(
                {"num": 2, "query": "q", "descField": "docString"},
                query_embedder=lambda _: [1.0, 0.0],
                rawdata_dir=rawdata,
            )

        self.assertEqual([record["name"] for record in result], ["second", "first"])

    def test_missing_embedding_file_runs_fetch_script(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rawdata = Path(tmp) / "rawdata"
            rawdata.mkdir()
            expected = rawdata / "mathlib4-prompts-embeddings-small.jsonl"
            calls = []

            from server import openai_similarity_search

            original = openai_similarity_search.run_fetch_script
            try:
                def fake_fetch() -> None:
                    calls.append("fetch")
                    write_jsonl(expected, [{"name": "created", "doc": "doc", "embedding": [1.0]}])

                openai_similarity_search.run_fetch_script = fake_fetch
                found = embedding_file("docString", rawdata)
            finally:
                openai_similarity_search.run_fetch_script = original

        self.assertEqual(found, expected)
        self.assertEqual(calls, ["fetch"])


if __name__ == "__main__":
    unittest.main()

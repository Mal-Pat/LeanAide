"""Similarity search over precomputed OpenAI embedding JSONL files.

The command-line interface accepts the same JSON payload sent by
`LeanAideCore/LeanAideCore/SimilaritySearch.lean`:

    {"num": 10, "query": "...", "descField": "docString"}

It embeds the query with OpenAI, streams the matching rawdata embedding file,
returns the nearest records, and removes stored embedding vectors from the
response records.
"""

from __future__ import annotations

import argparse
import heapq
import json
import math
import os
import sys
from pathlib import Path
from typing import Any, Callable, Iterable

from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]
RAWDATA_DIR = ROOT / "rawdata"
EMBEDDING_MODEL = os.environ.get("LEANAIDE_OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

FIELD_NAME = {
    "docString": "doc",
    "concise-description": "concise-description",
    "description": "description",
}

EMBEDDING_FIELD = {
    "docString": "embedding",
    "concise-description": "concise-description-embedding",
    "description": "description-embedding",
}


def openai_client() -> OpenAI:
    """Return an OpenAI client using the process environment."""
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def embed_query(query: str, client: OpenAI | None = None) -> list[float]:
    """Embed a query with the same OpenAI model used for the saved files."""
    client = client or openai_client()
    response = client.embeddings.create(input=query, model=EMBEDDING_MODEL)
    return response.data[0].embedding


def embedding_file(desc_field: str, rawdata_dir: Path = RAWDATA_DIR) -> Path:
    """Return the rawdata embedding file for a Lean similarity-search field."""
    if desc_field == "docString":
        candidates = [rawdata_dir / "mathlib4-prompts-embeddings-small.jsonl"]
    elif desc_field in {"description", "concise-description"}:
        candidates = [rawdata_dir / "mathlib4-descs-embeddings-small.jsonl"]
    else:
        raise ValueError(f"Incorrect descField: {desc_field}")

    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        "No OpenAI embedding file found for "
        f"{desc_field}; checked {', '.join(str(path) for path in candidates)}"
    )


def iter_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    """Yield nonempty JSON objects from a JSONL file."""
    with path.open("r", encoding="utf-8") as input_file:
        for line_no, line in enumerate(input_file, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_no} of {path}") from exc


def cosine_similarity(left: list[float], right: list[float]) -> float:
    """Return cosine similarity for two embedding vectors."""
    if len(left) != len(right):
        raise ValueError(f"Embedding dimensions differ: {len(left)} != {len(right)}")
    dot = sum(x * y for x, y in zip(left, right))
    left_norm = math.sqrt(sum(x * x for x in left))
    right_norm = math.sqrt(sum(y * y for y in right))
    if left_norm == 0 or right_norm == 0:
        return float("-inf")
    return dot / (left_norm * right_norm)


def record_text(record: dict[str, Any], desc_field: str) -> str | None:
    """Return the source text corresponding to a Lean descField."""
    field = FIELD_NAME[desc_field]
    if field in record:
        return record[field]
    if desc_field == "docString":
        return record.get("docString")
    return None


def sanitize_record(record: dict[str, Any], desc_field: str, distance: float) -> dict[str, Any]:
    """Remove embedding vectors and normalize the matched text to `docString`."""
    text = record_text(record, desc_field)
    cleaned = {
        key: value
        for key, value in record.items()
        if key != "embedding" and not key.endswith("-embedding")
    }
    if "docString" in cleaned:
        del cleaned["docString"]
    selected_field = FIELD_NAME[desc_field]
    if selected_field in cleaned:
        del cleaned[selected_field]
    cleaned["docString"] = text
    cleaned["distance"] = float(distance)
    return cleaned


def nearest_records(
    query_embedding: list[float],
    desc_field: str,
    num: int,
    *,
    rawdata_dir: Path = RAWDATA_DIR,
) -> list[dict[str, Any]]:
    """Stream the relevant rawdata file and return the nearest sanitized records."""
    if num < 1:
        return []

    path = embedding_file(desc_field, rawdata_dir)
    embedding_field = EMBEDDING_FIELD[desc_field]
    heap: list[tuple[float, int, dict[str, Any]]] = []

    for line_no, record in enumerate(iter_jsonl(path), start=1):
        embedding = record.get(embedding_field)
        if not isinstance(embedding, list):
            continue
        similarity = cosine_similarity(query_embedding, embedding)
        distance = 1.0 - similarity
        result = sanitize_record(record, desc_field, distance)
        item = (similarity, line_no, result)
        if len(heap) < num:
            heapq.heappush(heap, item)
        elif similarity > heap[0][0]:
            heapq.heapreplace(heap, item)

    return [record for _, _, record in sorted(heap, key=lambda item: item[0], reverse=True)]


def run_similarity_search(
    num: int,
    query: str,
    desc_field: str = "docString",
    *,
    query_embedder: Callable[[str], list[float]] = embed_query,
    rawdata_dir: Path = RAWDATA_DIR,
) -> list[dict[str, Any]]:
    """Embed the query and return nearest OpenAI-embedding rawdata records."""
    if desc_field not in FIELD_NAME:
        desc_field = "docString"
    query_embedding = query_embedder(query)
    return nearest_records(query_embedding, desc_field, int(num), rawdata_dir=rawdata_dir)


def run_similarity_search_payload(
    payload: dict[str, Any],
    *,
    query_embedder: Callable[[str], list[float]] = embed_query,
    rawdata_dir: Path = RAWDATA_DIR,
) -> list[dict[str, Any]]:
    """Run similarity search from the exact JSON object sent by Lean."""
    return run_similarity_search(
        int(payload.get("num", 10)),
        payload.get("query", "mathematics"),
        payload.get("descField", "docString"),
        query_embedder=query_embedder,
        rawdata_dir=rawdata_dir,
    )


def main() -> None:
    """Read a Lean-style JSON payload from argv or stdin and print JSON results."""
    parser = argparse.ArgumentParser(description="Run OpenAI-embedding similarity search.")
    parser.add_argument("payload", nargs="?", help="JSON payload; if omitted, read stdin.")
    args = parser.parse_args()

    payload_text = args.payload if args.payload is not None else sys.stdin.read()
    payload = json.loads(payload_text)
    result = run_similarity_search_payload(payload)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()

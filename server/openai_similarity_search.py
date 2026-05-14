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
import json
import os
import pickle
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any, Callable, Iterable

import numpy as np
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

_CACHE_LOCK = threading.Lock()
_CACHE: dict[tuple[str, str], tuple[np.ndarray, list[dict[str, Any]]]] = {}
_FETCH_LOCK = threading.Lock()


def openai_client() -> OpenAI:
    """Return an OpenAI client using the process environment."""
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def embed_query(query: str, client: OpenAI | None = None) -> list[float]:
    """Embed a query with the same OpenAI model used for the saved files."""
    client = client or openai_client()
    response = client.embeddings.create(input=query, model=EMBEDDING_MODEL)
    return response.data[0].embedding


def run_fetch_script() -> None:
    """Fetch raw embedding files by running the project-level fetch script."""
    fetch_script = ROOT / "fetch.sh"
    if not fetch_script.exists():
        raise FileNotFoundError(f"Fetch script not found: {fetch_script}")
    subprocess.run(["bash", str(fetch_script)], cwd=ROOT, check=True)


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
    with _FETCH_LOCK:
        if not any(candidate.exists() for candidate in candidates):
            run_fetch_script()
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


def record_text(record: dict[str, Any], desc_field: str) -> str | None:
    """Return the source text corresponding to a Lean descField."""
    field = FIELD_NAME[desc_field]
    if field in record:
        return record[field]
    if desc_field == "docString":
        return record.get("docString")
    return None


def sanitize_record(record: dict[str, Any], desc_field: str) -> dict[str, Any]:
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
    return cleaned


def pickle_file(path: Path, desc_field: str) -> Path:
    """Return the pickle cache path for a rawdata embedding file and field."""
    return path.with_name(f"{path.name}.{desc_field}.pickle")


def normalize_matrix(matrix: np.ndarray) -> np.ndarray:
    """Return row-normalized float32 embeddings for fast cosine search."""
    matrix = np.asarray(matrix, dtype=np.float32)
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return matrix / norms


def load_pickle_cache(path: Path, desc_field: str) -> tuple[np.ndarray, list[dict[str, Any]]] | None:
    """Load a valid pickle cache if it matches the source JSONL metadata."""
    cache_path = pickle_file(path, desc_field)
    if not cache_path.exists():
        return None
    with cache_path.open("rb") as cache_file:
        cache = pickle.load(cache_file)
    stat = path.stat()
    if (
        cache.get("source_path") != str(path)
        or cache.get("source_mtime_ns") != stat.st_mtime_ns
        or cache.get("source_size") != stat.st_size
        or cache.get("desc_field") != desc_field
    ):
        return None
    return cache["embeddings"], cache["records"]


def write_pickle_cache(path: Path, desc_field: str, embeddings: np.ndarray, records: list[dict[str, Any]]) -> None:
    """Persist parsed embeddings and metadata to avoid reloading JSONL next time."""
    cache_path = pickle_file(path, desc_field)
    stat = path.stat()
    payload = {
        "source_path": str(path),
        "source_mtime_ns": stat.st_mtime_ns,
        "source_size": stat.st_size,
        "desc_field": desc_field,
        "embeddings": embeddings,
        "records": records,
    }
    tmp_path = cache_path.with_suffix(cache_path.suffix + ".tmp")
    with tmp_path.open("wb") as cache_file:
        pickle.dump(payload, cache_file, protocol=pickle.HIGHEST_PROTOCOL)
    tmp_path.replace(cache_path)


def build_embedding_cache(path: Path, desc_field: str) -> tuple[np.ndarray, list[dict[str, Any]]]:
    """Parse JSONL embeddings into a normalized NumPy matrix and metadata list."""
    embedding_field = EMBEDDING_FIELD[desc_field]
    vectors: list[list[float]] = []
    records: list[dict[str, Any]] = []

    for record in iter_jsonl(path):
        embedding = record.get(embedding_field)
        if not isinstance(embedding, list):
            continue
        vectors.append(embedding)
        records.append(sanitize_record(record, desc_field))

    if not vectors:
        raise ValueError(f"No embeddings found in {path} for field {embedding_field}")
    embeddings = normalize_matrix(np.asarray(vectors, dtype=np.float32))
    write_pickle_cache(path, desc_field, embeddings, records)
    return embeddings, records


def load_embeddings(desc_field: str, rawdata_dir: Path = RAWDATA_DIR) -> tuple[np.ndarray, list[dict[str, Any]]]:
    """Load normalized embeddings from memory, pickle, or source JSONL."""
    path = embedding_file(desc_field, rawdata_dir)
    stat = path.stat()
    cache_key = (desc_field, f"{path}:{stat.st_mtime_ns}:{stat.st_size}")

    with _CACHE_LOCK:
        cached = _CACHE.get(cache_key)
        if cached is not None:
            return cached

        loaded = load_pickle_cache(path, desc_field)
        if loaded is None:
            loaded = build_embedding_cache(path, desc_field)
        _CACHE.clear()
        _CACHE[cache_key] = loaded
        return loaded


def nearest_records(
    query_embedding: list[float],
    desc_field: str,
    num: int,
    *,
    rawdata_dir: Path = RAWDATA_DIR,
) -> list[dict[str, Any]]:
    """Return nearest sanitized records using NumPy cosine search."""
    if num < 1:
        return []

    embeddings, records = load_embeddings(desc_field, rawdata_dir)
    query = normalize_matrix(np.asarray([query_embedding], dtype=np.float32))[0]
    similarities = embeddings @ query
    count = min(num, similarities.shape[0])
    if count == 0:
        return []
    candidate_indices = np.argpartition(similarities, -count)[-count:]
    ranked_indices = candidate_indices[np.argsort(similarities[candidate_indices])[::-1]]

    output = []
    for idx in ranked_indices:
        record = dict(records[int(idx)])
        record["distance"] = float(1.0 - similarities[int(idx)])
        output.append(record)
    return output


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

# mathdoc_agent

`mathdoc_agent` decomposes mathematical documents into structured JSON using
Python-owned orchestration. The tree state, node IDs, statuses, validation, and
replacement logic live in Python; agents only perform bounded local refinement
tasks.

The package is separate from `json_agent`.

## Output Shape

The public JSON export is intended to be close to `resources/PaperStructure.json`.
It uses `type` discriminators such as:

- `document`
- `Theorem`
- `ProofDetails`
- `induction_proof`
- `multi-condition_cases_proof`
- `assert_statement`

Internal Python models still use `kind` for handler dispatch, but
`mathdoc_agent.export.json.to_json` removes internal `kind` fields from exported
JSON.

## Command Line: Fake-Agent Examples

Run commands from the repository root.

For the induction plus cases example:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/leanaide_pycache \
./venv/bin/python -m mathdoc_agent.examples.even_induction_cases
```

This writes:

```text
mathdoc_agent/examples/even_induction_cases.json
```

For a small corpus covering several proof types:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/leanaide_pycache \
./venv/bin/python -m mathdoc_agent.examples.proof_type_examples
```

This writes `.md` and `.json` files to:

```text
mathdoc_agent/examples/proof_type_examples/
```

These examples use fake agents, so they do not require network access or API
keys.

## Python: Fake Agents

Use fake agents when you want deterministic tests or fixtures.

```python
import asyncio

from mathdoc_agent.examples.even_induction_cases import (
    SOURCE_TEXT,
    build_registries,
)
from mathdoc_agent.export.json import to_json
from mathdoc_agent.orchestration.document_orchestrator import (
    document_from_text,
    refine_math_document,
)


async def main():
    document_registry, proof_registry = build_registries()
    document = document_from_text(
        SOURCE_TEXT,
        id="example",
        title="Example",
    )
    refined = await refine_math_document(
        document,
        document_registry,
        proof_registry,
    )
    print(to_json(refined))


asyncio.run(main())
```

## Python: Live API-Backed Agents

The default registries use the agents defined in `mathdoc_agent.mathagents.definitions`.
Those definitions use the OpenAI Agents SDK if it is installed. Set the model with
`MATHDOC_AGENT_MODEL`; otherwise the package default is used.

```bash
export OPENAI_API_KEY="..."
export MATHDOC_AGENT_MODEL="gpt-5.4"
```

Then:

```python
import asyncio

from mathdoc_agent.pipeline import generate_math_document_json


source_text = """
Theorem. For every natural number n, either n is even or n+1 is even.

Proof. We prove this by induction on n. For n=0, n is even. For the induction
step, assume either n is even or n+1 is even. Split into cases. If n is even,
then n+2 is even. If n+1 is even, the desired disjunction is immediate.
"""


async def main():
    json_text = await generate_math_document_json(
        source_text,
        id="live_example",
        title="Live Example",
    )
    print(json_text)


asyncio.run(main())
```

For synchronous scripts:

```python
from mathdoc_agent.pipeline import generate_math_document_json_sync

json_text = generate_math_document_json_sync(
    "Theorem. ...\n\nProof. ...",
    id="live_example",
    title="Live Example",
)
print(json_text)
```

## Command Line: Live API Calls

There is no dedicated CLI wrapper yet. Use a short Python command:

```bash
export OPENAI_API_KEY="..."
export MATHDOC_AGENT_MODEL="gpt-5.4"

PYTHONPYCACHEPREFIX=/private/tmp/leanaide_pycache \
./venv/bin/python - <<'PY'
from mathdoc_agent.pipeline import generate_math_document_json_sync

source = """Theorem. For every natural number n, either n is even or n+1 is even.

Proof. We prove this by induction on n. The base case n=0 is immediate. For the
step, use the induction hypothesis and split into the two cases."""

print(generate_math_document_json_sync(source, id="cli_live_example", title="CLI Live Example"))
PY
```

## Tests

Run:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/leanaide_pycache \
./venv/bin/python -m unittest discover mathdoc_agent/tests
```

Compile check:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/leanaide_pycache \
./venv/bin/python -m compileall mathdoc_agent
```

`PYTHONPYCACHEPREFIX` keeps Python bytecode caches inside a writable location on
this macOS sandbox.

## Main Modules

- `mathdoc_agent.pipeline`: public programmatic entry points.
- `mathdoc_agent.models`: Pydantic models for document/proof trees.
- `mathdoc_agent.handlers`: refinement handlers.
- `mathdoc_agent.plugins`: default registry factories.
- `mathdoc_agent.orchestration`: worklist and refinement loops.
- `mathdoc_agent.export.json`: PaperStructure-style JSON export.
- `mathdoc_agent.examples`: deterministic example generators.

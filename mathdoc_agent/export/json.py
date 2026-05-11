from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel


def paper_structure_data(value: Any) -> Any:
    """Return JSON-ready data with public `type` discriminators, not internal `kind`.

    The orchestration layer keeps `kind` as an internal dispatch key. Exported JSON is
    intended for downstream Lean processing and should look closer to
    `resources/PaperStructure.json`, where `type` is the discriminator.
    """
    if isinstance(value, BaseModel):
        value = value.model_dump(mode="json")
    if isinstance(value, list):
        return [paper_structure_data(item) for item in value]
    if not isinstance(value, dict):
        return value

    cleaned_items = []
    for key, item in value.items():
        if key == "kind":
            continue
        cleaned_items.append((key, paper_structure_data(item)))

    if "type" not in value:
        return dict(cleaned_items)

    result: dict[str, Any] = {"type": value["type"]}
    for key, item in cleaned_items:
        if key != "type":
            result[key] = item
    return result


def to_json(model: BaseModel, *, indent: int = 2) -> str:
    return json.dumps(paper_structure_data(model), indent=indent, ensure_ascii=False)

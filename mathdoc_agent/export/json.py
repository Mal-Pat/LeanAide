from __future__ import annotations

from pydantic import BaseModel


def to_json(model: BaseModel, *, indent: int = 2) -> str:
    return model.model_dump_json(indent=indent)

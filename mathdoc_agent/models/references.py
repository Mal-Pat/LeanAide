from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class RefKind(str, Enum):
    document_node = "document_node"
    proof_node = "proof_node"
    named_result = "named_result"
    local_result = "local_result"
    external = "external"


class Reference(BaseModel):
    kind: RefKind
    target_id: Optional[str] = None
    label: Optional[str] = None
    text: Optional[str] = None

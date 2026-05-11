from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, Field


class AgentRunRecord(BaseModel):
    run_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    agent_name: str
    target_node_id: str
    target_node_kind: str

    input_summary: str
    output_summary: str

    validation_ok: bool
    issues: list[str] = Field(default_factory=list)

    old_status: str | None = None
    new_status: str | None = None

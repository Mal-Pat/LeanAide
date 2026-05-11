from __future__ import annotations

import inspect
from typing import Any, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


async def _maybe_await(value: Any) -> Any:
    if inspect.isawaitable(value):
        return await value
    return value


async def run_agent_typed(
    agent: Any,
    payload: BaseModel | dict[str, Any],
    output_type: type[T],
) -> T:
    """Run a bounded refinement agent and coerce its output to a Pydantic model.

    The wrapper accepts fake test agents, simple callables, objects exposing
    `.run(payload)`, and OpenAI Agents SDK Agent objects when the SDK is installed.
    """
    if isinstance(payload, BaseModel):
        input_payload: Any = payload.model_dump()
    else:
        input_payload = payload

    if callable(agent) and not hasattr(agent, "instructions"):
        output = await _maybe_await(agent(input_payload))
    elif hasattr(agent, "run"):
        output = await _maybe_await(agent.run(input_payload))
    else:
        try:
            from agents import Runner
        except ImportError as exc:
            raise RuntimeError(
                "No runnable fake agent was provided and the OpenAI Agents SDK is not installed."
            ) from exc
        result = await Runner.run(agent, input_payload)
        output = result.final_output

    if isinstance(output, output_type):
        return output
    if isinstance(output, BaseModel):
        return output_type.model_validate(output.model_dump())
    if isinstance(output, dict):
        return output_type.model_validate(output)
    if isinstance(output, str):
        return output_type.model_validate_json(output)
    if hasattr(output, "final_output"):
        return await run_agent_typed(lambda _: output.final_output, {}, output_type)
    return output_type.model_validate(output)

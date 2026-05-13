from __future__ import annotations

from mathdoc_agent.handlers.base import ProofRefinementHandler


class ProofHandlerRegistry:
    def __init__(self) -> None:
        self._handlers: dict[str, ProofRefinementHandler] = {}

    def register(self, kind: str, handler: ProofRefinementHandler) -> None:
        self._handlers[str(kind)] = handler

    def get(self, kind: str) -> ProofRefinementHandler:
        key = str(kind)
        if key in self._handlers:
            return self._handlers[key]
        if "unknown" not in self._handlers:
            raise KeyError("No proof handler registered for kind and no unknown fallback exists.")
        return self._handlers["unknown"]

    def kinds(self) -> list[str]:
        return sorted(self._handlers.keys())


proof_handler_registry = ProofHandlerRegistry()

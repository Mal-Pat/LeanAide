from __future__ import annotations

import sys

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
            print(
                f"[mathdoc_agent] unsupported proof handler kind={key!r}; no unknown fallback registered",
                file=sys.stderr,
                flush=True,
            )
            raise KeyError("No proof handler registered for kind and no unknown fallback exists.")
        print(
            f"[mathdoc_agent] unsupported proof handler kind={key!r}; using unknown fallback",
            file=sys.stderr,
            flush=True,
        )
        return self._handlers["unknown"]

    def kinds(self) -> list[str]:
        return sorted(self._handlers.keys())


proof_handler_registry = ProofHandlerRegistry()

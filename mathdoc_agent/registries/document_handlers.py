from __future__ import annotations

from mathdoc_agent.handlers.base import DocumentRefinementHandler


class DocumentHandlerRegistry:
    def __init__(self) -> None:
        self._handlers: dict[str, DocumentRefinementHandler] = {}

    def register(self, kind: str, handler: DocumentRefinementHandler) -> None:
        self._handlers[str(kind)] = handler

    def get(self, kind: str) -> DocumentRefinementHandler:
        key = str(kind)
        if key in self._handlers:
            return self._handlers[key]
        if "unknown" not in self._handlers:
            raise KeyError("No document handler registered for kind and no unknown fallback exists.")
        return self._handlers["unknown"]

    def kinds(self) -> list[str]:
        return sorted(self._handlers.keys())


document_handler_registry = DocumentHandlerRegistry()

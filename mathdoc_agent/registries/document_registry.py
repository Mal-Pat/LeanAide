from __future__ import annotations

from mathdoc_agent.models.base import DocumentKind
from mathdoc_agent.models.payloads import (
    DefinitionData,
    DocumentKindData,
    InductiveTypeDefinitionData,
    InstanceDefinitionData,
    StatementData,
    StructureDefinitionData,
)


def _kind_key(kind: str | DocumentKind) -> str:
    return kind.value if isinstance(kind, DocumentKind) else str(kind)


class DocumentPayloadRegistry:
    def __init__(self) -> None:
        self._models: dict[str, type[DocumentKindData]] = {}

    def register(self, kind: str | DocumentKind, model: type[DocumentKindData]) -> None:
        self._models[_kind_key(kind)] = model

    def get(self, kind: str | DocumentKind) -> type[DocumentKindData] | None:
        return self._models.get(_kind_key(kind))

    def validate_data(self, kind: str | DocumentKind, data: dict) -> DocumentKindData | None:
        model = self.get(kind)
        if model is None:
            return None
        return model.model_validate(data)


document_payload_registry = DocumentPayloadRegistry()
for theorem_kind in (
    DocumentKind.theorem,
    DocumentKind.lemma,
    DocumentKind.proposition,
    DocumentKind.corollary,
):
    document_payload_registry.register(theorem_kind, StatementData)
document_payload_registry.register(DocumentKind.definition, DefinitionData)
document_payload_registry.register(DocumentKind.structure_definition, StructureDefinitionData)
document_payload_registry.register(DocumentKind.instance_definition, InstanceDefinitionData)
document_payload_registry.register(DocumentKind.inductive_type_definition, InductiveTypeDefinitionData)

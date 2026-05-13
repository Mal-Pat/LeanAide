from typing import Optional

import model
import prompts
from openai import OpenAI
from pydantic import BaseModel, Field


_client_instance = None


def get_client() -> OpenAI:
    global _client_instance
    if _client_instance is None:
        _client_instance = OpenAI()
    return _client_instance


class ProofSourceExtractionResult(BaseModel):
    proof_source: Optional[str] = Field(
        None,
        description=(
            "The verbatim proof text if a proof is present in the block; otherwise null."
        ),
    )


class LogicalStepExtractionResult(BaseModel):
    steps: list[model.LogicalStep] = Field(
        ...,
        description='Ordered logical steps extracted from the source text.',
    )


class DocumentStructuringPipeline:
    """Document-level orchestration pipeline that returns the canonical DocumentContainer."""

    def __init__(self, model_name: str = "gpt-5.5") -> None:
        self.model_name = model_name

    def _parse_structured(self, system_prompt: str, user_prompt: str, response_format):
        completion = get_client().chat.completions.parse(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format=response_format,
        )
        return completion.choices[0].message.parsed
    
    def _orchestrate_document(self, source_text: str) -> model.DocumentOrchestrator:
        return self._parse_structured(
            system_prompt=prompts.DOCUMENT_ORCHESTRATOR_PROMPT,
            user_prompt=f"Please break down the following document:\n\n{source_text}",
            response_format=model.DocumentOrchestrator,
        )

    def _extract_proof_source(self, raw_source: str) -> Optional[str]:
        extraction = self._parse_structured(
            system_prompt=prompts.PROOF_SOURCE_EXTRACTION_PROMPT,
            user_prompt=f"Extract the proof from this block if present:\n\n{raw_source}",
            response_format=ProofSourceExtractionResult,
        )
        return extraction.proof_source

    def _extract_logical_steps(self, raw_source: str) -> model.LogicalStepSequence:
        extraction = self._parse_structured(
            system_prompt=prompts.LOGICAL_STEP_EXTRACTION_PROMPT,
            user_prompt=raw_source,
            response_format=LogicalStepExtractionResult,
        )
        return model.LogicalStepSequence(root=extraction.steps)


    def _extract_theorem(
        self,
        raw_source: str,
        header_hint: Optional[str] = None,
        label_hint: Optional[str] = None,
    ) -> model.Theorem:
        theorem = self._parse_structured(
            system_prompt=prompts.THEOREM_EXTRACTION_PROMPT,
            user_prompt=(
                f"[HEADER_HINT]\n{header_hint or 'None'}\n\n"
                f"[LABEL_HINT]\n{label_hint or 'None'}\n\n"
                f"[SOURCE_BLOCK]\n{raw_source}"
            ),
            response_format=model.Theorem,
        )

        proof_source = self._extract_proof_source(raw_source)
        if proof_source:
            proof_steps = self._extract_logical_steps(proof_source)
            theorem.proof = model.ProofDetails(root=proof_steps)

        return theorem

    def _extract_definition(
        self,
        raw_source: str,
        header_hint: Optional[str] = None,
        label_hint: Optional[str] = None,
    ) -> model.Definition:
        return self._parse_structured(
            system_prompt=prompts.DEFINITION_EXTRACTION_PROMPT,
            user_prompt=(
                f"[HEADER_HINT]\n{header_hint or 'None'}\n\n"
                f"[LABEL_HINT]\n{label_hint or 'None'}\n\n"
                f"[SOURCE_BLOCK]\n{raw_source}"
            ),
            response_format=model.Definition,
        )

    def _extract_figure(
        self, raw_source: str, label_hint: Optional[str] = None
    ) -> model.Figure:
        return self._parse_structured(
            system_prompt=prompts.FIGURE_EXTRACTION_PROMPT,
            user_prompt=(
                f"[LABEL_HINT]\n{label_hint or 'None'}\n\n"
                f"[SOURCE_BLOCK]\n{raw_source}"
            ),
            response_format=model.Figure,
        )

    def _extract_table(
        self, raw_source: str, label_hint: Optional[str] = None
    ) -> model.Table:
        return self._parse_structured(
            system_prompt=prompts.TABLE_EXTRACTION_PROMPT,
            user_prompt=(
                f"[LABEL_HINT]\n{label_hint or 'None'}\n\n"
                f"[SOURCE_BLOCK]\n{raw_source}"
            ),
            response_format=model.Table,
        )

    def _wrap_step(self, step) -> model.LogicalStep:
        return model.LogicalStep(root=step)

    def _build_section(self, element: model.OrchestratorElement) -> model.Section:
        content_steps = []
        if element.raw_source.strip():
            content_steps.append(
                self._wrap_step(model.Paragraph(text=element.raw_source.strip()))
            )
        return model.Section(
            label=element.label or "sec:unlabeled",
            header=element.header or "Untitled Section",
            content=model.LogicalStepSequence(root=content_steps),
        )

    def _build_paragraph(self, element: model.OrchestratorElement) -> model.Paragraph:
        text = element.raw_source.strip()
        if element.header and element.header not in text:
            text = f"{element.header}\n\n{text}"
        return model.Paragraph(text=text)

    def _build_math_paragraph_steps(
        self, element: model.OrchestratorElement
    ) -> list[model.LogicalStep]:
        source_text = element.raw_source.strip()
        if element.header and element.header not in source_text:
            source_text = f"{element.header}\n\n{source_text}"

        step_sequence = self._extract_logical_steps(source_text)
        return step_sequence.root

    def _convert_element_to_steps(
        self, element: model.OrchestratorElement
    ) -> list[model.LogicalStep]:
        if element.type == "theorem":
            return [
                self._wrap_step(
                    self._extract_theorem(
                        raw_source=element.raw_source,
                        header_hint=element.header,
                        label_hint=element.label,
                    )
                )
            ]
        if element.type == "definition":
            return [
                self._wrap_step(
                    self._extract_definition(
                        raw_source=element.raw_source,
                        header_hint=element.header,
                        label_hint=element.label,
                    )
                )
            ]
        if element.type == "section":
            return [self._wrap_step(self._build_section(element))]
        if element.type == "figure":
            return [
                self._wrap_step(
                    self._extract_figure(
                        raw_source=element.raw_source,
                        label_hint=element.label,
                    )
                )
            ]
        if element.type == "table":
            return [
                self._wrap_step(
                    self._extract_table(
                        raw_source=element.raw_source,
                        label_hint=element.label,
                    )
                )
            ]

        if element.content_kind == model.OrchestratorParagraphKind.mathematical_prose:
            return self._build_math_paragraph_steps(element)

        # `remark` does not have a dedicated canonical model in `model.py`,
        # so prose-like remarks are preserved as paragraph-like blocks.
        return [self._wrap_step(self._build_paragraph(element))]

    def run(self, source_text: str) -> model.DocumentContainer:
        orchestration = self._orchestrate_document(source_text)
        body_steps = []
        for element in orchestration.elements:
            body_steps.extend(self._convert_element_to_steps(element))
        document = model.Document(
            body=model.LogicalStepSequence(root=body_steps),
            title=orchestration.title,
            abstract=orchestration.abstract,
        )
        return model.DocumentContainer(document=document)

def document_container_agent(source_text: str) -> model.DocumentContainer:
    """Agentic entrypoint for converting a math document into DocumentContainer."""
    return DocumentStructuringPipeline().run(source_text)


# Backward-compatible alias for older imports.
DocumentContainerAgenticSystem = DocumentStructuringPipeline

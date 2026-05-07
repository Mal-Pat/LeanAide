# DocumentContainerAgenticSystem Agentic Loop

This diagram is based on the current implementation in [agents.py](/Users/ajaykumarnair/AgentAI/agents.py:35). It focuses on the orchestration loop in `DocumentContainerAgenticSystem.run(...)`, the per-element routing logic, and the nested proof/logical-step extraction path.

```mermaid
flowchart TD
    A["document_container_agent(source_text)"] --> B["DocumentContainerAgenticSystem.run(source_text)"]
    B --> C["_orchestrate_document(source_text)"]
    C --> D["DocumentOrchestrator"]
    D --> E["for each OrchestratorElement in orchestration.elements"]

    E --> F{"_convert_element_to_steps(element)"}

    F -->|type = theorem| G["_extract_theorem(raw_source, header_hint, label_hint)"]
    F -->|type = definition| H["_extract_definition(raw_source, header_hint, label_hint)"]
    F -->|type = section| I["_build_section(element)"]
    F -->|type = figure| J["_extract_figure(raw_source, label_hint)"]
    F -->|type = table| K["_extract_table(raw_source, label_hint)"]
    F -->|"paragraph or remark<br/>content_kind = mathematical_prose"| L["_build_math_paragraph_steps(element)"]
    F -->|"paragraph or remark<br/>content_kind = prose or unset"| M["_build_paragraph(element)"]

    G --> N{"proof present?"}
    N -->|yes| O["_extract_proof_source(raw_source)"]
    O --> P["_extract_logical_steps(proof_source)"]
    P --> Q["LogicalStepSequence"]
    Q --> R["attach theorem.proof = ProofDetails"]
    N -->|no| S["return theorem without proof"]
    R --> T["_wrap_step(theorem)"]
    S --> T

    H --> U["_wrap_step(definition)"]
    I --> V["_wrap_step(section)"]
    J --> W["_wrap_step(figure)"]
    K --> X["_wrap_step(table)"]
    L --> Y["LogicalStepSequence.root<br/>list of LogicalStep"]
    M --> Z["_wrap_step(paragraph)"]

    T --> AA["extend body_steps"]
    U --> AA
    V --> AA
    W --> AA
    X --> AA
    Y --> AA
    Z --> AA

    AA --> AB{"more elements?"}
    AB -->|yes| E
    AB -->|no| AC["document = model.Document(body = LogicalStepSequence(body_steps), title, abstract)"]
    AC --> AD["return model.DocumentContainer(document=document)"]

    classDef entry fill:#e8f1ff,stroke:#2f5ea8,stroke-width:1px;
    classDef loop fill:#eef8e8,stroke:#4d7c0f,stroke-width:1px;
    classDef llm fill:#fff3d6,stroke:#a16207,stroke-width:1px;
    classDef output fill:#f7e8ff,stroke:#7e22ce,stroke-width:1px;

    class A,B entry;
    class E,F,AA,AB loop;
    class C,G,H,J,K,L,O,P llm;
    class D,Q,AC,AD output;
```

## Reading Guide

- The outer agentic loop is `run(...)`:
  ingest document -> orchestrate into elements -> iterate over elements -> route each element -> append resulting steps -> build final `DocumentContainer`.
- The key routing decision happens in `_convert_element_to_steps(...)`:
  theorem/definition/figure/table go to specialized extractors, while paragraph-like elements branch on `content_kind`.
- `mathematical_prose` is special:
  instead of becoming a plain `Paragraph`, it is decomposed into a `LogicalStepSequence` and flattened into the main document body.
- The theorem branch has its own nested mini-loop:
  first extract the theorem statement, then optionally extract proof text, then parse that proof into logical steps, then attach it as `ProofDetails`.

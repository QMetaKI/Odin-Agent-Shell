# Odin Agent Shell — v7.1 Narrative Compiler Integration

This document is part of the v0.6.0 Narrative Aorta / Y* Compiler Lock. It preserves the Odin Agent Shell v7.1 functional canon and adds a typed, bounded, auditable meta-authoring and compile-prelude layer.

Hard boundary: Fairy prose never executes. Y* Native DSL validates and stages. Shadow Runtime remains code-near blueprint. Runtime packs load only after validation. Odin Host remains the stable local boundary.

## Purpose

The Fairy-to-Shadow IR compiler translates validated Y* units and mapped Fairy nodes into Shadow Runtime IR fragments.

It is deterministic and bounded. It does not invent runtime behavior. It lowers typed narrative structure into known Shadow Runtime contracts.

## Pipeline

```text
Fairy Story
→ Fairy Node Extraction
→ Y* Unit Validation
→ Fairy/Y* Mapping Validation
→ Y* Mediation Directive
→ Shadow IR Fragment
→ Shadow Runtime Compiler Input
```

## Compiler Inputs

- odin_fairy_story
- odin_ystar_native_unit
- odin_fairy_shadow_mapping
- odin_ystar_mediation_directive
- registries/fairy_dsl_registry.json
- registries/ystar_stage_registry.json
- registries/narrative_aorta_registry.json

## Compiler Outputs

- shadow_runtime_flow
- worklet_graph_template
- slot_contract_template
- policy_gate_template
- candidate_dna_template
- unresolved_holes_report
- confidence_report

## Lowering Rules

- Fairy role Gatekeeper lowers to binding/policy/claim gates.
- Fairy role Weaver lowers to context distillery / seed memory.
- Fairy role Messenger lowers to Candidate Artifact / Response Packet.
- Fairy role Lantern lowers to trace / receipt candidate.
- Fairy role Helper lowers to model worker route.

## Failure Rules

Fail closed if:

- any Fairy node is unmapped,
- Y* validation fails,
- target Shadow module is unknown,
- compile output would enable app mutation,
- compile output would enable external send,
- confidence is below policy threshold without explicit hole disclosure.

## Codex Rule

Codex must preserve the lowering table and add tests before adding new Fairy roles.

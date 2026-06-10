# Odin Agent Shell — v7.1 Narrative Compiler Integration

This document is part of the v0.6.0 Narrative Aorta / Y* Compiler Lock. It preserves the Odin Agent Shell v7.1 functional canon and adds a typed, bounded, auditable meta-authoring and compile-prelude layer.

Hard boundary: Fairy prose never executes. Y* Native DSL validates and stages. Shadow Runtime remains code-near blueprint. Runtime packs load only after validation. Odin Host remains the stable local boundary.

## Definition

The Narrative Aorta is the canonical story-spine that carries Odin's structural meaning across specs, shadow runtime, runtime packs, Codex tasks and human review.

It is not marketing copy. It is a semantic alignment surface and trace label system.

## Responsibilities

- preserve the center: app authority and candidate-only output,
- encode children/family-first as architecture boundaries,
- translate archetypic roles into module responsibilities,
- keep middle-out staging visible,
- give Codex a durable semantic map,
- support small-model compression by reducing repeated intent patterns.

## Aorta Node Contract

Each node has:

- node_id
- fairy_label
- ystar_node_ref
- runtime_contract_ref
- ring
- authority_posture
- forbidden_edges
- output_artifacts
- trace_label

## Example Node

```json
{
  "node_id": "aorta.weaver.red_threads",
  "fairy_label": "The weaver gathers the red threads",
  "ystar_node_ref": "context_distillery.build_context_capsule",
  "runtime_contract_ref": "odin_context_capsule",
  "ring": "R3",
  "authority_posture": "context_only",
  "forbidden_edges": ["app_apply", "external_send", "invent_facts"],
  "output_artifacts": ["context_capsule", "seed_profile"],
  "trace_label": "context.red_threads"
}
```

## Children / Family First as Semantics

In Odin this means:

- weak workers receive narrow work,
- no worker receives hidden authority,
- app/user decides what becomes real,
- every output is reviewable,
- every route has traceable lineage,
- no model is burdened with unbounded state.

## Red Lines

- no narrative node without machine mapping,
- no public persona simulation,
- no claim that story itself executes,
- no node that bypasses final gate,
- no unresolved holes hidden from Codex.

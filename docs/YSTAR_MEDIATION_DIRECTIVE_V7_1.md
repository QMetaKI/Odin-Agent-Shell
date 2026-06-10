# Odin Agent Shell — v7.1 Narrative Compiler Integration

This document is part of the v0.6.0 Narrative Aorta / Y* Compiler Lock. It preserves the Odin Agent Shell v7.1 functional canon and adds a typed, bounded, auditable meta-authoring and compile-prelude layer.

Hard boundary: Fairy prose never executes. Y* Native DSL validates and stages. Shadow Runtime remains code-near blueprint. Runtime packs load only after validation. Odin Host remains the stable local boundary.

## Purpose

Y* Mediation Directive is the staging contract between validated Y* Native DSL and Shadow Runtime IR.

Y* enriches and routes. It never owns final authority.

## Directive Fields

- directive_id
- ystar_unit_ref
- target_shadow_modules
- runtime_boundaries
- compile_hints
- holes
- risk
- confidence
- trace_labels

## Runtime Boundaries

Every directive must preserve:

- candidate_only
- no_app_mutation
- no_external_send
- final_gate_required
- local_first unless caller allows explicit remote
- smallest_sufficient_worker

## Example

```json
{
  "artifact_kind": "odin_ystar_mediation_directive",
  "protocol_version": "7.1",
  "directive_id": "YMD-001",
  "ystar_unit_ref": "YSTAR-001",
  "target_shadow_modules": [
    "universal_work_shadow",
    "semantic_bus_shadow",
    "slot_forge_shadow",
    "candidate_shadow"
  ],
  "runtime_boundaries": {
    "candidate_only": true,
    "no_app_mutation": true,
    "no_external_send": true,
    "final_gate_required": true
  },
  "compile_hints": {
    "resource_profile": "standard_local",
    "preferred_pack": "standard_local_runtime_pack",
    "model_strategy": "3b_7b_hybrid"
  },
  "holes": [],
  "risk": {
    "authority_drift": "low",
    "runtime_overclaim": "low"
  }
}
```

## Invalid Conditions

- target module unknown,
- boundary weaker than Y* unit,
- final gate absent,
- resource profile unknown,
- model strategy violates ladder,
- hidden unresolved hole,
- directive tries to become authority.

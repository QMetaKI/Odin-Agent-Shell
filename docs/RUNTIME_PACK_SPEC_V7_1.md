# Odin Agent Shell — v7.1 Narrative Compiler Integration

This document is part of the v0.6.0 Narrative Aorta / Y* Compiler Lock. It preserves the Odin Agent Shell v7.1 functional canon and adds a typed, bounded, auditable meta-authoring and compile-prelude layer.

Hard boundary: Fairy prose never executes. Y* Native DSL validates and stages. Shadow Runtime remains code-near blueprint. Runtime packs load only after validation. Odin Host remains the stable local boundary.

## Purpose

A Runtime Pack is a validated, frozen capability slice generated from Shadow Runtime IR.

## Pack Types

- low_memory_strict.pack
- standard_local.pack
- quality_local.pack
- heavy_local.pack
- developer_debug.pack
- app_capability_slice.pack

## Manifest Shape

```json
{
  "artifact_kind": "odin_runtime_pack",
  "pack_id": "standard_local_v7_1",
  "spec_version": "7.1",
  "source_shadow_hash": "sha256...",
  "source_ystar_hash": "sha256...",
  "resource_profile": "standard_local",
  "capabilities": ["universal_work", "semantic_bus", "context_distillery"],
  "forbidden_capabilities": ["direct_apply", "external_send", "unverified_runtime_claim"],
  "compiled_tables": {
    "verbs": "compiled/verbs.json",
    "routes": "compiled/routes.json",
    "policies": "compiled/policies.json",
    "schemas": "compiled/schemas.json"
  },
  "tests_required": ["candidate_only_gate", "claim_boundary_gate"],
  "load_policy": {"requires_validation": true, "rollback_on_failure": true}
}
```

## Required Gates

- schema validity,
- registry parity,
- source hash lineage,
- candidate-only boundary,
- no app mutation,
- no external send,
- rollback target exists,
- generated tests present.

## Load Rule

Odin Host may load only validated packs. Failed pack validation triggers rollback or safe minimal mode.

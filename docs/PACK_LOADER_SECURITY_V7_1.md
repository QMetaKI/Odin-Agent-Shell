# Odin Agent Shell — v7.1 Narrative Compiler Integration

This document is part of the v0.6.0 Narrative Aorta / Y* Compiler Lock. It preserves the Odin Agent Shell v7.1 functional canon and adds a typed, bounded, auditable meta-authoring and compile-prelude layer.

Hard boundary: Fairy prose never executes. Y* Native DSL validates and stages. Shadow Runtime remains code-near blueprint. Runtime packs load only after validation. Odin Host remains the stable local boundary.

## Purpose

Pack Loader Security defines how Odin Host loads compiled runtime packs without authority drift.

## Loader Requirements

- verify pack schema,
- verify source hash lineage,
- verify allowed capabilities,
- verify forbidden capabilities,
- verify required tests metadata,
- verify rollback target,
- reject pack with direct apply or external send,
- reject pack that weakens claim boundary.

## Rollback Flow

```text
load_candidate_pack
→ validate_manifest
→ validate_hash_lineage
→ validate_capabilities
→ run_static_pack_gates
→ activate_pack
→ on_failure rollback_previous_pack
```

## Red Lines

- no unsigned/unvalidated pack load,
- no model-generated executable code,
- no LLM in compiler default path,
- no pack may mutate app state,
- no pack may bypass schema validation.

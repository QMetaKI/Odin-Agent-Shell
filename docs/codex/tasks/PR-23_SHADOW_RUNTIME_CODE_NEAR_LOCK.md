# PR-23 — Shadow Runtime Code-Near Lock

## Objective

Create and preserve the Odin v7.1 Shadow Runtime as the code-near mechanical bridge between the full architecture/specs and future real implementation work.

This task does not implement the final Odin runtime. It locks the shape Codex must follow when implementing real modules.

## Primary Files

```text
docs/SHADOW_RUNTIME_LOCK_V7_1.md
docs/SHADOW_RUNTIME_CODE_NEAR_BOOK_V7_1.md
docs/SHADOW_RUNTIME_TO_REAL_BUILD_MAPPING_V7_1.md
docs/CONTRACT_TO_SHADOW_CODE_MAP_V7_1.md
docs/SHADOW_RUNTIME_STATE_MACHINES_V7_1.md
docs/SHADOW_RUNTIME_ACCEPTANCE_TESTS_V7_1.md
docs/YNODE_SHADOW_RUNTIME_PATTERN_ADAPTATION_V7_1.md
odin/shadow_runtime/
examples/shadow_runtime/
registries/shadow_runtime_contract_registry.json
tests/test_shadow_runtime_lock.py
```

## Required Behavior

- Shadow Runtime modules import without side effects.
- Valid Universal Work fixture produces a candidate-only ShadowRuntimeResult.
- Direct apply fixture is blocked.
- Standard route fixture selects `3b_7b_8b_hybrid`.
- Semantic bus batch includes local-only channel flow.
- Contract registry maps each shadow contract to future real target files.
- Shadow Runtime docs state the non-authority boundary.
- `validate-shadow-runtime` is part of `validate-all`.

## Forbidden Scope

- Do not call real models.
- Do not open sockets.
- Do not create public IRC.
- Do not add LAN mesh or federation.
- Do not mutate app state.
- Do not perform app apply.
- Do not add remote fallback.
- Do not claim runtime proof.

## Definition of Done

- `python -m odin.cli validate-shadow-runtime` passes.
- `python -m odin.cli validate-all` passes.
- `pytest` passes.
- PR-23 is listed in `codex_task_registry.json`.
- PR-23 is covered by REAL-PR-09.
- All shadow docs are referenced in SYSTEM_MAP.
- FILE_MANIFEST includes all new files.

## Codex PR Summary Template

```text
Implemented PR-23 Shadow Runtime Code-Near Lock.
Preserved candidate-only, app-owned apply, local-only semantic bus, no real model calls and no runtime-proof claims.
Added/updated docs, shadow_runtime package, fixtures, registry, validation and tests.
Validation:
- python -m odin.cli validate-all
- PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
```

## Implementation Notes

Codex should treat this PR as a bridge task. The purpose is not to add feature breadth, but to remove ambiguity from every later feature PR. Each future implementation should be able to point to a shadow type, a shadow function, a fixture, and a real target file. If no shadow contract exists, Codex must either add one in a follow-up task or explicitly justify why the new feature is outside the Shadow Runtime surface.

## Review Checklist

- Does the Shadow Runtime remain pure in-memory?
- Are all returned objects candidate-shaped?
- Is the final gate represented before any future real behavior?
- Are direct app actions blocked?
- Is the semantic bus explicitly local-only?
- Are model routes plans only, not live calls?
- Does every mapping have a fixture and test?
- Are docs, task registry and real bundle registry updated together?


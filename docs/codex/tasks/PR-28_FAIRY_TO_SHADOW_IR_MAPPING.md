# PR-28 — Fairy to Shadow IR Mapping

## Objective

Fairy to Shadow IR Mapping.

## Primary Files

- `odin/shadow_runtime/fairy_to_shadow_ir_shadow.py`
- `schemas/v7_1/odin_fairy_shadow_mapping.schema.json`

## Required Behavior

- mapping lowers to shadow fragment
- forbidden edges preserved

## Forbidden Scope

- ambiguous node compile
- hidden holes

## Definition of Done

- mapping fixture validates
- shadow contract registry updated

## Codex PR Summary Template

- Internal task: PR-28
- Scope completed:
- Files changed:
- Tests added:
- Gates run:
- Boundaries preserved:
- Remaining holes:

## Notes

This task is part of the v7.1 Narrative Aorta / Y* Compiler integration. It must preserve all v7.1 runtime invariants. It may add compiler-prelude and typed narrative artifacts but may not convert prose into executable behavior. Parser and validator work must precede emitter work. All outputs remain bounded, candidate-first and non-authoritative unless later real runtime code explicitly implements a validated pack loader.

## Traceability

- Architecture: `docs/MASTER_ARCHITECTURE_V7_1.md`
- Specs: `docs/MASTER_SPECS_V7_1.md`
- Narrative docs: `docs/FAIRY_DSL_V7_1.md`, `docs/YSTAR_NATIVE_DSL_V7_1.md`, `docs/NARRATIVE_AORTA_V7_1.md`
- Compiler docs: `docs/SHADOW_RUNTIME_COMPILER_V7_1.md`, `docs/RUNTIME_PACK_SPEC_V7_1.md`


## Detailed Build Constraints

This task is intentionally part of the v7.1 integrated narrative compiler layer, not a fork. The implementation must keep the existing Universal Work Kernel, Small Model Power Layer, Internal Semantic Bus, Candidate Artifact system and app-owned apply boundary intact. The new code or documentation may only add typed narrative compiler preparation, validation, mapping, or runtime-pack prelude behavior.

Codex must treat this task as a bounded mechanical transformation. It must update relevant schemas, registries, tests, fixtures, System Map and FILE_MANIFEST whenever files are added or moved. If a behavior is not represented in schema, fixture and test form, Codex must keep it as documented intent rather than runtime behavior.

The reviewer should reject any implementation that turns Fairy prose into executable authority, treats Y* as final decision maker, allows runtime pack loading without validation, adds app mutation capability to Odin, or bypasses candidate-only output posture. The correct result is a narrower, more traceable, more testable build surface.

## Validation Commands

- `python -m odin.cli validate-all`
- `python -m pytest -q -p no:cacheprovider`
- Review the changed task registry and real PR bundle registry.
- Verify that v7.1 invariants are unchanged.

## Handoff Notes

This task must remain understandable without the chat context. The document itself must state scope, boundaries, files, required behavior, forbidden scope and completion criteria. It is acceptable for the task to produce shadow or compile-prelude artifacts; it is not acceptable to claim finished runtime capability from those artifacts.

# PR-92 — Seed Pack Why Trace and Use Case Matrix

## Objective
Implement Seed Pack Why Trace and Use Case Matrix as part of v0.6.9 App Seed Pack Compiler Lock.

## Internal Tasks Covered
- PR-92

## Primary Files
- docs/SEED_PACK_WHY_TRACE_AND_EXPLAINABILITY_V7_1.md
- docs/SEED_PACK_USE_CASE_MATRIX_V7_1.md
- odin/shadow_runtime/seed_pack_why_trace_shadow.py

## Required Behavior
- Preserve candidate-only semantics.
- Seed packs are declarative and typed.
- Validate before compile.
- Compile before load.
- App seed packs may improve Odin precompute, QIRC hot windows, seed/archetype activation, slot forge, output composition and model-work avoidance.
- Update tests, schemas, registries, System Map and FILE_MANIFEST.

## Forbidden Scope
- No arbitrary seed-pack code execution.
- No app-state mutation.
- No external send.
- No remote permission grant.
- No bypass of Odin Final Gate.
- No license weakening.

## Definition of Done
- python -m odin.cli validate-all passes.
- pytest passes.
- Required schemas, registries, fixtures and shadow modules are present.
- Negative tests prove unsafe seed packs are blocked.
- PR remains bounded to the declared files and behavior.

## Codex PR Summary Template
```text
PR-92: Seed Pack Why Trace and Use Case Matrix
Summary:
Validation:
Risks:
Boundaries preserved:
```

## Detailed Implementation Notes
The implementation should be mechanical. Codex must first read MASTER_ARCHITECTURE_V7_1, MASTER_SPECS_V7_1, APP_SEED_PACK_COMPILER_V7_1, SEED_PACK_SECURITY_BOUNDARY_V7_1 and the relevant schema. Then it should implement the smallest real module that matches the shadow module. The seed pack compiler must prefer no-model and deterministic compilation before involving any model worker. App seed packs are not authorities; they are structured priors. If there is a conflict between seed pack instructions and Odin Core, Odin Core wins. If there is a conflict between app seed pack and app apply boundary, app apply boundary wins. If there is a conflict between seed pack and GPL-2.0-only policy, GPL policy wins.
## Detailed Implementation Notes
The implementation should be mechanical. Codex must first read MASTER_ARCHITECTURE_V7_1, MASTER_SPECS_V7_1, APP_SEED_PACK_COMPILER_V7_1, SEED_PACK_SECURITY_BOUNDARY_V7_1 and the relevant schema. Then it should implement the smallest real module that matches the shadow module. The seed pack compiler must prefer no-model and deterministic compilation before involving any model worker. App seed packs are not authorities; they are structured priors. If there is a conflict between seed pack instructions and Odin Core, Odin Core wins. If there is a conflict between app seed pack and app apply boundary, app apply boundary wins. If there is a conflict between seed pack and GPL-2.0-only policy, GPL policy wins.

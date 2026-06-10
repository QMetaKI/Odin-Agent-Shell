# REAL-PR-22 — App Seed Pack Compiler and Universal Seed Pack Runtime

## Objective
Implement the App Seed Pack Compiler and Universal Seed Pack Runtime as the next real Codex bundle after the universal LLM work construct. This bundle makes Odin able to consume app-provided seed packs of any kind as typed, declarative, validated, compiled priors that improve QIRC precompute, Seed/Archetype Economy, Fairy/Y*, Shadow Runtime, Runtime Packs, Model Work Avoidance and Output Intelligence Composition.

## Internal Tasks Covered
- PR-87
- PR-88
- PR-89
- PR-90
- PR-91
- PR-92

## Primary Files
- docs/APP_SEED_PACK_COMPILER_V7_1.md
- docs/UNIVERSAL_SEED_PACK_FORMAT_V7_1.md
- docs/OPERATIONAL_SEED_FUNCTIONS_V7_1.md
- docs/SEED_PACK_SECURITY_BOUNDARY_V7_1.md
- docs/SEED_PACK_TO_RUNTIME_PACK_COMPILER_V7_1.md
- docs/SEED_PACK_CAPABILITY_SLICES_V7_1.md
- schemas/v7_1/odin_app_seed_pack_manifest.schema.json
- registries/app_seed_pack_type_registry.json
- odin/shadow_runtime/app_seed_pack_compiler_shadow.py
- tests/test_app_seed_pack_compiler.py

## Required Behavior
- App seed packs must be represented by manifests.
- Operational seed functions must be declarative only.
- Seed packs must compile into Odin-owned profiles, not execute code.
- Seed pack compilation must update QIRC prewarm, seed/archetype activation, slot forge, model work avoidance and output composition only through valid contracts.
- Seed pack conflicts must resolve before model dispatch.
- Why Trace must disclose active seed packs and blocked seed packs.
- Runtime Pack capability slices must include only permitted seed channels and functions.

## Forbidden Scope
- No arbitrary seed-pack code execution.
- No plugin runtime.
- No app-state mutation.
- No external send.
- No remote permission grant.
- No bypass of Odin Final Gate.
- No hidden prompt injection from seed pack payloads.
- No weakening of GPL-2.0-only policy.

## Definition of Done
- python -m odin.cli validate-all passes.
- pytest passes.
- Valid and invalid seed pack fixtures exist.
- All seed-pack schemas are loadable JSON.
- Codex task registry includes PR-87 through PR-92.
- Real PR bundle registry covers PR-87 through PR-92 under REAL-PR-22.
- SYSTEM_MAP and FILE_MANIFEST are updated.
- Shadow runtime contract registry contains app seed pack compiler mappings.

## Codex PR Summary Template
```text
REAL-PR-22 — App Seed Pack Compiler and Universal Seed Pack Runtime
Summary:
Validation:
Changed files:
Boundaries preserved:
Known follow-ups:
```

## Senior Review Notes
This bundle is approved only as declarative seed-pack compilation. If Codex introduces executable seed pack logic, implicit remote access, app mutation, tool authorization, or unvalidated pack load, the PR must be rejected. The correct mental model is: app seed packs are domain-operational priors; Odin remains compiler, gate and runtime authority for LLM work.

The App Seed Pack Compiler must improve perceived intelligence by allowing apps to preload Odin with high-signal operational knowledge while keeping the final output candidate-only. The App Seed Pack Compiler must improve perceived intelligence by allowing apps to preload Odin with high-signal operational knowledge while keeping the final output candidate-only. The App Seed Pack Compiler must improve perceived intelligence by allowing apps to preload Odin with high-signal operational knowledge while keeping the final output candidate-only. The App Seed Pack Compiler must improve perceived intelligence by allowing apps to preload Odin with high-signal operational knowledge while keeping the final output candidate-only. The App Seed Pack Compiler must improve perceived intelligence by allowing apps to preload Odin with high-signal operational knowledge while keeping the final output candidate-only. The App Seed Pack Compiler must improve perceived intelligence by allowing apps to preload Odin with high-signal operational knowledge while keeping the final output candidate-only. The App Seed Pack Compiler must improve perceived intelligence by allowing apps to preload Odin with high-signal operational knowledge while keeping the final output candidate-only. The App Seed Pack Compiler must improve perceived intelligence by allowing apps to preload Odin with high-signal operational knowledge while keeping the final output candidate-only. The App Seed Pack Compiler must improve perceived intelligence by allowing apps to preload Odin with high-signal operational knowledge while keeping the final output candidate-only. The App Seed Pack Compiler must improve perceived intelligence by allowing apps to preload Odin with high-signal operational knowledge while keeping the final output candidate-only. The App Seed Pack Compiler must improve perceived intelligence by allowing apps to preload Odin with high-signal operational knowledge while keeping the final output candidate-only. The App Seed Pack Compiler must improve perceived intelligence by allowing apps to preload Odin with high-signal operational knowledge while keeping the final output candidate-only. The App Seed Pack Compiler must improve perceived intelligence by allowing apps to preload Odin with high-signal operational knowledge while keeping the final output candidate-only. The App Seed Pack Compiler must improve perceived intelligence by allowing apps to preload Odin with high-signal operational knowledge while keeping the final output candidate-only. The App Seed Pack Compiler must improve perceived intelligence by allowing apps to preload Odin with high-signal operational knowledge while keeping the final output candidate-only. The App Seed Pack Compiler must improve perceived intelligence by allowing apps to preload Odin with high-signal operational knowledge while keeping the final output candidate-only. The App Seed Pack Compiler must improve perceived intelligence by allowing apps to preload Odin with high-signal operational knowledge while keeping the final output candidate-only. The App Seed Pack Compiler must improve perceived intelligence by allowing apps to preload Odin with high-signal operational knowledge while keeping the final output candidate-only. The App Seed Pack Compiler must improve perceived intelligence by allowing apps to preload Odin with high-signal operational knowledge while keeping the final output candidate-only. The App Seed Pack Compiler must improve perceived intelligence by allowing apps to preload Odin with high-signal operational knowledge while keeping the final output candidate-only.

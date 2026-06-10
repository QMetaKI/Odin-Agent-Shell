# Codex Prompt Packs v0.4.0

Reusable prompts for each locked implementation task.

## Prompt Pack PR-00 — Canon Gates and Repo Hygiene

```text
You are implementing PR-00 — Canon Gates and Repo Hygiene for Odin Agent Shell v7.1.
Read:
- AGENTS.md
- CODEX_START_HERE.md
- docs/codex/CODEX_TASK_LOCK_V0_4_0.md
- docs/codex/tasks/PR-00_CANON_GATES_AND_REPO_HYGIENE.md
- all docs/schemas/registries referenced by the task file.

Goal:
Lock the repository as a deterministic build surface before feature work starts.

Hard boundaries:
- no LLM runtime in app templates
- candidate-only outputs
- app owns state/apply/external-send
- internal semantic bus local-only by default
- preserve 3B + 7B/8B default route strategy

After changes, run:
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider

Return a summary with subsystem, files changed, behavior added, validation, gates preserved, remaining scaffold, claims not made, next task.
```


## Prompt Pack PR-01 — Schema Strictening and Registry Parity

```text
You are implementing PR-01 — Schema Strictening and Registry Parity for Odin Agent Shell v7.1.
Read:
- AGENTS.md
- CODEX_START_HERE.md
- docs/codex/CODEX_TASK_LOCK_V0_4_0.md
- docs/codex/tasks/PR-01_SCHEMA_STRICTENING_AND_REGISTRY_PARITY.md
- all docs/schemas/registries referenced by the task file.

Goal:
Make JSON schemas and registries strict enough that protocol drift is caught early.

Hard boundaries:
- no LLM runtime in app templates
- candidate-only outputs
- app owns state/apply/external-send
- internal semantic bus local-only by default
- preserve 3B + 7B/8B default route strategy

After changes, run:
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider

Return a summary with subsystem, files changed, behavior added, validation, gates preserved, remaining scaffold, claims not made, next task.
```


## Prompt Pack PR-02 — Protocol Packets and Binding Gate

```text
You are implementing PR-02 — Protocol Packets and Binding Gate for Odin Agent Shell v7.1.
Read:
- AGENTS.md
- CODEX_START_HERE.md
- docs/codex/CODEX_TASK_LOCK_V0_4_0.md
- docs/codex/tasks/PR-02_PROTOCOL_PACKETS_AND_BINDING_GATE.md
- all docs/schemas/registries referenced by the task file.

Goal:
Implement local mediation packets, binding validation and caller policy enforcement.

Hard boundaries:
- no LLM runtime in app templates
- candidate-only outputs
- app owns state/apply/external-send
- internal semantic bus local-only by default
- preserve 3B + 7B/8B default route strategy

After changes, run:
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider

Return a summary with subsystem, files changed, behavior added, validation, gates preserved, remaining scaffold, claims not made, next task.
```


## Prompt Pack PR-03 — Universal Work Kernel

```text
You are implementing PR-03 — Universal Work Kernel for Odin Agent Shell v7.1.
Read:
- AGENTS.md
- CODEX_START_HERE.md
- docs/codex/CODEX_TASK_LOCK_V0_4_0.md
- docs/codex/tasks/PR-03_UNIVERSAL_WORK_KERNEL.md
- all docs/schemas/registries referenced by the task file.

Goal:
Implement Universal Work validation, compilation entrypoint and failure reasons.

Hard boundaries:
- no LLM runtime in app templates
- candidate-only outputs
- app owns state/apply/external-send
- internal semantic bus local-only by default
- preserve 3B + 7B/8B default route strategy

After changes, run:
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider

Return a summary with subsystem, files changed, behavior added, validation, gates preserved, remaining scaffold, claims not made, next task.
```


## Prompt Pack PR-04 — Candidate Artifacts Response Packets and Candidate DNA

```text
You are implementing PR-04 — Candidate Artifacts Response Packets and Candidate DNA for Odin Agent Shell v7.1.
Read:
- AGENTS.md
- CODEX_START_HERE.md
- docs/codex/CODEX_TASK_LOCK_V0_4_0.md
- docs/codex/tasks/PR-04_CANDIDATE_ARTIFACTS_RESPONSE_PACKETS_AND_CANDIDATE_DNA.md
- all docs/schemas/registries referenced by the task file.

Goal:
Implement candidate-only output objects, response bundles and traceable Candidate DNA.

Hard boundaries:
- no LLM runtime in app templates
- candidate-only outputs
- app owns state/apply/external-send
- internal semantic bus local-only by default
- preserve 3B + 7B/8B default route strategy

After changes, run:
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider

Return a summary with subsystem, files changed, behavior added, validation, gates preserved, remaining scaffold, claims not made, next task.
```


## Prompt Pack PR-05 — Internal Semantic Bus MVP

```text
You are implementing PR-05 — Internal Semantic Bus MVP for Odin Agent Shell v7.1.
Read:
- AGENTS.md
- CODEX_START_HERE.md
- docs/codex/CODEX_TASK_LOCK_V0_4_0.md
- docs/codex/tasks/PR-05_INTERNAL_SEMANTIC_BUS_MVP.md
- all docs/schemas/registries referenced by the task file.

Goal:
Build the local-only semantic event bus, event envelope validation and replay skeleton.

Hard boundaries:
- no LLM runtime in app templates
- candidate-only outputs
- app owns state/apply/external-send
- internal semantic bus local-only by default
- preserve 3B + 7B/8B default route strategy

After changes, run:
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider

Return a summary with subsystem, files changed, behavior added, validation, gates preserved, remaining scaffold, claims not made, next task.
```


## Prompt Pack PR-06 — Artifact Lenses and Context Distillery

```text
You are implementing PR-06 — Artifact Lenses and Context Distillery for Odin Agent Shell v7.1.
Read:
- AGENTS.md
- CODEX_START_HERE.md
- docs/codex/CODEX_TASK_LOCK_V0_4_0.md
- docs/codex/tasks/PR-06_ARTIFACT_LENSES_AND_CONTEXT_DISTILLERY.md
- all docs/schemas/registries referenced by the task file.

Goal:
Create artifact lens routing and compact context capsules bound to Universal Work.

Hard boundaries:
- no LLM runtime in app templates
- candidate-only outputs
- app owns state/apply/external-send
- internal semantic bus local-only by default
- preserve 3B + 7B/8B default route strategy

After changes, run:
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider

Return a summary with subsystem, files changed, behavior added, validation, gates preserved, remaining scaffold, claims not made, next task.
```


## Prompt Pack PR-07 — Worklet Graph Slot Forge and Gaptext

```text
You are implementing PR-07 — Worklet Graph Slot Forge and Gaptext for Odin Agent Shell v7.1.
Read:
- AGENTS.md
- CODEX_START_HERE.md
- docs/codex/CODEX_TASK_LOCK_V0_4_0.md
- docs/codex/tasks/PR-07_WORKLET_GRAPH_SLOT_FORGE_AND_GAPTEXT.md
- all docs/schemas/registries referenced by the task file.

Goal:
Split work into worklets, forge slot contracts and produce bounded gaptext.

Hard boundaries:
- no LLM runtime in app templates
- candidate-only outputs
- app owns state/apply/external-send
- internal semantic bus local-only by default
- preserve 3B + 7B/8B default route strategy

After changes, run:
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider

Return a summary with subsystem, files changed, behavior added, validation, gates preserved, remaining scaffold, claims not made, next task.
```


## Prompt Pack PR-08 — Model Scale Ladder Router and Mock Provider

```text
You are implementing PR-08 — Model Scale Ladder Router and Mock Provider for Odin Agent Shell v7.1.
Read:
- AGENTS.md
- CODEX_START_HERE.md
- docs/codex/CODEX_TASK_LOCK_V0_4_0.md
- docs/codex/tasks/PR-08_MODEL_SCALE_LADDER_ROUTER_AND_MOCK_PROVIDER.md
- all docs/schemas/registries referenced by the task file.

Goal:
Implement hardware-agnostic route selection with mock provider execution.

Hard boundaries:
- no LLM runtime in app templates
- candidate-only outputs
- app owns state/apply/external-send
- internal semantic bus local-only by default
- preserve 3B + 7B/8B default route strategy

After changes, run:
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider

Return a summary with subsystem, files changed, behavior added, validation, gates preserved, remaining scaffold, claims not made, next task.
```


## Prompt Pack PR-09 — Small Model Power Core

```text
You are implementing PR-09 — Small Model Power Core for Odin Agent Shell v7.1.
Read:
- AGENTS.md
- CODEX_START_HERE.md
- docs/codex/CODEX_TASK_LOCK_V0_4_0.md
- docs/codex/tasks/PR-09_SMALL_MODEL_POWER_CORE.md
- all docs/schemas/registries referenced by the task file.

Goal:
Add critic cascade, candidate tournament, style stabilizer and anti-generic engine.

Hard boundaries:
- no LLM runtime in app templates
- candidate-only outputs
- app owns state/apply/external-send
- internal semantic bus local-only by default
- preserve 3B + 7B/8B default route strategy

After changes, run:
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider

Return a summary with subsystem, files changed, behavior added, validation, gates preserved, remaining scaffold, claims not made, next task.
```


## Prompt Pack PR-10 — Thor Bridge and Bounded Code Work

```text
You are implementing PR-10 — Thor Bridge and Bounded Code Work for Odin Agent Shell v7.1.
Read:
- AGENTS.md
- CODEX_START_HERE.md
- docs/codex/CODEX_TASK_LOCK_V0_4_0.md
- docs/codex/tasks/PR-10_THOR_BRIDGE_AND_BOUNDED_CODE_WORK.md
- all docs/schemas/registries referenced by the task file.

Goal:
Map Thor-style handoff discipline into Odin candidate-only code and review flows.

Hard boundaries:
- no LLM runtime in app templates
- candidate-only outputs
- app owns state/apply/external-send
- internal semantic bus local-only by default
- preserve 3B + 7B/8B default route strategy

After changes, run:
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider

Return a summary with subsystem, files changed, behavior added, validation, gates preserved, remaining scaffold, claims not made, next task.
```


## Prompt Pack PR-11 — Storage Trace Receipt Layer

```text
You are implementing PR-11 — Storage Trace Receipt Layer for Odin Agent Shell v7.1.
Read:
- AGENTS.md
- CODEX_START_HERE.md
- docs/codex/CODEX_TASK_LOCK_V0_4_0.md
- docs/codex/tasks/PR-11_STORAGE_TRACE_RECEIPT_LAYER.md
- all docs/schemas/registries referenced by the task file.

Goal:
Add SQLite/object-store abstractions, trace entries, receipt candidates and retention hooks.

Hard boundaries:
- no LLM runtime in app templates
- candidate-only outputs
- app owns state/apply/external-send
- internal semantic bus local-only by default
- preserve 3B + 7B/8B default route strategy

After changes, run:
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider

Return a summary with subsystem, files changed, behavior added, validation, gates preserved, remaining scaffold, claims not made, next task.
```


## Prompt Pack PR-12 — Local API Server

```text
You are implementing PR-12 — Local API Server for Odin Agent Shell v7.1.
Read:
- AGENTS.md
- CODEX_START_HERE.md
- docs/codex/CODEX_TASK_LOCK_V0_4_0.md
- docs/codex/tasks/PR-12_LOCAL_API_SERVER.md
- all docs/schemas/registries referenced by the task file.

Goal:
Expose local-only HTTP endpoints for status, apps, work, bus, traces and scoreboard.

Hard boundaries:
- no LLM runtime in app templates
- candidate-only outputs
- app owns state/apply/external-send
- internal semantic bus local-only by default
- preserve 3B + 7B/8B default route strategy

After changes, run:
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider

Return a summary with subsystem, files changed, behavior added, validation, gates preserved, remaining scaffold, claims not made, next task.
```


## Prompt Pack PR-13 — SDKs and App Templates

```text
You are implementing PR-13 — SDKs and App Templates for Odin Agent Shell v7.1.
Read:
- AGENTS.md
- CODEX_START_HERE.md
- docs/codex/CODEX_TASK_LOCK_V0_4_0.md
- docs/codex/tasks/PR-13_SDKS_AND_APP_TEMPLATES.md
- all docs/schemas/registries referenced by the task file.

Goal:
Create TypeScript/Python SDK surfaces and no-LLM-in-app connector templates.

Hard boundaries:
- no LLM runtime in app templates
- candidate-only outputs
- app owns state/apply/external-send
- internal semantic bus local-only by default
- preserve 3B + 7B/8B default route strategy

After changes, run:
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider

Return a summary with subsystem, files changed, behavior added, validation, gates preserved, remaining scaffold, claims not made, next task.
```


## Prompt Pack PR-14 — Ollama and llama.cpp Provider Adapters

```text
You are implementing PR-14 — Ollama and llama.cpp Provider Adapters for Odin Agent Shell v7.1.
Read:
- AGENTS.md
- CODEX_START_HERE.md
- docs/codex/CODEX_TASK_LOCK_V0_4_0.md
- docs/codex/tasks/PR-14_OLLAMA_AND_LLAMA.CPP_PROVIDER_ADAPTERS.md
- all docs/schemas/registries referenced by the task file.

Goal:
Implement provider adapters behind ModelWorkPacket boundaries.

Hard boundaries:
- no LLM runtime in app templates
- candidate-only outputs
- app owns state/apply/external-send
- internal semantic bus local-only by default
- preserve 3B + 7B/8B default route strategy

After changes, run:
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider

Return a summary with subsystem, files changed, behavior added, validation, gates preserved, remaining scaffold, claims not made, next task.
```


## Prompt Pack PR-15 — Low-Memory Strict Mode

```text
You are implementing PR-15 — Low-Memory Strict Mode for Odin Agent Shell v7.1.
Read:
- AGENTS.md
- CODEX_START_HERE.md
- docs/codex/CODEX_TASK_LOCK_V0_4_0.md
- docs/codex/tasks/PR-15_LOW-MEMORY_STRICT_MODE.md
- all docs/schemas/registries referenced by the task file.

Goal:
Implement low-resource route limits, semantic bus light mode and small-slot preference.

Hard boundaries:
- no LLM runtime in app templates
- candidate-only outputs
- app owns state/apply/external-send
- internal semantic bus local-only by default
- preserve 3B + 7B/8B default route strategy

After changes, run:
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider

Return a summary with subsystem, files changed, behavior added, validation, gates preserved, remaining scaffold, claims not made, next task.
```


## Prompt Pack PR-16 — App QIRC Bridge Digest

```text
You are implementing PR-16 — App QIRC Bridge Digest for Odin Agent Shell v7.1.
Read:
- AGENTS.md
- CODEX_START_HERE.md
- docs/codex/CODEX_TASK_LOCK_V0_4_0.md
- docs/codex/tasks/PR-16_APP_QIRC_BRIDGE_DIGEST.md
- all docs/schemas/registries referenced by the task file.

Goal:
Prepare digest-only bridge between app-owned event systems and Odin internal bus.

Hard boundaries:
- no LLM runtime in app templates
- candidate-only outputs
- app owns state/apply/external-send
- internal semantic bus local-only by default
- preserve 3B + 7B/8B default route strategy

After changes, run:
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider

Return a summary with subsystem, files changed, behavior added, validation, gates preserved, remaining scaffold, claims not made, next task.
```


## Prompt Pack PR-17 — Model Dojo and Scoreboard

```text
You are implementing PR-17 — Model Dojo and Scoreboard for Odin Agent Shell v7.1.
Read:
- AGENTS.md
- CODEX_START_HERE.md
- docs/codex/CODEX_TASK_LOCK_V0_4_0.md
- docs/codex/tasks/PR-17_MODEL_DOJO_AND_SCOREBOARD.md
- all docs/schemas/registries referenced by the task file.

Goal:
Add model capability profiling and route quality metrics without model training.

Hard boundaries:
- no LLM runtime in app templates
- candidate-only outputs
- app owns state/apply/external-send
- internal semantic bus local-only by default
- preserve 3B + 7B/8B default route strategy

After changes, run:
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider

Return a summary with subsystem, files changed, behavior added, validation, gates preserved, remaining scaffold, claims not made, next task.
```


## Prompt Pack PR-18 — Control Center Skeleton

```text
You are implementing PR-18 — Control Center Skeleton for Odin Agent Shell v7.1.
Read:
- AGENTS.md
- CODEX_START_HERE.md
- docs/codex/CODEX_TASK_LOCK_V0_4_0.md
- docs/codex/tasks/PR-18_CONTROL_CENTER_SKELETON.md
- all docs/schemas/registries referenced by the task file.

Goal:
Prepare local control-center surfaces for apps, models, work lab, bus and traces.

Hard boundaries:
- no LLM runtime in app templates
- candidate-only outputs
- app owns state/apply/external-send
- internal semantic bus local-only by default
- preserve 3B + 7B/8B default route strategy

After changes, run:
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider

Return a summary with subsystem, files changed, behavior added, validation, gates preserved, remaining scaffold, claims not made, next task.
```


## Prompt Pack PR-19 — Windows Runtime Tray and Installer Prep

```text
You are implementing PR-19 — Windows Runtime Tray and Installer Prep for Odin Agent Shell v7.1.
Read:
- AGENTS.md
- CODEX_START_HERE.md
- docs/codex/CODEX_TASK_LOCK_V0_4_0.md
- docs/codex/tasks/PR-19_WINDOWS_RUNTIME_TRAY_AND_INSTALLER_PREP.md
- all docs/schemas/registries referenced by the task file.

Goal:
Define and scaffold Windows daemon lifecycle, tray integration and package boundaries.

Hard boundaries:
- no LLM runtime in app templates
- candidate-only outputs
- app owns state/apply/external-send
- internal semantic bus local-only by default
- preserve 3B + 7B/8B default route strategy

After changes, run:
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider

Return a summary with subsystem, files changed, behavior added, validation, gates preserved, remaining scaffold, claims not made, next task.
```


## Prompt Pack PR-20 — End-to-End Golden Flows

```text
You are implementing PR-20 — End-to-End Golden Flows for Odin Agent Shell v7.1.
Read:
- AGENTS.md
- CODEX_START_HERE.md
- docs/codex/CODEX_TASK_LOCK_V0_4_0.md
- docs/codex/tasks/PR-20_END-TO-END_GOLDEN_FLOWS.md
- all docs/schemas/registries referenced by the task file.

Goal:
Add representative local golden flows and negative paths across the full stack.

Hard boundaries:
- no LLM runtime in app templates
- candidate-only outputs
- app owns state/apply/external-send
- internal semantic bus local-only by default
- preserve 3B + 7B/8B default route strategy

After changes, run:
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider

Return a summary with subsystem, files changed, behavior added, validation, gates preserved, remaining scaffold, claims not made, next task.
```


## Prompt Pack PR-21 — Release Prep Hygiene and Support Bundle

```text
You are implementing PR-21 — Release Prep Hygiene and Support Bundle for Odin Agent Shell v7.1.
Read:
- AGENTS.md
- CODEX_START_HERE.md
- docs/codex/CODEX_TASK_LOCK_V0_4_0.md
- docs/codex/tasks/PR-21_RELEASE_PREP_HYGIENE_AND_SUPPORT_BUNDLE.md
- all docs/schemas/registries referenced by the task file.

Goal:
Add support bundle export, manifest refresh, docs parity and final pre-release gates.

Hard boundaries:
- no LLM runtime in app templates
- candidate-only outputs
- app owns state/apply/external-send
- internal semantic bus local-only by default
- preserve 3B + 7B/8B default route strategy

After changes, run:
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider

Return a summary with subsystem, files changed, behavior added, validation, gates preserved, remaining scaffold, claims not made, next task.
```

# v0.4.2 Prompt Pack Addendum

## PR-22 Prompt

Implement senior review hardening and anti-drift lock only. Do not add runtime features. Ensure review docs, traceability matrix, semantic bus red lines, risk register, registries, tests and FILE_MANIFEST are updated. Preserve no-LLM-in-app, candidate-only, app-owned apply, semantic-bus-local-only and default 3B+7B/8B hybrid invariants.


## PR-23 Shadow Runtime Prompt

Read `docs/SHADOW_RUNTIME_LOCK_V7_1.md`, `docs/SHADOW_RUNTIME_CODE_NEAR_BOOK_V7_1.md`, `docs/SHADOW_RUNTIME_TO_REAL_BUILD_MAPPING_V7_1.md`, and `odin/shadow_runtime/`. Implement only the next real target stated by the mapping. Preserve candidate-only, app-owned apply and semantic-bus local-only boundaries.


## v0.5.1 Full Shadow Runtime Coverage Update

- Added PR-24 — Full Shadow Runtime Coverage.
- Added REAL-PR-10 — Full Shadow Runtime Coverage.
- Rule: all future changes must update architecture/specs, internal PR ladder, REAL-PR bundle registry, shadow contract registry, System Map, tests and FILE_MANIFEST.

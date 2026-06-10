# Real GitHub PR Execution Plan v0.7.7

Actual execution registry: `registries/real_pr_execution_registry.json`.

This plan supersedes v0.7.6 by adding absolute alignment metadata: internal-task absorption, legacy-bundle absorption, existing/target path split, acceptance gates, proof boundaries and Master Architecture section binding.

## Actual Real PRs

### REAL-GH-PR-01 — Foundation, Canon, Protocol and Universal Work Core

- Depends on: none
- Internal tasks: PR-00, PR-01, PR-02, PR-03, PR-04, PR-116
- Legacy bundles: REAL-PR-01, REAL-PR-02, REAL-PR-28
- Existing paths: 11
- Target paths: 0
- Doc: `docs/codex/real_execution_prs/REAL-GH-PR-01_FOUNDATION_CANON_PROTOCOL_AND_UNIVERSAL_WORK_CORE.md`

Create the public repo foundation, strict JSON/registry hygiene, binding gate, Universal Work core, candidate artifact core, and current-canon root surface before feature implementation expands.

### REAL-GH-PR-02 — Semantic Bus, Storage, API, Worklets and Work Atom Runtime

- Depends on: REAL-GH-PR-01
- Internal tasks: PR-05, PR-06, PR-07, PR-11, PR-12, PR-108, PR-109, PR-110, PR-111
- Legacy bundles: REAL-PR-03, REAL-PR-05, REAL-PR-26
- Existing paths: 4
- Target paths: 5
- Doc: `docs/codex/real_execution_prs/REAL-GH-PR-02_SEMANTIC_BUS_STORAGE_API_WORKLETS_AND_WORK_ATOM_RUNTIME.md`

Implement local-only semantic bus, artifact lenses, context distillery, worklet graph, Work Atom runtime, storage/trace/receipt records and local API skeleton as one coherent execution substrate.

### REAL-GH-PR-03 — Model Runtime, Pre-LLM Intelligence and Universal Model/Agent Boundary

- Depends on: REAL-GH-PR-02
- Internal tasks: PR-08, PR-09, PR-14, PR-15, PR-17, PR-61, PR-62, PR-63, PR-64, PR-65, PR-66, PR-67, PR-68, PR-69, PR-70, PR-71, PR-72, PR-81, PR-82, PR-83, PR-84, PR-85
- Legacy bundles: REAL-PR-04, REAL-PR-07, REAL-PR-18, REAL-PR-19, REAL-PR-21
- Existing paths: 7
- Target paths: 3
- Doc: `docs/codex/real_execution_prs/REAL-GH-PR-03_MODEL_RUNTIME_PRE_LLM_INTELLIGENCE_AND_UNIVERSAL_MODEL_AGENT_BOUNDARY.md`

Build the model/agent worker layer: scale ladder, mock/local provider seams, low-memory strict behavior, pre-LLM intelligence, model-work avoidance, output composer, model/agent cards, permission cards and local/remote parity boundary.

### REAL-GH-PR-04 — Thor/Y/Mjolnir Handoff, AI-Git Safety and Review Pipeline

- Depends on: REAL-GH-PR-03
- Internal tasks: PR-10, PR-56, PR-57, PR-58, PR-59, PR-60, PR-73, PR-74, PR-75, PR-76, PR-77, PR-78, PR-79, PR-80, PR-86
- Legacy bundles: REAL-PR-05, REAL-PR-17, REAL-PR-20, REAL-PR-21
- Existing paths: 3
- Target paths: 7
- Doc: `docs/codex/real_execution_prs/REAL-GH-PR-04_THOR_Y_MJOLNIR_HANDOFF_AI_GIT_SAFETY_AND_REVIEW_PIPELINE.md`

Implement Thor bridge, bounded code work, AI-Git safety architecture, autonomy escalation gate, semantic diff/branch/merge, human review boundary and Thor/Y/Mjolnir handoff compiler pipeline.

### REAL-GH-PR-05 — Narrative Compiler, Shadow Runtime, Runtime Packs and Loki Anti-Pattern Layer

- Depends on: REAL-GH-PR-04
- Internal tasks: PR-23, PR-24, PR-25, PR-26, PR-27, PR-28, PR-29, PR-30, PR-31, PR-32, PR-33, PR-34, PR-35, PR-36, PR-37, PR-93, PR-94, PR-95, PR-96, PR-97
- Legacy bundles: REAL-PR-09, REAL-PR-10, REAL-PR-11, REAL-PR-12, REAL-PR-13, REAL-PR-23
- Existing paths: 8
- Target paths: 3
- Doc: `docs/codex/real_execution_prs/REAL-GH-PR-05_NARRATIVE_COMPILER_SHADOW_RUNTIME_RUNTIME_PACKS_AND_LOKI_ANTI_PATTERN_.md`

Build the code-near Shadow Runtime, Fairy/Y* narrative compiler, runtime pack/capability slice pipeline, generated gates, Shadow Narrative, Anti-Fairy DSL, Loki mediation and narrative red-team compiler.

### REAL-GH-PR-06 — Odin Core, QIRC Gold Spine, Seeds, Pattern Mines and Flow Packs

- Depends on: REAL-GH-PR-05
- Internal tasks: PR-38, PR-39, PR-40, PR-41, PR-42, PR-43, PR-44, PR-45, PR-46, PR-47, PR-48, PR-49, PR-50, PR-51, PR-52, PR-53, PR-54, PR-55, PR-87, PR-88, PR-89, PR-90, PR-91, PR-92, PR-103, PR-104, PR-105, PR-106, PR-107, PR-121
- Legacy bundles: REAL-PR-14, REAL-PR-15, REAL-PR-16, REAL-PR-22, REAL-PR-25, REAL-PR-28
- Existing paths: 6
- Target paths: 7
- Doc: `docs/codex/real_execution_prs/REAL-GH-PR-06_ODIN_CORE_QIRC_GOLD_SPINE_SEEDS_PATTERN_MINES_AND_FLOW_PACKS.md`

Implement Odin Core Centerline, QLI/DFAS/QMath route scoring, QIRC Gold Spine, Bug6/Q7 invariant layer, operational seed/archetype substrate, App Seed Pack compiler, Pattern Mine intake and Flow Pack bridge.

### REAL-GH-PR-07 — Windows Product Runtime, Odin Hub, Installer, IPC and Recovery

- Depends on: REAL-GH-PR-06
- Internal tasks: PR-18, PR-19, PR-98, PR-99, PR-100, PR-101, PR-102, PR-112, PR-113, PR-114, PR-115, PR-117, PR-118, PR-119, PR-120
- Legacy bundles: REAL-PR-07, REAL-PR-24, REAL-PR-27, REAL-PR-28
- Existing paths: 5
- Target paths: 6
- Doc: `docs/codex/real_execution_prs/REAL-GH-PR-07_WINDOWS_PRODUCT_RUNTIME_ODIN_HUB_INSTALLER_IPC_AND_RECOVERY.md`

Build the Windows product shape: host/daemon/tray/control center, Odin Hub panels, process contracts, named-pipe/localhost IPC, pairing/auth policy, installer/update/rollback, safe mode, diagnostics and support bundles.

### REAL-GH-PR-08 — App SDKs, App QIRC Digest, Golden Flows, Release Hygiene and Public Build Gate

- Depends on: REAL-GH-PR-07
- Internal tasks: PR-13, PR-16, PR-20, PR-21, PR-22, PR-122, PR-123
- Legacy bundles: REAL-PR-06, REAL-PR-08, REAL-PR-28
- Existing paths: 8
- Target paths: 0
- Doc: `docs/codex/real_execution_prs/REAL-GH-PR-08_APP_SDKS_APP_QIRC_DIGEST_GOLDEN_FLOWS_RELEASE_HYGIENE_AND_PUBLIC_BUILD.md`

Finalize app-facing SDK/templates, App QIRC digest bridge, golden flows, support bundle/release hygiene, senior-review hardening and public build-ready gate so the repo can be handed to Codex as a coherent build program.

## Execution Law

The eight PRs are the only actual GitHub implementation sequence. Internal ladders are traceability sources, not competing build plans.

# Codex Task Lock v0.4.0

**Status:** Codex Task Lock  
**Architecture:** Odin Agent Shell v7.1  
**Spec base:** v0.3.2 Deep Subsystem Spec Lock  
**Default model strategy:** 3B + 7B/8B hybrid  
**Purpose:** convert the full v7.1 architecture/spec canon into concrete Codex-ready implementation packages.

## 1. Codex Task Lock

This document is the controlling task map for the first implementation run. It does not replace `docs/MASTER_ARCHITECTURE_V7_1.md` or `docs/MASTER_SPECS_V7_1.md`. It binds implementation order, PR boundaries, Definition of Done, forbidden scope, and validation commands.

## 2. Reading Order

1. `START_HERE.md`
2. `CANON_ENTRY.md`
3. `SYSTEM_MAP.json`
4. `docs/MASTER_ARCHITECTURE_V7_1.md`
5. `docs/MASTER_SPECS_V7_1.md`
6. `docs/codex/CODEX_TASK_LOCK_V0_4_0.md`
7. `docs/codex/IMPLEMENTATION_SEQUENCE_V0_4_0.md`
8. exact task file under `docs/codex/tasks/`
9. relevant subsystem doc
10. relevant schema and registry

## 3. PR Task Index

| PR | Title | Depends On | Task Doc |
|---|---|---|---|
| PR-00 | Canon Gates and Repo Hygiene | none | `docs/codex/tasks/PR-00_CANON_GATES_AND_REPO_HYGIENE.md` |
| PR-01 | Schema Strictening and Registry Parity | PR-00 | `docs/codex/tasks/PR-01_SCHEMA_STRICTENING_AND_REGISTRY_PARITY.md` |
| PR-02 | Protocol Packets and Binding Gate | PR-01 | `docs/codex/tasks/PR-02_PROTOCOL_PACKETS_AND_BINDING_GATE.md` |
| PR-03 | Universal Work Kernel | PR-02 | `docs/codex/tasks/PR-03_UNIVERSAL_WORK_KERNEL.md` |
| PR-04 | Candidate Artifacts Response Packets and Candidate DNA | PR-03 | `docs/codex/tasks/PR-04_CANDIDATE_ARTIFACTS_RESPONSE_PACKETS_AND_CANDIDATE_DNA.md` |
| PR-05 | Internal Semantic Bus MVP | PR-02 | `docs/codex/tasks/PR-05_INTERNAL_SEMANTIC_BUS_MVP.md` |
| PR-06 | Artifact Lenses and Context Distillery | PR-03, PR-05 | `docs/codex/tasks/PR-06_ARTIFACT_LENSES_AND_CONTEXT_DISTILLERY.md` |
| PR-07 | Worklet Graph Slot Forge and Gaptext | PR-06 | `docs/codex/tasks/PR-07_WORKLET_GRAPH_SLOT_FORGE_AND_GAPTEXT.md` |
| PR-08 | Model Scale Ladder Router and Mock Provider | PR-07 | `docs/codex/tasks/PR-08_MODEL_SCALE_LADDER_ROUTER_AND_MOCK_PROVIDER.md` |
| PR-09 | Small Model Power Core | PR-08 | `docs/codex/tasks/PR-09_SMALL_MODEL_POWER_CORE.md` |
| PR-10 | Thor Bridge and Bounded Code Work | PR-04, PR-09 | `docs/codex/tasks/PR-10_THOR_BRIDGE_AND_BOUNDED_CODE_WORK.md` |
| PR-11 | Storage Trace Receipt Layer | PR-04, PR-05 | `docs/codex/tasks/PR-11_STORAGE_TRACE_RECEIPT_LAYER.md` |
| PR-12 | Local API Server | PR-03, PR-04, PR-05, PR-11 | `docs/codex/tasks/PR-12_LOCAL_API_SERVER.md` |
| PR-13 | SDKs and App Templates | PR-12 | `docs/codex/tasks/PR-13_SDKS_AND_APP_TEMPLATES.md` |
| PR-14 | Ollama and llama.cpp Provider Adapters | PR-08, PR-12 | `docs/codex/tasks/PR-14_OLLAMA_AND_LLAMA.CPP_PROVIDER_ADAPTERS.md` |
| PR-15 | Low-Memory Strict Mode | PR-08, PR-09 | `docs/codex/tasks/PR-15_LOW-MEMORY_STRICT_MODE.md` |
| PR-16 | App QIRC Bridge Digest | PR-05, PR-13 | `docs/codex/tasks/PR-16_APP_QIRC_BRIDGE_DIGEST.md` |
| PR-17 | Model Dojo and Scoreboard | PR-08, PR-09, PR-11 | `docs/codex/tasks/PR-17_MODEL_DOJO_AND_SCOREBOARD.md` |
| PR-18 | Control Center Skeleton | PR-12, PR-17 | `docs/codex/tasks/PR-18_CONTROL_CENTER_SKELETON.md` |
| PR-19 | Windows Runtime Tray and Installer Prep | PR-12, PR-18 | `docs/codex/tasks/PR-19_WINDOWS_RUNTIME_TRAY_AND_INSTALLER_PREP.md` |
| PR-20 | End-to-End Golden Flows | PR-13, PR-14, PR-16, PR-18 | `docs/codex/tasks/PR-20_END-TO-END_GOLDEN_FLOWS.md` |
| PR-21 | Release Prep Hygiene and Support Bundle | PR-20 | `docs/codex/tasks/PR-21_RELEASE_PREP_HYGIENE_AND_SUPPORT_BUNDLE.md` |

## 4. Dependency Rules

- Never skip a dependency unless the task file explicitly says the work is documentation-only.
- Never implement provider-specific inference before ModelWorkPacket validation exists.
- Never implement app templates with embedded provider logic.
- Never implement Windows UI before core packet, validation, semantic bus envelope and local API basics are stable.
- Never add remote provider behavior before local-only defaults, privacy gates and explicit permission policy are in place.

## 5. Gate Contract

Every PR must keep these commands green in the local repo context:

```bash
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider
```

Every PR must preserve:

```text
No LLM in App
Candidate-only output
App-owned state/apply/external-send
Internal Semantic Bus local-only by default
Model output is projection, not truth
Default sweet spot remains 3B + 7B/8B hybrid
Bigger models are escalation routes, not architecture
```

## 6. PR Granularity

Each PR must be small enough to review by subsystem but large enough to close a coherent contract. A PR may update docs, schemas, registries and code together only when those artifacts describe the same contract.

## 7. Codex Output Format

For every implementation answer or PR summary, Codex should report:

```text
Subsystem:
Files changed:
Behavior added:
Validation:
Gates preserved:
Known scaffold remaining:
Claims not made:
Next task:
```

## 8. Forbidden Implementation Moves

```text
Do not put LLM runtime logic in app templates.
Do not let Odin mutate app state.
Do not let Odin send externally.
Do not bypass ODIN_BINDING.
Do not bypass Caller Manifest.
Do not bypass output contracts.
Do not publish Internal Semantic Bus to WAN/LAN/public IRC by default.
Do not treat model output as truth.
Do not promote a candidate to applied state inside Odin.
Do not hardcode hardware-specific assumptions into the model route ladder.
```

## 9. Done for v0.4.0

v0.4.0 is done when:

- task registry exists and validates
- every task has a detailed PR doc
- dependency graph is explicit
- DoD matrix is explicit
- Codex prompt packs are present
- `SYSTEM_MAP.json` points to the task lock
- validation CLI checks Codex task coverage
- pytest includes task-lock tests


## v0.4.1 Bundle Overlay

PR-00 through PR-21 remain the internal task ladder. v0.4.1 adds REAL-PR-01 through REAL-PR-08 as the actual future Codex pull request bundles.

Use:

- `docs/codex/CODEX_REAL_PR_BUNDLE_PLAN_V0_4_1.md`
- `docs/codex/REAL_PR_BUNDLE_INDEX_V0_4_1.md`
- `registries/codex_pr_bundle_registry.json`
- `docs/codex/bundles/`

The bundle layer may not weaken or replace any internal PR task. It only groups tasks into reviewable implementation pull requests.

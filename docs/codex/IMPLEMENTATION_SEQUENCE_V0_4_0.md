# Implementation Sequence v0.4.0

This document gives the exact build order for Codex.

## Sequence Law

```text
contracts before runtime
schemas before validators
validators before model calls
candidate objects before app rendering
semantic bus envelope before bus behavior
mock provider before real providers
local-only before remote
```


## Step 1: PR-00 — Canon Gates and Repo Hygiene

**Dependency:** none  
**Task doc:** `docs/codex/tasks/PR-00_CANON_GATES_AND_REPO_HYGIENE.md`  
**Primary files:** `odin/cli.py`, `tests/test_validation_cli.py`, `SYSTEM_MAP.json`, `FILE_MANIFEST.json`

**Execution rule:** complete this step before dependent tasks. If a dependent task needs a new contract, update the contract in the same PR and add validation for the contract.

## Step 2: PR-01 — Schema Strictening and Registry Parity

**Dependency:** PR-00  
**Task doc:** `docs/codex/tasks/PR-01_SCHEMA_STRICTENING_AND_REGISTRY_PARITY.md`  
**Primary files:** `schemas/v7_1/`, `registries/`, `tests/test_registry_expansion.py`

**Execution rule:** complete this step before dependent tasks. If a dependent task needs a new contract, update the contract in the same PR and add validation for the contract.

## Step 3: PR-02 — Protocol Packets and Binding Gate

**Dependency:** PR-01  
**Task doc:** `docs/codex/tasks/PR-02_PROTOCOL_PACKETS_AND_BINDING_GATE.md`  
**Primary files:** `odin/protocol/`, `odin/apps/`, `schemas/v7_1/odin_binding.schema.json`

**Execution rule:** complete this step before dependent tasks. If a dependent task needs a new contract, update the contract in the same PR and add validation for the contract.

## Step 4: PR-03 — Universal Work Kernel

**Dependency:** PR-02  
**Task doc:** `docs/codex/tasks/PR-03_UNIVERSAL_WORK_KERNEL.md`  
**Primary files:** `odin/universal_work/`, `examples/universal_work/`, `tests/test_universal_work_validator.py`

**Execution rule:** complete this step before dependent tasks. If a dependent task needs a new contract, update the contract in the same PR and add validation for the contract.

## Step 5: PR-04 — Candidate Artifacts Response Packets and Candidate DNA

**Dependency:** PR-03  
**Task doc:** `docs/codex/tasks/PR-04_CANDIDATE_ARTIFACTS_RESPONSE_PACKETS_AND_CANDIDATE_DNA.md`  
**Primary files:** `odin/packets/`, `schemas/v7_1/odin_candidate_artifact.schema.json`

**Execution rule:** complete this step before dependent tasks. If a dependent task needs a new contract, update the contract in the same PR and add validation for the contract.

## Step 6: PR-05 — Internal Semantic Bus MVP

**Dependency:** PR-02  
**Task doc:** `docs/codex/tasks/PR-05_INTERNAL_SEMANTIC_BUS_MVP.md`  
**Primary files:** `odin/semantic_bus/`, `registries/semantic_bus_channels.json`, `tests/test_semantic_event.py`

**Execution rule:** complete this step before dependent tasks. If a dependent task needs a new contract, update the contract in the same PR and add validation for the contract.

## Step 7: PR-06 — Artifact Lenses and Context Distillery

**Dependency:** PR-03, PR-05  
**Task doc:** `docs/codex/tasks/PR-06_ARTIFACT_LENSES_AND_CONTEXT_DISTILLERY.md`  
**Primary files:** `odin/small_model_power/context_distillery.py`, `registries/artifact_lenses.json`

**Execution rule:** complete this step before dependent tasks. If a dependent task needs a new contract, update the contract in the same PR and add validation for the contract.

## Step 8: PR-07 — Worklet Graph Slot Forge and Gaptext

**Dependency:** PR-06  
**Task doc:** `docs/codex/tasks/PR-07_WORKLET_GRAPH_SLOT_FORGE_AND_GAPTEXT.md`  
**Primary files:** `odin/small_model_power/worklet_graph.py`, `odin/small_model_power/slot_forge.py`, `odin/slots/`

**Execution rule:** complete this step before dependent tasks. If a dependent task needs a new contract, update the contract in the same PR and add validation for the contract.

## Step 9: PR-08 — Model Scale Ladder Router and Mock Provider

**Dependency:** PR-07  
**Task doc:** `docs/codex/tasks/PR-08_MODEL_SCALE_LADDER_ROUTER_AND_MOCK_PROVIDER.md`  
**Primary files:** `odin/models/`, `registries/model_scale_ladder.json`

**Execution rule:** complete this step before dependent tasks. If a dependent task needs a new contract, update the contract in the same PR and add validation for the contract.

## Step 10: PR-09 — Small Model Power Core

**Dependency:** PR-08  
**Task doc:** `docs/codex/tasks/PR-09_SMALL_MODEL_POWER_CORE.md`  
**Primary files:** `odin/small_model_power/`, `odin/quality/`

**Execution rule:** complete this step before dependent tasks. If a dependent task needs a new contract, update the contract in the same PR and add validation for the contract.

## Step 11: PR-10 — Thor Bridge and Bounded Code Work

**Dependency:** PR-04, PR-09  
**Task doc:** `docs/codex/tasks/PR-10_THOR_BRIDGE_AND_BOUNDED_CODE_WORK.md`  
**Primary files:** `odin/thor_bridge/`, `docs/THOR_INTEGRATION.md`, `docs/BOUNDED_CODE_WORK.md`

**Execution rule:** complete this step before dependent tasks. If a dependent task needs a new contract, update the contract in the same PR and add validation for the contract.

## Step 12: PR-11 — Storage Trace Receipt Layer

**Dependency:** PR-04, PR-05  
**Task doc:** `docs/codex/tasks/PR-11_STORAGE_TRACE_RECEIPT_LAYER.md`  
**Primary files:** `odin/storage/`, `docs/STORAGE_SPEC.md`

**Execution rule:** complete this step before dependent tasks. If a dependent task needs a new contract, update the contract in the same PR and add validation for the contract.

## Step 13: PR-12 — Local API Server

**Dependency:** PR-03, PR-04, PR-05, PR-11  
**Task doc:** `docs/codex/tasks/PR-12_LOCAL_API_SERVER.md`  
**Primary files:** `odin/api/`, `docs/API_SPEC.md`

**Execution rule:** complete this step before dependent tasks. If a dependent task needs a new contract, update the contract in the same PR and add validation for the contract.

## Step 14: PR-13 — SDKs and App Templates

**Dependency:** PR-12  
**Task doc:** `docs/codex/tasks/PR-13_SDKS_AND_APP_TEMPLATES.md`  
**Primary files:** `sdk/`, `templates/app_connector/`, `docs/APP_INTEGRATION_STANDARD.md`

**Execution rule:** complete this step before dependent tasks. If a dependent task needs a new contract, update the contract in the same PR and add validation for the contract.

## Step 15: PR-14 — Ollama and llama.cpp Provider Adapters

**Dependency:** PR-08, PR-12  
**Task doc:** `docs/codex/tasks/PR-14_OLLAMA_AND_LLAMA.CPP_PROVIDER_ADAPTERS.md`  
**Primary files:** `odin/models/providers/`, `examples/model_profiles/`

**Execution rule:** complete this step before dependent tasks. If a dependent task needs a new contract, update the contract in the same PR and add validation for the contract.

## Step 16: PR-15 — Low-Memory Strict Mode

**Dependency:** PR-08, PR-09  
**Task doc:** `docs/codex/tasks/PR-15_LOW-MEMORY_STRICT_MODE.md`  
**Primary files:** `odin/core/resource_posture.py`, `docs/MODEL_SCALE_LADDER.md`

**Execution rule:** complete this step before dependent tasks. If a dependent task needs a new contract, update the contract in the same PR and add validation for the contract.

## Step 17: PR-16 — App QIRC Bridge Digest

**Dependency:** PR-05, PR-13  
**Task doc:** `docs/codex/tasks/PR-16_APP_QIRC_BRIDGE_DIGEST.md`  
**Primary files:** `odin/apps/app_qirc_bridge.py`, `schemas/v7_1/`

**Execution rule:** complete this step before dependent tasks. If a dependent task needs a new contract, update the contract in the same PR and add validation for the contract.

## Step 18: PR-17 — Model Dojo and Scoreboard

**Dependency:** PR-08, PR-09, PR-11  
**Task doc:** `docs/codex/tasks/PR-17_MODEL_DOJO_AND_SCOREBOARD.md`  
**Primary files:** `odin/small_model_power/model_dojo.py`, `registries/`

**Execution rule:** complete this step before dependent tasks. If a dependent task needs a new contract, update the contract in the same PR and add validation for the contract.

## Step 19: PR-18 — Control Center Skeleton

**Dependency:** PR-12, PR-17  
**Task doc:** `docs/codex/tasks/PR-18_CONTROL_CENTER_SKELETON.md`  
**Primary files:** `odin/api/`, `docs/WINDOWS_RUNTIME.md`, `templates/`

**Execution rule:** complete this step before dependent tasks. If a dependent task needs a new contract, update the contract in the same PR and add validation for the contract.

## Step 20: PR-19 — Windows Runtime Tray and Installer Prep

**Dependency:** PR-12, PR-18  
**Task doc:** `docs/codex/tasks/PR-19_WINDOWS_RUNTIME_TRAY_AND_INSTALLER_PREP.md`  
**Primary files:** `docs/WINDOWS_RUNTIME.md`, `.github/workflows/ci.yml`

**Execution rule:** complete this step before dependent tasks. If a dependent task needs a new contract, update the contract in the same PR and add validation for the contract.

## Step 21: PR-20 — End-to-End Golden Flows

**Dependency:** PR-13, PR-14, PR-16, PR-18  
**Task doc:** `docs/codex/tasks/PR-20_END-TO-END_GOLDEN_FLOWS.md`  
**Primary files:** `tests/`, `examples/`, `docs/FLOW_CATALOG_V7_1.md`

**Execution rule:** complete this step before dependent tasks. If a dependent task needs a new contract, update the contract in the same PR and add validation for the contract.

## Step 22: PR-21 — Release Prep Hygiene and Support Bundle

**Dependency:** PR-20  
**Task doc:** `docs/codex/tasks/PR-21_RELEASE_PREP_HYGIENE_AND_SUPPORT_BUNDLE.md`  
**Primary files:** `odin/storage/`, `docs/SECURITY_PRIVACY.md`, `README.md`

**Execution rule:** complete this step before dependent tasks. If a dependent task needs a new contract, update the contract in the same PR and add validation for the contract.

# v0.4.2 Sequence Addendum

PR-22 is executed after PR-21 as the final internal hardening step inside REAL-PR-08. It does not add runtime features. It locks review, traceability and anti-drift obligations.


## v0.5.1 Full Shadow Runtime Coverage Update

- Added PR-24 — Full Shadow Runtime Coverage.
- Added REAL-PR-10 — Full Shadow Runtime Coverage.
- Rule: all future changes must update architecture/specs, internal PR ladder, REAL-PR bundle registry, shadow contract registry, System Map, tests and FILE_MANIFEST.

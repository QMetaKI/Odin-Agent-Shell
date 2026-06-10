# Traceability Matrix v7.1

## Purpose

This matrix connects architecture laws, specs, subsystems, internal PR tasks and real PR bundles.

## Core Traceability

| Architecture Area | Primary Spec | Internal Tasks | Real Bundle |
|---|---|---|---|
| Canon / Gates / Repo Hygiene | AGENTS, CANON_ENTRY, CLAIM_BOUNDARY | PR-00 | REAL-PR-01 |
| Schemas / Registries | SCHEMA_POLICY, REGISTRY_POLICY | PR-01 | REAL-PR-01 |
| Protocol / Binding Gate | LOCAL_MEDIATION_PROTOCOL, APP_INTEGRATION_STANDARD | PR-02 | REAL-PR-01 |
| Universal Work Kernel | UNIVERSAL_WORK_KERNEL | PR-03 | REAL-PR-02 |
| Candidate Artifacts / Response Packets / Candidate DNA | MASTER_SPECS, DATA_CONTRACTS | PR-04 | REAL-PR-02 |
| Internal Semantic IRC Bus | INTERNAL_SEMANTIC_BUS | PR-05 | REAL-PR-03 |
| Artifact Lenses / Context Distillery | SMALL_MODEL_POWER_LAYER, ALGORITHMS | PR-06 | REAL-PR-03 |
| Worklet Graph / Slot Forge / Gaptext | SMALL_MODEL_POWER_LAYER, DATA_CONTRACTS | PR-07 | REAL-PR-03 |
| Model Scale Ladder / Mock Provider | MODEL_SCALE_LADDER | PR-08 | REAL-PR-04 |
| Small Model Power Core | SMALL_MODEL_POWER_LAYER | PR-09 | REAL-PR-04 |
| Thor Bridge / Bounded Code Work | THOR_INTEGRATION, BOUNDED_CODE_WORK | PR-10 | REAL-PR-05 |
| Storage / Trace / Receipt | STORAGE_SPEC, DATA_CONTRACTS | PR-11 | REAL-PR-05 |
| Local API | API_SPEC | PR-12 | REAL-PR-05 |
| SDKs / App Templates | APP_INTEGRATION_STANDARD | PR-13 | REAL-PR-06 |
| Provider Adapters | MODEL_SCALE_LADDER, API_SPEC | PR-14 | REAL-PR-04 |
| Low-Memory Strict Mode | MODEL_SCALE_LADDER, WINDOWS_RUNTIME | PR-15 | REAL-PR-04 |
| App QIRC Bridge Digest | APP_QIRC_BRIDGE_PREP, INTERNAL_SEMANTIC_BUS | PR-16 | REAL-PR-06 |
| Model Dojo / Scoreboard | SMALL_MODEL_POWER_LAYER | PR-17 | REAL-PR-07 |
| Control Center Skeleton | WINDOWS_RUNTIME | PR-18 | REAL-PR-07 |
| Windows Runtime / Tray / Installer Prep | WINDOWS_RUNTIME | PR-19 | REAL-PR-07 |
| End-to-End Golden Flows | FLOW_CATALOG, TESTING_AND_GATES | PR-20 | REAL-PR-08 |
| Release Hygiene / Support Bundle | SECURITY_PRIVACY, IMPLEMENTATION_DOD | PR-21 | REAL-PR-08 |
| Senior Review Hardening | SENIOR_REVIEW_REMEDIATION_PLAN, CODEX_ANTI_DRIFT_POLICY | PR-22 | REAL-PR-08 |

## Invariant Traceability

| Invariant | Enforced By | Must Be Tested In |
|---|---|---|
| No LLM in App | App templates, AGENTS, app integration tests | PR-13, REAL-PR-06 |
| Candidate-only outputs | Output contracts, response packets, final gate | PR-04, PR-20, REAL-PR-02, REAL-PR-08 |
| App owns apply | Binding gate, response actions, SDK renderer | PR-02, PR-13 |
| Semantic bus local-only | bus registry, bus API, security docs | PR-05, PR-16 |
| 3B + 7B/8B default | model scale ladder, router tests | PR-08, PR-14 |
| Bigger models escalation only | model router, resource profiles | PR-08, PR-15 |
| Remote explicit only | caller manifest, provider adapters | PR-02, PR-14 |
| Claim boundary | final gate, claim scanner, docs | PR-00, PR-04, PR-21 |
| Support bundle redacted by default | storage/export layer | PR-11, PR-21 |

## Required Use

Codex must reference this matrix when preparing PR summaries. Every real PR must identify which rows it touches and which invariants remain preserved.

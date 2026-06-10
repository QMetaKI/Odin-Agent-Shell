# REAL-PR-15 — Odin QIRC Gold Spine Hardening

## Objective

Bundle internal tasks PR-45 through PR-49 into one real Codex pull request scope. This bundle hardens Odin v7.1 around a deeper QIRC Gold Spine: channel taxonomy, event envelope v2, hot-window memory, seed/archetype prewarm, budget gates, admissibility, QMath/ring radar flow, why trace and runtime pack integration.

## Internal Tasks Covered

- PR-45 — QIRC Gold Spine Channel Taxonomy
- PR-46 — QIRC Event Envelope v2 and Hot Window Memory
- PR-47 — QIRC Seed / Archetype Prewarm and Budget Gates
- PR-48 — QIRC Admissibility / QMath / Ring Radar Flow
- PR-49 — QIRC Why Trace and Runtime Pack Integration

## Primary Files

- docs/ODIN_QIRC_GOLD_SPINE_V7_1.md
- docs/QIRC_CHANNEL_TAXONOMY_V7_1.md
- docs/QIRC_EVENT_ENVELOPE_V2_V7_1.md
- docs/QIRC_HOT_WINDOW_MEMORY_V7_1.md
- docs/QIRC_SEED_ARCHETYPE_PREWARM_V7_1.md
- docs/QIRC_ADMISSIBILITY_GATE_V7_1.md
- docs/QIRC_RING_RADAR_RUNTIME_V7_1.md
- docs/QIRC_WHY_TRACE_V7_1.md
- docs/QIRC_RUNTIME_PACK_INTEGRATION_V7_1.md
- docs/QIRC_APP_BRIDGE_DIGEST_V7_1.md
- schemas/v7_1/odin_qirc_event.schema.json
- registries/qirc_channel_registry.json
- odin/shadow_runtime/qirc_gold_spine_shadow.py
- tests/test_qirc_gold_spine.py

## Required Behavior

Codex must treat this bundle as QIRC centerline hardening, not network feature expansion. QIRC must remain local-only, internal, typed, append-only in posture, traceable and non-authoritative. The implementation must ensure that model dispatch cannot occur before admissibility, QIRC events carry trace and privacy metadata, seed/archetype prewarm is budgeted, ring activation is thresholded, why trace is redacted, and runtime packs can compile minimal channel slices.

## Forbidden Scope

- no public IRC
- no LAN/phone mesh
- no app-state ownership
- no app mutation
- no external send
- no provider dispatch before admissibility
- no unbounded seed fanout
- no raw secret payloads in QIRC events
- no hot-path runtime generation
- no weakening of existing v7.1 boundaries

## Definition of Done

- All PR-45..PR-49 task docs exist.
- All referenced docs, schemas, registries, shadow modules and tests exist.
- `validate-all` is clean.
- Test suite is green.
- PR bundle registry covers all internal tasks.
- FILE_MANIFEST is refreshed.
- QIRC explains why less model work was needed.

## Codex PR Summary Template

Summary:
- Added Odin QIRC Gold Spine hardening.
- Added typed QIRC event envelope, hot-window memory, seed prewarm, admissibility, ring radar and why-trace contracts.
- Preserved app-owned apply and candidate-only output.

Validation:
- `python -m odin.cli validate-all`
- `python -m pytest -q`

## Bundle Review Matrix

This bundle is accepted only if the implementation demonstrates one continuous internal event spine:

```text
Universal Work → QIRC Event → Hot Window → Seed Prewarm → Admissibility → QMath/Ring Radar → Worklet/Slot → Model Route or Hold → Candidate → Why Trace
```

Each stage must be independently testable and also composable through the QIRC Gold Spine shadow path.

## Bundle Negative Conditions

The bundle fails review if any QIRC path mutates app state, dispatches a model before admissibility, mirrors full app state, exposes raw private payloads, or adds network behavior to core.

# REAL-PR-14 — Odin Core / QLI / DFAS / Seed Economy Hardening

## Objective

Bundle internal tasks PR-38 through PR-44 into one real Codex pull request scope. This bundle hardens Odin v7.1 around centerline authority, QLI-like precompute interface, DFAS stability/admissibility, Seed/Archetype Economy, QMath Center Solver, Ring Radar/Resonance/Why Trace, Maria/Michael Superposition and QFoundation/QMetamodell intake bindings.

## Internal Tasks Covered

- PR-38 — Odin Core Centerline and QLI Master Interface
- PR-39 — DFAS Stability Core and Admissibility Gate
- PR-40 — Seed / Archetype Economy and Conflict Resolver
- PR-41 — QMath Center Solver and Route Score Engine
- PR-42 — Ring Radar / Resonance / Why Trace
- PR-43 — Maria / Michael Superposition Policy
- PR-44 — QFoundation / Q Metamodell Intake Binding

## Primary Files

- docs/ODIN_CORE_CENTERLINE_V7_1.md
- docs/ODIN_QLI_MASTER_INTERFACE_V7_1.md
- docs/DFAS_STABILITY_CORE_V7_1.md
- docs/SEED_ARCHETYPE_ECONOMY_V7_1.md
- docs/QMATH_CENTER_SOLVER_V7_1.md
- docs/RING_RADAR_RESONANCE_V7_1.md
- docs/WHY_TRACE_EXPLAINABILITY_V7_1.md
- docs/MARIA_MICHAEL_SUPERPOSITION_V7_1.md
- docs/QFOUNDATION_SYSTEM_INTAKE_V7_1.md
- docs/Q_METAMODELL_INTAKE_V7_1.md
- schemas/v7_1/odin_centerline_packet.schema.json
- registries/seed_registry.json
- odin/shadow_runtime/qli_master_interface_shadow.py
- tests/test_odin_core_qli_dfas_seed_economy.py

## Required Behavior

Codex must treat this bundle as centerline hardening, not feature expansion. The implementation must ensure that model routing cannot happen before admissibility, seed/archetype activation is budgeted and typed, route score explains model choice, Maria/Michael is a profile not persona, and Why Trace provides redacted explainability.

## Forbidden Scope

- no direct provider dispatch bypassing centerline
- no app authority takeover
- no persona simulation
- no unbounded seed fanout
- no hot-path runtime code generation
- no external send by Odin
- no app apply by Odin
- no unredacted why trace

## Definition of Done

- All PR-38..PR-44 task docs exist.
- All referenced docs, schemas, registries, shadow modules and tests exist.
- `validate-all` passes.
- Test suite passes.
- PR bundle registry covers all internal tasks.
- FILE_MANIFEST is refreshed.

## Codex PR Summary Template

Summary:
- Added Odin Core / QLI / DFAS / Seed Economy hardening.
- Added typed centerline, admissibility, seed/archetype, QMath, resonance and why-trace contracts.
- Preserved app-owned apply and candidate-only output.

Validation:
- `python -m odin.cli validate-all`
- `python -m pytest -q`


## Bundle Review Matrix

This bundle is accepted only if the implementation demonstrates a single continuous pre-model spine. The required chain is:

```text
Universal Work → Centerline Packet → Admissibility Decision → Seed Activation Packet → Archetype Role Packet → QMath Route Score → Ring Activation Map → Why Trace → Model Route / Hold / Ask / Split / Block
```

Each part must remain independently testable and also composable through the QLI Master Interface shadow path. The bundle must not add product-facing Q terminology unless deliberately documented as internal-only. Public repo wording should use Odin Core, Centerline, Stability Core, Seed Economy, Pattern Roles, Route Score and Why Trace.

## Bundle Negative Conditions

The bundle fails review if provider adapters can be called before admissibility, if route score is omitted, if seeds are unbounded, if Maria/Michael is implemented as persona text, if Why Trace includes raw private app state, or if any task weakens existing v7.1 boundaries.

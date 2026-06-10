# PR-47 — QIRC Seed / Archetype Prewarm and Budget Gates

## Objective

Implement and preserve the QIRC Seed / Archetype Prewarm and Budget Gates scope as a bounded Odin v7.1 QIRC Gold Spine slice. This task extends the existing v7.1 canon without weakening Universal Work, candidate-only output, app-owned apply, Internal Semantic Bus local-only constraints, Shadow Runtime boundaries, Odin Core / QLI admissibility, DFAS stability, Seed / Archetype Economy, Maria/Michael Superposition or the Narrative Aorta compiler discipline.

## Internal Task ID

PR-47

## Primary Files

- docs/QIRC_SEED_ARCHETYPE_PREWARM_V7_1.md
- registries/qirc_role_channel_matrix.json
- odin/shadow_runtime/qirc_seed_prewarm_shadow.py

- tests/test_qirc_gold_spine.py
- registries/codex_task_registry.json
- registries/codex_pr_bundle_registry.json

## Required Behavior

Codex must implement this task as typed contracts, deterministic helper functions, registry entries and tests. QIRC must remain local-only, typed, traceable, redacted, and non-authoritative. Every QIRC event must preserve candidate-only output and must not mutate app state. The QIRC Gold Spine must reduce model work through hot windows, seed prewarm, admissibility, ring-local activation, route scoring and why trace.

## Forbidden Scope

- no app mutation
- no external send
- no public IRC
- no network expansion in core
- no model dispatch before admissibility
- no unbounded seed fanout
- no raw secret payloads
- no app-state mirror
- no runtime-proof claims
- no weakening of claim boundary
- no bypass of Odin Final Gate

## Definition of Done

- Documentation exists and names the QIRC boundary clearly.
- Schema or registry exists when data is exchanged.
- Shadow module exists where runtime behavior is planned.
- Tests cover valid and invalid paths.
- SYSTEM_MAP, FILE_MANIFEST and registries are updated.
- This task is covered by `REAL-PR-15`.
- QIRC remains a reason Odin does less model guessing, not a new authority layer.

## Codex PR Summary Template

Summary:
- Implemented {title}.
- Preserved Odin candidate-only and app-owned authority boundaries.
- Added QIRC Gold Spine tests and registry coverage.

Validation:
- `python -m odin.cli validate-all`
- `python -m pytest -q`

## Implementation Notes

This task must be implemented in the same mechanical style as the rest of Odin: contract first, schema second, registry third, shadow module fourth, tests fifth. The implementation must remain deterministic and local-only. It must not introduce hidden agent autonomy, implied runtime proof, direct apply, external send or model route shortcuts.

Codex must explicitly preserve the following invariant chain:

```text
Universal Work → QIRC Hot Window → Seed Prewarm → Admissibility Gate → QMath/Ring Radar → Worklet/Slot → Model Route or Hold → Candidate Artifact → Why Trace
```

The task is incomplete if it only adds prose. It must include enough machine-readable structure for later implementation to follow mechanically.

## Review Checklist

- Does this task preserve app-owned state and app-owned apply?
- Does this task preserve candidate-only output?
- Does this task produce typed data rather than free-form prose?
- Does this task explain route decisions or blocked decisions?
- Does this task update Codex task registry, bundle registry and file manifest?
- Does this task keep public terminology neutral while preserving internal semantics?

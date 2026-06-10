# v0.7.6 — Real PR Execution Consolidation Lock

## Purpose

This lock converts the accumulated Odin internal PR ladder and legacy real-bundle ladder into a small actual GitHub PR execution sequence.

The repo now has three levels:

1. `codex_task_registry.json` — micro-task internal ladder.
2. `codex_pr_bundle_registry.json` — legacy internal bundle ladder.
3. `real_pr_execution_registry.json` — actual future GitHub PR execution ladder.

Only the third level should drive the real Codex build path.

## Consolidation Rule

Do not ask Codex to open 124 micro PRs or 28 legacy bundle PRs. Those are planning and traceability layers. The real build path is eight PRs:

- `REAL-GH-PR-01` — Foundation, Canon, Protocol and Universal Work Core
- `REAL-GH-PR-02` — Semantic Bus, Storage, API, Worklets and Work Atom Runtime
- `REAL-GH-PR-03` — Model Runtime, Pre-LLM Intelligence and Universal Model/Agent Boundary
- `REAL-GH-PR-04` — Thor/Y/Mjolnir Handoff, AI-Git Safety and Review Pipeline
- `REAL-GH-PR-05` — Narrative Compiler, Shadow Runtime, Runtime Packs and Loki Anti-Pattern Layer
- `REAL-GH-PR-06` — Odin Core, QIRC Gold Spine, Seeds, Pattern Mines and Flow Packs
- `REAL-GH-PR-07` — Windows Product Runtime, Odin Hub, Installer, IPC and Recovery
- `REAL-GH-PR-08` — App SDKs, App QIRC Digest, Golden Flows, Release Hygiene and Public Build Gate


## Senior Reviewer Simulation

### SR-01 — Reviewability

Eight PRs is acceptable. Each PR covers a coherent subsystem group and preserves dependency order.

### SR-02 — Risk Containment

The sequence prevents the largest risk: implementing Windows product runtime before core candidate/work/model boundaries exist.

### SR-03 — Scope Boundary

The old ladders must not be deleted because validators, traceability and detailed Codex task docs depend on them. They are reclassified as internal ladders.

### SR-04 — Execution Recommendation

Use `REAL-GH-PR-01` through `REAL-GH-PR-08` as the actual GitHub PR sequence. Keep the internal task IDs in each PR description as acceptance traceability.

## Non-Claims

This lock is repo-prep. It does not prove runtime execution, Windows host behavior, model inference, installer behavior, security certification, network transport, or app apply.


## v0.7.7 Absolute Alignment Update

The consolidated real execution registry is now upgraded by `docs/BUILD_LADDER_ABSOLUTE_ALIGNMENT_LOCK_V7_1.md`.

Every `REAL-GH-PR` now declares absorbed internal tasks, absorbed legacy bundles, existing prep paths, target implementation paths, acceptance gates, proof boundaries, required commands, invariants and Master Architecture section binding.

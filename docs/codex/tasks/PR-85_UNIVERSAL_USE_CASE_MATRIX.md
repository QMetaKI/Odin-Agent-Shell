# PR-85 — Universal Use Case Matrix

## Objective
Implement the Universal Use Case Matrix layer as part of the universal Thor+Odin AI-Git construct. This task keeps Odin v7.1 candidate-only, local-first where possible, app-owned for apply, and GPL-2.0-only. It must not introduce a runtime claim, model authority, agent swarm behavior, network relay behavior, or app mutation.

## Primary Files
- docs/UNIVERSAL_USE_CASE_MATRIX_V7_1.md
- odin/shadow_runtime/universal_use_case_matrix_shadow.py
- registries/codex_task_registry.json
- registries/codex_pr_bundle_registry.json
- SYSTEM_MAP.json
- FILE_MANIFEST.json

## Required Behavior
Codex must create typed, testable, candidate-only artifacts. All model and agent work must be represented by Capability Cards, Permission Cards, Work Capsules, Return Contracts, Candidate Artifacts and Why Trace. Any external or remote worker must be redacted and gated. The GPL-2.0-only policy must remain visible in license and policy files.

## Forbidden Scope
No model calls. No network calls. No app apply. No external send. No hidden tool execution. No claim acceptance. No receipt issuance by a model or agent. No broad autonomous agent framework. No weakening of Thor handoff boundaries. No weakening of Odin Final Gate. No license downgrade or permissive relicensing.

## Definition of Done
- validate-all passes.
- pytest passes.
- Required docs exist and contain boundary language.
- Registry entries are present.
- Shadow Runtime mappings are present where relevant.
- Any new schema is valid JSON Schema.
- Bundle coverage includes this task.
- FILE_MANIFEST is refreshed.

## Codex PR Summary Template
Summary: Implements PR-85 Universal Use Case Matrix as candidate-only, GPL-2.0-only, Thor+Odin AI-Git work infrastructure.
Validation: `python -m odin.cli validate-all`; `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`.
Boundaries: no apply, no external send, no model authority, no runtime proof claim.

## Notes
This task is intentionally broad enough to be a future implementation slice while still being bounded by the existing architecture. It must preserve the internal PR ladder and the REAL-PR bundle mapping.


## Additional implementation guidance
This section exists to make the future Codex implementation unambiguous. The task must preserve the whole v7.1 architecture: Universal Work, Thor handoff compiler, QIRC Gold Spine, Odin Core/QLI/DFAS, Seed/Archetype Economy, QMath, Shadow Runtime, Runtime Pack Compiler, AI-Git Safety, Pre-LLM Intelligence, Universal Model/Agent Parity and candidate-only returns. It must update schemas, registries, tests, examples, system map, file manifest and documentation together. It must never treat a model or an agent as authority. It must never create automatic apply, automatic merge, external send, unvalidated tool execution, raw secret exposure, or runtime proof claims. The implementation should prefer smallest sufficient worker, local-first routing, remote redaction, capability cards, permission cards, work capsules and why trace over prompt-only delegation.

## Review notes
Senior review should verify that the resulting PR is understandable without chat context, follows the existing PR ladder, maps into REAL-PR-21, and does not weaken prior REAL-PR bundles. The implementation should be boring, typed, testable and deterministic wherever possible. Any future model call, remote adapter, tool gateway or app bridge remains a candidate path until reviewed by app-owned apply gates.

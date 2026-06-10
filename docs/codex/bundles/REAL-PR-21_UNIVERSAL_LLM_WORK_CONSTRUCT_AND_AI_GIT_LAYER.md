# REAL-PR-21 — Universal LLM Work Construct and AI-Git Layer

## Objective
Consolidate Thor+Odin as a universal model/agent/app/workflow AI-Git layer. This bundle generalizes Odin beyond Y-native apps while preserving v7.1 invariants: candidate-only, app-owned apply, local-first where possible, QIRC/DFAS/Seed precompute before model work, and GPL-2.0-only license identity.

## Internal Tasks Covered
- PR-81 — Universal LLM Work Construct
- PR-82 — Universal Model Agent Adapter Contract
- PR-83 — Remote Worker Boundary and Local Remote Parity
- PR-84 — Agent Tool Permission Boundary
- PR-85 — Universal Use Case Matrix
- PR-86 — Thor Odin AI Git Work Session and GPL2 Policy

## Primary Files
- docs/UNIVERSAL_LLM_WORK_CONSTRUCT_V7_1.md
- docs/THOR_ODIN_AI_GIT_LAYER_V7_1.md
- docs/UNIVERSAL_MODEL_AGENT_ADAPTERS_V7_1.md
- docs/REMOTE_MODEL_WORKER_BOUNDARY_V7_1.md
- docs/LOCAL_REMOTE_LLM_PARITY_V7_1.md
- docs/AGENT_TOOL_PERMISSION_BOUNDARY_V7_1.md
- docs/UNIVERSAL_USE_CASE_MATRIX_V7_1.md
- docs/ANY_MODEL_ANY_AGENT_SAME_BOUNDARY_V7_1.md
- docs/THOR_ODIN_GPL2_ONLY_POLICY.md
- registries/universal_llm_worker_registry.json
- schemas/v7_1/odin_universal_llm_worker.schema.json
- odin/shadow_runtime/universal_llm_work_construct_shadow.py

## Required Behavior
Every model or agent is normalized into a Capability Card, Permission Card, Work Capsule, Adapter Boundary, Candidate Protocol and Why Trace. Remote models are candidate workers only. Tool agents are proposal workers only unless a future explicit app-owned gateway is added. Odin never applies, never sends externally and never accepts claims on behalf of a worker.

## Forbidden Scope
No autonomous agent framework. No agent swarm. No direct tool execution. No app apply. No external send. No license weakening. No permissive relicensing. No bypass of Thor return contracts. No bypass of Odin Final Gate. No raw secret payloads to remote workers.

## Definition of Done
- All PR-81 through PR-86 task docs exist.
- The bundle registry covers PR-81 through PR-86.
- New schemas and registries are valid.
- New shadow modules are present.
- License policy files exist and state GPL-2.0-only.
- validate-all passes.
- pytest passes.

## Codex PR Summary Template
Summary: Implements REAL-PR-21 universal model/agent work construct and GPL-2.0-only AI-Git layer.
Validation: `python -m odin.cli validate-all`; `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`.
Boundaries: same Odin boundary for any model/agent; candidate-only; app-owned apply; GPL-2.0-only.


## Additional implementation guidance
This section exists to make the future Codex implementation unambiguous. The task must preserve the whole v7.1 architecture: Universal Work, Thor handoff compiler, QIRC Gold Spine, Odin Core/QLI/DFAS, Seed/Archetype Economy, QMath, Shadow Runtime, Runtime Pack Compiler, AI-Git Safety, Pre-LLM Intelligence, Universal Model/Agent Parity and candidate-only returns. It must update schemas, registries, tests, examples, system map, file manifest and documentation together. It must never treat a model or an agent as authority. It must never create automatic apply, automatic merge, external send, unvalidated tool execution, raw secret exposure, or runtime proof claims. The implementation should prefer smallest sufficient worker, local-first routing, remote redaction, capability cards, permission cards, work capsules and why trace over prompt-only delegation.

## Review notes
Senior review should verify that the resulting PR is understandable without chat context, follows the existing PR ladder, maps into REAL-PR-21, and does not weaken prior REAL-PR bundles. The implementation should be boring, typed, testable and deterministic wherever possible. Any future model call, remote adapter, tool gateway or app bridge remains a candidate path until reviewed by app-owned apply gates.


## Additional implementation guidance
This section exists to make the future Codex implementation unambiguous. The task must preserve the whole v7.1 architecture: Universal Work, Thor handoff compiler, QIRC Gold Spine, Odin Core/QLI/DFAS, Seed/Archetype Economy, QMath, Shadow Runtime, Runtime Pack Compiler, AI-Git Safety, Pre-LLM Intelligence, Universal Model/Agent Parity and candidate-only returns. It must update schemas, registries, tests, examples, system map, file manifest and documentation together. It must never treat a model or an agent as authority. It must never create automatic apply, automatic merge, external send, unvalidated tool execution, raw secret exposure, or runtime proof claims. The implementation should prefer smallest sufficient worker, local-first routing, remote redaction, capability cards, permission cards, work capsules and why trace over prompt-only delegation.

## Review notes
Senior review should verify that the resulting PR is understandable without chat context, follows the existing PR ladder, maps into REAL-PR-21, and does not weaken prior REAL-PR bundles. The implementation should be boring, typed, testable and deterministic wherever possible. Any future model call, remote adapter, tool gateway or app bridge remains a candidate path until reviewed by app-owned apply gates.

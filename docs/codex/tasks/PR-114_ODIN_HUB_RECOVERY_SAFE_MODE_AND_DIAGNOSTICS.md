# PR-114 — Odin Hub Recovery Safe Mode and Diagnostics

## Objective
Define Hub recovery, safe-mode, rollback and support workflow.

## Internal Lock
This task belongs to the v0.7.4 Product / Pattern / Atom / Hub Lock. It must preserve all existing Odin v7.1 boundaries: candidate-only output, app-owned apply, local-first default, GPL-2.0-only identity, no hidden execution, no unvalidated runtime pack, and no agent/model authority transfer.

## Primary Files
- docs/ODIN_HUB_RECOVERY_AND_SAFE_MODE_V7_1.md
- odin/shadow_runtime/odin_hub_recovery_shadow.py

## Required Behavior
- Implement the documented contract as a candidate-only architecture/runtime-prep surface.
- Add schema, registry, fixture and test coverage before runtime behavior.
- Tie every visible operation to Why Trace, Candidate Artifact or support-bundle redaction where applicable.
- Preserve PR-Ladder and REAL-PR-Bundle traceability.
- Maintain negative fixtures for direct apply, external send, runtime proof and source-authority inflation.

## Forbidden Scope
- No direct app mutation.
- No external send.
- No public network expansion.
- No hidden execution.
- No production/runtime-proof claim.
- No weakening GPL-2.0-only policy.
- No bypass of Odin Final Gate.

## Definition of Done
- Primary files exist and are referenced by SYSTEM_MAP.json where relevant.
- At least one valid and one invalid fixture exists for the subsystem or lock group.
- Tests cover positive and negative behavior.
- `python -m odin.cli validate-all` succeeds.
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider` succeeds.
- FILE_MANIFEST.json is refreshed.

## Codex PR Summary Template
- Scope:
- Files changed:
- Validation run:
- Boundary checks:
- Remaining gaps:
- Why this preserves v7.1:

## Additional Codex Guardrails
Codex must treat this task as architecture-to-runtime preparation. It may add adapters, validators and shadow code, but may not claim executable host proof. Every candidate behavior must be paired with an invalid fixture. Every new registry entry must be referenced by either a schema, a shadow module, a task file, or a bundle file. The change must preserve previously defined v7.1 layers including Thor/Y/Mjölnir Handoff Compiler, QIRC Gold Spine, Odin Core/QLI/DFAS, Seed Economy, Shadow Runtime, Shadow Narrative/Loki, Universal LLM Work and App Seed Pack Compiler.

## Review Checklist
- Does the task preserve app-owned apply?
- Does the task avoid hidden execution?
- Does the task expose Why Trace or support-bundle context where relevant?
- Does the task avoid positive runtime-proof claims?
- Does the task keep GPL-2.0-only policy intact?
- Does the task update tests and registries?
- Does the task maintain Codex bundle traceability?

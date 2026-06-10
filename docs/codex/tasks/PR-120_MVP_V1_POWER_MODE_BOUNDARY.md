# PR-120 — MVP V1 Power Mode Boundary

## Objective

Implement the MVP V1 Power Mode Boundary scope as a candidate-only public repo and Windows build readiness preparation slice. This task is part of v0.7.5 and must preserve all existing v7.1 boundaries.

## Primary Files

- `docs/MVP_V1_POWER_MODE_BOUNDARY_V7_1.md`
- `registries/mvp_v1_power_mode_registry.json`

## Required Behavior

- Keep root documents focused on current canon.
- Preserve GPL-2.0-only identity.
- Preserve candidate-only output.
- Preserve app-owned apply and no external send by Odin.
- Add or update schemas, registries, shadow modules and tests when behavior changes.
- Keep Windows implementation work local-first, loopback-bound and pack-validation-aware.

## Forbidden Scope

- No app apply.
- No external send.
- No host validation claim.
- No model inference proof claim.
- No remote default.
- No hidden execution.
- No unvalidated runtime pack load.
- No seed or pattern pack executable code path.

## Definition of Done

- Relevant docs exist and contain concrete behavior.
- Registries include registry_id and version.
- JSON validates.
- `python -m odin.cli validate-all` succeeds.
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider` succeeds.
- FILE_MANIFEST is refreshed.
- SYSTEM_MAP references remain valid.

## Codex PR Summary Template

```text
Scope: PR-120 — MVP V1 Power Mode Boundary
Changed files:
Validation:
Boundary preservation:
Remaining gaps:
```

## Notes

This task is not a runtime-proof task. It only prepares the public repository and Windows build path for later implementation.

## Implementation Notes

Codex must treat this task as a repository-preparation and specification-hardening task. It may add scaffolding and validators, but must not claim live host behavior. Any code created in this task must be deterministic, local, and read-only unless the task explicitly declares a candidate artifact output. When a decision involves Windows host behavior, the implementation should prefer explicit state machines and manifest validation over ad-hoc helper behavior.

## Traceability Requirements

This task must remain traceable to the v7.1 Master Architecture, Master Specs, SYSTEM_MAP, FILE_MANIFEST, Codex Task Registry, Real PR Bundle Registry, and the relevant shadow runtime contracts. If a new artifact is added, it must be listed in FILE_MANIFEST and must not create an undocumented authority path. If a file introduces new terminology, it must either use existing registry terms or add a registry entry.

## Review Checklist

- Current-canon reading path remains clear.
- User/app authority remains outside Odin.
- Runtime claims remain bounded to prep/spec status.
- Windows behavior is represented as a build target, not a verified host state.
- Seed and pattern packs remain compile-only inputs.
- Local IPC remains loopback or named-pipe scoped.
- Safe mode and rollback are preserved as required behavior.
- Power Mode never weakens MVP safety.

## Negative Path Requirements

The implementation must include at least one negative-path consideration. Examples: invalid pairing token, external binding attempt, untrusted seed pack, pack validation failure, missing support-bundle redaction, root document drift, or Power Mode attempting to bypass MVP boundaries. Negative paths should produce candidate-safe diagnostics, not automatic repair claims.

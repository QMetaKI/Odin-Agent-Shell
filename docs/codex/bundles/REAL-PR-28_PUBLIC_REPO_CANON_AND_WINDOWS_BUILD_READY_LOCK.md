# REAL-PR-28 — Public Repo Canon and Windows Build Ready Lock

## Objective

Consolidate public repository canon clarity and Windows build readiness after the v0.7.4 product/pattern/atom/hub lock. This bundle prepares the repository for implementation work by cleaning the current entry path, defining Windows host drilldown, separating MVP/V1/Power modes, and hardening Seed/Pattern Pack security certification.

## Internal Tasks Covered

- PR-116 — Public Repo Canon Cleanup Lock
- PR-117 — Windows Implementation Drilldown
- PR-118 — Windows IPC Endpoint Contracts
- PR-119 — Windows Installer Update Rollback Drilldown
- PR-120 — MVP V1 Power Mode Boundary
- PR-121 — Seed Pattern Pack Security Certification
- PR-122 — Codex Public Build Ready Gate
- PR-123 — Public Repo Windows Build Ready Consolidation

## Primary Files

- `docs/PUBLIC_REPO_CANON_AND_WINDOWS_BUILD_READY_LOCK_V7_1.md`
- `docs/PUBLIC_REPO_ROOT_CLEANUP_POLICY_V7_1.md`
- `docs/WINDOWS_IMPLEMENTATION_DRILLDOWN_V7_1.md`
- `docs/WINDOWS_IPC_ENDPOINT_CONTRACTS_V7_1.md`
- `docs/WINDOWS_INSTALLER_UPDATE_ROLLBACK_DRILLDOWN_V7_1.md`
- `docs/MVP_V1_POWER_MODE_BOUNDARY_V7_1.md`
- `docs/SEED_PATTERN_PACK_SECURITY_CERTIFICATION_V7_1.md`
- `docs/CODEX_PUBLIC_BUILD_READY_GATE_V7_1.md`

## Required Behavior

The bundle must preserve the full v7.1 architecture and make the public repo entrypoint clearer. It must not claim a runtime is complete. It must define build readiness as implementation preparedness, not host validation. It must keep app apply outside Odin.

## Forbidden Scope

- No runtime proof.
- No host validation claim.
- No model inference proof claim.
- No production-readiness implication.
- No executable seed pack behavior.
- No app apply or external send.
- No remote-default policy.
- No public QIRC/network expansion.

## Definition of Done

- All covered task docs exist.
- Schemas and registries validate.
- Shadow modules exist.
- Tests cover the new lock.
- FILE_MANIFEST is refreshed.
- SYSTEM_MAP references are valid.
- `python -m odin.cli validate-all` succeeds.
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider` succeeds.

## Codex PR Summary Template

```text
Scope: REAL-PR-28 — Public Repo Canon and Windows Build Ready Lock
Internal tasks:
Changed files:
Validation:
Boundary preservation:
Remaining gaps:
```

## Bundle Review Strategy

This bundle should be reviewed as the final preparation layer before implementation begins. It does not replace the earlier architecture locks; it makes the repository easier to consume as a public GitHub project and gives Codex a stricter Windows build path. Reviewers should check that new public-facing docs are shorter and clearer where needed, while full depth remains in subsystem documentation.

## Implementation Sequencing

1. Clean root current-canon entrypoints.
2. Add Windows process and IPC drilldowns.
3. Add installer, update, rollback and safe-mode drilldowns.
4. Add MVP/V1/Power Mode boundary.
5. Add Seed/Pattern Pack certification.
6. Add build-ready gates and validation tests.
7. Refresh registries, SYSTEM_MAP and FILE_MANIFEST.

## Cross-Bundle Boundary

REAL-PR-28 depends on all earlier product, pattern, atom and hub locks. It does not supersede REAL-PR-24 through REAL-PR-27; it concentrates them into a public-repo and Windows-build entry posture. Codex must not start provider work, UI richness, or Power Mode diagnostics before the public build-ready gates are stable.

## Acceptance Summary

The repository is ready for implementation when a new contributor can open README, follow START_HERE, verify CANON_ENTRY, run validation, understand the Windows host target, identify MVP/V1/Power boundaries, and choose the next real PR bundle without needing hidden chat context.

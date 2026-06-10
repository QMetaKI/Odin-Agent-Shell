# Codex Start Here — Odin Agent Shell v7.1

This file orients Codex work to the current public repo canon.

## Current handoff lock

```text
Current handoff: v0.8.7 CODEX_REAL_PR_HANDOFF_LADDER_LOCK
Runtime base: v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK
Actual Codex/GitHub PR ladder: REAL-GH-PR-01..08
Internal traceability ladders: PR-00..PR-123 and REAL-PR-01..28 only
```

The current work starts from the v0.8.6 direct runtime release candidate source lock and proceeds through `REAL-GH-PR-01..08`. The internal PR ladder and legacy real-bundle ladder are traceability sources only.

## Required read order for real PR work

1. `START_HERE.md`
2. `CANON_ENTRY.md`
3. `SYSTEM_MAP.json`
4. `docs/CODEX_REAL_PR_HANDOFF_LADDER_LOCK_V0_8_7.md`
5. `docs/codex/CODEX_FINAL_HANDOFF_V0_8_7.md`
6. `docs/codex/REAL_GITHUB_PR_EXECUTION_PLAN_V0_8_7.md`
7. `docs/codex/REAL_GITHUB_PR_EXECUTION_INDEX_V0_8_7.md`
8. `registries/real_pr_execution_registry.json`
9. `registries/codex_real_pr_handoff_registry.json`
10. Exact `docs/codex/prompts/REAL-GH-PR-##_CODEX_PROMPT.md`.
11. Relevant subsystem docs, schemas, registries, examples, and tests.

## Scope rules

- Implement only the active `REAL-GH-PR-##` scope.
- Do not merge runtime bus, provider, Windows, Hub, app SDK, or QIRC implementation into foundation work unless the active prompt explicitly requires the bounded change.
- Do not convert traceability ladders into competing public execution ladders.
- Preserve candidate-only Universal Work and Candidate Artifact boundaries.
- Preserve caller/app-owned apply, storage, external sends, and domain authority.
- Providers are bounded workers, not authority.
- Preserve GPL-2.0-only and no-hidden-authority posture.

## Proof rules

Evidence must be generated in the current workspace. Use prior handoff/source-chat context only as context, not as proof.

Do not claim:

- production readiness proof
- runtime proof without host receipts
- live model inference proof
- model quality proof
- Windows service/tray/installer proof without actual Windows receipts
- security certification proof
- external send proof
- app-state mutation proof

## Required validation commands

```bash
python -m odin.cli validate-all
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
python -m odin.cli validate-direct-runtime-release-candidate
```

If a required command fails, the PR is blocked/incomplete until the failure is fixed or explicitly reported as an existing baseline blocker.

## Historical context

Docs and registries may retain v0.3.x through v0.7.x material as historical prep milestones, earlier architecture locks, legacy traceability layers, or previous source-chat build states. Those versions are not current public canon.

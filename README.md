# Odin Agent Shell

**Odin Agent Shell** is a Windows-first, local-first, protocol-bound Universal Work kernel and small-model performance OS for candidate-only AI work.

Apps contain only an **Odin Capability Bridge**. Apps send **Universal Work Objects**. Odin validates, precomputes, routes, and returns **Candidate Artifacts** wrapped in Response Packets. Apps render, decide, apply, persist, and send externally under their own authority.

## Current public canon

This root surface has one current public repo canon:

```text
Current handoff: v0.8.7 CODEX_REAL_PR_HANDOFF_LADDER_LOCK
Runtime base: v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK
Actual Codex/GitHub PR ladder: REAL-GH-PR-01..08
Internal traceability ladders: PR-00..PR-123 and REAL-PR-01..28 only
```

The v0.8.7 handoff starts from the v0.8.6 direct runtime release candidate source lock. It is a Codex/GitHub execution plan and hardening ladder, not a claim of production readiness, host validation, Windows service/tray/installer validation, live model inference, model quality, security certification, external sends, or app-state mutation proof.

## Canonical entrypoints

Read in this order:

1. `START_HERE.md`
2. `CANON_ENTRY.md`
3. `AGENTS.md`
4. `CODEX_START_HERE.md`
5. `SYSTEM_MAP.json`
6. `docs/CODEX_REAL_PR_HANDOFF_LADDER_LOCK_V0_8_7.md`
7. `docs/codex/CODEX_FINAL_HANDOFF_V0_8_7.md`
8. `docs/codex/REAL_GITHUB_PR_EXECUTION_PLAN_V0_8_7.md`
9. `docs/codex/REAL_GITHUB_PR_EXECUTION_INDEX_V0_8_7.md`
10. `docs/MASTER_ARCHITECTURE_V7_1.md`
11. `docs/MASTER_SPECS_V7_1.md`

## Core formula

```text
Anything in,
bounded Universal Work,
local semantic coordination,
smallest sufficient worker,
Candidate Artifact out,
caller/app-owned apply.
```

## Boundary invariants

- Odin does candidate work; callers/apps do reality work.
- Universal Work and Candidate Artifacts are candidate-only contracts.
- Apps own state, app apply, storage, domain truth, and external sends.
- Odin must not silently apply patches, mutate app state, or send externally.
- Providers are bounded workers, not authority.
- QIRC / Internal Semantic Bus is trace, receipt, and coordination infrastructure, not app-state authority.
- Model output is projection, not truth.
- Windows service/tray/installer proof requires actual Windows receipts.
- GPL-2.0-only and no-hidden-authority posture remain in force.

## Actual Codex/GitHub ladder

`REAL-GH-PR-01..08` is the actual Codex/GitHub execution sequence for the v0.8.7 handoff.

`PR-00..PR-123` is the internal micro-task traceability ladder. `REAL-PR-01..28` is the internal legacy bundle traceability ladder. They are retained for mapping and auditability only; they are not competing current public execution ladders.

## Validate repository

```bash
python -m odin.cli validate-all
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
python -m odin.cli validate-direct-runtime-release-candidate
```

Only command output produced in the current workspace is evidence for a test or validation claim.

## Historical lock trail

Earlier architecture/prep locks are preserved as historical/changelog context. They are not the current public repo canon:

- v0.3.x — historical deep subsystem spec prep.
- v0.4.x — historical Codex task and real-bundle overlay prep.
- v0.5.x — historical Shadow Runtime coverage prep.
- v0.6.x — historical narrative, seed, model/agent, handoff, and GPL lock expansions.
- v0.7.x — historical public repo, Windows build-ready, and alignment prep.
- v0.8.0 — historical direct runtime source candidate milestone.
- v0.8.6 — current runtime base for the v0.8.7 handoff.
- v0.8.7 — current public handoff canon and actual Codex/GitHub ladder lock.

## What is not claimed

This repository does not claim production readiness, security certification, deployment verification, live provider inference proof, model quality proof, external send proof, app-state mutation proof, or Windows service/tray/installer host validation unless exact local receipts are added for that claim.

## Local Runtime Hub rebaseline

The next practical product target is documented as **Odin Local Runtime Hub** in `docs/rebaseline/LOCAL_RUNTIME_HUB_TARGET_V1.md`. The current-state audit, coverage matrix, legacy quarantine policy, 100 percent definition, and LRH-PR-01..16 build ladder live under `docs/rebaseline/` and the matching machine-readable registries live in `registries/`.


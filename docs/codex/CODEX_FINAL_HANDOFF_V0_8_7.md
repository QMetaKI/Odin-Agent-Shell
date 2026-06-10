# Codex Final Handoff v0.8.7

## Start here

Base: `v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK`.

Codex should treat this repository as a running runtime candidate, not as a pure prep repository.

Primary files:

```text
CODEX_START_HERE.md
registries/real_pr_execution_registry.json
registries/codex_real_pr_handoff_registry.json
docs/codex/REAL_GITHUB_PR_EXECUTION_PLAN_V0_8_7.md
docs/codex/REAL_GITHUB_PR_EXECUTION_INDEX_V0_8_7.md
```

## Base claim

The current repo contains a local runtime candidate with tests, fixtures, CLI commands, Local API smoke path, provider stubs, SDK examples, Hub skeleton, and Windows handoff scripts.

## Codex task

Codex must execute the eight REAL-GH-PRs as completion/hardening PRs.

## Return report required per PR

```text
PR:
Branch:
Implemented:
Changed files:
Commands run:
Results:
Skipped:
Blocked:
Proof boundaries:
Next recommended PR:
```

## CODEX-PR-01..05 hardening overlay

The current handoff remains `v0.8.7 CODEX_REAL_PR_HANDOFF_LADDER_LOCK`, starting from `v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK`. For current Codex execution, use this five-PR hardening path:

1. `CODEX-PR-01` — Canon, Validation and Runtime Skeleton Hardening.
2. `CODEX-PR-02` — Runtime Bus, Worklets, Work Atoms, Local API and App SDK.
3. `CODEX-PR-03` — Provider Boundary, Pre-LLM, QIRC, Seeds, Pattern Mines and Flow Packs.
4. `CODEX-PR-04` — Handoff, AI-Git, Narrative Compiler, Shadow Runtime and Loki.
5. `CODEX-PR-05` — Windows Product Runtime, Odin Hub, Golden RC and Release Handoff.

Historical traceability is retained: `PR-00..PR-123`, `REAL-PR-01..28`, and `REAL-GH-PR-01..08` remain mapping ladders. This overlay does not delete or rewrite those ladders, and it does not claim production readiness, live model inference proof, model quality proof, Windows service/tray/installer proof, security certification proof, external send proof, or app-state mutation proof. Manual review remains required. Odin emits candidates only and app-owned apply remains mandatory.


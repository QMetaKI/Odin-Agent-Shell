# Start Here

This repository is the canonical starting point for building **Odin Agent Shell v7.1** from the current v0.8.7 Codex handoff lock.

## Current public canon

```text
Current handoff: v0.8.7 CODEX_REAL_PR_HANDOFF_LADDER_LOCK
Runtime base: v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK
Actual Codex/GitHub PR ladder: REAL-GH-PR-01..08
Internal traceability ladders: PR-00..PR-123 and REAL-PR-01..28 only
```

Older v0.3.x through v0.7.x lock language is historical/changelog context only when encountered in deeper documents. It is not a competing current state statement.

## Read order

1. `CANON_ENTRY.md` — short canonical scope, current handoff, and laws.
2. `AGENTS.md` — instructions for Codex/agents/human implementers.
3. `CODEX_START_HERE.md` — v0.8.7 implementation sequence and boundaries.
4. `SYSTEM_MAP.json` — machine-readable repository map.
5. `docs/CODEX_REAL_PR_HANDOFF_LADDER_LOCK_V0_8_7.md`.
6. `docs/codex/CODEX_FINAL_HANDOFF_V0_8_7.md`.
7. `docs/codex/REAL_GITHUB_PR_EXECUTION_PLAN_V0_8_7.md`.
8. `docs/codex/REAL_GITHUB_PR_EXECUTION_INDEX_V0_8_7.md`.
9. `docs/MASTER_ARCHITECTURE_V7_1.md` — full architecture canon.
10. `docs/MASTER_SPECS_V7_1.md` — full build specification.
11. The exact `docs/codex/prompts/REAL-GH-PR-##_CODEX_PROMPT.md` for the active real PR.

## Non-negotiables

- Apps contain no LLM runtime.
- Every AI-like task enters as Universal Work.
- Odin returns Candidate Artifacts only and preserves candidate-only boundaries.
- Apps own state, apply, external sends, storage, business logic, and domain authority.
- Internal Semantic Bus / QIRC remains local-first trace and coordination infrastructure, not app-state authority.
- Providers are bounded workers, not truth or authority.
- Caller/app-owned apply remains outside Odin.
- Bigger model is a route, not the architecture.
- 3B + 7B/8B hybrid remains the default sweet spot.
- GPL-2.0-only and no-hidden-authority posture remain in force.

## Required local validation

```bash
python -m odin.cli validate-all
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
python -m odin.cli validate-direct-runtime-release-candidate
```

Do not cite prior source-chat command output as current proof. Rerun commands in this workspace.

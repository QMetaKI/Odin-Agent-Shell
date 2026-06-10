# Real GitHub PR Execution Index v0.8.7


Base: `v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK`.
This index points Codex to the exact prompt for each actual PR.

- `REAL-GH-PR-01` → `docs/codex/prompts/REAL-GH-PR-01_CODEX_PROMPT.md` — Foundation, Canon, Protocol and Universal Work Core — Codex Hardening
- `REAL-GH-PR-02` → `docs/codex/prompts/REAL-GH-PR-02_CODEX_PROMPT.md` — Runtime Bus, Persistence, Local API, Worklets and Work Atoms — Completion
- `REAL-GH-PR-03` → `docs/codex/prompts/REAL-GH-PR-03_CODEX_PROMPT.md` — Model Provider Runtime, Pre-LLM Intelligence and Universal Worker Boundary — Provider-Ready
- `REAL-GH-PR-04` → `docs/codex/prompts/REAL-GH-PR-04_CODEX_PROMPT.md` — Thor/Y/Mjölnir Handoff, AI-Git Safety and Review Pipeline — Real Modules
- `REAL-GH-PR-05` → `docs/codex/prompts/REAL-GH-PR-05_CODEX_PROMPT.md` — Narrative Compiler, Shadow Runtime, Runtime Packs and Loki Anti-Pattern Layer — Executable Contracts
- `REAL-GH-PR-06` → `docs/codex/prompts/REAL-GH-PR-06_CODEX_PROMPT.md` — Odin Core, QIRC Gold Spine, Seeds, Pattern Mines and Flow Packs — Runtime Hardening
- `REAL-GH-PR-07` → `docs/codex/prompts/REAL-GH-PR-07_CODEX_PROMPT.md` — Windows Product Runtime, Odin Hub, Installer, IPC and Recovery — Host-Real Track
- `REAL-GH-PR-08` → `docs/codex/prompts/REAL-GH-PR-08_CODEX_PROMPT.md` — App SDKs, Golden Apps, Release Gates and Public Build Handoff — Final Codex RC

## Required base commands before each PR

```bash
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider
python -m odin.cli run-golden-flow
```

If any command fails before changes, Codex must report the baseline failure before editing.

## CODEX-PR-01..05 hardening overlay

The current handoff remains `v0.8.7 CODEX_REAL_PR_HANDOFF_LADDER_LOCK`, starting from `v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK`. For current Codex execution, use this five-PR hardening path:

1. `CODEX-PR-01` — Canon, Validation and Runtime Skeleton Hardening.
2. `CODEX-PR-02` — Runtime Bus, Worklets, Work Atoms, Local API and App SDK.
3. `CODEX-PR-03` — Provider Boundary, Pre-LLM, QIRC, Seeds, Pattern Mines and Flow Packs.
4. `CODEX-PR-04` — Handoff, AI-Git, Narrative Compiler, Shadow Runtime and Loki.
5. `CODEX-PR-05` — Windows Product Runtime, Odin Hub, Golden RC and Release Handoff.

Historical traceability is retained: `PR-00..PR-123`, `REAL-PR-01..28`, and `REAL-GH-PR-01..08` remain mapping ladders. This overlay does not delete or rewrite those ladders, and it does not claim production readiness, live model inference proof, model quality proof, Windows service/tray/installer proof, security certification proof, external send proof, or app-state mutation proof. Manual review remains required. Odin emits candidates only and app-owned apply remains mandatory.


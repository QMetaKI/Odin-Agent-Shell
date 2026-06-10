# Start Here

This repository is the canonical starting point for building **Odin Agent Shell v7.1**.

## Read order

1. `CANON_ENTRY.md` — short canonical scope and laws.
2. `AGENTS.md` — instructions for Codex/agents/human implementers.
3. `CODEX_START_HERE.md` — implementation sequence and boundaries.
4. `SYSTEM_MAP.json` — machine-readable repository map.
5. `docs/MASTER_ARCHITECTURE_V7_1.md` — full architecture canon.
6. `docs/MASTER_SPECS_V7_1.md` — full build specification.
7. `docs/codex/PHASE_0_CANON_LOCK.md` — first Codex task package.

## Non-negotiables

- Apps contain no LLM runtime.
- Odin returns Candidate Artifacts only.
- Apps own state, apply, and external sends.
- Internal Semantic Bus is local-only and coordination-only.
- Bigger model is a route, not the architecture.
- 3B + 7B/8B hybrid is the default sweet spot.


## v0.5.1 FULL_SHADOW_RUNTIME_COVERAGE

This repo prep now includes full major-subsystem Shadow Runtime coverage. Future changes must update specs, internal PR ladder, REAL-PR bundles, registries, tests, System Map and FILE_MANIFEST.

## v0.6.0 Narrative Aorta / Y* Compiler Integration

This repo now integrates the Fairy/Y* Narrative Aorta and Shadow Runtime Compiler Prelude into the v7.1 canon. v7.1 runtime invariants remain unchanged. New work must update the internal PR ladder, real PR bundles, registries, System Map, tests and FILE_MANIFEST.

New internal tasks: PR-26 through PR-37. New real bundles: REAL-PR-12 and REAL-PR-13.


---

# v0.7.5 Public Repo Canon and Windows Build Ready Lock

This section binds the v7.1 master architecture to the public repository and Windows implementation readiness posture.

## Current-lock additions

- Public Repo Canon and Windows Build Ready Lock.
- Public Repo Root Cleanup Policy.
- Windows Implementation Drilldown.
- Windows IPC Endpoint Contracts.
- Windows Installer Update Rollback Drilldown.
- MVP / V1 / Power Mode Boundary.
- Seed and Pattern Pack Security Certification.
- Codex Public Build Ready Gate.

## Canonical effect

The architecture remains candidate-only, app-owned apply, GPL-2.0-only and Universal LLM Work oriented. v0.7.5 does not add a new authority layer. It clarifies how the existing architecture becomes a public GitHub repository and a Windows-first implementation target.

## Windows build-ready effect

Windows build readiness means Odin has process, IPC, installer, rollback, safe-mode, support-bundle, app-pairing and runtime-pack lifecycle specs sufficient for Codex implementation. It does not claim host validation.

## Mode separation

MVP, V1 and Power Mode are distinct. MVP proves the minimal spine. V1 adds local model usefulness. Power Mode adds deep pattern and diagnostic systems. Every mode preserves candidate-only and app-owned apply.

## v0.7.7 — Build Ladder Absolute Alignment Lock

Current actual GitHub execution sequence: `REAL-GH-PR-01` through `REAL-GH-PR-08`.

The old `PR-00..PR-123` task ladder and `REAL-PR-01..REAL-PR-28` legacy bundle ladder are internal traceability layers only.

Current alignment docs:

- `docs/BUILD_LADDER_ABSOLUTE_ALIGNMENT_LOCK_V7_1.md`
- `docs/codex/REAL_GITHUB_PR_EXECUTION_PLAN_V0_7_7.md`
- `docs/codex/REAL_GITHUB_PR_EXECUTION_INDEX_V0_7_7.md`

The execution registry now separates existing prep paths from target implementation paths and binds every real PR to acceptance gates, proof boundaries and Master Architecture sections.



## v0.8.0 Direct Master Architecture Runtime Source Candidate

The current source candidate materializes the v7.1 master architecture beyond prep documentation. It adds executable local source paths for Universal Work, caller manifests, QIRC local ledger, seed packs, pattern mines, flow packs, work atoms, model-worker boundary, candidates, Why Trace, local API, Odin Hub, diagnostics and safe-mode planning.

Canonical command spine:

```text
python -m odin.cli validate-all
python -m odin.cli doctor
python -m odin.cli run-work examples/runtime/universal_work_full.valid.json --seed-pack examples/runtime/app_seed_pack_full.valid.json --pattern-mine examples/runtime/pattern_mine_full.valid.json --caller-manifest examples/runtime/app_caller_manifest.valid.json
python -m odin.cli compile-seed-pack examples/runtime/app_seed_pack_full.valid.json
python -m odin.cli compile-pattern-mine examples/runtime/pattern_mine_full.valid.json
python -m odin.cli build-hub --out .odin_runtime/hub/index.html
python -m odin.cli emit-support-bundle --out .odin_runtime/support
```

Claim boundary: this remains a local runtime source candidate. It does not assert Windows host behavior, live model inference, signed installer behavior, external network operation, or app-side application.


## v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK

Odin now includes a direct runtime release candidate body: runtime store/session/config, App SDK, golden app examples, local API endpoints, static Odin Hub, provider boundary stubs, Windows handoff scripts, support bundle, safe mode plan and release-candidate acceptance commands. This remains candidate-only: no app apply, no host proof, no service/tray/installer proof and no live model inference proof are claimed.
## v0.8.7 Codex Real PR Handoff Ladder Lock

Current Codex execution starts from `v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK` and uses the reoptimized eight-PR ladder:

```text
REAL-GH-PR-01..08 = actual Codex/GitHub completion sequence
PR-00..PR-123 = internal micro-task traceability
REAL-PR-01..28 = internal legacy bundle traceability
```

Primary handoff files:

```text
registries/real_pr_execution_registry.json
registries/codex_real_pr_handoff_registry.json
docs/codex/REAL_GITHUB_PR_EXECUTION_PLAN_V0_8_7.md
docs/codex/REAL_GITHUB_PR_EXECUTION_INDEX_V0_8_7.md
docs/codex/CODEX_FINAL_HANDOFF_V0_8_7.md
```

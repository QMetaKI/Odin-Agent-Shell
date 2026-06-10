# Codex Prompt — REAL-GH-PR-01 — Foundation, Canon, Protocol and Universal Work Core — Codex Hardening

## Base state

You are working in `Odin-Agent-Shell` after:

```text
v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK
```

This is a running runtime candidate. Do not restart from architecture-only assumptions.

## Objective

Create the public repo foundation, strict JSON/registry hygiene, binding gate, Universal Work core, candidate artifact core, and current-canon root surface before feature implementation expands. Post-v0.8.6 focus: complete and harden the direct runtime candidate already materialized by ChatGPT.

## Already materialized by ChatGPT

- root public canon documents
- Master Architecture / Specs v7.1
- Universal Work examples and validation path
- build-ladder alignment registry
- CLI validate-all entrypoint

## Codex completion focus

- normalize public repo entrypoints so v0.8.7 is the only current handoff
- turn Universal Work contracts into stricter typed interfaces where useful
- remove ambiguity between prep docs and runtime candidate docs
- harden schema/registry loading without weakening backwards compatibility
- keep GPL-2.0-only and claim-boundary language intact

## Expected deliverables

- current-canon root docs
- strict Universal Work contract checks
- source tree hygiene pass
- public README/START_HERE/CODEX_START_HERE synchronization
- foundation regression tests

## Existing files to preserve and inspect first

- `README.md`
- `START_HERE.md`
- `CANON_ENTRY.md`
- `CODEX_START_HERE.md`
- `SYSTEM_MAP.json`
- `FILE_MANIFEST.json`
- `odin/cli.py`
- `odin/protocol/`
- `schemas/v7_1/`
- `registries/`
- `tests/`

## Target/new paths allowed for this PR

- No mandatory new target path; update existing paths only unless required by implementation.

## Forbidden scope

- no live model provider execution
- no Windows tray/control-center implementation
- no app state mutation
- no remote/network enablement
- no runtime-proof claim

## Required behavior

- root docs point to one current canon
- validate-all blocks schema/registry drift
- Universal Work and Candidate Artifact contracts are app-renderable and candidate-only
- Binding gate preserves app authority and Odin non-apply posture

## Acceptance gates

- All modified registries and schemas remain JSON-valid
- Codex return report separates implemented, prepared, skipped and blocked work
- No host/model/provider proof is claimed without a receipt produced in that environment
- PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
- all proof gaps and non-claims are stated in the PR summary
- all public-entry docs point to this consolidated real PR execution plan
- every created or updated artifact is registered in FILE_MANIFEST.json
- pytest suite is green
- python -m odin.cli validate-all
- root docs contain no competing current-canon path
- validate-all is green

## Required commands

- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`
- `python -m odin.cli validate-all`
- `python -m pytest -q -p no:cacheprovider`

## Must preserve

- no_llm_in_app
- candidate_only
- local_first
- app_owns_state
- semantic_bus_local_only
- app_owns_apply
- gpl_2_0_only
- no_runtime_proof

## Proof boundaries

- ChatGPT-built runtime candidate is not a substitute for host-real Codex proof
- Codex must keep app-owned apply boundary intact
- Codex must preserve GPL-2.0-only policy and no-hidden-authority posture
- no_app_apply_authority_for_odin
- no_app_state_mutation
- no_external_send_by_odin
- no_live_model_provider_execution
- no_model_inference_proof_without_actual_model_receipts
- no_network_qirc_by_default
- no_production_readiness_claim
- no_remote/network_enablement
- no_runtime-proof_claim
- no_runtime_proof_without_host_receipts
- no_windows_tray/control-center_implementation

## Senior reviewer focus

- single current canon
- no competing build ladder
- no overclaim
- no scope creep into Windows/Provider implementation

## Return format

```text
PR: REAL-GH-PR-01
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

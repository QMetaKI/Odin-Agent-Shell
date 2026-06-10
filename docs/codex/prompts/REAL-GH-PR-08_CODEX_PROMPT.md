# Codex Prompt — REAL-GH-PR-08 — App SDKs, Golden Apps, Release Gates and Public Build Handoff — Final Codex RC

## Base state

You are working in `Odin-Agent-Shell` after:

```text
v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK
```

This is a running runtime candidate. Do not restart from architecture-only assumptions.

## Objective

Finalize app-facing SDK/templates, App QIRC digest bridge, golden flows, support bundle/release hygiene, senior-review hardening and public build-ready gate so the repo can be handed to Codex as a coherent build program. Post-v0.8.6 focus: complete and harden the direct runtime candidate already materialized by ChatGPT.

## Already materialized by ChatGPT

- odin_app_sdk
- minimal notes app
- wedding studio mock
- codex handoff mock
- game quest mock
- run-golden-flow
- direct runtime RC validator

## Codex completion focus

- turn example apps into robust integration fixtures
- harden SDK client error handling and API compatibility
- add public release checklist and Codex return report format
- ensure all previous PR gates are represented in final RC validation
- prepare final repo hygiene pass

## Expected deliverables

- SDK integration tests
- golden app snapshots
- release-candidate acceptance report
- Codex final return template
- public repo hygiene verification

## Existing files to preserve and inspect first

- `sdk/`
- `templates/`
- `examples/`
- `docs/codex/`
- `docs/PUBLIC_REPO_RELEASE_CHECKLIST_V7_1.md`
- `docs/CODEX_PUBLIC_BUILD_READY_GATE_V7_1.md`
- `registries/public_build_readiness_registry.json`
- `tests/`

## Target/new paths allowed for this PR

- No mandatory new target path; update existing paths only unless required by implementation.

## Forbidden scope

- no app-owned state stored inside Odin
- no direct external send from Odin
- no production-ready wording
- no hidden model credentials
- no collapsing internal ladders into unexplained mega-PR

## Required behavior

- apps integrate through SDK/template bridges without LLM logic
- App QIRC bridge is digest-only by default
- golden flows exercise full candidate path
- public build gate blocks overclaims and missing docs/fixtures

## Acceptance gates

- All modified registries and schemas remain JSON-valid
- Codex return report separates implemented, prepared, skipped and blocked work
- No host/model/provider proof is claimed without a receipt produced in that environment
- PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
- all internal tasks are covered by consolidated real execution PRs
- all proof gaps and non-claims are stated in the PR summary
- every created or updated artifact is registered in FILE_MANIFEST.json
- golden flow fixtures validate
- python -m odin.cli validate-all
- release checklist is current-canon only
- senior-review anti-drift gates remain active

## Required commands

- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`
- `python -m odin.cli run-golden-flow`
- `python -m odin.cli validate-all`
- `python -m odin.cli validate-direct-runtime-release-candidate`
- `python -m pytest -q -p no:cacheprovider`

## Must preserve

- no_llm_in_app
- candidate_only
- local_first
- app_owns_state
- semantic_bus_local_only
- default_model_strategy_3b_7b_8b
- app_owns_apply
- gpl_2_0_only
- no_runtime_proof

## Proof boundaries

- ChatGPT-built runtime candidate is not a substitute for host-real Codex proof
- Codex must keep app-owned apply boundary intact
- Codex must preserve GPL-2.0-only policy and no-hidden-authority posture
- no_app-owned_state_stored_inside_odin
- no_app_apply_authority_for_odin
- no_collapsing_internal_ladders_into_unexplained_mega-pr
- no_direct_external_send_from_odin
- no_external_send_by_odin
- no_hidden_model_credentials
- no_model_inference_proof_without_actual_model_receipts
- no_network_qirc_by_default
- no_production-ready_wording
- no_production_readiness_claim
- no_runtime_proof_without_host_receipts

## Senior reviewer focus

- apps keep apply authority
- Golden Apps are examples not production apps
- final RC report distinguishes proven vs prepared

## Return format

```text
PR: REAL-GH-PR-08
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

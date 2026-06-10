# Real GitHub PR Execution Plan v0.8.7

## Base

```text
Odin-Agent-Shell v0.8.6 Direct Runtime Release Candidate
```

## Execution plan

The following eight PRs are the only actual Codex/GitHub PRs for the next build sequence.

## REAL-GH-PR-01 — Foundation, Canon, Protocol and Universal Work Core — Codex Hardening

**Depends on:** none

**Already materialized by ChatGPT:**
- root public canon documents
- Master Architecture / Specs v7.1
- Universal Work examples and validation path
- build-ladder alignment registry
- CLI validate-all entrypoint

**Codex completion focus:**
- normalize public repo entrypoints so v0.8.7 is the only current handoff
- turn Universal Work contracts into stricter typed interfaces where useful
- remove ambiguity between prep docs and runtime candidate docs
- harden schema/registry loading without weakening backwards compatibility
- keep GPL-2.0-only and claim-boundary language intact

**Required commands:**
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`
- `python -m odin.cli validate-all`
- `python -m pytest -q -p no:cacheprovider`

**Proof boundaries:**
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

## REAL-GH-PR-02 — Runtime Bus, Persistence, Local API, Worklets and Work Atoms — Completion

**Depends on:** REAL-GH-PR-01

**Already materialized by ChatGPT:**
- RuntimeStore
- WorkSession state machine
- Work Atom Runtime
- Local API smoke endpoints
- candidate/session/qirc local file persistence
- run-golden-flow candidate path

**Codex completion focus:**
- split current runtime flow into clearer bus/worklet/store boundaries
- complete persistent store semantics and error taxonomy
- add actual worklet graph abstraction above work atoms
- harden Local API request/response validation
- improve deterministic fixture coverage for storage and atom planning

**Required commands:**
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`
- `python -m odin.cli run-golden-flow`
- `python -m odin.cli serve --host 127.0.0.1 --port 8877 --once-smoke || true`
- `python -m odin.cli validate-all`

**Proof boundaries:**
- ChatGPT-built runtime candidate is not a substitute for host-real Codex proof
- Codex must keep app-owned apply boundary intact
- Codex must preserve GPL-2.0-only policy and no-hidden-authority posture
- no_app_apply_authority_for_odin
- no_app_apply_endpoint
- no_external_send_by_odin
- no_hidden_background_worker_autonomy
- no_model_inference_proof_without_actual_model_receipts
- no_model_provider_implementation
- no_network_qirc_by_default
- no_production_readiness_claim
- no_runtime_proof_without_host_receipts
- no_unbounded_atom_recursion
- no_wan_or_lan_transport

## REAL-GH-PR-03 — Model Provider Runtime, Pre-LLM Intelligence and Universal Worker Boundary — Provider-Ready

**Depends on:** REAL-GH-PR-02

**Already materialized by ChatGPT:**
- provider base classes
- MockProvider
- Null/Echo-like stub cards
- provider registry/list-providers
- model route inside runtime engine
- candidate-only worker boundary docs

**Codex completion focus:**
- finish provider contract isolation
- add Ollama/llama.cpp/OpenAI-compatible/Claude-compatible adapters as disabled-by-default stubs or optional integrations
- harden provider config redaction
- strengthen pre-LLM routing and model-work-avoidance tests
- ensure every provider return is candidate-only and gate-checked

**Required commands:**
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`
- `python -m odin.cli list-providers`
- `python -m odin.cli run-golden-flow`
- `python -m odin.cli validate-all`

**Proof boundaries:**
- ChatGPT-built runtime candidate is not a substitute for host-real Codex proof
- Codex must keep app-owned apply boundary intact
- Codex must preserve GPL-2.0-only policy and no-hidden-authority posture
- no_app_apply_authority_for_odin
- no_app_state_ownership_by_odin
- no_external_send_by_odin
- no_model_inference_proof_without_actual_model_receipts
- no_model_output_accepted_as_truth
- no_network_qirc_by_default
- no_production_performance_claim
- no_production_readiness_claim
- no_remote_provider_credentials
- no_runtime_proof_without_host_receipts
- no_unreviewed_tool_use_by_agents

## REAL-GH-PR-04 — Thor/Y/Mjölnir Handoff, AI-Git Safety and Review Pipeline — Real Modules

**Depends on:** REAL-GH-PR-03

**Already materialized by ChatGPT:**
- handoff/compiler specs and registries
- candidate artifact/why trace code
- AI-Git safety architecture docs
- review boundary docs
- semantic diff concepts

**Codex completion focus:**
- materialize Thor handoff compiler modules
- materialize candidate branch/semantic diff/review gate modules
- connect handoff packets into Universal Work runtime path
- add negative tests for direct-apply handoffs and fake receipts
- keep Thor/Y/Mjölnir as candidate workers only

**Required commands:**
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`
- `python -m odin.cli validate-all`
- `python -m pytest -q -p no:cacheprovider`

**Proof boundaries:**
- ChatGPT-built runtime candidate is not a substitute for host-real Codex proof
- Codex must keep app-owned apply boundary intact
- Codex must preserve GPL-2.0-only policy and no-hidden-authority posture
- no_app_apply_authority_for_odin
- no_auto-apply
- no_auto-merge
- no_autonomous_pr_creation
- no_claim_acceptance_without_evidence_gate
- no_external_send_by_odin
- no_model_inference_proof_without_actual_model_receipts
- no_network_qirc_by_default
- no_production_readiness_claim
- no_receipt_issuance_by_model/agent
- no_runtime_proof_without_host_receipts

## REAL-GH-PR-05 — Narrative Compiler, Shadow Runtime, Runtime Packs and Loki Anti-Pattern Layer — Executable Contracts

**Depends on:** REAL-GH-PR-04

**Already materialized by ChatGPT:**
- Shadow Runtime modules
- Fairy/Y*/Loki docs and schemas
- Anti-Fairy/Shadow Narrative registries
- runtime pack docs and gates
- negative Loki authority fixture

**Codex completion focus:**
- make narrative/compiler modules produce typed intermediate artifacts consumed by runtime engine
- compile Shadow Narrative anti-patterns into gate hints
- connect runtime packs to work atom planning
- add bounded no-execution checks for generated runtime packs
- improve red-team fixture generation

**Required commands:**
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`
- `python -m odin.cli validate-all`
- `python -m pytest -q -p no:cacheprovider`

**Proof boundaries:**
- ChatGPT-built runtime candidate is not a substitute for host-real Codex proof
- Codex must keep app-owned apply boundary intact
- Codex must preserve GPL-2.0-only policy and no-hidden-authority posture
- no_app_apply_authority_for_odin
- no_external_send_by_odin
- no_generated_hot-path_executable_runtime
- no_loki_authority
- no_model_inference_proof_without_actual_model_receipts
- no_narrative_claim_treated_as_truth
- no_network_qirc_by_default
- no_production_readiness_claim
- no_prose-only_execution
- no_runtime_proof_without_host_receipts
- no_unvalidated_runtime_pack_load

## REAL-GH-PR-06 — Odin Core, QIRC Gold Spine, Seeds, Pattern Mines and Flow Packs — Runtime Hardening

**Depends on:** REAL-GH-PR-05

**Already materialized by ChatGPT:**
- odin/core package
- QIRC local ledger
- seed pack compiler/security
- pattern mine intake/spine
- flow pack compiler
- run-work end-to-end golden flow

**Codex completion focus:**
- harden QIRC envelope and replay semantics
- add signature/review/certification states for seed and pattern packs
- stress-test pattern mine ingestion without importing truth authority
- improve flow-pack to work-atom planning
- add conflict resolution and activation budget tests

**Required commands:**
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`
- `python -m odin.cli compile-pattern-mine examples/runtime/pattern_mine_full.valid.json`
- `python -m odin.cli compile-seed-pack examples/runtime/app_seed_pack_full.valid.json`
- `python -m odin.cli run-golden-flow`
- `python -m odin.cli validate-all`

**Proof boundaries:**
- ChatGPT-built runtime candidate is not a substitute for host-real Codex proof
- Codex must keep app-owned apply boundary intact
- Codex must preserve GPL-2.0-only policy and no-hidden-authority posture
- no_app_apply_authority_for_odin
- no_bypass_of_odin_final_gate
- no_executable_seed_pack_code
- no_external_send_by_odin
- no_model_inference_proof_without_actual_model_receipts
- no_network_qirc_by_default
- no_production_readiness_claim
- no_qirc_network_expansion
- no_religious/domain_truth_leakage_from_pattern_mines
- no_runtime_proof_without_host_receipts
- no_unbounded_seed_fanout

## REAL-GH-PR-07 — Windows Product Runtime, Odin Hub, Installer, IPC and Recovery — Host-Real Track

**Depends on:** REAL-GH-PR-06

**Already materialized by ChatGPT:**
- static Odin Hub builder
- Local API smoke path
- diagnostics/support bundle
- safe mode module
- PowerShell scripts
- service/tray stubs and Windows host docs

**Codex completion focus:**
- make Windows scripts robust on real Windows
- implement or scaffold real service/tray project path without overclaiming host proof
- harden localhost auth and optional named-pipe plan
- add update/rollback/safe-mode receipts
- document exact host-proof commands

**Required commands:**
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`
- `python -m odin.cli build-hub`
- `python -m odin.cli emit-support-bundle`
- `python -m odin.cli serve --host 127.0.0.1 --port 8877 --once-smoke || true`
- `python -m odin.cli validate-all`

**Proof boundaries:**
- ChatGPT-built runtime candidate is not a substitute for host-real Codex proof
- Codex must keep app-owned apply boundary intact
- Codex must preserve GPL-2.0-only policy and no-hidden-authority posture
- no_app_apply_authority_for_odin
- no_daemon_ownership_of_app_state
- no_external_send_by_odin
- no_installer_production_claim_without_host_proof
- no_model_inference_proof_without_actual_model_receipts
- no_network_qirc_by_default
- no_privileged_global_mutation_by_tray/ui
- no_production_readiness_claim
- no_runtime_proof_without_host_receipts
- no_support_bundle_secret_leak
- no_wan_ipc

## REAL-GH-PR-08 — App SDKs, Golden Apps, Release Gates and Public Build Handoff — Final Codex RC

**Depends on:** REAL-GH-PR-07

**Already materialized by ChatGPT:**
- odin_app_sdk
- minimal notes app
- wedding studio mock
- codex handoff mock
- game quest mock
- run-golden-flow
- direct runtime RC validator

**Codex completion focus:**
- turn example apps into robust integration fixtures
- harden SDK client error handling and API compatibility
- add public release checklist and Codex return report format
- ensure all previous PR gates are represented in final RC validation
- prepare final repo hygiene pass

**Required commands:**
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`
- `python -m odin.cli run-golden-flow`
- `python -m odin.cli validate-all`
- `python -m odin.cli validate-direct-runtime-release-candidate`
- `python -m pytest -q -p no:cacheprovider`

**Proof boundaries:**
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


## Final rule

Every Codex PR must include a return report with implemented, changed, skipped, blocked, tests-run, and proof-boundary sections.

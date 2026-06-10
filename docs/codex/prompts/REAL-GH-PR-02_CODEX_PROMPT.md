# Codex Prompt — REAL-GH-PR-02 — Runtime Bus, Persistence, Local API, Worklets and Work Atoms — Completion

## Base state

You are working in `Odin-Agent-Shell` after:

```text
v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK
```

This is a running runtime candidate. Do not restart from architecture-only assumptions.

## Objective

Implement local-only semantic bus, artifact lenses, context distillery, worklet graph, Work Atom runtime, storage/trace/receipt records and local API skeleton as one coherent execution substrate. Post-v0.8.6 focus: complete and harden the direct runtime candidate already materialized by ChatGPT.

## Already materialized by ChatGPT

- RuntimeStore
- WorkSession state machine
- Work Atom Runtime
- Local API smoke endpoints
- candidate/session/qirc local file persistence
- run-golden-flow candidate path

## Codex completion focus

- split current runtime flow into clearer bus/worklet/store boundaries
- complete persistent store semantics and error taxonomy
- add actual worklet graph abstraction above work atoms
- harden Local API request/response validation
- improve deterministic fixture coverage for storage and atom planning

## Expected deliverables

- odin/bus or equivalent semantic bus module
- odin/worklets module
- hardened odin/runtime/store.py
- Local API endpoint tests
- work atom negative tests

## Existing files to preserve and inspect first

- `odin/storage/`
- `odin/api/`
- `docs/WORK_ATOM_RUNTIME_LOCK_V7_1.md`
- `tests/`

## Target/new paths allowed for this PR

- `odin/bus/`
- `odin/worklets/`
- `odin/work_atoms/`
- `schemas/v7_1/odin_work_atom*.json`
- `registries/work_atom_*`

## Forbidden scope

- no model provider implementation
- no app apply endpoint
- no WAN or LAN transport
- no unbounded atom recursion
- no hidden background worker autonomy

## Required behavior

- semantic events remain local-only
- Universal Work decomposes into bounded Worklets and Work Atoms
- Work Atom budgets stop runaway micro-op expansion
- storage, trace and local API surfaces preserve candidate-only discipline

## Acceptance gates

- All modified registries and schemas remain JSON-valid
- Codex return report separates implemented, prepared, skipped and blocked work
- No host/model/provider proof is claimed without a receipt produced in that environment
- PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
- all proof gaps and non-claims are stated in the PR summary
- bus fixtures validate
- every created or updated artifact is registered in FILE_MANIFEST.json
- local API remains localhost/local IPC scoped
- negative recursion/budget fixtures fail closed
- python -m odin.cli validate-all
- work atom fixtures validate

## Required commands

- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`
- `python -m odin.cli run-golden-flow`
- `python -m odin.cli serve --host 127.0.0.1 --port 8877 --once-smoke || true`
- `python -m odin.cli validate-all`

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

## Senior reviewer focus

- state determinism
- no hidden apply
- no external networking beyond localhost candidate API
- small composable atoms

## Return format

```text
PR: REAL-GH-PR-02
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

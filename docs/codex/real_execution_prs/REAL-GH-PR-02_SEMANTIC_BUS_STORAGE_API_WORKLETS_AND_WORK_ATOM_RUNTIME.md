# REAL-GH-PR-02 — Semantic Bus, Storage, API, Worklets and Work Atom Runtime

## Objective

Implement local-only semantic bus, artifact lenses, context distillery, worklet graph, Work Atom runtime, storage/trace/receipt records and local API skeleton as one coherent execution substrate.

## Position in the Real Execution Chain

- Execution PR: `REAL-GH-PR-02`
- Depends on: REAL-GH-PR-01
- Legacy internal tasks covered: PR-05, PR-06, PR-07, PR-11, PR-12, PR-108, PR-109, PR-110, PR-111

This document is the Codex-facing real GitHub PR bundle. The older `PR-00..PR-123` task ladder and the older `REAL-PR-01..REAL-PR-28` bundle ladder are retained as internal planning detail only. Codex should build from this document when executing the real repository sequence.

## Internal Tasks Covered

- `PR-05` — Internal Semantic Bus MVP
- `PR-06` — Artifact Lenses and Context Distillery
- `PR-07` — Worklet Graph Slot Forge and Gaptext
- `PR-11` — Storage Trace Receipt Layer
- `PR-12` — Local API Server
- `PR-108` — Work Atom Core Schema and Registry
- `PR-109` — Work Atom Graph and Budget Gate
- `PR-110` — Micro to Macro Work Synthesis
- `PR-111` — Work Atom Shadow Runtime and Fixtures

## Primary Files

- `odin/bus/`
- `odin/worklets/`
- `odin/work_atoms/`
- `odin/storage/`
- `odin/api/`
- `schemas/v7_1/odin_work_atom*.json`
- `registries/work_atom_*`
- `docs/WORK_ATOM_RUNTIME_LOCK_V7_1.md`
- `tests/`

## Required Behavior

- semantic events remain local-only
- Universal Work decomposes into bounded Worklets and Work Atoms
- Work Atom budgets stop runaway micro-op expansion
- storage, trace and local API surfaces preserve candidate-only discipline

## Forbidden Scope

- no model provider implementation
- no app apply endpoint
- no WAN or LAN transport
- no unbounded atom recursion
- no hidden background worker autonomy

## Acceptance / Definition of Done

- bus fixtures validate
- work atom fixtures validate
- negative recursion/budget fixtures fail closed
- local API remains localhost/local IPC scoped

Additional Definition of Done:

- `python -m odin.cli validate-all` returns no errors.
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider` returns a green suite.
- No new file claims runtime proof, host validation, production status, network proof, model-inference proof, security certification, or app-apply authority.
- All created schemas, registries, fixtures, docs and tests are included in `FILE_MANIFEST.json`.
- The PR summary explicitly separates implemented code, shadow/prep contracts, fixtures, validation results, and known proof gaps.

## Codex PR Summary Template

```text
{b['id']} — {b['title']}

Scope:
- ...

Implemented:
- ...

Validation:
- python -m odin.cli validate-all: ...
- PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider: ...

Proof gaps / non-claims:
- no runtime proof unless actually executed on host
- no model-inference proof unless actual local/remote model run is evidenced
- no app-apply authority for Odin
```

## Senior Reviewer Notes

This PR is intentionally large enough to be real-reviewable as a GitHub PR but not so large that unrelated runtime, Windows, model and release concerns are mixed without a dependency boundary. Do not split it back into the internal micro-ladder unless Codex is blocked by file-size or review-size constraints.
---

## v0.7.7 Build Ladder Absolute Alignment Addendum


This addendum is authoritative for the actual GitHub execution ladder. It separates existing prep files from target implementation paths and binds this PR to Master Architecture v7.1.

### Absorbed Internal Tasks

- `PR-05`
- `PR-06`
- `PR-07`
- `PR-11`
- `PR-12`
- `PR-108`
- `PR-109`
- `PR-110`
- `PR-111`

### Absorbed Legacy Bundles

Full absorption:

- `REAL-PR-03`
- `REAL-PR-26`

Partial absorption:

- `REAL-PR-05` — covers PR-11, PR-12 of 3 internal tasks

### Existing Prep Files / Paths

- `odin/storage/`
- `odin/api/`
- `docs/WORK_ATOM_RUNTIME_LOCK_V7_1.md`
- `tests/`

### Target Implementation Files / Paths

- `odin/bus/`
- `odin/worklets/`
- `odin/work_atoms/`
- `schemas/v7_1/odin_work_atom*.json`
- `registries/work_atom_*`

### Master Architecture Sections

- `Internal Semantic Bus`
- `Storage Spec`
- `API Spec`
- `Worklet Runtime`
- `Work Atom Runtime`

### Acceptance Gates

- `bus fixtures validate`
- `work atom fixtures validate`
- `negative recursion/budget fixtures fail closed`
- `local API remains localhost/local IPC scoped`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`
- `every created or updated artifact is registered in FILE_MANIFEST.json`
- `all proof gaps and non-claims are stated in the PR summary`

### Must Run

- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`

### Must Preserve

- `no_llm_in_app`
- `candidate_only`
- `local_first`
- `app_owns_state`
- `semantic_bus_local_only`
- `app_owns_apply`
- `gpl_2_0_only`
- `no_runtime_proof`

### Proof Boundaries

- `no_runtime_proof_without_host_receipts`
- `no_model_inference_proof_without_actual_model_receipts`
- `no_app_apply_authority_for_odin`
- `no_external_send_by_odin`
- `no_network_qirc_by_default`
- `no_production_readiness_claim`
- `no_model_provider_implementation`
- `no_app_apply_endpoint`
- `no_wan_or_lan_transport`
- `no_unbounded_atom_recursion`
- `no_hidden_background_worker_autonomy`

### Codex Stop Conditions

- stop if a target path would bypass the app-owned apply boundary
- stop if a model, agent, seed pack, flow pack, runtime pack or Windows component attempts to become authority
- stop if the implementation requires external network behavior not explicitly authorized by the current PR
- stop if validation cannot distinguish implemented code from shadow/prep contracts
- stop if public docs would imply host proof, model proof, security certification, or completed product behavior without receipts


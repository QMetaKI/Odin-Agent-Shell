# REAL-GH-PR-08 — App SDKs, App QIRC Digest, Golden Flows, Release Hygiene and Public Build Gate

## Objective

Finalize app-facing SDK/templates, App QIRC digest bridge, golden flows, support bundle/release hygiene, senior-review hardening and public build-ready gate so the repo can be handed to Codex as a coherent build program.

## Position in the Real Execution Chain

- Execution PR: `REAL-GH-PR-08`
- Depends on: REAL-GH-PR-07
- Legacy internal tasks covered: PR-13, PR-16, PR-20, PR-21, PR-22, PR-122, PR-123

This document is the Codex-facing real GitHub PR bundle. The older `PR-00..PR-123` task ladder and the older `REAL-PR-01..REAL-PR-28` bundle ladder are retained as internal planning detail only. Codex should build from this document when executing the real repository sequence.

## Internal Tasks Covered

- `PR-13` — SDKs and App Templates
- `PR-16` — App QIRC Bridge Digest
- `PR-20` — End-to-End Golden Flows
- `PR-21` — Release Prep Hygiene and Support Bundle
- `PR-22` — Senior Review Hardening and Anti-Drift Lock
- `PR-122` — Codex Public Build Ready Gate
- `PR-123` — Public Repo Windows Build Ready Consolidation

## Primary Files

- `sdk/`
- `templates/`
- `examples/`
- `docs/codex/`
- `docs/PUBLIC_REPO_RELEASE_CHECKLIST_V7_1.md`
- `docs/CODEX_PUBLIC_BUILD_READY_GATE_V7_1.md`
- `registries/public_build_readiness_registry.json`
- `tests/`

## Required Behavior

- apps integrate through SDK/template bridges without LLM logic
- App QIRC bridge is digest-only by default
- golden flows exercise full candidate path
- public build gate blocks overclaims and missing docs/fixtures

## Forbidden Scope

- no app-owned state stored inside Odin
- no direct external send from Odin
- no production-ready wording
- no hidden model credentials
- no collapsing internal ladders into unexplained mega-PR

## Acceptance / Definition of Done

- golden flow fixtures validate
- release checklist is current-canon only
- senior-review anti-drift gates remain active
- all internal tasks are covered by consolidated real execution PRs

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

- `PR-13`
- `PR-16`
- `PR-20`
- `PR-21`
- `PR-22`
- `PR-122`
- `PR-123`

### Absorbed Legacy Bundles

Full absorption:

- `REAL-PR-06`
- `REAL-PR-08`

Partial absorption:

- `REAL-PR-28` — covers PR-122, PR-123 of 8 internal tasks

### Existing Prep Files / Paths

- `sdk/`
- `templates/`
- `examples/`
- `docs/codex/`
- `docs/PUBLIC_REPO_RELEASE_CHECKLIST_V7_1.md`
- `docs/CODEX_PUBLIC_BUILD_READY_GATE_V7_1.md`
- `registries/public_build_readiness_registry.json`
- `tests/`

### Target Implementation Files / Paths

- none

### Master Architecture Sections

- `App SDKs and Templates`
- `App QIRC Digest`
- `Golden Flows`
- `Public Build Gate`

### Acceptance Gates

- `golden flow fixtures validate`
- `release checklist is current-canon only`
- `senior-review anti-drift gates remain active`
- `all internal tasks are covered by consolidated real execution PRs`
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
- `default_model_strategy_3b_7b_8b`
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
- `no_app-owned_state_stored_inside_odin`
- `no_direct_external_send_from_odin`
- `no_production-ready_wording`
- `no_hidden_model_credentials`
- `no_collapsing_internal_ladders_into_unexplained_mega-pr`

### Codex Stop Conditions

- stop if a target path would bypass the app-owned apply boundary
- stop if a model, agent, seed pack, flow pack, runtime pack or Windows component attempts to become authority
- stop if the implementation requires external network behavior not explicitly authorized by the current PR
- stop if validation cannot distinguish implemented code from shadow/prep contracts
- stop if public docs would imply host proof, model proof, security certification, or completed product behavior without receipts


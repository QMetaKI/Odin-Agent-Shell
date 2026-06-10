# REAL-GH-PR-01 — Foundation, Canon, Protocol and Universal Work Core

## Objective

Create the public repo foundation, strict JSON/registry hygiene, binding gate, Universal Work core, candidate artifact core, and current-canon root surface before feature implementation expands.

## Position in the Real Execution Chain

- Execution PR: `REAL-GH-PR-01`
- Depends on: none
- Legacy internal tasks covered: PR-00, PR-01, PR-02, PR-03, PR-04, PR-116

This document is the Codex-facing real GitHub PR bundle. The older `PR-00..PR-123` task ladder and the older `REAL-PR-01..REAL-PR-28` bundle ladder are retained as internal planning detail only. Codex should build from this document when executing the real repository sequence.

## Internal Tasks Covered

- `PR-00` — Canon Gates and Repo Hygiene
- `PR-01` — Schema Strictening and Registry Parity
- `PR-02` — Protocol Packets and Binding Gate
- `PR-03` — Universal Work Kernel
- `PR-04` — Candidate Artifacts Response Packets and Candidate DNA
- `PR-116` — Public Repo Canon Cleanup Lock

## Primary Files

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

## Required Behavior

- root docs point to one current canon
- validate-all blocks schema/registry drift
- Universal Work and Candidate Artifact contracts are app-renderable and candidate-only
- Binding gate preserves app authority and Odin non-apply posture

## Forbidden Scope

- no live model provider execution
- no Windows tray/control-center implementation
- no app state mutation
- no remote/network enablement
- no runtime-proof claim

## Acceptance / Definition of Done

- validate-all is green
- pytest suite is green
- root docs contain no competing current-canon path
- all public-entry docs point to this consolidated real PR execution plan

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

- `PR-00`
- `PR-01`
- `PR-02`
- `PR-03`
- `PR-04`
- `PR-116`

### Absorbed Legacy Bundles

Full absorption:

- `REAL-PR-01`
- `REAL-PR-02`

Partial absorption:

- `REAL-PR-28` — covers PR-116 of 8 internal tasks

### Existing Prep Files / Paths

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

### Target Implementation Files / Paths

- none

### Master Architecture Sections

- `0 Architecture Status`
- `Universal Work Kernel`
- `Binding Gate`
- `Candidate Artifact`
- `Public Canon`

### Acceptance Gates

- `validate-all is green`
- `pytest suite is green`
- `root docs contain no competing current-canon path`
- `all public-entry docs point to this consolidated real PR execution plan`
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
- `no_live_model_provider_execution`
- `no_windows_tray/control-center_implementation`
- `no_app_state_mutation`
- `no_remote/network_enablement`
- `no_runtime-proof_claim`

### Codex Stop Conditions

- stop if a target path would bypass the app-owned apply boundary
- stop if a model, agent, seed pack, flow pack, runtime pack or Windows component attempts to become authority
- stop if the implementation requires external network behavior not explicitly authorized by the current PR
- stop if validation cannot distinguish implemented code from shadow/prep contracts
- stop if public docs would imply host proof, model proof, security certification, or completed product behavior without receipts


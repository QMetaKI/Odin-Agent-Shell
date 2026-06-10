# REAL-GH-PR-05 — Narrative Compiler, Shadow Runtime, Runtime Packs and Loki Anti-Pattern Layer

## Objective

Build the code-near Shadow Runtime, Fairy/Y* narrative compiler, runtime pack/capability slice pipeline, generated gates, Shadow Narrative, Anti-Fairy DSL, Loki mediation and narrative red-team compiler.

## Position in the Real Execution Chain

- Execution PR: `REAL-GH-PR-05`
- Depends on: REAL-GH-PR-04
- Legacy internal tasks covered: PR-23, PR-24, PR-25, PR-26, PR-27, PR-28, PR-29, PR-30, PR-31, PR-32, PR-33, PR-34, PR-35, PR-36, PR-37, PR-93, PR-94, PR-95, PR-96, PR-97

This document is the Codex-facing real GitHub PR bundle. The older `PR-00..PR-123` task ladder and the older `REAL-PR-01..REAL-PR-28` bundle ladder are retained as internal planning detail only. Codex should build from this document when executing the real repository sequence.

## Internal Tasks Covered

- `PR-23` — Shadow Runtime Code-Near Lock
- `PR-24` — Full Shadow Runtime Coverage
- `PR-25` — Shadow Runtime Near-Final Optimization Lock
- `PR-26` — Y* Native DSL and Narrative Aorta Spec
- `PR-27` — Fairy DSL Parser / Validator Shadow Layer
- `PR-28` — Fairy to Shadow IR Mapping
- `PR-29` — Y* Mediation Directive and Runtime Pack Prelude
- `PR-30` — Narrative Code Boundary Gates
- `PR-31` — Shadow Runtime IR Formalization
- `PR-32` — Runtime Pack Manifest and Validator
- `PR-33` — AOT Runtime Pack Compiler
- `PR-34` — Capability Slice Compiler
- `PR-35` — Pack Loader, Cache and Rollback
- `PR-36` — Generated Gates and Golden Tests
- `PR-37` — Low-Memory / Standard / Quality Runtime Packs
- `PR-93` — Shadow Narrative Core
- `PR-94` — Anti-Fairy DSL and Narrative Anti-Pattern Mirror
- `PR-95` — Loki Mediation Layer and Boundary Policy
- `PR-96` — Shadow Narrative to Gate Compiler
- `PR-97` — Narrative Red-Team Fixtures and Negative Runtime Tests

## Primary Files

- `odin/shadow_runtime/`
- `odin/compiler/`
- `examples/fairy/`
- `examples/compiler/`
- `examples/shadow_narrative/`
- `registries/fairy_*`
- `registries/shadow_*`
- `registries/loki_*`
- `docs/SHADOW_RUNTIME_LOCK_V7_1.md`
- `docs/SHADOW_NARRATIVE_V7_1.md`
- `tests/`

## Required Behavior

- narrative units compile into typed shadow/runtime artifacts
- Shadow Runtime is code-near but non-authoritative
- Loki emits risk candidates only
- anti-patterns map to signals, gates, fixtures and repairs

## Forbidden Scope

- no prose-only execution
- no generated hot-path executable runtime
- no Loki authority
- no unvalidated runtime pack load
- no narrative claim treated as truth

## Acceptance / Definition of Done

- shadow runtime registry contracts validate
- Fairy/Y*/runtime pack fixtures validate
- Loki authority escalation fixture is invalid
- negative red-team cases map to gates

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

- `PR-23`
- `PR-24`
- `PR-25`
- `PR-26`
- `PR-27`
- `PR-28`
- `PR-29`
- `PR-30`
- `PR-31`
- `PR-32`
- `PR-33`
- `PR-34`
- `PR-35`
- `PR-36`
- `PR-37`
- `PR-93`
- `PR-94`
- `PR-95`
- `PR-96`
- `PR-97`

### Absorbed Legacy Bundles

Full absorption:

- `REAL-PR-09`
- `REAL-PR-10`
- `REAL-PR-11`
- `REAL-PR-12`
- `REAL-PR-13`
- `REAL-PR-23`

Partial absorption:

- none

### Existing Prep Files / Paths

- `odin/shadow_runtime/`
- `odin/compiler/`
- `examples/fairy/`
- `examples/compiler/`
- `examples/shadow_narrative/`
- `docs/SHADOW_RUNTIME_LOCK_V7_1.md`
- `docs/SHADOW_NARRATIVE_V7_1.md`
- `tests/`

### Target Implementation Files / Paths

- `registries/fairy_*`
- `registries/shadow_*`
- `registries/loki_*`

### Master Architecture Sections

- `Shadow Runtime`
- `Fairy/Y* Narrative Compiler`
- `Runtime Packs`
- `Loki Anti-Pattern Layer`

### Acceptance Gates

- `shadow runtime registry contracts validate`
- `Fairy/Y*/runtime pack fixtures validate`
- `Loki authority escalation fixture is invalid`
- `negative red-team cases map to gates`
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
- `shadow_runtime_non_authority`
- `resource_based_model_routing`
- `v7_1_invariants`
- `no_prose_execution`
- `validated_pack_load_only`
- `app_owns_apply`
- `no_loki_authority`
- `gpl_2_0_only`

### Proof Boundaries

- `no_runtime_proof_without_host_receipts`
- `no_model_inference_proof_without_actual_model_receipts`
- `no_app_apply_authority_for_odin`
- `no_external_send_by_odin`
- `no_network_qirc_by_default`
- `no_production_readiness_claim`
- `no_prose-only_execution`
- `no_generated_hot-path_executable_runtime`
- `no_loki_authority`
- `no_unvalidated_runtime_pack_load`
- `no_narrative_claim_treated_as_truth`

### Codex Stop Conditions

- stop if a target path would bypass the app-owned apply boundary
- stop if a model, agent, seed pack, flow pack, runtime pack or Windows component attempts to become authority
- stop if the implementation requires external network behavior not explicitly authorized by the current PR
- stop if validation cannot distinguish implemented code from shadow/prep contracts
- stop if public docs would imply host proof, model proof, security certification, or completed product behavior without receipts


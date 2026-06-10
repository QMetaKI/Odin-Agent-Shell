# REAL-GH-PR-03 — Model Runtime, Pre-LLM Intelligence and Universal Model/Agent Boundary

## Objective

Build the model/agent worker layer: scale ladder, mock/local provider seams, low-memory strict behavior, pre-LLM intelligence, model-work avoidance, output composer, model/agent cards, permission cards and local/remote parity boundary.

## Position in the Real Execution Chain

- Execution PR: `REAL-GH-PR-03`
- Depends on: REAL-GH-PR-02
- Legacy internal tasks covered: PR-08, PR-09, PR-14, PR-15, PR-17, PR-61, PR-62, PR-63, PR-64, PR-65, PR-66, PR-67, PR-68, PR-69, PR-70, PR-71, PR-72, PR-81, PR-82, PR-83, PR-84, PR-85

This document is the Codex-facing real GitHub PR bundle. The older `PR-00..PR-123` task ladder and the older `REAL-PR-01..REAL-PR-28` bundle ladder are retained as internal planning detail only. Codex should build from this document when executing the real repository sequence.

## Internal Tasks Covered

- `PR-08` — Model Scale Ladder Router and Mock Provider
- `PR-09` — Small Model Power Core
- `PR-14` — Ollama and llama.cpp Provider Adapters
- `PR-15` — Low-Memory Strict Mode
- `PR-17` — Model Dojo and Scoreboard
- `PR-61` — Pre-LLM Intelligence Layer
- `PR-62` — Model Work Avoidance and Admissibility Expansion
- `PR-63` — Output Intelligence Composer
- `PR-64` — Perceived Intelligence Metrics
- `PR-65` — Micro-to-Macro Candidate Synthesis
- `PR-66` — Universal Model / Agent Parity Matrix
- `PR-67` — Model / Agent Capability Cards
- `PR-68` — Work Capsules and Capability Packs for Agents
- `PR-69` — External Agent Adapter Boundary
- `PR-70` — Universal Agent Candidate Protocol
- `PR-71` — Agent Permission Cards and Apply Boundary
- `PR-72` — Universal Agent Why Trace and Archetype Roles
- `PR-81` — Universal LLM Work Construct
- `PR-82` — Universal Model Agent Adapter Contract
- `PR-83` — Remote Worker Boundary and Local Remote Parity
- `PR-84` — Agent Tool Permission Boundary
- `PR-85` — Universal Use Case Matrix

## Primary Files

- `odin/models/`
- `odin/precompute/`
- `odin/agents/`
- `odin/output/`
- `registries/model_*`
- `registries/universal_llm_worker_registry.json`
- `registries/remote_worker_boundary_registry.json`
- `docs/PRE_LLM_INTELLIGENCE_LAYER_V7_1.md`
- `docs/UNIVERSAL_LLM_WORK_CONSTRUCT_V7_1.md`
- `tests/`

## Required Behavior

- Odin does deterministic/precompute work before model dispatch
- smallest sufficient worker is selected from declared capability cards
- remote workers are candidate workers only
- permission cards block apply, external send and authority escalation

## Forbidden Scope

- no remote provider credentials
- no unreviewed tool use by agents
- no model output accepted as truth
- no app state ownership by Odin
- no production performance claim

## Acceptance / Definition of Done

- model routing negative cases fail closed
- remote worker boundary fixtures validate
- agent permission fixtures block apply/tool escalation
- pre-LLM direct-apply example remains invalid

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

- `PR-08`
- `PR-09`
- `PR-14`
- `PR-15`
- `PR-17`
- `PR-61`
- `PR-62`
- `PR-63`
- `PR-64`
- `PR-65`
- `PR-66`
- `PR-67`
- `PR-68`
- `PR-69`
- `PR-70`
- `PR-71`
- `PR-72`
- `PR-81`
- `PR-82`
- `PR-83`
- `PR-84`
- `PR-85`

### Absorbed Legacy Bundles

Full absorption:

- `REAL-PR-04`
- `REAL-PR-18`
- `REAL-PR-19`

Partial absorption:

- `REAL-PR-07` — covers PR-17 of 3 internal tasks
- `REAL-PR-21` — covers PR-81, PR-82, PR-83, PR-84, PR-85 of 6 internal tasks

### Existing Prep Files / Paths

- `odin/models/`
- `odin/precompute/`
- `registries/universal_llm_worker_registry.json`
- `registries/remote_worker_boundary_registry.json`
- `docs/PRE_LLM_INTELLIGENCE_LAYER_V7_1.md`
- `docs/UNIVERSAL_LLM_WORK_CONSTRUCT_V7_1.md`
- `tests/`

### Target Implementation Files / Paths

- `odin/agents/`
- `odin/output/`
- `registries/model_*`

### Master Architecture Sections

- `Model Scale Ladder`
- `Pre-LLM Intelligence`
- `Universal Model/Agent Boundary`
- `Remote Worker Boundary`

### Acceptance Gates

- `model routing negative cases fail closed`
- `remote worker boundary fixtures validate`
- `agent permission fixtures block apply/tool escalation`
- `pre-LLM direct-apply example remains invalid`
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
- `pre_model_admissibility`
- `truthful_perceived_intelligence`
- `universal_worker_boundary`
- `why_trace`
- `same_boundary_for_all_workers`
- `gpl_2_0_only`

### Proof Boundaries

- `no_runtime_proof_without_host_receipts`
- `no_model_inference_proof_without_actual_model_receipts`
- `no_app_apply_authority_for_odin`
- `no_external_send_by_odin`
- `no_network_qirc_by_default`
- `no_production_readiness_claim`
- `no_remote_provider_credentials`
- `no_unreviewed_tool_use_by_agents`
- `no_model_output_accepted_as_truth`
- `no_app_state_ownership_by_odin`
- `no_production_performance_claim`

### Codex Stop Conditions

- stop if a target path would bypass the app-owned apply boundary
- stop if a model, agent, seed pack, flow pack, runtime pack or Windows component attempts to become authority
- stop if the implementation requires external network behavior not explicitly authorized by the current PR
- stop if validation cannot distinguish implemented code from shadow/prep contracts
- stop if public docs would imply host proof, model proof, security certification, or completed product behavior without receipts


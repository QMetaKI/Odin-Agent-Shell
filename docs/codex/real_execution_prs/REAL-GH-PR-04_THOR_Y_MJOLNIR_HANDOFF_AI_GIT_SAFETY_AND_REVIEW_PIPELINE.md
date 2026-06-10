# REAL-GH-PR-04 — Thor/Y/Mjolnir Handoff, AI-Git Safety and Review Pipeline

## Objective

Implement Thor bridge, bounded code work, AI-Git safety architecture, autonomy escalation gate, semantic diff/branch/merge, human review boundary and Thor/Y/Mjolnir handoff compiler pipeline.

## Position in the Real Execution Chain

- Execution PR: `REAL-GH-PR-04`
- Depends on: REAL-GH-PR-03
- Legacy internal tasks covered: PR-10, PR-56, PR-57, PR-58, PR-59, PR-60, PR-73, PR-74, PR-75, PR-76, PR-77, PR-78, PR-79, PR-80, PR-86

This document is the Codex-facing real GitHub PR bundle. The older `PR-00..PR-123` task ladder and the older `REAL-PR-01..REAL-PR-28` bundle ladder are retained as internal planning detail only. Codex should build from this document when executing the real repository sequence.

## Internal Tasks Covered

- `PR-10` — Thor Bridge and Bounded Code Work
- `PR-56` — AI-Git Safety Architecture Consolidation
- `PR-57` — Autonomy Escalation Gate Lock
- `PR-58` — Safety Superposition Policy Lock
- `PR-59` — Semantic Diff Branch Merge and Human Review Boundary
- `PR-60` — Skynet Pattern Boundary and AI-Git Why Trace
- `PR-73` — Thor Prompt Pull and Handoff Compiler Core
- `PR-74` — Thor Return Review and Receipt Boundary Pipeline
- `PR-75` — Y Handoff Bridge and Centerline Packet Compiler
- `PR-76` — Mjolnir Focused Strike Handoff Bridge
- `PR-77` — Handoff Prompt Canonicalization and Pattern Registry
- `PR-78` — Handoff to Universal Work Conversion
- `PR-79` — Handoff Postprocessing Candidate Pipeline
- `PR-80` — Thor Y Mjolnir Consolidated Handoff Gates
- `PR-86` — Thor Odin AI Git Work Session and GPL2 Policy

## Primary Files

- `odin/handoff/`
- `odin/aigit/`
- `odin/review/`
- `odin/thor/`
- `odin/mjolnir/`
- `registries/handoff_*`
- `registries/ai_git_*`
- `docs/THOR_Y_HANDOFF_COMPILER_CORE_V7_1.md`
- `docs/AI_GIT_SAFETY_ARCHITECTURE_V7_1.md`
- `tests/`

## Required Behavior

- handoffs compile into Universal Work rather than uncontrolled prompts
- returns become candidate artifacts with review metadata
- semantic diff and branch/merge are candidate-only
- human/app review remains outside model authority

## Forbidden Scope

- no auto-merge
- no auto-apply
- no receipt issuance by model/agent
- no autonomous PR creation
- no claim acceptance without evidence gate

## Acceptance / Definition of Done

- Thor handoff fixtures validate
- direct-apply handoff fixtures fail closed
- AI-Git why trace is produced for candidate branches
- review pipeline preserves app-owned apply

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

- `PR-10`
- `PR-56`
- `PR-57`
- `PR-58`
- `PR-59`
- `PR-60`
- `PR-73`
- `PR-74`
- `PR-75`
- `PR-76`
- `PR-77`
- `PR-78`
- `PR-79`
- `PR-80`
- `PR-86`

### Absorbed Legacy Bundles

Full absorption:

- `REAL-PR-17`
- `REAL-PR-20`

Partial absorption:

- `REAL-PR-05` — covers PR-10 of 3 internal tasks
- `REAL-PR-21` — covers PR-86 of 6 internal tasks

### Existing Prep Files / Paths

- `docs/THOR_Y_HANDOFF_COMPILER_CORE_V7_1.md`
- `docs/AI_GIT_SAFETY_ARCHITECTURE_V7_1.md`
- `tests/`

### Target Implementation Files / Paths

- `odin/handoff/`
- `odin/aigit/`
- `odin/review/`
- `odin/thor/`
- `odin/mjolnir/`
- `registries/handoff_*`
- `registries/ai_git_*`

### Master Architecture Sections

- `Thor Handoff Compiler`
- `AI-Git Safety Layer`
- `Human Review Boundary`
- `Semantic Diff`

### Acceptance Gates

- `Thor handoff fixtures validate`
- `direct-apply handoff fixtures fail closed`
- `AI-Git why trace is produced for candidate branches`
- `review pipeline preserves app-owned apply`
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
- `bug6_children_first`
- `q7_stability`
- `safety_superposition`
- `app_owned_apply`
- `no_authority_transfer`
- `no_hidden_execution`
- `thor_kernel_bound`
- `y_centerline_bound`
- `mjolnir_candidate_only`
- `app_owns_apply`
- `same_boundary_for_all_workers`
- `gpl_2_0_only`

### Proof Boundaries

- `no_runtime_proof_without_host_receipts`
- `no_model_inference_proof_without_actual_model_receipts`
- `no_app_apply_authority_for_odin`
- `no_external_send_by_odin`
- `no_network_qirc_by_default`
- `no_production_readiness_claim`
- `no_auto-merge`
- `no_auto-apply`
- `no_receipt_issuance_by_model/agent`
- `no_autonomous_pr_creation`
- `no_claim_acceptance_without_evidence_gate`

### Codex Stop Conditions

- stop if a target path would bypass the app-owned apply boundary
- stop if a model, agent, seed pack, flow pack, runtime pack or Windows component attempts to become authority
- stop if the implementation requires external network behavior not explicitly authorized by the current PR
- stop if validation cannot distinguish implemented code from shadow/prep contracts
- stop if public docs would imply host proof, model proof, security certification, or completed product behavior without receipts


# Codex Prompt — REAL-GH-PR-04 — Thor/Y/Mjölnir Handoff, AI-Git Safety and Review Pipeline — Real Modules

## Base state

You are working in `Odin-Agent-Shell` after:

```text
v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK
```

This is a running runtime candidate. Do not restart from architecture-only assumptions.

## Objective

Implement Thor bridge, bounded code work, AI-Git safety architecture, autonomy escalation gate, semantic diff/branch/merge, human review boundary and Thor/Y/Mjolnir handoff compiler pipeline. Post-v0.8.6 focus: complete and harden the direct runtime candidate already materialized by ChatGPT.

## Already materialized by ChatGPT

- handoff/compiler specs and registries
- candidate artifact/why trace code
- AI-Git safety architecture docs
- review boundary docs
- semantic diff concepts

## Codex completion focus

- materialize Thor handoff compiler modules
- materialize candidate branch/semantic diff/review gate modules
- connect handoff packets into Universal Work runtime path
- add negative tests for direct-apply handoffs and fake receipts
- keep Thor/Y/Mjölnir as candidate workers only

## Expected deliverables

- odin/handoff module
- odin/aigit module
- odin/review module
- handoff-to-work tests
- semantic diff fixtures
- receipt-boundary tests

## Existing files to preserve and inspect first

- `docs/THOR_Y_HANDOFF_COMPILER_CORE_V7_1.md`
- `docs/AI_GIT_SAFETY_ARCHITECTURE_V7_1.md`
- `tests/`

## Target/new paths allowed for this PR

- `odin/handoff/`
- `odin/aigit/`
- `odin/review/`
- `odin/thor/`
- `odin/mjolnir/`
- `registries/handoff_*`
- `registries/ai_git_*`

## Forbidden scope

- no auto-merge
- no auto-apply
- no receipt issuance by model/agent
- no autonomous PR creation
- no claim acceptance without evidence gate

## Required behavior

- handoffs compile into Universal Work rather than uncontrolled prompts
- returns become candidate artifacts with review metadata
- semantic diff and branch/merge are candidate-only
- human/app review remains outside model authority

## Acceptance gates

- AI-Git why trace is produced for candidate branches
- All modified registries and schemas remain JSON-valid
- Codex return report separates implemented, prepared, skipped and blocked work
- No host/model/provider proof is claimed without a receipt produced in that environment
- PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
- Thor handoff fixtures validate
- all proof gaps and non-claims are stated in the PR summary
- direct-apply handoff fixtures fail closed
- every created or updated artifact is registered in FILE_MANIFEST.json
- python -m odin.cli validate-all
- review pipeline preserves app-owned apply

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
- bug6_children_first
- q7_stability
- safety_superposition
- app_owned_apply
- no_authority_transfer
- no_hidden_execution
- thor_kernel_bound
- y_centerline_bound
- mjolnir_candidate_only
- app_owns_apply
- same_boundary_for_all_workers
- gpl_2_0_only

## Proof boundaries

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

## Senior reviewer focus

- candidate-only handoff
- no receipt fabrication
- no agent swarm
- no tool/apply authority transfer

## Return format

```text
PR: REAL-GH-PR-04
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

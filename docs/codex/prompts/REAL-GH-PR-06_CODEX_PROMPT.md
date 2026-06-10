# Codex Prompt — REAL-GH-PR-06 — Odin Core, QIRC Gold Spine, Seeds, Pattern Mines and Flow Packs — Runtime Hardening

## Base state

You are working in `Odin-Agent-Shell` after:

```text
v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK
```

This is a running runtime candidate. Do not restart from architecture-only assumptions.

## Objective

Implement Odin Core Centerline, QLI/DFAS/QMath route scoring, QIRC Gold Spine, Bug6/Q7 invariant layer, operational seed/archetype substrate, App Seed Pack compiler, Pattern Mine intake and Flow Pack bridge. Post-v0.8.6 focus: complete and harden the direct runtime candidate already materialized by ChatGPT.

## Already materialized by ChatGPT

- odin/core package
- QIRC local ledger
- seed pack compiler/security
- pattern mine intake/spine
- flow pack compiler
- run-work end-to-end golden flow

## Codex completion focus

- harden QIRC envelope and replay semantics
- add signature/review/certification states for seed and pattern packs
- stress-test pattern mine ingestion without importing truth authority
- improve flow-pack to work-atom planning
- add conflict resolution and activation budget tests

## Expected deliverables

- pack certification state machine
- seed/pattern conflict tests
- QIRC replay/snapshot tests
- flow-pack planning tests
- bulk pattern-mine fixture with claim-boundary lock

## Existing files to preserve and inspect first

- `odin/core/`
- `registries/flow_pack_registry.json`
- `docs/ODIN_CORE_CENTERLINE_V7_1.md`
- `docs/APP_SEED_PACK_COMPILER_V7_1.md`
- `docs/PATTERN_MINE_FLOW_PACK_INTAKE_LOCK_V7_1.md`
- `tests/`

## Target/new paths allowed for this PR

- `odin/qirc/`
- `odin/seeds/`
- `odin/patterns/`
- `odin/flow_packs/`
- `registries/qirc_*`
- `registries/seed_*`
- `registries/pattern_*`

## Forbidden scope

- no executable seed pack code
- no religious/domain truth leakage from pattern mines
- no QIRC network expansion
- no unbounded seed fanout
- no bypass of Odin final gate

## Required behavior

- centerline/admissibility gates run before dispatch
- QIRC stays local/internal and trace-bound
- seed and pattern packs are declarative, signed/classified or review-required
- Pattern Mines compile to pattern spines/flow packs without becoming truth authority

## Acceptance gates

- All modified registries and schemas remain JSON-valid
- Bug6/Q7 gates remain present in route decisions
- Codex return report separates implemented, prepared, skipped and blocked work
- No host/model/provider proof is claimed without a receipt produced in that environment
- PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
- QIRC event envelope requires trace_id
- all proof gaps and non-claims are stated in the PR summary
- every created or updated artifact is registered in FILE_MANIFEST.json
- pattern mine claim-boundary examples validate
- python -m odin.cli validate-all
- seed pack invalid executable example fails closed

## Required commands

- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`
- `python -m odin.cli compile-pattern-mine examples/runtime/pattern_mine_full.valid.json`
- `python -m odin.cli compile-seed-pack examples/runtime/app_seed_pack_full.valid.json`
- `python -m odin.cli run-golden-flow`
- `python -m odin.cli validate-all`

## Must preserve

- no_llm_in_app
- candidate_only
- local_first
- app_owns_state
- semantic_bus_local_only
- qirc_digest_only_bridge
- bug6_children_first
- q7_stability
- app_owns_apply
- seed_packs_declarative_only
- gpl_2_0_only
- no_runtime_proof

## Proof boundaries

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

## Senior reviewer focus

- pattern packs are pattern sources not truth sources
- no executable seed code
- QIRC remains local ledger unless explicitly future-scoped

## Return format

```text
PR: REAL-GH-PR-06
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

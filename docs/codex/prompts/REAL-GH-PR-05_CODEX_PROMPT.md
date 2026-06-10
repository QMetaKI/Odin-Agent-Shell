# Codex Prompt — REAL-GH-PR-05 — Narrative Compiler, Shadow Runtime, Runtime Packs and Loki Anti-Pattern Layer — Executable Contracts

## Base state

You are working in `Odin-Agent-Shell` after:

```text
v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK
```

This is a running runtime candidate. Do not restart from architecture-only assumptions.

## Objective

Build the code-near Shadow Runtime, Fairy/Y* narrative compiler, runtime pack/capability slice pipeline, generated gates, Shadow Narrative, Anti-Fairy DSL, Loki mediation and narrative red-team compiler. Post-v0.8.6 focus: complete and harden the direct runtime candidate already materialized by ChatGPT.

## Already materialized by ChatGPT

- Shadow Runtime modules
- Fairy/Y*/Loki docs and schemas
- Anti-Fairy/Shadow Narrative registries
- runtime pack docs and gates
- negative Loki authority fixture

## Codex completion focus

- make narrative/compiler modules produce typed intermediate artifacts consumed by runtime engine
- compile Shadow Narrative anti-patterns into gate hints
- connect runtime packs to work atom planning
- add bounded no-execution checks for generated runtime packs
- improve red-team fixture generation

## Expected deliverables

- typed narrative IR objects
- shadow-to-gate compiler tests
- runtime pack loader hardening
- Loki anti-pattern gate integration
- negative fixtures for over-poetic/no-op narrative artifacts

## Existing files to preserve and inspect first

- `odin/shadow_runtime/`
- `odin/compiler/`
- `examples/fairy/`
- `examples/compiler/`
- `examples/shadow_narrative/`
- `docs/SHADOW_RUNTIME_LOCK_V7_1.md`
- `docs/SHADOW_NARRATIVE_V7_1.md`
- `tests/`

## Target/new paths allowed for this PR

- `registries/fairy_*`
- `registries/shadow_*`
- `registries/loki_*`

## Forbidden scope

- no prose-only execution
- no generated hot-path executable runtime
- no Loki authority
- no unvalidated runtime pack load
- no narrative claim treated as truth

## Required behavior

- narrative units compile into typed shadow/runtime artifacts
- Shadow Runtime is code-near but non-authoritative
- Loki emits risk candidates only
- anti-patterns map to signals, gates, fixtures and repairs

## Acceptance gates

- All modified registries and schemas remain JSON-valid
- Codex return report separates implemented, prepared, skipped and blocked work
- Fairy/Y*/runtime pack fixtures validate
- Loki authority escalation fixture is invalid
- No host/model/provider proof is claimed without a receipt produced in that environment
- PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
- all proof gaps and non-claims are stated in the PR summary
- every created or updated artifact is registered in FILE_MANIFEST.json
- negative red-team cases map to gates
- python -m odin.cli validate-all
- shadow runtime registry contracts validate

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
- shadow_runtime_non_authority
- resource_based_model_routing
- v7_1_invariants
- no_prose_execution
- validated_pack_load_only
- app_owns_apply
- no_loki_authority
- gpl_2_0_only

## Proof boundaries

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

## Senior reviewer focus

- narrative is code-near but not executable code
- Loki emits risk candidates only
- anti-patterns must map to gate/repair/test

## Return format

```text
PR: REAL-GH-PR-05
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

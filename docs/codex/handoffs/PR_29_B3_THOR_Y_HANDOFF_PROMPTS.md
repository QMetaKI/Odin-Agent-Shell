# PR-29 B3 Thor/Y Handoff Prompts

claim_boundary: y_handoff_prompts_are_static_composition_guides_not_runtime_proof

Note: Thor/Y CLI commands (thor y analyze, thor y compose, thor y handoff, thor y handoff-spine) were not available in thor-agent-kit 4.1.1. These prompts are manual Y-discipline handoff structures following the Thor/Y patterns.

---

## 1. Thor/Y Analyze Prompt

**Purpose:** Analyze the B3 task to identify composition requirements before handoff.

```
Thor/Y Analyze — Odin B3

Task: ModelWorkPacket / Scale Ladder / Provider Seams / Small-Model Hybrid Director for Odin v7.1.1

Analyze:
1. What canonical slices does B3 cover? (V711-R100-076..105)
2. What prior bundle outputs does B3 depend on? (B2 Slot Forge route classes, B2 Context Distillery)
3. What new contracts are needed? (ModelWorkPacket, Scale Ladder, Provider Seam, Small-Model Power, Hybrid Director)
4. What external surfaces are consumed? (Thor handoff protocol shape, Claude worker adapter pattern)
5. What must not be added? (provider execution, live model, app mutation, network calls)

Output: Analysis record with dependency map, new artifact list, forbidden scope.
Claim boundary: analysis_is_candidate_composition_guide_not_runtime_proof
```

---

## 2. Thor/Y Compose Prompt

**Purpose:** Dry-run composition of B3 work packets without execution.

```
Thor/Y Compose --dry-run — Odin B3

Input artifacts from prior bundles:
- B2 Slot Forge route classes → B3 Scale Ladder route classes
- B2 Context Capsule → B3 ModelWorkPacket context_capsule_ref
- B2 Gaptext → B3 ModelWorkPacket gaptext_ref
- B2 Worklet Graph nodes → B3 ModelWorkPacket slot_contract_ref

New B3 artifacts to compose:
- ModelWorkPacket (assembles slot, capsule, gaptext into routable work unit)
- Model Scale Ladder (routes work to smallest sufficient model class)
- Provider Seam (transport contract for eventual model execution)
- Small-Model Power modules (pipeline: distill → worklet → slot → gaptext → packet → route)
- Hybrid Director roles (router, compressor, writer, reviewer, critic, composer, final_gate_advisor)
- Claude Worker Adapter (formal contract for Claude Code as external worker)
- Thor Handoff Intake (static intake schema for Thor protocol references)

Compose strategy: static contract only, no execution, candidate_only: true on all outputs.
Claim boundary: composition_is_dry_run_candidate_plan_not_execution_proof
```

---

## 3. Thor/Y Handoff Prompt

**Purpose:** Dry-run handoff planning for B3 work to Claude Code worker.

```
Thor/Y Handoff --dry-run — Odin B3

Worker: Claude Code (external local worker)
Adapter contract: odin_claude_worker_adapter_example_b3_001

Handoff pack shape (from Thor HANDOFF_PACKS.md):
- README.md: orientation → PR_29_B3_THOR_COMPACT_HANDOFF_PROMPT.md
- HANDOFF.md: work order → this prompt
- PATCHPLAN.md: change plan → B3 artifact list
- GUARD.md: boundary contract → claim boundaries in all artifacts
- EXPECTED_OUTPUT.md: return shape → return_contract in worker adapter
- RETURN_CONTRACT.md: human return contract → return report template

Kernel binding:
- task: B3 ModelWorkPacket / Scale Ladder / Provider Seams / Small-Model Hybrid Director
- allowed_paths: schemas/, registries/, examples/v7_1_1/, tools/v7_1_1/, reports/, tests/, docs/codex/, SYSTEM_MAP.json, FILE_MANIFEST.json, registries/v7_1_1_actual_codex_bundle_plan.json
- forbidden_paths: odin/, runtime/, sdk/, odin_app_sdk/, .env, secrets
- stop_conditions: [need forbidden paths, need secrets, need scope expansion, provider SDK import required]
- claim_ceiling: candidate_patch

Non-claims:
- not correctness proof
- not runtime proof
- not provider execution proof
- not model quality proof
- not production readiness

Claim boundary: y_handoff_is_dry_run_candidate_handoff_plan_not_execution_proof
```

---

## 4. Thor/Y Review Prompt

**Purpose:** Review B3 candidate work against claim boundaries and contract requirements.

```
Thor/Y Review — Odin B3

Review checklist:
1. B3 maps exactly V711-R100-076..105 (30 slices, no more, no less)
2. B3 absorbs PR-31-MODELWORKPACKET-SCALE-LADDER and PR-32-SMALL-MODEL-HYBRID-DIRECTOR
3. B1 and B2 mappings preserved unchanged
4. Canonical ladder not rewritten
5. All schemas have required fields: claim_boundary, candidate_only, non_claims
6. All registries have required fields: registry_id, version, claim_boundary, candidate_only
7. All examples have required fields: claim_boundary, candidate_only, non_claims
8. ModelWorkPacket forbids: direct_apply, external_send, app_state_mutation, runtime_proof_claim, model_quality_proof_claim
9. Scale Ladder includes: deterministic_no_model, cannot_safely_complete; enforces smallest_sufficient
10. Provider Seam has: cannot_safely_complete class; no execution claims
11. No provider SDK imports (requests, httpx, openai, ollama) in B3 code files
12. Claude Worker Adapter forbids: direct_apply, app_state_mutation, claim_runtime_proof
13. Thor Handoff Intake not claimed as runtime bridge
14. B3 validator runs deterministically
15. B3 report has zero hard_violations
16. Tests 1-45 all pass
17. FILE_MANIFEST free of ignored generated artifacts

Claim findings:
- Any artifact lacking claim_boundary → HARD VIOLATION
- Any artifact claiming runtime proof → HARD VIOLATION
- Any provider SDK import → HARD VIOLATION

Required fixes: address all hard violations before merging.
Decision recommendation: merge only when hard_violations = [] and all tests pass.

Claim boundary: y_review_is_candidate_review_not_correctness_or_production_proof
```

---

## 5. Thor/Y Receipt Prompt

**Purpose:** Record receipt of reviewed B3 candidate work.

```
Thor/Y Receipt — Odin B3

Accepted claim refs:
- b3_maps_v711_r100_076_105: TRUE if exactly 30 slices mapped
- b3_absorbs_pr31_pr32: TRUE if both families present in bundle plan
- b1_b2_preserved: TRUE if B1/B2 bundle entries unchanged
- canonical_ladder_preserved: TRUE if ladder registry not modified
- modelworkpacket_schema_exists: TRUE if schema file present
- scale_ladder_schema_exists: TRUE if schema file present
- provider_seam_schema_exists: TRUE if schema file present
- small_model_power_schema_exists: TRUE if schema file present
- hybrid_director_schema_exists: TRUE if schema file present
- claude_worker_adapter_schema_exists: TRUE if schema file present
- thor_handoff_intake_schema_exists: TRUE if schema file present
- b3_validator_runs: TRUE if tool exits 0 with deterministic timestamp
- b3_report_zero_hard_violations: TRUE if hard_violations = []
- all_45_tests_pass: TRUE if pytest exit 0

Denied claim refs:
- runtime_completion: DENIED — B3 is static contract only
- provider_execution: DENIED — no provider SDK used
- live_model_inference: DENIED — no model called
- app_state_mutation: DENIED — no app mutation
- external_send: DENIED — no external send
- model_quality_proof: DENIED — no quality measurement
- production_readiness: DENIED — not production certified
- security_certification: DENIED — not security audited

Pending claim refs:
- actual_small_model_execution: PENDING until B5+ runtime layer
- actual_provider_integration: PENDING until B5+ runtime layer

Receipt does not accept, apply, or merge the work.
Claim boundary: y_receipt_is_bookkeeping_record_not_claim_acceptance_or_apply_authority
```

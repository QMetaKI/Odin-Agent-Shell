# PR-30 B4 Thor/Y Critic and Final Gate Prompts

**claim_boundary:** thor_y_prompts_are_external_candidate_handoff_guidance_not_runtime_proof
**thor_artifact_is_external_candidate_handoff_guidance_not_runtime_proof:** true

All prompts below are static candidate guidance. They do not execute models, do not call providers, do not mutate app state, and do not send externally.

---

## Thor/Y Analyze Prompt

```
thor y analyze "B4 Minicheck Critics Tournament Candidate DNA Response Packet Final Gate Advisory for Odin v7.1.1"

# Not available in Thor 4.1.1 without .thor/ workspace initialization.
# Manually applied discipline from docs/v3.5/ARTIFACT_SPECS.md.

Analyze target:
  - Scope: static candidate evaluation spine (minicheck → critic → tournament → DNA → artifact → response → final gate → receipt)
  - B3 consumption: ModelWorkPacket route_class → CriticWorkPacket critic_tier
  - Hard boundary: Final Gate Advisory is advisory-only, never Apply Gate
  - Negative contracts: no runtime, no provider, no app authority, no external send

Candidate-only: true
```

---

## Thor/Y Compose Prompt

```
thor y compose --dry-run "B4 Minicheck Critics Tournament Candidate DNA Response Packet Final Gate Advisory for Odin v7.1.1" --json

# Not available in Thor 4.1.1 without workspace. Manually applied.

Compose B4 artifacts in this order:
1. schemas (9 B4 + 1 report schema)
2. registries (9 B4 registries, update actual_codex_bundle_plan.json)
3. examples (9 B4 examples)
4. tools/v7_1_1/check_b4_minicheck_critics_final_gate.py
5. reports/v7_1_1_b4_minicheck_critics_final_gate_report.json
6. tests/test_v7_1_1_b4_minicheck_critics_final_gate.py
7. Thor intake docs (4 files in docs/codex/handoffs/)
8. Audit and return report
9. SYSTEM_MAP.json and FILE_MANIFEST.json updates
10. registries/v7_1_1_llm_work_audit_findings_registry.json updates

Each artifact: candidate_only=true, claim_boundary set, non_claims non-empty
```

---

## Thor/Y Handoff Prompt

```
thor y handoff --dry-run "B4 Minicheck Critics Tournament Candidate DNA Response Packet Final Gate Advisory for Odin v7.1.1" --json

# Manually applied.

Handoff surface:
  agent: claude-code
  task_label: Odin B4
  repo: QMetaKI/Odin-Agent-Shell
  branch: claude/pr-30-b4-minicheck-critics-final-gate-dq8dys
  base_commit: cbef841a56d8ddffa199a0e49b3411079c8d2afd
  
  THOR_HANDOFF.kernel_binding:
    - consumed_b3_artifacts: [modelworkpacket_contract, model_scale_ladder_registry, hybrid_director_registry]
    - produced_b4_artifacts: [minicheck, critic_work_packet, critic_cascade, tournament_selection, candidate_dna, candidate_artifact, response_packet, final_gate_advisory, receipt_boundary]
    - forbidden_actions: [direct_apply, external_send, app_state_mutation, provider_execution_without_policy, live_model_execution, final_gate_as_apply_gate]
    - candidate_only: true
```

---

## Thor/Y Review Prompt

```
thor y review "B4 Minicheck Critics Tournament ..."

# Manually applied.

Senior Reviewer simulation:
  - Verify Final Gate Advisory is correctly named "Advisory" not "Authority"
  - Verify is_apply_gate=false enforced as const in schema
  - Verify Receipt Boundary partitions accepted/denied/pending (not absolute truth)
  - Verify all 10 B3 route classes covered in critic route mapping
  - Verify critic tiers are static contract roles (no live model execution)
  - Verify B4 validator returns 0 hard violations
  - Verify all 62+ B4 tests pass
  - Verify validate-all passes
  - Verify no absolute local paths in report
  - Verify no provider SDK imports in B4 files

Senior Code Reviewer simulation:
  - All schemas use const:false for is_apply_gate, is_absolute_truth
  - All schemas use const:true for candidate_only
  - additionalProperties:true for forward compatibility
  - No circular dependencies between B4 artifacts
  - Validator writes only to --out path
  - Examples use odin_ prefixed IDs (no absolute paths)
```

---

## Thor/Y Receipt Prompt

```
thor y receipt "B4 Minicheck Critics Tournament ..."

# Manually applied.

THOR_RECEIPT mapping:
  accepted_claim_refs:
    - "B4 static candidate evaluation spine added"
    - "All B4 schemas/registries/examples created"
    - "B4 validator returns 0 hard violations"
    - "62+ B4 tests pass"
    - "validate-all passes"
    - "prior PR tests (25/26/B1/B2/B3) still pass"

  denied_claim_refs:
    - "not_runtime_completion"
    - "not_live_model_inference_proof"
    - "not_provider_execution_proof"
    - "not_model_quality_proof"
    - "not_production_readiness"
    - "not_final_gate_as_apply_gate"

  pending_claim_refs:
    - "B5 storage/trace/receipt integration"
    - "B5 local provider seam runtime"
    - "B7+ Thor-Odin bridge"
    - "Production readiness evaluation"
```

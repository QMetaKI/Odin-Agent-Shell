# PR-29 B3 Thor Compact Handoff Prompt

claim_boundary: compact_handoff_prompt_is_task_summary_not_runtime_proof

## Task

Implement Odin v7.1.1 Road-to-100 Bundle B3: ModelWorkPacket / Model Scale Ladder / Provider Seams / Small-Model Power / Hybrid Director.

This is a static contract/compiler-spine PR. No runtime, no provider execution, no live model.

## Branch

claude/pr-29-b3-modelworkpacket-scale-hybrid-jxvek1 from a0a4ee5f1a183e6c180af9e1a2b7e21315cb53c9

## Bundle Mapping

- B3: V711-R100-076..105 (30 slices)
- Absorbs: PR-31-MODELWORKPACKET-SCALE-LADDER, PR-32-SMALL-MODEL-HYBRID-DIRECTOR
- Status: static_contract_evidence_added_not_runtime_complete

## Allowed Scope

1. Update registries/v7_1_1_actual_codex_bundle_plan.json — update B3 status and fields
2. Create schemas: modelworkpacket, model_scale_ladder, provider_seam, small_model_power_contract, hybrid_director, odin_claude_worker_adapter, thor_handoff_intake, b3_report
3. Create registries: for each schema above
4. Create examples in examples/v7_1_1/: for each major contract
5. Create tools/v7_1_1/check_b3_modelworkpacket_scale_hybrid.py (static validator)
6. Create reports/v7_1_1_b3_modelworkpacket_scale_hybrid_report.json (generated report)
7. Create tests/test_v7_1_1_b3_modelworkpacket_scale_hybrid.py (45 tests)
8. Create docs/codex/handoffs/: intake, compact prompt, Y handoff prompts, protocol shape mapping
9. Create docs/codex/audits/PR_29_B3_THOR_ODIN_CLAUDE_CODE_AUDIT.md
10. Create docs/codex/reports/PR_29_B3_MODELWORKPACKET_SCALE_HYBRID_RETURN_REPORT.md
11. Update registries/v7_1_1_llm_work_audit_findings_registry.json with B3 findings
12. Update SYSTEM_MAP.json and FILE_MANIFEST.json

## Hard Guards

- NO provider SDK imports (requests, httpx, openai, ollama, llama_cpp)
- NO network calls
- NO live model execution
- NO app mutation
- NO external send
- candidate_only: true on all artifacts
- no_claims: not_runtime_proof, not_model_quality_proof, not_live_inference_proof

## External Reference

- Thor-Agent-Kit: https://github.com/QMetaKI/Thor-Agent-Kit
- SHA: e9af7a333e4bcb11f2461696e4ebbcde994b98b1
- Do not commit Thor files or .thor/ artifacts

## Return Contract

Return report must include:
- files_changed list
- commands_run with exit codes
- test results
- hard_violations: []
- senior reviewer simulation
- senior code reviewer simulation
- B4/B5/B7+ findings

## Claim Boundary

compact_handoff_prompt_is_task_summary_not_runtime_proof

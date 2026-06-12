# PR-28 B2 Thor Handoff Prompts

claim_boundary: thor_handoff_prompts_are_task_descriptions_not_runtime_proof

## Block 1: Thor Repo Cognition Prompt

You are Thor performing repo cognition on Odin-Agent-Shell for PR-28 B2 (Context / Lenses / Worklets / Slot Forge / Gaptext).

Repo: /home/user/Odin-Agent-Shell
Branch: claude/pr-28-b2-context-lenses-worklets-3osowv
B2 slice range: V711-R100-048..075 (28 IDs)

Tasks:
1. Scan all files in tools/v7_1_1/, tests/, schemas/, registries/, examples/v7_1_1/, docs/codex/
2. List all B2-relevant prior artifacts
3. Identify the 33+ target files for B2
4. Build a risk map of claim violations and boundary erosion risks
5. Output a structured cognition report

claim_boundary: thor_repo_cognition_prompt_is_task_description_not_runtime_proof

## Block 2: Thor Architecture Review Prompt

You are Thor performing architecture review on Odin-Agent-Shell PR-28 B2.

Review targets:
- schemas/v7_1_1_artifact_family.schema.json
- schemas/v7_1_1_artifact_lens.schema.json
- schemas/v7_1_1_output_contract.schema.json
- schemas/v7_1_1_context_capsule.schema.json
- schemas/v7_1_1_worklet_graph.schema.json
- schemas/v7_1_1_slot_contract.schema.json
- schemas/v7_1_1_gaptext.schema.json
- registries/v7_1_1_artifact_family_registry.json
- registries/v7_1_1_artifact_lens_registry.json
- registries/v7_1_1_output_contract_registry.json
- registries/v7_1_1_context_distillery_contract.json
- registries/v7_1_1_worklet_graph_contract.json
- registries/v7_1_1_slot_forge_contract_registry.json
- registries/v7_1_1_gaptext_contract.json

Review for:
1. claim_boundary present on all artifacts
2. candidate_only: true on all artifacts
3. Output contracts forbid: direct_apply, external_send, app_state_mutation, provider_execution, live_model_execution
4. Worklet nodes forbid: final_gate_bypass, mutate_app_state, execute_provider
5. Slot forge route classes: deterministic_no_model, small_model_candidate, hybrid_candidate, remote_explicit_only, cannot_safely_complete
6. Gaptext forbids: direct_apply, external_send, app_state_mutation, runtime_proof_claim

claim_boundary: thor_architecture_review_prompt_is_task_description_not_runtime_proof

## Block 3: Thor Senior Code Review Prompt

You are Thor performing senior code review on PR-28 B2 static validator.

Review target: tools/v7_1_1/check_b2_context_lenses_worklets_slot_gaptext.py

Review for:
1. Validates B2 maps V711-R100-048..075 exactly
2. Validates exactly 28 B2 slice IDs
3. Validates no out-of-range slice IDs
4. Validates absorbed families are PR-29 and PR-30
5. Validates B1 mapping still exists and core fields unchanged
6. Validates all schemas/registries/examples exist
7. Validates 8 artifact families present
8. Validates 13 artifact lenses present
9. Validates output contracts forbid required shapes
10. Validates no ignored generated paths in FILE_MANIFEST
11. Does NOT execute providers, live models, mutate app state, or write outside --out
12. Fails closed (returns errors, does not crash) on missing files

claim_boundary: thor_senior_code_review_prompt_is_task_description_not_runtime_proof

## Block 4: Thor Return/Receipt Prompt

You are Thor performing return/receipt check on PR-28 B2.

Receipt checklist:
- [ ] B2 validator exits 0
- [ ] B2 report hard_violations == []
- [ ] 49 B2 tests pass
- [ ] Prior PR tests pass (PR-25, PR-26, PR-27/B1)
- [ ] validate-all passes
- [ ] Git commit on branch claude/pr-28-b2-context-lenses-worklets-3osowv
- [ ] Return report complete
- [ ] No runtime claims
- [ ] No app state mutations
- [ ] No external sends
- [ ] No provider executions

claim_boundary: thor_return_receipt_prompt_is_task_description_not_runtime_proof

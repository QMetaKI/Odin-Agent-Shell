# PR-28 B2 Odin / Claude Work Packet

claim_boundary: b2_work_packet_is_claude_code_local_worker_not_odin_runtime

## Universal Work Reference

- universal_work_ref: "odin.v7_1_1.universal_work"
- binding_ref: "odin.v7_1_1.binding_contract"
- work_id: "PR-28-B2-CONTEXT-LENSES-WORKLETS-SLOT-GAPTEXT"
- work_version: "7.1.1"

## Semantic Bus Channels Used

- #odin.context
- #odin.lens
- #odin.worklet
- #odin.slot
- #odin.gaptext
- #odin.candidate
- #odin.trace

## Input Artifacts

- registries/v7_1_1_road_to_100_ladder.json
- registries/v7_1_1_actual_codex_bundle_plan.json
- registries/v7_1_1_claim_boundary_registry.json
- registries/v7_1_1_forbidden_claim_registry.json
- schemas/v7_1_1_app_manifest.schema.json
- schemas/v7_1_1_binding_contract.schema.json
- schemas/v7_1_1_universal_work.schema.json
- schemas/v7_1_1_semantic_bus_event.schema.json
- schemas/v7_1_1_b1_app_boundary_universal_work_qirc_spine_report.schema.json
- reports/v7_1_1_b1_app_boundary_universal_work_qirc_spine_report.json

## Transformation Verb

compile_semantic_work_contracts

## Output Contract

- contract_type: "candidate_only_static_contracts"
- candidate_only: true
- app_owned_apply: true
- app_owned_state: true
- app_owned_external_send: true

## Constraints

- No app state mutation
- No external send
- No provider execution
- No live model execution
- No QIRC server claims
- No production readiness claims
- No direct apply
- Fail closed on missing files
- Write only to --out path

## Privacy Class

internal_development

## Candidate Only

candidate_only: true

## Forbidden Actions

- app_state_apply
- external_send
- hidden_tool_execution
- provider_api_call_without_receipt
- claiming_proof_without_receipt
- domain_state_mutation
- live_model_execution
- qirc_server_claim

## Claim Boundary

b2_work_packet_is_claude_code_local_worker_not_odin_runtime

## Worker Profile

- worker: claude-code
- worker_mode: agent_operator
- agent_operator_profile: claude-code
- candidate_only: true
- app_owned_apply: true

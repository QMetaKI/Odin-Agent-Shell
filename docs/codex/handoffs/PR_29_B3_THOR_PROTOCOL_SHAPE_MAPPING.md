# PR-29 B3 Thor Protocol Shape Mapping

claim_boundary: protocol_shape_mapping_is_static_reference_not_runtime_proof

This document maps Thor protocol artifacts to Odin B3 requirements and implementation artifacts.

---

## 1. THOR_HANDOFF → Odin B3 Work Packet / Binding Refs

| Thor HANDOFF field | Odin B3 mapping |
|---|---|
| kernel_binding.task | B3 task: ModelWorkPacket / Scale Ladder / Provider Seams / Small-Model Hybrid Director |
| kernel_binding.allowed_paths | schemas/, registries/, examples/v7_1_1/, tools/v7_1_1/, reports/, tests/, docs/codex/, SYSTEM_MAP.json, FILE_MANIFEST.json |
| kernel_binding.forbidden_paths | odin/, runtime/, sdk/, odin_app_sdk/, .env, secrets/, provider_sdk |
| kernel_binding.stop_conditions | need forbidden paths; need secrets; need scope expansion; provider SDK import required |
| kernel_binding.expected_output | static contract schemas, registries, examples, validator, report, tests, handoff docs |
| kernel_binding.claim_boundary | b3_static_contract_only_not_runtime_proof |
| kernel_binding.return_contract | summary, files_changed, commands_run, tests_status, evidence_refs, known_gaps |
| HANDOFF.md content | PR_29_B3_THOR_COMPACT_HANDOFF_PROMPT.md |
| PATCHPLAN.md content | B3 artifact list in return report |
| GUARD.md content | claim_boundary and forbidden_actions in all B3 artifacts |
| EXPECTED_OUTPUT.md | return_contract in odin_claude_worker_adapter schema |
| RETURN_CONTRACT.md | return report RETURN_CONTRACT section |

---

## 2. THOR_RETURN → Odin PR Return Report Requirements

| Thor RETURN field | Odin B3 return report requirement |
|---|---|
| artifact_kind | odin_b3_modelworkpacket_scale_hybrid_return_report |
| version | 7.1.1 |
| summary | B3 adds ModelWorkPacket/Scale Ladder/Provider Seam/Small-Model/Hybrid Director static contracts |
| files_changed | complete list of all B3 added/modified files |
| commands_run | pip install, validator tool, pytest runs, validate-all |
| tests_status | passed / partial / not_run with explicit counts |
| evidence_refs | report JSON, test output receipts |
| known_gaps | deferred: runtime provider integration, actual small-model execution, Thor-Odin bridge |
| claims | candidate_only: true; no runtime/provider/model-quality claims |
| reviewer_notes | senior reviewer and senior code reviewer simulation |

---

## 3. THOR_REVIEW → Senior Reviewer + Senior Code Reviewer Simulations

| Thor REVIEW field | Odin B3 simulation mapping |
|---|---|
| claim_findings | list of artifacts reviewed for claim boundary compliance |
| required_fixes | list of violations requiring correction before acceptance |
| decision_recommendation | ready_for_merge or blocked_on_violations |
| reviewer_identity | Senior Reviewer (architecture/scope) + Senior Code Reviewer (code quality/safety) |

### Senior Reviewer checks (architecture/scope):
1. B3 scope is static contract only — no runtime behavior added
2. B3 bundle mapping correct: V711-R100-076..105, 30 slices, PR-31 + PR-32 absorbed
3. B1/B2 mappings preserved; canonical ladder not modified
4. Thor intake documented; no Thor files committed
5. Claude worker adapter formalizes the B2 audit finding
6. Thor handoff intake formalizes the B2 audit finding
7. Claim boundaries present and correct on all artifacts
8. No forbidden scope (provider SDK, network, live model, app mutation) introduced

### Senior Code Reviewer checks (code quality/safety):
1. B3 validator tool: no provider SDK imports; deterministic; writes only to --out
2. B3 tests: covers all 45 required test cases; negative tests present; no test weakening
3. Schema files: valid JSON; required fields present; correct $schema and $id
4. Registry files: valid JSON; registry_id, version, claim_boundary, candidate_only present
5. Example files: valid JSON; claim_boundary, candidate_only present
6. No absolute local paths in report
7. No .odin_runtime/, __pycache__, egg-info in FILE_MANIFEST
8. validate-all integration: read-only / in-memory only

---

## 4. THOR_RECEIPT → Final Audit and Non-Claim Receipt Model

| Thor RECEIPT field | Odin B3 receipt mapping |
|---|---|
| accepted_claim_refs | B3 slice mapping, schema existence, registry existence, example existence, validator runs, report zero violations, all tests pass |
| denied_claim_refs | runtime_completion, provider_execution, live_model_inference, app_state_mutation, external_send, model_quality_proof, production_readiness, security_certification |
| pending_claim_refs | actual_small_model_execution (B5+), actual_provider_integration (B5+), thor_odin_runtime_bridge (B7+) |
| receipt_authority | bookkeeping record only; does not accept, apply, or merge work |

### Non-Claim Inventory for B3

| non_claim_id | denial_reason |
|---|---|
| not_runtime_completion | B3 is static contract layer only |
| not_production_readiness | not production certified |
| not_release_certification | not release audited |
| not_security_certification | not security audited |
| not_target_host_proof | no target host deployment |
| not_live_model_inference_proof | no model called |
| not_model_quality_proof | no quality measurement |
| not_measured_small_model_improvement | no improvement measured |
| not_qirc_server_runtime_proof | no QIRC server implemented |
| not_provider_execution_proof | no provider SDK used |
| not_app_apply_authority | no app mutation |
| not_external_send_authority | no external send |

---

## Claim Boundary

protocol_shape_mapping_is_static_reference_not_runtime_proof

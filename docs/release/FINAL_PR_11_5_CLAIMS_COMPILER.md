# FINAL-PR-11.5: Claims Compiler v0

**Claim boundary:** claims_compiler_v0_compiles_safe_claims_from_evidence_not_certification
**candidate_only:** true

## What It Does

Claims Compiler v0 classifies claims and produces safe wording. It does NOT certify truth. It maps claims to evidence requirements and safe alternatives.

## Claim Classes

| Class | Description |
|-------|-------------|
| allowed_structural_claim | Claim about repo structure, validated |
| allowed_host_scoped_claim | Host-scoped local receipt claim |
| allowed_candidate_only_claim | Candidate-only claim, no app apply |
| downgrade_required | Claim requires downgrade to be safe |
| external_receipt_required | Requires external receipt |
| forbidden_release_claim | Forbidden release claim |
| forbidden_model_superiority_claim | Forbidden model superiority claim |
| forbidden_security_claim | Forbidden security claim |
| forbidden_production_claim | Forbidden production claim |

## Forbidden Claims

- production_readiness
- security_certification
- release_certification
- general_live_model_inference
- real_model_benchmark
- model_superiority
- provider_execution_by_default
- app_apply
- app_state_mutation
- external_send
- public_network
- hidden_agent_authority

## How FINAL-PR-13 Uses It

FINAL-PR-13 (Release Closure) will use Claims Compiler to validate all release claims before generating the release closure document. Claims Compiler v0 is the first version and is prepared here for use in PR13.

## Not Proven

- production_readiness
- security_certification
- release_certification
- real_model_benchmark
- model_superiority

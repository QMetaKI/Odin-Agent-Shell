"""Claims Compiler — claim type definitions.

Claim boundary: claims_compiler_v0_compiles_safe_claims_from_evidence_not_certification
candidate_only: true
"""
from __future__ import annotations

CLAIM_CLASSES: list[str] = [
    "allowed_structural_claim",
    "allowed_host_scoped_claim",
    "allowed_candidate_only_claim",
    "downgrade_required",
    "external_receipt_required",
    "forbidden_release_claim",
    "forbidden_model_superiority_claim",
    "forbidden_security_claim",
    "forbidden_production_claim",
]

# Maps claim_text_pattern -> reason (why it's forbidden)
FORBIDDEN_CLAIMS: dict[str, str] = {
    "production_readiness": "Odin does not certify production readiness; this requires external audit.",
    "security_certification": "Odin does not perform security certification; this requires external security review.",
    "release_certification": "Odin does not certify releases; this requires release authority outside repo.",
    "general_live_model_inference": "Odin does not claim live model inference without a host-scoped receipt.",
    "real_model_benchmark": "Odin does not perform real model benchmarks; route evaluation is structural only.",
    "model_superiority": "Odin does not claim model superiority; no benchmark evidence.",
    "provider_execution_by_default": "Provider execution is disabled by default; requires explicit flag.",
    "app_apply": "Odin does not apply app state; app owns all apply decisions.",
    "app_state_mutation": "Odin does not mutate app state; app owns all state.",
    "external_send": "Odin does not send external messages; app owns external send.",
    "public_network": "Odin does not use public network by default.",
    "hidden_agent_authority": "Odin does not grant hidden agent authority; all agent work is advisory.",
}

"""Claims Compiler Reports — release claims policy.

Claim boundary: claims_compiler_v0_compiles_safe_claims_from_evidence_not_certification
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "claims_compiler_v0_compiles_safe_claims_from_evidence_not_certification"

NOT_PROVEN = [
    "production_readiness",
    "live_model_inference",
    "app_state_mutation",
    "external_send_authority",
]


def build_release_claims_policy(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Build release claims policy."""
    from .claim_types import FORBIDDEN_CLAIMS, CLAIM_CLASSES

    forbidden_list = [
        {"pattern": k, "reason": v}
        for k, v in FORBIDDEN_CLAIMS.items()
    ]

    return {
        "artifact_kind": "odin_release_claims_policy",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "forbidden_claims": forbidden_list,
        "allowed_claim_classes": [
            c for c in CLAIM_CLASSES
            if not c.startswith("forbidden")
        ],
        "policy_summary": (
            "Odin claims compiler v0 classifies release claims. "
            "Allowed claims: structural evidence, host-scoped local receipts, candidate-only outputs. "
            "Forbidden claims: production readiness, security certification, release certification, "
            "live model inference without receipt, model superiority, app apply, app state mutation, "
            "external send, public network, hidden agent authority."
        ),
        "not_proven": NOT_PROVEN,
    }

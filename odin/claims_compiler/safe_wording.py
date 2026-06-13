"""Claims Compiler — safe wording lookup.

Claim boundary: claims_compiler_v0_compiles_safe_claims_from_evidence_not_certification
candidate_only: true
"""
from __future__ import annotations

_SAFE_WORDING_MAP: dict[str, str] = {
    "allowed_structural_claim": (
        "This claim is supported by structural evidence in the repo. "
        "It does not claim production readiness, security certification, or live model inference."
    ),
    "allowed_host_scoped_claim": (
        "This claim is supported by host-scoped local evidence. "
        "It does not generalize to other hosts or environments without re-execution."
    ),
    "allowed_candidate_only_claim": (
        "This claim describes a candidate-only output. "
        "Apps own all apply, state, and external-send decisions."
    ),
    "downgrade_required": (
        "This claim requires downgrading to a weaker form with explicit evidence class and not_proven list."
    ),
    "external_receipt_required": (
        "This claim cannot be satisfied by repo-local evidence alone. "
        "An external audit, benchmark, or certification receipt is required."
    ),
    "forbidden_release_claim": (
        "This claim is forbidden for release. "
        "It implies certification or authority that Odin does not hold."
    ),
    "forbidden_model_superiority_claim": (
        "This claim is forbidden. "
        "Odin does not claim model superiority or benchmark results."
    ),
    "forbidden_security_claim": (
        "This claim is forbidden. "
        "Odin does not perform security certification or security audits."
    ),
    "forbidden_production_claim": (
        "This claim is forbidden. "
        "Odin does not certify production readiness."
    ),
}


def get_safe_wording(claim_text: str, classification: str) -> str:
    """Return safe wording for the given classification."""
    return _SAFE_WORDING_MAP.get(
        classification,
        f"Claim classification '{classification}' has no registered safe wording. Review claim boundary.",
    )

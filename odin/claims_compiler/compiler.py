"""Claims Compiler — classify and compile safe claims.

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

_FORBIDDEN_PATTERN_TO_CLASS: dict[str, str] = {
    "production_readiness": "forbidden_production_claim",
    "security_certification": "forbidden_security_claim",
    "release_certification": "forbidden_release_claim",
    "general_live_model_inference": "forbidden_release_claim",
    "real_model_benchmark": "forbidden_model_superiority_claim",
    "model_superiority": "forbidden_model_superiority_claim",
    "provider_execution_by_default": "forbidden_release_claim",
    "app_apply": "forbidden_release_claim",
    "app_state_mutation": "forbidden_release_claim",
    "external_send": "forbidden_release_claim",
    "public_network": "forbidden_release_claim",
    "hidden_agent_authority": "forbidden_release_claim",
}

_EVIDENCE_CLASS_TO_ALLOWED: dict[str, str] = {
    "structural_evidence": "allowed_structural_claim",
    "host_scoped_local_receipt": "allowed_host_scoped_claim",
    "candidate_only": "allowed_candidate_only_claim",
    "target_only": "external_receipt_required",
    "doc_only": "downgrade_required",
    "external_receipt_required": "external_receipt_required",
}


def _detect_forbidden(claim_text: str) -> tuple[str | None, str | None]:
    """Detect forbidden pattern in claim text. Returns (pattern, class) or (None, None).

    Patterns appearing in negation context ("not X", "no X") are excluded.
    """
    lower = claim_text.lower()
    for pattern, cls in _FORBIDDEN_PATTERN_TO_CLASS.items():
        phrase = pattern.replace("_", " ")
        for token in (phrase, pattern):
            if token in lower:
                idx = lower.find(token)
                prefix = lower[max(0, idx - 5):idx]
                if "not " in prefix or "no " in prefix:
                    continue
                return pattern, cls
    return None, None


def classify_claim(
    claim_text: str,
    *,
    evidence_refs: list[str] | None = None,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Classify a claim and return safe wording."""
    from .claim_types import FORBIDDEN_CLAIMS
    from .safe_wording import get_safe_wording

    if evidence_refs is None:
        evidence_refs = []

    forbidden_pattern, forbidden_class = _detect_forbidden(claim_text)

    if forbidden_pattern:
        classification = forbidden_class
        allowed = False
        forbidden_reason = FORBIDDEN_CLAIMS.get(forbidden_pattern, f"Forbidden pattern: {forbidden_pattern}")
        evidence_class = "forbidden"
    else:
        classification = "allowed_candidate_only_claim"
        allowed = True
        forbidden_reason = None
        evidence_class = "structural_evidence" if evidence_refs else "candidate_only"

    safe_wording = get_safe_wording(claim_text, classification)

    return {
        "claim_text": claim_text,
        "classification": classification,
        "safe_wording": safe_wording,
        "required_evidence": evidence_refs,
        "evidence_class": evidence_class,
        "allowed": allowed,
        "forbidden_reason": forbidden_reason,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "not_proven": NOT_PROVEN,
    }


def compile_safe_claim(
    claim_text: str,
    *,
    evidence_class: str,
    evidence_refs: list[str],
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Compile a safe claim for use in docs."""
    from .safe_wording import get_safe_wording

    forbidden_pattern, forbidden_class = _detect_forbidden(claim_text)

    if forbidden_pattern:
        from .claim_types import FORBIDDEN_CLAIMS
        classification = forbidden_class
        allowed = False
        forbidden_reason = FORBIDDEN_CLAIMS.get(forbidden_pattern, f"Forbidden: {forbidden_pattern}")
    else:
        classification = _EVIDENCE_CLASS_TO_ALLOWED.get(evidence_class, "allowed_candidate_only_claim")
        allowed = True
        forbidden_reason = None

    safe_wording = get_safe_wording(claim_text, classification)

    return {
        "claim_text": claim_text,
        "classification": classification,
        "safe_wording": safe_wording,
        "required_evidence": evidence_refs,
        "evidence_class": evidence_class,
        "allowed": allowed,
        "forbidden_reason": forbidden_reason,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "not_proven": NOT_PROVEN,
    }

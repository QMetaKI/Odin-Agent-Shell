"""FINAL-PR-13: Donations Plan.

Claim boundary: donation_surface_documents_optional_donations_without_entitlement
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "donation_surface_documents_optional_donations_without_entitlement"

PAYPAL_ADDRESS = "QMetaKI@gmail.com"


def build_donations_plan(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    return {
        "artifact_kind": "odin_final_pr_13_donations_plan",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "paypal": PAYPAL_ADDRESS,
        "donations_optional": True,
        "no_support_obligation": True,
        "no_private_licensing_rights": True,
        "no_priority_guarantee": True,
        "no_governance_rights": True,
        "no_licensing_exception": True,
        "no_commercial_entitlement": True,
        "no_paid_support_promise": True,
        "no_feature_request_right": True,
        "not_tax_advice": True,
        "license": "GPL-2.0-only",
        "source": "adapted from Thor-Agent-Kit DONATIONS.md",
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    }

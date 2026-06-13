"""FINAL-PR-13: Donation Surface Reports.

Claim boundary: donation_surface_documents_optional_donations_without_entitlement
candidate_only: true
"""
from __future__ import annotations

from pathlib import Path

from .donations_plan import build_donations_plan, PAYPAL_ADDRESS

CLAIM_BOUNDARY = "donation_surface_documents_optional_donations_without_entitlement"


def build_donation_surface_report(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    plan = build_donations_plan(generated_at_utc=generated_at_utc)
    root = Path(__file__).resolve().parents[2]
    donations_path = root / "DONATIONS.md"
    donations_exists = donations_path.exists()
    paypal_present = False
    odin_reference_present = False
    optional_present = False
    if donations_exists:
        text = donations_path.read_text(encoding="utf-8")
        paypal_present = PAYPAL_ADDRESS in text
        odin_reference_present = "Odin" in text
        optional_present = "optional" in text.lower()
    return {
        "artifact_kind": "odin_final_pr_13_donation_surface_report",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "status": "ok" if donations_exists else "missing",
        "donations_exists": donations_exists,
        "paypal_present": paypal_present,
        "odin_reference_present": odin_reference_present,
        "optional_framing_present": optional_present,
        "plan": plan,
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    }

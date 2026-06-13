"""Evidence Closure Dry Run — Receipt Classifier.

Claim boundary: evidence_closure_dry_run_classifies_receipts_not_release_closure
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "evidence_closure_dry_run_classifies_receipts_not_release_closure"


def classify_evidence_receipt(
    receipt: dict,
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    keys = list(receipt.keys()) if isinstance(receipt, dict) else []
    if "structural_proof" in keys:
        evidence_class = "structural_evidence"
        basis = "receipt contains structural_proof key"
    elif "host_scoped" in keys or "local_receipt" in keys:
        evidence_class = "host_scoped_local_receipt"
        basis = "receipt contains host_scoped or local_receipt key"
    elif "external_required" in keys:
        evidence_class = "external_receipt_required"
        basis = "receipt contains external_required key"
    elif "historical" in keys:
        evidence_class = "historical_evidence"
        basis = "receipt contains historical key"
    else:
        evidence_class = "not_evidence"
        basis = "receipt does not match any known evidence key pattern"
    return {
        "artifact_kind": "odin_evidence_receipt_classification",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "input_receipt_keys": keys,
        "evidence_class": evidence_class,
        "classification_basis": basis,
        "not_proven": ["release_closure", "production_readiness"],
    }

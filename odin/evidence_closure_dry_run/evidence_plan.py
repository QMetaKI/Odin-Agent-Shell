"""Evidence Closure Dry Run — Evidence Plan.

Claim boundary: evidence_closure_dry_run_classifies_receipts_not_release_closure
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "evidence_closure_dry_run_classifies_receipts_not_release_closure"

EVIDENCE_CLASSES = [
    "structural_evidence",
    "host_scoped_local_receipt",
    "external_receipt_required",
    "historical_evidence",
    "not_evidence",
]

_CLAIMS = [
    {"claim_id": "candidate_only_architecture", "claim_text": "Odin outputs are candidate-only", "required_evidence_class": "structural_evidence"},
    {"claim_id": "app_owned_apply", "claim_text": "App owns all apply decisions", "required_evidence_class": "structural_evidence"},
    {"claim_id": "local_provider_receipt", "claim_text": "Local provider receipt harness is host-scoped", "required_evidence_class": "host_scoped_local_receipt"},
    {"claim_id": "host_scoped_boundary", "claim_text": "Receipt boundary separates host-scoped from WAN/LAN", "required_evidence_class": "structural_evidence"},
    {"claim_id": "semantic_kernel_closed", "claim_text": "Semantic kernel IR is structurally defined", "required_evidence_class": "structural_evidence"},
    {"claim_id": "v711_coverage_closed", "claim_text": "V711 coverage items are mapped to repo evidence", "required_evidence_class": "structural_evidence"},
    {"claim_id": "command_surface_indexed", "claim_text": "CLI command surface is indexed", "required_evidence_class": "structural_evidence"},
    {"claim_id": "docs_readiness_indexed", "claim_text": "Docs readiness index is built", "required_evidence_class": "structural_evidence"},
    {"claim_id": "packaging_boundary_inventoried", "claim_text": "Packaging boundary inventory exists", "required_evidence_class": "structural_evidence"},
    {"claim_id": "release_certification", "claim_text": "Release is certified for distribution", "required_evidence_class": "external_receipt_required"},
    {"claim_id": "production_readiness", "claim_text": "System is production-ready", "required_evidence_class": "external_receipt_required"},
    {"claim_id": "security_certification", "claim_text": "System is security-certified", "required_evidence_class": "external_receipt_required"},
    {"claim_id": "model_performance", "claim_text": "Model performance meets benchmark", "required_evidence_class": "external_receipt_required"},
]


def build_evidence_closure_plan(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    return {
        "artifact_kind": "odin_evidence_closure_dry_run_plan",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "evidence_classes": EVIDENCE_CLASSES,
        "claims": _CLAIMS,
        "not_proven": ["release_closure", "production_readiness", "security_certification", "release_certification", "final_pr_13_release_closure"],
    }

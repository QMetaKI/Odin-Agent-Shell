"""Route evaluation report builder — FINAL-PR-11."""
from __future__ import annotations

from odin.route_evaluation.fixtures import CLAIM_BOUNDARY, _NOT_PROVEN


def build_route_evaluation_report(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Build a structural report on the route evaluation receipt harness."""
    return {
        "artifact_kind": "odin_route_evaluation_report",
        "candidate_only": True,
        "local_only": True,
        "app_owned_apply": True,
        "evidence_class": "structural_evidence",
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": list(_NOT_PROVEN),
        "not_a_model_quality_benchmark": True,
        "no_superiority_claim": True,
        "evaluation_dimensions": [
            "schema_valid",
            "candidate_only_valid",
            "forbidden_actions_clean",
            "slot_completeness",
            "not_proven_present",
            "receipt_present",
            "boundary_violations",
            "output_length_chars",
        ],
        "fixture_routes": [
            "deterministic_no_model",
            "3b_primary",
            "7b_primary",
            "3b_7b_hybrid",
        ],
        "generated_at_utc": generated_at_utc,
    }

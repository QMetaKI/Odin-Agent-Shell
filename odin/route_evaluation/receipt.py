"""Route evaluation receipt — FINAL-PR-11."""
from __future__ import annotations

from odin.route_evaluation.evaluator import evaluate_route_candidate
from odin.route_evaluation.fixtures import CLAIM_BOUNDARY, _NOT_PROVEN, build_route_eval_fixtures


def run_route_evaluation_receipt(
    *,
    allow_local_provider_execution: bool = False,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Run route evaluation on all fixtures and return a receipt.

    NOT a model quality benchmark. NOT a superiority claim.
    Execution remains disabled unless explicitly enabled (not used in evaluation).
    """
    fixtures = build_route_eval_fixtures()
    results = []
    for fixture in fixtures:
        route_name = fixture.get("route_name", "unknown")
        result = evaluate_route_candidate(route_name, fixture, generated_at_utc=generated_at_utc)
        results.append(result)

    all_pass = all(r.get("overall_pass") for r in results)
    total_violations = sum(r.get("dimensions", {}).get("boundary_violations", 0) for r in results)

    return {
        "artifact_kind": "odin_route_evaluation_receipt",
        "candidate_only": True,
        "local_only": True,
        "app_owned_apply": True,
        "app_apply": False,
        "external_send": False,
        "public_network": False,
        "not_a_model_quality_benchmark": True,
        "no_superiority_claim": True,
        "evidence_class": "structural_evidence",
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": list(_NOT_PROVEN),
        "routes_evaluated": len(results),
        "all_pass": all_pass,
        "total_boundary_violations": total_violations,
        "route_results": results,
        "generated_at_utc": generated_at_utc,
        "evaluation_note": (
            "Route evaluation measures structural validity and boundary cleanliness. "
            "It does not measure model quality, performance, or production readiness."
        ),
    }

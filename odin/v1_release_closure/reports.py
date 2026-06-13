"""FINAL-PR-13: v1.0 Release Closure Reports.

Claim boundary: v1_release_closure_closes_local_candidate_release_not_external_release
candidate_only: true
"""
from __future__ import annotations

from .closure_matrix import build_v1_release_closure_matrix
from .release_truth import build_v1_release_truth
from .proof_packet import build_v1_release_closure_proof_packet

CLAIM_BOUNDARY = "v1_release_closure_closes_local_candidate_release_not_external_release"


def build_v1_release_closure_report(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    matrix = build_v1_release_closure_matrix(generated_at_utc=generated_at_utc)
    truth = build_v1_release_truth(generated_at_utc=generated_at_utc)
    proof = build_v1_release_closure_proof_packet(generated_at_utc=generated_at_utc)
    return {
        "artifact_kind": "odin_final_pr_13_v1_release_closure_report",
        "candidate_only": True,
        "app_owned_apply": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "status": "ok",
        "local_candidate_release_closed": True,
        "external_release_claimed": False,
        "matrix_row_count": len(matrix.get("matrix", [])),
        "release_truth": truth,
        "proof_packet": proof,
        "not_proven": proof["not_proven"],
    }

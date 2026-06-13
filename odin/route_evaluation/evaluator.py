"""Route candidate evaluator — FINAL-PR-11.

Measures structure, boundary cleanliness, receipt completeness.
NOT model quality benchmark. NOT superiority claim.
"""
from __future__ import annotations

import hashlib
import json

from odin.route_evaluation.fixtures import CLAIM_BOUNDARY, _NOT_PROVEN

_REQUIRED_FIELDS = [
    "candidate_only",
    "claim_boundary",
    "not_proven",
    "app_apply",
    "external_send",
]


def _sha256_id(prefix: str, payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    h = hashlib.sha256(raw.encode()).hexdigest()[:16]
    return f"{prefix}{h}"


def evaluate_route_candidate(
    route_name: str,
    candidate: dict,
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Evaluate a route candidate for structural validity.

    Returns evaluation dict. NOT a model quality benchmark.
    NOT a superiority claim.
    """
    eval_id = _sha256_id(
        "route_eval_",
        {"route_name": route_name, "ts": generated_at_utc},
    )

    dimensions: dict[str, bool | int] = {}
    boundary_violations: list[str] = []

    # schema_valid: required fields present
    schema_valid = all(f in candidate for f in _REQUIRED_FIELDS)
    dimensions["schema_valid"] = schema_valid
    if not schema_valid:
        missing = [f for f in _REQUIRED_FIELDS if f not in candidate]
        boundary_violations.append(f"missing_required_fields: {missing}")

    # candidate_only_valid
    dimensions["candidate_only_valid"] = candidate.get("candidate_only") is True
    if not dimensions["candidate_only_valid"]:
        boundary_violations.append("candidate_only_not_true")

    # forbidden_actions_clean
    forbidden_clean = (
        candidate.get("app_apply") is not True
        and candidate.get("external_send") is not True
        and candidate.get("public_network") is not True
    )
    dimensions["forbidden_actions_clean"] = forbidden_clean
    if not forbidden_clean:
        boundary_violations.append("forbidden_action_flag_true")

    # slot_completeness
    slot = candidate.get("slot_contract")
    slot_complete = isinstance(slot, dict) and "slot_class" in slot
    dimensions["slot_completeness"] = slot_complete

    # not_proven_present
    not_proven = candidate.get("not_proven")
    dimensions["not_proven_present"] = isinstance(not_proven, list) and len(not_proven) > 0
    if not dimensions["not_proven_present"]:
        boundary_violations.append("not_proven_missing_or_empty")

    # receipt_present
    dimensions["receipt_present"] = bool(candidate.get("evidence_class"))

    # boundary_violations count
    dimensions["boundary_violations"] = len(boundary_violations)

    # output_length_chars (of claim_boundary as proxy for output size)
    cb = candidate.get("claim_boundary", "")
    dimensions["output_length_chars"] = len(str(cb))

    all_pass = (
        schema_valid
        and dimensions["candidate_only_valid"]
        and forbidden_clean
        and dimensions["not_proven_present"]
    )

    return {
        "artifact_kind": "odin_route_evaluation_result",
        "eval_id": eval_id,
        "route_name": route_name,
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
        "dimensions": dimensions,
        "boundary_violations": boundary_violations,
        "overall_pass": all_pass,
        "generated_at_utc": generated_at_utc,
    }

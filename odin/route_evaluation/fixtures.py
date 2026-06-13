"""Route evaluation fixtures — FINAL-PR-11."""
from __future__ import annotations

CLAIM_BOUNDARY = "route_evaluation_receipts_measure_structure_not_model_quality_benchmark"

_NOT_PROVEN = [
    "production_readiness",
    "security_certification",
    "release_certification",
    "real_model_benchmark",
    "model_quality_superiority",
    "app_apply",
    "external_send",
    "public_network",
]

_ROUTE_FIXTURES = [
    {
        "route_name": "deterministic_no_model",
        "candidate_only": True,
        "claim_boundary": "deterministic_no_model_route_structural_only",
        "not_proven": list(_NOT_PROVEN),
        "slot_contract": {"slot_class": "deterministic", "requires_model": False},
        "output_contract": {"candidate_only": True, "app_owned_apply": True},
        "app_apply": False,
        "external_send": False,
        "public_network": False,
        "requires_model": False,
        "evidence_class": "structural_evidence",
        "artifact_kind": "odin_route_eval_fixture",
    },
    {
        "route_name": "3b_primary",
        "candidate_only": True,
        "claim_boundary": "3b_primary_route_structural_only",
        "not_proven": list(_NOT_PROVEN),
        "slot_contract": {"slot_class": "3b", "requires_model": True, "model_scale": "3b"},
        "output_contract": {"candidate_only": True, "app_owned_apply": True},
        "app_apply": False,
        "external_send": False,
        "public_network": False,
        "requires_model": True,
        "evidence_class": "structural_evidence",
        "artifact_kind": "odin_route_eval_fixture",
    },
    {
        "route_name": "7b_primary",
        "candidate_only": True,
        "claim_boundary": "7b_primary_route_structural_only",
        "not_proven": list(_NOT_PROVEN),
        "slot_contract": {"slot_class": "7b", "requires_model": True, "model_scale": "7b"},
        "output_contract": {"candidate_only": True, "app_owned_apply": True},
        "app_apply": False,
        "external_send": False,
        "public_network": False,
        "requires_model": True,
        "evidence_class": "structural_evidence",
        "artifact_kind": "odin_route_eval_fixture",
    },
    {
        "route_name": "3b_7b_hybrid",
        "candidate_only": True,
        "claim_boundary": "3b_7b_hybrid_route_structural_only",
        "not_proven": list(_NOT_PROVEN),
        "slot_contract": {"slot_class": "hybrid", "requires_model": True, "model_scale": "3b_7b_hybrid"},
        "output_contract": {"candidate_only": True, "app_owned_apply": True},
        "app_apply": False,
        "external_send": False,
        "public_network": False,
        "requires_model": True,
        "evidence_class": "structural_evidence",
        "artifact_kind": "odin_route_eval_fixture",
    },
]


def build_route_eval_fixtures() -> list[dict]:
    """Return deterministic route evaluation fixtures."""
    return list(_ROUTE_FIXTURES)

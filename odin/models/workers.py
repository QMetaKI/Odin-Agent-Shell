from __future__ import annotations
from odin.runtime.ids import stable_id
from odin.models.permissions import build_permission_card


def build_worker_card(worker_id: str, worker_type: str = "mock_local") -> dict:
    permission_card = build_permission_card(worker_id, worker_type)
    return {
        "artifact_kind": "odin_model_worker_card",
        "protocol_version": "7.1",
        "worker_id": worker_id,
        "worker_type": worker_type,
        "allowed_roles": permission_card["allowed_roles"],
        "forbidden_roles": permission_card["forbidden_roles"],
        "may_apply": False,
        "may_send_external": False,
        "may_mutate_app_state": False,
        "may_issue_receipt": False,
        "may_accept_claim": False,
        "may_call_tools": False,
        "allowed_outputs": permission_card["allowed_outputs"],
        "forbidden_outputs": permission_card["forbidden_outputs"],
        "permission_card": permission_card,
        "candidate_only": True,
        "claim_boundary": "model_workers_project_candidates_only",
    }


def mock_generate(worker_card: dict, work: dict, atom_execution: dict, route: str) -> dict:
    return {
        "artifact_kind": "odin_mock_model_projection",
        "protocol_version": "7.1",
        "projection_id": stable_id("PROJ", {"worker": worker_card.get("worker_id"), "work": work.get("work_id")}, 12),
        "route": route,
        "worker_id": worker_card.get("worker_id"),
        "summary": f"Candidate projection for {work.get('work_id')} using {route}",
        "work_atom_result_count": len(atom_execution.get("results", [])),
        "candidate_only": True,
        "may_apply": False,
        "may_send_external": False,
        "may_mutate_app_state": False,
        "may_accept_claim": False,
        "may_issue_receipt": False,
        "model_inference_verified": False,
        "claim_boundary": "mock_projection_is_not_live_model_inference",
    }

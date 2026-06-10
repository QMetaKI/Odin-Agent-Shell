from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

FORBIDDEN_WORKER_ROLES = [
    "app_authority",
    "apply_executor",
    "claim_acceptor",
    "receipt_issuer",
    "external_sender",
    "state_mutator",
]

ALLOWED_OUTPUTS = ["candidate_artifact", "provider_result", "review_note", "route_note"]
FORBIDDEN_OUTPUTS = ["applied_patch", "external_send", "app_state_write", "production_receipt"]


@dataclass(frozen=True)
class WorkerPermissionCard:
    worker_id: str
    worker_class: str = "deterministic_candidate_worker"
    may_apply: bool = False
    may_send_external: bool = False
    may_mutate_app_state: bool = False
    may_issue_receipt: bool = False
    may_accept_claim: bool = False
    may_call_tools: bool = False
    allowed_outputs: list[str] = field(default_factory=lambda: list(ALLOWED_OUTPUTS))
    forbidden_outputs: list[str] = field(default_factory=lambda: list(FORBIDDEN_OUTPUTS))
    allowed_roles: list[str] = field(default_factory=lambda: ["candidate_worker", "projection_worker", "review_worker"])
    forbidden_roles: list[str] = field(default_factory=lambda: list(FORBIDDEN_WORKER_ROLES))
    claim_boundary: str = "worker_permission_card_candidate_only_no_app_authority"

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_kind": "odin_model_worker_permission_card",
            "protocol_version": "7.1",
            "worker_id": self.worker_id,
            "worker_class": self.worker_class,
            "may_apply": self.may_apply,
            "may_send_external": self.may_send_external,
            "may_mutate_app_state": self.may_mutate_app_state,
            "may_issue_receipt": self.may_issue_receipt,
            "may_accept_claim": self.may_accept_claim,
            "may_call_tools": self.may_call_tools,
            "allowed_outputs": list(self.allowed_outputs),
            "forbidden_outputs": list(self.forbidden_outputs),
            "allowed_roles": list(self.allowed_roles),
            "forbidden_roles": list(self.forbidden_roles),
            "candidate_only": True,
            "claim_boundary": self.claim_boundary,
        }


def build_permission_card(worker_id: str, worker_class: str = "deterministic_candidate_worker") -> dict[str, Any]:
    return WorkerPermissionCard(worker_id=worker_id, worker_class=worker_class).to_dict()


def check_permission_escalation(card: dict[str, Any], requested: dict[str, Any] | None = None) -> dict[str, Any]:
    requested = requested or {}
    blocked: list[str] = []
    boolean_gates = [
        "may_apply",
        "may_send_external",
        "may_mutate_app_state",
        "may_issue_receipt",
        "may_accept_claim",
        "may_call_tools",
    ]
    for gate in boolean_gates:
        if requested.get(gate) is True and card.get(gate) is not True:
            blocked.append(gate)
    for role in requested.get("roles", []):
        if role in card.get("forbidden_roles", []):
            blocked.append(f"role:{role}")
    for output in requested.get("outputs", []):
        if output in card.get("forbidden_outputs", []) or output not in card.get("allowed_outputs", []):
            blocked.append(f"output:{output}")
    return {
        "artifact_kind": "odin_worker_permission_decision",
        "status": "blocked" if blocked else "allowed",
        "blocked_reasons": blocked,
        "candidate_only": True,
        "claim_boundary": "permission_escalation_fails_closed_no_app_authority",
    }


def assert_no_permission_escalation(card: dict[str, Any], requested: dict[str, Any] | None = None) -> None:
    decision = check_permission_escalation(card, requested)
    if decision["status"] == "blocked":
        raise PermissionError("worker permission escalation blocked: " + ", ".join(decision["blocked_reasons"]))

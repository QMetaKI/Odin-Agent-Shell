from __future__ import annotations
from dataclasses import dataclass
from odin.runtime.ids import stable_id

FORBIDDEN_PROVIDER_ROLES = [
    "app_authority",
    "apply_executor",
    "claim_acceptor",
    "receipt_issuer",
    "external_sender",
    "state_mutator",
]
ALLOWED_PROVIDER_OUTPUTS = ["candidate_artifact", "provider_result", "review_note", "route_note"]
FORBIDDEN_PROVIDER_OUTPUTS = ["applied_patch", "external_send", "app_state_write", "production_receipt"]


@dataclass(frozen=True)
class ProviderResult:
    provider_id: str
    route: str
    text: str
    model_inference_verified: bool = False
    result_kind: str = "deterministic_no_model_output"
    status: str = "ok"
    claim_boundary: str = "provider_result_is_candidate_projection_not_authority"

    def to_dict(self) -> dict:
        projection_id = stable_id(
            "PROVIDERPROJ",
            {"provider": self.provider_id, "route": self.route, "text": self.text, "result_kind": self.result_kind, "status": self.status},
            12,
        )
        return {
            "artifact_kind": "odin_provider_result",
            "protocol_version": "7.1",
            "provider_id": self.provider_id,
            "projection_id": projection_id,
            "route": self.route,
            "text": self.text,
            "status": self.status,
            "result_kind": self.result_kind,
            "candidate_only": True,
            "app_owned_apply": True,
            "may_apply": False,
            "may_mutate_app_state": False,
            "may_send_external": False,
            "may_accept_claim": False,
            "may_issue_receipt": False,
            "model_inference_verified": self.model_inference_verified,
            "truth_claim": False,
            "claim_boundary": self.claim_boundary,
        }

class BaseProvider:
    provider_id = "base"
    provider_kind = "base"
    external_network = False
    enabled_by_default = False
    configured = False
    live_inference_supported = False
    live_inference_verified = False
    result_kind = "deterministic_no_model_output"

    def generate(self, prompt: str, *, route: str = "deterministic_no_model", context: dict | None = None) -> ProviderResult:
        raise NotImplementedError

    def capability_card(self) -> dict:
        return {
            "artifact_kind": "odin_provider_capability_card",
            "protocol_version": "7.1",
            "provider_id": self.provider_id,
            "provider_kind": self.provider_kind,
            "external_network": self.external_network,
            "enabled_by_default": self.enabled_by_default,
            "configured": self.configured,
            "live_inference_supported": self.live_inference_supported,
            "live_inference_verified": self.live_inference_verified,
            "allowed_role": "candidate_worker",
            "allowed_roles": ["candidate_worker", "projection_worker"],
            "forbidden_roles": list(FORBIDDEN_PROVIDER_ROLES),
            "allowed_outputs": list(ALLOWED_PROVIDER_OUTPUTS),
            "forbidden_outputs": list(FORBIDDEN_PROVIDER_OUTPUTS),
            "candidate_only": True,
            "may_apply": False,
            "may_mutate_app_state": False,
            "may_send_external": False,
            "may_accept_claim": False,
            "may_issue_receipt": False,
            "claim_boundary": "provider_card_declares_candidate_worker_boundary_not_live_provider_proof",
        }

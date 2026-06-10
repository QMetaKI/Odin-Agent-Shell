from __future__ import annotations
from dataclasses import dataclass
from odin.runtime.ids import stable_id

@dataclass(frozen=True)
class ProviderResult:
    provider_id: str
    route: str
    text: str
    model_inference_verified: bool = False

    def to_dict(self) -> dict:
        return {
            "artifact_kind": "odin_provider_result",
            "protocol_version": "7.1",
            "provider_id": self.provider_id,
            "projection_id": stable_id("PROVIDERPROJ", {"provider": self.provider_id, "route": self.route, "text": self.text}, 12),
            "route": self.route,
            "text": self.text,
            "candidate_only": True,
            "model_inference_verified": self.model_inference_verified,
            "claim_boundary": "provider_result_is_candidate_projection_not_authority",
        }

class BaseProvider:
    provider_id = "base"
    external_network = False

    def generate(self, prompt: str, *, route: str = "deterministic_no_model", context: dict | None = None) -> ProviderResult:
        raise NotImplementedError

    def capability_card(self) -> dict:
        return {
            "artifact_kind": "odin_provider_capability_card",
            "provider_id": self.provider_id,
            "external_network": self.external_network,
            "allowed_role": "candidate_worker",
            "forbidden_roles": ["app_authority", "apply_executor", "claim_acceptor"],
            "claim_boundary": "provider_card_declares_boundary_not_live_provider_proof",
        }

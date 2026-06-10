from __future__ import annotations
from .base import BaseProvider, ProviderResult

class NullProvider(BaseProvider):
    provider_id = "null_provider"
    provider_kind = "deterministic"
    enabled_by_default = True
    configured = True
    result_kind = "deterministic_no_model_output"
    def generate(self, prompt: str, *, route: str = "deterministic_no_model", context: dict | None = None) -> ProviderResult:
        return ProviderResult(self.provider_id, route, "", result_kind=self.result_kind)

class EchoProvider(BaseProvider):
    provider_id = "echo_provider"
    provider_kind = "deterministic"
    enabled_by_default = True
    configured = True
    result_kind = "deterministic_no_model_output"
    def generate(self, prompt: str, *, route: str = "deterministic_no_model", context: dict | None = None) -> ProviderResult:
        return ProviderResult(self.provider_id, route, f"echo:{prompt[:400]}", result_kind=self.result_kind)

class MockProvider(BaseProvider):
    provider_id = "mock_provider"
    provider_kind = "mock"
    enabled_by_default = True
    configured = True
    live_inference_supported = False
    live_inference_verified = False
    result_kind = "mock_output"
    def generate(self, prompt: str, *, route: str = "3b_7b_8b_hybrid", context: dict | None = None) -> ProviderResult:
        atom_count = len((context or {}).get("atom_results", []))
        return ProviderResult(
            self.provider_id,
            route,
            f"mock candidate projection for route={route}; atom_count={atom_count}",
            model_inference_verified=False,
            result_kind=self.result_kind,
            claim_boundary="mock_provider_result_is_candidate_projection_not_live_inference_or_truth",
        )

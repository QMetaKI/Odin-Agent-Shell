from __future__ import annotations
from .base import BaseProvider, ProviderResult

class StubProvider(BaseProvider):
    provider_id = "stub_provider"
    provider_kind = "disabled_adapter_stub"
    external_network = False
    enabled_by_default = False
    configured = False
    live_inference_supported = False
    live_inference_verified = False
    result_kind = "stub_output"

    def generate(self, prompt: str, *, route: str = "remote_optional_explicit", context: dict | None = None) -> ProviderResult:
        return ProviderResult(
            self.provider_id,
            route,
            f"{self.provider_id} is disabled by default; no live inference, network call, credential use, download, or process spawn occurred.",
            model_inference_verified=False,
            result_kind=self.result_kind,
            status="disabled",
            claim_boundary="provider_adapter_is_disabled_stub_not_live_inference",
        )

class OllamaProviderStub(StubProvider):
    provider_id = "ollama_provider_stub"
    provider_kind = "local_disabled_adapter_stub"

class LlamaCppProviderStub(StubProvider):
    provider_id = "llamacpp_provider_stub"
    provider_kind = "local_disabled_adapter_stub"

class OpenAICompatibleProviderStub(StubProvider):
    provider_id = "openai_compatible_provider_stub"
    provider_kind = "remote_disabled_adapter_stub"
    external_network = True

class ClaudeCompatibleProviderStub(StubProvider):
    provider_id = "claude_compatible_provider_stub"
    provider_kind = "remote_disabled_adapter_stub"
    external_network = True

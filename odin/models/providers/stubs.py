from __future__ import annotations
from .base import BaseProvider, ProviderResult

class StubProvider(BaseProvider):
    provider_id = "stub_provider"
    external_network = False
    configured = False

    def generate(self, prompt: str, *, route: str = "remote_optional_explicit", context: dict | None = None) -> ProviderResult:
        return ProviderResult(
            self.provider_id,
            route,
            f"{self.provider_id} is a boundary stub. Wire a real provider in Codex/host proof stage.",
            model_inference_verified=False,
        )

class OllamaProviderStub(StubProvider):
    provider_id = "ollama_provider_stub"

class LlamaCppProviderStub(StubProvider):
    provider_id = "llamacpp_provider_stub"

class OpenAICompatibleProviderStub(StubProvider):
    provider_id = "openai_compatible_provider_stub"
    external_network = True

class ClaudeCompatibleProviderStub(StubProvider):
    provider_id = "claude_compatible_provider_stub"
    external_network = True

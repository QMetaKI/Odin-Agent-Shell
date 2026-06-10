from __future__ import annotations
from .base import BaseProvider, ProviderResult

class NullProvider(BaseProvider):
    provider_id = "null_provider"
    def generate(self, prompt: str, *, route: str = "deterministic_no_model", context: dict | None = None) -> ProviderResult:
        return ProviderResult(self.provider_id, route, "")

class EchoProvider(BaseProvider):
    provider_id = "echo_provider"
    def generate(self, prompt: str, *, route: str = "deterministic_no_model", context: dict | None = None) -> ProviderResult:
        return ProviderResult(self.provider_id, route, f"echo:{prompt[:400]}")

class MockProvider(BaseProvider):
    provider_id = "mock_provider"
    def generate(self, prompt: str, *, route: str = "3b_7b_8b_hybrid", context: dict | None = None) -> ProviderResult:
        atom_count = len((context or {}).get("atom_results", []))
        return ProviderResult(self.provider_id, route, f"mock candidate projection for route={route}; atom_count={atom_count}")

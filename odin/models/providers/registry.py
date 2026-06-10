from __future__ import annotations
from .mock import NullProvider, EchoProvider, MockProvider
from .stubs import OllamaProviderStub, LlamaCppProviderStub, OpenAICompatibleProviderStub, ClaudeCompatibleProviderStub

PROVIDERS = {
    "null": NullProvider,
    "echo": EchoProvider,
    "mock": MockProvider,
    "ollama_stub": OllamaProviderStub,
    "llamacpp_stub": LlamaCppProviderStub,
    "openai_compatible_stub": OpenAICompatibleProviderStub,
    "claude_compatible_stub": ClaudeCompatibleProviderStub,
}

def list_provider_cards() -> list[dict]:
    return [cls().capability_card() for cls in PROVIDERS.values()]

def get_provider(name: str):
    if name not in PROVIDERS:
        raise KeyError(f"unknown provider: {name}")
    return PROVIDERS[name]()

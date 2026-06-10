from __future__ import annotations

from pathlib import Path
from typing import Any
import json

from .redaction import redact_secrets


def load_provider_config(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as f:
        data = json.load(f)
    errors = validate_provider_config(data)
    if errors:
        raise ValueError("provider config invalid: " + "; ".join(errors))
    return data


def validate_provider_config(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if config.get("artifact_kind") != "odin_provider_config":
        errors.append("artifact_kind must be odin_provider_config")
    for provider in config.get("providers", []):
        pid = provider.get("provider_id", "unknown")
        if provider.get("enabled_by_default") is True:
            errors.append(f"{pid}: remote/provider configs must not enable by default")
        if provider.get("live_inference_verified") is True:
            errors.append(f"{pid}: live_inference_verified requires explicit external receipt not accepted in fixture")
        credentials = provider.get("credentials") or {}
        if credentials:
            errors.append(f"{pid}: credentials must not be committed in provider config examples")
    return errors


def provider_status(config: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": "odin_provider_config_status",
        "providers": redact_secrets(config.get("providers", [])),
        "candidate_only": True,
        "claim_boundary": "provider_config_status_redacted_not_live_inference_proof",
    }

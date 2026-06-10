from __future__ import annotations

from typing import Any

SECRET_KEY_MARKERS: frozenset[str] = frozenset({
    "token",
    "secret",
    "password",
    "authorization",
    "api_key",
    "apikey",
    "bearer",
    "client_secret",
    "refresh_token",
    "access_token",
    "credential",
})

REDACTED_PLACEHOLDER = "[REDACTED]"

DOCTOR_REDACTION_CLAIM = "doctor_output_redacted_no_secret_values"


def is_secret_key(key: str) -> bool:
    lowered = key.lower().replace("-", "_").replace(".", "_")
    return any(marker in lowered for marker in SECRET_KEY_MARKERS)


def redact_value(key: str, value: Any) -> Any:
    if is_secret_key(str(key)):
        return REDACTED_PLACEHOLDER
    return redact_recursive(value)


def redact_recursive(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: redact_value(k, v) for k, v in value.items()}
    if isinstance(value, list):
        return [redact_recursive(v) for v in value]
    if isinstance(value, str) and value.lower().startswith("bearer "):
        return REDACTED_PLACEHOLDER
    return value


def redact_env_snapshot(env: dict[str, str]) -> dict[str, str]:
    return {k: (REDACTED_PLACEHOLDER if is_secret_key(k) else v) for k, v in env.items()}

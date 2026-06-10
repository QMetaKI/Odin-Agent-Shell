from __future__ import annotations

import json
from typing import Any

SECRET_KEY_MARKERS = ("api_key", "token", "secret", "authorization", "password", "bearer", "client_secret", "refresh_token", "access_token")
REDACTION = "[REDACTED]"


def is_secret_key(key: str) -> bool:
    lowered = key.lower().replace("-", "_")
    return any(marker in lowered for marker in SECRET_KEY_MARKERS)


def redact_secrets(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: (REDACTION if is_secret_key(str(k)) else redact_secrets(v)) for k, v in value.items()}
    if isinstance(value, list):
        return [redact_secrets(v) for v in value]
    if isinstance(value, str) and value.lower().startswith("bearer "):
        return REDACTION
    return value


def dumps_redacted(value: Any) -> str:
    return json.dumps(redact_secrets(value), indent=2, ensure_ascii=False, sort_keys=True)

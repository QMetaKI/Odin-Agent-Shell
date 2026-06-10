from __future__ import annotations

import re
from typing import Any, Dict

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{8,}"),
    re.compile(r"(?i)(api[_-]?key\s*[:=]\s*)[^\s]+"),
    re.compile(r"(?i)(password\s*[:=]\s*)[^\s]+"),
]


def redact_shadow_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    hits = 0
    scrubbed = {}
    for key, value in payload.items():
        key_l = str(key).lower()
        if any(token in key_l for token in ["api_key", "apikey", "password", "secret", "token"]):
            hits += 1
            scrubbed[key] = "[REDACTED]"
        else:
            scrubbed[key] = value
    text = str(scrubbed)
    for pattern in SECRET_PATTERNS:
        matches = pattern.findall(text)
        hits += len(matches)
        text = pattern.sub("[REDACTED]", text)
    return {
        "artifact_kind": "odin_shadow_redaction_result",
        "protocol_version": "7.1-shadow",
        "redacted_preview": text[:500],
        "secret_hits": hits,
        "remote_allowed": False if hits else payload.get("remote_allowed", False),
        "boundary": "redaction_candidate_only_no_secret_storage",
    }

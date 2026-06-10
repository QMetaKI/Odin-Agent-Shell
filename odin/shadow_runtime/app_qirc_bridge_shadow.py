from __future__ import annotations

from typing import Any, Dict, List


BLOCKED_CHANNELS = {"secrets", "private.raw", "credentials", "full_state_firehose"}


def validate_shadow_app_qirc_digest(digest: Dict[str, Any]) -> Dict[str, Any]:
    allowed = set(digest.get("allowed_channels", []) or [])
    blocked = set(digest.get("blocked_channels", []) or [])
    requested = set(digest.get("requested_channels", []) or allowed)
    violations = sorted((requested & BLOCKED_CHANNELS) - blocked)
    return {
        "artifact_kind": "odin_shadow_app_qirc_bridge_validation",
        "protocol_version": "7.1-shadow",
        "bridge_id": digest.get("bridge_id"),
        "ok": not violations and digest.get("digest_mode") in {"summary_only", "redacted_summary"},
        "violations": violations,
        "odin_consumes": "digest_only",
        "odin_owns_app_qirc": False,
        "boundary": "app_qirc_digest_only_no_state_authority",
    }

from __future__ import annotations

from typing import Any, Dict


def build_shadow_api_plan(endpoint: str, work: Dict[str, Any] | None = None) -> Dict[str, Any]:
    work = work or {}
    allowed = endpoint in {
        "/v7/status", "/v7/health", "/v7/universal-work/validate", "/v7/universal-work/run", "/v7/bus/status", "/v7/response/compile"
    }
    return {
        "artifact_kind": "odin_shadow_api_plan",
        "protocol_version": "7.1-shadow",
        "endpoint": endpoint,
        "work_id": work.get("work_id"),
        "allowed_in_shadow": allowed,
        "localhost_only": True,
        "side_effects": "none",
        "returns": "candidate_or_status_projection",
        "boundary": "api_plan_only_no_live_server_claim",
    }

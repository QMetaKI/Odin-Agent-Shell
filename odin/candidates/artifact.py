from __future__ import annotations
from odin.runtime.ids import stable_id
from odin.core.claim_boundary import filter_claims


def build_candidate_artifact(work: dict, content: dict | str, trace_id: str, claims: list[str] | None = None) -> dict:
    allowed, blocked = filter_claims(claims or work.get("claim_boundary", {}).get("claims", []))
    return {
        "artifact_kind": "odin_candidate_artifact",
        "protocol_version": "7.1",
        "candidate_id": stable_id("CAND", {"work_id": work.get("work_id"), "content": content}, 14),
        "work_id": work.get("work_id"),
        "caller_id": work.get("caller_id"),
        "candidate_only": True,
        "app_owned_apply": True,
        "may_apply": False,
        "content": content,
        "claims": allowed,
        "blocked_claims": blocked,
        "trace_id": trace_id,
        "claim_boundary": "candidate_artifact_not_app_apply",
    }

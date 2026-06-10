from __future__ import annotations

CANDIDATE_ONLY = True
NO_APP_MUTATION = True
NO_EXTERNAL_SEND = True


def run_failure_story_registry_shadow(packet: dict) -> dict:
    """Shadow-only bounded function for v0.7.0. No runtime effects."""
    if packet.get("request_direct_apply") or packet.get("grant_authority"):
        return {"ok": False, "decision": "block", "reason": "shadow_narrative_boundary"}
    return {"ok": True, "decision": "candidate", "artifact_kind": "odin_failure_story", "claim_boundary": "candidate_only_not_runtime"}

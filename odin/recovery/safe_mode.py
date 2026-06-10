from __future__ import annotations

def build_safe_mode_plan(reason: str = "manual") -> dict:
    return {
        "artifact_kind": "odin_safe_mode_plan",
        "protocol_version": "7.1",
        "reason": reason,
        "actions": ["disable_remote_workers", "disable_external_send", "load_minimal_runtime_pack", "require_app_apply_gate"],
        "claim_boundary": "safe_mode_plan_is_candidate_until_host_applies_it",
    }

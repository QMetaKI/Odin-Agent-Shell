from __future__ import annotations

FORBIDDEN = {"apply", "external_send", "runtime_proof", "app_mutation"}

def run_odin_hub_panel_router_shadow(packet: dict | None = None) -> dict:
    """Candidate-only shadow function for v0.7.4 Product/Pattern/Atom/Hub Lock."""
    packet = packet or {}
    text = str(packet).lower()
    if any(marker in text for marker in FORBIDDEN):
        return {"ok": False, "decision": "block", "reason": "forbidden_boundary_marker", "claim_boundary": "candidate_only_not_runtime"}
    return {"ok": True, "decision": "candidate", "candidate_type": "odin_hub_panel_candidate", "claim_boundary": "candidate_only_not_runtime", "why_trace": ["v0.7.4_shadow_candidate"]}

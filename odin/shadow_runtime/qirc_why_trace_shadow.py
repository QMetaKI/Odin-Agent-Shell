from __future__ import annotations

def build_qirc_why_trace(centerline: str, route_scores: dict[str, float], active_seeds: list[str]) -> dict:
    best = max(route_scores, key=route_scores.get) if route_scores else "hold"
    return {"artifact_kind": "odin_qirc_why_trace", "protocol_version": "7.1", "summary": f"{best} selected by route score under {centerline}.", "centerline": centerline, "active_seeds": active_seeds, "route_score": route_scores, "final_gate": "candidate_only_preserved"}

from __future__ import annotations

def score_candidate(candidate: dict) -> float:
    score = 1.0
    if candidate.get("blocked_claims"):
        score -= 0.5
    content = candidate.get("content")
    if isinstance(content, dict) and content.get("work_atom_execution"):
        score += 0.2
    if candidate.get("candidate_only") is True and candidate.get("app_owned_apply") is True:
        score += 0.3
    return score


def select_candidate(candidates: list[dict]) -> dict:
    if not candidates:
        return {"selected": None, "reason": "no_candidates"}
    ranked = sorted(candidates, key=score_candidate, reverse=True)
    return {"selected": ranked[0], "ranked_ids": [c.get("candidate_id") for c in ranked], "scores": {c.get("candidate_id"): score_candidate(c) for c in ranked}}

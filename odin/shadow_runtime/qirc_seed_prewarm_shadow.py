from __future__ import annotations

def prewarm_qirc_seeds(context_tags: list[str], budget: int = 24) -> dict:
    base = ["claim_boundary", "minimal_sufficient_depth", "candidate_only"]
    selected = []
    for seed in base + list(context_tags):
        if seed not in selected:
            selected.append(seed)
    selected = selected[:budget]
    return {"artifact_kind": "odin_qirc_seed_budget", "protocol_version": "7.1", "active_seeds": selected, "max_active_seeds": budget, "conflicts_removed": 0, "noise_gate": "hard"}

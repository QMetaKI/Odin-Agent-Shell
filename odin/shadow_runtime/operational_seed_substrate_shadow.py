from __future__ import annotations
HARD_SEEDS = ["children_family_first", "candidate_only", "claim_boundary", "app_authority_preserve", "no_hidden_apply", "local_first"]
def activate_operational_seeds(context_tags: list[str], budget: int = 12) -> dict:
    candidates = list(dict.fromkeys(HARD_SEEDS + list(context_tags)))
    active = candidates[:max(budget, len(HARD_SEEDS))]
    suppressed = candidates[len(active):]
    return {"artifact_kind":"odin_seed_activation_packet","active_seeds":active,"suppressed_seeds":suppressed,"conflicts_removed":[],"budget_profile":"standard_local","top_k_limit":budget}

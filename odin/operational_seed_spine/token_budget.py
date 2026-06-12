"""Per-seed token budget — routing hints for work scoping.

Claim boundary: operational_seed_spine_routes_work_not_authority
candidate_only: true

Token budget is a routing hint, not a model enforcement proof.
No provider/model dependency. No external tokenizer dependency.
"""
from __future__ import annotations

from typing import List

CLAIM_BOUNDARY = "operational_seed_spine_routes_work_not_authority"

TOKEN_BUDGETS: dict[str, dict] = {
    "tiny": {
        "budget_key": "tiny",
        "max_input_tokens_hint": 500,
        "max_output_tokens_hint": 300,
        "compression_required": False,
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
    },
    "small": {
        "budget_key": "small",
        "max_input_tokens_hint": 2000,
        "max_output_tokens_hint": 1200,
        "compression_required": False,
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
    },
    "medium": {
        "budget_key": "medium",
        "max_input_tokens_hint": 6000,
        "max_output_tokens_hint": 3000,
        "compression_required": False,
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
    },
    "large": {
        "budget_key": "large",
        "max_input_tokens_hint": 16000,
        "max_output_tokens_hint": 6000,
        "compression_required": True,
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
    },
    "audit": {
        "budget_key": "audit",
        "max_input_tokens_hint": 8000,
        "max_output_tokens_hint": 4000,
        "compression_required": False,
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
    },
}

REQUIRED_BUDGET_KEYS: List[str] = ["tiny", "small", "medium", "large", "audit"]

_FALLBACK_BUDGET = TOKEN_BUDGETS["small"]


def get_token_budget(budget_key: str) -> dict:
    """Return the token budget dict for the given key. Falls back to 'small'."""
    return TOKEN_BUDGETS.get(budget_key, _FALLBACK_BUDGET)

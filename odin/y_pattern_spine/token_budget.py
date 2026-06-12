"""Y Token Budget — minimal/normal/deep modes.

Claim boundary: y_pattern_spine_candidate_only_no_app_apply_no_provider_no_runtime_authority
candidate_only: true
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

CLAIM_BOUNDARY = "y_pattern_spine_candidate_only_no_app_apply_no_provider_no_runtime_authority"


@dataclass
class YTokenBudget:
    mode: str
    description: str
    includes: List[str]
    excludes: List[str]
    typical_token_range: str

    def to_dict(self) -> dict:
        return {
            "mode": self.mode,
            "description": self.description,
            "includes": self.includes,
            "excludes": self.excludes,
            "typical_token_range": self.typical_token_range,
        }


TOKEN_BUDGET_MODES: Dict[str, YTokenBudget] = {
    "minimal": YTokenBudget(
        mode="minimal",
        description="Route hint + work capsule + required files only",
        includes=["route_hint", "work_capsule", "required_files", "validators"],
        excludes=["source_summaries", "pattern_mine_audit", "full_repo_context"],
        typical_token_range="500–2000",
    ),
    "normal": YTokenBudget(
        mode="normal",
        description="Minimal + source summaries + validators",
        includes=["route_hint", "work_capsule", "required_files", "validators", "source_summaries"],
        excludes=["pattern_mine_audit_background", "full_repo_context"],
        typical_token_range="2000–6000",
    ),
    "deep": YTokenBudget(
        mode="deep",
        description="Normal + pattern mine audit background",
        includes=["route_hint", "work_capsule", "required_files", "validators", "source_summaries", "pattern_mine_audit"],
        excludes=["full_repo_context"],
        typical_token_range="6000–15000",
    ),
}


def get_budget(mode: str) -> YTokenBudget:
    if mode not in TOKEN_BUDGET_MODES:
        raise ValueError(f"Unknown token budget mode: {mode!r}. Valid: {list(TOKEN_BUDGET_MODES)}")
    return TOKEN_BUDGET_MODES[mode]

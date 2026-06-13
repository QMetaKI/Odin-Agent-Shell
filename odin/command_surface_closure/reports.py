"""Command Surface Closure — Reports.

Claim boundary: command_surface_closure_indexes_cli_surface_not_runtime_completion
candidate_only: true
"""
from __future__ import annotations

from .command_index import build_command_surface_index
from .alias_policy import build_command_alias_policy
from .coverage import build_command_surface_coverage

CLAIM_BOUNDARY = "command_surface_closure_indexes_cli_surface_not_runtime_completion"


def build_command_surface_report(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    index = build_command_surface_index(generated_at_utc=generated_at_utc)
    alias_policy = build_command_alias_policy(generated_at_utc=generated_at_utc)
    coverage = build_command_surface_coverage(generated_at_utc=generated_at_utc)
    return {
        "artifact_kind": "odin_command_surface_closure_report",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "command_index": index,
        "alias_policy": alias_policy,
        "coverage": coverage,
        "summary": "Command surface indexed. Neutral naming applied. FINAL-PR-13 remains deferred.",
        "not_proven": ["runtime_completion", "production_readiness"],
    }

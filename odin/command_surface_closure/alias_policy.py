"""Command Surface Closure — Alias Policy.

Claim boundary: command_surface_closure_indexes_cli_surface_not_runtime_completion
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "command_surface_closure_indexes_cli_surface_not_runtime_completion"


def build_command_alias_policy(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    return {
        "artifact_kind": "odin_command_alias_policy",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "policy": "New commands use neutral names. Historical aliases are preserved for backward compatibility.",
        "neutral_naming_applied": True,
        "historical_aliases_preserved": True,
        "aliases": [
            {"alias": "validate-final-pr-11-5-semantic-kernel-coverage", "canonical": "validate-final-pr-11-5-semantic-kernel-coverage", "type": "historical_canonical", "notes": "Historical name preserved for backward compat"},
            {"alias": "validate-final-pr-11-provider-critic-thor", "canonical": "validate-final-pr-11-provider-critic-thor", "type": "historical_canonical", "notes": "Historical name preserved"},
            {"alias": "release-preflight", "canonical": "validate-final-release-preflight", "type": "legacy_alias", "notes": "Short form preserved"},
        ],
        "not_proven": ["runtime_completion"],
    }

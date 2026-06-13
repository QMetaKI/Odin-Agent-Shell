"""Status Classifier — classifies each mapping's implementation status.

Claim boundary: y_pattern_operationalization_index_maps_internal_patterns_to_neutral_odin_not_authority
candidate_only: true
"""
from __future__ import annotations

# Maps internal_pattern -> status
_STATUS_MAP: dict[str, str] = {
    "Internal Semantic Bus": "structural_evidence",
    "AI without AI": "implemented",
    "evidence gates": "implemented",
    "mirror critics": "implemented",
    "seeds / pattern mines": "structural_evidence",
    "narrative compiler": "structural_evidence",
    "fit / resonance": "partial",
    "Thor": "implemented",
    "orchestration profile": "partial",
    "app sovereignty": "implemented",
    "candidate reality": "implemented",
    "golden traces": "implemented",
    "authority drift scanner": "partial",
    "boundary coherence scanner": "partial",
}


def classify_status(internal_pattern: str) -> str:
    """Return status for an internal pattern."""
    return _STATUS_MAP.get(internal_pattern, "target_only")

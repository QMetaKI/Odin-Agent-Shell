"""Materialization level constants for FINAL-PR-08 Projection Candidate Spine."""
from __future__ import annotations

MATERIALIZATION_LEVELS: list[str] = [
    "M0_raw_input",
    "M1_handoff_context",
    "M2_universal_work",
    "M3_seed_route",
    "M4_field_selection",
    "M5_projection_set",
    "M6_candidate_artifact",
    "M7_response_packet",
    "M8_trace_receipt",
    "M9_release_evidence",
]

_LEVEL_INDEX: dict[str, int] = {level: idx for idx, level in enumerate(MATERIALIZATION_LEVELS)}


def validate_materialization_level(level: str) -> bool:
    return level in _LEVEL_INDEX


def materialization_index(level: str) -> int:
    if level not in _LEVEL_INDEX:
        raise ValueError(f"unknown materialization level: {level!r}")
    return _LEVEL_INDEX[level]

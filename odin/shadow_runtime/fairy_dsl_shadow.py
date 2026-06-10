"""Fairy DSL shadow layer.

This module is code-near, non-executing, and non-authoritative.
It extracts and validates narrative nodes before Y* lowering.
"""
from __future__ import annotations
from dataclasses import dataclass

FORBIDDEN_FAIRY_MARKERS = {"direct_apply", "external_send", "runtime_verified", "tests_passed"}

@dataclass(frozen=True)
class FairyStoryShadow:
    story_id: str
    title: str
    fairy_spine: str
    ystar_unit_ref: str
    nodes: tuple[str, ...]
    claim_boundary: str = "fairy_story_is_not_executable"


def validate_fairy_story_shadow(story: FairyStoryShadow) -> list[str]:
    errors: list[str] = []
    if not story.ystar_unit_ref:
        errors.append("missing_ystar_unit_ref")
    if not story.nodes:
        errors.append("missing_nodes")
    text = (story.fairy_spine + " " + " ".join(story.nodes)).lower()
    for marker in FORBIDDEN_FAIRY_MARKERS:
        if marker in text:
            errors.append(f"forbidden_marker:{marker}")
    if story.claim_boundary != "fairy_story_is_not_executable":
        errors.append("invalid_claim_boundary")
    return errors

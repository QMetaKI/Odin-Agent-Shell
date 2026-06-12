"""Hole density calculation for required public evidence."""
from __future__ import annotations

from odin.field_selection_spine.fields import bound_score


def calculate_hole_density(required_evidence: list[str], evidence_items: list[str]) -> float:
    if not required_evidence:
        return 0.0
    evidence_text = "\n".join(str(item).lower() for item in evidence_items)
    missing = 0
    for requirement in required_evidence:
        token = str(requirement).lower()
        if token not in evidence_text:
            missing += 1
    return bound_score(missing / len(required_evidence))

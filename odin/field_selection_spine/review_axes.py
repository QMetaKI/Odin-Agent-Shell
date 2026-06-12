"""Review axes for deterministic field scoring."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReviewAxis:
    axis_id: str
    description: str
    scoring_method: str

    def to_dict(self) -> dict:
        return {"axis_id": self.axis_id, "description": self.description, "scoring_method": self.scoring_method}


REVIEW_AXES: list[ReviewAxis] = [
    ReviewAxis("scope", "Checks whether the work remains bounded to the requested slice.", "explicit-context-signal"),
    ReviewAxis("claim_boundary", "Checks candidate-only and no-truth boundary evidence.", "explicit-boundary-signal"),
    ReviewAxis("repo_reality", "Checks whether repo evidence is present.", "explicit-evidence-signal"),
    ReviewAxis("runtime_truth", "Checks whether runtime claims are avoided unless receipts exist.", "receipt-gap-signal"),
    ReviewAxis("locality", "Checks local-only and no-public-network constraints.", "boundary-flag-signal"),
    ReviewAxis("candidate_integrity", "Checks candidate-only output integrity.", "candidate-flag-signal"),
    ReviewAxis("evidence", "Checks explicit public evidence availability.", "evidence-count-signal"),
    ReviewAxis("token_efficiency", "Checks whether concise route hints are enough.", "context-size-signal"),
    ReviewAxis("app_authority", "Checks app-owned apply boundary.", "authority-boundary-signal"),
    ReviewAxis("release_readiness", "Checks that release closure remains deferred.", "closure-boundary-signal"),
]
REVIEW_AXIS_IDS = [axis.axis_id for axis in REVIEW_AXES]

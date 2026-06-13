"""v7.1.1 Coverage Compiler — maps v7.1.1 target canon to repo-real evidence.

Claim boundary: v711_coverage_compiler_maps_target_to_repo_evidence_not_runtime_completion
candidate_only: true
app_owned_apply: true
"""
from .coverage_matrix import build_v711_coverage_matrix
from .gap_index import build_v711_gap_index
from .target_loader import load_v711_targets
from .evidence_mapper import map_targets_to_repo_evidence
from .next_pr_recommender import recommend_next_prs_from_v711_gaps
from .reports import build_v711_coverage_report

__all__ = [
    "build_v711_coverage_matrix",
    "build_v711_gap_index",
    "load_v711_targets",
    "map_targets_to_repo_evidence",
    "recommend_next_prs_from_v711_gaps",
    "build_v711_coverage_report",
]

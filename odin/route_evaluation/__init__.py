"""Route Evaluation Receipt Harness — FINAL-PR-11.

Claim boundary: route_evaluation_receipts_measure_structure_not_model_quality_benchmark
candidate_only: true

Measures structure, boundary cleanliness, receipt completeness.
NOT a model quality benchmark. NOT a superiority claim.
"""
from odin.route_evaluation.fixtures import build_route_eval_fixtures
from odin.route_evaluation.evaluator import evaluate_route_candidate
from odin.route_evaluation.receipt import run_route_evaluation_receipt

__all__ = [
    "build_route_eval_fixtures",
    "evaluate_route_candidate",
    "run_route_evaluation_receipt",
]

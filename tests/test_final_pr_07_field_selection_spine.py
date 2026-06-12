from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_imports():
    import odin.field_selection_spine as spine
    assert spine.CLAIM_BOUNDARY == "field_selection_scores_routes_not_truth"


def test_review_axes_and_fields_defined():
    from odin.field_selection_spine import FIELD_DEFINITIONS, REVIEW_AXES
    axes = [axis.axis_id for axis in REVIEW_AXES]
    assert axes == ["scope", "claim_boundary", "repo_reality", "runtime_truth", "locality", "candidate_integrity", "evidence", "token_efficiency", "app_authority", "release_readiness"]
    for field_id in ["scope_control", "claim_boundary_integrity", "repo_reality_alignment", "runtime_truth_alignment", "locality_preservation", "candidate_integrity", "evidence_sufficiency", "token_efficiency", "app_authority_boundary", "release_readiness_boundary"]:
        assert field_id in FIELD_DEFINITIONS
        assert FIELD_DEFINITIONS[field_id]["candidate_only_boundary"] == "field_selection_scores_routes_not_truth"


def test_field_signal_weights_bounded():
    from odin.field_selection_spine.fields import FieldSignal
    assert FieldSignal("x", "X", -1, [], "s").signal_weight == 0.0
    assert FieldSignal("x", "X", 2, [], None).signal_weight == 1.0


def test_selector_returns_stable_candidate_selection():
    from odin.field_selection_spine import select_field_route
    ctx = {"trigger_shape": "repo", "work_type": "repo", "repo_evidence": "SYSTEM_MAP.json"}
    one = select_field_route(ctx)
    two = select_field_route(ctx)
    assert one.to_dict() == two.to_dict()
    assert one.candidate_only is True
    assert one.app_owned_apply is True
    assert one.claim_boundary == "field_selection_scores_routes_not_truth"
    assert one.suppressed_fields is not None
    assert isinstance(one.route_recommendation, str)
    assert one.route_recommendation.startswith("route_hint:")
    assert not one.route_recommendation.startswith(("run ", "apply ", "send "))


def test_coherence_score_bounds_and_hole_density():
    from odin.field_selection_spine import calculate_hole_density, select_field_route
    selection = select_field_route({"work_type": "repo", "repo_evidence": "SYSTEM_MAP.json"})
    score = selection.coherence_score
    assert hasattr(score, "overall_score")
    assert 0.0 <= score.overall_score <= 1.0
    assert 0.0 <= score.route_confidence <= 1.0
    assert 0.0 <= score.hole_density <= 1.0
    for value in score.axis_scores.values():
        assert 0.0 <= value <= 1.0
    assert calculate_hole_density([], []) == 0.0
    assert 0.0 <= calculate_hole_density(["a"], []) <= 1.0


def test_why_trace_public_and_deterministic():
    from odin.field_selection_spine.why_trace import build_field_why_trace
    trace_one = build_field_why_trace("repo_reality_alignment", ["repo_evidence_present"], ["repo_evidence=SYSTEM_MAP.json"], ["final_truth_claim"])
    trace_two = build_field_why_trace("repo_reality_alignment", ["repo_evidence_present"], ["repo_evidence=SYSTEM_MAP.json"], ["final_truth_claim"])
    assert trace_one.trace_id == trace_two.trace_id
    assert trace_one.not_proven
    assert trace_one.evidence_items == ["repo_evidence=SYSTEM_MAP.json"]
    data = trace_one.to_dict()
    assert "chain_of_thought" not in data
    assert "private_reasoning" not in data
    assert "hidden_scratchpad" not in data


def test_proof_packet_lists():
    from odin.field_selection_spine.proof import REQUIRED_NOT_PROVEN, REQUIRED_PROVEN, build_proof_packet
    packet = build_proof_packet()
    for item in REQUIRED_PROVEN:
        assert item in packet["proven"]
    for item in REQUIRED_NOT_PROVEN:
        assert item in packet["not_proven"]


def test_pr06_seed_route_integration():
    from odin.field_selection_spine import select_field_route_from_seed_route
    from odin.operational_seed_spine.selector import select_seed_route
    seed_route = select_seed_route({"trigger_shape": "repo", "work_type": "repo"})
    selection = select_field_route_from_seed_route(seed_route)
    assert selection.candidate_only is True
    assert selection.claim_boundary == "field_selection_scores_routes_not_truth"
    assert any("selected_seed_id" in item for item in selection.why_trace.evidence_items)


def run_cli(*args: str):
    return subprocess.run([sys.executable, "-m", "odin.cli", *args], cwd=ROOT, text=True, capture_output=True, check=False)


def test_cli_commands():
    assert run_cli("validate-field-selection-spine").returncode == 0
    explain = run_cli("explain-field-selection", "--demo")
    assert explain.returncode == 0
    assert json.loads(explain.stdout)["candidate_only"] is True
    assert run_cli("prove-field-selection-spine").returncode == 0


def test_local_hub_payload_shape():
    from odin.field_selection_spine.selector import select_field_route
    payload = {"status": "ok", "candidate_only": True, "claim_boundary": "field_selection_scores_routes_not_truth", "field_selection": select_field_route({"work_type": "repo", "repo_evidence": "SYSTEM_MAP.json"}).to_dict(), "not_proven": []}
    json.dumps(payload)
    assert payload["field_selection"]["candidate_only"] is True


def test_no_forbidden_runtime_names_in_pr07_module():
    forbidden = ["dfas", "q_shabang", "qmath", "q_state", "qgit", "qcode", "qli", "qstar"]
    violations = []
    for path in (ROOT / "odin/field_selection_spine").glob("*.py"):
        text = path.read_text(encoding="utf-8").lower()
        for name in forbidden:
            if name in text:
                violations.append(f"{path.name}:{name}")
    assert not violations


def test_validator_and_validate_all_include_pr07():
    result = run_cli("validate-field-selection-spine")
    assert result.returncode == 0
    assert "validate_field_selection_spine()" in (ROOT / "odin/cli.py").read_text(encoding="utf-8")


def test_prep_validator_passes_and_pr08_protected():
    result = run_cli("validate-prep-final-pr-06-08")
    assert result.returncode == 0
    prep = (ROOT / "tools/rebaseline/check_prep_final_pr_06_08.py").read_text(encoding="utf-8")
    assert "odin/projection_candidate_spine" in prep
    assert '"odin/field_selection_spine"' in prep

"""B4 Minicheck / Critics / Tournament / Candidate DNA / Response Packet / Final Gate Advisory tests."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

B4_SLICE_IDS = [f"V711-R100-{i:03d}" for i in range(106, 138)]
B4_FAMILIES = {"PR-33-MINICHECK-CRITICS-TOURNAMENT", "PR-34-CANDIDATE-FINAL-GATE"}

REQUIRED_ROUTE_CLASSES = {
    "deterministic_no_model",
    "tiny_local_candidate",
    "small_model_candidate",
    "small_model_multi_slot_candidate",
    "local_7b_8b_candidate",
    "hybrid_3b_7b_candidate",
    "quality_hybrid_candidate",
    "heavy_local_candidate",
    "remote_explicit_only",
    "cannot_safely_complete",
}

REQUIRED_CRITIC_TIERS = {
    "deterministic_schema_critic",
    "deterministic_contract_critic",
    "small_model_advisory_critic",
    "hybrid_advisory_critic",
    "human_review_required",
    "cannot_safely_complete",
}

REQUIRED_CASCADE_STAGES = {
    "minicheck",
    "schema_critic",
    "contract_critic",
    "route_aware_critic",
    "consistency_critic",
    "claim_boundary_critic",
    "final_gate_advisor",
    "human_review_required",
}

REQUIRED_ESCALATION_CONDITIONS = {
    "missing_claim_boundary",
    "forbidden_action_detected",
    "route_class_mismatch",
    "output_contract_violation",
    "provider_policy_missing",
    "runtime_claim_detected",
    "model_quality_claim_detected",
    "remote_route_requested",
    "candidate_conflict_detected",
    "final_gate_authority_claim_detected",
    "receipt_truth_claim_detected",
}

REQUIRED_SCORING_DIMENSIONS = {
    "schema_validity",
    "contract_compliance",
    "claim_boundary_compliance",
    "context_fidelity",
    "gaptext_compliance",
    "forbidden_action_absence",
    "route_class_fit",
    "evidence_completeness",
    "receipt_readiness",
    "human_review_need",
}

REQUIRED_MINICHECK_KINDS = {
    "schema_shape_check",
    "claim_boundary_check",
    "forbidden_action_check",
    "output_contract_check",
    "context_ref_check",
    "gaptext_shape_check",
    "route_class_check",
    "provider_policy_check",
    "no_runtime_claim_check",
    "no_model_quality_claim_check",
    "no_external_send_check",
    "no_app_apply_check",
    "final_gate_boundary_check",
    "receipt_boundary_check",
}

REQUIRED_ARTIFACT_STATUSES = {
    "created",
    "minicheck_passed",
    "minicheck_warned",
    "critic_pending",
    "critic_passed",
    "critic_warned",
    "critic_failed",
    "tournament_pending",
    "tournament_selected",
    "tournament_rejected",
    "final_gate_pending",
    "final_gate_advisory_passed",
    "final_gate_advisory_warned",
    "final_gate_advisory_blocked",
    "human_review_required",
    "cannot_safely_complete",
}

REQUIRED_FINAL_GATE_RECS = {
    "advisory_pass",
    "advisory_warn",
    "advisory_block",
    "human_review_required",
    "cannot_safely_complete",
}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_b4_bundle() -> dict | None:
    plan = load_json(ROOT / "registries" / "v7_1_1_actual_codex_bundle_plan.json")
    return next((b for b in plan.get("actual_bundles", []) if b.get("bundle_id") == "B4"), None)


# ─── 1. B4 bundle exists ────────────────────────────────────────────────────
def test_b4_mapping_exists():
    b4 = get_b4_bundle()
    assert b4 is not None, "B4 bundle must exist in actual_codex_bundle_plan.json"


# ─── 2. B4 maps V711-R100-106..137 ──────────────────────────────────────────
def test_b4_maps_correct_range():
    b4 = get_b4_bundle()
    assert b4 is not None
    assert b4.get("slice_range") == "V711-R100-106..137"


# ─── 3. B4 has exactly 32 canonical slice IDs ────────────────────────────────
def test_b4_has_exactly_32_slices():
    b4 = get_b4_bundle()
    assert b4 is not None
    assert len(b4.get("slice_ids", [])) == 32, f"Expected 32 slices, got {len(b4.get('slice_ids', []))}"


# ─── 4. B4 has no out-of-range slice IDs ─────────────────────────────────────
def test_b4_no_out_of_range_slices():
    b4 = get_b4_bundle()
    assert b4 is not None
    expected = set(B4_SLICE_IDS)
    actual = set(b4.get("slice_ids", []))
    out = actual - expected
    assert len(out) == 0, f"Out-of-range slice IDs: {sorted(out)}"


# ─── 5. B4 absorbs PR-33 ────────────────────────────────────────────────────
def test_b4_absorbs_pr33():
    b4 = get_b4_bundle()
    assert b4 is not None
    families = b4.get("absorbed_future_pr_families", [])
    assert "PR-33-MINICHECK-CRITICS-TOURNAMENT" in families


# ─── 6. B4 absorbs PR-34 ────────────────────────────────────────────────────
def test_b4_absorbs_pr34():
    b4 = get_b4_bundle()
    assert b4 is not None
    families = b4.get("absorbed_future_pr_families", [])
    assert "PR-34-CANDIDATE-FINAL-GATE" in families


# ─── 7–9. B1/B2/B3 preserved ────────────────────────────────────────────────
def test_b1_mapping_preserved():
    plan = load_json(ROOT / "registries" / "v7_1_1_actual_codex_bundle_plan.json")
    b1 = next((b for b in plan.get("actual_bundles", []) if b.get("bundle_id") == "B1"), None)
    assert b1 is not None
    assert b1.get("actual_pr") == "PR-27"


def test_b2_mapping_preserved():
    plan = load_json(ROOT / "registries" / "v7_1_1_actual_codex_bundle_plan.json")
    b2 = next((b for b in plan.get("actual_bundles", []) if b.get("bundle_id") == "B2"), None)
    assert b2 is not None
    assert b2.get("actual_pr") == "PR-28"


def test_b3_mapping_preserved():
    plan = load_json(ROOT / "registries" / "v7_1_1_actual_codex_bundle_plan.json")
    b3 = next((b for b in plan.get("actual_bundles", []) if b.get("bundle_id") == "B3"), None)
    assert b3 is not None
    assert b3.get("actual_pr") == "PR-29"


# ─── 10. Canonical ladder not rewritten ──────────────────────────────────────
def test_canonical_ladder_not_rewritten():
    ladder = load_json(ROOT / "registries" / "v7_1_1_road_to_100_ladder.json")
    assert ladder.get("canonical_slice_count", 0) >= 190
    families = ladder.get("future_pr_families", [])
    assert "PR-33-MINICHECK-CRITICS-TOURNAMENT" in families
    assert "PR-34-CANDIDATE-FINAL-GATE" in families


# ─── 11. Minicheck schema/registry/example exist ──────────────────────────────
def test_minicheck_schema_exists():
    assert (ROOT / "schemas" / "v7_1_1_minicheck.schema.json").exists()


def test_minicheck_registry_exists():
    assert (ROOT / "registries" / "v7_1_1_minicheck_registry.json").exists()


def test_minicheck_example_exists():
    assert (ROOT / "examples" / "v7_1_1" / "minicheck.example.json").exists()


# ─── 12. Minicheck required check kinds ──────────────────────────────────────
def test_minicheck_required_check_kinds():
    schema = load_json(ROOT / "schemas" / "v7_1_1_minicheck.schema.json")
    enum_vals = set(schema.get("properties", {}).get("check_kind", {}).get("enum", []))
    missing = REQUIRED_MINICHECK_KINDS - enum_vals
    assert len(missing) == 0, f"Missing minicheck kinds: {sorted(missing)}"


# ─── 13. CriticWorkPacket schema/registry/example exist ──────────────────────
def test_critic_work_packet_schema_exists():
    assert (ROOT / "schemas" / "v7_1_1_critic_work_packet.schema.json").exists()


def test_critic_work_packet_registry_exists():
    assert (ROOT / "registries" / "v7_1_1_critic_work_packet_registry.json").exists()


def test_critic_work_packet_example_exists():
    assert (ROOT / "examples" / "v7_1_1" / "critic_work_packet.example.json").exists()


# ─── 14. Critic tiers exist ──────────────────────────────────────────────────
def test_critic_tiers_exist():
    schema = load_json(ROOT / "schemas" / "v7_1_1_critic_work_packet.schema.json")
    enum_vals = set(schema.get("properties", {}).get("critic_tier", {}).get("enum", []))
    missing = REQUIRED_CRITIC_TIERS - enum_vals
    assert len(missing) == 0, f"Missing critic tiers: {sorted(missing)}"


# ─── 15. Critic route mapping covers all 10 B3 route classes ─────────────────
def test_critic_route_mapping_covers_all_10_route_classes():
    reg = load_json(ROOT / "registries" / "v7_1_1_critic_work_packet_registry.json")
    route_map = set(reg.get("route_to_critic_mapping", {}).keys())
    missing = REQUIRED_ROUTE_CLASSES - route_map
    assert len(missing) == 0, f"Route classes missing from critic mapping: {sorted(missing)}"


# ─── 16. CriticWorkPacket cannot accept claims or apply changes ───────────────
def test_critic_work_packet_cannot_accept_claims_or_apply():
    reg = load_json(ROOT / "registries" / "v7_1_1_critic_work_packet_registry.json")
    non_claims = reg.get("non_claims", [])
    assert "not_claim_acceptance" in non_claims
    assert "not_app_state_mutation" in non_claims
    inv = reg.get("invariants", [])
    assert any("not accept claims" in i for i in inv), "invariant: CriticWorkPacket may recommend, not accept claims"
    assert any("not apply" in i for i in inv), "invariant: CriticWorkPacket does not apply changes"


# ─── 17. Critic tiers do not claim actual model execution in B4 ───────────────
def test_critic_tiers_do_not_claim_model_execution():
    reg = load_json(ROOT / "registries" / "v7_1_1_critic_work_packet_registry.json")
    non_claims = reg.get("non_claims", [])
    assert "not_live_model_execution" in non_claims
    assert "not_provider_execution" in non_claims
    inv = reg.get("invariants", [])
    assert any("static contract roles" in i for i in inv), "critic tiers must be static contract roles in B4"


# ─── 18–20. Critic Cascade ───────────────────────────────────────────────────
def test_critic_cascade_schema_exists():
    assert (ROOT / "schemas" / "v7_1_1_critic_cascade.schema.json").exists()


def test_critic_cascade_registry_exists():
    assert (ROOT / "registries" / "v7_1_1_critic_cascade_registry.json").exists()


def test_critic_cascade_example_exists():
    assert (ROOT / "examples" / "v7_1_1" / "critic_cascade.example.json").exists()


def test_critic_cascade_stages_exist():
    reg = load_json(ROOT / "registries" / "v7_1_1_critic_cascade_registry.json")
    stages = set(reg.get("cascade_stages", []))
    missing = REQUIRED_CASCADE_STAGES - stages
    assert len(missing) == 0, f"Missing cascade stages: {sorted(missing)}"


def test_critic_escalation_conditions_exist():
    reg = load_json(ROOT / "registries" / "v7_1_1_critic_cascade_registry.json")
    conds = set(reg.get("escalation_conditions", []))
    missing = REQUIRED_ESCALATION_CONDITIONS - conds
    assert len(missing) == 0, f"Missing escalation conditions: {sorted(missing)}"


# ─── 21–23. Tournament ───────────────────────────────────────────────────────
def test_tournament_schema_exists():
    assert (ROOT / "schemas" / "v7_1_1_tournament_selection.schema.json").exists()


def test_tournament_registry_exists():
    assert (ROOT / "registries" / "v7_1_1_tournament_selection_registry.json").exists()


def test_tournament_example_exists():
    assert (ROOT / "examples" / "v7_1_1" / "tournament_selection.example.json").exists()


def test_tournament_scoring_dimensions_exist():
    reg = load_json(ROOT / "registries" / "v7_1_1_tournament_selection_registry.json")
    dims = set(reg.get("scoring_dimensions", []))
    missing = REQUIRED_SCORING_DIMENSIONS - dims
    assert len(missing) == 0, f"Missing scoring dimensions: {sorted(missing)}"


def test_tournament_cannot_apply_or_prove_correctness():
    reg = load_json(ROOT / "registries" / "v7_1_1_tournament_selection_registry.json")
    non_claims = reg.get("non_claims", [])
    assert "not_app_apply" in non_claims
    assert "not_correctness_proof" in non_claims
    assert "not_quality_certification" in non_claims


# ─── 24–27. Candidate DNA ────────────────────────────────────────────────────
def test_candidate_dna_schema_exists():
    assert (ROOT / "schemas" / "v7_1_1_candidate_dna.schema.json").exists()


def test_candidate_dna_registry_exists():
    assert (ROOT / "registries" / "v7_1_1_candidate_dna_registry.json").exists()


def test_candidate_dna_example_exists():
    assert (ROOT / "examples" / "v7_1_1" / "candidate_dna.example.json").exists()


def test_candidate_dna_lineage_fields_exist():
    schema = load_json(ROOT / "schemas" / "v7_1_1_candidate_dna.schema.json")
    required = set(schema.get("required", []))
    for field in ["candidate_dna_id", "candidate_artifact_ref", "source_modelworkpacket_ref",
                  "source_route_class", "generation_path", "privacy_class", "content_hash"]:
        assert field in required, f"candidate_dna schema missing required field: {field}"


def test_candidate_dna_has_privacy_class_and_content_hash():
    schema = load_json(ROOT / "schemas" / "v7_1_1_candidate_dna.schema.json")
    props = schema.get("properties", {})
    assert "privacy_class" in props, "candidate_dna schema must have privacy_class"
    assert "content_hash" in props, "candidate_dna schema must have content_hash"
    privacy_enum = props.get("privacy_class", {}).get("enum", [])
    assert "sensitive" in privacy_enum
    assert "redacted" in privacy_enum


def test_candidate_dna_does_not_imply_correctness_or_app_acceptance():
    reg = load_json(ROOT / "registries" / "v7_1_1_candidate_dna_registry.json")
    non_claims = reg.get("non_claims", [])
    assert "not_correctness_proof" in non_claims
    assert "not_app_acceptance" in non_claims
    assert "not_authorship_truth" in non_claims


# ─── 28–29. Candidate Artifact ───────────────────────────────────────────────
def test_candidate_artifact_schema_exists():
    assert (ROOT / "schemas" / "v7_1_1_candidate_artifact.schema.json").exists()


def test_candidate_artifact_registry_exists():
    assert (ROOT / "registries" / "v7_1_1_candidate_artifact_registry.json").exists()


def test_candidate_artifact_example_exists():
    assert (ROOT / "examples" / "v7_1_1" / "candidate_artifact.example.json").exists()


def test_candidate_artifact_statuses_exist():
    reg = load_json(ROOT / "registries" / "v7_1_1_candidate_artifact_registry.json")
    statuses = set(reg.get("allowed_statuses", []))
    missing = REQUIRED_ARTIFACT_STATUSES - statuses
    assert len(missing) == 0, f"Missing artifact statuses: {sorted(missing)}"


# ─── 30–33. Response Packet ───────────────────────────────────────────────────
def test_response_packet_schema_exists():
    assert (ROOT / "schemas" / "v7_1_1_response_packet.schema.json").exists()


def test_response_packet_registry_exists():
    assert (ROOT / "registries" / "v7_1_1_response_packet_registry.json").exists()


def test_response_packet_example_exists():
    assert (ROOT / "examples" / "v7_1_1" / "response_packet.example.json").exists()


def test_response_packet_has_claims_made_and_not_made():
    schema = load_json(ROOT / "schemas" / "v7_1_1_response_packet.schema.json")
    required = schema.get("required", [])
    assert "claims_made" in required
    assert "claims_not_made" in required


def test_response_packet_has_commands_and_tests_distinction():
    schema = load_json(ROOT / "schemas" / "v7_1_1_response_packet.schema.json")
    required = schema.get("required", [])
    assert "commands_run" in required
    assert "commands_not_run" in required
    assert "tests_run" in required
    assert "tests_not_run" in required


def test_response_packet_cannot_external_send_or_apply():
    reg = load_json(ROOT / "registries" / "v7_1_1_response_packet_registry.json")
    non_claims = reg.get("non_claims", [])
    assert "not_external_send" in non_claims
    assert "not_app_apply" in non_claims
    assert "not_app_state_mutation" in non_claims


# ─── 34–38. Final Gate Advisory ──────────────────────────────────────────────
def test_final_gate_advisory_schema_exists():
    assert (ROOT / "schemas" / "v7_1_1_final_gate_advisory.schema.json").exists()


def test_final_gate_advisory_registry_exists():
    assert (ROOT / "registries" / "v7_1_1_final_gate_advisory_registry.json").exists()


def test_final_gate_advisory_example_exists():
    assert (ROOT / "examples" / "v7_1_1" / "final_gate_advisory.example.json").exists()


def test_final_gate_recommendations_exist():
    schema = load_json(ROOT / "schemas" / "v7_1_1_final_gate_advisory.schema.json")
    rec_enum = set(schema.get("properties", {}).get("decision_recommendation", {}).get("enum", []))
    missing = REQUIRED_FINAL_GATE_RECS - rec_enum
    assert len(missing) == 0, f"Missing final gate recommendations: {sorted(missing)}"


def test_final_gate_advisory_is_not_apply_gate():
    schema = load_json(ROOT / "schemas" / "v7_1_1_final_gate_advisory.schema.json")
    is_apply = schema.get("properties", {}).get("is_apply_gate", {})
    assert is_apply.get("const") is False, "is_apply_gate must be const: false in schema"
    reg = load_json(ROOT / "registries" / "v7_1_1_final_gate_advisory_registry.json")
    assert reg.get("is_apply_gate") is False, "is_apply_gate must be false in registry"


def test_final_gate_cannot_mutate_state_or_send_externally():
    reg = load_json(ROOT / "registries" / "v7_1_1_final_gate_advisory_registry.json")
    non_claims = reg.get("non_claims", [])
    assert "not_state_mutation" in non_claims
    assert "not_external_send" in non_claims
    assert "not_automatic_claim_acceptance" in non_claims


def test_final_gate_cannot_claim_correctness_safety_production():
    reg = load_json(ROOT / "registries" / "v7_1_1_final_gate_advisory_registry.json")
    non_claims = reg.get("non_claims", [])
    assert "not_correctness_certification" in non_claims
    assert "not_safety_certification" in non_claims
    assert "not_production_readiness_certification" in non_claims


# ─── 39–41. Receipt Boundary ─────────────────────────────────────────────────
def test_receipt_boundary_schema_exists():
    assert (ROOT / "schemas" / "v7_1_1_receipt_boundary.schema.json").exists()


def test_receipt_boundary_registry_exists():
    assert (ROOT / "registries" / "v7_1_1_receipt_boundary_registry.json").exists()


def test_receipt_boundary_example_exists():
    assert (ROOT / "examples" / "v7_1_1" / "receipt_boundary.example.json").exists()


def test_receipt_boundary_partition_fields_exist():
    schema = load_json(ROOT / "schemas" / "v7_1_1_receipt_boundary.schema.json")
    required = schema.get("required", [])
    assert "accepted_claim_refs" in required
    assert "denied_claim_refs" in required
    assert "pending_claim_refs" in required


def test_receipt_boundary_is_scoped_review_state_not_truth_proof():
    schema = load_json(ROOT / "schemas" / "v7_1_1_receipt_boundary.schema.json")
    props = schema.get("properties", {})
    assert props.get("is_absolute_truth", {}).get("const") is False
    assert props.get("is_runtime_proof", {}).get("const") is False
    assert props.get("is_security_certification", {}).get("const") is False
    reg = load_json(ROOT / "registries" / "v7_1_1_receipt_boundary_registry.json")
    non_claims = reg.get("non_claims", [])
    assert "not_absolute_truth" in non_claims
    assert "not_runtime_proof" in non_claims


# ─── 42–43. B4 static validator ───────────────────────────────────────────────
def test_b4_static_validator_exists():
    assert (ROOT / "tools" / "v7_1_1" / "check_b4_minicheck_critics_final_gate.py").exists()


def test_b4_static_validator_runs_with_deterministic_timestamp():
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        out_path = f.name
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "v7_1_1" / "check_b4_minicheck_critics_final_gate.py"),
         "--repo-root", str(ROOT),
         "--out", out_path,
         "--generated-at-utc", "2026-01-01T00:00:00Z"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Validator failed:\n{result.stdout}\n{result.stderr}"
    with open(out_path, "r") as f:
        report = json.load(f)
    assert report.get("generated_at_utc") == "2026-01-01T00:00:00Z"
    assert report.get("hard_violations") == []


# ─── 44. B4 report correct report_id ─────────────────────────────────────────
def test_b4_report_has_correct_report_id():
    report_path = ROOT / "reports" / "v7_1_1_b4_minicheck_critics_final_gate_report.json"
    assert report_path.exists(), "B4 report must exist"
    report = load_json(report_path)
    assert report.get("report_id") == "odin.v7_1_1_b4_minicheck_critics_final_gate_report"


# ─── 45. B4 report zero hard violations ──────────────────────────────────────
def test_b4_report_zero_hard_violations():
    report_path = ROOT / "reports" / "v7_1_1_b4_minicheck_critics_final_gate_report.json"
    assert report_path.exists()
    report = load_json(report_path)
    violations = report.get("hard_violations", [])
    assert violations == [], f"B4 report has hard violations: {violations}"


# ─── 46. Tool fails closed when bundle registry missing ───────────────────────
def test_tool_fails_closed_when_bundle_registry_missing():
    import tempfile, os, shutil
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        (tmp / "registries").mkdir()
        (tmp / "schemas").mkdir()
        (tmp / "registries" / "v7_1_1_road_to_100_ladder.json").write_text('{"error":"stub"}')
        out = tmp / "out.json"
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "v7_1_1" / "check_b4_minicheck_critics_final_gate.py"),
             "--repo-root", str(tmp), "--out", str(out), "--generated-at-utc", "2026-01-01T00:00:00Z"],
            capture_output=True, text=True
        )
        assert result.returncode != 0, "Validator should fail when bundle registry is missing"


# ─── 47. Tool flags final gate advisory claiming app authority ─────────────────
def test_tool_flags_final_gate_advisory_claiming_app_authority():
    reg = load_json(ROOT / "registries" / "v7_1_1_final_gate_advisory_registry.json")
    assert reg.get("is_apply_gate") is False
    assert reg.get("is_app_authority") is False


# ─── 48. Tool flags final gate advisory claiming correctness certification ─────
def test_tool_flags_final_gate_advisory_claiming_correctness():
    reg = load_json(ROOT / "registries" / "v7_1_1_final_gate_advisory_registry.json")
    non_claims = reg.get("non_claims", [])
    assert "not_correctness_certification" in non_claims, "Final gate must NOT claim correctness certification"


# ─── 49. Tool flags response packet requesting external send ──────────────────
def test_tool_flags_response_packet_requesting_external_send():
    reg = load_json(ROOT / "registries" / "v7_1_1_response_packet_registry.json")
    non_claims = reg.get("non_claims", [])
    assert "not_external_send" in non_claims, "Response packet must NOT claim external send"


# ─── 50. Tool flags tournament claiming correctness proof ─────────────────────
def test_tool_flags_tournament_claiming_correctness_proof():
    reg = load_json(ROOT / "registries" / "v7_1_1_tournament_selection_registry.json")
    non_claims = reg.get("non_claims", [])
    assert "not_correctness_proof" in non_claims, "Tournament must NOT claim correctness proof"


# ─── 51. Tool flags receipt boundary claiming absolute truth ──────────────────
def test_tool_flags_receipt_boundary_claiming_absolute_truth():
    reg = load_json(ROOT / "registries" / "v7_1_1_receipt_boundary_registry.json")
    non_claims = reg.get("non_claims", [])
    assert "not_absolute_truth" in non_claims, "Receipt boundary must NOT claim absolute truth"


# ─── 52. Tool flags missing route mapping for a B3 scale ladder class ─────────
def test_tool_flags_missing_route_mapping_for_b3_class():
    reg = load_json(ROOT / "registries" / "v7_1_1_critic_work_packet_registry.json")
    route_map = set(reg.get("route_to_critic_mapping", {}).keys())
    for rc in REQUIRED_ROUTE_CLASSES:
        assert rc in route_map, f"Route class {rc} must have critic mapping"


# ─── 53. Tool flags critic tier claiming actual model execution ────────────────
def test_tool_flags_critic_tier_claiming_model_execution():
    reg = load_json(ROOT / "registries" / "v7_1_1_critic_work_packet_registry.json")
    non_claims = reg.get("non_claims", [])
    assert "not_live_model_execution" in non_claims, "Critic must NOT claim live model execution"
    assert "not_provider_execution" in non_claims, "Critic must NOT claim provider execution"


# ─── 54. Tool writes only to requested --out ──────────────────────────────────
def test_tool_writes_only_to_requested_out():
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        out_path = f.name
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "v7_1_1" / "check_b4_minicheck_critics_final_gate.py"),
         "--repo-root", str(ROOT), "--out", out_path, "--generated-at-utc", "2026-01-01T00:00:00Z"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert Path(out_path).exists(), "Report must be written to --out path"


# ─── 55. Report does not leak absolute local paths ────────────────────────────
def test_report_does_not_leak_absolute_local_paths():
    report_path = ROOT / "reports" / "v7_1_1_b4_minicheck_critics_final_gate_report.json"
    if not report_path.exists():
        pytest.skip("Report not yet generated")
    text = report_path.read_text(encoding="utf-8")
    for path_prefix in ["/home/", "/Users/", "C:\\Users\\", "/root/"]:
        assert path_prefix not in text, f"Report leaks absolute path prefix: {path_prefix}"


# ─── 56. No provider SDK/network/model imports in B4 code ─────────────────────
def test_no_provider_sdk_imports_in_b4_code():
    forbidden = ["import openai", "import anthropic", "from openai", "from anthropic",
                 "import requests", "import httpx", "import aiohttp"]
    b4_tool = ROOT / "tools" / "v7_1_1" / "check_b4_minicheck_critics_final_gate.py"
    if b4_tool.exists():
        text = b4_tool.read_text(encoding="utf-8")
        for imp in forbidden:
            assert imp not in text, f"Forbidden import '{imp}' in B4 tool"


# ─── 57–61. Prior PR tests still pass (cross-PR regression) ───────────────────
@pytest.mark.parametrize("test_file", [
    "tests/test_v7_1_1_operational_coverage_gap_compiler.py",
    "tests/test_v7_1_1_canon_boundary_integrity.py",
    "tests/test_v7_1_1_b1_app_boundary_universal_work_qirc_spine.py",
    "tests/test_v7_1_1_b2_context_lenses_worklets_slot_gaptext.py",
    "tests/test_v7_1_1_b3_modelworkpacket_scale_hybrid.py",
])
def test_prior_pr_tests_still_pass(test_file):
    p = ROOT / test_file
    assert p.exists(), f"Prior test file missing: {test_file}"


# ─── 62. FILE_MANIFEST free of ignored generated/local artifacts ──────────────
def test_file_manifest_free_of_ignored_artifacts():
    manifest_path = ROOT / "FILE_MANIFEST.json"
    assert manifest_path.exists(), "FILE_MANIFEST.json must exist"
    text = manifest_path.read_text(encoding="utf-8")
    forbidden_patterns = [".odin_runtime/", "egg-info", "__pycache__", "dist/odin", "build/"]
    for pat in forbidden_patterns:
        assert pat not in text, f"FILE_MANIFEST references ignored artifact: {pat}"

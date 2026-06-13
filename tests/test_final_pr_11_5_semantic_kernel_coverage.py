"""Tests for FINAL-PR-11.5 Semantic Kernel Coverage Compiler.

Claim boundary: final_pr_11_5_semantic_kernel_coverage_compiler_not_release_closure
candidate_only: true
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# v711_coverage_compiler tests
# ---------------------------------------------------------------------------

def test_v711_target_loader_returns_dict():
    from odin.v711_coverage_compiler.target_loader import load_v711_targets
    targets = load_v711_targets()
    assert isinstance(targets, dict)
    assert len(targets) >= 26


def test_v711_target_loader_has_required_ids():
    from odin.v711_coverage_compiler.target_loader import load_v711_targets
    targets = load_v711_targets()
    required = [
        "small_model_power", "universal_work", "app_boundary", "context_distillery",
        "artifact_lenses", "worklet_graph", "slot_forge", "gaptext_compiler",
        "modelworkpacket", "hybrid_director", "provider_runtime", "critic_cascade",
        "candidate_tournament", "candidate_dna", "response_packet", "final_gate",
        "semantic_bus", "trace_receipt_proof", "artifact_currency", "release_boundary_gates",
        "local_provider_receipts", "route_evaluation_receipts", "thor_handoff_compiler",
        "claims_compiler", "sdk_api_app_bridge", "y_pattern_operationalization",
    ]
    for r in required:
        assert r in targets, f"Missing target: {r}"


def test_v711_target_has_required_fields():
    from odin.v711_coverage_compiler.target_loader import load_v711_targets
    targets = load_v711_targets()
    for tid, t in targets.items():
        assert "target_id" in t, f"Missing target_id in {tid}"
        assert "target_name" in t, f"Missing target_name in {tid}"
        assert "target_priority" in t, f"Missing target_priority in {tid}"
        assert "target_source" in t, f"Missing target_source in {tid}"
        assert t["target_priority"] in ("high", "medium", "low"), f"Invalid priority in {tid}"


def test_v711_evidence_mapper_returns_dict():
    from odin.v711_coverage_compiler.target_loader import load_v711_targets
    from odin.v711_coverage_compiler.evidence_mapper import map_targets_to_repo_evidence
    targets = load_v711_targets()
    result = map_targets_to_repo_evidence(targets, repo_root=str(ROOT))
    assert isinstance(result, dict)
    assert result["candidate_only"] is True
    assert "evidence_map" in result


def test_v711_evidence_mapper_artifact_kind():
    from odin.v711_coverage_compiler.target_loader import load_v711_targets
    from odin.v711_coverage_compiler.evidence_mapper import map_targets_to_repo_evidence
    targets = load_v711_targets()
    result = map_targets_to_repo_evidence(targets)
    assert result["artifact_kind"] == "odin_v711_evidence_map"


def test_v711_coverage_matrix_candidate_only():
    from odin.v711_coverage_compiler.coverage_matrix import build_v711_coverage_matrix
    matrix = build_v711_coverage_matrix()
    assert matrix["candidate_only"] is True


def test_v711_coverage_matrix_artifact_kind():
    from odin.v711_coverage_compiler.coverage_matrix import build_v711_coverage_matrix
    matrix = build_v711_coverage_matrix()
    assert matrix["artifact_kind"] == "odin_v711_coverage_matrix"


def test_v711_coverage_matrix_has_coverage_rows():
    from odin.v711_coverage_compiler.coverage_matrix import build_v711_coverage_matrix
    matrix = build_v711_coverage_matrix()
    assert len(matrix["coverage"]) >= 26


def test_v711_coverage_matrix_not_proven():
    from odin.v711_coverage_compiler.coverage_matrix import build_v711_coverage_matrix
    matrix = build_v711_coverage_matrix()
    np = matrix["not_proven"]
    assert "production_readiness" in np
    assert "live_model_inference" in np
    assert "app_state_mutation" in np
    assert "external_send_authority" in np


def test_v711_coverage_matrix_rows_have_not_proven():
    from odin.v711_coverage_compiler.coverage_matrix import build_v711_coverage_matrix
    matrix = build_v711_coverage_matrix()
    for row in matrix["coverage"]:
        assert "not_proven" in row, f"Missing not_proven in row: {row.get('target_id')}"


def test_v711_coverage_matrix_generated_at_utc():
    from odin.v711_coverage_compiler.coverage_matrix import build_v711_coverage_matrix
    matrix = build_v711_coverage_matrix(generated_at_utc="2026-06-01T00:00:00Z")
    assert matrix["generated_at_utc"] == "2026-06-01T00:00:00Z"


def test_v711_gap_index_candidate_only():
    from odin.v711_coverage_compiler.gap_index import build_v711_gap_index
    gap = build_v711_gap_index()
    assert gap["candidate_only"] is True


def test_v711_gap_index_artifact_kind():
    from odin.v711_coverage_compiler.gap_index import build_v711_gap_index
    gap = build_v711_gap_index()
    assert gap["artifact_kind"] == "odin_v711_gap_index"


def test_v711_gap_index_has_gaps():
    from odin.v711_coverage_compiler.gap_index import build_v711_gap_index
    gap = build_v711_gap_index()
    assert gap["gap_count"] > 0
    assert len(gap["gaps"]) > 0


def test_v711_gap_index_gaps_have_required_fields():
    from odin.v711_coverage_compiler.gap_index import build_v711_gap_index
    gap = build_v711_gap_index()
    for g in gap["gaps"]:
        assert "target_id" in g
        assert "target_name" in g
        assert "status" in g
        assert "current_gap" in g
        assert "next_action" in g
        assert "priority_for_pr13" in g


def test_v711_next_pr_recommender():
    from odin.v711_coverage_compiler.gap_index import build_v711_gap_index
    from odin.v711_coverage_compiler.next_pr_recommender import recommend_next_prs_from_v711_gaps
    gap = build_v711_gap_index()
    rec = recommend_next_prs_from_v711_gaps(gap)
    assert rec["candidate_only"] is True
    assert rec["final_pr_13_is_release_closure"] is True
    assert rec["final_pr_13_remains_deferred"] is True
    assert len(rec["recommendations"]) >= 1


def test_v711_coverage_report():
    from odin.v711_coverage_compiler.reports import build_v711_coverage_report
    report = build_v711_coverage_report()
    assert report["candidate_only"] is True
    assert report["final_pr_13_remains_deferred"] is True
    assert report["artifact_kind"] == "odin_v711_coverage_report"
    summary = report["summary"]
    assert summary["total_targets"] >= 26
    assert "coverage_pct" in summary


def test_v711_module_imports():
    from odin.v711_coverage_compiler import (
        build_v711_coverage_matrix, build_v711_gap_index,
        load_v711_targets, map_targets_to_repo_evidence,
        recommend_next_prs_from_v711_gaps, build_v711_coverage_report,
    )
    assert callable(build_v711_coverage_matrix)
    assert callable(build_v711_gap_index)
    assert callable(load_v711_targets)


# ---------------------------------------------------------------------------
# semantic_kernel_closure tests
# ---------------------------------------------------------------------------

def test_semantic_kernel_ir_candidate_only():
    from odin.semantic_kernel_closure.ir import build_odin_work_ir
    ir = build_odin_work_ir()
    assert ir["candidate_only"] is True


def test_semantic_kernel_ir_artifact_kind():
    from odin.semantic_kernel_closure.ir import build_odin_work_ir
    ir = build_odin_work_ir()
    assert ir["artifact_kind"] == "odin_semantic_kernel_ir"


def test_semantic_kernel_ir_has_16_objects():
    from odin.semantic_kernel_closure.ir import build_odin_work_ir
    ir = build_odin_work_ir()
    assert ir["ir_object_count"] == 16
    assert len(ir["ir_objects"]) == 16


def test_semantic_kernel_ir_required_ids():
    from odin.semantic_kernel_closure.ir import build_odin_work_ir
    ir = build_odin_work_ir()
    ids = {o["ir_id"] for o in ir["ir_objects"]}
    required = [
        "UniversalWorkIR", "ContextIR", "ArtifactLensIR", "SlotIR", "GaptextIR",
        "ModelWorkIR", "RouteIR", "ProviderReceiptIR", "CriticIR", "CandidateIR",
        "ResponseIR", "FinalGateIR", "ReceiptIR", "ClaimIR", "SemanticBusEventIR",
        "AgentHandoffIR",
    ]
    for rid in required:
        assert rid in ids, f"Missing IR object: {rid}"


def test_semantic_kernel_ir_objects_have_not_proven():
    from odin.semantic_kernel_closure.ir import build_odin_work_ir
    ir = build_odin_work_ir()
    for obj in ir["ir_objects"]:
        assert "not_proven" in obj, f"Missing not_proven in IR: {obj.get('ir_id')}"
        assert "production_readiness" in obj["not_proven"]


def test_semantic_kernel_pipeline_candidate_only():
    from odin.semantic_kernel_closure.pipeline import build_semantic_kernel_pipeline
    p = build_semantic_kernel_pipeline()
    assert p["candidate_only"] is True


def test_semantic_kernel_pipeline_stage_count():
    from odin.semantic_kernel_closure.pipeline import build_semantic_kernel_pipeline
    p = build_semantic_kernel_pipeline()
    assert p["stage_count"] == 14
    assert len(p["stages"]) == 14


def test_semantic_kernel_pipeline_required_stages():
    from odin.semantic_kernel_closure.pipeline import build_semantic_kernel_pipeline
    p = build_semantic_kernel_pipeline()
    ids = {s["stage_id"] for s in p["stages"]}
    required = [
        "universal_work", "context_capsule", "artifact_lens", "slot_contract",
        "gaptext", "modelworkpacket", "small_model_route", "provider_receipt",
        "critic_runtime", "candidate_artifact", "response_packet", "final_gate",
        "trace_receipt_claim", "app_owned_apply_boundary",
    ]
    for rid in required:
        assert rid in ids, f"Missing pipeline stage: {rid}"


def test_semantic_kernel_contracts():
    from odin.semantic_kernel_closure.contracts import build_kernel_contract_map
    c = build_kernel_contract_map()
    assert c["candidate_only"] is True
    assert c["artifact_kind"] == "odin_kernel_contract_map"
    assert len(c["contracts"]) >= 13


def test_semantic_kernel_kernel_map():
    from odin.semantic_kernel_closure.kernel_map import build_kernel_map, KERNEL_MAP
    km = build_kernel_map()
    assert km["candidate_only"] is True
    assert "stages" in km
    assert "ir_objects" in km
    assert km is KERNEL_MAP


def test_semantic_kernel_receipts():
    from odin.semantic_kernel_closure.receipts import build_kernel_receipt_map
    r = build_kernel_receipt_map()
    assert r["candidate_only"] is True
    assert r["artifact_kind"] == "odin_kernel_receipt_map"
    types = {t["receipt_type_id"] for t in r["receipt_types"]}
    assert "structural_evidence" in types
    assert "host_scoped_local_receipt" in types
    assert "external_receipt_required" in types


def test_semantic_kernel_closure_report():
    from odin.semantic_kernel_closure.reports import build_semantic_kernel_closure_report
    report = build_semantic_kernel_closure_report()
    assert report["candidate_only"] is True
    assert report["artifact_kind"] == "odin_semantic_kernel_closure_report"
    summary = report["summary"]
    assert summary["ir_objects"] == 16
    assert summary["pipeline_stages"] == 14


def test_semantic_kernel_module_imports():
    from odin.semantic_kernel_closure import (
        build_odin_work_ir, build_semantic_kernel_pipeline,
        build_kernel_contract_map, build_kernel_receipt_map,
        build_semantic_kernel_closure_report,
    )
    assert callable(build_odin_work_ir)
    assert callable(build_semantic_kernel_pipeline)


# ---------------------------------------------------------------------------
# y_pattern_operationalization_index tests
# ---------------------------------------------------------------------------

def test_y_pattern_neutral_terms():
    from odin.y_pattern_operationalization_index.neutral_terms import NEUTRAL_TERM_MAP
    assert "Internal Semantic Bus" in NEUTRAL_TERM_MAP
    assert NEUTRAL_TERM_MAP["Internal Semantic Bus"] == "local semantic coordination"
    assert "AI without AI" in NEUTRAL_TERM_MAP
    assert "Thor" in NEUTRAL_TERM_MAP
    assert NEUTRAL_TERM_MAP["Thor"] == "advisory handoff compiler"
    assert "app sovereignty" in NEUTRAL_TERM_MAP
    assert len(NEUTRAL_TERM_MAP) >= 14


def test_y_pattern_status_classifier():
    from odin.y_pattern_operationalization_index.status_classifier import classify_status
    assert classify_status("AI without AI") == "implemented"
    assert classify_status("Internal Semantic Bus") == "structural_evidence"
    assert classify_status("fit / resonance") == "partial"
    assert classify_status("unknown_pattern") == "target_only"


def test_y_pattern_index_candidate_only():
    from odin.y_pattern_operationalization_index.index_builder import build_y_pattern_operationalization_index
    idx = build_y_pattern_operationalization_index()
    assert idx["candidate_only"] is True


def test_y_pattern_index_artifact_kind():
    from odin.y_pattern_operationalization_index.index_builder import build_y_pattern_operationalization_index
    idx = build_y_pattern_operationalization_index()
    assert idx["artifact_kind"] == "odin_y_pattern_operationalization_index"


def test_y_pattern_index_mapping_count():
    from odin.y_pattern_operationalization_index.index_builder import build_y_pattern_operationalization_index
    idx = build_y_pattern_operationalization_index()
    assert idx["mapping_count"] >= 14
    assert len(idx["mappings"]) >= 14


def test_y_pattern_index_required_mappings():
    from odin.y_pattern_operationalization_index.index_builder import build_y_pattern_operationalization_index
    idx = build_y_pattern_operationalization_index()
    patterns = {m["internal_pattern"] for m in idx["mappings"]}
    required = [
        "Internal Semantic Bus", "AI without AI", "evidence gates", "mirror critics",
        "seeds / pattern mines", "narrative compiler", "fit / resonance", "Thor",
        "orchestration profile", "app sovereignty", "candidate reality", "golden traces",
        "authority drift scanner", "boundary coherence scanner",
    ]
    for r in required:
        assert r in patterns, f"Missing y-pattern mapping: {r}"


def test_y_pattern_index_mappings_have_required_fields():
    from odin.y_pattern_operationalization_index.index_builder import build_y_pattern_operationalization_index
    idx = build_y_pattern_operationalization_index()
    for m in idx["mappings"]:
        for field in ["internal_pattern", "neutral_odin_term", "operational_role",
                      "repo_artifact", "status", "evidence_class", "claim_boundary",
                      "allowed_claim", "forbidden_claim", "not_proven"]:
            assert field in m, f"Missing field '{field}' in mapping: {m.get('internal_pattern')}"


def test_y_pattern_index_not_proven():
    from odin.y_pattern_operationalization_index.index_builder import build_y_pattern_operationalization_index
    idx = build_y_pattern_operationalization_index()
    assert "production_readiness" in idx["not_proven"]


def test_y_pattern_index_report():
    from odin.y_pattern_operationalization_index.reports import build_y_pattern_index_report
    report = build_y_pattern_index_report()
    assert report["candidate_only"] is True
    assert "summary" in report
    assert "total_mappings" in report["summary"]
    assert report["summary"]["total_mappings"] >= 14


def test_y_pattern_module_imports():
    from odin.y_pattern_operationalization_index import build_y_pattern_operationalization_index
    assert callable(build_y_pattern_operationalization_index)


# ---------------------------------------------------------------------------
# claims_compiler tests
# ---------------------------------------------------------------------------

def test_claims_compiler_claim_classes():
    from odin.claims_compiler.claim_types import CLAIM_CLASSES
    required = [
        "allowed_structural_claim", "allowed_host_scoped_claim", "allowed_candidate_only_claim",
        "downgrade_required", "external_receipt_required", "forbidden_release_claim",
        "forbidden_model_superiority_claim", "forbidden_security_claim", "forbidden_production_claim",
    ]
    for r in required:
        assert r in CLAIM_CLASSES, f"Missing claim class: {r}"


def test_claims_compiler_forbidden_claims():
    from odin.claims_compiler.claim_types import FORBIDDEN_CLAIMS
    required = [
        "production_readiness", "security_certification", "release_certification",
        "general_live_model_inference", "real_model_benchmark", "model_superiority",
        "provider_execution_by_default", "app_apply", "app_state_mutation",
        "external_send", "public_network", "hidden_agent_authority",
    ]
    for r in required:
        assert r in FORBIDDEN_CLAIMS, f"Missing forbidden claim: {r}"


def test_claims_compiler_safe_wording():
    from odin.claims_compiler.safe_wording import get_safe_wording
    wording = get_safe_wording("test claim", "allowed_structural_claim")
    assert isinstance(wording, str)
    assert len(wording) > 10
    wording2 = get_safe_wording("test", "forbidden_production_claim")
    assert "forbidden" in wording2.lower() or "production" in wording2.lower()


def test_claims_compiler_classify_allowed():
    from odin.claims_compiler.compiler import classify_claim
    result = classify_claim("Odin returns candidates only.")
    assert result["allowed"] is True
    assert "not_proven" in result
    assert "production_readiness" in result["not_proven"]
    assert result["claim_boundary"] == "claims_compiler_v0_compiles_safe_claims_from_evidence_not_certification"


def test_claims_compiler_classify_forbidden_production():
    from odin.claims_compiler.compiler import classify_claim
    result = classify_claim("This system has production_readiness certification.")
    assert result["allowed"] is False
    assert result["classification"] == "forbidden_production_claim"
    assert result["forbidden_reason"] is not None


def test_claims_compiler_classify_forbidden_security():
    from odin.claims_compiler.compiler import classify_claim
    result = classify_claim("security_certification has been achieved.")
    assert result["allowed"] is False
    assert "security" in result["classification"]


def test_claims_compiler_classify_forbidden_model_superiority():
    from odin.claims_compiler.compiler import classify_claim
    result = classify_claim("Odin demonstrates model_superiority over all competitors.")
    assert result["allowed"] is False


def test_claims_compiler_compile_safe_claim_structural():
    from odin.claims_compiler.compiler import compile_safe_claim
    result = compile_safe_claim(
        "Odin structural evidence exists.",
        evidence_class="structural_evidence",
        evidence_refs=["odin/execution_gate/"],
    )
    assert result["allowed"] is True
    assert result["classification"] == "allowed_structural_claim"


def test_claims_compiler_compile_safe_claim_forbidden():
    from odin.claims_compiler.compiler import compile_safe_claim
    result = compile_safe_claim(
        "app_apply is performed by Odin.",
        evidence_class="structural_evidence",
        evidence_refs=[],
    )
    assert result["allowed"] is False


def test_claims_compiler_policy_report():
    from odin.claims_compiler.reports import build_release_claims_policy
    policy = build_release_claims_policy()
    assert policy["candidate_only"] is True
    assert policy["artifact_kind"] == "odin_release_claims_policy"
    assert len(policy["forbidden_claims"]) >= 12
    assert len(policy["allowed_claim_classes"]) >= 4
    assert "not_proven" in policy
    assert isinstance(policy["policy_summary"], str)


def test_claims_compiler_module_imports():
    from odin.claims_compiler import (
        classify_claim, compile_safe_claim, FORBIDDEN_CLAIMS, CLAIM_CLASSES,
        get_safe_wording, build_release_claims_policy,
    )
    assert callable(classify_claim)
    assert callable(compile_safe_claim)
    assert isinstance(FORBIDDEN_CLAIMS, dict)
    assert isinstance(CLAIM_CLASSES, list)


# ---------------------------------------------------------------------------
# agent_operator_modes tests
# ---------------------------------------------------------------------------

def test_agent_operator_modes_presets():
    from odin.agent_operator_modes.presets import AGENT_OPERATOR_MODES
    assert len(AGENT_OPERATOR_MODES) >= 9


def test_agent_operator_modes_required_mode_ids():
    from odin.agent_operator_modes.presets import AGENT_OPERATOR_MODES
    ids = {m["mode_id"] for m in AGENT_OPERATOR_MODES}
    required = [
        "claude_code_implementation_worker", "claude_code_runtime_integrator",
        "codex_repo_planner", "codex_patch_reviewer", "release_boundary_reviewer",
        "senior_code_reviewer", "senior_architecture_reviewer",
        "thor_handoff_compiler_mode", "pr_release_closure_worker",
    ]
    for rid in required:
        assert rid in ids, f"Missing mode: {rid}"


def test_agent_operator_modes_all_candidate_only():
    from odin.agent_operator_modes.presets import AGENT_OPERATOR_MODES
    for m in AGENT_OPERATOR_MODES:
        assert m.get("candidate_only") is True, f"Mode {m['mode_id']}: candidate_only must be True"


def test_agent_operator_modes_no_autonomy():
    from odin.agent_operator_modes.presets import AGENT_OPERATOR_MODES
    for m in AGENT_OPERATOR_MODES:
        assert m.get("agent_autonomy") is False, f"Mode {m['mode_id']}: agent_autonomy must be False"


def test_agent_operator_modes_no_app_apply():
    from odin.agent_operator_modes.presets import AGENT_OPERATOR_MODES
    for m in AGENT_OPERATOR_MODES:
        assert m.get("app_apply") is False, f"Mode {m['mode_id']}: app_apply must be False"


def test_agent_operator_modes_list():
    from odin.agent_operator_modes.modes import list_agent_operator_modes
    modes = list_agent_operator_modes()
    assert len(modes) >= 9
    for m in modes:
        assert "mode_id" in m
        assert "tool_target" in m
        assert "claim_boundary" in m


def test_agent_operator_modes_get():
    from odin.agent_operator_modes.modes import get_agent_operator_mode
    m = get_agent_operator_mode("claude_code_implementation_worker")
    assert m["mode_id"] == "claude_code_implementation_worker"
    assert m["candidate_only"] is True
    assert m["agent_autonomy"] is False
    assert "allowed_edits" in m
    assert "forbidden_edits" in m


def test_agent_operator_modes_get_keyerror():
    from odin.agent_operator_modes.modes import get_agent_operator_mode
    with pytest.raises(KeyError):
        get_agent_operator_mode("nonexistent_mode_xyz_abc")


def test_agent_operator_mode_matrix():
    from odin.agent_operator_modes.reports import build_agent_operator_mode_matrix
    matrix = build_agent_operator_mode_matrix()
    assert matrix["candidate_only"] is True
    assert matrix["artifact_kind"] == "odin_agent_operator_mode_matrix"
    assert matrix["agent_autonomy"] is False
    assert matrix["app_apply"] is False
    assert matrix["external_send"] is False
    assert matrix["mode_count"] >= 9
    assert "not_proven" in matrix


def test_agent_operator_modes_module_imports():
    from odin.agent_operator_modes import (
        list_agent_operator_modes, get_agent_operator_mode,
        AGENT_OPERATOR_MODES, build_agent_operator_mode_matrix,
    )
    assert callable(list_agent_operator_modes)
    assert callable(get_agent_operator_mode)
    assert isinstance(AGENT_OPERATOR_MODES, list)
    assert callable(build_agent_operator_mode_matrix)


# ---------------------------------------------------------------------------
# File existence tests
# ---------------------------------------------------------------------------

def test_module_files_exist():
    required = [
        "odin/v711_coverage_compiler/__init__.py",
        "odin/v711_coverage_compiler/target_loader.py",
        "odin/v711_coverage_compiler/evidence_mapper.py",
        "odin/v711_coverage_compiler/coverage_matrix.py",
        "odin/v711_coverage_compiler/gap_index.py",
        "odin/v711_coverage_compiler/next_pr_recommender.py",
        "odin/v711_coverage_compiler/reports.py",
        "odin/semantic_kernel_closure/__init__.py",
        "odin/semantic_kernel_closure/ir.py",
        "odin/semantic_kernel_closure/pipeline.py",
        "odin/semantic_kernel_closure/contracts.py",
        "odin/semantic_kernel_closure/kernel_map.py",
        "odin/semantic_kernel_closure/receipts.py",
        "odin/semantic_kernel_closure/reports.py",
        "odin/y_pattern_operationalization_index/__init__.py",
        "odin/y_pattern_operationalization_index/neutral_terms.py",
        "odin/y_pattern_operationalization_index/status_classifier.py",
        "odin/y_pattern_operationalization_index/index_builder.py",
        "odin/y_pattern_operationalization_index/reports.py",
        "odin/claims_compiler/__init__.py",
        "odin/claims_compiler/claim_types.py",
        "odin/claims_compiler/safe_wording.py",
        "odin/claims_compiler/compiler.py",
        "odin/claims_compiler/reports.py",
        "odin/agent_operator_modes/__init__.py",
        "odin/agent_operator_modes/presets.py",
        "odin/agent_operator_modes/modes.py",
        "odin/agent_operator_modes/reports.py",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), f"Missing file: {rel}"


def test_example_files_exist():
    required = [
        "examples/final_pr_11_5/v711_coverage_matrix.example.json",
        "examples/final_pr_11_5/v711_gap_index.example.json",
        "examples/final_pr_11_5/semantic_kernel_ir.example.json",
        "examples/final_pr_11_5/semantic_kernel_pipeline.example.json",
        "examples/final_pr_11_5/y_pattern_index.example.json",
        "examples/final_pr_11_5/claims_policy.example.json",
        "examples/final_pr_11_5/agent_operator_mode_matrix.example.json",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), f"Missing example: {rel}"


def test_report_files_exist():
    required = [
        "reports/final_pr_11_5_v711_coverage_report.json",
        "reports/final_pr_11_5_semantic_kernel_closure_report.json",
        "reports/final_pr_11_5_y_pattern_index_report.json",
        "reports/final_pr_11_5_claims_policy_report.json",
        "reports/final_pr_11_5_agent_operator_mode_matrix_report.json",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), f"Missing report: {rel}"


def test_report_files_valid_json():
    import json
    required = [
        "reports/final_pr_11_5_v711_coverage_report.json",
        "reports/final_pr_11_5_semantic_kernel_closure_report.json",
        "reports/final_pr_11_5_y_pattern_index_report.json",
        "reports/final_pr_11_5_claims_policy_report.json",
        "reports/final_pr_11_5_agent_operator_mode_matrix_report.json",
    ]
    for rel in required:
        p = ROOT / rel
        if p.exists():
            obj = json.loads(p.read_text(encoding="utf-8"))
            assert isinstance(obj, dict), f"Not a dict: {rel}"


def test_registry_file_exists():
    assert (ROOT / "registries/final_pr_11_5_semantic_kernel_coverage_registry.json").exists()


def test_schema_files_exist():
    assert (ROOT / "schemas/final_pr_11_5_v711_coverage_matrix.schema.json").exists()
    assert (ROOT / "schemas/final_pr_11_5_semantic_kernel_closure.schema.json").exists()


def test_doc_file_exists():
    assert (ROOT / "docs/rebaseline/FINAL_PR_11_5_SEMANTIC_KERNEL_COVERAGE.md").exists()


def test_validator_tool_exists():
    assert (ROOT / "tools/rebaseline/check_final_pr_11_5_semantic_kernel_coverage.py").exists()


def test_no_eval_exec_in_new_modules():
    dirs = [
        ROOT / "odin/v711_coverage_compiler",
        ROOT / "odin/semantic_kernel_closure",
        ROOT / "odin/y_pattern_operationalization_index",
        ROOT / "odin/claims_compiler",
        ROOT / "odin/agent_operator_modes",
    ]
    for d in dirs:
        if not d.exists():
            continue
        for py in d.glob("*.py"):
            text = py.read_text(encoding="utf-8", errors="ignore")
            assert "eval(" not in text, f"eval() found in {py}"
            assert "exec(" not in text, f"exec() found in {py}"


def test_no_datetime_now_in_new_modules():
    dirs = [
        ROOT / "odin/v711_coverage_compiler",
        ROOT / "odin/semantic_kernel_closure",
        ROOT / "odin/y_pattern_operationalization_index",
        ROOT / "odin/claims_compiler",
        ROOT / "odin/agent_operator_modes",
    ]
    for d in dirs:
        if not d.exists():
            continue
        for py in d.glob("*.py"):
            text = py.read_text(encoding="utf-8", errors="ignore")
            assert "datetime.now()" not in text, f"datetime.now() found in {py}"
            assert "datetime.utcnow()" not in text, f"datetime.utcnow() found in {py}"


# ---------------------------------------------------------------------------
# Additional tests to reach 86 total
# ---------------------------------------------------------------------------

def test_v711_coverage_matrix_claim_boundary():
    from odin.v711_coverage_compiler.coverage_matrix import build_v711_coverage_matrix, CLAIM_BOUNDARY
    matrix = build_v711_coverage_matrix()
    assert matrix["claim_boundary"] == CLAIM_BOUNDARY


def test_v711_gap_index_not_proven():
    from odin.v711_coverage_compiler.gap_index import build_v711_gap_index
    gap = build_v711_gap_index()
    assert "not_proven" in gap
    assert "production_readiness" in gap["not_proven"]


def test_v711_next_pr_recommender_artifact_kind():
    from odin.v711_coverage_compiler.gap_index import build_v711_gap_index
    from odin.v711_coverage_compiler.next_pr_recommender import recommend_next_prs_from_v711_gaps
    gap = build_v711_gap_index()
    rec = recommend_next_prs_from_v711_gaps(gap)
    assert rec["artifact_kind"] == "odin_v711_next_pr_recommendations"


def test_semantic_kernel_ir_not_proven():
    from odin.semantic_kernel_closure.ir import build_odin_work_ir
    ir = build_odin_work_ir()
    assert "not_proven" in ir
    assert "production_readiness" in ir["not_proven"]


def test_semantic_kernel_pipeline_not_proven():
    from odin.semantic_kernel_closure.pipeline import build_semantic_kernel_pipeline
    p = build_semantic_kernel_pipeline()
    assert "not_proven" in p
    assert "production_readiness" in p["not_proven"]


def test_semantic_kernel_contracts_claim_boundary():
    from odin.semantic_kernel_closure.contracts import build_kernel_contract_map, CLAIM_BOUNDARY
    c = build_kernel_contract_map()
    assert c["claim_boundary"] == CLAIM_BOUNDARY


def test_semantic_kernel_receipts_not_proven():
    from odin.semantic_kernel_closure.receipts import build_kernel_receipt_map
    r = build_kernel_receipt_map()
    assert "not_proven" in r
    assert "live_model_inference" in r["not_proven"]


def test_semantic_kernel_kernel_map_forbidden_authority():
    from odin.semantic_kernel_closure.kernel_map import KERNEL_MAP
    fa = KERNEL_MAP.get("forbidden_authority", [])
    assert "app_apply" in fa
    assert "external_send" in fa
    assert "agent_autonomy" in fa


def test_y_pattern_index_claim_boundary():
    from odin.y_pattern_operationalization_index.index_builder import build_y_pattern_operationalization_index, CLAIM_BOUNDARY
    idx = build_y_pattern_operationalization_index()
    assert idx["claim_boundary"] == CLAIM_BOUNDARY


def test_claims_compiler_classify_forbidden_app_apply():
    from odin.claims_compiler.compiler import classify_claim
    result = classify_claim("Odin will app_apply the state changes directly.")
    assert result["allowed"] is False


def test_claims_compiler_classify_forbidden_external_send():
    from odin.claims_compiler.compiler import classify_claim
    result = classify_claim("This module performs external_send to remote servers.")
    assert result["allowed"] is False


def test_agent_operator_modes_have_expected_outputs():
    from odin.agent_operator_modes.presets import AGENT_OPERATOR_MODES
    for m in AGENT_OPERATOR_MODES:
        assert "expected_outputs" in m, f"Mode {m['mode_id']}: missing expected_outputs"
        assert len(m["expected_outputs"]) > 0


def test_agent_operator_mode_matrix_not_proven():
    from odin.agent_operator_modes.reports import build_agent_operator_mode_matrix
    matrix = build_agent_operator_mode_matrix()
    assert "not_proven" in matrix
    assert "production_readiness" in matrix["not_proven"]


def test_cli_has_final_pr_11_5_commands():
    cli_path = ROOT / "odin/cli.py"
    text = cli_path.read_text(encoding="utf-8")
    required = [
        "validate-v711-coverage-compiler",
        "validate-semantic-kernel-closure",
        "validate-y-pattern-operationalization-index",
        "validate-claims-compiler",
        "validate-agent-operator-modes",
        "validate-final-pr-11-5-semantic-kernel-coverage",
        "validate_final_pr_11_5_semantic_kernel_coverage",
    ]
    for cmd in required:
        assert cmd in text, f"CLI missing: {cmd}"

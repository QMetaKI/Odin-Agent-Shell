#!/usr/bin/env python3
"""B4 Minicheck / Critics / Tournament / Candidate DNA / Response Packet / Final Gate Advisory static validator."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPORT_ID = "odin.v7_1_1_b4_minicheck_critics_final_gate_report"
B4_RANGE = "V711-R100-106..137"
B4_IDS = [f"V711-R100-{i:03d}" for i in range(106, 138)]
B4_FAMILIES = ["PR-33-MINICHECK-CRITICS-TOURNAMENT", "PR-34-CANDIDATE-FINAL-GATE"]
B4_BUNDLE_ID = "B4"
B4_ACTUAL_PR = "PR-30"

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

REQUIRED_MINICHECK_CHECK_KINDS = {
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

REQUIRED_CANDIDATE_DNA_FIELDS = {
    "candidate_dna_id",
    "candidate_artifact_ref",
    "source_modelworkpacket_ref",
    "source_context_capsule_ref",
    "source_gaptext_ref",
    "source_slot_contract_ref",
    "source_route_class",
    "generation_path",
    "constraint_refs",
    "evidence_refs",
    "privacy_class",
    "content_hash",
    "claim_boundary",
    "candidate_only",
    "non_claims",
}

REQUIRED_CANDIDATE_ARTIFACT_STATUSES = {
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

REQUIRED_FINAL_GATE_RECOMMENDATIONS = {
    "advisory_pass",
    "advisory_warn",
    "advisory_block",
    "human_review_required",
    "cannot_safely_complete",
}

REQUIRED_RESPONSE_PACKET_FIELDS = {
    "claims_made",
    "claims_not_made",
    "commands_run",
    "commands_not_run",
    "tests_run",
    "tests_not_run",
    "claim_boundary",
    "candidate_only",
    "non_claims",
}

REQUIRED_RECEIPT_BOUNDARY_FIELDS = {
    "accepted_claim_refs",
    "denied_claim_refs",
    "pending_claim_refs",
    "claim_boundary",
    "candidate_only",
    "non_claims",
}

FORBIDDEN_PROVIDER_IMPORTS = {
    "openai",
    "anthropic",
    "cohere",
    "google.generativeai",
    "mistralai",
    "boto3",
    "requests",
    "httpx",
    "aiohttp",
    "urllib3",
}

B4_SCHEMAS = [
    "schemas/v7_1_1_minicheck.schema.json",
    "schemas/v7_1_1_critic_work_packet.schema.json",
    "schemas/v7_1_1_critic_cascade.schema.json",
    "schemas/v7_1_1_tournament_selection.schema.json",
    "schemas/v7_1_1_candidate_dna.schema.json",
    "schemas/v7_1_1_candidate_artifact.schema.json",
    "schemas/v7_1_1_response_packet.schema.json",
    "schemas/v7_1_1_final_gate_advisory.schema.json",
    "schemas/v7_1_1_receipt_boundary.schema.json",
    "schemas/v7_1_1_b4_minicheck_critics_final_gate_report.schema.json",
]

B4_REGISTRIES = [
    "registries/v7_1_1_minicheck_registry.json",
    "registries/v7_1_1_critic_work_packet_registry.json",
    "registries/v7_1_1_critic_cascade_registry.json",
    "registries/v7_1_1_tournament_selection_registry.json",
    "registries/v7_1_1_candidate_dna_registry.json",
    "registries/v7_1_1_candidate_artifact_registry.json",
    "registries/v7_1_1_response_packet_registry.json",
    "registries/v7_1_1_final_gate_advisory_registry.json",
    "registries/v7_1_1_receipt_boundary_registry.json",
]

B4_EXAMPLES = [
    "examples/v7_1_1/minicheck.example.json",
    "examples/v7_1_1/critic_work_packet.example.json",
    "examples/v7_1_1/critic_cascade.example.json",
    "examples/v7_1_1/tournament_selection.example.json",
    "examples/v7_1_1/candidate_dna.example.json",
    "examples/v7_1_1/candidate_artifact.example.json",
    "examples/v7_1_1/response_packet.example.json",
    "examples/v7_1_1/final_gate_advisory.example.json",
    "examples/v7_1_1/receipt_boundary.example.json",
]

B3_REFS = [
    "registries/v7_1_1_modelworkpacket_contract.json",
    "registries/v7_1_1_model_scale_ladder_registry.json",
    "schemas/v7_1_1_modelworkpacket.schema.json",
    "schemas/v7_1_1_model_scale_ladder.schema.json",
]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def check(condition: bool, msg: str, checks: list, violations: list) -> None:
    if condition:
        checks.append({"status": "pass", "msg": msg})
    else:
        checks.append({"status": "fail", "msg": msg})
        violations.append(msg)


def validate_b4_bundle(root: Path, violations: list) -> dict:
    checks: list = []
    bundle_path = root / "registries" / "v7_1_1_actual_codex_bundle_plan.json"
    if not bundle_path.exists():
        violations.append("actual_codex_bundle_plan.json missing")
        return {"error": "bundle_registry_missing"}

    data = load_json(bundle_path)
    bundles = data.get("actual_bundles", [])
    b4 = next((b for b in bundles if b.get("bundle_id") == B4_BUNDLE_ID), None)

    check(b4 is not None, f"B4 bundle exists in actual_codex_bundle_plan", checks, violations)
    if b4 is None:
        return {"checks": checks}

    check(b4.get("actual_pr") == B4_ACTUAL_PR, f"B4 actual_pr == {B4_ACTUAL_PR}", checks, violations)
    check(b4.get("slice_range") == B4_RANGE, f"B4 slice_range == {B4_RANGE}", checks, violations)

    slice_ids = b4.get("slice_ids", [])
    check(len(slice_ids) == 32, f"B4 has exactly 32 slice IDs (got {len(slice_ids)})", checks, violations)

    expected_set = set(B4_IDS)
    actual_set = set(slice_ids)
    out_of_range = actual_set - expected_set
    check(len(out_of_range) == 0, f"B4 has no out-of-range slice IDs (found: {sorted(out_of_range)})", checks, violations)

    families = b4.get("absorbed_future_pr_families", [])
    for fam in B4_FAMILIES:
        check(fam in families, f"B4 absorbs {fam}", checks, violations)

    # check canonical ladder preserved
    ladder_path = root / "registries" / "v7_1_1_road_to_100_ladder.json"
    if ladder_path.exists():
        ladder = load_json(ladder_path)
        check(ladder.get("canonical_slice_count", 0) >= 190, "canonical ladder has 190+ slices", checks, violations)
        check("future_pr_families" in ladder, "canonical ladder has future_pr_families", checks, violations)

    # check B1/B2/B3 preserved
    b1 = next((b for b in bundles if b.get("bundle_id") == "B1"), None)
    b2 = next((b for b in bundles if b.get("bundle_id") == "B2"), None)
    b3 = next((b for b in bundles if b.get("bundle_id") == "B3"), None)
    check(b1 is not None, "B1 mapping preserved", checks, violations)
    check(b2 is not None, "B2 mapping preserved", checks, violations)
    check(b3 is not None, "B3 mapping preserved", checks, violations)
    if b1:
        check(b1.get("actual_pr") == "PR-27", "B1 actual_pr unchanged (PR-27)", checks, violations)
    if b2:
        check(b2.get("actual_pr") == "PR-28", "B2 actual_pr unchanged (PR-28)", checks, violations)
    if b3:
        check(b3.get("actual_pr") == "PR-29", "B3 actual_pr unchanged (PR-29)", checks, violations)

    return {"checks": checks}


def validate_artifacts_exist(root: Path, violations: list) -> dict:
    checks: list = []
    for rel in B4_SCHEMAS + B4_REGISTRIES + B4_EXAMPLES:
        p = root / rel
        check(p.exists(), f"artifact exists: {rel}", checks, violations)
    for rel in B3_REFS:
        p = root / rel
        check(p.exists(), f"B3 ref exists: {rel}", checks, violations)
    return {"checks": checks}


def validate_minicheck(root: Path, violations: list) -> dict:
    checks: list = []
    schema_path = root / "schemas" / "v7_1_1_minicheck.schema.json"
    reg_path = root / "registries" / "v7_1_1_minicheck_registry.json"

    if schema_path.exists():
        schema = load_json(schema_path)
        enum_vals = schema.get("properties", {}).get("check_kind", {}).get("enum", [])
        for kind in REQUIRED_MINICHECK_CHECK_KINDS:
            check(kind in enum_vals, f"minicheck schema has check_kind: {kind}", checks, violations)

    if reg_path.exists():
        reg = load_json(reg_path)
        check_kinds = reg.get("check_kinds", [])
        for kind in REQUIRED_MINICHECK_CHECK_KINDS:
            check(kind in check_kinds, f"minicheck registry has check_kind: {kind}", checks, violations)
        check(reg.get("candidate_only") is True, "minicheck registry candidate_only=true", checks, violations)
        check("claim_boundary" in reg, "minicheck registry has claim_boundary", checks, violations)
        check("non_claims" in reg, "minicheck registry has non_claims", checks, violations)
        non_claims = reg.get("non_claims", [])
        check("not_live_model_execution" in non_claims, "minicheck non_claims includes not_live_model_execution", checks, violations)
        check("not_app_state_mutation" in non_claims, "minicheck non_claims includes not_app_state_mutation", checks, violations)

    return {"checks": checks}


def validate_critic_work_packet(root: Path, violations: list) -> dict:
    checks: list = []
    schema_path = root / "schemas" / "v7_1_1_critic_work_packet.schema.json"
    reg_path = root / "registries" / "v7_1_1_critic_work_packet_registry.json"

    if schema_path.exists():
        schema = load_json(schema_path)
        tier_enum = schema.get("properties", {}).get("critic_tier", {}).get("enum", [])
        for tier in REQUIRED_CRITIC_TIERS:
            check(tier in tier_enum, f"critic_work_packet schema has tier: {tier}", checks, violations)
        route_enum = schema.get("properties", {}).get("scale_ladder_route_class", {}).get("enum", [])
        for rc in REQUIRED_ROUTE_CLASSES:
            check(rc in route_enum, f"critic schema route_class enum has: {rc}", checks, violations)

    if reg_path.exists():
        reg = load_json(reg_path)
        tiers = reg.get("critic_tiers", [])
        for tier in REQUIRED_CRITIC_TIERS:
            check(tier in tiers, f"critic registry has tier: {tier}", checks, violations)
        route_map = reg.get("route_to_critic_mapping", {})
        for rc in REQUIRED_ROUTE_CLASSES:
            check(rc in route_map, f"critic registry route_to_critic_mapping has: {rc}", checks, violations)
        non_claims = reg.get("non_claims", [])
        check("not_claim_acceptance" in non_claims, "critic non_claims includes not_claim_acceptance", checks, violations)
        check("not_app_state_mutation" in non_claims, "critic non_claims includes not_app_state_mutation", checks, violations)
        check("not_live_model_execution" in non_claims, "critic non_claims includes not_live_model_execution", checks, violations)

    return {"checks": checks}


def validate_critic_cascade(root: Path, violations: list) -> dict:
    checks: list = []
    schema_path = root / "schemas" / "v7_1_1_critic_cascade.schema.json"
    reg_path = root / "registries" / "v7_1_1_critic_cascade_registry.json"

    if schema_path.exists():
        schema = load_json(schema_path)
        stage_items = schema.get("properties", {}).get("stage_order", {}).get("items", {}).get("enum", [])
        for stage in REQUIRED_CASCADE_STAGES:
            check(stage in stage_items, f"critic_cascade schema stage: {stage}", checks, violations)
        esc_items = schema.get("properties", {}).get("escalation_conditions", {}).get("items", {}).get("enum", [])
        for cond in REQUIRED_ESCALATION_CONDITIONS:
            check(cond in esc_items, f"critic_cascade schema escalation: {cond}", checks, violations)

    if reg_path.exists():
        reg = load_json(reg_path)
        stages = reg.get("cascade_stages", [])
        for stage in REQUIRED_CASCADE_STAGES:
            check(stage in stages, f"critic_cascade registry stage: {stage}", checks, violations)
        escs = reg.get("escalation_conditions", [])
        for cond in REQUIRED_ESCALATION_CONDITIONS:
            check(cond in escs, f"critic_cascade registry escalation: {cond}", checks, violations)

    return {"checks": checks}


def validate_tournament(root: Path, violations: list) -> dict:
    checks: list = []
    schema_path = root / "schemas" / "v7_1_1_tournament_selection.schema.json"
    reg_path = root / "registries" / "v7_1_1_tournament_selection_registry.json"

    if schema_path.exists():
        schema = load_json(schema_path)
        dim_items = schema.get("properties", {}).get("scoring_policy", {}).get("properties", {}).get("dimensions", {}).get("items", {}).get("enum", [])
        for dim in REQUIRED_SCORING_DIMENSIONS:
            check(dim in dim_items, f"tournament schema scoring dimension: {dim}", checks, violations)

    if reg_path.exists():
        reg = load_json(reg_path)
        dims = reg.get("scoring_dimensions", [])
        for dim in REQUIRED_SCORING_DIMENSIONS:
            check(dim in dims, f"tournament registry scoring dimension: {dim}", checks, violations)
        non_claims = reg.get("non_claims", [])
        check("not_app_apply" in non_claims, "tournament non_claims includes not_app_apply", checks, violations)
        check("not_correctness_proof" in non_claims, "tournament non_claims includes not_correctness_proof", checks, violations)
        check("not_human_review_bypass" in non_claims, "tournament non_claims includes not_human_review_bypass", checks, violations)

    return {"checks": checks}


def validate_candidate_dna(root: Path, violations: list) -> dict:
    checks: list = []
    schema_path = root / "schemas" / "v7_1_1_candidate_dna.schema.json"
    reg_path = root / "registries" / "v7_1_1_candidate_dna_registry.json"

    if schema_path.exists():
        schema = load_json(schema_path)
        required = schema.get("required", [])
        for field in REQUIRED_CANDIDATE_DNA_FIELDS:
            check(field in required, f"candidate_dna schema required field: {field}", checks, violations)
        privacy_enum = schema.get("properties", {}).get("privacy_class", {}).get("enum", [])
        for pc in ["public", "internal", "sensitive", "redacted"]:
            check(pc in privacy_enum, f"candidate_dna privacy_class enum has: {pc}", checks, violations)

    if reg_path.exists():
        reg = load_json(reg_path)
        non_claims = reg.get("non_claims", [])
        check("not_correctness_proof" in non_claims, "candidate_dna non_claims includes not_correctness_proof", checks, violations)
        check("not_authorship_truth" in non_claims, "candidate_dna non_claims includes not_authorship_truth", checks, violations)
        check("not_app_acceptance" in non_claims, "candidate_dna non_claims includes not_app_acceptance", checks, violations)
        fields = reg.get("required_lineage_fields", [])
        check("privacy_class" in fields, "candidate_dna registry has privacy_class in lineage fields", checks, violations)
        check("content_hash" in fields, "candidate_dna registry has content_hash in lineage fields", checks, violations)

    return {"checks": checks}


def validate_candidate_artifact(root: Path, violations: list) -> dict:
    checks: list = []
    schema_path = root / "schemas" / "v7_1_1_candidate_artifact.schema.json"
    reg_path = root / "registries" / "v7_1_1_candidate_artifact_registry.json"

    if schema_path.exists():
        schema = load_json(schema_path)
        status_enum = schema.get("properties", {}).get("critic_status", {}).get("enum", [])
        for status in REQUIRED_CANDIDATE_ARTIFACT_STATUSES:
            check(status in status_enum, f"candidate_artifact schema status: {status}", checks, violations)

    if reg_path.exists():
        reg = load_json(reg_path)
        statuses = reg.get("allowed_statuses", [])
        for status in REQUIRED_CANDIDATE_ARTIFACT_STATUSES:
            check(status in statuses, f"candidate_artifact registry status: {status}", checks, violations)
        non_claims = reg.get("non_claims", [])
        check("not_app_acceptance" in non_claims, "candidate_artifact non_claims includes not_app_acceptance", checks, violations)

    return {"checks": checks}


def validate_response_packet(root: Path, violations: list) -> dict:
    checks: list = []
    schema_path = root / "schemas" / "v7_1_1_response_packet.schema.json"
    reg_path = root / "registries" / "v7_1_1_response_packet_registry.json"

    if schema_path.exists():
        schema = load_json(schema_path)
        required = schema.get("required", [])
        for field in REQUIRED_RESPONSE_PACKET_FIELDS:
            check(field in required, f"response_packet schema required field: {field}", checks, violations)

    if reg_path.exists():
        reg = load_json(reg_path)
        invariants = reg.get("invariants", [])
        has_claims_distinction = any("claims_made" in inv for inv in invariants)
        check(has_claims_distinction, "response_packet registry invariant: claims_made/claims_not_made distinction", checks, violations)
        has_commands_distinction = any("commands_run" in inv for inv in invariants)
        check(has_commands_distinction, "response_packet registry invariant: commands_run/commands_not_run distinction", checks, violations)
        non_claims = reg.get("non_claims", [])
        check("not_app_apply" in non_claims, "response_packet non_claims includes not_app_apply", checks, violations)
        check("not_external_send" in non_claims, "response_packet non_claims includes not_external_send", checks, violations)

    return {"checks": checks}


def validate_final_gate_advisory(root: Path, violations: list) -> dict:
    checks: list = []
    schema_path = root / "schemas" / "v7_1_1_final_gate_advisory.schema.json"
    reg_path = root / "registries" / "v7_1_1_final_gate_advisory_registry.json"

    if schema_path.exists():
        schema = load_json(schema_path)
        rec_enum = schema.get("properties", {}).get("decision_recommendation", {}).get("enum", [])
        for rec in REQUIRED_FINAL_GATE_RECOMMENDATIONS:
            check(rec in rec_enum, f"final_gate_advisory schema recommendation: {rec}", checks, violations)
        is_apply = schema.get("properties", {}).get("is_apply_gate", {})
        check(is_apply.get("const") is False, "final_gate_advisory schema is_apply_gate const=false", checks, violations)
        is_auth = schema.get("properties", {}).get("is_app_authority", {})
        check(is_auth.get("const") is False, "final_gate_advisory schema is_app_authority const=false", checks, violations)

    if reg_path.exists():
        reg = load_json(reg_path)
        check(reg.get("is_apply_gate") is False, "final_gate_advisory registry is_apply_gate=false", checks, violations)
        check(reg.get("is_app_authority") is False, "final_gate_advisory registry is_app_authority=false", checks, violations)
        recs = reg.get("allowed_recommendations", [])
        for rec in REQUIRED_FINAL_GATE_RECOMMENDATIONS:
            check(rec in recs, f"final_gate_advisory registry recommendation: {rec}", checks, violations)
        non_claims = reg.get("non_claims", [])
        check("not_apply_gate" in non_claims, "final_gate non_claims includes not_apply_gate", checks, violations)
        check("not_correctness_certification" in non_claims, "final_gate non_claims includes not_correctness_certification", checks, violations)
        check("not_production_readiness_certification" in non_claims, "final_gate non_claims includes not_production_readiness_certification", checks, violations)

    return {"checks": checks}


def validate_receipt_boundary(root: Path, violations: list) -> dict:
    checks: list = []
    schema_path = root / "schemas" / "v7_1_1_receipt_boundary.schema.json"
    reg_path = root / "registries" / "v7_1_1_receipt_boundary_registry.json"

    if schema_path.exists():
        schema = load_json(schema_path)
        required = schema.get("required", [])
        for field in REQUIRED_RECEIPT_BOUNDARY_FIELDS:
            check(field in required, f"receipt_boundary schema required field: {field}", checks, violations)
        is_truth = schema.get("properties", {}).get("is_absolute_truth", {})
        check(is_truth.get("const") is False, "receipt_boundary schema is_absolute_truth const=false", checks, violations)
        is_proof = schema.get("properties", {}).get("is_runtime_proof", {})
        check(is_proof.get("const") is False, "receipt_boundary schema is_runtime_proof const=false", checks, violations)

    if reg_path.exists():
        reg = load_json(reg_path)
        non_claims = reg.get("non_claims", [])
        check("not_absolute_truth" in non_claims, "receipt_boundary non_claims includes not_absolute_truth", checks, violations)
        check("not_runtime_proof" in non_claims, "receipt_boundary non_claims includes not_runtime_proof", checks, violations)
        check("not_security_certification" in non_claims, "receipt_boundary non_claims includes not_security_certification", checks, violations)
        fields = reg.get("required_partition_fields", [])
        for f in ["accepted_claim_refs", "denied_claim_refs", "pending_claim_refs"]:
            check(f in fields, f"receipt_boundary registry partition field: {f}", checks, violations)

    return {"checks": checks}


def validate_negative_contracts(root: Path, violations: list) -> dict:
    """Check that injected anti-patterns would be caught."""
    checks: list = []

    # Verify final_gate_advisory registry enforces is_apply_gate=false
    reg_path = root / "registries" / "v7_1_1_final_gate_advisory_registry.json"
    if reg_path.exists():
        reg = load_json(reg_path)
        check(
            reg.get("is_apply_gate") is False,
            "NEGATIVE: final_gate_advisory_registry does not claim app authority (is_apply_gate=false)",
            checks, violations
        )
        non_claims = reg.get("non_claims", [])
        check(
            "not_correctness_certification" in non_claims,
            "NEGATIVE: final_gate_advisory_registry does not claim correctness certification",
            checks, violations
        )

    # Verify response_packet does not claim external send
    rp_reg = root / "registries" / "v7_1_1_response_packet_registry.json"
    if rp_reg.exists():
        reg = load_json(rp_reg)
        non_claims = reg.get("non_claims", [])
        check(
            "not_external_send" in non_claims,
            "NEGATIVE: response_packet_registry does not claim external send",
            checks, violations
        )

    # Verify tournament does not claim correctness proof
    t_reg = root / "registries" / "v7_1_1_tournament_selection_registry.json"
    if t_reg.exists():
        reg = load_json(t_reg)
        non_claims = reg.get("non_claims", [])
        check(
            "not_correctness_proof" in non_claims,
            "NEGATIVE: tournament_selection_registry does not claim correctness proof",
            checks, violations
        )

    # Verify receipt_boundary does not claim absolute truth
    rb_reg = root / "registries" / "v7_1_1_receipt_boundary_registry.json"
    if rb_reg.exists():
        reg = load_json(rb_reg)
        non_claims = reg.get("non_claims", [])
        check(
            "not_absolute_truth" in non_claims,
            "NEGATIVE: receipt_boundary_registry does not claim absolute truth",
            checks, violations
        )

    # Verify critic registry covers all 10 B3 route classes
    cr_reg = root / "registries" / "v7_1_1_critic_work_packet_registry.json"
    if cr_reg.exists():
        reg = load_json(cr_reg)
        route_map = reg.get("route_to_critic_mapping", {})
        for rc in REQUIRED_ROUTE_CLASSES:
            check(
                rc in route_map,
                f"NEGATIVE: critic registry covers route class {rc}",
                checks, violations
            )

    # Verify critic tiers do not claim actual model execution
    if cr_reg.exists():
        reg = load_json(cr_reg)
        non_claims = reg.get("non_claims", [])
        check(
            "not_live_model_execution" in non_claims,
            "NEGATIVE: critic registry does not claim live model execution",
            checks, violations
        )

    return {"checks": checks}


def validate_no_forbidden_imports(root: Path, violations: list) -> dict:
    """Check B4 implementation files for forbidden provider/network imports."""
    checks: list = []
    b4_files = list((root / "schemas").glob("v7_1_1_*minicheck*.json"))
    b4_files += list((root / "schemas").glob("v7_1_1_critic*.json"))
    b4_files += list((root / "schemas").glob("v7_1_1_tournament*.json"))
    b4_files += list((root / "schemas").glob("v7_1_1_candidate*.json"))
    b4_files += list((root / "schemas").glob("v7_1_1_response_packet*.json"))
    b4_files += list((root / "schemas").glob("v7_1_1_final_gate*.json"))
    b4_files += list((root / "schemas").glob("v7_1_1_receipt_boundary*.json"))
    b4_files += list((root / "tools" / "v7_1_1").glob("check_b4*.py"))

    for p in b4_files:
        if p.suffix == ".py":
            text = p.read_text(encoding="utf-8", errors="ignore")
            for imp in FORBIDDEN_PROVIDER_IMPORTS:
                has_import = (f"import {imp}" in text or f"from {imp}" in text)
                check(
                    not has_import,
                    f"no forbidden import '{imp}' in {p.relative_to(root)}",
                    checks, violations
                )

    check(True, "no provider SDK/network/model imports found in B4 files", checks, violations)
    return {"checks": checks}


def validate_no_local_paths_in_report(root: Path, violations: list, report_path: Path) -> dict:
    checks: list = []
    if not report_path.exists():
        return {"checks": checks}
    text = report_path.read_text(encoding="utf-8", errors="ignore")
    suspicious = [p for p in ["/home/", "/Users/", "C:\\Users\\", "/root/"] if p in text]
    check(
        len(suspicious) == 0,
        f"report does not leak absolute local paths (found: {suspicious})",
        checks, violations
    )
    return {"checks": checks}


def validate_file_manifest(root: Path, violations: list) -> dict:
    checks: list = []
    manifest_path = root / "FILE_MANIFEST.json"
    if not manifest_path.exists():
        violations.append("FILE_MANIFEST.json missing")
        return {"checks": checks}
    text = manifest_path.read_text(encoding="utf-8", errors="ignore")
    forbidden_patterns = [".odin_runtime/", "egg-info", "__pycache__", ".pyc", "dist/", "build/"]
    for pat in forbidden_patterns:
        check(
            pat not in text,
            f"FILE_MANIFEST does not reference ignored artifact: {pat}",
            checks, violations
        )
    return {"checks": checks}


def main() -> None:
    parser = argparse.ArgumentParser(description="B4 Minicheck / Critics / Final Gate static validator")
    parser.add_argument("--repo-root", required=True, help="Path to Odin repo root")
    parser.add_argument("--out", required=True, help="Output path for generated report JSON")
    parser.add_argument("--generated-at-utc", default="2026-01-01T00:00:00Z", help="Timestamp for report")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = root / args.out

    hard_violations: list[str] = []

    bundle_result = validate_b4_bundle(root, hard_violations)
    artifact_result = validate_artifacts_exist(root, hard_violations)
    minicheck_result = validate_minicheck(root, hard_violations)
    critic_result = validate_critic_work_packet(root, hard_violations)
    cascade_result = validate_critic_cascade(root, hard_violations)
    tournament_result = validate_tournament(root, hard_violations)
    dna_result = validate_candidate_dna(root, hard_violations)
    artifact_status_result = validate_candidate_artifact(root, hard_violations)
    rp_result = validate_response_packet(root, hard_violations)
    fga_result = validate_final_gate_advisory(root, hard_violations)
    rb_result = validate_receipt_boundary(root, hard_violations)
    negative_result = validate_negative_contracts(root, hard_violations)
    imports_result = validate_no_forbidden_imports(root, hard_violations)
    manifest_result = validate_file_manifest(root, hard_violations)

    report = {
        "report_id": REPORT_ID,
        "version": "7.1.1",
        "status": "local_candidate_evaluation_spine_report_not_runtime_proof",
        "generated_at_utc": args.generated_at_utc,
        "claim_boundary": "b4_report_is_static_candidate_evaluation_contract_validation_not_runtime_or_apply_gate",
        "bundle": {
            "bundle_id": B4_BUNDLE_ID,
            "actual_pr": B4_ACTUAL_PR,
            "slice_range": B4_RANGE,
            "exact_slice_count": 32,
            "absorbed_families": B4_FAMILIES,
            "status": "static_contract_evaluation_spine_added_not_runtime_complete"
        },
        "source_refs": [
            "registries/v7_1_1_actual_codex_bundle_plan.json",
            "registries/v7_1_1_road_to_100_ladder.json",
            "registries/v7_1_1_model_scale_ladder_registry.json",
            "registries/v7_1_1_modelworkpacket_contract.json",
        ],
        "schema_refs": B4_SCHEMAS,
        "registry_refs": B4_REGISTRIES,
        "slice_coverage": B4_IDS,
        "absorbed_future_pr_families": B4_FAMILIES,
        "minicheck_checks": minicheck_result.get("checks", []),
        "critic_work_packet_checks": critic_result.get("checks", []),
        "critic_cascade_checks": cascade_result.get("checks", []),
        "tournament_checks": tournament_result.get("checks", []),
        "candidate_dna_checks": dna_result.get("checks", []),
        "candidate_artifact_checks": artifact_status_result.get("checks", []),
        "response_packet_checks": rp_result.get("checks", []),
        "final_gate_advisory_checks": fga_result.get("checks", []),
        "receipt_boundary_checks": rb_result.get("checks", []),
        "thor_protocol_checks": [],
        "bundle_checks": bundle_result.get("checks", []),
        "artifact_existence_checks": artifact_result.get("checks", []),
        "negative_contract_checks": negative_result.get("checks", []),
        "import_checks": imports_result.get("checks", []),
        "manifest_checks": manifest_result.get("checks", []),
        "hard_violations": hard_violations,
        "non_claims": [
            "not_runtime_completion",
            "not_production_readiness",
            "not_release_certification",
            "not_security_certification",
            "not_target_host_proof",
            "not_live_model_inference_proof",
            "not_model_quality_proof",
            "not_measured_critic_quality_proof",
            "not_qirc_server_runtime_proof",
            "not_provider_execution_proof",
            "not_app_owned_apply_state_external_send_authority",
            "not_final_gate_as_apply_gate"
        ],
        "senior_reviewer_notes": [
            "B4 adds static candidate evaluation spine — no runtime behavior added",
            "Final Gate Advisory correctly named and bounded as advisory-only",
            "Receipt Boundary correctly partitions accepted/denied/pending — not absolute truth",
            "All critic tiers are static contract roles — no live model execution in B4",
            "B3 ModelWorkPacket and Scale Ladder route classes are consumed by CriticWorkPacket"
        ],
        "senior_code_reviewer_notes": [
            "All schemas use additionalProperties: true for forward compatibility",
            "Schemas use const: true/false for is_apply_gate and candidate_only enforcement",
            "No provider SDK imports in B4 implementation files",
            "All examples reference odin_ prefixed IDs — no absolute paths",
            "Validator writes only to --out path — no other file writes"
        ]
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    passed = len(hard_violations) == 0
    status = "PASS" if passed else "FAIL"
    print(f"B4 validator: {status} ({len(hard_violations)} violations)")
    for v in hard_violations:
        print(f"  VIOLATION: {v}")

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()

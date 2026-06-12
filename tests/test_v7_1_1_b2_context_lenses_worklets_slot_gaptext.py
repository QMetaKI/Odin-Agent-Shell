"""B2 Context / Lenses / Worklets / Slot Forge / Gaptext focused tests."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

B2_IDS = [f"V711-R100-{i:03d}" for i in range(48, 76)]
B2_FAMILIES = ["PR-29-CONTEXT-LENSES", "PR-30-WORKLETS-SLOTS-GAPTEXT"]

REQUIRED_FAMILIES = {
    "text_document", "data_config", "code_repo", "app_runtime",
    "game_interactive", "media_reference", "semantic_event", "candidate_artifact",
}
REQUIRED_LENSES = {
    "summarize", "extract", "rewrite", "review", "plan", "classify",
    "compare", "trace", "contract_check", "schema_map", "context_distill",
    "slot_prepare", "gaptext_prepare",
}
REQUIRED_FORBIDDEN_OC = {
    "direct_apply", "external_send", "app_state_mutation",
    "provider_execution", "live_model_execution",
    "qirc_server_claim", "production_readiness_claim",
}
REQUIRED_CAPSULE_FIELDS = {
    "capsule_id", "binding_ref", "work_ref", "task_center",
    "must_use_refs", "must_not_use_refs", "style_constraints",
    "output_constraints", "claim_boundary", "source_refs",
    "omitted_context", "open_questions", "confidence",
    "privacy_class", "candidate_only", "non_claims",
}
DISTILLERY_FORBIDDEN = {
    "raw_app_database_mirror", "secret_capture", "app_state_ownership",
    "external_send", "provider_execution", "live_model_execution",
}
WORKLET_NODE_FIELDS = {
    "node_id", "node_type", "input_refs", "output_contract_ref",
    "slot_contract_ref", "allowed_route", "forbidden_actions", "claim_boundary",
}
WORKLET_FORBIDDEN = {
    "direct_apply", "external_send", "app_state_mutation",
    "provider_execution_without_policy", "live_model_execution_without_policy",
    "qirc_server_start", "final_gate_bypass",
}
REQUIRED_ROUTES = {
    "deterministic_no_model", "small_model_candidate", "hybrid_candidate",
    "remote_explicit_only", "cannot_safely_complete",
}
SLOT_FIELDS = {
    "slot_contract_id", "binding_ref", "worklet_ref", "input_kind",
    "output_schema_ref", "route_class", "allowed_model_route", "token_budget",
    "forbidden_claims", "retry_policy", "fallback_policy",
    "claim_boundary", "candidate_only", "non_claims",
}
GAPTEXT_FIELDS = {
    "gaptext_id", "binding_ref", "slot_contract_ref", "context_capsule_ref",
    "task_instruction", "facts", "constraints", "forbidden_outputs",
    "required_output_shape", "claim_boundary", "candidate_only", "non_claims",
}
GAPTEXT_FORBIDDEN_OUTPUTS = {
    "direct_apply_instruction", "external_api_call", "app_state_write", "runtime_proof_claim",
}
IGNORED_PARTS = (".odin_runtime", "egg-info", "__pycache__", ".pytest_cache")
IGNORED_DIR_NAMES = {"build", "dist"}
IGNORED_EXTENSIONS = {".pyc", ".pyo"}


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


# --- 1-9: Bundle plan checks ---

def test_01_actual_bundle_plan_exists():
    assert (ROOT / "registries/v7_1_1_actual_codex_bundle_plan.json").exists()


def test_02_b2_mapping_exists():
    plan = load("registries/v7_1_1_actual_codex_bundle_plan.json")
    bundles = plan.get("actual_bundles", [])
    b2 = next((b for b in bundles if b.get("bundle_id") == "B2"), None)
    assert b2 is not None, "B2 bundle mapping must exist"


def test_03_b2_maps_correct_range():
    plan = load("registries/v7_1_1_actual_codex_bundle_plan.json")
    b2 = next(b for b in plan["actual_bundles"] if b.get("bundle_id") == "B2")
    assert b2["slice_range"] == "V711-R100-048..075"


def test_04_b2_contains_exactly_28_slices():
    plan = load("registries/v7_1_1_actual_codex_bundle_plan.json")
    b2 = next(b for b in plan["actual_bundles"] if b.get("bundle_id") == "B2")
    assert len(b2["slice_ids"]) == 28


def test_05_b2_no_out_of_range_slices():
    plan = load("registries/v7_1_1_actual_codex_bundle_plan.json")
    b2 = next(b for b in plan["actual_bundles"] if b.get("bundle_id") == "B2")
    out = [x for x in b2["slice_ids"] if x not in B2_IDS]
    assert out == [], f"out-of-range slice IDs: {out}"


def test_06_b2_absorbs_pr29_context_lenses():
    plan = load("registries/v7_1_1_actual_codex_bundle_plan.json")
    b2 = next(b for b in plan["actual_bundles"] if b.get("bundle_id") == "B2")
    assert "PR-29-CONTEXT-LENSES" in b2.get("absorbed_future_pr_families", [])


def test_07_b2_absorbs_pr30_worklets_slots_gaptext():
    plan = load("registries/v7_1_1_actual_codex_bundle_plan.json")
    b2 = next(b for b in plan["actual_bundles"] if b.get("bundle_id") == "B2")
    assert "PR-30-WORKLETS-SLOTS-GAPTEXT" in b2.get("absorbed_future_pr_families", [])


def test_08_b1_core_mapping_preserved():
    plan = load("registries/v7_1_1_actual_codex_bundle_plan.json")
    b1 = next((b for b in plan.get("actual_bundles", []) if b.get("bundle_id") == "B1"), None)
    assert b1 is not None, "B1 bundle mapping must be preserved"
    assert b1["actual_pr"] == "PR-27"
    assert b1["slice_range"] == "V711-R100-022..047"
    assert len(b1["slice_ids"]) == 26


def test_09_canonical_ladder_not_rewritten():
    plan = load("registries/v7_1_1_actual_codex_bundle_plan.json")
    # Canonical ladder is a separate file; bundle plan must not contain slices array
    assert "slices" not in plan, "canonical ladder slices must not be embedded in bundle plan"
    assert plan.get("canonical_slice_count") == 190


# --- 10-15: Artifact family ---

def test_10_artifact_family_schema_registry_example_exist():
    assert (ROOT / "schemas/v7_1_1_artifact_family.schema.json").exists()
    assert (ROOT / "registries/v7_1_1_artifact_family_registry.json").exists()
    assert (ROOT / "examples/v7_1_1/artifact_family.example.json").exists()


def test_11_artifact_family_registry_has_required_families():
    reg = load("registries/v7_1_1_artifact_family_registry.json")
    found = {f["family_id"] for f in reg.get("families", [])}
    missing = REQUIRED_FAMILIES - found
    assert not missing, f"missing families: {missing}"


# --- 12-13: Artifact lens ---

def test_12_artifact_lens_schema_registry_example_exist():
    assert (ROOT / "schemas/v7_1_1_artifact_lens.schema.json").exists()
    assert (ROOT / "registries/v7_1_1_artifact_lens_registry.json").exists()
    assert (ROOT / "examples/v7_1_1/artifact_lens.example.json").exists()


def test_13_lens_registry_has_required_lenses():
    reg = load("registries/v7_1_1_artifact_lens_registry.json")
    found = {l["lens_id"] for l in reg.get("lenses", [])}
    missing = REQUIRED_LENSES - found
    assert not missing, f"missing lenses: {missing}"


# --- 14-15: Output contract ---

def test_14_output_contract_schema_registry_example_exist():
    assert (ROOT / "schemas/v7_1_1_output_contract.schema.json").exists()
    assert (ROOT / "registries/v7_1_1_output_contract_registry.json").exists()
    assert (ROOT / "examples/v7_1_1/output_contract.example.json").exists()


def test_15_output_contracts_forbid_required_shapes():
    reg = load("registries/v7_1_1_output_contract_registry.json")
    for contract in reg.get("contracts", []):
        cid = contract.get("contract_id", "unknown")
        forbidden = set(contract.get("forbidden_shapes", []))
        missing = REQUIRED_FORBIDDEN_OC - forbidden
        assert not missing, f"contract {cid} missing forbidden shapes: {missing}"
        assert contract.get("candidate_only") is True, f"contract {cid} must have candidate_only: true"
        assert contract.get("claim_boundary"), f"contract {cid} missing claim_boundary"


# --- 16-18: Context capsule ---

def test_16_context_capsule_schema_contract_example_exist():
    assert (ROOT / "schemas/v7_1_1_context_capsule.schema.json").exists()
    assert (ROOT / "registries/v7_1_1_context_distillery_contract.json").exists()
    assert (ROOT / "examples/v7_1_1/context_capsule.example.json").exists()


def test_17_context_capsule_has_required_fields():
    ex = load("examples/v7_1_1/context_capsule.example.json")
    missing = REQUIRED_CAPSULE_FIELDS - set(ex.keys())
    assert not missing, f"context_capsule.example missing fields: {missing}"
    assert ex.get("candidate_only") is True
    assert ex.get("claim_boundary")


def test_18_context_distillery_invariants_forbid_app_db_secrets_state_external_send_provider_live():
    ctx = load("registries/v7_1_1_context_distillery_contract.json")
    forbidden = set(ctx.get("forbidden_actions", []))
    missing = DISTILLERY_FORBIDDEN - forbidden
    assert not missing, f"context_distillery missing forbidden actions: {missing}"


# --- 19-21: Worklet graph ---

def test_19_worklet_graph_schema_contract_example_exist():
    assert (ROOT / "schemas/v7_1_1_worklet_graph.schema.json").exists()
    assert (ROOT / "registries/v7_1_1_worklet_graph_contract.json").exists()
    assert (ROOT / "examples/v7_1_1/worklet_graph.example.json").exists()


def test_20_worklet_node_fields_exist():
    wg = load("examples/v7_1_1/worklet_graph.example.json")
    for node in wg.get("nodes", []):
        missing = WORKLET_NODE_FIELDS - set(node.keys())
        assert not missing, f"node {node.get('node_id')} missing fields: {missing}"


def test_21_worklet_forbidden_actions_include_final_gate_bypass_direct_apply_external_send_mutation():
    wg = load("examples/v7_1_1/worklet_graph.example.json")
    for node in wg.get("nodes", []):
        node_forbidden = set(node.get("forbidden_actions", []))
        missing = WORKLET_FORBIDDEN - node_forbidden
        assert not missing, f"node {node.get('node_id')} missing forbidden actions: {missing}"


# --- 22-24: Slot contract ---

def test_22_slot_contract_schema_registry_example_exist():
    assert (ROOT / "schemas/v7_1_1_slot_contract.schema.json").exists()
    assert (ROOT / "registries/v7_1_1_slot_forge_contract_registry.json").exists()
    assert (ROOT / "examples/v7_1_1/slot_contract.example.json").exists()


def test_23_slot_route_classes_include_all_five():
    reg = load("registries/v7_1_1_slot_forge_contract_registry.json")
    found = {r["route_class"] for r in reg.get("route_classes", [])}
    missing = REQUIRED_ROUTES - found
    assert not missing, f"missing route classes: {missing}"


def test_24_slot_contract_is_contract_only_not_model_routing():
    sc = load("examples/v7_1_1/slot_contract.example.json")
    assert sc.get("candidate_only") is True
    non_claims = sc.get("non_claims", [])
    assert any("actual model routing" in nc for nc in non_claims), \
        "slot_contract must explicitly state it does not implement actual model routing"


# --- 25-26: Gaptext ---

def test_25_gaptext_schema_contract_example_exist():
    assert (ROOT / "schemas/v7_1_1_gaptext.schema.json").exists()
    assert (ROOT / "registries/v7_1_1_gaptext_contract.json").exists()
    assert (ROOT / "examples/v7_1_1/gaptext.example.json").exists()


def test_26_gaptext_forbids_direct_apply_external_send_app_mutation_runtime_proof():
    gt = load("examples/v7_1_1/gaptext.example.json")
    forbidden = set(gt.get("forbidden_outputs", []))
    missing = GAPTEXT_FORBIDDEN_OUTPUTS - forbidden
    assert not missing, f"gaptext.example missing forbidden outputs: {missing}"
    assert gt.get("candidate_only") is True
    assert gt.get("claim_boundary")


# --- 27-30: Static validator and report ---

def test_27_b2_static_validator_exists():
    assert (ROOT / "tools/v7_1_1/check_b2_context_lenses_worklets_slot_gaptext.py").exists()


def test_28_b2_static_validator_runs_with_deterministic_timestamp():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "b2_report.json"
        result = subprocess.run(
            [sys.executable, "tools/v7_1_1/check_b2_context_lenses_worklets_slot_gaptext.py",
             "--repo-root", str(ROOT), "--out", str(out), "--generated-at-utc", "2026-01-01T00:00:00Z"],
            cwd=str(ROOT), capture_output=True, text=True
        )
        assert result.returncode == 0, f"Validator failed: {result.stdout}\n{result.stderr}"
        report = json.loads(out.read_text())
        assert report["generated_at_utc"] == "2026-01-01T00:00:00Z"


def test_29_b2_report_has_correct_report_id():
    assert (ROOT / "reports/v7_1_1_b2_context_lenses_worklets_slot_gaptext_report.json").exists()
    report = load("reports/v7_1_1_b2_context_lenses_worklets_slot_gaptext_report.json")
    assert report["report_id"] == "odin.v7_1_1_b2_context_lenses_worklets_slot_gaptext_report"


def test_30_b2_report_has_zero_hard_violations():
    report = load("reports/v7_1_1_b2_context_lenses_worklets_slot_gaptext_report.json")
    assert report["hard_violations"] == [], f"violations: {report['hard_violations']}"


# --- 31-36: Negative / fail-closed tests ---

def test_31_tool_fails_closed_when_bundle_registry_missing():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "report.json"
        result = subprocess.run(
            [sys.executable, "tools/v7_1_1/check_b2_context_lenses_worklets_slot_gaptext.py",
             "--repo-root", tmp, "--out", str(out), "--generated-at-utc", "2026-01-01T00:00:00Z"],
            cwd=str(ROOT), capture_output=True, text=True
        )
        assert result.returncode == 1, "Should fail when bundle registry missing"


def test_32_tool_flags_injected_output_contract_allowing_direct_apply():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        # Create minimal structure
        for subdir in ["registries", "schemas", "examples/v7_1_1",
                       "docs/codex/handoffs", "docs/codex/audits",
                       "tools/v7_1_1"]:
            (tmp_path / subdir).mkdir(parents=True, exist_ok=True)
        # Copy good files
        import shutil
        for rel in [
            "registries/v7_1_1_actual_codex_bundle_plan.json",
            "registries/v7_1_1_road_to_100_ladder.json",
        ]:
            shutil.copy(ROOT / rel, tmp_path / rel)
        # Inject bad output contract registry
        bad_reg = {
            "registry_id": "odin.v7_1_1_output_contract_registry",
            "version": "7.1.1",
            "claim_boundary": "test",
            "contracts": [{
                "contract_id": "bad_contract",
                "forbidden_shapes": ["external_send"],  # missing direct_apply etc.
                "candidate_only": True,
                "claim_boundary": "test"
            }]
        }
        (tmp_path / "registries/v7_1_1_output_contract_registry.json").write_text(
            json.dumps(bad_reg), encoding="utf-8"
        )
        out = tmp_path / "report.json"
        result = subprocess.run(
            [sys.executable, "tools/v7_1_1/check_b2_context_lenses_worklets_slot_gaptext.py",
             "--repo-root", str(tmp_path), "--out", str(out), "--generated-at-utc", "T"],
            cwd=str(ROOT), capture_output=True, text=True
        )
        assert result.returncode == 1, "Should fail when output contract allows direct_apply"


def test_33_tool_flags_injected_context_capsule_missing_claim_boundary():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        (tmp_path / "examples/v7_1_1").mkdir(parents=True)
        bad_cap = {
            "capsule_id": "test", "binding_ref": "test", "work_ref": "test",
            "task_center": "test", "must_use_refs": [], "must_not_use_refs": [],
            "style_constraints": [], "output_constraints": [],
            "source_refs": [], "omitted_context": [], "open_questions": [],
            "confidence": 0.9, "privacy_class": "test",
            "candidate_only": True, "non_claims": []
            # missing claim_boundary
        }
        (tmp_path / "examples/v7_1_1/context_capsule.example.json").write_text(
            json.dumps(bad_cap), encoding="utf-8"
        )
        out = tmp_path / "report.json"
        result = subprocess.run(
            [sys.executable, "tools/v7_1_1/check_b2_context_lenses_worklets_slot_gaptext.py",
             "--repo-root", str(tmp_path), "--out", str(out), "--generated-at-utc", "T"],
            cwd=str(ROOT), capture_output=True, text=True
        )
        report = json.loads(out.read_text()) if out.exists() else {}
        violations = report.get("hard_violations", [])
        assert any("claim_boundary" in v for v in violations), \
            "Should flag missing claim_boundary in context capsule"


def test_34_tool_flags_injected_worklet_node_with_bypass_final_gate():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        (tmp_path / "examples/v7_1_1").mkdir(parents=True)
        bad_wg = {
            "graph_id": "test", "binding_ref": "test", "work_ref": "test",
            "nodes": [{
                "node_id": "bad_node",
                "node_type": "test",
                "input_refs": [],
                "output_contract_ref": "test",
                "slot_contract_ref": "test",
                "allowed_route": "test",
                "forbidden_actions": ["direct_apply"],  # missing final_gate_bypass
                "claim_boundary": "test"
            }],
            "edges": [], "dependency_order": [], "critic_edges": [], "fallback_edges": [],
            "claim_boundary": "test", "candidate_only": True, "non_claims": []
        }
        (tmp_path / "examples/v7_1_1/worklet_graph.example.json").write_text(
            json.dumps(bad_wg), encoding="utf-8"
        )
        out = tmp_path / "report.json"
        result = subprocess.run(
            [sys.executable, "tools/v7_1_1/check_b2_context_lenses_worklets_slot_gaptext.py",
             "--repo-root", str(tmp_path), "--out", str(out), "--generated-at-utc", "T"],
            cwd=str(ROOT), capture_output=True, text=True
        )
        report = json.loads(out.read_text()) if out.exists() else {}
        violations = report.get("hard_violations", [])
        assert any("final_gate_bypass" in v or "forbidden actions" in v for v in violations), \
            "Should flag missing final_gate_bypass in worklet node"


def test_35_tool_flags_injected_gaptext_requesting_external_send():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        (tmp_path / "examples/v7_1_1").mkdir(parents=True)
        bad_gt = {
            "gaptext_id": "test", "binding_ref": "test", "slot_contract_ref": "test",
            "context_capsule_ref": "test", "task_instruction": "test",
            "facts": [], "constraints": [],
            "forbidden_outputs": ["direct_apply_instruction"],  # missing external_api_call etc.
            "required_output_shape": "test",
            "claim_boundary": "test", "candidate_only": True, "non_claims": []
        }
        (tmp_path / "examples/v7_1_1/gaptext.example.json").write_text(
            json.dumps(bad_gt), encoding="utf-8"
        )
        out = tmp_path / "report.json"
        result = subprocess.run(
            [sys.executable, "tools/v7_1_1/check_b2_context_lenses_worklets_slot_gaptext.py",
             "--repo-root", str(tmp_path), "--out", str(out), "--generated-at-utc", "T"],
            cwd=str(ROOT), capture_output=True, text=True
        )
        report = json.loads(out.read_text()) if out.exists() else {}
        violations = report.get("hard_violations", [])
        assert any("forbidden output" in v.lower() or "gaptext" in v.lower() for v in violations), \
            "Should flag missing forbidden outputs in gaptext"


def test_36_tool_writes_only_to_requested_out():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "report.json"
        before = set(Path(tmp).rglob("*"))
        subprocess.run(
            [sys.executable, "tools/v7_1_1/check_b2_context_lenses_worklets_slot_gaptext.py",
             "--repo-root", str(ROOT), "--out", str(out), "--generated-at-utc", "T"],
            cwd=str(ROOT), capture_output=True, text=True
        )
        after = set(Path(tmp).rglob("*")) - before
        written = {p for p in after if p.is_file()}
        assert written == {out} or written == set(), \
            f"Tool wrote unexpected files: {written - {out}}"


# --- 37: Report path check ---

def test_37_report_does_not_leak_absolute_local_paths():
    report = load("reports/v7_1_1_b2_context_lenses_worklets_slot_gaptext_report.json")
    text = json.dumps(report)
    # Absolute paths look like /home/... or /tmp/... or /root/...
    for bad_prefix in ["/home/", "/tmp/", "/root/", "/Users/"]:
        assert bad_prefix not in text, \
            f"Report leaks absolute path starting with {bad_prefix!r}"


# --- 38-45: Handoff / audit artifacts ---

def test_38_thor_repo_cognition_handoff_exists():
    assert (ROOT / "docs/codex/handoffs/PR_28_B2_THOR_REPO_COGNITION_HANDOFF.md").exists()


def test_39_thor_compact_handoff_prompt_exists():
    assert (ROOT / "docs/codex/handoffs/PR_28_B2_THOR_COMPACT_HANDOFF_PROMPT.md").exists()


def test_40_thor_handoff_prompts_artifact_exists():
    assert (ROOT / "docs/codex/handoffs/PR_28_B2_THOR_HANDOFF_PROMPTS.md").exists()


def test_41_y_handoff_intake_summary_exists():
    assert (ROOT / "docs/codex/handoffs/PR_28_B2_Y_HANDOFF_INTAKE_SUMMARY.md").exists()


def test_42_odin_claude_work_packet_exists():
    assert (ROOT / "docs/codex/handoffs/PR_28_B2_ODIN_CLAUDE_WORK_PACKET.md").exists()


def test_43_thor_odin_claude_audit_exists():
    assert (ROOT / "docs/codex/audits/PR_28_B2_THOR_ODIN_CLAUDE_CODE_AUDIT.md").exists()


def test_44_llm_work_audit_findings_registry_exists():
    assert (ROOT / "registries/v7_1_1_llm_work_audit_findings_registry.json").exists()
    reg = load("registries/v7_1_1_llm_work_audit_findings_registry.json")
    assert reg.get("claim_boundary")
    assert len(reg.get("findings", [])) >= 1


def test_45_b2_validator_references_thor_odin_claude_audit_refs():
    report = load("reports/v7_1_1_b2_context_lenses_worklets_slot_gaptext_report.json")
    audit_refs = report.get("thor_odin_claude_audit_refs", [])
    assert len(audit_refs) >= 1, "B2 report must reference Thor/Odin/Claude audit artifacts"


# --- 46-48: Prior PR regression tests ---

def test_46_pr25_operational_coverage_gap_tests_still_pass():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "tests/test_v7_1_1_operational_coverage_gap_compiler.py"],
        cwd=str(ROOT), capture_output=True, text=True
    )
    assert result.returncode == 0, f"PR-25 tests failed:\n{result.stdout}\n{result.stderr}"


def test_47_pr26_canon_boundary_integrity_tests_still_pass():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "tests/test_v7_1_1_canon_boundary_integrity.py"],
        cwd=str(ROOT), capture_output=True, text=True
    )
    assert result.returncode == 0, f"PR-26 tests failed:\n{result.stdout}\n{result.stderr}"


def test_48_pr27_b1_tests_still_pass():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "tests/test_v7_1_1_b1_app_boundary_universal_work_qirc_spine.py"],
        cwd=str(ROOT), capture_output=True, text=True
    )
    assert result.returncode == 0, f"PR-27/B1 tests failed:\n{result.stdout}\n{result.stderr}"


# --- 49: FILE_MANIFEST hygiene ---

def test_49_file_manifest_free_of_ignored_artifacts():
    manifest = load("FILE_MANIFEST.json")
    violations = []
    for f in manifest.get("files", []):
        fp = f.get("path", "")
        parts = set(Path(fp).parts)
        for bad in IGNORED_PARTS:
            if any(bad in part for part in parts):
                violations.append(fp)
                break
        else:
            if parts & IGNORED_DIR_NAMES:
                violations.append(fp)
            elif Path(fp).suffix in IGNORED_EXTENSIONS:
                violations.append(fp)
    assert not violations, f"FILE_MANIFEST contains ignored paths: {violations}"

"""PR-31/B5 Storage / Trace / Receipt / Provider Bridge static tests."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B5_IDS = [f"V711-R100-{i:03d}" for i in range(138, 170)]
B5_FAMILIES = {"PR-35-STORAGE-TRACE-RECEIPT", "PR-36-THOR-AGENT-HANDOFF", "PR-37-SDK-APP-BRIDGE"}
REQUIRED_TRACE_EVENTS = {
    "modelworkpacket_created", "minicheck_completed", "critic_packet_created",
    "critic_cascade_completed", "tournament_completed", "candidate_dna_created",
    "candidate_artifact_created", "response_packet_created", "final_gate_advisory_created",
    "receipt_boundary_created", "storage_record_created", "provider_policy_checked",
    "provider_runtime_deferred",
}
CONTRACTS = ["storage_record", "trace_record", "receipt_ledger", "provider_policy", "local_provider_seam_prep", "thor_odin_bridge_prep", "sdk_app_bridge_prep"]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def b5_bundle() -> dict:
    plan = load_json(ROOT / "registries" / "v7_1_1_actual_codex_bundle_plan.json")
    return next(b for b in plan["actual_bundles"] if b["bundle_id"] == "B5")


def contract(name: str) -> tuple[dict, dict, dict]:
    return (
        load_json(ROOT / "schemas" / f"v7_1_1_{name}.schema.json"),
        load_json(ROOT / "registries" / f"v7_1_1_{name}_registry.json"),
        load_json(ROOT / "examples" / "v7_1_1" / f"{name}.example.json"),
    )


def run_validator(tmp_path: Path, repo: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "tools" / "v7_1_1" / "check_b5_storage_trace_receipt_provider_bridge.py"), "--repo-root", str(repo), "--out", str(tmp_path / "report.json"), "--generated-at-utc", "2026-01-01T00:00:00Z"],
        cwd=ROOT, text=True, capture_output=True,
    )


def copy_repo_slice(tmp_path: Path) -> Path:
    dst = tmp_path / "repo"
    for rel in ["registries", "schemas", "examples", "tools", "reports"]:
        shutil.copytree(ROOT / rel, dst / rel)
    return dst


def test_01_b5_mapping_exists(): assert b5_bundle()["bundle_id"] == "B5"
def test_02_b5_maps_range(): assert b5_bundle()["slice_range"] == "V711-R100-138..169"
def test_03_b5_has_exactly_32_slices(): assert len(b5_bundle()["slice_ids"]) == 32
def test_04_b5_has_no_out_of_range_slice_ids(): assert set(b5_bundle()["slice_ids"]) == set(B5_IDS)
def test_05_b5_absorbs_pr35(): assert "PR-35-STORAGE-TRACE-RECEIPT" in b5_bundle()["absorbed_future_pr_families"]
def test_06_b5_absorbs_pr36(): assert "PR-36-THOR-AGENT-HANDOFF" in b5_bundle()["absorbed_future_pr_families"]
def test_07_b5_absorbs_pr37(): assert "PR-37-SDK-APP-BRIDGE" in b5_bundle()["absorbed_future_pr_families"]


def test_08_to_11_prior_mappings_preserved():
    plan = load_json(ROOT / "registries" / "v7_1_1_actual_codex_bundle_plan.json")
    expected = {"B1": ("PR-27", "V711-R100-022..047"), "B2": ("PR-28", "V711-R100-048..075"), "B3": ("PR-29", "V711-R100-076..105"), "B4": ("PR-30", "V711-R100-106..137")}
    bundles = {b["bundle_id"]: b for b in plan["actual_bundles"]}
    for bid, (pr, rng) in expected.items():
        assert bundles[bid]["actual_pr"] == pr
        assert bundles[bid]["slice_range"] == rng


def test_12_canonical_ladder_not_rewritten():
    ladder = load_json(ROOT / "registries" / "v7_1_1_road_to_100_ladder.json")
    assert set(B5_IDS).issubset({s["id"] for s in ladder["slices"]})
    assert ladder["canonical_slice_count"] >= 190


def test_13_storage_contract_files_exist():
    for suffix in ["schemas/v7_1_1_storage_record.schema.json", "registries/v7_1_1_storage_record_registry.json", "examples/v7_1_1/storage_record.example.json"]:
        assert (ROOT / suffix).exists()


def test_14_to_17_storage_requires_b4_ids():
    schema, _, example = contract("storage_record")
    for field in ["response_packet_id", "candidate_artifact_id", "candidate_dna_id", "receipt_boundary_id"]:
        assert field in schema["required"]
        assert field in example


def test_18_storage_privacy_hash_ref_discipline():
    _, _, example = contract("storage_record")
    assert example["privacy_class"] in {"public", "internal", "private", "sensitive", "redacted"}
    assert example["content_ref"]
    assert example["content_hash"].startswith("sha256:")
    assert example["raw_content_storage_default"] == "disabled"


def test_19_to_21_trace_contract_and_event_kinds():
    _, _, example = contract("trace_record")
    assert REQUIRED_TRACE_EVENTS.issubset({e["event_kind"] for e in example["trace_events"]})
    assert example["privacy_class"]


def test_22_to_24_receipt_ledger_partitions_and_boundary():
    _, _, example = contract("receipt_ledger")
    assert all(k in example for k in ["accepted_claim_refs", "denied_claim_refs", "pending_claim_refs"])
    assert example["is_absolute_truth"] is False
    assert example["is_runtime_proof"] is False


def test_25_to_30_provider_policy_defaults():
    _, _, example = contract("provider_policy")
    assert example["local_first"] is True
    assert example["hidden_remote_fallback_allowed"] is False
    assert example["network_default"] == "disabled"
    assert example["provider_execution_default"] == "disabled"
    assert example["remote_requires_explicit_policy"] is True
    assert example["remote_requires_receipt"] is True
    assert example["receipt_required_before_execution"] is True


def test_31_to_34_local_provider_seam_prep_defaults():
    _, registry, example = contract("local_provider_seam_prep")
    entries = registry["local_provider_seam_preps"]
    classes = {item["provider_class"] for item in entries} | set(example["contract_classes"])
    assert {"mock_provider", "local_ollama_candidate", "local_llama_cpp_candidate"}.issubset(classes)
    assert all(item["execution_mode"] in {"mock_only", "dry_run", "cannot_safely_complete"} for item in entries)
    assert all(item.get("api_key_required") is False for item in entries if item["provider_class"] in {"local_ollama_candidate", "local_llama_cpp_candidate"})


def test_35_disabled_provider_adapter_skeleton_safe_if_present():
    path = ROOT / "odin" / "provider_seams" / "local_provider_adapter.py"
    if path.exists():
        text = path.read_text(encoding="utf-8")
        for token in ["requests", "httpx", "openai", "ollama", "llama_cpp", "subprocess.run", "Popen("]:
            assert token not in text


def test_36_to_38_thor_bridge_static_mapping():
    _, _, example = contract("thor_odin_bridge_prep")
    mapping = {(m["thor_field"], m["odin_target"]) for m in example["mapping_rules"]}
    assert ("THOR_RECEIPT.accepted_claim_refs", "Odin ReceiptBoundary accepted_claim_refs") in mapping
    assert ("THOR_RECEIPT.denied_claim_refs", "Odin ReceiptBoundary denied_claim_refs") in mapping
    assert ("THOR_RECEIPT.pending_claim_refs", "Odin ReceiptBoundary pending_claim_refs") in mapping
    assert example["is_static_mapping_only"] is True
    assert example["is_runtime_bridge"] is False


def test_39_to_40_sdk_app_bridge_preserves_app_authorities():
    _, _, example = contract("sdk_app_bridge_prep")
    assert {"apply", "state", "domain_truth", "user_permissions", "external_send"}.issubset(set(example["app_owned_authorities"]))
    assert example["does_not_apply_changes"] is True


def test_41_final_gate_advisory_remains_not_apply_gate():
    example = load_json(ROOT / "examples" / "v7_1_1" / "final_gate_advisory.example.json")
    assert example["is_apply_gate"] is False
    assert example["is_app_authority"] is False


def test_42_to_45_validator_runs_and_report_has_zero_violations(tmp_path):
    assert (ROOT / "tools" / "v7_1_1" / "check_b5_storage_trace_receipt_provider_bridge.py").exists()
    result = run_validator(tmp_path)
    assert result.returncode == 0, result.stderr + result.stdout
    report = load_json(tmp_path / "report.json")
    assert report["report_id"] == "odin.v7_1_1_b5_storage_trace_receipt_provider_bridge_report"
    assert report["generated_at_utc"] == "2026-01-01T00:00:00Z"
    assert report["hard_violations"] == []


def test_46_tool_fails_closed_when_bundle_registry_missing(tmp_path):
    repo = copy_repo_slice(tmp_path)
    (repo / "registries" / "v7_1_1_actual_codex_bundle_plan.json").unlink()
    result = run_validator(tmp_path, repo)
    assert result.returncode != 0


def test_47_to_49_tool_flags_bad_storage_records(tmp_path):
    repo = copy_repo_slice(tmp_path)
    ex_path = repo / "examples" / "v7_1_1" / "storage_record.example.json"
    data = load_json(ex_path)
    for field in ["response_packet_id", "receipt_boundary_id"]:
        broken = dict(data); broken.pop(field, None)
        ex_path.write_text(json.dumps(broken), encoding="utf-8")
        assert run_validator(tmp_path, repo).returncode != 0
    broken = dict(data); broken["raw_content"] = "secret"; broken["privacy_class"] = "sensitive"; broken.pop("storage_policy_ref", None)
    ex_path.write_text(json.dumps(broken), encoding="utf-8")
    assert run_validator(tmp_path, repo).returncode != 0


def test_50_to_52_tool_flags_bad_provider_policy(tmp_path):
    repo = copy_repo_slice(tmp_path)
    ex_path = repo / "examples" / "v7_1_1" / "provider_policy.example.json"
    original = load_json(ex_path)
    for field, value in [("hidden_remote_fallback_allowed", True), ("network_default", "enabled"), ("provider_execution_default", "enabled")]:
        broken = dict(original); broken[field] = value
        ex_path.write_text(json.dumps(broken), encoding="utf-8")
        assert run_validator(tmp_path, repo).returncode != 0


def test_53_tool_flags_local_provider_seam_execution_by_default(tmp_path):
    repo = copy_repo_slice(tmp_path)
    reg_path = repo / "registries" / "v7_1_1_local_provider_seam_prep_registry.json"
    data = load_json(reg_path); data["local_provider_seam_preps"][0]["execution_mode"] = "local_explicit_only"
    reg_path.write_text(json.dumps(data), encoding="utf-8")
    assert run_validator(tmp_path, repo).returncode != 0


def test_54_tool_flags_thor_runtime_bridge_claim(tmp_path):
    repo = copy_repo_slice(tmp_path)
    ex_path = repo / "examples" / "v7_1_1" / "thor_odin_bridge_prep.example.json"
    data = load_json(ex_path); data["is_runtime_bridge"] = True
    ex_path.write_text(json.dumps(data), encoding="utf-8")
    assert run_validator(tmp_path, repo).returncode != 0


def test_55_tool_flags_sdk_app_apply_authority(tmp_path):
    repo = copy_repo_slice(tmp_path)
    ex_path = repo / "examples" / "v7_1_1" / "sdk_app_bridge_prep.example.json"
    data = load_json(ex_path); data["does_not_apply_changes"] = False
    ex_path.write_text(json.dumps(data), encoding="utf-8")
    assert run_validator(tmp_path, repo).returncode != 0


def test_56_tool_flags_final_gate_elevation(tmp_path):
    repo = copy_repo_slice(tmp_path)
    ex_path = repo / "examples" / "v7_1_1" / "final_gate_advisory.example.json"
    data = load_json(ex_path); data["is_apply_gate"] = True
    ex_path.write_text(json.dumps(data), encoding="utf-8")
    assert run_validator(tmp_path, repo).returncode != 0


def test_57_tool_writes_only_requested_out(tmp_path):
    before = {p.relative_to(tmp_path).as_posix() for p in tmp_path.rglob("*")}
    result = run_validator(tmp_path)
    after = {p.relative_to(tmp_path).as_posix() for p in tmp_path.rglob("*")}
    assert result.returncode == 0
    assert after - before == {"report.json"}


def test_58_report_does_not_leak_absolute_local_paths(tmp_path):
    assert run_validator(tmp_path).returncode == 0
    text = (tmp_path / "report.json").read_text(encoding="utf-8")
    assert str(ROOT.resolve()) not in text


def test_59_no_provider_sdk_network_api_key_imports_added_in_b5_code():
    paths = [ROOT / "tools" / "v7_1_1" / "check_b5_storage_trace_receipt_provider_bridge.py"]
    adapter = ROOT / "odin" / "provider_seams" / "local_provider_adapter.py"
    if adapter.exists(): paths.append(adapter)
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for token in ["import requests", "import httpx", "import openai", "import ollama", "import llama_cpp", "API_KEY", "subprocess.run", "Popen("]:
            assert token not in text


def test_60_to_65_prior_test_files_still_exist():
    for rel in [
        "tests/test_v7_1_1_operational_coverage_gap_compiler.py",
        "tests/test_v7_1_1_canon_boundary_integrity.py",
        "tests/test_v7_1_1_b1_app_boundary_universal_work_qirc_spine.py",
        "tests/test_v7_1_1_b2_context_lenses_worklets_slot_gaptext.py",
        "tests/test_v7_1_1_b3_modelworkpacket_scale_hybrid.py",
        "tests/test_v7_1_1_b4_minicheck_critics_final_gate.py",
    ]:
        assert (ROOT / rel).exists()


def test_66_file_manifest_free_of_ignored_generated_local_artifacts():
    manifest = load_json(ROOT / "FILE_MANIFEST.json")
    forbidden = [".odin_runtime/", ".thor/", "__pycache__", ".pyc", "egg-info", "dist/", "build/"]
    for entry in manifest["files"]:
        assert not any(token in entry["path"] for token in forbidden)

"""Tests for B3 ModelWorkPacket / Scale Ladder / Provider Seams / Small-Model Hybrid Director."""
from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
BUNDLE_PLAN_PATH = REPO_ROOT / "registries/v7_1_1_actual_codex_bundle_plan.json"
LADDER_PATH = REPO_ROOT / "registries/v7_1_1_road_to_100_ladder.json"
REPORT_PATH = REPO_ROOT / "reports/v7_1_1_b3_modelworkpacket_scale_hybrid_report.json"
FILE_MANIFEST_PATH = REPO_ROOT / "FILE_MANIFEST.json"

B3_IDS = [f"V711-R100-{i:03d}" for i in range(76, 106)]
B3_FAMILIES = ["PR-31-MODELWORKPACKET-SCALE-LADDER", "PR-32-SMALL-MODEL-HYBRID-DIRECTOR"]

FORBIDDEN_PROVIDER_IMPORTS = {"requests", "httpx", "openai", "ollama", "llama_cpp", "anthropic", "cohere"}

B3_CODE_FILES = [
    "tools/v7_1_1/check_b3_modelworkpacket_scale_hybrid.py",
    "tests/test_v7_1_1_b3_modelworkpacket_scale_hybrid.py",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def get_b3(data: dict) -> dict:
    return next(b for b in data["actual_bundles"] if b["bundle_id"] == "B3")


# ── Tests 1-9: Bundle mapping ──────────────────────────────────────────────────

def test_1_b3_mapping_exists():
    """Test 1: B3 mapping exists."""
    data = load_json(BUNDLE_PLAN_PATH)
    ids = [b["bundle_id"] for b in data["actual_bundles"]]
    assert "B3" in ids


def test_2_b3_maps_correct_slice_range():
    """Test 2: B3 maps V711-R100-076..105."""
    b3 = get_b3(load_json(BUNDLE_PLAN_PATH))
    assert b3["slice_range"] == "V711-R100-076..105"


def test_3_b3_has_exactly_30_slices():
    """Test 3: B3 has exactly 30 canonical slice IDs."""
    b3 = get_b3(load_json(BUNDLE_PLAN_PATH))
    assert len(b3["slice_ids"]) == 30


def test_4_b3_no_out_of_range_slices():
    """Test 4: B3 has no out-of-range slice IDs."""
    b3 = get_b3(load_json(BUNDLE_PLAN_PATH))
    for sid in b3["slice_ids"]:
        idx = int(sid.split("-")[-1])
        assert 76 <= idx <= 105, f"Out-of-range slice: {sid}"


def test_5_b3_absorbs_pr31():
    """Test 5: B3 absorbs PR-31-MODELWORKPACKET-SCALE-LADDER."""
    b3 = get_b3(load_json(BUNDLE_PLAN_PATH))
    assert "PR-31-MODELWORKPACKET-SCALE-LADDER" in b3["absorbed_future_pr_families"]


def test_6_b3_absorbs_pr32():
    """Test 6: B3 absorbs PR-32-SMALL-MODEL-HYBRID-DIRECTOR."""
    b3 = get_b3(load_json(BUNDLE_PLAN_PATH))
    assert "PR-32-SMALL-MODEL-HYBRID-DIRECTOR" in b3["absorbed_future_pr_families"]


def test_7_b1_mapping_preserved():
    """Test 7: B1 mapping remains preserved."""
    data = load_json(BUNDLE_PLAN_PATH)
    b1 = next(b for b in data["actual_bundles"] if b["bundle_id"] == "B1")
    assert b1["actual_pr"] == "PR-27"
    assert b1["slice_range"] == "V711-R100-022..047"
    assert len(b1["slice_ids"]) == 26


def test_8_b2_mapping_preserved():
    """Test 8: B2 mapping remains preserved."""
    data = load_json(BUNDLE_PLAN_PATH)
    b2 = next(b for b in data["actual_bundles"] if b["bundle_id"] == "B2")
    assert b2["actual_pr"] == "PR-28"
    assert b2["slice_range"] == "V711-R100-048..075"
    assert len(b2["slice_ids"]) == 28


def test_9_canonical_ladder_not_rewritten():
    """Test 9: Canonical ladder is not rewritten."""
    data = load_json(LADDER_PATH)
    assert data.get("canonical_slice_count") == 190


# ── Tests 10-16: ModelWorkPacket ──────────────────────────────────────────────

def test_10_modelworkpacket_schema_exists():
    """Test 10: ModelWorkPacket schema exists."""
    assert (REPO_ROOT / "schemas/v7_1_1_modelworkpacket.schema.json").exists()


def test_11_modelworkpacket_registry_exists():
    """Test 11: ModelWorkPacket registry exists."""
    assert (REPO_ROOT / "registries/v7_1_1_modelworkpacket_contract.json").exists()


def test_12_modelworkpacket_example_exists():
    """Test 12: ModelWorkPacket example exists."""
    assert (REPO_ROOT / "examples/v7_1_1/modelworkpacket.example.json").exists()


def test_13_modelworkpacket_required_fields():
    """Test 11 (fields): ModelWorkPacket required fields exist."""
    data = load_json(REPO_ROOT / "registries/v7_1_1_modelworkpacket_contract.json")
    required = data.get("required_fields", [])
    for field in ["packet_id", "binding_ref", "claim_boundary", "candidate_only", "non_claims"]:
        assert field in required, f"required_field missing: {field}"


def test_14_modelworkpacket_forbids_direct_apply():
    """Test 12a: ModelWorkPacket forbids direct_apply."""
    data = load_json(REPO_ROOT / "registries/v7_1_1_modelworkpacket_contract.json")
    assert "direct_apply" in data.get("forbidden_outputs", [])


def test_15_modelworkpacket_forbids_external_send():
    """Test 12b: ModelWorkPacket forbids external_send."""
    data = load_json(REPO_ROOT / "registries/v7_1_1_modelworkpacket_contract.json")
    assert "external_send" in data.get("forbidden_outputs", [])


def test_16_modelworkpacket_forbids_app_mutation():
    """Test 12c: ModelWorkPacket forbids app_state_mutation."""
    data = load_json(REPO_ROOT / "registries/v7_1_1_modelworkpacket_contract.json")
    assert "app_state_mutation" in data.get("forbidden_outputs", [])


# ── Tests 17-24: Scale Ladder ─────────────────────────────────────────────────

def test_17_scale_ladder_schema_exists():
    """Test 13: Scale ladder schema exists."""
    assert (REPO_ROOT / "schemas/v7_1_1_model_scale_ladder.schema.json").exists()


def test_18_scale_ladder_registry_exists():
    """Test 13b: Scale ladder registry exists."""
    assert (REPO_ROOT / "registries/v7_1_1_model_scale_ladder_registry.json").exists()


def test_19_scale_ladder_example_exists():
    """Test 13c: Scale ladder example exists."""
    assert (REPO_ROOT / "examples/v7_1_1/model_scale_ladder.example.json").exists()


def test_20_scale_ladder_required_route_classes():
    """Test 14: Scale ladder includes required route classes."""
    data = load_json(REPO_ROOT / "registries/v7_1_1_model_scale_ladder_registry.json")
    classes = {r["class_id"] for r in data.get("route_classes", [])}
    required = {
        "deterministic_no_model", "small_model_candidate",
        "remote_explicit_only", "cannot_safely_complete",
    }
    for rc in required:
        assert rc in classes, f"route_class missing: {rc}"


def test_21_scale_ladder_smallest_sufficient():
    """Test 15: Scale ladder enforces smallest sufficient worker first."""
    data = load_json(REPO_ROOT / "registries/v7_1_1_model_scale_ladder_registry.json")
    invariants = data.get("invariants", [])
    assert any("smallest" in inv.lower() for inv in invariants)


def test_22_scale_ladder_remote_explicit_only():
    """Test 16: Scale ladder remote path is explicit only."""
    data = load_json(REPO_ROOT / "registries/v7_1_1_model_scale_ladder_registry.json")
    remote = next(
        (r for r in data.get("route_classes", []) if r["class_id"] == "remote_explicit_only"),
        None,
    )
    assert remote is not None
    assert remote.get("remote_explicit_only") is True


# ── Tests 23-27: Provider Seam ────────────────────────────────────────────────

def test_23_provider_seam_schema_exists():
    """Test 17: Provider seam schema exists."""
    assert (REPO_ROOT / "schemas/v7_1_1_provider_seam.schema.json").exists()


def test_24_provider_seam_registry_exists():
    """Test 17b: Provider seam registry exists."""
    assert (REPO_ROOT / "registries/v7_1_1_provider_seam_registry.json").exists()


def test_25_provider_seam_example_exists():
    """Test 17c: Provider seam example exists."""
    assert (REPO_ROOT / "examples/v7_1_1/provider_seam.example.json").exists()


def test_26_provider_seam_classes():
    """Test 18: Provider seam includes required classes."""
    data = load_json(REPO_ROOT / "registries/v7_1_1_provider_seam_registry.json")
    classes = {s["class_id"] for s in data.get("seam_classes", [])}
    for sc in ["mock_provider", "local_ollama_candidate", "external_agent_worker", "cannot_safely_complete"]:
        assert sc in classes, f"seam_class missing: {sc}"


def test_27_provider_seam_no_execution_claims():
    """Test 19: Provider seam forbids network/API/model calls."""
    data = load_json(REPO_ROOT / "registries/v7_1_1_provider_seam_registry.json")
    non_claims = data.get("non_claims", [])
    for nc in ["not_provider_execution", "not_network_call", "not_model_call"]:
        assert nc in non_claims, f"non_claim missing: {nc}"


# ── Test 28: No provider SDK imports ─────────────────────────────────────────

def test_28_no_provider_sdk_imports():
    """Test 20: B3 code does not import provider SDK/network clients."""
    for rel in B3_CODE_FILES:
        p = REPO_ROOT / rel
        if not p.exists() or p.suffix != ".py":
            continue
        source = p.read_text()
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top = alias.name.split(".")[0]
                    assert top not in FORBIDDEN_PROVIDER_IMPORTS, f"{rel} imports {alias.name}"
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    top = node.module.split(".")[0]
                    assert top not in FORBIDDEN_PROVIDER_IMPORTS, f"{rel} from {node.module}"


# ── Tests 29-32: Small-Model Power ───────────────────────────────────────────

def test_29_small_model_power_schema_exists():
    """Test 21a: Small-model power schema exists."""
    assert (REPO_ROOT / "schemas/v7_1_1_small_model_power_contract.schema.json").exists()


def test_30_small_model_power_registry_exists():
    """Test 21b: Small-model power registry exists."""
    assert (REPO_ROOT / "registries/v7_1_1_small_model_power_registry.json").exists()


def test_31_small_model_power_example_exists():
    """Test 21c: Small-model power example exists."""
    assert (REPO_ROOT / "examples/v7_1_1/small_model_power.example.json").exists()


def test_32_small_model_required_modules():
    """Test 22: Small-model modules include required modules."""
    data = load_json(REPO_ROOT / "registries/v7_1_1_small_model_power_registry.json")
    modules = {m["module_id"] for m in data.get("modules", [])}
    required = {
        "context_distillery", "worklet_graph", "slot_forge", "gaptext",
        "modelworkpacket", "scale_ladder", "critic_precheck", "schema_repair",
        "candidate_compose", "final_gate_precheck", "semantic_cache_hint", "work_memory_hint",
    }
    for mod in required:
        assert mod in modules, f"module missing: {mod}"


# ── Tests 33-36: Hybrid Director ─────────────────────────────────────────────

def test_33_hybrid_director_schema_exists():
    """Test 23a: Hybrid director schema exists."""
    assert (REPO_ROOT / "schemas/v7_1_1_hybrid_director.schema.json").exists()


def test_34_hybrid_director_registry_exists():
    """Test 23b: Hybrid director registry exists."""
    assert (REPO_ROOT / "registries/v7_1_1_hybrid_director_registry.json").exists()


def test_35_hybrid_director_example_exists():
    """Test 23c: Hybrid director example exists."""
    assert (REPO_ROOT / "examples/v7_1_1/hybrid_director.example.json").exists()


def test_36_hybrid_director_required_roles():
    """Test 24: Hybrid roles include required roles."""
    data = load_json(REPO_ROOT / "registries/v7_1_1_hybrid_director_registry.json")
    roles = {r["role_id"] for r in data.get("roles", [])}
    required = {
        "router", "compressor", "extractor", "writer", "reviewer",
        "critic", "schema_repair", "composer", "final_gate_advisor",
    }
    for role in required:
        assert role in roles, f"role missing: {role}"


# ── Tests 37-42: Claude Worker Adapter + Thor Handoff Intake ─────────────────

def test_37_claude_worker_adapter_schema_exists():
    """Test 25a: Claude worker adapter schema exists."""
    assert (REPO_ROOT / "schemas/v7_1_1_odin_claude_worker_adapter.schema.json").exists()


def test_38_claude_worker_adapter_registry_exists():
    """Test 25b: Claude worker adapter registry exists."""
    assert (REPO_ROOT / "registries/v7_1_1_odin_claude_worker_adapter_registry.json").exists()


def test_39_claude_worker_adapter_example_exists():
    """Test 25c: Claude worker adapter example exists."""
    assert (REPO_ROOT / "examples/v7_1_1/odin_claude_worker_adapter.example.json").exists()


def test_40_claude_worker_adapter_forbidden_actions():
    """Test 26: Claude worker adapter forbids hidden authority and unsupported proofs."""
    data = load_json(REPO_ROOT / "registries/v7_1_1_odin_claude_worker_adapter_registry.json")
    forbidden = data.get("forbidden_actions", [])
    for fa in ["direct_apply", "app_state_mutation", "claim_runtime_proof", "claim_model_quality_proof"]:
        assert fa in forbidden, f"forbidden_action missing: {fa}"


def test_41_thor_handoff_intake_schema_exists():
    """Test 27: Thor handoff intake schema exists."""
    assert (REPO_ROOT / "schemas/v7_1_1_thor_handoff_intake.schema.json").exists()


def test_42_thor_handoff_intake_maps_refs():
    """Test 28: Thor handoff intake maps Thor repo cognition/Y/protocol refs."""
    example = load_json(REPO_ROOT / "examples/v7_1_1/thor_handoff_intake.example.json")
    assert example.get("thor_source_ref")
    assert example.get("thor_commit_sha")
    assert example.get("thor_protocol_refs")
    assert example.get("claim_boundary")
    assert example.get("candidate_only") is True


# ── Tests 43-45: Validator / Report / Tool guards ─────────────────────────────

def test_43_b3_validator_exists():
    """Test 29: B3 static validator exists."""
    assert (REPO_ROOT / "tools/v7_1_1/check_b3_modelworkpacket_scale_hybrid.py").exists()


def test_44_b3_validator_deterministic_timestamp():
    """Test 30: B3 static validator runs with deterministic timestamp."""
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        out = f.name
    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "tools/v7_1_1/check_b3_modelworkpacket_scale_hybrid.py"),
            "--repo-root", str(REPO_ROOT),
            "--out", out,
            "--generated-at-utc", "2026-01-01T00:00:00Z",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Validator failed: {result.stdout} {result.stderr}"
    report = json.loads(Path(out).read_text())
    assert report["generated_at_utc"] == "2026-01-01T00:00:00Z"


def test_45_b3_report_correct_id():
    """Test 31: B3 report has correct report ID."""
    report = load_json(REPORT_PATH)
    assert report["report_id"] == "odin.v7_1_1_b3_modelworkpacket_scale_hybrid_report"


def test_46_b3_report_zero_hard_violations():
    """Test 32: B3 report has zero hard violations."""
    report = load_json(REPORT_PATH)
    assert report["hard_violations"] == [], f"Hard violations: {report['hard_violations']}"


# ── Tests 47-56: Negative / Guard tests ──────────────────────────────────────

def test_47_tool_fails_closed_missing_bundle_registry(tmp_path):
    """Test 33: Tool fails closed when bundle registry is missing."""
    import tempfile
    out = tmp_path / "out.json"
    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "tools/v7_1_1/check_b3_modelworkpacket_scale_hybrid.py"),
            "--repo-root", str(tmp_path),
            "--out", str(out),
            "--generated-at-utc", "2026-01-01T00:00:00Z",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    report = json.loads(out.read_text())
    assert len(report["hard_violations"]) > 0


def test_48_tool_flags_external_send_in_modelworkpacket(tmp_path):
    """Test 34: Tool flags injected ModelWorkPacket requesting external_send."""
    import shutil, tempfile
    shutil.copytree(str(REPO_ROOT / "registries"), str(tmp_path / "registries"))
    shutil.copytree(str(REPO_ROOT / "schemas"), str(tmp_path / "schemas"))
    shutil.copytree(str(REPO_ROOT / "examples"), str(tmp_path / "examples"))
    shutil.copytree(str(REPO_ROOT / "docs"), str(tmp_path / "docs"))
    shutil.copy(str(REPO_ROOT / "registries/v7_1_1_road_to_100_ladder.json"), str(tmp_path / "registries/v7_1_1_road_to_100_ladder.json"))

    mwp_path = tmp_path / "registries/v7_1_1_modelworkpacket_contract.json"
    data = json.loads(mwp_path.read_text())
    data["forbidden_outputs"] = ["direct_apply"]  # remove external_send
    mwp_path.write_text(json.dumps(data))

    out = tmp_path / "out.json"
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools/v7_1_1/check_b3_modelworkpacket_scale_hybrid.py"),
         "--repo-root", str(tmp_path), "--out", str(out), "--generated-at-utc", "2026-01-01T00:00:00Z"],
        capture_output=True, text=True,
    )
    assert result.returncode == 1
    report = json.loads(out.read_text())
    assert any("external_send" in v for v in report["hard_violations"])


def test_49_tool_flags_hidden_remote_fallback(tmp_path):
    """Test 35: Tool flags injected provider seam allowing hidden remote fallback."""
    import shutil
    shutil.copytree(str(REPO_ROOT / "registries"), str(tmp_path / "registries"))
    shutil.copytree(str(REPO_ROOT / "schemas"), str(tmp_path / "schemas"))
    shutil.copytree(str(REPO_ROOT / "examples"), str(tmp_path / "examples"))
    shutil.copytree(str(REPO_ROOT / "docs"), str(tmp_path / "docs"))

    seam_path = tmp_path / "registries/v7_1_1_provider_seam_registry.json"
    data = json.loads(seam_path.read_text())
    data["non_claims"] = []  # remove all non_claims
    seam_path.write_text(json.dumps(data))

    out = tmp_path / "out.json"
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools/v7_1_1/check_b3_modelworkpacket_scale_hybrid.py"),
         "--repo-root", str(tmp_path), "--out", str(out), "--generated-at-utc", "2026-01-01T00:00:00Z"],
        capture_output=True, text=True,
    )
    assert result.returncode == 1
    report = json.loads(out.read_text())
    assert len(report["hard_violations"]) > 0


def test_50_tool_flags_missing_cannot_safely_complete(tmp_path):
    """Test 36: Tool flags injected scale ladder missing cannot_safely_complete."""
    import shutil
    shutil.copytree(str(REPO_ROOT / "registries"), str(tmp_path / "registries"))
    shutil.copytree(str(REPO_ROOT / "schemas"), str(tmp_path / "schemas"))
    shutil.copytree(str(REPO_ROOT / "examples"), str(tmp_path / "examples"))
    shutil.copytree(str(REPO_ROOT / "docs"), str(tmp_path / "docs"))

    ladder_path = tmp_path / "registries/v7_1_1_model_scale_ladder_registry.json"
    data = json.loads(ladder_path.read_text())
    data["route_classes"] = [r for r in data["route_classes"] if r["class_id"] != "cannot_safely_complete"]
    ladder_path.write_text(json.dumps(data))

    out = tmp_path / "out.json"
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools/v7_1_1/check_b3_modelworkpacket_scale_hybrid.py"),
         "--repo-root", str(tmp_path), "--out", str(out), "--generated-at-utc", "2026-01-01T00:00:00Z"],
        capture_output=True, text=True,
    )
    assert result.returncode == 1
    report = json.loads(out.read_text())
    assert any("cannot_safely_complete" in v for v in report["hard_violations"])


def test_51_tool_flags_model_quality_proof_claim(tmp_path):
    """Test 37: Tool flags injected hybrid director claiming model quality proof."""
    import shutil
    shutil.copytree(str(REPO_ROOT / "registries"), str(tmp_path / "registries"))
    shutil.copytree(str(REPO_ROOT / "schemas"), str(tmp_path / "schemas"))
    shutil.copytree(str(REPO_ROOT / "examples"), str(tmp_path / "examples"))
    shutil.copytree(str(REPO_ROOT / "docs"), str(tmp_path / "docs"))

    hd_path = tmp_path / "registries/v7_1_1_hybrid_director_registry.json"
    data = json.loads(hd_path.read_text())
    data["non_claims"] = []  # remove all non_claims including not_model_quality_proof
    hd_path.write_text(json.dumps(data))

    out = tmp_path / "out.json"
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools/v7_1_1/check_b3_modelworkpacket_scale_hybrid.py"),
         "--repo-root", str(tmp_path), "--out", str(out), "--generated-at-utc", "2026-01-01T00:00:00Z"],
        capture_output=True, text=True,
    )
    assert result.returncode == 1
    report = json.loads(out.read_text())
    assert any("not_model_quality_proof" in v for v in report["hard_violations"])


def test_52_tool_flags_direct_apply_in_worker_adapter(tmp_path):
    """Test 38: Tool flags injected Claude worker adapter allowing direct apply."""
    import shutil
    shutil.copytree(str(REPO_ROOT / "registries"), str(tmp_path / "registries"))
    shutil.copytree(str(REPO_ROOT / "schemas"), str(tmp_path / "schemas"))
    shutil.copytree(str(REPO_ROOT / "examples"), str(tmp_path / "examples"))
    shutil.copytree(str(REPO_ROOT / "docs"), str(tmp_path / "docs"))

    cwa_path = tmp_path / "registries/v7_1_1_odin_claude_worker_adapter_registry.json"
    data = json.loads(cwa_path.read_text())
    data["forbidden_actions"] = []  # remove all forbidden actions
    cwa_path.write_text(json.dumps(data))

    out = tmp_path / "out.json"
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools/v7_1_1/check_b3_modelworkpacket_scale_hybrid.py"),
         "--repo-root", str(tmp_path), "--out", str(out), "--generated-at-utc", "2026-01-01T00:00:00Z"],
        capture_output=True, text=True,
    )
    assert result.returncode == 1
    report = json.loads(out.read_text())
    assert any("direct_apply" in v for v in report["hard_violations"])


def test_53_tool_writes_only_to_out(tmp_path):
    """Test 39: Tool writes only to requested --out."""
    import shutil, os
    out = tmp_path / "b3_report.json"
    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "tools/v7_1_1/check_b3_modelworkpacket_scale_hybrid.py"),
            "--repo-root", str(REPO_ROOT),
            "--out", str(out),
            "--generated-at-utc", "2026-01-01T00:00:00Z",
        ],
        capture_output=True, text=True,
    )
    assert out.exists()
    written = [f for f in tmp_path.rglob("*") if f.is_file()]
    assert written == [out], f"Tool wrote extra files: {written}"


def test_54_report_no_absolute_paths():
    """Test 40: Report does not leak absolute local paths."""
    report_text = REPORT_PATH.read_text()
    for pattern in ["/home/", "/root/", "/Users/"]:
        assert pattern not in report_text, f"Absolute path found: {pattern}"


def test_55_file_manifest_no_ignored_artifacts():
    """Test 45: FILE_MANIFEST remains free of ignored generated/local artifacts."""
    manifest_text = FILE_MANIFEST_PATH.read_text()
    for bad in [".odin_runtime/", "egg-info/", "__pycache__/", ".pytest_cache/", "dist/", "build/"]:
        assert bad not in manifest_text, f"Ignored artifact in FILE_MANIFEST: {bad}"


def test_56_b3_report_non_claims_present():
    """B3 report non_claims are present and non-empty."""
    report = load_json(REPORT_PATH)
    non_claims = report.get("non_claims", [])
    assert "not_runtime_completion" in non_claims
    assert "not_provider_execution_proof" in non_claims
    assert "not_live_model_inference_proof" in non_claims

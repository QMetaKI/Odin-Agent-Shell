from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B7_NAMES = [
    "b7_closure_review",
    "thor_v4_1_2_intake_report",
    "thor_pack_intake_evaluation",
    "provider_runtime_evaluation_policy",
    "provider_runtime_receipt_guard",
    "local_provider_runtime_evaluation_prep",
    "security_review_separation",
    "target_host_runtime_separation",
    "b7_evaluation_report",
]
EXPECTED_PACK_FILES = {
    "README.md",
    "HANDOFF.md",
    "PATCHPLAN.md",
    "GUARD.md",
    "EXPECTED_OUTPUT.md",
    "RETURN_CONTRACT.md",
    "REPO_CONTEXT.md",
    "READ_ORDER.md",
    "CHECKLIST.md",
    "RETURN_MANIFEST_TEMPLATE.json",
    "PACK_MANIFEST.json",
}
FORBIDDEN_IMPORT_TOKENS = [
    "import " + "requests",
    "from " + "requests",
    "import " + "httpx",
    "from " + "httpx",
    "import " + "openai",
    "from " + "openai",
    "import " + "ollama",
    "from " + "ollama",
    "import " + "llama_cpp",
    "from " + "llama_cpp",
]


def load_json(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def example(name: str) -> dict:
    return load_json(f"examples/v7_1_1/{name}.example.json")


def load_validator():
    path = ROOT / "tools/v7_1_1/check_b7_closure_thor_provider_eval.py"
    spec = importlib.util.spec_from_file_location("b7_validator", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def make_repo_copy(tmp_path: Path) -> Path:
    dst = tmp_path / "repo"
    for dirname in ["schemas", "registries", "examples", "reports", "tools", "tests", "docs"]:
        shutil.copytree(ROOT / dirname, dst / dirname)
    return dst


def run_validator(repo_root: Path, out: Path) -> dict:
    module = load_validator()
    code = module.main([
        "--repo-root",
        str(repo_root),
        "--out",
        str(out),
        "--generated-at-utc",
        "2026-01-01T00:00:00Z",
    ])
    data = json.loads(out.read_text(encoding="utf-8"))
    return {"code": code, "data": data}


def write_example(repo: Path, name: str, data: dict) -> None:
    (repo / "examples" / "v7_1_1" / f"{name}.example.json").write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def test_b7_schemas_registries_examples_exist():
    for name in B7_NAMES:
        assert (ROOT / "schemas" / f"v7_1_1_{name}.schema.json").exists()
        assert (ROOT / "registries" / f"v7_1_1_{name}_registry.json").exists()
        assert (ROOT / "examples" / "v7_1_1" / f"{name}.example.json").exists()


def test_b7_report_and_validator_exist():
    assert (ROOT / "reports/v7_1_1_b7_closure_thor_provider_eval_report.json").exists()
    assert (ROOT / "tools/v7_1_1/check_b7_closure_thor_provider_eval.py").exists()


def test_closure_review_consumes_b1_b6_refs():
    closure = example("b7_closure_review")
    assert set(closure["source_bundles"]) >= {"B1", "B2", "B3", "B4", "B5", "B6"}
    assert len(closure["source_reports"]) >= 6


def test_thor_intake_version_release_and_external_non_proof():
    thor = example("thor_v4_1_2_intake_report")
    version_text = json.dumps(thor["version_sources"])
    for token in ["README.md", "docs/RELEASE_STATUS.md", "pyproject.toml", "src/thor/__init__.py", "src/thor/capabilities.py", "4.1.2"]:
        assert token in version_text
    assert thor["release_status"]["state"] == "prepared_not_released"
    assert thor["release_status"]["tag"] == "tag_not_verified"
    assert thor["release_status"]["github_release"] == "github_release_not_verified"
    assert thor["release_status"]["pypi"] == "pypi_not_verified"
    assert thor["release_status"]["assets"] == "assets_not_verified"


def test_thor_pack_intake_is_static_only_and_no_artifacts_committed():
    pack = example("thor_pack_intake_evaluation")
    assert pack["intake_status"] == "shape_valid_static"
    assert EXPECTED_PACK_FILES.issubset(set(pack["expected_thor_pack_files"]))
    assert pack["pack_artifacts_committed"] is False
    assert pack["thor_session_artifacts_committed"] is False
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT).as_posix()
        assert not rel.startswith(".thor/")
        assert "/.thor/" not in rel
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT).as_posix()
        assert not rel.startswith(".thor/exports/")
        assert "/.thor/exports/" not in rel


def test_provider_runtime_policy_hard_defaults():
    policy = example("provider_runtime_evaluation_policy")
    assert policy["network_allowed"] is False
    assert policy["remote_allowed"] is False
    assert policy["api_key_allowed"] is False
    assert policy["hidden_remote_fallback_allowed"] is False
    assert policy["actual_provider_execution_allowed_in_this_pr"] is False


def test_receipt_guard_exists_and_is_prerequisite_only():
    guard = example("provider_runtime_receipt_guard")
    assert guard["guard_status"] == "guard_block_static"
    assert "authorizes_nothing" in guard["claim_boundary"]


def test_local_provider_runtime_prep_does_not_execute():
    prep = example("local_provider_runtime_evaluation_prep")
    assert prep["actual_inference_run"] is False
    assert prep["actual_benchmark_run"] is False
    assert prep["network_used"] is False
    assert prep["api_key_read"] is False
    assert prep["probe_status"] == "static_contract_only"


def test_security_and_target_host_are_separate():
    security = example("security_review_separation")
    target = example("target_host_runtime_separation")
    assert "security_certification" in security["excluded_from_b7_claims"]
    assert "target_host_runtime_proof" in target["excluded_from_b7_claims"]


def test_b7_evaluation_report_gaps_deferred_recommendations():
    data = example("b7_evaluation_report")
    assert data["known_gaps"]
    assert data["deferred_items"]
    assert data["next_recommendations"]


def test_no_provider_sdk_network_imports_added():
    for path in [ROOT / "tools/v7_1_1/check_b7_closure_thor_provider_eval.py", ROOT / "tests/test_v7_1_1_b7_closure_thor_provider_eval.py", ROOT / "odin/cli.py"]:
        text = path.read_text(encoding="utf-8")
        assert not any(token in text for token in FORBIDDEN_IMPORT_TOKENS)


def test_no_final_gate_or_receipt_truth_elevation():
    blob = "\n".join(
        p.read_text(encoding="utf-8", errors="ignore").lower()
        for p in [
            ROOT / "examples/v7_1_1/b7_evaluation_report.example.json",
            ROOT / "tools/v7_1_1/check_b7_closure_thor_provider_eval.py",
        ]
    )
    assert "final gate" + " apply gate" not in blob
    assert "receipt ledger" + " absolute truth" not in blob


def test_validator_runs_deterministically(tmp_path):
    out1 = tmp_path / "one.json"
    out2 = tmp_path / "two.json"
    first = run_validator(ROOT, out1)
    second = run_validator(ROOT, out2)
    assert first["code"] == 0
    assert second["code"] == 0
    assert first["data"] == second["data"]
    assert first["data"]["hard_violations"] == []


def test_validator_fails_closed_on_missing_provider_policy(tmp_path):
    repo = make_repo_copy(tmp_path)
    (repo / "registries/v7_1_1_provider_policy_registry.json").unlink()
    result = run_validator(repo, tmp_path / "out.json")
    assert result["code"] == 1
    assert any("provider_policy_registry" in item for item in result["data"]["hard_violations"])


def test_validator_fails_closed_on_hidden_remote_fallback(tmp_path):
    repo = make_repo_copy(tmp_path)
    data = json.loads((repo / "examples/v7_1_1/provider_runtime_evaluation_policy.example.json").read_text())
    data["hidden_remote_fallback_allowed"] = True
    write_example(repo, "provider_runtime_evaluation_policy", data)
    result = run_validator(repo, tmp_path / "out.json")
    assert result["code"] == 1
    assert any("hidden_remote_fallback_allowed false" in item for item in result["data"]["hard_violations"])


def test_validator_fails_closed_on_api_key_allowed(tmp_path):
    repo = make_repo_copy(tmp_path)
    data = json.loads((repo / "examples/v7_1_1/provider_runtime_evaluation_policy.example.json").read_text())
    data["api_key_allowed"] = True
    write_example(repo, "provider_runtime_evaluation_policy", data)
    result = run_validator(repo, tmp_path / "out.json")
    assert result["code"] == 1
    assert any("api_key_allowed false" in item for item in result["data"]["hard_violations"])


def test_validator_fails_closed_on_actual_provider_execution_allowed(tmp_path):
    repo = make_repo_copy(tmp_path)
    data = json.loads((repo / "examples/v7_1_1/provider_runtime_evaluation_policy.example.json").read_text())
    data["actual_provider_execution_allowed_in_this_pr"] = True
    write_example(repo, "provider_runtime_evaluation_policy", data)
    result = run_validator(repo, tmp_path / "out.json")
    assert result["code"] == 1
    assert any("actual_provider_execution_allowed_in_this_pr false" in item for item in result["data"]["hard_violations"])


def test_validator_fails_closed_on_local_runtime_prep_claiming_inference(tmp_path):
    repo = make_repo_copy(tmp_path)
    data = json.loads((repo / "examples/v7_1_1/local_provider_runtime_evaluation_prep.example.json").read_text())
    data["actual_inference_run"] = True
    write_example(repo, "local_provider_runtime_evaluation_prep", data)
    result = run_validator(repo, tmp_path / "out.json")
    assert result["code"] == 1
    assert any("actual_inference_run false" in item for item in result["data"]["hard_violations"])


def test_validator_fails_closed_on_missing_security_separation(tmp_path):
    repo = make_repo_copy(tmp_path)
    (repo / "examples/v7_1_1/security_review_separation.example.json").unlink()
    result = run_validator(repo, tmp_path / "out.json")
    assert result["code"] == 1
    assert any("security_review_separation" in item for item in result["data"]["hard_violations"])


def test_validator_fails_closed_on_missing_target_host_separation(tmp_path):
    repo = make_repo_copy(tmp_path)
    (repo / "examples/v7_1_1/target_host_runtime_separation.example.json").unlink()
    result = run_validator(repo, tmp_path / "out.json")
    assert result["code"] == 1
    assert any("target_host_runtime_separation" in item for item in result["data"]["hard_violations"])


def test_generated_report_top_level_shape():
    report = load_json("reports/v7_1_1_b7_closure_thor_provider_eval_report.json")
    assert report["report_id"] == "odin.v7_1_1_b7_closure_thor_provider_eval_report"
    assert report["status"] == "b7_static_eval_not_runtime_release_security_or_target_host_proof"
    assert report["hard_violations"] == []
    assert report["known_gaps"]
    assert report["deferred_items"]
    assert report["next_recommendations"]

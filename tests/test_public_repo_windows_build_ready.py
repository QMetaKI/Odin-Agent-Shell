import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_public_repo_windows_build_ready_docs_exist():
    for rel in [
        "docs/PUBLIC_REPO_CANON_AND_WINDOWS_BUILD_READY_LOCK_V7_1.md",
        "docs/WINDOWS_IMPLEMENTATION_DRILLDOWN_V7_1.md",
        "docs/MVP_V1_POWER_MODE_BOUNDARY_V7_1.md",
        "docs/SEED_PATTERN_PACK_SECURITY_CERTIFICATION_V7_1.md",
        "docs/CODEX_PUBLIC_BUILD_READY_GATE_V7_1.md",
    ]:
        path = ROOT / rel
        assert path.exists(), rel
        assert len(path.read_text(encoding="utf-8")) > 900


def test_public_repo_new_registries_have_ids():
    for rel in [
        "registries/public_repo_canon_registry.json",
        "registries/windows_build_mode_registry.json",
        "registries/mvp_v1_power_mode_registry.json",
        "registries/seed_pattern_pack_security_registry.json",
        "registries/windows_ipc_endpoint_registry.json",
        "registries/public_build_readiness_registry.json",
    ]:
        data = json.loads((ROOT / rel).read_text(encoding="utf-8"))
        assert data["registry_id"]
        assert data["version"] == "7.1"


def test_public_repo_task_and_bundle_present():
    tasks = json.loads((ROOT / "registries/codex_task_registry.json").read_text(encoding="utf-8"))["tasks"]
    task_ids = {task["id"] for task in tasks}
    for tid in ["PR-116", "PR-117", "PR-118", "PR-119", "PR-120", "PR-121", "PR-122", "PR-123"]:
        assert tid in task_ids
    bundles = json.loads((ROOT / "registries/codex_pr_bundle_registry.json").read_text(encoding="utf-8"))["bundles"]
    assert "REAL-PR-28" in {bundle["id"] for bundle in bundles}

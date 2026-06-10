import json
from pathlib import Path
from odin.cli import validate_real_pr_execution

ROOT = Path(__file__).resolve().parents[1]


def test_real_pr_execution_registry_is_consolidated_and_complete():
    assert validate_real_pr_execution() == []
    data = json.loads((ROOT / "registries/real_pr_execution_registry.json").read_text(encoding="utf-8"))
    assert len(data["execution_prs"]) == 8
    tasks = json.loads((ROOT / "registries/codex_task_registry.json").read_text(encoding="utf-8"))["tasks"]
    task_ids = {task["id"] for task in tasks}
    covered = {tid for pr in data["execution_prs"] for tid in pr["internal_tasks"]}
    assert task_ids <= covered


def test_legacy_ladders_are_marked_internal():
    task_registry = json.loads((ROOT / "registries/codex_task_registry.json").read_text(encoding="utf-8"))
    bundle_registry = json.loads((ROOT / "registries/codex_pr_bundle_registry.json").read_text(encoding="utf-8"))
    assert "internal" in task_registry["status"]
    assert "internal" in bundle_registry["status"]
    assert task_registry["actual_execution_registry"] == "registries/real_pr_execution_registry.json"
    assert bundle_registry["actual_execution_registry"] == "registries/real_pr_execution_registry.json"

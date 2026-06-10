import json
from pathlib import Path
from odin import cli

ROOT = Path(__file__).resolve().parents[1]


def test_codex_pr_bundle_registry_covers_all_internal_tasks():
    bundles = json.loads((ROOT / "registries/codex_pr_bundle_registry.json").read_text())["bundles"]
    tasks = json.loads((ROOT / "registries/codex_task_registry.json").read_text())["tasks"]
    task_ids = {t["id"] for t in tasks}
    covered = {tid for b in bundles for tid in b["internal_tasks"]}
    assert task_ids <= covered
    assert len(bundles) >= 9


def test_codex_pr_bundle_docs_are_validated():
    assert cli.validate_codex_bundles() == []

import json
from pathlib import Path
from odin.cli import validate_senior_review

ROOT = Path(__file__).resolve().parents[1]


def test_senior_review_validation_clean():
    assert validate_senior_review() == []


def test_pr22_is_registered_and_bundled():
    tasks = json.loads((ROOT / "registries/codex_task_registry.json").read_text(encoding="utf-8"))["tasks"]
    assert any(task["id"] == "PR-22" for task in tasks)
    bundles = json.loads((ROOT / "registries/codex_pr_bundle_registry.json").read_text(encoding="utf-8"))["bundles"]
    assert any("PR-22" in bundle["internal_tasks"] for bundle in bundles)


def test_traceability_and_redlines_are_present():
    trace = (ROOT / "docs/TRACEABILITY_MATRIX_V7_1.md").read_text(encoding="utf-8")
    redlines = (ROOT / "docs/SEMANTIC_BUS_RED_LINES_V7_1.md").read_text(encoding="utf-8")
    assert "PR-22" in trace
    assert "REAL-PR-08" in trace
    assert "The bus may not mutate app state" in redlines
    assert "candidate_applied" in redlines

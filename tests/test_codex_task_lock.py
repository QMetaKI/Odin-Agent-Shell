import json
from pathlib import Path
from odin.cli import validate_codex_tasks

ROOT = Path(__file__).resolve().parents[1]


def test_codex_task_lock_validation_clean():
    assert validate_codex_tasks() == []


def test_codex_task_registry_is_substantial():
    data = json.loads((ROOT / "registries/codex_task_registry.json").read_text(encoding="utf-8"))
    tasks = data["tasks"]
    assert len(tasks) >= 20
    ids = [t["id"] for t in tasks]
    assert ids[0] == "PR-00"
    assert "PR-21" in ids
    for task in tasks:
        assert (ROOT / task["doc"]).exists(), task["doc"]
        text = (ROOT / task["doc"]).read_text(encoding="utf-8")
        assert "Definition of Done" in text
        assert "Forbidden Scope" in text


def test_codex_task_lock_docs_present():
    required = [
        "docs/codex/CODEX_TASK_LOCK_V0_4_0.md",
        "docs/codex/IMPLEMENTATION_SEQUENCE_V0_4_0.md",
        "docs/codex/PR_DEPENDENCY_GRAPH_V0_4_0.md",
        "docs/codex/TASK_DOD_MATRIX_V0_4_0.md",
        "docs/codex/CODEX_PROMPT_PACKS_V0_4_0.md",
        "docs/codex/PR_TASK_INDEX.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists()

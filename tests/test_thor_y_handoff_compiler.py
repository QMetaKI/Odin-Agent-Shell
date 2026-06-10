from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def test_thor_y_handoff_docs_and_red_lines_exist():
    docs = [
        "docs/THOR_Y_HANDOFF_COMPILER_CORE_V7_1.md",
        "docs/THOR_PROMPT_EXTRACTION_AND_PULL_V7_1.md",
        "docs/THOR_RETURN_REVIEW_RECEIPT_PIPELINE_V7_1.md",
        "docs/Y_HANDOFF_COMPILER_BRIDGE_V7_1.md",
        "docs/MJOLNIR_STRIKE_HANDOFF_BRIDGE_V7_1.md",
        "docs/HANDOFF_PROMPT_CANONICALIZATION_V7_1.md",
        "docs/HANDOFF_TO_UNIVERSAL_WORK_FLOW_V7_1.md",
        "docs/HANDOFF_POSTPROCESSING_CANDIDATE_PIPELINE_V7_1.md",
        "docs/THOR_Y_MJOLNIR_CONSOLIDATION_V7_1.md",
    ]
    for rel in docs:
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert "candidate-only" in text
        assert "No autonomous" in text or "No agent swarm" in text
        assert "Universal Work" in text
        assert "Why Trace" in text


def test_handoff_registries_and_tasks_are_wired():
    for rel in [
        "registries/handoff_source_registry.json",
        "registries/thor_handoff_mode_registry.json",
        "registries/handoff_prompt_pattern_registry.json",
        "registries/y_handoff_bridge_registry.json",
        "registries/mjolnir_bridge_registry.json",
        "registries/handoff_postprocess_registry.json",
    ]:
        data = json.loads((ROOT / rel).read_text(encoding="utf-8"))
        assert "registry_id" in data
        assert "version" in data
    tasks = json.loads((ROOT / "registries/codex_task_registry.json").read_text(encoding="utf-8"))["tasks"]
    task_ids = {t["id"] for t in tasks}
    for i in range(73, 81):
        assert f"PR-{i:02d}" in task_ids
    bundles = json.loads((ROOT / "registries/codex_pr_bundle_registry.json").read_text(encoding="utf-8"))["bundles"]
    real20 = [b for b in bundles if b["id"] == "REAL-PR-20"][0]
    assert set(real20["internal_tasks"]) == {f"PR-{i:02d}" for i in range(73, 81)}


def test_handoff_shadow_modules_and_fixtures_exist():
    for rel in [
        "odin/shadow_runtime/thor_handoff_compiler_shadow.py",
        "odin/shadow_runtime/handoff_prompt_pull_shadow.py",
        "odin/shadow_runtime/thor_return_review_shadow.py",
        "odin/shadow_runtime/y_handoff_bridge_shadow.py",
        "odin/shadow_runtime/mjolnir_strike_bridge_shadow.py",
        "odin/shadow_runtime/handoff_to_universal_work_shadow.py",
        "odin/shadow_runtime/handoff_postprocessing_shadow.py",
        "examples/handoff/thor_handoff_compile_flow.valid.json",
        "examples/handoff/thor_direct_apply_handoff.invalid.json",
        "examples/handoff/y_handoff_bridge.valid.json",
        "examples/handoff/mjolnir_strike_candidate.valid.json",
    ]:
        assert (ROOT / rel).exists(), rel

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REBASELINE_DOCS = [
    "docs/rebaseline/LOCAL_RUNTIME_HUB_TARGET_V1.md",
    "docs/rebaseline/CURRENT_STATE_AUDIT_LOCAL_RUNTIME_HUB.md",
    "docs/rebaseline/SLICE_PR_COVERAGE_MATRIX_LOCAL_RUNTIME_HUB.md",
    "docs/rebaseline/LEGACY_QUARANTINE_PLAN_LOCAL_RUNTIME_HUB.md",
    "docs/rebaseline/LOCAL_RUNTIME_HUB_BUILD_LADDER_V1.md",
    "docs/rebaseline/LOCAL_RUNTIME_HUB_100_PERCENT_DEFINITION.md",
]

PROMPTS = [
    "docs/rebaseline/prompts/LRH-PR-01_REBASELINE.md",
    "docs/rebaseline/prompts/LRH-PR-02_AGENT_OPERATOR_MODE.md",
    "docs/rebaseline/prompts/LRH-PR-03_PORTABLE_LOCAL_RUNTIME_STARTER.md",
    "docs/rebaseline/prompts/LRH-PR-04_RUNTIME_DOCTOR_BOOTSTRAP.md",
    "docs/rebaseline/prompts/LRH-PR-05_LOCALHOST_API_SDK_BRIDGE.md",
    "docs/rebaseline/prompts/LRH-PR-06_BROWSER_ODIN_HUB_SHELL.md",
]

LIVE_SOURCE_PREFIXES = (
    "odin/",
    "odin_app_sdk/",
    "sdk/",
    "schemas/v7_1/",
    "tests/",
)


def load_json(rel: str):
    with (ROOT / rel).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def test_rebaseline_documents_exist() -> None:
    for rel in REBASELINE_DOCS:
        path = ROOT / rel
        assert path.exists(), rel
        assert path.read_text(encoding="utf-8").strip(), rel


def test_rebaseline_registries_are_valid_json() -> None:
    manifest = load_json("registries/rebaseline_manifest_v1.json")
    assert manifest["artifact_kind"] == "odin_rebaseline_manifest"
    assert manifest["target"] == "Odin Local Runtime Hub"

    coverage = load_json("registries/rebaseline_coverage_matrix_v1.json")
    assert coverage["artifact_kind"] == "odin_rebaseline_coverage_matrix"
    assert coverage["entries"]


def test_build_ladder_ids_are_deterministic_and_ordered() -> None:
    ladder = load_json("registries/local_runtime_hub_build_ladder_v1.json")
    ids = [entry["id"] for entry in ladder["ladder"]]
    assert ids == [f"LRH-PR-{index:02d}" for index in range(1, 18)]
    assert ladder["ladder"][0]["expected_branch_name"] == "codex/rebaseline-local-runtime-hub-build-ladder"


def test_first_five_prompts_exist() -> None:
    for rel in PROMPTS:
        path = ROOT / rel
        assert path.exists(), rel
        text = path.read_text(encoding="utf-8")
        for anchor in ["Branch", "PR title", "Objective", "Required commands", "Proof boundaries"]:
            assert anchor in text, f"{rel} missing {anchor}"


def test_legacy_map_valid_and_no_live_source_paths_moved() -> None:
    legacy_map = load_json("legacy/LEGACY_MAP.json")
    assert legacy_map["policy"] == "quarantine_not_delete"
    for move in legacy_map.get("moves", []):
        old_path = move.get("old_path", "")
        assert not old_path.startswith(LIVE_SOURCE_PREFIXES), old_path
        assert move.get("do_not_delete") is True


def test_system_map_references_rebaseline_docs() -> None:
    system_map = load_json("SYSTEM_MAP.json")
    docs = set(system_map.get("canonical_docs", []))
    for rel in REBASELINE_DOCS:
        assert rel in docs
    lrh = system_map.get("local_runtime_hub_rebaseline", {})
    assert lrh.get("target") == "Odin Local Runtime Hub"


def test_agent_operator_mode_inserted_as_lrh_pr_02() -> None:
    target = (ROOT / "docs/rebaseline/LOCAL_RUNTIME_HUB_TARGET_V1.md").read_text(encoding="utf-8")
    ladder_doc = (ROOT / "docs/rebaseline/LOCAL_RUNTIME_HUB_BUILD_LADDER_V1.md").read_text(encoding="utf-8")
    for text in [target, ladder_doc]:
        assert "Odin Agent Operator Mode" in text
        assert "Thor-compatible" in text
        assert "Codex" in text
        assert "Claude Code" in text

    ladder = load_json("registries/local_runtime_hub_build_ladder_v1.json")
    lrh_pr_02 = ladder["ladder"][1]
    assert lrh_pr_02["id"] == "LRH-PR-02"
    assert lrh_pr_02["title"] == "Odin Agent Operator Mode"
    serialized = json.dumps(lrh_pr_02)
    assert "Codex" in serialized
    assert "Claude Code" in serialized
    assert "Thor-compatible" in serialized
    assert ladder["ladder"][2]["id"] == "LRH-PR-03"
    assert ladder["ladder"][2]["title"] == "Portable Local Runtime Starter"


def test_agent_operator_manifest_and_coverage_mapping() -> None:
    manifest = load_json("registries/rebaseline_manifest_v1.json")
    assert manifest["new_ladder"] == "LRH-PR-01..17"
    assert "Agent Operator Mode" in json.dumps(manifest)

    coverage = load_json("registries/rebaseline_coverage_matrix_v1.json")
    mapped = {entry["id"]: entry for entry in coverage["entries"]}
    for required in [
        "AGENT-OPERATOR-THOR",
        "AGENT-OPERATOR-CODEX",
        "AGENT-OPERATOR-CLAUDE-CODE",
        "AGENT-OPERATOR-FUTURE-LOCAL-AGENTS",
    ]:
        assert mapped[required]["new_ladder_mapping"].startswith("LRH-PR-02")

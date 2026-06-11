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
    assert ladder["ladder"][0]["expected_branch_name"] == "codex/rebaseline-local-runtime-hub"


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



def test_final_road_to_100_normalization() -> None:
    audit = (ROOT / "docs/rebaseline/CURRENT_STATE_AUDIT_LOCAL_RUNTIME_HUB.md").read_text(encoding="utf-8")
    assert "codex/rebaseline-local-runtime-hub-build-ladder" not in audit
    assert "75aa45b" not in audit
    assert "Branch | `codex/rebaseline-local-runtime-hub`" in audit
    assert "Runtime behavior changed | no" in audit

    ladder = load_json("registries/local_runtime_hub_build_ladder_v1.json")
    ids = [entry["id"] for entry in ladder["ladder"]]
    assert ids == [f"LRH-PR-{index:02d}" for index in range(1, 18)]
    by_id = {entry["id"]: entry for entry in ladder["ladder"]}
    assert by_id["LRH-PR-02"]["title"] == "Odin Agent Operator Mode"
    assert by_id["LRH-PR-03"]["title"] == "Portable Local Runtime Starter"
    assert "LRH-PR-02" in by_id["LRH-PR-03"]["depends_on"]
    assert by_id["LRH-PR-12"]["title"] == "Neutral External App Bridge Pack"
    assert by_id["LRH-PR-13"]["title"] == "Generic App Bridge Examples and Golden Harness"
    for entry in ladder["ladder"]:
        for field in [
            "id", "title", "objective", "why_this_slice_exists", "depends_on",
            "current_coverage", "missing_work", "target_files", "allowed_new_files",
            "forbidden_scope", "required_behavior", "required_tests", "required_commands",
            "acceptance_gates", "proof_boundaries", "senior_reviewer_focus",
            "senior_code_reviewer_focus", "expected_branch_name", "expected_pr_title",
            "old_ladder_mapping", "definition_of_done", "next_slice_unlock",
        ]:
            assert field in entry, f"{entry['id']} missing {field}"
        assert "implementation, tests, receipts" not in json.dumps(entry)


def test_road_to_100_acceptance_harness_exists_and_is_valid() -> None:
    doc = ROOT / "docs/rebaseline/ROAD_TO_100_ACCEPTANCE_HARNESS_V1.md"
    assert doc.exists()
    assert "future target proof commands" in doc.read_text(encoding="utf-8")
    harness = load_json("registries/road_to_100_acceptance_harness_v1.json")
    assert harness["artifact_kind"] == "odin_road_to_100_acceptance_harness"
    # LRH-PR-17 updated schema: command_matrix with status/known_non_proof fields
    cmd_entries = harness.get("command_matrix", harness.get("commands", []))
    commands = {}
    for entry in cmd_entries:
        cmd = entry["command"]
        # Index by full command and by base suffix (without flags) for lookup
        commands[cmd] = entry
        base = cmd.replace("python -m odin.cli ", "").split()[0]
        commands[base] = entry
    for suffix in [
        "prove-local-runtime",
        "prove-agent-operator-mode",
        "prove-sdk-bridge",
        "prove-browser-hub",
        "prove-external-app-bridge",
        "prove-portable-package",
        "emit-support-bundle",
    ]:
        assert suffix in commands, f"command not found in registry: {suffix}"
        entry = commands[suffix]
        assert entry.get("known_non_proof") or entry.get("proof_boundary"), (
            f"{suffix}: known_non_proof or proof_boundary required"
        )
        assert entry.get("status") in {"implemented_now", "missing_command"}, (
            f"{suffix}: status must be implemented_now or missing_command"
        )


def test_100_percent_definition_categories_and_review_verdict() -> None:
    definition = (ROOT / "docs/rebaseline/LOCAL_RUNTIME_HUB_100_PERCENT_DEFINITION.md").read_text(encoding="utf-8")
    for category in [
        "A. Startability", "B. Runtime Health", "C. Localhost API", "D. Browser Hub",
        "E. Agent Operator Mode", "F. SDK Bridge", "G. External App Bridge",
        "H. Universal Work Playground", "I. Provider / Worker / Pre-LLM Visibility",
        "J. Packaging", "K. Support Bundle", "L. Boundary Preservation",
        "M. CI/Test Acceptance", "N. Public Naming Neutrality",
    ]:
        assert category in definition
    assert "No concrete external app/product/project names" in definition

    review = (ROOT / "docs/rebaseline/REBASELINE_REVIEW_REPORT_V1.md").read_text(encoding="utf-8")
    assert "Required amendment before merge" not in review
    assert "Merge-ready after validation if all tests pass" in review


def test_prompt_pack_and_public_naming_neutrality() -> None:
    for rel in [
        "docs/rebaseline/prompts/LRH-PR-02_AGENT_OPERATOR_MODE.md",
        "docs/rebaseline/prompts/LRH-PR-03_PORTABLE_LOCAL_RUNTIME_STARTER.md",
        "docs/rebaseline/prompts/LRH-PR-06_BROWSER_ODIN_HUB_SHELL.md",
    ]:
        assert (ROOT / rel).exists(), rel

    checked_roots = [
        ROOT / "docs/rebaseline",
        ROOT / "registries/local_runtime_hub_build_ladder_v1.json",
        ROOT / "registries/rebaseline_manifest_v1.json",
        ROOT / "registries/rebaseline_coverage_matrix_v1.json",
        ROOT / "registries/road_to_100_acceptance_harness_v1.json",
        ROOT / "tests/test_local_runtime_hub_rebaseline.py",
    ]
    banned = ["Y" + "Node", "y" + "node"]
    haystack = []
    for path in checked_roots:
        if path.is_dir():
            for child in path.rglob("*"):
                if child.is_file():
                    haystack.append((str(child.relative_to(ROOT)), child.read_text(encoding="utf-8")))
        else:
            haystack.append((str(path.relative_to(ROOT)), path.read_text(encoding="utf-8")))
    for name, content in haystack:
        for banned_name in banned:
            assert banned_name not in content, f"{banned_name} found in {name}"
    neutral_text = "\n".join(content for _, content in haystack)
    for neutral in ["external app", "host app", "reference app", "generic app bridge"]:
        assert neutral in neutral_text

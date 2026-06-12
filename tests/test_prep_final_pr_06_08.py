from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_master_prep_plan_loads() -> None:
    data = json.loads(read("registries/prep_final_pr_06_08_plan.v1.json"))
    assert data["roadmap_amendment"]["FINAL-PR-06"].startswith("Operational Seed Spine")
    assert data["status"] == "prepared_not_complete"


def test_source_pattern_synthesis_loads() -> None:
    data = json.loads(read("reports/prep_final_pr_06_08_source_pattern_synthesis.json"))
    assert data["candidate_only"] is True
    assert len(data["source_classes"]) >= 9
    assert "not truth" in data["required_note"]


def test_pr06_prompt_exists_and_contains_operational_seed_objective() -> None:
    text = read("docs/codex/prompts/FINAL_PR_06_OPERATIONAL_SEED_SPINE_CLAUDE_PROMPT.md")
    assert "Operational Seed Spine" in text
    assert "Implement operational intent seeds" in text


def test_pr07_prompt_exists_and_contains_dfas_field_selection_objective() -> None:
    text = read("docs/codex/prompts/FINAL_PR_07_DFAS_FIELD_SELECTION_CLAUDE_PROMPT.md")
    assert "DFAS Field Selection" in text
    assert "field selection" in text.lower()


def test_pr08_prompt_exists_and_contains_projection_spine_objective() -> None:
    text = read("docs/codex/prompts/FINAL_PR_08_PROJECTION_SHADOW_CANDIDATE_CLAUDE_PROMPT.md")
    assert "Projection Spine" in text
    assert "expression packet" in text.lower()


def test_pr09_prompt_exists_and_contains_release_closure_objective() -> None:
    text = read("docs/codex/prompts/FINAL_PR_09_RELEASE_CLOSURE_CLAUDE_PROMPT.md")
    assert "Release / Closure" in text
    assert "FINAL-PR-09 runs after FINAL-PR-06" in text


def test_all_future_prompts_contain_forbidden_scope() -> None:
    for rel in [
        "docs/codex/prompts/FINAL_PR_06_OPERATIONAL_SEED_SPINE_CLAUDE_PROMPT.md",
        "docs/codex/prompts/FINAL_PR_07_DFAS_FIELD_SELECTION_CLAUDE_PROMPT.md",
        "docs/codex/prompts/FINAL_PR_08_PROJECTION_SHADOW_CANDIDATE_CLAUDE_PROMPT.md",
        "docs/codex/prompts/FINAL_PR_09_RELEASE_CLOSURE_CLAUDE_PROMPT.md",
    ]:
        assert "## Forbidden scope" in read(rel)


def test_all_future_prompts_contain_validator_tests_and_proof_requirements() -> None:
    for rel in [
        "docs/codex/prompts/FINAL_PR_06_OPERATIONAL_SEED_SPINE_CLAUDE_PROMPT.md",
        "docs/codex/prompts/FINAL_PR_07_DFAS_FIELD_SELECTION_CLAUDE_PROMPT.md",
        "docs/codex/prompts/FINAL_PR_08_PROJECTION_SHADOW_CANDIDATE_CLAUDE_PROMPT.md",
        "docs/codex/prompts/FINAL_PR_09_RELEASE_CLOSURE_CLAUDE_PROMPT.md",
    ]:
        text = read(rel)
        assert "## Validator requirement" in text
        assert "## Tests requirement" in text
        assert "## Proof packet requirement" in text


def test_pr06_prompt_forbids_seed_authority() -> None:
    text = read("docs/codex/prompts/FINAL_PR_06_OPERATIONAL_SEED_SPINE_CLAUDE_PROMPT.md")
    assert "Seeds do not decide truth" in text
    assert "Role profiles are not personas" in text


def test_pr07_prompt_forbids_field_selection_authority() -> None:
    text = read("docs/codex/prompts/FINAL_PR_07_DFAS_FIELD_SELECTION_CLAUDE_PROMPT.md")
    assert "does not authorize apply" in text
    assert "model execution" in text
    assert "external send" in text


def test_pr08_prompt_forbids_projection_runtime_proof() -> None:
    text = read("docs/codex/prompts/FINAL_PR_08_PROJECTION_SHADOW_CANDIDATE_CLAUDE_PROMPT.md")
    assert "not runtime proof" in text
    assert "not executable runtime" in text


def test_release_closure_moved_to_final_pr09() -> None:
    roadmap = read("docs/rebaseline/FINAL_MINIMAL_ROAD_TO_100_PR_ROADMAP_V1.md")
    acceptance = json.loads(read("registries/final_100_percent_acceptance_definition_v1.json"))
    assert "FINAL-PR-09: Release / Closure / Full Acceptance" in roadmap
    assert acceptance["release_closure_shift"] == "FINAL-PR-09 runs after FINAL-PR-06, FINAL-PR-07, and FINAL-PR-08."


def test_validate_prep_final_pr_06_08_passes() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "validate-prep-final-pr-06-08"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    assert result.returncode == 0, result.stdout


def test_validate_all_passes() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "validate-all"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    assert result.returncode == 0, result.stdout


def test_full_pytest_command_is_required_in_prep_plan() -> None:
    plan = json.loads(read("registries/prep_final_pr_06_08_plan.v1.json"))
    commands = "\n".join(plan["expected_tests"]) + "\n" + read("docs/codex/reports/PREP_FINAL_PR_06_08_RETURN_REPORT.md")
    assert "test_final_pr_06_operational_seed_spine.py" in commands
    assert "test_final_pr_07_field_selection.py" in commands
    assert "test_final_pr_08_projection_spine.py" in commands


def test_return_report_contains_merge_conflict_repair_section() -> None:
    text = read("docs/codex/reports/PREP_FINAL_PR_06_08_RETURN_REPORT.md")
    assert "## Merge Conflict Repair" in text
    assert "current main SHA used" in text
    assert "conflicted files" in text
    assert "resolution policy" in text


def test_generated_report_contains_merge_conflict_repair_object() -> None:
    data = json.loads(read("reports/prep_final_pr_06_08_report.json"))
    repair = data.get("merge_conflict_repair", {})
    assert repair.get("current_main_sha_used")
    assert repair.get("final_status", "").startswith("prep_repair_bounded")

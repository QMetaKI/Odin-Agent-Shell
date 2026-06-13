"""Tests for PREP FINAL-PR-09++/10++ Q-Shabang small-model prep.

Claim boundary: prep_tests_check_scaffold_artifacts_not_runtime_execution
candidate_only: true
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/codex/prompts/FINAL_PR_09_PLUSPLUS_SMALL_MODEL_OPERATIONAL_SPINE_CLAUDE_CODE_PROMPT.md",
    "docs/codex/prompts/FINAL_PR_10_PLUSPLUS_QSHABANG_BOUNDARY_RELEASE_CLAUDE_CODE_PROMPT.md",
    "docs/codex/handoffs/PREP_FINAL_PR_09_10_PLUSPLUS_QSHABANG_SMALLMODEL_WORK_PACKET.md",
    "docs/release/FINAL_PR_09_10_PLUSPLUS_QSHABANG_SMALLMODEL_ACCEPTANCE_MATRIX.md",
    "reports/final_pr_09_10_plusplus_qshabang_smallmodel_acceptance_matrix.json",
    "registries/final_pr_09_10_plusplus_qshabang_smallmodel_prep_registry.json",
    "reports/final_pr_09_10_plusplus_qshabang_smallmodel_prep_report.json",
]

REQUIRED_SUBSYSTEMS = [
    "Local Hub", "CLI", "Universal Work", "Handoff-First", "Runtime Engine", "Context Capsule",
    "Artifact Lens", "Slot Forge", "Gaptext", "ModelWorkPacket", "Small Model Route Plan", "3B Roles",
    "7B Roles", "3B+7B Hybrid Roles", "No-Model Precompute", "Semantic Cache", "Work Memory",
    "QIRC", "Provider Probe", "Execution Gate", "Operational Seed Spine", "Field Selection Spine",
    "Projection Candidate Spine", "Minicheck", "Critic Cascade", "Candidate Tournament", "Candidate Artifact",
    "Response Packet", "Final Gate", "Trace/Receipt/Proof", "App-Owned Apply Boundary",
    "Q-Shabang Runtime Map", "Bug6/Q7 Boundary Map", "Artifact Currency", "Release Evidence", "Final Preflight",
]

REQUIRED_ANCHORS = [
    "candidate-only", "app-owned apply", "no external send", "no hidden authority",
    "no live model inference claim", "local provider seam disabled by default", "operational spine",
    "small-model route plan", "3B", "7B", "hybrid", "ModelWorkPacket", "Q-Shabang operational map",
    "deferred system lift", "boundary matrix", "model role authority", "release preflight", "FINAL-PR-11",
]

FORBIDDEN_PHRASES = [
    "security_verified",
    "model benchmark verified",
    "live_model_inference_verified",
    "release certified",
    "external send enabled by default",
]


def load_json(rel: str):
    with (ROOT / rel).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def test_prep_artifacts_exist():
    for rel in REQUIRED_FILES:
        assert (ROOT / rel).exists(), rel


def test_json_artifacts_parse():
    for rel in [
        "reports/final_pr_09_10_plusplus_qshabang_smallmodel_acceptance_matrix.json",
        "registries/final_pr_09_10_plusplus_qshabang_smallmodel_prep_registry.json",
        "reports/final_pr_09_10_plusplus_qshabang_smallmodel_prep_report.json",
    ]:
        assert isinstance(load_json(rel), dict)


def test_prompts_contain_required_anchors():
    text = "\n".join((ROOT / rel).read_text(encoding="utf-8") for rel in REQUIRED_FILES if rel.endswith(".md"))
    lower = text.lower()
    for anchor in REQUIRED_ANCHORS:
        assert anchor.lower() in lower, anchor


def test_acceptance_matrix_contains_all_required_subsystems():
    text = (ROOT / "docs/release/FINAL_PR_09_10_PLUSPLUS_QSHABANG_SMALLMODEL_ACCEPTANCE_MATRIX.md").read_text(encoding="utf-8")
    matrix = load_json("reports/final_pr_09_10_plusplus_qshabang_smallmodel_acceptance_matrix.json")
    json_subsystems = {row["subsystem"] for row in matrix["subsystems"]}
    for subsystem in REQUIRED_SUBSYSTEMS:
        assert subsystem in text
        assert subsystem in json_subsystems


def test_registry_references_existing_files():
    registry = load_json("registries/final_pr_09_10_plusplus_qshabang_smallmodel_prep_registry.json")
    assert registry["candidate_only"] is True
    for key in ["prompt_files", "work_packet_files", "acceptance_matrix_files"]:
        for rel in registry[key]:
            assert (ROOT / rel).exists(), rel


def test_validator_command_can_run():
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "validate-final-pr-09-10-qshabang-smallmodel-prep"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_no_forbidden_positive_claims_in_prep_artifacts():
    text = "\n".join((ROOT / rel).read_text(encoding="utf-8", errors="ignore") for rel in REQUIRED_FILES)
    lower = text.lower()
    for phrase in FORBIDDEN_PHRASES:
        assert phrase not in lower, phrase

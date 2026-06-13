"""Validate PREP FINAL-PR-09++/10++ Q-Shabang small-model artifacts.

Claim boundary: prep_validator_checks_artifact_presence_not_runtime_proof
candidate_only: true
local_only: true
stdlib_only: true
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
from pathlib import Path

CLAIM_BOUNDARY = "prep_validator_checks_artifact_presence_not_runtime_proof"

PROMPTS = [
    "docs/codex/prompts/FINAL_PR_09_PLUSPLUS_SMALL_MODEL_OPERATIONAL_SPINE_CLAUDE_CODE_PROMPT.md",
    "docs/codex/prompts/FINAL_PR_10_PLUSPLUS_QSHABANG_BOUNDARY_RELEASE_CLAUDE_CODE_PROMPT.md",
]
WORK_PACKET = "docs/codex/handoffs/PREP_FINAL_PR_09_10_PLUSPLUS_QSHABANG_SMALLMODEL_WORK_PACKET.md"
ACCEPTANCE_MD = "docs/release/FINAL_PR_09_10_PLUSPLUS_QSHABANG_SMALLMODEL_ACCEPTANCE_MATRIX.md"
ACCEPTANCE_JSON = "reports/final_pr_09_10_plusplus_qshabang_smallmodel_acceptance_matrix.json"
REGISTRY = "registries/final_pr_09_10_plusplus_qshabang_smallmodel_prep_registry.json"
REPORT = "reports/final_pr_09_10_plusplus_qshabang_smallmodel_prep_report.json"

REQUIRED_FILES = [*PROMPTS, WORK_PACKET, ACCEPTANCE_MD, ACCEPTANCE_JSON, REGISTRY, REPORT]
JSON_FILES = [ACCEPTANCE_JSON, REGISTRY, REPORT, "SYSTEM_MAP.json", "FILE_MANIFEST.json"]
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
FORBIDDEN_POSITIVE_CLAIMS = [
    "security_verified",
    "model benchmark verified",
    "live_model_inference_verified",
    "release certified",
    "external send enabled by default",
]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def rel_exists(repo_root: Path, rel: str) -> bool:
    return (repo_root / rel).exists()


def combined_text(repo_root: Path) -> str:
    chunks = []
    for rel in REQUIRED_FILES:
        p = repo_root / rel
        if p.exists() and p.suffix.lower() in {".md", ".json"}:
            chunks.append(p.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(chunks)


def validate(repo_root: Path) -> list[str]:
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not rel_exists(repo_root, rel):
            errors.append(f"missing required prep artifact: {rel}")

    for rel in JSON_FILES:
        p = repo_root / rel
        if not p.exists():
            errors.append(f"missing JSON artifact: {rel}")
            continue
        try:
            load_json(p)
        except Exception as exc:  # pragma: no cover - diagnostic path
            errors.append(f"JSON parse failed for {rel}: {exc}")

    text = combined_text(repo_root)
    lower = text.lower()
    for anchor in REQUIRED_ANCHORS:
        if anchor.lower() not in lower:
            errors.append(f"missing required anchor across prep artifacts: {anchor}")

    acceptance = repo_root / ACCEPTANCE_MD
    if acceptance.exists():
        md = acceptance.read_text(encoding="utf-8", errors="ignore")
        for subsystem in REQUIRED_SUBSYSTEMS:
            if subsystem not in md:
                errors.append(f"acceptance matrix missing subsystem: {subsystem}")

    try:
        registry = load_json(repo_root / REGISTRY)
    except Exception:
        registry = {}
    if registry:
        if registry.get("candidate_only") is not True:
            errors.append("registry candidate_only must be true")
        for key in ["prep_id", "claim_boundary", "target_prs", "prompt_files", "work_packet_files", "acceptance_matrix_files", "qshabang_components", "small_model_roles", "deferred_systems", "expected_future_files", "non_scope", "validation_commands", "release_sequence", "not_proven"]:
            if key not in registry:
                errors.append(f"registry missing key: {key}")
        for group_key in ["prompt_files", "work_packet_files", "acceptance_matrix_files"]:
            for rel in registry.get(group_key, []):
                if not rel_exists(repo_root, rel):
                    errors.append(f"registry references missing file in {group_key}: {rel}")

    system_map = load_json(repo_root / "SYSTEM_MAP.json") if (repo_root / "SYSTEM_MAP.json").exists() else {}
    if "prep_final_pr_09_10_qshabang_smallmodel" not in system_map:
        errors.append("SYSTEM_MAP.json missing prep_final_pr_09_10_qshabang_smallmodel entry")

    manifest = load_json(repo_root / "FILE_MANIFEST.json") if (repo_root / "FILE_MANIFEST.json").exists() else {}
    manifest_paths = {entry.get("path") for entry in manifest.get("files", []) if isinstance(entry, dict)}
    for rel in REQUIRED_FILES + ["tools/rebaseline/check_final_pr_09_10_qshabang_smallmodel_prep.py", "tests/test_final_pr_09_10_qshabang_smallmodel_prep.py"]:
        if rel not in manifest_paths:
            errors.append(f"FILE_MANIFEST.json missing required path: {rel}")

    for phrase in FORBIDDEN_POSITIVE_CLAIMS:
        if phrase in lower:
            errors.append(f"forbidden positive claim phrase introduced: {phrase}")

    return errors


def build_report(repo_root: Path, errors: list[str], generated_at_utc: str) -> dict:
    return {
        "artifact_kind": "final_pr_09_10_qshabang_smallmodel_prep_validation_report",
        "candidate_only": True,
        "local_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "status": "ok" if not errors else "error",
        "errors": errors,
        "checked_files": REQUIRED_FILES,
        "required_anchors": REQUIRED_ANCHORS,
        "not_proven": [
            "production_readiness", "security_certification", "real_model_benchmark",
            "live_model_inference", "release_certification",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", default=None)
    parser.add_argument("--generated-at-utc", default=None)
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    generated_at = args.generated_at_utc or _dt.datetime.now(_dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    errors = validate(repo_root)
    report = build_report(repo_root, errors, generated_at)
    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

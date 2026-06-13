#!/usr/bin/env python3
"""Validate FINAL-PR-08 Projection Candidate Spine artifacts."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CLAIM_BOUNDARY = "projection_candidate_spine_prepares_candidates_not_runtime_execution"

REQUIRED_MATERIALIZATION_LEVELS = [
    "M0_raw_input", "M1_handoff_context", "M2_universal_work", "M3_seed_route",
    "M4_field_selection", "M5_projection_set", "M6_candidate_artifact",
    "M7_response_packet", "M8_trace_receipt", "M9_release_evidence",
]

REQUIRED_FILES = [
    "odin/projection_candidate_spine/__init__.py",
    "odin/projection_candidate_spine/materialization.py",
    "odin/projection_candidate_spine/candidate_graph.py",
    "odin/projection_candidate_spine/projection_set.py",
    "odin/projection_candidate_spine/expression_packet.py",
    "odin/projection_candidate_spine/compare.py",
    "odin/projection_candidate_spine/receipt_link.py",
    "odin/projection_candidate_spine/proof.py",
    "registries/final_pr_08_projection_candidate_spine_registry.json",
    "schemas/final_pr_08_projection_candidate_spine_proof_packet.schema.json",
    "examples/final_pr_08/projection_set.example.json",
    "examples/final_pr_08/candidate_graph.example.json",
    "examples/final_pr_08/expression_packet.example.json",
    "examples/final_pr_08/projection_proof_packet.example.json",
    "tools/rebaseline/check_final_pr_08_projection_candidate_spine.py",
    "tests/test_final_pr_08_projection_candidate_spine.py",
    "reports/final_pr_08_projection_candidate_spine_proof_packet.json",
    "reports/final_pr_08_projection_candidate_spine_report.json",
    "docs/rebaseline/FINAL_PR_08_PROJECTION_CANDIDATE_SPINE.md",
    "docs/codex/handoffs/FINAL_PR_08_REPO_COGNITION_SUMMARY.md",
    "docs/codex/handoffs/FINAL_PR_08_THOR_STYLE_FIELD_TO_PROJECTION_HANDOFF.md",
    "docs/codex/handoffs/FINAL_PR_08_ODIN_AGENT_OPERATOR_WORK_PACKET.md",
    "docs/codex/audits/FINAL_PR_08_PROJECTION_CANDIDATE_SPINE_AUDIT.md",
    "docs/codex/audits/FINAL_PR_08_SENIOR_REVIEW.md",
    "docs/codex/audits/FINAL_PR_08_CODE_REVIEW.md",
    "docs/codex/audits/FINAL_PR_08_THOR_ODIN_Y_EFFECTIVENESS_AUDIT.md",
    "docs/codex/reports/FINAL_PR_08_PROJECTION_CANDIDATE_SPINE_RETURN_REPORT.md",
]

REQUIRED_PROVEN = [
    "materialization_levels_defined",
    "projection_set_candidate_only",
    "candidate_graph_structured",
    "expression_packet_near_code_not_executed",
    "receipt_link_traceable",
]

REQUIRED_NOT_PROVEN = [
    "hidden_runtime",
    "model_inference",
    "provider_execution",
    "app_apply",
    "app_state_mutation",
    "external_send",
    "generated_code_correctness",
    "production_readiness",
    "security_certification",
]

FORBIDDEN_NAMES = ["dfas", "q_shabang", "qmath", "q_state", "qgit", "qcode", "qli", "qstar"]
FORBIDDEN_CALL_TOKENS = [
    "openai.", "anthropic.", "requests.", "urllib.request.urlopen",
    "http.client", "socket.", "subprocess.", "os.system",
    "eval(", "exec(",
]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def add(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def validate(repo_root: Path) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    checked: list[str] = []

    # Required files exist
    for rel in REQUIRED_FILES:
        p = repo_root / rel
        checked.append(rel)
        add(errors, p.exists(), f"missing required file: {rel}")

    # Registry checks
    registry_path = repo_root / "registries/final_pr_08_projection_candidate_spine_registry.json"
    if registry_path.exists():
        try:
            reg = load_json(registry_path)
            add(errors, reg.get("candidate_only") is True, "registry candidate_only must be true")
            add(errors, reg.get("app_owned_apply") is True, "registry app_owned_apply must be true")
            add(errors, reg.get("claim_boundary") == CLAIM_BOUNDARY, "registry claim_boundary mismatch")
            mat_levels = reg.get("materialization_levels", [])
            for level in REQUIRED_MATERIALIZATION_LEVELS:
                add(errors, level in mat_levels, f"registry missing materialization_level: {level}")
            add(errors, len(mat_levels) == 10, f"registry must have exactly 10 materialization_levels, got {len(mat_levels)}")
        except Exception as exc:
            errors.append(f"registry parse error: {exc}")

    # Schema check
    schema_path = repo_root / "schemas/final_pr_08_projection_candidate_spine_proof_packet.schema.json"
    if schema_path.exists():
        try:
            load_json(schema_path)
        except Exception as exc:
            errors.append(f"schema parse error: {exc}")

    # Materialization levels in module
    mat_path = repo_root / "odin/projection_candidate_spine/materialization.py"
    if mat_path.exists():
        mat_text = mat_path.read_text(encoding="utf-8")
        for level in REQUIRED_MATERIALIZATION_LEVELS:
            add(errors, f'"{level}"' in mat_text, f"materialization.py missing level: {level}")
        add(errors, "MATERIALIZATION_LEVELS" in mat_text, "materialization.py must define MATERIALIZATION_LEVELS")

    # Example files parse and candidate_only
    for rel, check_candidate_only in [
        ("examples/final_pr_08/projection_set.example.json", True),
        ("examples/final_pr_08/candidate_graph.example.json", True),
        ("examples/final_pr_08/expression_packet.example.json", True),
        ("examples/final_pr_08/projection_proof_packet.example.json", True),
    ]:
        p = repo_root / rel
        if p.exists():
            try:
                data = load_json(p)
                if check_candidate_only:
                    add(errors, data.get("candidate_only") is True, f"{rel}: candidate_only must be true")
            except Exception as exc:
                errors.append(f"{rel} parse error: {exc}")

    # ExpressionPacket example: near_code not executed
    expr_example = repo_root / "examples/final_pr_08/expression_packet.example.json"
    if expr_example.exists():
        try:
            expr_data = load_json(expr_example)
            add(errors, expr_data.get("near_code_execution") is False,
                "expression_packet example: near_code_execution must be false")
        except Exception:
            pass

    # CandidateGraph example: explicit edges
    graph_example = repo_root / "examples/final_pr_08/candidate_graph.example.json"
    if graph_example.exists():
        try:
            graph_data = load_json(graph_example)
            edges = graph_data.get("edges", [])
            add(errors, len(edges) > 0, "candidate_graph example must have explicit edges")
            if edges:
                for edge in edges:
                    add(errors, "from_node_id" in edge, "graph edge missing from_node_id")
                    add(errors, "to_node_id" in edge, "graph edge missing to_node_id")
                    add(errors, "relation" in edge, "graph edge missing relation")
        except Exception:
            pass

    # Proof packet checks
    proof_path = repo_root / "reports/final_pr_08_projection_candidate_spine_proof_packet.json"
    if proof_path.exists():
        try:
            proof = load_json(proof_path)
            for item in REQUIRED_PROVEN:
                add(errors, item in proof.get("proven", []), f"proof packet missing proven: {item}")
            for item in REQUIRED_NOT_PROVEN:
                add(errors, item in proof.get("not_proven", []), f"proof packet missing not_proven: {item}")
            add(errors, proof.get("candidate_only") is True, "proof packet candidate_only must be true")
            add(errors, proof.get("claim_boundary") == CLAIM_BOUNDARY, "proof packet claim_boundary mismatch")
        except Exception as exc:
            errors.append(f"proof packet parse error: {exc}")

    # Module files: no forbidden names, no forbidden calls
    module_dir = repo_root / "odin/projection_candidate_spine"
    if module_dir.exists():
        for py_file in sorted(module_dir.glob("*.py")):
            rel = py_file.relative_to(repo_root).as_posix()
            checked.append(rel)
            try:
                text = py_file.read_text(encoding="utf-8")
                text_lower = text.lower()
                for forbidden in FORBIDDEN_NAMES:
                    add(errors, forbidden not in text_lower, f"forbidden runtime name {forbidden!r} in {rel}")
                for token in FORBIDDEN_CALL_TOKENS:
                    add(errors, token not in text, f"forbidden call token {token!r} in {rel}")
            except Exception as exc:
                errors.append(f"could not read {rel}: {exc}")

    # CLI commands registered
    cli_path = repo_root / "odin/cli.py"
    if cli_path.exists():
        cli = cli_path.read_text(encoding="utf-8")
        for cmd in ["validate-projection-candidate-spine", "explain-projection-candidate", "prove-projection-candidate-spine"]:
            add(errors, cmd in cli, f"CLI command not registered: {cmd}")
        add(errors, "validate_projection_candidate_spine()" in cli,
            "validate_all must call validate_projection_candidate_spine()")

    # SYSTEM_MAP has PR08 entry
    system_map_path = repo_root / "SYSTEM_MAP.json"
    if system_map_path.exists():
        system_map_text = system_map_path.read_text(encoding="utf-8")
        add(errors, "final_pr_08_projection_candidate_spine" in system_map_text,
            "SYSTEM_MAP missing final_pr_08_projection_candidate_spine")

    # FILE_MANIFEST contains every required PR08 file
    manifest_path = repo_root / "FILE_MANIFEST.json"
    if manifest_path.exists():
        manifest_text = manifest_path.read_text(encoding="utf-8")
        for rel in REQUIRED_FILES:
            add(errors, rel in manifest_text, f"FILE_MANIFEST missing PR08 file: {rel}")

    # Prep validator recognizes PR08 as implemented
    prep_path = repo_root / "tools/rebaseline/check_prep_final_pr_06_08.py"
    if prep_path.exists():
        prep = prep_path.read_text(encoding="utf-8")
        add(errors,
            '"odin/projection_candidate_spine"' in prep and "IMPLEMENTED_PR_MODULE_DIRS" in prep,
            "prep validator does not recognize PR08 implementation in IMPLEMENTED_PR_MODULE_DIRS")

    # Prep validator still keeps PR09 deferred
    if prep_path.exists():
        prep = prep_path.read_text(encoding="utf-8")
        add(errors, "final_pr_09" in prep or "release_closure" in prep.lower(),
            "prep validator should still reference PR09 release closure protection")

    # Local hub has PR08 endpoint
    server_path = repo_root / "odin/local_hub/server.py"
    if server_path.exists():
        server = server_path.read_text(encoding="utf-8")
        add(errors, "/demo/projection-candidate.json" in server,
            "local hub server missing /demo/projection-candidate.json endpoint")

    # UI has PR08 section
    ui_path = repo_root / "odin/local_hub/ui.py"
    if ui_path.exists():
        ui = ui_path.read_text(encoding="utf-8")
        add(errors, "projection-candidate-spine-section" in ui,
            "local hub UI missing projection-candidate-spine-section ID")
        add(errors, "Projection Candidate Spine organizes candidate artifacts" in ui,
            "local hub UI missing Dev Mode copy for projection candidate spine")
        add(errors, "Odin organizes candidate work into structured sets" in ui,
            "local hub UI missing normal-user copy for projection candidate spine")
        add(errors, '"projection-candidate-spine-section"' in ui,
            "REQUIRED_IDS missing projection-candidate-spine-section")

    return errors, warnings, sorted(set(checked))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate FINAL-PR-08 Projection Candidate Spine")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", default="reports/final_pr_08_projection_candidate_spine_report.json")
    parser.add_argument("--generated-at-utc", default="2026-01-01T00:00:00Z")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    errors, warnings, checked = validate(repo_root)

    report = {
        "status": "ok" if not errors else "error",
        "error_count": len(errors),
        "warning_count": len(warnings),
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "checked_files": checked,
        "errors": errors,
        "warnings": warnings,
        "generated_at_utc": args.generated_at_utc,
    }

    out = Path(args.out)
    if not out.is_absolute():
        out = repo_root / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())

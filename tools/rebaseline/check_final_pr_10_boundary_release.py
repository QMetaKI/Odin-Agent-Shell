"""FINAL-PR-10++ Boundary-Gated Release Operationalization Validator.

Stdlib only. No external deps. No model calls. No network. No app apply.

Usage:
    python tools/rebaseline/check_final_pr_10_boundary_release.py \
        --repo-root . \
        --out reports/final_pr_10_release_preflight_report.json \
        --generated-at-utc 2026-01-01T00:00:00Z

Claim boundary: final_pr_10_boundary_gated_release_operationalization_not_release_certification
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

_CLAIM_BOUNDARY = "final_pr_10_boundary_gated_release_operationalization_not_release_certification"

_REQUIRED_MODULE_FILES = [
    "odin/release_boundaries/__init__.py",
    "odin/release_boundaries/boundary_matrix.py",
    "odin/release_boundaries/ring_authority_map.py",
    "odin/release_boundaries/bug6_q7_operational_map.py",
    "odin/release_boundaries/qshabang_release_gate_map.py",
    "odin/release_boundaries/model_role_authority.py",
    "odin/release_boundaries/artifact_currency.py",
    "odin/release_boundaries/evidence_closure.py",
    "odin/release_boundaries/final_preflight.py",
    "odin/release_boundaries/reports.py",
]

_REQUIRED_DOCS = [
    "docs/rebaseline/FINAL_PR_10_BOUNDARY_RELEASE.md",
    "docs/release/FINAL_PR_10_BOUNDARY_MATRIX.md",
    "docs/release/FINAL_PR_10_RING_AUTHORITY_MAP.md",
    "docs/release/FINAL_PR_10_BUG6_Q7_OPERATIONAL_MAP.md",
    "docs/release/FINAL_PR_10_QSHABANG_RELEASE_GATE_MAP.md",
    "docs/release/FINAL_PR_10_MODEL_ROLE_AUTHORITY_MATRIX.md",
    "docs/release/FINAL_PR_10_ARTIFACT_CURRENCY_INDEX.md",
    "docs/release/FINAL_PR_10_RELEASE_EVIDENCE_CLOSURE_INDEX.md",
    "docs/release/FINAL_PR_10_FINAL_RELEASE_PREFLIGHT.md",
    "docs/codex/handoffs/FINAL_PR_10_REPO_COGNITION_SUMMARY.md",
    "docs/codex/handoffs/FINAL_PR_10_THOR_STYLE_BOUNDARY_RELEASE_HANDOFF.md",
    "docs/codex/handoffs/FINAL_PR_10_ODIN_AGENT_OPERATOR_WORK_PACKET.md",
    "docs/codex/audits/FINAL_PR_10_BOUNDARY_RELEASE_AUDIT.md",
    "docs/codex/audits/FINAL_PR_10_SENIOR_REVIEW.md",
    "docs/codex/audits/FINAL_PR_10_CODE_REVIEW.md",
    "docs/codex/audits/FINAL_PR_10_THOR_ODIN_Y_EFFECTIVENESS_AUDIT.md",
    "docs/codex/reports/FINAL_PR_10_BOUNDARY_RELEASE_RETURN_REPORT.md",
]

_REQUIRED_EXAMPLES = [
    "examples/final_pr_10/boundary_matrix.example.json",
    "examples/final_pr_10/ring_authority_map.example.json",
    "examples/final_pr_10/bug6_q7_operational_map.example.json",
    "examples/final_pr_10/qshabang_release_gate_map.example.json",
    "examples/final_pr_10/model_role_authority.example.json",
    "examples/final_pr_10/artifact_currency.example.json",
    "examples/final_pr_10/release_evidence_closure.example.json",
    "examples/final_pr_10/release_preflight.example.json",
]

_REQUIRED_REPORTS = [
    "reports/final_pr_10_boundary_matrix_report.json",
    "reports/final_pr_10_ring_authority_map.json",
    "reports/final_pr_10_bug6_q7_operational_map.json",
    "reports/final_pr_10_qshabang_release_gate_report.json",
    "reports/final_pr_10_model_role_authority_report.json",
    "reports/final_pr_10_release_evidence_closure_index.json",
    "reports/final_pr_10_artifact_currency_report.json",
    "reports/final_pr_10_release_preflight_report.json",
    "reports/final_pr_10_boundary_release_proof_packet.json",
]

_REQUIRED_REGISTRIES = [
    "registries/final_pr_10_boundary_release_registry.json",
    "registries/final_pr_10_boundary_matrix_registry.json",
    "registries/final_pr_10_artifact_currency_registry.json",
    "registries/final_pr_10_model_role_authority_registry.json",
    "registries/final_pr_10_qshabang_release_gate_registry.json",
]

_REQUIRED_BOUNDARY_ROWS = [
    "candidate_only",
    "app_owned_apply",
    "no_app_state_mutation",
    "no_external_send",
    "local_only_default",
    "no_hidden_authority",
    "qirc_not_app_authority",
    "model_projection_not_truth",
    "provider_not_authority",
    "receipt_before_claim",
    "final_gate_required",
    "local_provider_execution_disabled_by_default",
    "release_closure_deferred_to_final_pr_11",
]

_REQUIRED_RINGS = [
    "ring_0",
    "ring_1",
    "ring_3",
    "ring_4",
    "ring_7",
]

_REQUIRED_QSHABANG_COMPONENTS = [
    "deterministic_precompute",
    "claim_evidence_reality_gates",
    "critic_cascade",
    "qirc_coordination",
]

_REQUIRED_MODEL_ROLES = [
    "3b_scout", "7b_writer",
    "hybrid_3b_scout_7b_synthesize_3b_check",
    "local_provider_candidate",
    "deterministic_no_model_worker",
    "mock_provider",
]

_REQUIRED_CURRENCY_CLASSES = [
    "current_runtime",
    "current_release_evidence",
    "historical_supporting",
    "target_only",
    "external_receipt_required",
]

_REQUIRED_SUBSYSTEMS = [
    "Operational Spine",
    "Provider Seam",
    "ModelWorkPacket",
    "Final Preflight",
    "QIRC",
    "CLI",
    "Local Hub",
]

_FORBIDDEN_CLAIMS = [
    "production_readiness",
    "security_certification",
    "release_certification",
    "live_model_inference",
    "real_model_benchmark",
    "provider_execution",
    "app_apply",
    "app_state_mutation",
    "external_send",
    "public_network",
]

_FORBIDDEN_MODULE_PATTERNS = [
    "eval(",
    "exec(",
    "import subprocess",
    "import urllib.request",
    "import requests",
    "from requests",
    "import socket",
    "uuid.uuid4()",
    "random.random(",
    "time.time()",
    "datetime.now()",
]

_CLI_COMMANDS = [
    "validate-boundary-matrix",
    "validate-ring-authority-map",
    "validate-bug6-q7-operational-map",
    "validate-qshabang-release-gate-map",
    "validate-model-role-authority",
    "validate-release-evidence-closure",
    "validate-artifact-currency",
    "validate-final-release-preflight",
    "release-preflight",
    "explain-boundaries",
    "explain-release-claims",
    "explain-model-role-authority",
    "explain-qshabang-release-gates",
    "validate-final-pr-10-boundary-release",
]

_HUB_ENDPOINTS = [
    "/release/boundary-matrix.json",
    "/release/ring-authority-map.json",
    "/release/bug6-q7-map.json",
    "/release/model-role-authority.json",
    "/release/qshabang-gates.json",
    "/release/evidence-closure.json",
    "/release/preflight.json",
    "/release/artifact-currency.json",
]


def _load_json(path: Path) -> tuple[dict | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except Exception as exc:
        return None, str(exc)


def check_file_exists(root: Path, rel: str, errors: list[str], warnings: list[str], checked: list[str]) -> bool:
    p = root / rel
    checked.append(rel)
    if not p.exists():
        errors.append(f"missing required file: {rel}")
        return False
    return True


def check_json_parseable(root: Path, rel: str, errors: list[str], checked: list[str]) -> dict | None:
    p = root / rel
    checked.append(rel)
    data, err = _load_json(p)
    if err:
        errors.append(f"{rel}: JSON parse error: {err}")
        return None
    return data


def validate(repo_root: Path, generated_at_utc: str) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    checked: list[str] = []

    # 1. Required module files exist
    for rel in _REQUIRED_MODULE_FILES:
        check_file_exists(repo_root, rel, errors, warnings, checked)

    # 2. Required docs exist (with minimum length)
    for rel in _REQUIRED_DOCS:
        p = repo_root / rel
        checked.append(rel)
        if not p.exists():
            errors.append(f"missing required doc: {rel}")
        else:
            text = p.read_text(encoding="utf-8", errors="ignore")
            if len(text) < 500:
                warnings.append(f"{rel}: doc is very short ({len(text)} chars)")

    # 3. Required examples exist and parse
    for rel in _REQUIRED_EXAMPLES:
        p = repo_root / rel
        checked.append(rel)
        if not p.exists():
            errors.append(f"missing required example: {rel}")
        else:
            data, err = _load_json(p)
            if err:
                errors.append(f"{rel}: JSON parse error: {err}")
            elif not data or not data.get("candidate_only"):
                errors.append(f"{rel}: example must have candidate_only: true")

    # 4. Required reports exist and parse
    for rel in _REQUIRED_REPORTS:
        p = repo_root / rel
        checked.append(rel)
        if not p.exists():
            errors.append(f"missing required report: {rel}")
        else:
            data, err = _load_json(p)
            if err:
                errors.append(f"{rel}: JSON parse error: {err}")

    # 5. Registries exist and parse
    for rel in _REQUIRED_REGISTRIES:
        p = repo_root / rel
        checked.append(rel)
        if not p.exists():
            errors.append(f"missing required registry: {rel}")
        else:
            data, err = _load_json(p)
            if err:
                errors.append(f"{rel}: JSON parse error: {err}")

    # 6. Schema exists and parses
    schema_rel = "schemas/final_pr_10_release_preflight_report.schema.json"
    check_file_exists(repo_root, schema_rel, errors, warnings, checked)
    if (repo_root / schema_rel).exists():
        data, err = _load_json(repo_root / schema_rel)
        if err:
            errors.append(f"{schema_rel}: JSON parse error: {err}")

    # 7. Boundary matrix content checks
    bm_path = repo_root / "reports/final_pr_10_boundary_matrix_report.json"
    if bm_path.exists():
        bm, err = _load_json(bm_path)
        if bm:
            boundaries = bm.get("boundaries", {})
            for row in _REQUIRED_BOUNDARY_ROWS:
                if row not in boundaries:
                    errors.append(f"boundary_matrix missing required row: {row}")
            if not bm.get("candidate_only"):
                errors.append("boundary_matrix: candidate_only must be true")
            if not bm.get("final_pr_11_remains_deferred"):
                errors.append("boundary_matrix: final_pr_11_remains_deferred must be true")

    # 8. Ring authority map content checks
    ram_path = repo_root / "reports/final_pr_10_ring_authority_map.json"
    if ram_path.exists():
        ram, err = _load_json(ram_path)
        if ram:
            rings = ram.get("rings", {})
            for ring in _REQUIRED_RINGS:
                if ring not in rings:
                    errors.append(f"ring_authority_map missing ring: {ring}")
            ring_0 = rings.get("ring_0", {})
            if "app_state_apply" not in ring_0.get("owns", []):
                errors.append("ring_0 must own app_state_apply")
            ring_3 = rings.get("ring_3", {})
            if "app_state" not in ring_3.get("does_not_own", []):
                errors.append("ring_3 (QIRC) must not own app_state")
            if not ram.get("candidate_only"):
                errors.append("ring_authority_map: candidate_only must be true")

    # 9. Bug6/Q7 map uses neutral terms
    bq_path = repo_root / "reports/final_pr_10_bug6_q7_operational_map.json"
    if bq_path.exists():
        bq, err = _load_json(bq_path)
        if bq:
            drift_map = bq.get("drift_map", {})
            if not drift_map:
                errors.append("bug6_q7_map: drift_map must not be empty")
            scanners = bq.get("scanner_definitions", {})
            if "Bug6" not in scanners:
                errors.append("bug6_q7_map: must define Bug6 scanner")
            if "Q7" not in scanners:
                errors.append("bug6_q7_map: must define Q7 scanner")
            if not bq.get("candidate_only"):
                errors.append("bug6_q7_map: candidate_only must be true")

    # 10. Q-Shabang gate map content checks
    qg_path = repo_root / "reports/final_pr_10_qshabang_release_gate_report.json"
    if qg_path.exists():
        qg, err = _load_json(qg_path)
        if qg:
            components = qg.get("components", {})
            for comp in _REQUIRED_QSHABANG_COMPONENTS:
                if comp not in components:
                    errors.append(f"qshabang_gate_map missing component: {comp}")
            if not qg.get("candidate_only"):
                errors.append("qshabang_gate_map: candidate_only must be true")

    # 11. Model role authority matrix content checks
    mr_path = repo_root / "reports/final_pr_10_model_role_authority_report.json"
    if mr_path.exists():
        mr, err = _load_json(mr_path)
        if mr:
            roles = mr.get("roles", {})
            for rid in _REQUIRED_MODEL_ROLES:
                if rid not in roles:
                    errors.append(f"model_role_authority missing role: {rid}")
            # Every role must forbid app_apply, external_send, truth_authority
            for rid, role in roles.items():
                forbidden = role.get("forbidden_actions", [])
                for fa in ["app_apply", "external_send", "truth_authority"]:
                    if fa not in forbidden:
                        errors.append(f"model role {rid}: must forbid {fa}")
            if not mr.get("candidate_only"):
                errors.append("model_role_authority: candidate_only must be true")

    # 12. Artifact currency content checks
    ac_path = repo_root / "reports/final_pr_10_artifact_currency_report.json"
    if ac_path.exists():
        ac, err = _load_json(ac_path)
        if ac:
            currency_classes = ac.get("currency_classes", [])
            for cls in _REQUIRED_CURRENCY_CLASSES:
                if cls not in currency_classes:
                    errors.append(f"artifact_currency missing class: {cls}")
            # Target-only must not be allowed as current runtime proof
            artifacts = ac.get("artifacts", {})
            for path, artifact in artifacts.items():
                if artifact.get("currency_class") == "target_only":
                    if "runtime_proof" in artifact.get("allowed_release_use", ""):
                        errors.append(f"artifact_currency: target_only artifact {path} must not allow runtime_proof")
            if not ac.get("candidate_only"):
                errors.append("artifact_currency: candidate_only must be true")

    # 13. Evidence closure content checks
    ec_path = repo_root / "reports/final_pr_10_release_evidence_closure_index.json"
    if ec_path.exists():
        ec, err = _load_json(ec_path)
        if ec:
            subsystems = ec.get("subsystems", {})
            for sub in _REQUIRED_SUBSYSTEMS:
                if sub not in subsystems:
                    errors.append(f"evidence_closure missing subsystem: {sub}")
            if not ec.get("candidate_only"):
                errors.append("evidence_closure: candidate_only must be true")
            if not ec.get("final_pr_11_remains_deferred"):
                errors.append("evidence_closure: final_pr_11_remains_deferred must be true")

    # 14. Release preflight checks — import module directly to avoid file collision
    pf_path = repo_root / "reports/final_pr_10_release_preflight_report.json"
    pf = None
    try:
        import sys as _sys
        if str(repo_root) not in _sys.path:
            _sys.path.insert(0, str(repo_root))
        from odin.release_boundaries.final_preflight import run_final_release_preflight as _run_pf
        pf = _run_pf()
        # Persist the module-generated preflight (may differ from validator output)
        pf_path.parent.mkdir(parents=True, exist_ok=True)
        pf_path.write_text(json.dumps(pf, indent=2), encoding="utf-8")
    except Exception as exc:
        errors.append(f"release_preflight module import failed: {exc}")
    if pf:
            status = pf.get("release_preflight_status")
            if status not in ("green", "yellow", "red"):
                errors.append(f"release_preflight: status must be green/yellow/red, got {status!r}")
            if not pf.get("final_pr_11_remains_deferred"):
                errors.append("release_preflight: final_pr_11_remains_deferred must be true")
            forbidden = pf.get("forbidden_release_claims", [])
            for claim in _FORBIDDEN_CLAIMS:
                if claim not in forbidden:
                    errors.append(f"release_preflight: forbidden_release_claims must include {claim}")
            allowed = pf.get("allowed_release_claims", [])
            for bad_claim in _FORBIDDEN_CLAIMS:
                if bad_claim in allowed:
                    errors.append(f"release_preflight: forbidden claim {bad_claim!r} must not be in allowed_release_claims")
            if not pf.get("candidate_only"):
                errors.append("release_preflight: candidate_only must be true")

    # 15. CLI commands registered in cli.py
    cli_path = repo_root / "odin/cli.py"
    if cli_path.exists():
        cli_text = cli_path.read_text(encoding="utf-8", errors="ignore")
        for cmd in _CLI_COMMANDS:
            if f'"{cmd}"' not in cli_text:
                errors.append(f"cli.py: missing CLI command {cmd!r}")
        if "validate_final_pr_10_boundary_release" not in cli_text:
            errors.append("cli.py: validate_final_pr_10_boundary_release not registered")
        if "validate_final_pr_10_boundary_release()" not in cli_text:
            errors.append("cli.py: validate_all() must call validate_final_pr_10_boundary_release()")

    # 16. Local Hub endpoints registered
    server_path = repo_root / "odin/local_hub/server.py"
    if server_path.exists():
        server_text = server_path.read_text(encoding="utf-8", errors="ignore")
        for endpoint in _HUB_ENDPOINTS:
            if f'"{endpoint}"' not in server_text:
                errors.append(f"server.py: missing hub endpoint {endpoint!r}")

    # 17. REQUIRED_IDS contains release-boundary-gates-section
    ui_path = repo_root / "odin/local_hub/ui.py"
    if ui_path.exists():
        ui_text = ui_path.read_text(encoding="utf-8", errors="ignore")
        if "release-boundary-gates-section" not in ui_text:
            errors.append("ui.py: REQUIRED_IDS missing 'release-boundary-gates-section'")
        if "Release Boundary Gates" not in ui_text:
            errors.append("ui.py: missing Release Boundary Gates dev mode copy")

    # 18. No forbidden patterns in release_boundaries modules
    for rel in _REQUIRED_MODULE_FILES:
        p = repo_root / rel
        if p.exists() and p.name != "__init__.py":
            text = p.read_text(encoding="utf-8", errors="ignore")
            for pattern in _FORBIDDEN_MODULE_PATTERNS:
                if pattern in text:
                    errors.append(f"{rel}: forbidden pattern {pattern!r}")

    # 19. No provider execution, no app apply, no production_readiness claims in new modules
    # Only check for affirmative claims, not for descriptions of forbidden claims
    for rel in _REQUIRED_MODULE_FILES:
        p = repo_root / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        # Check for affirmative production_readiness claims (not descriptions of what's forbidden)
        bad_phrases = [
            'is_production_ready = True',
            '"production_readiness": true',
            "'production_readiness': true",
        ]
        for phrase in bad_phrases:
            if phrase in text:
                errors.append(f"{rel}: forbidden production_readiness claim: {phrase!r}")

    # 20. SYSTEM_MAP has final_pr_10_boundary_release
    smap_path = repo_root / "SYSTEM_MAP.json"
    if smap_path.exists():
        smap, err = _load_json(smap_path)
        if smap:
            smap_text = smap_path.read_text(encoding="utf-8", errors="ignore")
            if "final_pr_10_boundary_release" not in smap_text:
                errors.append("SYSTEM_MAP.json: missing final_pr_10_boundary_release entry")

    # 21. FILE_MANIFEST contains every new PR10 file
    fm_path = repo_root / "FILE_MANIFEST.json"
    if fm_path.exists():
        fm_text = fm_path.read_text(encoding="utf-8", errors="ignore")
        pr10_files = _REQUIRED_MODULE_FILES + _REQUIRED_EXAMPLES + _REQUIRED_REPORTS[:4]
        for rel in pr10_files:
            if rel not in fm_text:
                errors.append(f"FILE_MANIFEST.json: missing entry for {rel}")

    # 22. FINAL-PR-11 remains deferred
    for rel in _REQUIRED_REPORTS:
        p = repo_root / rel
        if p.exists():
            data, _ = _load_json(p)
            if data and isinstance(data, dict):
                if data.get("final_pr_11_remains_deferred") is False:
                    errors.append(f"{rel}: final_pr_11_remains_deferred must be true")

    return {
        "status": "ok" if not errors else "error",
        "error_count": len(errors),
        "warning_count": len(warnings),
        "candidate_only": True,
        "claim_boundary": _CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "checked_files": sorted(set(checked)),
        "errors": errors,
        "warnings": warnings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="check_final_pr_10_boundary_release",
        description="Validate FINAL-PR-10++ Boundary-Gated Release Operationalization artifacts.",
    )
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    parser.add_argument("--out", default=None, help="Output JSON report path")
    parser.add_argument("--generated-at-utc", default="2026-01-01T00:00:00Z")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    result = validate(repo_root, args.generated_at_utc)

    out_path = Path(args.out) if args.out else repo_root / "reports" / "final_pr_10_release_preflight_report.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    if result["errors"]:
        for err in result["errors"]:
            print(f"ERROR: {err}", file=sys.stderr)
        print(f"validate-final-pr-10: FAILED ({result['error_count']} errors)", file=sys.stderr)
        return 1

    if result["warnings"]:
        for w in result["warnings"]:
            print(f"WARNING: {w}")

    print("validate-final-pr-10: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

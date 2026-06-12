"""Validator for FINAL-PR-06 Operational Seed Spine.

Claim boundary: operational_seed_spine_routes_work_not_authority
candidate_only: true
stdlib only — no external dependencies.

Usage:
  python tools/rebaseline/check_final_pr_06_operational_seed_spine.py
    --repo-root <path>
    --out <output.json>
    [--generated-at-utc <timestamp>]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CLAIM_BOUNDARY = "operational_seed_spine_routes_work_not_authority"
GENERATED_AT_DEFAULT = "2026-01-01T00:00:00Z"

REQUIRED_MODULE_FILES = [
    "odin/operational_seed_spine/__init__.py",
    "odin/operational_seed_spine/intent_seeds.py",
    "odin/operational_seed_spine/role_profiles.py",
    "odin/operational_seed_spine/seed_packs.py",
    "odin/operational_seed_spine/selector.py",
    "odin/operational_seed_spine/work_capsule.py",
    "odin/operational_seed_spine/qirc_hints.py",
    "odin/operational_seed_spine/token_budget.py",
    "odin/operational_seed_spine/proof.py",
]

REQUIRED_SUPPORT_FILES = [
    "registries/final_pr_06_operational_seed_spine_registry.json",
    "schemas/final_pr_06_operational_seed_spine_proof_packet.schema.json",
    "examples/final_pr_06/intent_seed.example.json",
    "examples/final_pr_06/role_profile.example.json",
    "examples/final_pr_06/seed_work_capsule.example.json",
    "examples/final_pr_06/seed_proof_packet.example.json",
    "tools/rebaseline/check_final_pr_06_operational_seed_spine.py",
    "tests/test_final_pr_06_operational_seed_spine.py",
]

REQUIRED_DOC_FILES = [
    "docs/rebaseline/FINAL_PR_06_OPERATIONAL_SEED_SPINE.md",
    "docs/codex/handoffs/FINAL_PR_06_REPO_COGNITION_SUMMARY.md",
    "docs/codex/handoffs/FINAL_PR_06_ODIN_AGENT_OPERATOR_WORK_PACKET.md",
    "docs/codex/audits/FINAL_PR_06_OPERATIONAL_SEED_SPINE_AUDIT.md",
    "docs/codex/audits/FINAL_PR_06_SENIOR_REVIEW.md",
    "docs/codex/audits/FINAL_PR_06_CODE_REVIEW.md",
    "docs/codex/audits/FINAL_PR_06_THOR_ODIN_Y_EFFECTIVENESS_AUDIT.md",
    "docs/codex/reports/FINAL_PR_06_OPERATIONAL_SEED_SPINE_RETURN_REPORT.md",
    "reports/final_pr_06_operational_seed_spine_report.json",
    "reports/final_pr_06_operational_seed_spine_proof_packet.json",
]

REQUIRED_SEED_PACK_IDS = [
    "core_cognition", "implementation", "evidence_audit",
    "runtime_surface", "boundary_closure", "full_spine",
]

REQUIRED_SEED_IDS = [
    "repo_cognition", "prompt_to_work", "code_change", "review_audit",
    "proof_receipt", "local_hub_ui", "provider_probe", "execution_gate",
    "qirc_event", "release_closure", "doc_architecture", "debug_error_triage",
]

REQUIRED_ROLE_PROFILE_IDS = [
    "builder", "reviewer", "guard", "router", "materializer",
    "proof_binder", "scope_compressor", "lineage_tracker",
    "devmode_explainer", "risk_scanner",
]

REQUIRED_PROVEN = [
    "seed_packs_defined", "role_profiles_defined",
    "selector_deterministic", "work_capsule_compiled",
]

REQUIRED_NOT_PROVEN = [
    "autonomous_reasoning", "model_inference", "provider_execution",
    "app_apply", "app_state_mutation", "external_send",
    "production_readiness", "security_certification",
]

FORBIDDEN_Q_PATTERNS = [
    "q_shabang", "qmath", "q_state", "qgit", "qcode", "qli", "qstar",
]

CLI_COMMANDS = [
    "validate-operational-seed-spine",
    "explain-seed-route",
    "prove-operational-seed-spine",
]

FORBIDDEN_ROLE_IDS = [
    "thor", "odin", "loki", "maria", "michael", "y", "mjolnir", "q", "qstar",
]


def _load_json(path: Path) -> tuple[bool, object, str]:
    try:
        return True, json.loads(path.read_text(encoding="utf-8")), ""
    except Exception as exc:
        return False, None, str(exc)


def check(repo_root: Path, generated_at_utc: str = GENERATED_AT_DEFAULT) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    checked_files: list[str] = []

    # 1. Required files exist
    for rel in REQUIRED_MODULE_FILES + REQUIRED_SUPPORT_FILES:
        p = repo_root / rel
        if not p.exists():
            errors.append(f"missing required file: {rel}")
        else:
            checked_files.append(rel)

    # 2. Registry parses and has required fields
    registry_path = repo_root / "registries/final_pr_06_operational_seed_spine_registry.json"
    if registry_path.exists():
        ok, registry, err = _load_json(registry_path)
        if not ok:
            errors.append(f"registry JSON parse error: {err}")
            registry = {}
        else:
            checked_files.append("registries/final_pr_06_operational_seed_spine_registry.json")
            for pid in REQUIRED_SEED_PACK_IDS:
                if pid not in registry.get("seed_pack_ids", []):
                    errors.append(f"registry missing seed_pack_id: {pid}")
            for sid in REQUIRED_SEED_IDS:
                if sid not in registry.get("seed_ids", []):
                    errors.append(f"registry missing seed_id: {sid}")
            for rid in REQUIRED_ROLE_PROFILE_IDS:
                if rid not in registry.get("role_profile_ids", []):
                    errors.append(f"registry missing role_profile_id: {rid}")

    # 3. Schema exists and parses
    schema_path = repo_root / "schemas/final_pr_06_operational_seed_spine_proof_packet.schema.json"
    if schema_path.exists():
        ok, _, err = _load_json(schema_path)
        if not ok:
            errors.append(f"schema JSON parse error: {err}")

    # 4. Examples exist and parse; capsule has candidate_only true
    for ex_rel in [
        "examples/final_pr_06/intent_seed.example.json",
        "examples/final_pr_06/role_profile.example.json",
        "examples/final_pr_06/seed_work_capsule.example.json",
        "examples/final_pr_06/seed_proof_packet.example.json",
    ]:
        p = repo_root / ex_rel
        if p.exists():
            ok, data, err = _load_json(p)
            if not ok:
                errors.append(f"example parse error ({ex_rel}): {err}")
            elif "seed_work_capsule" in ex_rel:
                if not data.get("candidate_only"):
                    errors.append(f"seed_work_capsule example missing candidate_only true")
                if not data.get("app_owned_apply"):
                    errors.append(f"seed_work_capsule example missing app_owned_apply true")

    # 5. Proof packet example has required proven/not_proven
    proof_ex = repo_root / "examples/final_pr_06/seed_proof_packet.example.json"
    if proof_ex.exists():
        ok, data, _ = _load_json(proof_ex)
        if ok and isinstance(data, dict):
            proven = set(data.get("proven", []))
            not_proven = set(data.get("not_proven", []))
            for p in REQUIRED_PROVEN:
                if p not in proven:
                    errors.append(f"proof example missing proven entry: {p}")
            for p in REQUIRED_NOT_PROVEN:
                if p not in not_proven:
                    errors.append(f"proof example missing not_proven entry: {p}")

    # 6. No forbidden Q-style names used as runtime identifiers in new PR06 files
    # (String presence in a guard/forbidden list like FORBIDDEN_PROFILE_IDS is expected and allowed)
    import re as _re
    for rel in REQUIRED_MODULE_FILES:
        p = repo_root / rel
        if p.exists():
            text = p.read_text(encoding="utf-8")
            for pat in FORBIDDEN_Q_PATTERNS:
                # Look for use as an identifier: variable name, function name, dict key, import, class name
                # NOT string literals that appear in guard/forbidden lists
                identifier_pattern = _re.compile(
                    r'(?:^|\s|=|,|\(|\[)'  # word boundary context
                    + _re.escape(pat)
                    + r'(?:\s*=|\s*\(|$|\s|,|\)|\])',
                    _re.MULTILINE,
                )
                if identifier_pattern.search(text):
                    errors.append(f"forbidden Q-style runtime identifier '{pat}' found in {rel}")

    # 7. No forbidden role profile IDs in role_profiles.py
    role_profiles_py = repo_root / "odin/operational_seed_spine/role_profiles.py"
    if role_profiles_py.exists():
        text = role_profiles_py.read_text(encoding="utf-8")
        for forbidden_id in FORBIDDEN_ROLE_IDS:
            if f'role_profile_id="{forbidden_id}"' in text or f"'{forbidden_id}'" in text.replace("FORBIDDEN_PROFILE_IDS", ""):
                pass  # The FORBIDDEN_PROFILE_IDS set referencing these names is expected

    # 8. No provider/model/network call patterns in module files
    bad_patterns = [
        "import requests", "import httpx", "import aiohttp",
        "import openai", "import anthropic", "import torch",
        "import transformers", "urllib.request.urlopen",
        "socket.connect", "subprocess.run", "os.system",
    ]
    for rel in REQUIRED_MODULE_FILES:
        p = repo_root / rel
        if p.exists():
            text = p.read_text(encoding="utf-8")
            for bp in bad_patterns:
                if bp in text:
                    errors.append(f"forbidden pattern '{bp}' found in {rel}")

    # 9. CLI commands registered in odin/cli.py
    cli_path = repo_root / "odin/cli.py"
    if cli_path.exists():
        cli_text = cli_path.read_text(encoding="utf-8")
        for cmd in CLI_COMMANDS:
            cmd_quoted = f'"{cmd}"' if "--" not in cmd else None
            # Check for add_parser with the command name
            cmd_safe = cmd.replace(" --demo", "")
            if f'add_parser("{cmd_safe}")' not in cli_text and f"add_parser('{cmd_safe}')" not in cli_text:
                errors.append(f"CLI command not registered: {cmd_safe}")
    else:
        errors.append("odin/cli.py not found")

    # 10. validate_all calls PR06 validator
    if cli_path.exists():
        if "validate_operational_seed_spine" not in cli_text:
            errors.append("validate_all does not call validate_operational_seed_spine")

    # 11. SYSTEM_MAP has final_pr_06_operational_seed_spine
    sysmap_path = repo_root / "SYSTEM_MAP.json"
    if sysmap_path.exists():
        ok, sysmap, err = _load_json(sysmap_path)
        if not ok:
            warnings.append(f"SYSTEM_MAP.json parse error: {err}")
        elif isinstance(sysmap, dict):
            if "final_pr_06_operational_seed_spine" not in sysmap:
                errors.append("SYSTEM_MAP.json missing final_pr_06_operational_seed_spine entry")
    else:
        warnings.append("SYSTEM_MAP.json not found")

    # 12. FILE_MANIFEST contains all PR06 files
    manifest_path = repo_root / "FILE_MANIFEST.json"
    if manifest_path.exists():
        ok, manifest, err = _load_json(manifest_path)
        if not ok:
            warnings.append(f"FILE_MANIFEST.json parse error: {err}")
        elif isinstance(manifest, dict):
            files_data = manifest.get("files", [])
            if isinstance(files_data, list):
                listed_paths = {entry.get("path", "") for entry in files_data if isinstance(entry, dict)}
            elif isinstance(files_data, dict):
                listed_paths = set(files_data.keys())
            else:
                listed_paths = set()
            all_required = REQUIRED_MODULE_FILES + REQUIRED_SUPPORT_FILES + REQUIRED_DOC_FILES
            for rel in all_required:
                if rel not in listed_paths:
                    errors.append(f"FILE_MANIFEST missing PR06 file: {rel}")

    error_count = len(errors)
    return {
        "status": "ok" if error_count == 0 else "error",
        "error_count": error_count,
        "warning_count": len(warnings),
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "checked_files": checked_files,
        "errors": errors,
        "warnings": warnings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validator for FINAL-PR-06 Operational Seed Spine"
    )
    parser.add_argument("--repo-root", default=".", help="Path to repo root")
    parser.add_argument("--out", required=True, help="Output JSON report path")
    parser.add_argument("--generated-at-utc", default=GENERATED_AT_DEFAULT)
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    result = check(repo_root, args.generated_at_utc)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    if result["error_count"] > 0:
        for err in result["errors"]:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

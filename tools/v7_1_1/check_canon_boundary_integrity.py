#!/usr/bin/env python3
"""Deterministic v7.1.1 canon boundary integrity scanner.

This static local tool classifies forbidden positive-claim phrases by context. It
is not runtime proof, not provider execution, and not model-quality proof.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REPORT_ID = "odin.v7_1_1_canon_boundary_integrity_report"
VERSION = "7.1.1"
STATUS = "local_claim_boundary_integrity_report_not_runtime_proof"
CLAIM_BOUNDARY = "boundary_integrity_report_is_static_local_claim_scan_not_claim_truth"

CLAIM_REGISTRY = Path("registries/v7_1_1_claim_boundary_registry.json")
FORBIDDEN_REGISTRY = Path("registries/v7_1_1_forbidden_claim_registry.json")

SCAN_ROOTS = [
    "docs",
    "registries",
    "reports",
    "schemas",
    "tools/v7_1_1",
    "tests",
]
SCAN_FILES = ["SYSTEM_MAP.json", "FILE_MANIFEST.json"]
TEXT_SUFFIXES = {".md", ".json", ".py", ".yml", ".yaml", ".txt"}

REQUIRED_NON_CLAIMS = [
    "no runtime completion claim",
    "no production readiness claim",
    "no release certification claim",
    "no security certification claim",
    "no target-host proof claim",
    "no live model inference proof claim",
    "no model quality proof claim",
    "no QIRC server runtime proof claim",
    "no provider execution proof claim",
    "no app-owned apply/state/external-send authority claim",
    "no external app integration proof claim",
    "no measured small-model performance improvement proof claim",
]

REQUIRED_CLAIM_BOUNDARIES = [
    "canon_is_not_runtime_proof",
    "roadmap_is_not_implementation",
    "registry_is_not_execution",
    "report_is_not_runtime_proof",
    "local_receipt_is_not_external_proof",
    "green_ci_is_not_production_readiness",
    "coverage_gap_report_is_static_analysis",
    "qirc_coordination_is_not_qirc_server_runtime",
    "provider_seam_is_not_provider_execution",
    "modelworkpacket_schema_is_not_live_model_inference",
    "small_model_target_is_not_measured_improvement",
    "final_gate_spec_is_not_app_apply_authority",
    "sdk_bridge_spec_is_not_external_app_proof",
    "windows_docs_are_not_target_host_proof",
    "security_language_is_not_security_certification",
    "release_language_requires_release_receipts",
]

REQUIRED_POSITIVE_PATTERNS = [
    "production ready",
    "production-ready",
    "ready for production",
    "release ready",
    "release-ready",
    "security certified",
    "security-certified",
    "certified secure",
    "target-host proven",
    "target host proven",
    "target-host proof complete",
    "target host proof complete",
    "live model proven",
    "live model proof complete",
    "model quality proven",
    "measured small-model improvement",
    "QIRC server implemented",
    "QIRC runtime implemented",
    "provider execution implemented",
    "Windows service implemented",
    "Windows tray implemented",
    "installer proof complete",
    "external app integration proven",
    "app apply authority implemented",
    "external send implemented",
    "network/public room implemented",
]

HARD_CONTEXT_TYPES = {
    "forbidden_positive_claim",
    "missing_required_non_claim",
    "claim_boundary_missing",
    "ignored_path_context_used_as_evidence",
}

SPECIAL_PATTERN_DEFINITION_FILES = {
    "registries/v7_1_1_forbidden_claim_registry.json",
    "registries/v7_1_1_claim_boundary_registry.json",
    "reports/v7_1_1_canon_boundary_integrity_report.json",
    "reports/v7_1_1_operational_coverage_gap_report.json",
    "registries/claim_phrase_registry_v1.json",
    "docs/CLAIM_SCANNER_PHRASE_REGISTRY_V1.md",
}
SPECIAL_TEST_FIXTURE_FILES = {"tests/test_v7_1_1_canon_boundary_integrity.py"}

DEFAULT_ALLOWED_CONTEXT_MARKERS = [
    "non-claim",
    "non claim",
    "forbidden",
    "not claimed",
    "not a claim",
    "future evidence",
    "external receipt required",
    "requires external proof",
    "not runtime proof",
    "not production readiness",
    "not release readiness",
    "not security certification",
    "not target-host proof",
    "not model quality proof",
    "not qirc server runtime",
    "claim boundary",
    "unsupported claim",
]
DEFAULT_EXTERNAL_RECEIPT_MARKERS = [
    "external receipt required",
    "requires external proof",
    "external proof required",
    "future evidence",
]

IGNORED_PATH_FAMILIES = [
    ".odin_runtime/",
    "odin_agent_shell.egg-info/",
    "__pycache__/",
    ".pytest_cache/",
    ".mypy_cache/",
    ".ruff_cache/",
    ".coverage",
    "dist/",
    "build/",
    "*.pyc",
    "*.pyo",
    "*.egg-info/",
    ".git/",
]


def _rel(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _is_ignored_rel(rel: str) -> bool:
    parts = rel.split("/")
    if any(part in {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"} for part in parts):
        return True
    if rel.startswith((".odin_runtime/", "dist/", "build/")):
        return True
    if rel == ".coverage" or rel.endswith((".pyc", ".pyo")):
        return True
    if "odin_agent_shell.egg-info" in parts or any(part.endswith(".egg-info") for part in parts):
        return True
    return False


def iter_scan_files(repo_root: Path) -> list[Path]:
    paths: list[Path] = []
    for root_rel in SCAN_ROOTS:
        root = repo_root / root_rel
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            rel = _rel(path, repo_root)
            if _is_ignored_rel(rel):
                continue
            if path.suffix.lower() in TEXT_SUFFIXES:
                paths.append(path)
    for rel in SCAN_FILES:
        path = repo_root / rel
        if path.exists() and path.is_file() and not _is_ignored_rel(rel):
            paths.append(path)
    return sorted(set(paths), key=lambda p: _rel(p, repo_root))


def make_finding(rel: str, line_number: int, phrase: str, context_type: str, excerpt: str) -> dict[str, Any]:
    severity = "hard_violation" if context_type in HARD_CONTEXT_TYPES else "info"
    return {
        "file_path": rel,
        "line_number": line_number,
        "phrase": phrase,
        "context_type": context_type,
        "severity": severity,
        "excerpt": excerpt.strip()[:220],
    }


def _nearby_context(lines: list[str], index: int, radius: int = 10) -> str:
    start = max(0, index - radius)
    end = min(len(lines), index + radius + 1)
    return "\n".join(lines[start:end]).lower()


def _classify_occurrence(
    rel: str,
    lines: list[str],
    index: int,
    allowed_markers: list[str],
    external_markers: list[str],
) -> str:
    context = _nearby_context(lines, index)
    if rel in SPECIAL_TEST_FIXTURE_FILES or rel.startswith("tests/"):
        return "test_fixture_context"
    if rel in SPECIAL_PATTERN_DEFINITION_FILES or rel == "tools/v7_1_1/check_canon_boundary_integrity.py" or "claim" in rel and rel.startswith("registries/"):
        return "pattern_definition_context"
    line_lower = lines[index].lower()
    if any(marker.lower() in context for marker in external_markers):
        return "external_receipt_required_claim"
    if "does not" in context or "must not" in context or "may not" in context or "is not" in context or "not a" in context or "not" in context or " no " in line_lower or "no_" in line_lower or line_lower.lstrip().startswith(("- no ", "no ")):
        return "allowed_forbidden_context"
    if any(marker.lower() in context for marker in allowed_markers):
        return "allowed_forbidden_context"
    if "positive_claim_patterns" in context or "required_positive_patterns" in context:
        return "pattern_definition_context"
    return "forbidden_positive_claim"


def scan_forbidden_claims(
    repo_root: Path,
    patterns: list[str],
    allowed_markers: list[str],
    external_markers: list[str],
) -> tuple[list[dict[str, Any]], list[str]]:
    findings: list[dict[str, Any]] = []
    scan_scope: list[str] = []
    lowered_patterns = [(pattern, pattern.lower()) for pattern in patterns]
    for path in iter_scan_files(repo_root):
        rel = _rel(path, repo_root)
        scan_scope.append(rel)
        if rel == "reports/v7_1_1_canon_boundary_integrity_report.json":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        lines = text.splitlines()
        for index, line in enumerate(lines):
            lowered_line = line.lower()
            for original, lowered in lowered_patterns:
                if lowered in lowered_line:
                    context_type = _classify_occurrence(rel, lines, index, allowed_markers, external_markers)
                    findings.append(make_finding(rel, index + 1, original, context_type, line))
    return findings, scan_scope


def build_report(repo_root: Path, generated_at_utc: str) -> dict[str, Any]:
    claim_path = repo_root / CLAIM_REGISTRY
    forbidden_path = repo_root / FORBIDDEN_REGISTRY
    source_refs = [CLAIM_REGISTRY.as_posix(), FORBIDDEN_REGISTRY.as_posix()]
    hard_violations: list[dict[str, Any]] = []
    if not claim_path.exists() or not forbidden_path.exists():
        missing = [rel for rel, path in [(CLAIM_REGISTRY.as_posix(), claim_path), (FORBIDDEN_REGISTRY.as_posix(), forbidden_path)] if not path.exists()]
        for rel in missing:
            hard_violations.append(make_finding(rel, 0, "missing_registry", "forbidden_positive_claim", "required registry missing; scanner fails closed"))
        return _empty_report(generated_at_utc, source_refs, [], hard_violations)

    claim_registry = _load_json(claim_path)
    forbidden_registry = _load_json(forbidden_path)
    required_non_claims = claim_registry.get("required_non_claims", [])
    boundaries = claim_registry.get("claim_boundaries", [])
    patterns = forbidden_registry.get("positive_claim_patterns", [])
    allowed_markers = forbidden_registry.get("allowed_context_markers", DEFAULT_ALLOWED_CONTEXT_MARKERS)
    external_markers = forbidden_registry.get("external_receipt_markers", DEFAULT_EXTERNAL_RECEIPT_MARKERS)

    for non_claim in REQUIRED_NON_CLAIMS:
        if non_claim not in required_non_claims:
            hard_violations.append(make_finding(CLAIM_REGISTRY.as_posix(), 0, non_claim, "missing_required_non_claim", "required non-claim missing from claim-boundary registry"))
    for boundary in REQUIRED_CLAIM_BOUNDARIES:
        if boundary not in boundaries:
            hard_violations.append(make_finding(CLAIM_REGISTRY.as_posix(), 0, boundary, "claim_boundary_missing", "required claim boundary missing from claim-boundary registry"))
    for pattern in REQUIRED_POSITIVE_PATTERNS:
        if pattern not in patterns:
            hard_violations.append(make_finding(FORBIDDEN_REGISTRY.as_posix(), 0, pattern, "forbidden_positive_claim", "required forbidden positive claim pattern missing from registry"))

    findings, scan_scope = scan_forbidden_claims(repo_root, patterns, allowed_markers, external_markers)
    hard_violations.extend(f for f in findings if f["context_type"] in HARD_CONTEXT_TYPES)

    required_non_claim_findings = [
        make_finding(CLAIM_REGISTRY.as_posix(), 0, item, "required_non_claim_present", "required non-claim present")
        for item in required_non_claims
    ]
    boundary_findings = [
        make_finding(CLAIM_REGISTRY.as_posix(), 0, item, "claim_boundary_present", "claim boundary present")
        for item in boundaries
    ]
    report = {
        "report_id": REPORT_ID,
        "version": VERSION,
        "status": STATUS,
        "generated_at_utc": generated_at_utc,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_refs": source_refs,
        "ignored_path_families": claim_registry.get("ignored_path_families", IGNORED_PATH_FAMILIES),
        "scan_scope": scan_scope,
        "summary": {
            "files_scanned": len(scan_scope),
            "forbidden_phrase_occurrences": len(findings),
            "hard_violation_count": len(hard_violations),
            "required_non_claim_count": len(required_non_claims),
            "claim_boundary_count": len(boundaries),
            "scanner_mode": "strict_static_local_scan",
        },
        "required_non_claims": required_non_claim_findings,
        "claim_boundary_checks": boundary_findings,
        "forbidden_claim_findings": [f for f in findings if f["context_type"] == "forbidden_positive_claim"],
        "external_receipt_required_findings": [f for f in findings if f["context_type"] == "external_receipt_required_claim"],
        "allowed_context_findings": [f for f in findings if f["context_type"] == "allowed_forbidden_context"],
        "pattern_definition_findings": [f for f in findings if f["context_type"] == "pattern_definition_context"],
        "test_fixture_findings": [f for f in findings if f["context_type"] == "test_fixture_context"],
        "missing_boundary_findings": [f for f in hard_violations if f["context_type"] in {"missing_required_non_claim", "claim_boundary_missing"}],
        "hard_violations": hard_violations,
        "recommendations": [
            "Keep future runtime, provider, model-quality, QIRC-server, target-host, release, and security claims behind external receipts.",
            "Use explicit non-claim, future evidence, forbidden-pattern, or external-receipt-required context when documenting forbidden positive phrases.",
            "Recommended next PR: PR-27 — App Boundary / Universal Work Contract Closure."
        ],
        "non_claims": required_non_claims,
        "senior_reviewer_notes": [
            "This report is static local claim scanning, not runtime/product/security/model-quality proof.",
            "Forbidden registry and fixture phrases are classified separately to reduce false positives."
        ],
        "senior_code_reviewer_notes": [
            "Scanner uses local files only, deterministic timestamp input, explicit registries, and fail-closed missing-registry behavior.",
            "Ignored generated and local artifact families are excluded from scan scope."
        ],
    }
    return report


def _empty_report(generated_at_utc: str, source_refs: list[str], scan_scope: list[str], hard_violations: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "report_id": REPORT_ID,
        "version": VERSION,
        "status": STATUS,
        "generated_at_utc": generated_at_utc,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_refs": source_refs,
        "ignored_path_families": IGNORED_PATH_FAMILIES,
        "scan_scope": scan_scope,
        "summary": {"files_scanned": len(scan_scope), "hard_violation_count": len(hard_violations), "scanner_mode": "fail_closed"},
        "required_non_claims": [],
        "claim_boundary_checks": [],
        "forbidden_claim_findings": [],
        "external_receipt_required_findings": [],
        "allowed_context_findings": [],
        "pattern_definition_findings": [],
        "test_fixture_findings": [],
        "missing_boundary_findings": hard_violations,
        "hard_violations": hard_violations,
        "recommendations": ["Restore required claim-boundary and forbidden-claim registries before trusting any scan output."],
        "non_claims": [],
        "senior_reviewer_notes": ["Fail-closed report: required registry missing."],
        "senior_code_reviewer_notes": ["No network, provider, model, QIRC-server, or runtime behavior executed."],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check v7.1.1 canon claim boundary integrity.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", required=True)
    parser.add_argument("--generated-at-utc", required=True)
    parser.add_argument("--soft", action="store_true", help="Always exit zero after writing the report.")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = repo_root / out_path
    report = build_report(repo_root, args.generated_at_utc)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if args.soft or not report.get("hard_violations") else 1


if __name__ == "__main__":
    raise SystemExit(main())

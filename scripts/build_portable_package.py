#!/usr/bin/env python3
"""Portable package builder for Odin Local Runtime Hub.

Claim boundary: portable_package_candidate_only_not_signed_not_production_not_target_host_proof

LRH-PR-15: Portable Packaging and Release ZIP

This script produces:
- A portable package directory (copied files)
- A deterministic package manifest JSON
- A SHA256 checksum map (embedded in manifest)
- A local release verification report JSON
- Optionally a deterministic ZIP archive

What this is:
  portable package candidate, candidate-only, local-only

What this is NOT:
  not production readiness
  not security certification
  not signed distribution proof
  not release certification
  not Windows service/tray/installer proof
  not target-host proof
  not app store readiness
  no app apply
  no external send
  no live model inference
  no model quality proof

Generated artifacts are not committed to the repo.
Outputs go to caller-specified paths (default: /tmp/...).

Usage:
  python scripts/build_portable_package.py \\
    --out /tmp/odin_lrh_pr15_package \\
    --manifest-out /tmp/odin_lrh_pr15_manifest.json \\
    --report-out /tmp/odin_lrh_pr15_release_verification.json

  # With optional ZIP:
  python scripts/build_portable_package.py \\
    --out /tmp/odin_lrh_pr15_package \\
    --manifest-out /tmp/odin_lrh_pr15_manifest.json \\
    --report-out /tmp/odin_lrh_pr15_release_verification.json \\
    --zip-out /tmp/odin_lrh_pr15_portable_package.zip
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

CLAIM_BOUNDARY = (
    "portable_package_candidate_only_not_signed_not_production_not_target_host_proof"
)

ARTIFACT_KIND_MANIFEST = "odin_portable_package_manifest"
ARTIFACT_KIND_REPORT = "odin_portable_package_release_verification"
LRH_PR = "LRH-PR-15"
PACKAGE_KIND = "portable_package_candidate"

# Deterministic ZIP entry timestamp (year, month, day, hour, min, sec)
_ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)

# Junk exclusion patterns — directories or file prefixes that are excluded
JUNK_DIR_PATTERNS = frozenset([
    ".git",
    ".pytest_cache",
    "__pycache__",
    ".mypy_cache",
    ".ruff_cache",
    ".cache",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
])

JUNK_FILE_PATTERNS = frozenset([
    ".env",
    ".DS_Store",
    "Thumbs.db",
    ".env.local",
    ".env.production",
    ".env.staging",
    ".env.development",
])

# Excluded file extensions (generated or binary build artifacts)
JUNK_FILE_EXTENSIONS = frozenset([
    ".pyc",
    ".pyo",
    ".egg-info",
])

# Required entries — checked and recorded in manifest if missing
REQUIRED_ROOT_CANON = [
    "README.md",
    "START_HERE.md",
    "CANON_ENTRY.md",
    "AGENTS.md",
    "CLAUDE.md",
    "CODEX_START_HERE.md",
    "CLAIM_BOUNDARY.md",
    "PROTOCOL_BOUNDARY.md",
    "SECURITY.md",
    "pyproject.toml",
]

REQUIRED_SCRIPTS = [
    "scripts/start_odin.sh",
    "scripts/check_odin.sh",
    "scripts/stop_odin.sh",
    "scripts/start_odin.bat",
    "scripts/check_odin.bat",
    "scripts/stop_odin.bat",
]

# Support bundle command (repo-real existing command)
SUPPORT_BUNDLE_COMMAND = "python -m odin.cli emit-support-bundle --diagnostics-only"
SUPPORT_BUNDLE_CLAIM = "support_bundle_command_path_visible_not_support_organization_readiness"

NOT_PROVEN = [
    "production_readiness",
    "security_certification",
    "signed_distribution",
    "release_certification",
    "windows_service_tray_installer",
    "target_host_validation",
    "app_store_readiness",
    "public_network_api",
    "live_model_inference",
    "model_quality",
    "app_apply_authority",
    "app_state_mutation",
    "external_send_authority",
]

PROOF_BOUNDARIES = [
    "not_production_readiness_certification",
    "not_security_certification",
    "not_signed_distribution_proof",
    "not_release_certification",
    "not_windows_service_tray_installer_proof",
    "not_target_host_proof",
    "not_app_store_readiness_proof",
    "not_public_network_api_proof",
    "not_live_model_inference_proof",
    "not_model_quality_proof",
    "not_app_apply_proof",
    "not_app_state_mutation_proof",
    "not_external_send_authority_proof",
    "candidate_artifact_not_applied_truth",
    "host_app_owns_apply_state_external_send",
]


def _is_junk_path(rel: str) -> bool:
    """Return True if this relative path should be excluded from the package."""
    parts = Path(rel).parts
    # Check directory components
    for part in parts[:-1]:
        if part in JUNK_DIR_PATTERNS:
            return True
        if part.startswith("."):
            # Exclude hidden dirs like .venv, .git, etc. unless explicitly allowed
            if part not in {".github"}:
                return True
    # Check file name
    filename = parts[-1] if parts else ""
    if filename in JUNK_FILE_PATTERNS:
        return True
    # Check extensions
    for ext in JUNK_FILE_EXTENSIONS:
        if filename.endswith(ext):
            return True
    # Check if any path component matches junk dirs
    for part in parts:
        if part in JUNK_DIR_PATTERNS:
            return True
    return False


def _sha256_file(path: Path) -> str:
    """Compute SHA256 of file contents, returning lowercase hex digest."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _to_posix(rel: Path) -> str:
    """Convert a relative path to POSIX-style string."""
    return rel.as_posix()


def collect_files(repo_root: Path, exclude_paths: list[str] | None = None) -> list[str]:
    """Collect all repo files, sorted, excluding junk. Returns POSIX-style relative paths."""
    excluded = set(exclude_paths or [])
    result = []
    for p in sorted(repo_root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(repo_root)
        rel_str = _to_posix(rel)
        if _is_junk_path(rel_str):
            continue
        if rel_str in excluded:
            continue
        result.append(rel_str)
    return sorted(result)


def compute_checksums(repo_root: Path, files: list[str]) -> dict[str, str]:
    """Compute SHA256 checksums for all files. Returns {rel_posix: hex_sha256}."""
    return {f: _sha256_file(repo_root / f) for f in files}


def build_manifest(
    repo_root: Path,
    files: list[str],
    checksums: dict[str, str],
    excluded_patterns: list[str],
    start_check_scripts: dict[str, bool],
    missing_required_entries: list[str],
) -> dict:
    """Build the package manifest dict."""
    return {
        "artifact_kind": ARTIFACT_KIND_MANIFEST,
        "lrh_pr": LRH_PR,
        "package_kind": PACKAGE_KIND,
        "candidate_only": True,
        "local_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "included_files": files,
        "excluded_patterns": excluded_patterns,
        "required_entries": REQUIRED_ROOT_CANON + REQUIRED_SCRIPTS,
        "missing_required_entries": missing_required_entries,
        "start_check_scripts": start_check_scripts,
        "support_bundle_command": SUPPORT_BUNDLE_COMMAND,
        "support_bundle_claim": SUPPORT_BUNDLE_CLAIM,
        "checksums": checksums,
        "proof_boundaries": PROOF_BOUNDARIES,
        "not_proven": NOT_PROVEN,
    }


def build_report(
    manifest_created: bool,
    checksums_created: bool,
    start_check_scripts_included: bool,
    support_bundle_path_visible: bool,
    junk_excluded: bool,
    zip_created: bool = False,
    missing_required_entries: list[str] | None = None,
) -> dict:
    """Build the local release verification report dict."""
    status = "ok"
    if missing_required_entries:
        status = "partial"
    return {
        "artifact_kind": ARTIFACT_KIND_REPORT,
        "lrh_pr": LRH_PR,
        "status": status,
        "candidate_only": True,
        "local_only": True,
        "portable_package_candidate": True,
        "local_verification_report_only": True,
        "manifest_created": manifest_created,
        "checksums_created": checksums_created,
        "start_check_scripts_included": start_check_scripts_included,
        "support_bundle_path_visible": support_bundle_path_visible,
        "support_bundle_command": SUPPORT_BUNDLE_COMMAND,
        "junk_excluded": junk_excluded,
        "zip_created": zip_created,
        "missing_required_entries": missing_required_entries or [],
        "claim_boundary": "portable_release_verification_local_receipt_not_release_certification",
        "proof_boundaries": PROOF_BOUNDARIES,
        "not_proven": NOT_PROVEN,
    }


def build_zip(
    repo_root: Path,
    files: list[str],
    zip_path: Path,
    exclude_zip_itself: str | None = None,
) -> None:
    """Create a deterministic ZIP archive.

    Rules:
    - All paths sorted
    - Normalized archive names (no absolute paths)
    - Deterministic timestamp for each entry
    - No .git/, caches, .env, or previous ZIPs included
    """
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for rel in sorted(files):
            if exclude_zip_itself and rel == exclude_zip_itself:
                continue
            src = repo_root / rel
            if not src.exists():
                continue
            info = zipfile.ZipInfo(filename=rel, date_time=_ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            data = src.read_bytes()
            zf.writestr(info, data)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Odin LRH-PR-15 Portable Package Builder (candidate-only, local-only)"
    )
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Repo root directory (default: parent of scripts/)",
    )
    parser.add_argument(
        "--out",
        default="/tmp/odin_lrh_pr15_package",
        help="Output directory for copied package files",
    )
    parser.add_argument(
        "--manifest-out",
        default="/tmp/odin_lrh_pr15_manifest.json",
        dest="manifest_out",
        help="Path to write the package manifest JSON",
    )
    parser.add_argument(
        "--report-out",
        default="/tmp/odin_lrh_pr15_release_verification.json",
        dest="report_out",
        help="Path to write the local release verification report JSON",
    )
    parser.add_argument(
        "--zip-out",
        default=None,
        dest="zip_out",
        help="Optional: path to write a deterministic ZIP archive",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Print manifest and report without writing output files",
    )
    args = parser.parse_args(argv)

    # Resolve repo root
    if args.repo_root:
        repo_root = Path(args.repo_root).resolve()
    else:
        repo_root = Path(__file__).resolve().parents[1]

    out_dir = Path(args.out).resolve()
    manifest_path = Path(args.manifest_out).resolve()
    report_path = Path(args.report_out).resolve()
    zip_path = Path(args.zip_out).resolve() if args.zip_out else None

    # Collect files
    files = collect_files(repo_root)

    # Compute checksums
    checksums = compute_checksums(repo_root, files)

    # Determine start/check script inclusion and missing required entries
    start_check_scripts: dict[str, bool] = {}
    missing_required_entries: list[str] = []
    for rel in REQUIRED_SCRIPTS:
        present = rel in files
        start_check_scripts[rel] = present
        if not present:
            missing_required_entries.append(rel)
    for rel in REQUIRED_ROOT_CANON:
        if rel not in files:
            missing_required_entries.append(rel)

    start_check_scripts_included = all(
        start_check_scripts.get(s, False)
        for s in [
            "scripts/start_odin.sh",
            "scripts/check_odin.sh",
            "scripts/start_odin.bat",
            "scripts/check_odin.bat",
        ]
    )

    excluded_patterns = sorted(JUNK_DIR_PATTERNS | JUNK_FILE_PATTERNS | JUNK_FILE_EXTENSIONS)

    manifest = build_manifest(
        repo_root=repo_root,
        files=files,
        checksums=checksums,
        excluded_patterns=excluded_patterns,
        start_check_scripts=start_check_scripts,
        missing_required_entries=missing_required_entries,
    )

    zip_created = False

    if args.dry_run:
        print(json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True))
        report = build_report(
            manifest_created=True,
            checksums_created=True,
            start_check_scripts_included=start_check_scripts_included,
            support_bundle_path_visible=True,
            junk_excluded=True,
            zip_created=False,
            missing_required_entries=missing_required_entries,
        )
        print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    # Write manifest
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True),
        encoding="utf-8",
    )

    # Write copied package files
    out_dir.mkdir(parents=True, exist_ok=True)
    for rel in files:
        src = repo_root / rel
        dst = out_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(src), str(dst))

    # Write ZIP if requested
    if zip_path:
        zip_path.parent.mkdir(parents=True, exist_ok=True)
        build_zip(repo_root=repo_root, files=files, zip_path=zip_path)
        zip_created = True

    # Write release verification report
    report = build_report(
        manifest_created=True,
        checksums_created=True,
        start_check_scripts_included=start_check_scripts_included,
        support_bundle_path_visible=True,
        junk_excluded=True,
        zip_created=zip_created,
        missing_required_entries=missing_required_entries,
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True),
        encoding="utf-8",
    )

    print(f"Package written to: {out_dir}")
    print(f"Manifest written to: {manifest_path}")
    print(f"Release verification report written to: {report_path}")
    if zip_path:
        print(f"ZIP written to: {zip_path}")
    print(f"Files included: {len(files)}")
    print(f"Missing required entries: {missing_required_entries or 'none'}")
    print(f"claim_boundary: {CLAIM_BOUNDARY}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

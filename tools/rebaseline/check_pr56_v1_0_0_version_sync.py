#!/usr/bin/env python3
"""PR56 deterministic version-sync and external-release-prep validator."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

CLAIM_BOUNDARY = "pr56_v1_0_0_version_sync_external_release_prep_not_external_release"
POSTURE = "v1.0.0 prepared_not_released"
VERSION = "1.0.0"
OLD_DESCRIPTION = "Odin Agent Shell v7.1 repo prep full shadow runtime coverage and validation scaffold"
NEW_DESCRIPTION = "Local-first candidate-work kernel for bounded AI coordination, receipt discipline, and app-owned apply workflows"
PR56_FILES = [
    "pyproject.toml",
    "README.md",
    "docs/release/V1_0_0_EXTERNAL_RELEASE_PREP.md",
    "docs/release/V1_0_0_MANUAL_RELEASE_CHECKLIST.md",
    "docs/release/V1_0_0_RELEASE_NOTES_DRAFT.md",
    "tools/rebaseline/check_pr56_v1_0_0_version_sync.py",
    "reports/pr56_v1_0_0_version_sync_report.json",
    "tests/test_pr56_v1_0_0_version_sync.py",
    "docs/codex/reports/PR56_V1_0_0_VERSION_SYNC_RETURN_REPORT.md",
]
FORBIDDEN_SCRIPT_TOKENS = ["eval(", "exec(", "subprocess", "urllib", "requests", "socket", "twine ", "python -m build", "git tag", "gh release", "publish "]

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def has_positive_claim(text: str, phrase: str) -> bool:
    safe_prefixes = ("no ", "not ", "does not claim ", "is not ", "unless ", "without ")
    low = text.lower()
    start = 0
    phrase = phrase.lower()
    while True:
        idx = low.find(phrase, start)
        if idx == -1:
            return False
        before = low[max(0, idx - 32):idx]
        if not any(before.endswith(prefix) for prefix in safe_prefixes):
            return True
        start = idx + len(phrase)

def build_report(repo_root: Path, generated_at_utc: str | None) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    pyproject = repo_root / "pyproject.toml"
    readme = repo_root / "README.md"
    if not pyproject.exists():
        errors.append("pyproject.toml missing")
        py = ""
    else:
        py = read(pyproject)
        if 'version = "1.0.0"' not in py:
            errors.append("pyproject.toml version is not 1.0.0")
        if OLD_DESCRIPTION in py:
            errors.append("old internal/prep description remains in pyproject.toml")
        if NEW_DESCRIPTION not in py:
            errors.append("new public description missing from pyproject.toml")
    if not readme.exists():
        errors.append("README.md missing")
        rm = ""
    else:
        rm = read(readme)
        if POSTURE not in rm:
            errors.append("README.md missing v1.0.0 prepared_not_released")
        for phrase, label in [("tag exists", "tag"), ("github release exists", "GitHub Release"), ("published to pypi", "PyPI"), ("available on pypi", "PyPI availability"), ("release assets uploaded", "release assets")]:
            if has_positive_claim(rm, phrase):
                errors.append(f"README.md appears to positively claim {label}")
        if "DONATIONS.md" not in rm:
            errors.append("README.md missing DONATIONS.md link")
        if "## Danke / Thank You" not in rm:
            errors.append("README.md missing Danke / Thank You block header")
        if "model output is projection, not truth" not in rm.lower() and "model output" not in rm.lower():
            errors.append("README.md missing model-output/projection boundary language")
    if not (repo_root / "DONATIONS.md").exists():
        errors.append("DONATIONS.md missing")
    for path in PR56_FILES[2:5]:
        if not (repo_root / path).exists():
            errors.append(f"missing release-prep doc: {path}")
    checklist = repo_root / "docs/release/V1_0_0_MANUAL_RELEASE_CHECKLIST.md"
    if checklist.exists():
        ck = read(checklist)
        for token in ["tag", "GitHub Release", "PyPI", "assets"]:
            if token not in ck:
                errors.append(f"manual checklist missing {token}")
        if ck.count("manual_only: true") < 5 or ck.count("claimed_by_pr56: false") < 5:
            errors.append("manual external actions are not all marked manual_only and unclaimed")
    sm = repo_root / "SYSTEM_MAP.json"
    if not sm.exists() or "pr56_v1_0_0_version_sync" not in read(sm):
        errors.append("SYSTEM_MAP.json missing PR56 entry")
    fm = repo_root / "FILE_MANIFEST.json"
    fm_text = read(fm) if fm.exists() else ""
    if not fm.exists():
        errors.append("FILE_MANIFEST.json missing")
    else:
        for path in PR56_FILES:
            if path not in fm_text:
                errors.append(f"FILE_MANIFEST.json missing {path}")
    cli = repo_root / "odin/cli.py"
    if not cli.exists() or "validate_pr56_v1_version_sync" not in read(cli) or "validate-pr56-v1-version-sync" not in read(cli):
        errors.append("odin/cli.py missing PR56 validate-all/command integration")
    script = read(repo_root / "tools/rebaseline/check_pr56_v1_0_0_version_sync.py")
    inspected = "\n".join(line for line in script.splitlines() if "FORBIDDEN_SCRIPT_TOKENS" not in line and not line.strip().startswith("\"") and not line.strip().startswith("'") )
    for token in FORBIDDEN_SCRIPT_TOKENS:
        if token in inspected:
            errors.append(f"PR56 script contains forbidden token: {token}")
    return {
        "status": "ok" if not errors else "error",
        "error_count": len(errors),
        "warning_count": len(warnings),
        "claim_boundary": CLAIM_BOUNDARY,
        "package_version": VERSION,
        "release_posture": POSTURE,
        "external_release_claimed": False,
        "tag_creation_claimed": False,
        "github_release_claimed": False,
        "pypi_publication_claimed": False,
        "release_asset_upload_claimed": False,
        "generated_at_utc": generated_at_utc,
        "errors": errors,
        "warnings": warnings,
    }

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", required=True)
    parser.add_argument("--generated-at-utc", default=None)
    args = parser.parse_args(argv)
    report = build_report(Path(args.repo_root).resolve(), args.generated_at_utc)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if report["status"] == "ok" else 1

if __name__ == "__main__":
    raise SystemExit(main())

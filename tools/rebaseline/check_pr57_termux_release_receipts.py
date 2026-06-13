#!/usr/bin/env python3
"""PR57 Termux temp-path and v1.0.0 release-receipts validator."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

PR57_FILES = [
    "tests/test_lrh_pr_09_trace_viewer.py",
    "docs/release/V1_0_0_EXTERNAL_RELEASE_RECEIPTS.md",
    "reports/pr57_termux_and_release_receipts_report.json",
    "tools/rebaseline/check_pr57_termux_release_receipts.py",
    "tests/test_pr57_termux_release_receipts.py",
]
FORBIDDEN_TMP = "/tmp/lrh_pr_09_packet.json"
FORBIDDEN_POSITIVE = [
    "production_ready",
    "security certified",
    "security certification verified",
    "model benchmark verified",
    "published to pypi",
    "available on pypi",
    "release assets uploaded",
    "assets uploaded",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def build_report(repo_root: Path, generated_at_utc: str | None = None) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    legacy_test = repo_root / "tests/test_lrh_pr_09_trace_viewer.py"
    if not legacy_test.exists():
        errors.append("missing tests/test_lrh_pr_09_trace_viewer.py")
        legacy_text = ""
    else:
        legacy_text = read(legacy_test)
        if FORBIDDEN_TMP in legacy_text:
            errors.append(f"hardcoded Termux-hostile path remains: {FORBIDDEN_TMP}")
        if "tmp_path" not in legacy_text and "tempfile.gettempdir" not in legacy_text and ".tmp" not in legacy_text:
            errors.append("LRH-PR-09 tests do not show portable temp path usage")
        for token in ["agent-handoff", "agent-guard", "agent-check", "LRH-PR-09", "candidate_only", "app_owned_apply"]:
            if token not in legacy_text:
                errors.append(f"LRH-PR-09 test intent weakened; missing {token}")
    doc = repo_root / "docs/release/V1_0_0_EXTERNAL_RELEASE_RECEIPTS.md"
    if not doc.exists():
        errors.append("missing docs/release/V1_0_0_EXTERNAL_RELEASE_RECEIPTS.md")
        doc_text = ""
    else:
        doc_text = read(doc)
        for token in ["v1.0.0", "GitHub Release", "PyPI publication | not claimed", "Release assets | not claimed"]:
            if token not in doc_text:
                errors.append(f"release receipt doc missing {token}")
        low = doc_text.lower()
        for phrase in FORBIDDEN_POSITIVE:
            start = 0
            while True:
                idx = low.find(phrase, start)
                if idx == -1:
                    break
                before = low[max(0, idx - 48):idx]
                if not any(marker in before for marker in ["no ", "not ", "does not claim", "without "]):
                    errors.append(f"release receipt doc contains unsupported positive claim: {phrase}")
                    break
                start = idx + len(phrase)
    report = repo_root / "reports/pr57_termux_and_release_receipts_report.json"
    if not report.exists():
        errors.append("missing reports/pr57_termux_and_release_receipts_report.json")
    else:
        try:
            data = json.loads(read(report))
            if data.get("release_receipts", {}).get("pypi_claimed") is not False:
                errors.append("PR57 report must not claim PyPI")
            if data.get("release_receipts", {}).get("assets_claimed") is not False:
                errors.append("PR57 report must not claim release assets")
        except Exception as exc:
            errors.append(f"PR57 report is invalid JSON: {exc}")
    cli = repo_root / "odin/cli.py"
    cli_text = read(cli) if cli.exists() else ""
    if "validate_pr57_termux_release_receipts" not in cli_text or "validate-pr57-termux-release-receipts" not in cli_text:
        errors.append("odin/cli.py missing PR57 command integration")
    if "errors.extend(validate_pr57_termux_release_receipts())" not in cli_text:
        errors.append("validate-all does not include PR57")
    system_map = read(repo_root / "SYSTEM_MAP.json") if (repo_root / "SYSTEM_MAP.json").exists() else ""
    if "pr57_termux_release_receipts" not in system_map:
        errors.append("SYSTEM_MAP.json missing PR57 entry")
    manifest = read(repo_root / "FILE_MANIFEST.json") if (repo_root / "FILE_MANIFEST.json").exists() else ""
    for path in PR57_FILES:
        if path not in manifest:
            errors.append(f"FILE_MANIFEST.json missing {path}")
    return {
        "status": "ok" if not errors else "error",
        "error_count": len(errors),
        "warning_count": len(warnings),
        "claim_boundary": "pr57_termux_release_receipts_no_external_overclaim",
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

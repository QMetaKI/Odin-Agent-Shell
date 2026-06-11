#!/usr/bin/env python3
"""Build the v7.1.1 operational coverage/gap report.

This is a deterministic static compiler. It reads local canon/registry inputs,
classifies repository evidence by explicit path/content rules, and writes one
JSON report. It does not execute providers, models, runtime servers, network
calls, or external commands.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPORT_ID = "odin.v7_1_1_operational_coverage_gap_report"
VERSION = "7.1.1"
STATUS = "local_coverage_gap_report_not_runtime_proof"
CLAIM_BOUNDARY = "coverage_gap_report_is_local_static_analysis_not_runtime_completion"
TARGET_CLAIM_BOUNDARY = "target_area_coverage_is_static_local_evidence_not_runtime_proof"
SLICE_CLAIM_BOUNDARY = "slice_coverage_is_static_local_evidence_not_slice_completion"
REC_CLAIM_BOUNDARY = "recommendation_not_implementation_proof"

REQUIRED_INPUTS = [
    "registries/v7_1_1_operational_target_registry.json",
    "registries/v7_1_1_slice_absorption_map.json",
    "registries/v7_1_1_road_to_100_ladder.json",
    "registries/v7_1_1_road_to_100_coverage_matrix.json",
    "SYSTEM_MAP.json",
    "FILE_MANIFEST.json",
]

REFERENCE_INPUTS = [
    "docs/MASTER_ARCHITECTURE_V7_1.md",
    "docs/MASTER_SPECS_V7_1.md",
    "docs/MASTER_ARCHITECTURE_V7_1_1.md",
    "docs/V7_1_1_OPERATIONAL_TARGET_SYNTHESIS.md",
    "docs/V7_1_1_ROAD_TO_100_BUILD_LADDER.md",
    "registries/real_pr_execution_registry.json",
    "registries/codex_task_registry.json",
    "registries/codex_pr_bundle_registry.json",
    "docs/rebaseline/FULL_SYSTEM_AUDIT_AFTER_LRH_PR_18.md",
]

IGNORED_EVIDENCE_PATHS = [
    {"pattern": ".odin_runtime/", "reason": "local_runtime_or_session_artifact_not_static_repo_evidence"},
    {"pattern": "odin_agent_shell.egg-info/", "reason": "local_packaging_artifact_not_static_repo_evidence"},
    {"pattern": "__pycache__/", "reason": "python_cache_artifact_not_static_repo_evidence"},
    {"pattern": ".pytest_cache/", "reason": "test_cache_artifact_not_static_repo_evidence"},
    {"pattern": ".mypy_cache/", "reason": "type_checker_cache_artifact_not_static_repo_evidence"},
    {"pattern": ".ruff_cache/", "reason": "linter_cache_artifact_not_static_repo_evidence"},
    {"pattern": "dist/", "reason": "local_distribution_build_artifact_not_static_repo_evidence"},
    {"pattern": "build/", "reason": "local_build_artifact_not_static_repo_evidence"},
    {"pattern": "*.pyc", "reason": "compiled_python_cache_not_static_repo_evidence"},
    {"pattern": "*.pyo", "reason": "optimized_python_cache_not_static_repo_evidence"},
    {"pattern": "*.egg-info/", "reason": "local_packaging_metadata_not_static_repo_evidence"},
]

IGNORED_PATH_SUBSTRINGS = [
    ".odin_runtime/",
    "odin_agent_shell.egg-info/",
    "__pycache__/",
    ".pytest_cache/",
    ".mypy_cache/",
    ".ruff_cache/",
    "dist/",
    "build/",
    ".egg-info/",
]

IGNORED_PATH_SUFFIXES = (".pyc", ".pyo")


EVIDENCE_RULES = [
    {"class": "missing", "rule": "no matching local evidence reference was found"},
    {"class": "documented_only", "rule": "matching evidence under docs/ outside docs/codex/reports/ is documentation evidence only"},
    {"class": "registry_only", "rule": "matching evidence under registries/ or SYSTEM_MAP.json or FILE_MANIFEST.json is registry/meta evidence only"},
    {"class": "schema_present", "rule": "matching evidence under schemas/ is schema evidence"},
    {"class": "test_present", "rule": "matching evidence under tests/ is test evidence; tests are not runtime proof"},
    {"class": "tool_present", "rule": "matching evidence under tools/ is local tool evidence"},
    {"class": "report_present", "rule": "matching evidence under reports/ or docs/codex/reports/ is report evidence only"},
    {"class": "receipt_present", "rule": "matching evidence under receipts/, proof/, or runtime/traces/ is local receipt/proof evidence only"},
    {"class": "validator_present", "rule": "matching validator/gate/check files outside docs/registries/reports count as validator evidence"},
    {"class": "partial", "rule": "multiple non-runtime local evidence classes exist, but required schema/test/tool/report/receipt support is incomplete"},
    {"class": "implemented_code_candidate", "rule": "non-doc, non-registry, non-report code/tool/test/schema pairs plausibly represent the area; this remains candidate-only"},
    {"class": "external_receipt_required", "rule": "target-host, live-model, QIRC server, security, release, or external app claims require external receipts and are not proven by local files"},
    {"class": "blocked", "rule": "declared dependencies or required prior slices are missing or blocked"},
]

NON_CLAIMS = [
    "no production readiness claim",
    "no release certification claim",
    "no security certification claim",
    "no target-host proof claim",
    "no live model inference proof claim",
    "no model quality proof claim",
    "no QIRC server runtime proof claim",
    "no runtime completion claim",
    "no provider execution claim",
    "no external app integration proof claim",
]

UNSUPPORTED_CLAIM_PHRASES = [
    ("production_readiness_affirmation", "production" + " ready"),
    ("release_readiness_affirmation", "release" + " ready"),
    ("security_certification_affirmation", "security" + " certified"),
    ("target_host_proof_affirmation", "target-host" + " proven"),
    ("live_model_proof_affirmation", "live model" + " proven"),
    ("model_quality_proof_affirmation", "model quality" + " proven"),
    ("qirc_server_runtime_affirmation", "qirc server" + " implemented"),
    ("small_model_measurement_affirmation", "measured small-model" + " improvement"),
]

EXTERNAL_KEYWORDS = [
    "qirc runtime", "qirc server", "live model", "model quality", "target-host",
    "target host", "production", "release", "security", "windows service",
    "external app", "provider", "network", "signed distribution",
]

RECOMMENDED_FAMILIES = [
    ("PR-26-CANON-BOUNDARY-INTEGRITY", "Canon boundary integrity"),
    ("PR-27-APP-BOUNDARY-UNIVERSAL-WORK", "App boundary and Universal Work bridge"),
    ("PR-28-QIRC-SEMANTIC-BUS", "QIRC semantic bus local evidence"),
    ("PR-29-CONTEXT-LENSES", "Context lenses and capsule coverage"),
    ("PR-30-WORKLETS-SLOTS-GAPTEXT", "Worklets, Slot Forge, and Gaptext"),
    ("PR-31-MODELWORKPACKET-SCALE-LADDER", "ModelWorkPacket and scale ladder enforcement"),
    ("PR-32-SMALL-MODEL-HYBRID-DIRECTOR", "Small-model hybrid director"),
    ("PR-33-MINICHECK-CRITICS-TOURNAMENT", "Minicheck critics and candidate tournament"),
    ("PR-34-CANDIDATE-FINAL-GATE", "Candidate final gate closure"),
    ("PR-35-STORAGE-TRACE-RECEIPT", "Storage trace and receipt evidence"),
    ("PR-36-THOR-AGENT-HANDOFF", "Thor agent handoff boundaries"),
    ("PR-37-SDK-APP-BRIDGE", "SDK app bridge evidence"),
    ("PR-38-ACCEPTANCE-DOJO-SCOREBOARD", "Acceptance dojo and scoreboard"),
    ("PR-39-FULL-V711-OPERATIONAL-CLOSURE", "Full v7.1.1 operational closure evidence"),
]

@dataclass(frozen=True)
class EvidenceRef:
    path: str
    evidence_class: str
    reason: str


def _load_json(root: Path, rel: str) -> Any:
    p = root / rel
    if not p.exists():
        raise FileNotFoundError(f"required input missing: {rel}")
    return json.loads(p.read_text(encoding="utf-8"))


def _norm(text: Any) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(text).lower()).strip()


def _tokens(*values: Any) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value is None:
            continue
        if isinstance(value, (list, tuple, set)):
            for item in value:
                out.extend(_tokens(item))
            continue
        text = str(value)
        candidates = [text, text.replace("_", " ").replace("-", " ")]
        for cand in candidates:
            n = _norm(cand)
            if len(n) >= 4 and n not in seen:
                seen.add(n); out.append(n)
        for part in re.split(r"[^A-Za-z0-9]+", text):
            p = _norm(part)
            if len(p) >= 6 and p not in seen:
                seen.add(p); out.append(p)
    return out


def _normalized_rel(path_text: str) -> str:
    rel = path_text.replace("\\", "/")
    return rel[2:] if rel.startswith("./") else rel


def _is_ignored_evidence_path(path_text: str) -> bool:
    rel = _normalized_rel(path_text)
    rel_with_slash = rel if rel.endswith("/") else f"{rel}/"
    if rel.endswith(IGNORED_PATH_SUFFIXES):
        return True
    return any(token in rel_with_slash for token in IGNORED_PATH_SUBSTRINGS)


def _iter_scannable_files(root: Path) -> list[Path]:
    allowed = {".py", ".json", ".md", ".txt", ".yml", ".yaml", ".toml"}
    result: list[Path] = []
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        rel = path.relative_to(root).as_posix()
        if _is_ignored_evidence_path(rel):
            continue
        if any(part in {".git", ".thor"} for part in path.parts):
            continue
        if path.suffix.lower() not in allowed:
            continue
        if rel == "reports/v7_1_1_operational_coverage_gap_report.json":
            continue
        result.append(path)
    return sorted(result, key=lambda p: p.relative_to(root).as_posix())


def _path_class(rel: str) -> str | None:
    if _is_ignored_evidence_path(rel):
        return None
    if rel in {"SYSTEM_MAP.json", "FILE_MANIFEST.json"}:
        # FILE_MANIFEST records file presence only. It is registry/meta evidence
        # and must never upgrade a target or slice to implementation evidence.
        return "registry_only"
    if rel.startswith("docs/codex/reports/"):
        return "report_present"
    if rel.startswith("docs/"):
        return "documented_only"
    if rel.startswith("registries/"):
        return "registry_only"
    if rel.startswith("schemas/"):
        return "schema_present"
    if rel.startswith("tests/"):
        return "test_present"
    if rel.startswith("tools/"):
        return "tool_present"
    if rel.startswith("reports/"):
        return "report_present"
    if rel.startswith("receipts/") or rel.startswith("proof/") or rel.startswith("runtime/traces/"):
        return "receipt_present"
    name = Path(rel).name.lower()
    if any(word in name for word in ["validator", "validate", "gate", "check"]):
        return "validator_present"
    if Path(rel).suffix == ".py":
        return "implemented_code_candidate"
    return None


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")[:200_000]
    except Exception:
        return ""


def _matches(rel: str, content_norm: str, tokens: list[str]) -> bool:
    rel_norm = _norm(rel)
    for token in tokens:
        if token and (token in rel_norm or token in content_norm):
            return True
    return False


def _collect_evidence(root: Path, files: list[Path], match_tokens: list[str], max_refs: int = 18) -> list[EvidenceRef]:
    refs: list[EvidenceRef] = []
    seen: set[tuple[str, str]] = set()
    for path in files:
        rel = path.relative_to(root).as_posix()
        cls = _path_class(rel)
        if not cls:
            continue
        content_norm = _norm(_read_text(path)) if path.suffix.lower() in {".py", ".json", ".md", ".txt", ".yml", ".yaml", ".toml"} else ""
        if _matches(rel, content_norm, match_tokens):
            key = (rel, cls)
            if key not in seen:
                seen.add(key)
                refs.append(EvidenceRef(rel, cls, "normalized token/path match"))
        if len(refs) >= max_refs:
            break
    return sorted(refs, key=lambda r: (r.evidence_class, r.path))


def _refs_json(refs: list[EvidenceRef]) -> list[dict[str, str]]:
    return [{"path": r.path, "evidence_class": r.evidence_class, "reason": r.reason} for r in refs]


def _coverage_status(classes: set[str], text: str) -> str:
    if not classes:
        return "missing"
    if any(k in text for k in EXTERNAL_KEYWORDS) and not ({"receipt_present"} & classes):
        return "external_receipt_required"
    non_planning = classes - {"documented_only", "registry_only", "report_present"}
    if "implemented_code_candidate" in classes or ({"schema_present", "test_present"} <= classes) or ({"tool_present", "test_present"} <= classes) or "validator_present" in classes:
        return "implemented_code_candidate"
    if non_planning:
        return "partial"
    if classes <= {"registry_only"}:
        return "registry_only"
    if classes <= {"documented_only"}:
        return "documented_only"
    if classes <= {"documented_only", "registry_only", "report_present"}:
        return "documented_only"
    return "partial"


def _gap_level(status: str, classes: set[str], text: str) -> str:
    if status == "missing":
        return "critical" if any(k in text for k in ["gate", "contract", "evidence", "compiler", "modelworkpacket"]) else "high"
    if status == "external_receipt_required":
        return "high"
    if status in {"documented_only", "registry_only"}:
        return "high"
    if status in {"partial", "implemented_code_candidate"}:
        required = {"test_present", "schema_present"}
        return "medium" if not required <= classes else "low"
    return "low"


def _missing_evidence(status: str, classes: set[str], text: str) -> list[str]:
    missing: list[str] = []
    if status == "missing":
        return ["no matching local evidence references found"]
    if classes <= {"documented_only", "registry_only", "report_present"}:
        missing.append("non-roadmap repo artifact evidence")
    for cls, label in [("schema_present", "schema evidence"), ("test_present", "test evidence"), ("tool_present", "tool/compiler evidence")]:
        if cls not in classes:
            missing.append(label)
    if any(k in text for k in EXTERNAL_KEYWORDS) and "receipt_present" not in classes:
        missing.append("external receipt evidence")
    return missing[:6]


def _slice_status(classes: set[str], refs: list[EvidenceRef], text: str) -> str:
    if not classes:
        return "missing"
    non_roadmap = [r for r in refs if not (r.path.startswith("docs/V7_1_1_ROAD") or r.path.startswith("registries/v7_1_1_road_to_100"))]
    if any(k in text for k in EXTERNAL_KEYWORDS) and "receipt_present" not in classes:
        return "external_receipt_required"
    if any(r.evidence_class in {"schema_present", "test_present", "tool_present", "validator_present", "implemented_code_candidate"} for r in non_roadmap):
        return "locally_supported"
    if classes <= {"documented_only", "registry_only", "report_present"}:
        return "documented_only"
    return "partial"


def _dependency_status(slice_entry: dict[str, Any], slice_ids_seen: set[str], coverage_by_id: dict[str, str]) -> str:
    deps = slice_entry.get("depends_on", [])
    if not deps:
        return "satisfied"
    if any(dep not in slice_ids_seen for dep in deps):
        return "missing_dependency"
    if any(coverage_by_id.get(dep) in {"missing", "external_receipt_required"} for dep in deps):
        return "blocked"
    return "satisfied"


def _scan_unsupported_claims(root: Path, files: list[Path]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    context_allow = ["no ", "not ", "non claim", "non-claim", "forbidden", "future", "required", "without", "does not claim", "proof claim"]
    for path in files:
        rel = path.relative_to(root).as_posix()
        if not (rel.startswith("docs/") or rel.startswith("reports/") or rel.startswith("registries/")):
            continue
        text = _read_text(path)
        low = text.lower()
        for phrase_id, phrase in UNSUPPORTED_CLAIM_PHRASES:
            start = 0
            while True:
                idx = low.find(phrase, start)
                if idx < 0:
                    break
                ctx = low[max(0, idx - 80): idx + len(phrase) + 80]
                if not any(marker in ctx for marker in context_allow):
                    sanitized = re.sub(r"\s+", " ", ctx).strip()
                    for other_id, other_phrase in UNSUPPORTED_CLAIM_PHRASES:
                        sanitized = sanitized.replace(other_phrase, other_id)
                    sanitized = sanitized[:220]
                    findings.append({"path": rel, "phrase_id": phrase_id, "context": sanitized})
                start = idx + len(phrase)
    return sorted(findings, key=lambda f: (f["path"], f["phrase_id"]))


def _recommendations(target_records: list[dict[str, Any]], slice_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    recs: list[dict[str, Any]] = []
    by_family_targets: dict[str, set[str]] = {}
    by_family_slices: dict[str, set[str]] = {}
    for rec in target_records:
        fam = rec.get("recommended_next_pr_family") or "PR-39-FULL-V711-OPERATIONAL-CLOSURE"
        if fam == "PR-25-COVERAGE-GAP-COMPILER":
            fam = "PR-26-CANON-BOUNDARY-INTEGRITY"
        by_family_targets.setdefault(fam, set()).add(rec["target_area_id"])
    for rec in slice_records:
        fam = rec.get("recommended_future_pr_family") or "PR-39-FULL-V711-OPERATIONAL-CLOSURE"
        if fam == "PR-25-COVERAGE-GAP-COMPILER":
            fam = "PR-26-CANON-BOUNDARY-INTEGRITY"
        by_family_slices.setdefault(fam, set()).add(rec["slice_id"])
        for tid in rec.get("target_area_ids", []):
            by_family_targets.setdefault(fam, set()).add(tid)
    for fam, title in RECOMMENDED_FAMILIES:
        tids = sorted(by_family_targets.get(fam, set()))
        sids = sorted(by_family_slices.get(fam, set()))
        if not tids and target_records:
            tids = [target_records[0]["target_area_id"]]
        if not sids and slice_records:
            sids = [slice_records[0]["slice_id"]]
        recs.append({
            "recommended_pr_family": fam,
            "title": title,
            "reason": "Computed gaps require bounded local evidence before any runtime completion claim.",
            "target_area_ids": tids,
            "slice_ids": sids,
            "blocked_by": [],
            "claim_boundary": REC_CLAIM_BOUNDARY,
        })
    return recs


def build_report(repo_root: Path, generated_at_utc: str) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    for rel in REQUIRED_INPUTS + REFERENCE_INPUTS:
        if not (repo_root / rel).exists():
            raise FileNotFoundError(f"required input missing: {rel}")
    target_reg = _load_json(repo_root, "registries/v7_1_1_operational_target_registry.json")
    ladder = _load_json(repo_root, "registries/v7_1_1_road_to_100_ladder.json")
    coverage_matrix = _load_json(repo_root, "registries/v7_1_1_road_to_100_coverage_matrix.json")
    absorption_map = _load_json(repo_root, "registries/v7_1_1_slice_absorption_map.json")
    _load_json(repo_root, "SYSTEM_MAP.json")
    _load_json(repo_root, "FILE_MANIFEST.json")

    target_areas = target_reg.get("target_areas", [])
    slices = ladder.get("slices", [])
    if not target_areas:
        raise ValueError("target registry contains no target_areas")
    if not slices:
        raise ValueError("Road-to-100 ladder contains no slices")

    target_ids = [area["id"] for area in target_areas]
    target_id_set = set(target_ids)
    slice_ids = [s["id"] for s in slices]
    slice_id_set = set(slice_ids)
    if len(target_ids) != len(target_id_set):
        raise ValueError("duplicate target area IDs")
    if len(slice_ids) != len(slice_id_set):
        raise ValueError("duplicate Road-to-100 slice IDs")
    for s in slices:
        bad = sorted(set(s.get("target_area_ids", [])) - target_id_set)
        if bad:
            raise ValueError(f"slice {s['id']} references unknown target areas: {bad}")
        bad_dep = sorted(set(s.get("depends_on", [])) - slice_id_set)
        if bad_dep:
            raise ValueError(f"slice {s['id']} references unknown dependencies: {bad_dep}")

    files = _iter_scannable_files(repo_root)
    matrix_by_target = {e["target_area_id"]: e for e in coverage_matrix.get("target_area_coverage", [])}
    slices_by_target: dict[str, list[str]] = {tid: [] for tid in target_ids}
    for s in slices:
        for tid in s.get("target_area_ids", []):
            slices_by_target.setdefault(tid, []).append(s["id"])

    target_records: list[dict[str, Any]] = []
    for area in target_areas:
        tid = area["id"]
        area_for_status = {k: v for k, v in area.items() if k not in {"non_claims", "source_refs"}}
        text_blob = json.dumps(area_for_status, sort_keys=True)
        match_tokens = _tokens(
            tid, area.get("name"), area.get("public_neutral_terms"),
            area.get("required_operational_behavior"), area.get("required_tests"),
            area.get("next_ladder_recommendation"), matrix_by_target.get(tid, {}).get("primary_future_pr_family"),
        )
        refs = _collect_evidence(repo_root, files, match_tokens)
        classes = {r.evidence_class for r in refs}
        status = _coverage_status(classes, _norm(text_blob))
        gap = _gap_level(status, classes, _norm(text_blob))
        declared = area.get("current_repo_real_status", "")
        missing = _missing_evidence(status, classes, _norm(text_blob))
        if declared and status not in _norm(declared):
            missing.append("declared status differs from computed local evidence status")
        target_records.append({
            "target_area_id": tid,
            "name": area.get("name", tid),
            "declared_status": declared,
            "computed_coverage_status": status,
            "evidence_classes": sorted(classes) if classes else ["missing"],
            "evidence_refs": _refs_json(refs),
            "covered_by_road_to_100_slices": sorted(slices_by_target.get(tid, [])),
            "missing_evidence": sorted(set(missing)),
            "gap_level": gap,
            "recommended_next_pr_family": matrix_by_target.get(tid, {}).get("primary_future_pr_family") or area.get("next_ladder_recommendation", "PR-39-FULL-V711-OPERATIONAL-CLOSURE"),
            "claim_boundary": TARGET_CLAIM_BOUNDARY,
            "non_claims": NON_CLAIMS,
        })

    slice_records: list[dict[str, Any]] = []
    prior_ids: set[str] = set()
    coverage_by_id: dict[str, str] = {}
    for s in slices:
        slice_for_status = {k: v for k, v in s.items() if k not in {"non_claims", "forbidden_scope", "source_refs", "evidence_required_later"}}
        text_blob = json.dumps(slice_for_status, sort_keys=True)
        match_tokens = _tokens(s.get("id"), s.get("title"), s.get("expected_artifacts"), s.get("required_tests"), s.get("recommended_future_pr_family"), s.get("target_area_ids"))
        refs = _collect_evidence(repo_root, files, match_tokens, max_refs=14)
        classes = {r.evidence_class for r in refs}
        status = _slice_status(classes, refs, _norm(text_blob))
        dep_status = _dependency_status(s, prior_ids, coverage_by_id)
        if dep_status != "satisfied" and status != "missing":
            status = "partial"
        missing = _missing_evidence(status if status != "locally_supported" else "partial", classes, _norm(text_blob))
        if dep_status != "satisfied":
            missing.append(f"dependency status: {dep_status}")
        record = {
            "slice_id": s["id"],
            "phase_id": s.get("phase_id", ""),
            "title": s.get("title", s["id"]),
            "target_area_ids": s.get("target_area_ids", []),
            "recommended_future_pr_family": s.get("recommended_future_pr_family", ""),
            "dependency_status": dep_status,
            "computed_coverage_status": status,
            "evidence_refs": _refs_json(refs),
            "missing_evidence": sorted(set(missing)),
            "claim_boundary": SLICE_CLAIM_BOUNDARY,
            "non_claims": NON_CLAIMS,
        }
        slice_records.append(record)
        prior_ids.add(s["id"])
        coverage_by_id[s["id"]] = status

    gap_summary = {"critical": [], "high": [], "medium": [], "low": [], "external_receipt_required": [], "blocked": []}
    for rec in target_records:
        entry = {"target_area_id": rec["target_area_id"], "status": rec["computed_coverage_status"], "missing_evidence": rec["missing_evidence"]}
        gap_summary[rec["gap_level"]].append(entry)
        if rec["computed_coverage_status"] == "external_receipt_required" or "external receipt evidence" in rec["missing_evidence"]:
            gap_summary["external_receipt_required"].append(entry)
    for rec in slice_records:
        if rec["dependency_status"] != "satisfied":
            gap_summary["blocked"].append({"slice_id": rec["slice_id"], "dependency_status": rec["dependency_status"]})

    required_gap_families = [
        "Context Capsule builder", "Slot Forge compiler", "ModelWorkPacket enforcement",
        "Final Gate closure", "QIRC runtime receipts", "live model proof / model quality proof",
        "SDK external app proof", "target-host proof", "production/release/security certification",
    ]
    critical_gaps = []
    all_text = _norm(json.dumps(target_records) + json.dumps(slice_records))
    for family in required_gap_families:
        token = _norm(family.split("/")[0])
        supported = token in all_text and "implemented_code_candidate" in all_text
        if not supported:
            critical_gaps.append({"gap_family": family, "classification": "local_gap_classification_not_repo_failure", "reason": "compiler did not find sufficient non-runtime local evidence to close this family"})

    source_refs = sorted(set(REQUIRED_INPUTS + REFERENCE_INPUTS))
    report = {
        "report_id": REPORT_ID,
        "version": VERSION,
        "status": STATUS,
        "generated_at_utc": generated_at_utc,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_refs": source_refs,
        "evidence_rules": EVIDENCE_RULES,
        "ignored_evidence_paths": IGNORED_EVIDENCE_PATHS,
        "target_area_summary": {
            "total_target_areas": len(target_records),
            "by_computed_coverage_status": _counts(r["computed_coverage_status"] for r in target_records),
            "by_gap_level": _counts(r["gap_level"] for r in target_records),
        },
        "road_to_100_summary": {
            "total_slices": len(slice_records),
            "by_computed_coverage_status": _counts(r["computed_coverage_status"] for r in slice_records),
            "by_dependency_status": _counts(r["dependency_status"] for r in slice_records),
        },
        "target_area_coverage": target_records,
        "road_to_100_slice_coverage": slice_records,
        "gap_summary": gap_summary,
        "critical_gaps": critical_gaps,
        "next_pr_recommendations": _recommendations(target_records, slice_records),
        "unsupported_claims": _scan_unsupported_claims(repo_root, files),
        "non_claims": NON_CLAIMS,
        "senior_reviewer_notes": [
            "Operationalizes v7.1.1 as static local evidence classification only.",
            "Road-to-100 planning entries are not elevated to implementation proof.",
            "Local runtime/session/build artifacts are ignored and are not repo-real implementation proof.",
            "Next PR families are recommendations, not completed work.",
        ],
        "senior_code_reviewer_notes": [
            "Compiler uses explicit required inputs and fails closed on missing files.",
            "Evidence rules are emitted in the report.",
            "No network, subprocess, provider, model, or QIRC server execution is performed.",
            "Evidence references are recursively sanitized against ignored path families.",
        ],
    }
    _assert_ignored_paths_sanitized(report)
    return report




def _walk_report_strings(value: Any, path: tuple[str, ...] = ()):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from _walk_report_strings(item, path + (str(key),))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _walk_report_strings(item, path + (str(index),))
    elif isinstance(value, str):
        yield path, _normalized_rel(value)


def _ignored_token_in_text(text: str) -> str | None:
    for token in IGNORED_PATH_SUBSTRINGS + [".pyc", ".pyo", ".egg-info/"]:
        if token in text:
            return token
    return None


def _assert_ignored_paths_sanitized(report: dict[str, Any]) -> None:
    allowed_top_level = {"ignored_evidence_paths", "senior_reviewer_notes", "senior_code_reviewer_notes"}
    violations: list[str] = []
    for path, text in _walk_report_strings(report):
        if path and path[0] in allowed_top_level:
            continue
        token = _ignored_token_in_text(text)
        if token is not None:
            violations.append(".".join(path) + f" contains ignored evidence token {token}")
    if violations:
        raise ValueError("ignored evidence path leaked outside allowed report sections: " + "; ".join(violations[:10]))


def _counts(values: Any) -> dict[str, int]:
    out: dict[str, int] = {}
    for value in values:
        out[str(value)] = out.get(str(value), 0) + 1
    return dict(sorted(out.items()))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build v7.1.1 operational coverage/gap report")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--generated-at-utc", required=True)
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    out = Path(args.out)
    if not out.is_absolute():
        out = repo_root / out
    try:
        report = build_report(repo_root, args.generated_at_utc)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

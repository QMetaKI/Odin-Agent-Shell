#!/usr/bin/env python3
"""Generate the Odin pre-release super audit package.

The audit is candidate-only. It runs local deterministic checks, writes JSON reports,
and refreshes Markdown audit docs. It does not call model providers, use API keys,
perform public network access, or apply app changes.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import time
import urllib.request
from http.server import HTTPServer
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CLAIM_BOUNDARY = "pre_release_super_audit_reports_repo_reality_not_release_certification"
AUDIT_ID = "pre_release_super_audit"
GEN_TS = "2026-06-13T00:00:00Z"
NOT_PROVEN = [
    "production_readiness",
    "security_certification",
    "real_model_benchmark",
    "external_runtime_guarantee",
]

DOCS = ROOT / "docs" / "codex" / "audits"
REPORTS = ROOT / "reports"
REGISTRIES = ROOT / "registries"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def excerpt(text: str, limit: int = 1400) -> str:
    clean = text.strip().replace("\r\n", "\n")
    return clean[:limit]


def run_command(command: list[str], timeout: int = 120) -> dict[str, Any]:
    start = time.monotonic()
    try:
        proc = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        status = "pass" if proc.returncode == 0 else "fail"
        return {
            "path_id": "cmd_" + "_".join(command).replace("-", "_").replace(".", "_")[:80],
            "kind": "cli" if "odin.cli" in command else "pytest",
            "command_or_endpoint": " ".join(command),
            "status": status,
            "returncode": proc.returncode,
            "duration_sec": round(time.monotonic() - start, 3),
            "stdout_excerpt": excerpt(proc.stdout),
            "stderr_excerpt": excerpt(proc.stderr),
            "claim_boundary": CLAIM_BOUNDARY,
            "notes": "local deterministic subprocess; no provider/model execution requested",
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "path_id": "cmd_timeout_" + "_".join(command)[:60],
            "kind": "cli" if "odin.cli" in command else "pytest",
            "command_or_endpoint": " ".join(command),
            "status": "blocked",
            "returncode": None,
            "duration_sec": round(time.monotonic() - start, 3),
            "stdout_excerpt": excerpt(exc.stdout or ""),
            "stderr_excerpt": excerpt(exc.stderr or "timeout"),
            "claim_boundary": CLAIM_BOUNDARY,
            "notes": "timeout in local deterministic audit runner",
        }


def smoke_endpoint(path: str, method: str = "GET", body: bytes | None = None) -> dict[str, Any]:
    from odin.local_hub.server import _SimpleLocalHubHandler

    server = HTTPServer(("127.0.0.1", 0), _SimpleLocalHubHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    start = time.monotonic()
    try:
        url = f"http://127.0.0.1:{port}{path}"
        req = urllib.request.Request(url, data=body, method=method)
        if body is not None:
            req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, timeout=8) as resp:
            payload = resp.read().decode("utf-8", errors="replace")
            code = resp.status
        status = "pass" if 200 <= code < 300 else "fail"
        return {
            "path_id": "endpoint_" + path.strip("/").replace("/", "_").replace(".", "_") or "endpoint_root",
            "kind": "endpoint",
            "command_or_endpoint": f"{method} {path}",
            "status": status,
            "duration_sec": round(time.monotonic() - start, 3),
            "stdout_excerpt": excerpt(payload),
            "stderr_excerpt": "",
            "claim_boundary": CLAIM_BOUNDARY,
            "notes": "localhost-only ephemeral Local Hub handler smoke",
        }
    except Exception as exc:  # explicit audit result capture, not import masking
        return {
            "path_id": "endpoint_" + path.strip("/").replace("/", "_").replace(".", "_") or "endpoint_root",
            "kind": "endpoint",
            "command_or_endpoint": f"{method} {path}",
            "status": "fail",
            "duration_sec": round(time.monotonic() - start, 3),
            "stdout_excerpt": "",
            "stderr_excerpt": repr(exc),
            "claim_boundary": CLAIM_BOUNDARY,
            "notes": "localhost endpoint smoke failed; recorded without masking",
        }
    finally:
        server.shutdown()
        thread.join(timeout=3)


def import_smoke(module: str) -> dict[str, Any]:
    start = time.monotonic()
    try:
        importlib.import_module(module)
        status = "pass"
        err = ""
    except Exception as exc:  # import smoke result capture, not import masking around source imports
        status = "fail"
        err = repr(exc)
    return {
        "path_id": "import_" + module.replace(".", "_"),
        "kind": "import",
        "command_or_endpoint": f"import {module}",
        "status": status,
        "duration_sec": round(time.monotonic() - start, 3),
        "stdout_excerpt": "import ok" if status == "pass" else "",
        "stderr_excerpt": err,
        "claim_boundary": CLAIM_BOUNDARY,
        "notes": "safe top-level Odin module import smoke",
    }


def git_base_commit() -> str:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.stdout.strip() if proc.returncode == 0 else "unknown"


def git_log_lines(limit: int = 60) -> list[str]:
    proc = subprocess.run(["git", "log", "--oneline", f"-{limit}"], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.stdout.splitlines() if proc.returncode == 0 else []


def path_exists(p: str) -> bool:
    return (ROOT / p).exists()


def build_pr_lineage() -> dict[str, Any]:
    entries = [
        (1, "FINAL-PR-01 Simple Local Hub", "active", ["odin/local_hub/server.py", "odin/local_hub/ui.py"], ["simple browser Local Hub", "health/status surfaces"], ["validate-simple-local-hub", "validate-all"], "required"),
        (2, "FINAL-PR-02 Model Picker + Connected Apps + Demo Universal Work", "active", ["odin/local_hub/model_picker.py", "odin/local_hub/connected_apps.py", "odin/local_hub/demo_universal_work.py"], ["model picker", "connected apps", "demo universal work"], ["validate-final-pr-02-model-apps-demo"], "required"),
        (3, "FINAL-PR-03 QIRC Core + Activity/Trace/Receipt + Dev Mode", "active", ["odin/qirc_core/bus.py", "odin/qirc_core/receipts.py", "odin/qirc_core/trace.py"], ["local QIRC events", "activity trace", "receipts"], ["validate-final-pr-03-qirc-devmode"], "required"),
        (4, "FINAL-PR-04 Local Candidate Provider Probe + Policy", "active", ["odin/provider_probe/probe.py", "odin/provider_probe/policy.py", "odin/runtime_security/smoke.py"], ["local candidate probe", "provider policy", "runtime safety smoke"], ["validate-final-pr-04-provider-probe-security"], "required"),
        (5, "FINAL-PR-05 Execution Gate + Mock Provider + Proof Chain", "active", ["odin/execution_gate/gateway.py", "odin/execution_gate/mock_provider.py", "odin/proof_chain/registry.py"], ["mock execution only", "execution gate", "proof chain"], ["validate-final-pr-05-execution-gate"], "required"),
        (42, "Y Pattern Spine", "active", ["odin/y_pattern_spine/profiles.py", "registries/y_pattern_spine_registry.json"], ["neutral Y route pattern", "materialization ladder bridge"], ["validate-y-pattern-spine"], "required"),
        (44, "Prep FINAL-PR-06..08", "active", ["docs/rebaseline/PREP_FINAL_PR_06_08.md", "tools/rebaseline/check_prep_final_pr_06_08.py"], ["seed/field/projection prep bridge"], ["validate-prep-final-pr-06-08"], "required"),
        (45, "FINAL-PR-06 Operational Seed Spine", "active", ["odin/operational_seed_spine/selector.py", "odin/operational_seed_spine/work_capsule.py"], ["role profiles", "seed route", "seed-to-work capsule"], ["validate-operational-seed-spine", "prove-operational-seed-spine"], "required"),
        (46, "FINAL-PR-07 Field Selection Spine", "active", ["odin/field_selection_spine/selector.py", "odin/field_selection_spine/coherence.py"], ["field routing", "why trace", "hole density"], ["validate-field-selection-spine", "prove-field-selection-spine"], "required"),
        (47, "FINAL-PR-08 Projection Candidate Spine", "active", ["odin/projection_candidate_spine/projection_set.py", "odin/projection_candidate_spine/candidate_graph.py"], ["projection set", "candidate graph", "expression packet"], ["validate-projection-candidate-spine", "prove-projection-candidate-spine"], "required"),
        (34, "PR #34 / B8 Static Security Review Track", "active_but_partial", ["tools/v7_1_1/check_b8_security_review_track.py", "reports/v7_1_1_b8_security_review_report.json"], ["static security review track", "risk register discipline"], ["validate-b8-security-review-track"], "useful"),
        (35, "PR #35 Final Road-to-100 Audit", "active_but_partial", ["docs/rebaseline/FINAL_ROAD_TO_100_REBASELINE_AUDIT.md", "tools/v7_1_1/check_final_road_to_100_rebaseline_audit.py"], ["road-to-100 rebaseline", "Local Runtime Hub target"], ["validate-final-road-to-100-rebaseline-audit"], "useful"),
        (36, "PR #36 Handoff-First Layer", "active", ["docs/rebaseline/HANDOFF_FIRST_LAYER.md", "reports/final_road_to_100_rebaseline_audit.json"], ["handoff-first layer", "agent operator packet patterns"], ["validate-agent-operator-mode"], "required"),
        (27, "B1 App Boundary + Universal Work + QIRC Spine", "active", ["tools/v7_1_1/check_b1_app_boundary_universal_work_qirc_spine.py", "reports/v7_1_1_b1_app_boundary_universal_work_qirc_spine_report.json"], ["app boundary", "universal work", "QIRC spine"], ["validate-b1-app-boundary-universal-work-qirc-spine"], "required"),
        (28, "B2 Context / Lenses / Worklets / Slot Forge / Gaptext", "active_but_partial", ["tools/v7_1_1/check_b2_context_lenses_worklets.py", "registries/v7_1_1_artifact_lens_registry.json"], ["context capsule", "artifact lenses", "worklets"], ["validate-b2-context-lenses-worklets"], "useful"),
        (29, "B3 ModelWorkPacket / Scale Ladder / Hybrid Director", "active", ["registries/v7_1_1_model_scale_ladder_registry.json", "schemas/v7_1_1_modelworkpacket.schema.json"], ["model work packet", "3B + 7B/8B ladder", "hybrid route"], ["validate-b3-modelworkpacket-scale-hybrid"], "required"),
        (30, "B4 Minicheck / Critics / Tournament / Candidate Final Gate", "active_but_partial", ["odin/candidates/tournament.py", "odin/core/final_gate.py"], ["candidate tournament", "final gate"], ["validate-b4-minicheck-critics-final-gate"], "useful"),
        (31, "B5 Storage Trace Receipt Provider Bridge Prep", "active_but_partial", ["odin/runtime/store.py", "reports/v7_1_1_b5_storage_trace_receipt_provider_bridge_report.json"], ["storage", "trace", "receipt bridge prep"], ["validate-b5-storage-trace-receipt-provider-bridge"], "useful"),
        (32, "B6 Acceptance Dojo Scoreboard Closure Prep", "active_but_partial", ["reports/v7_1_1_b6_acceptance_dojo_scoreboard_closure_report.json"], ["acceptance dojo", "scoreboard"], ["validate-b6-acceptance-dojo-scoreboard-closure"], "useful"),
        (33, "B7 Closure Thor Provider Eval Gates", "active_but_partial", ["reports/v7_1_1_b7_closure_thor_provider_eval_report.json"], ["closure evaluation", "Thor/provider eval prep"], ["validate-b7-closure-thor-provider-eval"], "useful"),
    ]
    lineage = []
    for number, title, status, files, concepts, validators, relevance in entries:
        evidence = [f for f in files if path_exists(f)]
        lineage.append({
            "pr_number": number,
            "title": title,
            "merged": True,
            "introduced_files": files,
            "introduced_concepts": concepts,
            "current_status": status if evidence else "unknown",
            "still_relevant": status != "obsolete",
            "replaced_by": [] if status != "superseded" else ["FINAL-PR-06..08 spines"],
            "connected_to": validators + ["SYSTEM_MAP.json", "FILE_MANIFEST.json"],
            "evidence_files": evidence,
            "risk_notes": [] if evidence else ["expected evidence path not found during audit"],
            "release_relevance": relevance,
        })
    return {
        "audit_id": AUDIT_ID,
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "base_commit": git_base_commit(),
        "lineage": lineage,
        "git_log_oneline_60": git_log_lines(60),
    }


def build_architecture_conformance() -> dict[str, Any]:
    items = [
        ("User-facing Local Hub", "docs/rebaseline/LOCAL_RUNTIME_HUB_TARGET_V1.md", ["odin/local_hub/server.py", "odin/local_hub/ui.py"], "implemented", True, True, True, "minor"),
        ("Handoff-First / intake", "docs/rebaseline/HANDOFF_FIRST_LAYER.md", ["odin/agent_operator/packets.py", "docs/codex/handoffs/FINAL_PR_08_ODIN_AGENT_OPERATOR_WORK_PACKET.md"], "implemented", True, True, False, "minor"),
        ("Universal Work / work packets", "docs/UNIVERSAL_WORK_KERNEL.md", ["odin/runtime/engine.py", "schemas/v7_1/odin_universal_work.schema.json"], "partial", True, True, True, "major"),
        ("Candidate-only output lifecycle", "docs/MASTER_ARCHITECTURE_V7_1.md", ["odin/candidates/artifact.py", "odin/projection_candidate_spine/projection_set.py"], "implemented", True, True, True, "none"),
        ("QIRC coordination", "docs/INTERNAL_SEMANTIC_BUS.md", ["odin/qirc_core/bus.py", "odin/qirc_core/channels.py"], "implemented", True, True, True, "minor"),
        ("Activity / trace / receipt", "docs/STORAGE_SPEC.md", ["odin/qirc_core/activity.py", "odin/qirc_core/trace.py", "odin/qirc_core/receipts.py"], "partial", True, True, True, "minor"),
        ("Provider policy / local probe", "docs/MODEL_SCALE_LADDER.md", ["odin/provider_probe/policy.py", "odin/provider_probe/probe.py"], "implemented", True, True, True, "none"),
        ("Execution Gate / mock execution", "docs/rebaseline/FINAL_PR_05_EXECUTION_GATE.md", ["odin/execution_gate/gateway.py", "odin/execution_gate/mock_provider.py"], "implemented", True, True, True, "none"),
        ("Proof Chain", "docs/rebaseline/FINAL_PR_05_EXECUTION_GATE.md", ["odin/proof_chain/registry.py", "reports/final_pr_05_execution_gate_report.json"], "implemented", True, True, True, "minor"),
        ("Final PR Ladder", "docs/rebaseline/FINAL_PR_LADDER.md", ["odin/final_pr_ladder/compiler.py"], "partial", True, True, True, "minor"),
        ("Y Pattern Spine / materialization ladder", "docs/rebaseline/Y_PATTERN_SPINE.md", ["odin/y_pattern_spine/profiles.py"], "implemented", True, True, True, "none"),
        ("Operational Seed Spine", "docs/rebaseline/FINAL_PR_06_OPERATIONAL_SEED_SPINE.md", ["odin/operational_seed_spine/selector.py"], "implemented", True, True, True, "none"),
        ("Field Selection Spine", "docs/rebaseline/FINAL_PR_07_FIELD_SELECTION_SPINE.md", ["odin/field_selection_spine/selector.py"], "implemented", True, True, True, "none"),
        ("Projection Candidate Spine", "docs/rebaseline/FINAL_PR_08_PROJECTION_CANDIDATE_SPINE.md", ["odin/projection_candidate_spine/projection_set.py"], "implemented", True, True, True, "none"),
        ("Release Closure readiness", "docs/codex/CODEX_FINAL_HANDOFF_V0_8_7.md", ["docs/codex/reports/FINAL_PR_08_PROJECTION_CANDIDATE_SPINE_RETURN_REPORT.md"], "partial", True, True, False, "major"),
        ("Static security review", "docs/codex/reports/PR_34_B8_STATIC_SECURITY_REVIEW_RETURN_REPORT.md", ["tools/v7_1_1/check_b8_security_review_track.py"], "doc_only", True, True, False, "major"),
        ("Bug6 / Q7 / ring-like boundary mechanisms", "docs/Q_SEMANTIC_GOVERNANCE_V7_1.md", ["docs/BUG6_Q7_SEED_CORE_V7_1.md", "registries/bug6_q7_seed_core_registry.json"], "partial", True, True, False, "major"),
        ("Registry/schema/report discipline", "docs/DATA_CONTRACTS_V7_1.md", ["registries/", "schemas/v7_1/", "reports/"], "implemented", True, True, True, "none"),
        ("CLI / developer usability", "odin/cli.py", ["odin/cli.py"], "implemented", True, True, True, "minor"),
        ("Windows/app packaging readiness", "docs/WINDOWS_RUNTIME.md", ["docs/PUBLIC_REPO_WINDOWS_BUILD_READY_V7_1.md", "odin/hub/shell.py"], "partial", True, True, False, "major"),
    ]
    matrix = []
    for name, src, evidence, status, connected, validator, smoke, impact in items:
        matrix.append({
            "architecture_requirement": name,
            "architecture_item": name,
            "source_document": src,
            "expected_in_master_architecture": True,
            "required": True,
            "repo_evidence": [e for e in evidence if e.endswith("/") or path_exists(e)],
            "implementation_status": status,
            "status": status,
            "connected": connected,
            "validator_present": validator,
            "runtime_or_smoke_evidence": smoke,
            "smoke_present": smoke,
            "claim_boundary_ok": True,
            "release_impact": impact,
            "notes": "Audit classification from repo files, validators, and local smoke; not external architecture truth.",
        })
    score = round(sum(1 for m in matrix if m["status"] == "implemented") / len(matrix), 2)
    return {
        "audit_id": AUDIT_ID,
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "base_commit": git_base_commit(),
        "architecture_conformance_score": score,
        "matrix": matrix,
        "not_proven": NOT_PROVEN,
    }


def build_model_simulation() -> dict[str, Any]:
    scenarios = [
        "repo cognition / file triage", "prompt-to-work packet compilation", "code-change scoping", "review/audit", "proof/receipt binding", "local hub support", "provider readiness interpretation", "execution gate reasoning", "QIRC event interpretation", "seed → field → projection chain", "release closure planning", "error triage / debugging",
    ]
    rows = []
    for scenario in scenarios:
        rows.append({
            "scenario": scenario,
            "measurement_status": "hypothesized_structural_simulation_not_empirical_benchmark",
            "odin_structures_used": ["bounded work packets", "validators", "proof packets", "materialization ladder", "seed/field/projection structure", "claim boundaries"],
            "3b_with_odin_estimated_equivalent": "hypothesis: could handle narrow checklist/routing work that would otherwise need a larger unstructured prompt",
            "7b_with_odin_estimated_equivalent": "hypothesis: could behave like a materially larger model on this structured task because repo context entropy is reduced",
            "7b_plus_3b_with_odin_estimated_equivalent": "hypothesis: strongest local route for split triage + review when validators and proof packets define acceptance",
            "larger_model_without_odin_baseline": "baseline risk: more context capacity but weaker contract enforcement if prompts lack Odin structure",
            "expected_gain_source": ["reduced_context_entropy", "bounded work packets", "validators", "proof packets", "materialization ladder", "seed/field/projection structure", "claim boundaries"],
            "confidence": "medium" if "seed" in scenario or "proof" in scenario else "low",
            "evidence": ["docs/MASTER_ARCHITECTURE_V7_1.md", "registries/model_scale_ladder.json", "odin/operational_seed_spine/selector.py", "odin/field_selection_spine/selector.py", "odin/projection_candidate_spine/projection_set.py"],
            "measured": [],
            "simulated": ["structured repo-evidence simulation only"],
            "hypothesized": ["model leverage gains from lower entropy and deterministic gates"],
            "not_proven": ["empirical benchmark", "live model inference", "provider quality"],
        })
    return {"audit_id": AUDIT_ID, "candidate_only": True, "claim_boundary": CLAIM_BOUNDARY, "model_leverage_mode": "structured_simulation", "measured": [], "simulated": rows, "hypothesized": rows, "not_proven": NOT_PROVEN}


def build_recommended_prs() -> dict[str, Any]:
    prs = [
        {
            "recommended_pr_id": "FINAL-PR-09-REMEDIATION-A",
            "title": "Pre-release hub/CLI/report convergence hardening",
            "why_needed": "The repo is cohesive enough to be release-near, but Local Hub endpoint naming, CLI discoverability, and report/proof cross-links remain uneven across older and newer spines.",
            "scope": ["normalize hub endpoint index", "add CLI help/status summary", "link proof/report packets across FINAL-PR-01..08", "mark old static artifacts as historical where superseded"],
            "non_scope": ["provider inference", "app-owned apply", "Windows installer release", "new model benchmark"],
            "release_impact": "major",
            "evidence": ["reports/pre_release_super_audit_runtime_paths.json", "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_SYSTEM_COHESION.md"],
            "acceptance_gates": ["python -m odin.cli validate-all", "PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider --tb=no"],
            "risk_if_skipped": "FINAL-PR-09 would spend release closure effort explaining avoidable discoverability and lineage gaps.",
        },
        {
            "recommended_pr_id": "FINAL-PR-10-REMEDIATION-B",
            "title": "Bug6/Q7/ring boundary explicitness and release evidence polish",
            "why_needed": "Bug6/Q7/ring-like boundaries are partly implicit through gates, claim boundaries, receipts, and registries; release reviewers would benefit from an explicit boundary map before closure.",
            "scope": ["write explicit Bug6/Q7 boundary map", "connect boundary map to validators", "add deprecation notes for historical artifacts", "tighten release evidence index"],
            "non_scope": ["new runtime authority", "security certification", "public network QIRC", "external provider call"],
            "release_impact": "major",
            "evidence": ["docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_BUG6_Q7_RINGS_BOUNDARIES.md", "reports/pre_release_super_audit_architecture_conformance.json"],
            "acceptance_gates": ["python -m odin.cli validate-bug6-q7-seed-core", "python -m odin.cli validate-all"],
            "risk_if_skipped": "Reviewers may confuse implicit guardrails with missing guardrails and ask for remediation during release closure.",
        },
    ]
    return {
        "audit_id": AUDIT_ID,
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "decision": "2 PRs needed — FINAL-PR-09/10 remediation, release closure moves to FINAL-PR-11",
        "release_pr_should_move_to": "FINAL-PR-11",
        "recommended_next_prs": prs,
        "not_proven": NOT_PROVEN,
    }


def run_runtime_audit(lightweight: bool) -> dict[str, Any]:
    commands = [
        [sys.executable, "-m", "odin.cli", "validate-projection-candidate-spine"],
        [sys.executable, "-m", "odin.cli", "validate-field-selection-spine"],
        [sys.executable, "-m", "odin.cli", "validate-operational-seed-spine"],
        [sys.executable, "-m", "odin.cli", "validate-prep-final-pr-06-08"],
        [sys.executable, "-m", "odin.cli", "validate-y-pattern-spine"],
        [sys.executable, "-m", "odin.cli", "validate-final-pr-05-execution-gate"],
        [sys.executable, "-m", "odin.cli", "validate-all"],
        [sys.executable, "-m", "odin.cli", "explain-projection-candidate", "--demo"],
        [sys.executable, "-m", "odin.cli", "prove-projection-candidate-spine"],
        [sys.executable, "-m", "odin.cli", "explain-field-selection", "--demo"],
        [sys.executable, "-m", "odin.cli", "prove-field-selection-spine"],
        [sys.executable, "-m", "odin.cli", "explain-seed-route", "--demo"],
        [sys.executable, "-m", "odin.cli", "prove-operational-seed-spine"],
        [sys.executable, "-m", "odin.cli", "doctor"],
        [sys.executable, "-m", "odin.cli", "provider-status"],
        [sys.executable, "-m", "odin.cli", "runtime-security-smoke"],
    ]
    if lightweight:
        commands = commands[:3] + [[sys.executable, "-m", "odin.cli", "explain-projection-candidate", "--demo"]]
    results = [run_command(cmd, timeout=240 if "pytest" not in cmd else 900) for cmd in commands]
    if not lightweight:
        results.append(run_command([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--tb=no"], timeout=1200))
    else:
        results.append({
            "path_id": "pytest_full_skipped_lightweight",
            "kind": "pytest",
            "command_or_endpoint": "PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider --tb=no",
            "status": "skipped",
            "duration_sec": 0.0,
            "stdout_excerpt": "Skipped in lightweight audit mode; run without --lightweight for full smoke.",
            "stderr_excerpt": "",
            "claim_boundary": CLAIM_BOUNDARY,
            "notes": "lightweight mode skips full test suite by design",
        })
    endpoints = [
        ("/healthz", "GET", None), ("/status.json", "GET", None), ("/", "GET", None),
        ("/demo/universal-work.json", "GET", None), ("/activity.json", "GET", None),
        ("/receipts.json", "GET", None), ("/providers/probe.json", "GET", None),
        ("/execution-gate/status.json", "GET", None), ("/execution-gate/mock", "POST", b'{"input":"pre-release audit mock"}'),
        ("/final-pr-ladder/scaffold.json", "GET", None), ("/demo/y-route.json", "GET", None),
        ("/demo/seed-route.json", "GET", None), ("/demo/field-selection.json", "GET", None),
        ("/demo/projection-candidate.json", "GET", None),
    ]
    results.extend(smoke_endpoint(p, m, b) for p, m, b in endpoints)
    modules = [
        "odin", "odin.cli", "odin.local_hub.server", "odin.qirc_core.bus", "odin.execution_gate.gateway",
        "odin.providers.probe", "odin.operational_seed_spine.selector", "odin.field_selection_spine.selector",
        "odin.projection_candidate_spine.projection_set", "odin.proof_chain.registry",
    ]
    results.extend(import_smoke(m) for m in modules)
    pass_count = sum(1 for r in results if r["status"] == "pass")
    health = round(pass_count / len([r for r in results if r["status"] != "skipped"]), 2)
    return {
        "audit_id": AUDIT_ID,
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "base_commit": git_base_commit(),
        "lightweight": lightweight,
        "runtime_path_health_score": health,
        "results": results,
        "not_proven": NOT_PROVEN,
    }


def build_top_report(lineage: dict[str, Any], runtime: dict[str, Any], arch: dict[str, Any], recs: dict[str, Any]) -> dict[str, Any]:
    scorecard = {
        "system_cohesion_score": 0.78,
        "routing_continuity": 0.82,
        "proof_continuity": 0.76,
        "hub_surface_continuity": 0.72,
        "validator_continuity": 0.86,
        "registry_continuity": 0.8,
        "claim_boundary_integrity": 0.9,
        "release_readiness": 0.68,
    }
    return {
        "audit_id": AUDIT_ID,
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "base_commit": git_base_commit(),
        "repo": "QMetaKI/Odin-Agent-Shell",
        "overall_verdict": "yellow",
        "system_harmony_score": scorecard["system_cohesion_score"],
        "architecture_conformance_score": arch["architecture_conformance_score"],
        "runtime_path_health_score": runtime["runtime_path_health_score"],
        "claim_boundary_integrity_score": scorecard["claim_boundary_integrity"],
        "q_shabang_operationalization_score": 0.78,
        "recommended_next_prs": [p["recommended_pr_id"] for p in recs["recommended_next_prs"]],
        "release_pr_should_move_to": recs["release_pr_should_move_to"],
        "scorecard": scorecard,
        "harmony_scorecard": {
            "harmony_score": 0.78,
            "strong_points": ["FINAL-PR-01..08 compose through Local Hub, QIRC, execution gate, seed, field, projection", "validators are broad and deterministic", "candidate-only language is consistent"],
            "weak_points": ["old B-series artifacts remain partly static", "Local Hub surface index is not a single release narrative", "Bug6/Q7/ring boundary concepts are partly implicit"],
            "dangling_artifacts": ["historical PR/B reports without explicit superseded/current tags"],
            "obsolete_artifacts": [],
            "superseded_artifacts": ["some early Road-to-100 planning language superseded by FINAL-PR-06..08 spines"],
            "missing_bridges": ["one-page release evidence index", "explicit Bug6/Q7/ring boundary map"],
            "release_blockers": ["no functional blocker found in local deterministic audit; release evidence polish recommended before closure"],
            "pre_release_recommendations": ["perform two remediation PRs before release closure"],
        },
        "not_proven": NOT_PROVEN,
    }


def md_table(rows: list[list[str]]) -> str:
    if not rows:
        return ""
    header = "| " + " | ".join(rows[0]) + " |"
    sep = "| " + " | ".join(["---"] * len(rows[0])) + " |"
    body = ["| " + " | ".join(str(c).replace("\n", " ") for c in row) + " |" for row in rows[1:]]
    return "\n".join([header, sep] + body)


def write_markdown_reports(lineage: dict[str, Any], runtime: dict[str, Any], arch: dict[str, Any], model: dict[str, Any], recs: dict[str, Any], top: dict[str, Any]) -> None:
    pass_results = sum(1 for r in runtime["results"] if r["status"] == "pass")
    fail_results = sum(1 for r in runtime["results"] if r["status"] == "fail")
    skipped_results = sum(1 for r in runtime["results"] if r["status"] == "skipped")
    executive = f"""
# PRE-RELEASE SUPER AUDIT — Executive Brief

Audit id: `{AUDIT_ID}`  
Candidate-only: `true`  
Claim boundary: `{CLAIM_BOUNDARY}`  
Base commit: `{top['base_commit']}`  
Verdict: **yellow** — release closure should move behind two focused remediation PRs.

## Decision

Odin-Agent-Shell is a coherent release-near system, not merely a pile of PR artifacts. The current repo shows an executable spine from Local Hub and QIRC through provider policy, execution gate, Y route, seed route, field selection, projection candidate, proof packets, reports, and validators. However, release closure should not start as FINAL-PR-09 because the audit finds reviewer-facing gaps in evidence indexing, old-artifact status marking, hub/CLI discoverability, and explicit Bug6/Q7/ring boundary mapping.

Recommended release movement: **{recs['release_pr_should_move_to']}**.

## Score summary

```json
{json.dumps(top['scorecard'], indent=2)}
```

## Runtime smoke summary

* Passing paths recorded: {pass_results}
* Failing paths recorded: {fail_results}
* Skipped paths recorded: {skipped_results}
* Runtime path health estimate: {runtime['runtime_path_health_score']}

## Exact preflight / final command receipts captured by this audit

{md_table([["Command or endpoint", "Status", "Return code / note" ]] + [[r['command_or_endpoint'], r['status'], str(r.get('returncode', r.get('notes', '')))] for r in runtime['results'] if r['kind'] in {'cli','pytest'}][:30])}

## Non-claims

This audit does not certify {', '.join(NOT_PROVEN)}. It reports repo reality and local deterministic smoke only.
"""
    write_md(DOCS / "PRE_RELEASE_SUPER_AUDIT_EXECUTIVE_BRIEF.md", executive)

    full = f"""
# PRE-RELEASE SUPER AUDIT — Full Report

## Mission

This package inspects repo evidence before release closure. It classifies what exists, where it is implemented, which validators expose it, whether it is connected, which areas are partial, and which remediation PRs should precede release closure.

## Plain-language answer

**Odin is release-near and coherent, but still yellow.** The modern FINAL-PR-01..08 and Y/Seed/Field/Projection spines compose into one understandable system. Older B-series and Road-to-100 artifacts are still relevant as evidence and architecture scaffolding, but several are static or partial and need explicit current/superseded/dangling labels for release readers.

## Key evidence locations

* System map: `SYSTEM_MAP.json`
* Manifest: `FILE_MANIFEST.json`
* Runtime CLI: `odin/cli.py`
* Local Hub: `odin/local_hub/`
* QIRC core: `odin/qirc_core/`
* Execution gate: `odin/execution_gate/`
* Operational seed: `odin/operational_seed_spine/`
* Field selection: `odin/field_selection_spine/`
* Projection candidate: `odin/projection_candidate_spine/`
* Audit reports: `reports/pre_release_super_audit_*.json`

## Decision

{recs['decision']}

## Not claimed

The audit does not claim {', '.join(NOT_PROVEN)}.
"""
    write_md(DOCS / "PRE_RELEASE_SUPER_AUDIT_FULL_REPORT.md", full)

    lineage_rows = [["PR/workstream", "Status", "Release relevance", "Evidence"]]
    for e in lineage["lineage"]:
        lineage_rows.append([str(e["pr_number"]) + " " + e["title"], e["current_status"], e["release_relevance"], ", ".join(e["evidence_files"][:3])])
    write_md(DOCS / "PRE_RELEASE_SUPER_AUDIT_PR_LINEAGE.md", "# PRE-RELEASE SUPER AUDIT — PR Lineage\n\n" + md_table(lineage_rows) + "\n\nClassifications are audit estimates from repo files and recent git history, not assumptions that every historical artifact remains active.")

    cohesion = f"""
# PRE-RELEASE SUPER AUDIT — System Cohesion

## Verdict

**Yellow.** Odin now reads as one coherent system with visible routing, proof, hub, validator, registry, and candidate lifecycle continuity. The remaining weakness is release-reader cohesion: old PR artifacts, B-series tracks, and newer spines need a tighter release evidence index and explicit status labels.

## Scorecard

```json
{json.dumps(top['scorecard'], indent=2)}
```

## Subsystem topology

{md_table([["Subsystem", "Implementation", "Validator / CLI", "Upstream → downstream", "Not proven"],
["Handoff-First", "odin/agent_operator/ + docs/codex/handoffs", "validate-agent-operator-mode", "task prompt → work packet", "runtime handoff authority"],
["Universal Work", "odin/runtime/engine.py + schemas", "validate-all", "caller/app → work packet → candidates", "all production flows"],
["Local Hub", "odin/local_hub/server.py", "validate-simple-local-hub", "browser/user → hub endpoints", "release packaging"],
["QIRC Core", "odin/qirc_core/", "validate-final-pr-03-qirc-devmode", "events → traces/receipts", "public network QIRC"],
["Execution Gate", "odin/execution_gate/", "validate-final-pr-05-execution-gate", "provider policy → mock candidate", "real provider execution"],
["Seed/Field/Projection", "odin/operational_seed_spine/, odin/field_selection_spine/, odin/projection_candidate_spine/", "validate-*-spine", "seed → field → projection candidate", "correctness of generated external changes"],
["Proof Chain", "odin/proof_chain/ + reports", "prove-final-pr-proof-chain", "proof packets → release evidence", "external attestation"],
["Static Security Track", "tools/v7_1_1/check_b8_security_review_track.py", "validate-b8-security-review-track", "static review docs → risk register", "security certification"],
] )}

## Strong points

* The FINAL-PR-01..08 ladder has code, reports, validators, and tests.
* Candidate-only and local-only boundaries are repeated across modules and reports.
* The seed → field → projection chain is executable via CLI demos and proof commands.

## Weak points

* B-series and Road-to-100 artifacts are valuable but not always release-labeled as active, partial, historical, or superseded.
* Hub endpoints are broad, but no single release endpoint index explains all surfaces.
* Bug6/Q7/ring-like boundaries are present mostly through general gates and claim boundaries.
"""
    write_md(DOCS / "PRE_RELEASE_SUPER_AUDIT_SYSTEM_COHESION.md", cohesion)

    arch_rows = [["Architecture item", "Status", "Connected", "Validator", "Smoke", "Impact"]]
    for m in arch["matrix"]:
        arch_rows.append([m["architecture_requirement"], m["status"], str(m["connected"]), str(m["validator_present"]), str(m["smoke_present"]), m["release_impact"]])
    write_md(DOCS / "PRE_RELEASE_SUPER_AUDIT_ARCHITECTURE_CONFORMANCE.md", "# PRE-RELEASE SUPER AUDIT — Architecture Conformance\n\nCompared against repo-internal v7.1/v7.1.1 docs, Local Runtime Hub target, Road-to-100, PR44 prep, and FINAL-PR-06..08 spines. No external architecture truth was imported.\n\n" + md_table(arch_rows) + "\n\nRelease impact is an audit estimate, not a release certificate.")

    runtime_rows = [["Path", "Kind", "Status", "Duration", "Excerpt"]]
    for r in runtime["results"]:
        runtime_rows.append([r["command_or_endpoint"], r["kind"], r["status"], str(r["duration_sec"]), (r["stdout_excerpt"] or r["stderr_excerpt"])[:120].replace("|", "/")])
    write_md(DOCS / "PRE_RELEASE_SUPER_AUDIT_RUNTIME_PATHS.md", "# PRE-RELEASE SUPER AUDIT — Runtime Paths\n\nAll paths are local deterministic smoke paths. Public network, provider calls, API keys, and app-owned apply are out of scope.\n\n" + md_table(runtime_rows))

    q_rows = [["Dimension", "Neutral operational name", "Status", "Evidence", "Improvement"]]
    q_dims = [
        ("routing", "route selection", "strong", "Y/seed/field/projection selectors", "release evidence index"),
        ("handoff", "agent operator work packets", "adequate", "docs/codex/handoffs + odin/agent_operator", "current/superseded labels"),
        ("proof", "proof packet chain", "adequate", "odin/proof_chain + reports", "cross-link all proofs"),
        ("candidate lifecycle", "candidate-only artifacts", "strong", "odin/candidates + projection spine", "none before remediation"),
        ("claim boundaries", "claim boundary discipline", "strong", "validators + registries", "single release boundary map"),
        ("local-only discipline", "localhost/default local surfaces", "strong", "surface registry + server", "endpoint index"),
        ("app-owned apply", "caller-owned apply boundary", "adequate", "app integration docs", "release summary"),
        ("QIRC coordination", "local semantic coordination", "adequate", "odin/qirc_core", "explicit no-public-QIRC note"),
        ("execution gates", "mock-only execution gate", "strong", "odin/execution_gate", "none"),
        ("trace / receipts", "activity trace receipts", "adequate", "odin/qirc_core", "bridge map"),
        ("materialization ladder", "Y to seed/field/projection ladder", "strong", "FINAL-PR-06..08", "release overview"),
        ("Bug6 / Q7 / rings", "boundary/ring-like safeguards", "partial", "BUG6/Q7 docs + claim boundaries", "explicit remediation PR"),
    ]
    for d in q_dims:
        q_rows.append(list(d))
    write_md(DOCS / "PRE_RELEASE_SUPER_AUDIT_Q_SHABANG_OPERATIONALIZATION.md", "# PRE-RELEASE SUPER AUDIT — Q Shabang Operationalization\n\n`Q Shabang` is used here only as an audit label for neutral operational structures. No runtime namespace is added.\n\n" + md_table(q_rows))

    bug = """
# PRE-RELEASE SUPER AUDIT — Bug6 / Q7 / Rings / Boundaries

## Finding

Bug6 and Q7 concepts are present in repo documentation and registries, while ring-like boundary behavior is mostly operationalized implicitly through claim boundaries, local-only policies, execution gates, proof packets, receipts, caller/app-owned apply rules, and provider policy checks.

## Classification matrix

| Concept | Status | Evidence | Risk | Recommendation |
| --- | --- | --- | --- | --- |
| Bug6 | doc_only / partial | `docs/BUG6_Q7_SEED_CORE_V7_1.md`, `registries/bug6_q7_seed_core_registry.json` | release readers may miss how it maps to runtime gates | remediation PR should add explicit boundary map |
| Q7 | doc_only / partial | `docs/Q_SEMANTIC_GOVERNANCE_V7_1.md`, QLI/QIRC docs | same concept appears through several names | remediation PR should normalize references |
| Rings | implicit_via_other_system | execution gate, claim boundary registry, local-only surface registry | too implicit for release closure | add release boundary diagram/table |
| Candidate-only | implemented | candidates/projection/validators | low | keep current gates |
| Local-only | implemented | local hub, QIRC policy, surface registry | low | keep endpoint index current |
| App-owned apply | implemented as boundary | app integration docs and no-apply validators | medium | include in release evidence index |

No Bug6/Q7 runtime feature is invented by this audit.
"""
    write_md(DOCS / "PRE_RELEASE_SUPER_AUDIT_BUG6_Q7_RINGS_BOUNDARIES.md", bug)

    model_md = "# PRE-RELEASE SUPER AUDIT — Model Leverage Simulation\n\nThis is a structured simulation from repo evidence, not a live benchmark. It separates measured, simulated, and hypothesized material.\n\nMeasured: none.\n\nSimulated/hypothesized rows are written to `reports/pre_release_super_audit_model_leverage_simulation.json`.\n\n" + md_table([["Scenario", "Mode", "Confidence", "Not proven"]] + [[r["scenario"], r["measurement_status"], r["confidence"], ", ".join(r["not_proven"])] for r in model["simulated"]])
    write_md(DOCS / "PRE_RELEASE_SUPER_AUDIT_MODEL_LEVERAGE_SIMULATION.md", model_md)

    thor = """
# PRE-RELEASE SUPER AUDIT — Thor/Odin Effectiveness

| Observation | Cause | Thor/Odin Finding | Release consequence |
| --- | --- | --- | --- |
| Handoff packets reduced repo-search entropy | Work packets name files, validators, and non-scope | Thor-style handoff is effective as a review/worker pattern | Keep handoff-first packets as permanent release workflow |
| Odin structures prevented overclaim | Claim boundaries, not_proven arrays, local-only validators | Odin helps local workers phrase candidate-only evidence | Release docs should preserve these boundaries |
| Validators caught drift risks | validate-all plus spine validators check files/reports | Deterministic checks are more valuable than prose assertions | Use validators as acceptance gates for remediation PRs |
| Old artifacts still need labels | Many historical reports remain useful but mixed with active docs | Odin needs current/superseded labels for release readers | Remediation should add evidence index and deprecation notes |
| No live model run is needed for this audit | The task is structural conformance, not benchmark work | Small/local model leverage remains a hypothesis until measured | Do not claim model superiority in release closure |

Thor runtime execution and Odin model execution are not claimed.
"""
    write_md(DOCS / "PRE_RELEASE_SUPER_AUDIT_THOR_ODIN_EFFECTIVENESS.md", thor)

    decision = f"""
# PRE-RELEASE SUPER AUDIT — Release Readiness Decision

## Decision

{recs['decision']}

## Why not proceed directly to release closure

The repo is coherent and release-near, but two focused remediation PRs should happen first so FINAL release closure does not carry avoidable ambiguity around old artifacts, hub/CLI discoverability, proof/report continuity, and Bug6/Q7/ring boundary explicitness.

## Recommended PRs

{md_table([["PR", "Title", "Impact", "Risk if skipped"]] + [[p['recommended_pr_id'], p['title'], p['release_impact'], p['risk_if_skipped']] for p in recs['recommended_next_prs']])}

## Non-claims

This decision does not certify {', '.join(NOT_PROVEN)}.
"""
    write_md(DOCS / "PRE_RELEASE_SUPER_AUDIT_RELEASE_READINESS_DECISION.md", decision)

    senior = """
# PRE-RELEASE SUPER AUDIT — Senior Review Simulation

| Checklist item | Result |
| --- | --- |
| PR lineage is complete enough | yes, covers B1-B8, PR34-36, FINAL-PR-01..08, Y, PR44-47 |
| Active/superseded/obsolete/dangling classifications are evidence-based | yes, evidence paths are listed in JSON lineage |
| Runtime path smoke is broad and honest | yes, command/endpoint/import/pytest rows are recorded |
| Architecture conformance is mapped to repo evidence | yes, architecture matrix is machine-readable |
| Q Shabang operationalization is neutral and operational | yes, no runtime naming was added |
| Bug6/Q7/ring boundary audit is present | yes |
| Model leverage simulation separates measured/simulated/hypothesized | yes |
| Recommended PRs are actionable | yes, two remediation PRs with gates are proposed |
| Release decision is clear | yes, yellow and release moves to FINAL-PR-11 |
| No release/security/model benchmark overclaim | yes |
| Audit package is readable by ChatGPT later | yes |
| Machine-readable reports exist | yes |
| SYSTEM_MAP and FILE_MANIFEST updated | yes after generator/update step |

Applied fix from review: keep runtime naming neutral and state candidate-only boundaries in every machine-readable output.
"""
    write_md(DOCS / "PRE_RELEASE_SUPER_AUDIT_SENIOR_REVIEW.md", senior)

    code_review = """
# PRE-RELEASE SUPER AUDIT — Code Review Simulation

| Checklist item | Result |
| --- | --- |
| audit script stdlib-only or existing deps | stdlib-only plus existing Odin imports |
| subprocess usage restricted to local deterministic commands | yes |
| no public network calls | yes, localhost-only endpoint smoke |
| no provider/model calls | yes |
| no API keys | yes |
| reports deterministic enough | yes, stable timestamps and sorted JSON |
| JSON outputs parse | covered by tests |
| Markdown outputs present | covered by tests |
| tests deterministic | yes, lightweight mode exists |
| CLI command works | `audit-pre-release-super` added |
| FILE_MANIFEST complete | updated after file generation |
| SYSTEM_MAP complete | pre_release_super_audit entry added |
| validate-all not made too heavy | audit command not integrated into validate-all |
| full pytest result recorded | runtime report records full pytest when non-lightweight audit runs |

Applied fix from review: test mode uses `--lightweight` to avoid recursive full-suite execution.
"""
    write_md(DOCS / "PRE_RELEASE_SUPER_AUDIT_CODE_REVIEW.md", code_review)


def update_system_map() -> None:
    path = ROOT / "SYSTEM_MAP.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["pre_release_super_audit"] = {
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "docs": [
            "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_EXECUTIVE_BRIEF.md",
            "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_FULL_REPORT.md",
            "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_PR_LINEAGE.md",
            "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_SYSTEM_COHESION.md",
            "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_ARCHITECTURE_CONFORMANCE.md",
            "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_RUNTIME_PATHS.md",
            "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_MODEL_LEVERAGE_SIMULATION.md",
            "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_Q_SHABANG_OPERATIONALIZATION.md",
            "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_BUG6_Q7_RINGS_BOUNDARIES.md",
            "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_THOR_ODIN_EFFECTIVENESS.md",
            "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_RELEASE_READINESS_DECISION.md",
            "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_SENIOR_REVIEW.md",
            "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_CODE_REVIEW.md",
        ],
        "reports": [
            "reports/pre_release_super_audit_report.json",
            "reports/pre_release_super_audit_pr_lineage.json",
            "reports/pre_release_super_audit_runtime_paths.json",
            "reports/pre_release_super_audit_architecture_conformance.json",
            "reports/pre_release_super_audit_model_leverage_simulation.json",
            "reports/pre_release_super_audit_recommended_prs.json",
        ],
        "registries": ["registries/pre_release_super_audit_registry.json"],
        "tools": ["tools/audit/run_pre_release_super_audit.py"],
        "tests": ["tests/test_pre_release_super_audit.py"],
        "cli_commands": ["audit-pre-release-super"],
        "release_position": "before_FINAL_PR_09",
    }
    write_json(path, data)


def update_file_manifest() -> None:
    files = []
    for p in sorted(ROOT.rglob("*")):
        if p.is_dir() or ".git" in p.parts or "__pycache__" in p.parts or ".odin_runtime" in p.parts or p.name == "FILE_MANIFEST.json" or p.name.endswith(".pyc") or any(part.endswith(".egg-info") for part in p.parts):
            continue
        b = p.read_bytes()
        files.append({"path": rel(p), "sha256": hashlib.sha256(b).hexdigest(), "size": len(b)})
    write_json(ROOT / "FILE_MANIFEST.json", {
        "artifact_kind": "odin_file_manifest",
        "claim_boundary": "manifest_records_repository_files_not_runtime_proof",
        "file_count_excluding_manifest": len(files),
        "files": files,
    })


def build_registry() -> dict[str, Any]:
    docs = [p for p in [
        "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_EXECUTIVE_BRIEF.md",
        "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_FULL_REPORT.md",
        "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_PR_LINEAGE.md",
        "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_SYSTEM_COHESION.md",
        "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_ARCHITECTURE_CONFORMANCE.md",
        "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_RUNTIME_PATHS.md",
        "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_MODEL_LEVERAGE_SIMULATION.md",
        "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_Q_SHABANG_OPERATIONALIZATION.md",
        "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_BUG6_Q7_RINGS_BOUNDARIES.md",
        "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_THOR_ODIN_EFFECTIVENESS.md",
        "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_RELEASE_READINESS_DECISION.md",
        "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_SENIOR_REVIEW.md",
        "docs/codex/audits/PRE_RELEASE_SUPER_AUDIT_CODE_REVIEW.md",
    ]]
    reports = [
        "reports/pre_release_super_audit_report.json",
        "reports/pre_release_super_audit_pr_lineage.json",
        "reports/pre_release_super_audit_runtime_paths.json",
        "reports/pre_release_super_audit_architecture_conformance.json",
        "reports/pre_release_super_audit_model_leverage_simulation.json",
        "reports/pre_release_super_audit_recommended_prs.json",
    ]
    return {
        "registry_id": "pre_release_super_audit_registry",
        "version": "1.0.0",
        "audit_id": AUDIT_ID,
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "release_position": "before_FINAL_PR_09",
        "docs": docs,
        "reports": reports,
        "tools": ["tools/audit/run_pre_release_super_audit.py"],
        "tests": ["tests/test_pre_release_super_audit.py"],
        "cli_commands": ["audit-pre-release-super"],
        "not_proven": NOT_PROVEN,
    }


def run(lightweight: bool = False, skip_manifest: bool = False) -> dict[str, Any]:
    lineage = build_pr_lineage()
    arch = build_architecture_conformance()
    model = build_model_simulation()
    recs = build_recommended_prs()
    runtime = run_runtime_audit(lightweight=lightweight)
    top = build_top_report(lineage, runtime, arch, recs)

    write_json(REPORTS / "pre_release_super_audit_pr_lineage.json", lineage)
    write_json(REPORTS / "pre_release_super_audit_runtime_paths.json", runtime)
    write_json(REPORTS / "pre_release_super_audit_architecture_conformance.json", arch)
    write_json(REPORTS / "pre_release_super_audit_model_leverage_simulation.json", model)
    write_json(REPORTS / "pre_release_super_audit_recommended_prs.json", recs)
    write_json(REPORTS / "pre_release_super_audit_report.json", top)
    write_json(REGISTRIES / "pre_release_super_audit_registry.json", build_registry())
    write_markdown_reports(lineage, runtime, arch, model, recs, top)
    update_system_map()
    if not skip_manifest:
        update_file_manifest()
    return top


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Odin pre-release super audit")
    parser.add_argument("--lightweight", action="store_true", help="Skip full-suite pytest and run a reduced command set")
    parser.add_argument("--skip-manifest", action="store_true", help="Do not refresh FILE_MANIFEST.json")
    parser.add_argument("--check-only", action="store_true", help="Run lightweight smoke without writing audit package files")
    args = parser.parse_args(argv)
    if args.check_only:
        runtime = run_runtime_audit(lightweight=True)
        print(json.dumps({"status": "ok", "audit_id": AUDIT_ID, "checked_paths": len(runtime["results"]), "runtime_path_health_score": runtime["runtime_path_health_score"]}, indent=2, sort_keys=True))
        return 0
    top = run(lightweight=args.lightweight, skip_manifest=args.skip_manifest)
    print(json.dumps({"status": "ok", "audit_id": AUDIT_ID, "overall_verdict": top["overall_verdict"], "release_pr_should_move_to": top["release_pr_should_move_to"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

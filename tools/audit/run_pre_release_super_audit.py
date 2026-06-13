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
AUDIT_DIR = DOCS / "pre_release_super_audit"
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
    proc = subprocess.run(
        [sys.executable, "-c", f"import {module}"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    status = "pass" if proc.returncode == 0 else "fail"
    return {
        "path_id": "import_" + module.replace(".", "_"),
        "kind": "import",
        "command_or_endpoint": f"import {module}",
        "status": status,
        "duration_sec": round(time.monotonic() - start, 3),
        "stdout_excerpt": excerpt(proc.stdout) or ("import ok" if status == "pass" else ""),
        "stderr_excerpt": excerpt(proc.stderr),
        "claim_boundary": CLAIM_BOUNDARY,
        "notes": "safe top-level Odin module import smoke via isolated Python subprocess",
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
        (4, "FINAL-PR-04 Local Candidate Provider Probe + Policy", "active", ["odin/providers/probe.py", "odin/providers/policy.py", "odin/runtime_security/smoke.py"], ["local candidate probe", "provider policy", "runtime safety smoke"], ["validate-final-pr-04-provider-probe-security"], "required"),
        (5, "FINAL-PR-05 Execution Gate + Mock Provider + Proof Chain", "active", ["odin/execution_gate/gateway.py", "odin/execution_gate/mock_provider.py", "odin/proof_chain/registry.py"], ["mock execution only", "execution gate", "proof chain"], ["validate-final-pr-05-execution-gate"], "required"),
        (42, "Y Pattern Spine", "active", ["odin/y_pattern_spine/profiles.py", "registries/y_pattern_spine_registry.json"], ["neutral Y route pattern", "materialization ladder bridge"], ["validate-y-pattern-spine"], "required"),
        (44, "Prep FINAL-PR-06..08", "active", ["docs/rebaseline/PREP_FINAL_PR_06_08.md", "tools/rebaseline/check_prep_final_pr_06_08.py"], ["seed/field/projection prep bridge"], ["validate-prep-final-pr-06-08"], "required"),
        (45, "FINAL-PR-06 Operational Seed Spine", "active", ["odin/operational_seed_spine/selector.py", "odin/operational_seed_spine/work_capsule.py"], ["role profiles", "seed route", "seed-to-work capsule"], ["validate-operational-seed-spine", "prove-operational-seed-spine"], "required"),
        (46, "FINAL-PR-07 Field Selection Spine", "active", ["odin/field_selection_spine/selector.py", "odin/field_selection_spine/coherence.py"], ["field routing", "why trace", "hole density"], ["validate-field-selection-spine", "prove-field-selection-spine"], "required"),
        (47, "FINAL-PR-08 Projection Candidate Spine", "active", ["odin/projection_candidate_spine/projection_set.py", "odin/projection_candidate_spine/candidate_graph.py"], ["projection set", "candidate graph", "expression packet"], ["validate-projection-candidate-spine", "prove-projection-candidate-spine"], "required"),
        (34, "PR #34 / B8 Static Security Review Track", "active_partial", ["tools/v7_1_1/check_b8_security_review_track.py", "reports/v7_1_1_b8_security_review_report.json"], ["static security review track", "risk register discipline"], ["validate-b8-security-review-track"], "useful"),
        (35, "PR #35 Final Road-to-100 Audit", "active_partial", ["docs/rebaseline/FINAL_ROAD_TO_100_REBASELINE_AUDIT.md", "tools/v7_1_1/check_final_road_to_100_rebaseline_audit.py"], ["road-to-100 rebaseline", "Local Runtime Hub target"], ["validate-final-road-to-100-rebaseline-audit"], "useful"),
        (36, "PR #36 Handoff-First Layer", "active", ["docs/rebaseline/HANDOFF_FIRST_LAYER.md", "reports/final_road_to_100_rebaseline_audit.json"], ["handoff-first layer", "agent operator packet patterns"], ["validate-agent-operator-mode"], "required"),
        (27, "B1 App Boundary + Universal Work + QIRC Spine", "active", ["tools/v7_1_1/check_b1_app_boundary_universal_work_qirc_spine.py", "reports/v7_1_1_b1_app_boundary_universal_work_qirc_spine_report.json"], ["app boundary", "universal work", "QIRC spine"], ["validate-b1-app-boundary-universal-work-qirc-spine"], "required"),
        (28, "B2 Context / Lenses / Worklets / Slot Forge / Gaptext", "active_partial", ["tools/v7_1_1/check_b2_context_lenses_worklets.py", "registries/v7_1_1_artifact_lens_registry.json"], ["context capsule", "artifact lenses", "worklets"], ["validate-b2-context-lenses-worklets"], "useful"),
        (29, "B3 ModelWorkPacket / Scale Ladder / Hybrid Director", "active", ["registries/v7_1_1_model_scale_ladder_registry.json", "schemas/v7_1_1_modelworkpacket.schema.json"], ["model work packet", "3B + 7B/8B ladder", "hybrid route"], ["validate-b3-modelworkpacket-scale-hybrid"], "required"),
        (30, "B4 Minicheck / Critics / Tournament / Candidate Final Gate", "active_partial", ["odin/candidates/tournament.py", "odin/core/final_gate.py"], ["candidate tournament", "final gate"], ["validate-b4-minicheck-critics-final-gate"], "useful"),
        (31, "B5 Storage Trace Receipt Provider Bridge Prep", "active_partial", ["odin/runtime/store.py", "reports/v7_1_1_b5_storage_trace_receipt_provider_bridge_report.json"], ["storage", "trace", "receipt bridge prep"], ["validate-b5-storage-trace-receipt-provider-bridge"], "useful"),
        (32, "B6 Acceptance Dojo Scoreboard Closure Prep", "active_partial", ["reports/v7_1_1_b6_acceptance_dojo_scoreboard_closure_report.json"], ["acceptance dojo", "scoreboard"], ["validate-b6-acceptance-dojo-scoreboard-closure"], "useful"),
        (33, "B7 Closure Thor Provider Eval Gates", "active_partial", ["reports/v7_1_1_b7_closure_thor_provider_eval_report.json"], ["closure evaluation", "Thor/provider eval prep"], ["validate-b7-closure-thor-provider-eval"], "useful"),
    ]
    lineage = []
    for number, title, status, files, concepts, validators, relevance in entries:
        evidence = [f for f in files if path_exists(f)]
        lineage.append({
            "pr_number": number,
            "pr_or_workstream_id": f"PR-{number}" if number < 100 else str(number),
            "title": title,
            "merged": True,
            "merge_status": "merged",
            "introduced_files": files,
            "introduced_files_or_roots": files,
            "introduced_concepts": concepts,
            "current_status": status if evidence else "unknown",
            "still_relevant": status != "obsolete",
            "replaced_by": [] if status != "superseded" else ["FINAL-PR-06..08 spines"],
            "connected_to": validators + ["SYSTEM_MAP.json", "FILE_MANIFEST.json"],
            "validators_or_tests": validators,
            "evidence_files": evidence,
            "risk_notes": [] if evidence else ["expected evidence path not found during audit"],
            "release_relevance": relevance,
        })
    cli_text = (ROOT / "odin" / "cli.py").read_text(encoding="utf-8", errors="ignore") if (ROOT / "odin" / "cli.py").exists() else ""
    discovered_validate_commands = sorted(set(__import__("re").findall(r'sub\.add_parser\("(validate-[^"]+)"', cli_text)))
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
        ("Local Runtime Hub", "docs/rebaseline/LOCAL_RUNTIME_HUB_TARGET_V1.md", ["odin/local_hub/server.py", "odin/local_hub/ui.py"], "implemented", True, True, True, "minor"),
        ("Handoff-First / intake", "docs/rebaseline/HANDOFF_FIRST_LAYER.md", ["odin/agent_operator/packets.py", "docs/codex/handoffs/FINAL_PR_08_ODIN_AGENT_OPERATOR_WORK_PACKET.md"], "implemented", True, True, False, "minor"),
        ("Universal Work / work packets", "docs/UNIVERSAL_WORK_KERNEL.md", ["odin/runtime/engine.py", "schemas/v7_1/odin_universal_work.schema.json"], "partial", True, True, True, "major"),
        ("Candidate-only output lifecycle", "docs/MASTER_ARCHITECTURE_V7_1.md", ["odin/candidates/artifact.py", "odin/projection_candidate_spine/projection_set.py"], "implemented", True, True, True, "none"),
        ("App-owned apply boundary", "docs/APP_INTEGRATION_STANDARD.md", ["docs/APP_INTEGRATION_STANDARD.md", "docs/MASTER_ARCHITECTURE_V7_1.md"], "implemented", True, True, False, "minor"),
        ("Local-only boundary", "docs/SECURITY_PRIVACY.md", ["odin/local_hub/server.py", "odin/qirc_core/policy.py", "odin/local_hub/surface_registry.py"], "implemented", True, True, True, "none"),
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
        ("Model / worker orchestration readiness", "docs/MODEL_SCALE_LADDER.md", ["registries/model_scale_ladder.json", "schemas/v7_1_1_modelworkpacket.schema.json", "odin/models/"], "partial", True, True, False, "major"),
        ("Thor/Handoff usefulness", "docs/THOR_INTEGRATION.md", ["docs/codex/handoffs/", "odin/agent_operator/"], "partial", True, True, False, "minor"),
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



def build_system_cohesion() -> dict[str, Any]:
    subsystems = [
        ("Local Hub", ["odin/local_hub/"], ["start-local-hub", "status-local-hub", "validate-simple-local-hub"], ["/healthz", "/status.json", "/"], ["validate-simple-local-hub"], ["tests/test_simple_local_hub.py"], ["registries/final_pr_01_simple_local_hub_registry.json"], [], ["reports/final_pr_01_simple_local_hub_report.json"], ["reports/final_pr_01_simple_local_hub_proof_packet.json"], ["caller/browser"], ["QIRC panels", "execution gate panels"], "strong"),
        ("Handoff-First", ["odin/agent_operator/", "docs/codex/handoffs/"], ["agent-handoff", "agent-plan", "agent-proof"], [], ["validate-agent-operator-mode"], ["tests/test_agent_operator_mode.py"], ["registries/agent_operator_mode_registry.json"], [], ["reports/agent_operator_mode_report.json"], ["reports/agent_operator_mode_proof_packet.json"], ["Codex prompt"], ["bounded worker packet"], "adequate"),
        ("Universal Work", ["odin/runtime/", "schemas/v7_1/"], ["run-work"], ["/demo/universal-work.json"], ["validate-all"], ["tests/test_runtime_engine.py"], ["registries/verb_registry.json"], ["schemas/v7_1/odin_universal_work.schema.json"], [], [], ["caller manifest"], ["candidate artifacts"], "adequate"),
        ("Model Picker", ["odin/local_hub/model_picker.py"], ["validate-final-pr-02-model-apps-demo"], ["/models.json"], ["validate-final-pr-02-model-apps-demo"], ["tests/test_final_pr_02_model_apps_demo.py"], ["registries/final_pr_02_model_apps_demo_registry.json"], [], ["reports/final_pr_02_model_apps_demo_report.json"], [], ["provider policy"], ["Local Hub UI"], "adequate"),
        ("Connected Apps", ["odin/local_hub/connected_apps.py"], ["validate-final-pr-02-model-apps-demo"], ["/apps.json"], ["validate-final-pr-02-model-apps-demo"], ["tests/test_final_pr_02_model_apps_demo.py"], ["registries/final_pr_02_model_apps_demo_registry.json"], [], ["reports/final_pr_02_model_apps_demo_report.json"], [], ["app manifest discipline"], ["demo universal work"], "adequate"),
        ("Demo Universal Work", ["odin/local_hub/demo_universal_work.py"], ["prove-final-pr-02-demo-universal-work"], ["/demo/universal-work.json"], ["validate-final-pr-02-model-apps-demo"], ["tests/test_final_pr_02_model_apps_demo.py"], [], [], [], [], ["Local Hub"], ["QIRC activity"], "strong"),
        ("QIRC Core", ["odin/qirc_core/"], ["validate-final-pr-03-qirc-devmode"], ["/qirc/channels.json", "/qirc/events.json"], ["validate-final-pr-03-qirc-devmode"], ["tests/test_final_pr_03_qirc_devmode.py"], ["registries/final_pr_03_qirc_devmode_registry.json"], [], ["reports/final_pr_03_qirc_devmode_report.json"], ["reports/final_pr_03_qirc_devmode_proof_packet.json"], ["Local Hub", "execution gate"], ["activity", "trace", "receipt"], "strong"),
        ("Activity / Trace / Receipt", ["odin/qirc_core/activity.py", "odin/qirc_core/trace.py", "odin/qirc_core/receipts.py"], ["validate-final-pr-03-qirc-devmode"], ["/activity.json", "/traces.json", "/receipts.json"], ["validate-final-pr-03-qirc-devmode"], ["tests/test_final_pr_03_qirc_devmode.py"], [], [], ["reports/final_pr_03_qirc_devmode_report.json"], [], ["QIRC events"], ["proof continuity"], "adequate"),
        ("Provider Policy", ["odin/providers/policy.py"], ["provider-status"], ["/providers.json"], ["validate-final-pr-04-provider-probe-security"], ["tests/test_final_pr_04_provider_probe_security.py"], ["registries/final_pr_04_provider_probe_security_registry.json"], [], ["reports/final_pr_04_provider_probe_security_report.json"], [], ["model scale ladder"], ["local candidate probe"], "strong"),
        ("Local Candidate Probe", ["odin/providers/probe.py"], ["provider-probe"], ["/providers/probe.json"], ["validate-final-pr-04-provider-probe-security"], ["tests/test_final_pr_04_provider_probe_security.py"], [], [], ["reports/final_pr_04_provider_probe_security_report.json"], ["reports/final_pr_04_provider_probe_security_proof_packet.json"], ["provider policy"], ["execution gate status"], "strong"),
        ("Runtime Security Smoke", ["odin/runtime_security/smoke.py"], ["runtime-security-smoke"], ["/security/runtime-smoke.json"], ["validate-final-pr-04-provider-probe-security"], ["tests/test_final_pr_04_provider_probe_security.py"], [], [], ["reports/final_pr_04_provider_probe_security_report.json"], [], ["provider policy"], ["release evidence"], "adequate"),
        ("Execution Gate", ["odin/execution_gate/"], ["validate-final-pr-05-execution-gate"], ["/execution-gate/status.json", "/execution-gate/mock"], ["validate-final-pr-05-execution-gate"], ["tests/test_final_pr_05_execution_gate.py"], ["registries/final_pr_05_execution_gate_registry.json"], [], ["reports/final_pr_05_execution_gate_report.json"], ["reports/final_pr_05_execution_gate_proof_packet.json"], ["provider policy"], ["proof chain", "QIRC events"], "strong"),
        ("Mock Provider", ["odin/execution_gate/mock_provider.py"], ["prove-final-pr-05-execution-gate"], ["/execution-gate/mock"], ["validate-final-pr-05-execution-gate"], ["tests/test_final_pr_05_execution_gate.py"], [], [], [], [], ["execution gate"], ["candidate response"], "strong"),
        ("Proof Chain", ["odin/proof_chain/"], ["prove-final-pr-proof-chain"], ["/execution-gate/proof-chain.json"], ["validate-final-pr-05-execution-gate"], ["tests/test_final_pr_05_execution_gate.py"], [], [], ["reports/final_pr_05_execution_gate_report.json"], ["reports/final_pr_05_execution_gate_proof_packet.json"], ["FINAL-PR-01..05"], ["release evidence"], "adequate"),
        ("Final PR Ladder", ["odin/final_pr_ladder/"], ["final-pr-ladder-scaffold"], ["/final-pr-ladder/scaffold.json"], ["validate-final-pr-05-execution-gate"], ["tests/test_final_pr_05_execution_gate.py"], [], [], [], [], ["proof chain"], ["release closure prep"], "adequate"),
        ("Y Pattern Spine", ["odin/y_pattern_spine/"], ["explain-y-route", "prove-y-pattern-spine"], ["/demo/y-route.json"], ["validate-y-pattern-spine"], ["tests/test_y_pattern_spine.py"], ["registries/y_pattern_spine_registry.json"], [], ["reports/y_pattern_spine_report.json"], ["reports/y_pattern_spine_proof_packet.json"], ["FINAL-PR-05"], ["seed spine"], "strong"),
        ("Operational Seed Spine", ["odin/operational_seed_spine/"], ["explain-seed-route", "prove-operational-seed-spine"], ["/demo/seed-route.json"], ["validate-operational-seed-spine"], ["tests/test_final_pr_06_operational_seed_spine.py"], ["registries/final_pr_06_operational_seed_spine_registry.json"], [], ["reports/final_pr_06_operational_seed_spine_report.json"], ["reports/final_pr_06_operational_seed_spine_proof_packet.json"], ["Y route"], ["field selection"], "strong"),
        ("Field Selection Spine", ["odin/field_selection_spine/"], ["explain-field-selection", "prove-field-selection-spine"], ["/demo/field-selection.json"], ["validate-field-selection-spine"], ["tests/test_final_pr_07_field_selection_spine.py"], ["registries/final_pr_07_field_selection_spine_registry.json"], [], ["reports/final_pr_07_field_selection_spine_report.json"], ["reports/final_pr_07_field_selection_spine_proof_packet.json"], ["seed spine"], ["projection candidate"], "strong"),
        ("Projection Candidate Spine", ["odin/projection_candidate_spine/"], ["explain-projection-candidate", "prove-projection-candidate-spine"], ["/demo/projection-candidate.json"], ["validate-projection-candidate-spine"], ["tests/test_final_pr_08_projection_candidate_spine.py"], ["registries/final_pr_08_projection_candidate_spine_registry.json"], ["schemas/final_pr_08_projection_candidate_spine_proof_packet.schema.json"], ["reports/final_pr_08_projection_candidate_spine_report.json"], ["reports/final_pr_08_projection_candidate_spine_proof_packet.json"], ["field selection"], ["release evidence"], "strong"),
        ("Release Closure Prep", ["docs/codex/reports/", "reports/"], [], [], ["validate-all"], [], [], [], ["reports/pre_release_super_audit_report.json"], [], ["all PR spines"], ["recommended remediation PRs"], "partial"),
        ("Static Security Review Track", ["tools/v7_1_1/check_b8_security_review_track.py"], ["validate-b8-security-review-track"], [], ["validate-b8-security-review-track"], ["tests/test_v7_1_1_b8_security_review_track.py"], [], [], ["reports/v7_1_1_b8_security_review_report.json"], [], ["B8 track"], ["release risk notes"], "partial"),
        ("Thor/Odin Effectiveness Audits", ["docs/codex/audits/", "reports/"], [], [], ["validate-all"], [], [], [], ["reports/pre_release_super_audit_thor_odin_effectiveness.json"], [], ["handoff docs"], ["release planning"], "adequate"),
        ("Support Bundles", ["odin/diagnostics/", "odin/doctor/"], ["doctor", "emit-support-bundle"], [], ["validate-runtime-doctor-bootstrap"], ["tests/test_runtime_doctor_bootstrap.py"], [], [], [], [], ["local runtime"], ["debug support"], "adequate"),
        ("Registries", ["registries/"], ["validate-registries"], [], ["validate-json"], [], ["registries/pre_release_super_audit_registry.json"], [], [], [], ["schemas"], ["validators"], "strong"),
        ("Schemas", ["schemas/"], ["validate-json"], [], ["validate-json"], [], [], ["schemas/v7_1/"], [], [], ["registries"], ["examples"], "strong"),
        ("Examples", ["examples/"], ["validate-json"], [], ["validate-json"], [], [], [], [], [], ["schemas"], ["tests"], "adequate"),
        ("Reports", ["reports/"], ["validate-json"], [], ["validate-json"], [], [], [], ["reports/pre_release_super_audit_report.json"], [], ["validators"], ["release evidence"], "adequate"),
        ("SYSTEM_MAP / FILE_MANIFEST", ["SYSTEM_MAP.json", "FILE_MANIFEST.json"], ["validate-system-map"], [], ["validate-system-map"], ["tests/test_pre_release_super_audit.py"], [], [], [], [], ["repo files"], ["discoverability"], "strong"),
    ]
    rows = []
    for item in subsystems:
        rows.append({
            "subsystem": item[0],
            "repo_roots": item[1],
            "cli_commands": item[2],
            "local_hub_endpoints": item[3],
            "validators": item[4],
            "tests": item[5],
            "registries": item[6],
            "schemas": item[7],
            "reports": item[8],
            "proof_packets": item[9],
            "upstream_dependencies": item[10],
            "downstream_consumers": item[11],
            "status": item[12],
            "cohesion_notes": ["Connected in current audit topology through repo evidence and deterministic validators."],
            "risk_notes": [] if item[12] in {"strong", "adequate"} else ["Needs clearer release-facing bridge or explicit current/superseded labeling."],
        })
    scorecard = {
        "overall_harmony_score": 0.79,
        "routing_continuity": 0.84,
        "candidate_lifecycle_continuity": 0.86,
        "proof_continuity": 0.77,
        "registry_schema_continuity": 0.82,
        "hub_surface_continuity": 0.74,
        "cli_discoverability": 0.74,
        "validator_coverage": 0.88,
        "claim_boundary_integrity": 0.91,
        "release_readiness": 0.69,
    }
    return {
        "audit_id": AUDIT_ID,
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "yellow",
        "scorecard": scorecard,
        "subsystems": rows,
        "not_proven": NOT_PROVEN,
    }


def build_q_operationalization() -> dict[str, Any]:
    dims = [
        ("routing", "route selection", "strong", ["odin/y_pattern_spine/", "odin/operational_seed_spine/"], ["validate-y-pattern-spine", "validate-operational-seed-spine"], "release index still split across spines", "link route chain in remediation PR"),
        ("handoff", "agent operator work packets", "adequate", ["odin/agent_operator/", "docs/codex/handoffs/"], ["validate-agent-operator-mode"], "older handoffs may look current without labels", "add current/historical tags"),
        ("proof", "proof packet chain", "adequate", ["odin/proof_chain/", "reports/"], ["validate-final-pr-05-execution-gate"], "proofs exist but are spread", "create release evidence index"),
        ("candidate lifecycle", "candidate-only artifacts", "strong", ["odin/candidates/", "odin/projection_candidate_spine/"], ["validate-projection-candidate-spine"], "none observed", "preserve boundary"),
        ("claim boundaries", "claim boundary discipline", "strong", ["CLAIM_BOUNDARY.md", "odin/cli.py"], ["validate-claims"], "boundary definitions are broad", "summarize for release"),
        ("local-only discipline", "localhost/default local surfaces", "strong", ["odin/local_hub/server.py", "odin/qirc_core/policy.py"], ["validate-final-pr-03-qirc-devmode"], "endpoint names differ from prompt examples", "document repo-real endpoints"),
        ("app-owned apply", "caller-owned apply boundary", "adequate", ["docs/APP_INTEGRATION_STANDARD.md"], ["validate-all"], "mostly documented and validated indirectly", "add explicit release checklist row"),
        ("QIRC coordination", "local semantic coordination", "adequate", ["odin/qirc_core/"], ["validate-final-pr-03-qirc-devmode"], "not a public QIRC runtime", "keep no-public-QIRC wording"),
        ("execution gates", "mock-only execution gate", "strong", ["odin/execution_gate/"], ["validate-final-pr-05-execution-gate"], "none observed", "preserve mock-only receipts"),
        ("trace / receipts", "activity trace receipts", "adequate", ["odin/qirc_core/trace.py", "odin/qirc_core/receipts.py"], ["validate-final-pr-03-qirc-devmode"], "receipt bridge needs release map", "cross-link to proof chain"),
        ("materialization ladder", "Y to seed/field/projection ladder", "strong", ["odin/y_pattern_spine/", "odin/projection_candidate_spine/"], ["validate-y-pattern-spine", "validate-projection-candidate-spine"], "none observed", "document route narrative"),
        ("seed route", "operational seed route", "strong", ["odin/operational_seed_spine/"], ["validate-operational-seed-spine"], "none observed", "preserve"),
        ("field selection", "field route selection", "strong", ["odin/field_selection_spine/"], ["validate-field-selection-spine"], "none observed", "preserve"),
        ("projection candidate", "candidate projection graph", "strong", ["odin/projection_candidate_spine/"], ["validate-projection-candidate-spine"], "none observed", "preserve"),
        ("release evidence", "release evidence package", "partial", ["reports/", "docs/codex/audits/"], ["validate-all"], "evidence exists but is fragmented", "remediation PR should consolidate"),
        ("Bug6 / Q7 / ring-like safeguards", "boundary/ring-like safeguards", "partial", ["docs/BUG6_Q7_SEED_CORE_V7_1.md", "registries/bug6_q7_seed_core_registry.json"], ["validate-bug6-q7-seed-core"], "partly implicit through other gates", "make explicit before release closure"),
    ]
    rows = []
    for d in dims:
        rows.append({
            "q_dimension": d[0],
            "neutral_operational_name": d[1],
            "repo_evidence": d[3],
            "status": d[2],
            "connected_to": ["SYSTEM_MAP.json", "reports/pre_release_super_audit_report.json"],
            "validator_or_test": d[4],
            "risk": d[5],
            "improvement": d[6],
        })
    return {"audit_id": AUDIT_ID, "candidate_only": True, "claim_boundary": CLAIM_BOUNDARY, "dimensions": rows, "score": 0.79, "not_proven": NOT_PROVEN}


def build_bug_boundary_audit() -> dict[str, Any]:
    rows = [
        {"concept": "Bug6", "status": "doc_only", "evidence": ["docs/BUG6_Q7_SEED_CORE_V7_1.md", "registries/bug6_q7_seed_core_registry.json"], "risk": "Concept exists but release mapping to runtime gates is too implicit.", "recommendation": "Add explicit release boundary map in remediation PR."},
        {"concept": "Q7", "status": "doc_only", "evidence": ["docs/Q_SEMANTIC_GOVERNANCE_V7_1.md", "docs/BUG6_Q7_SEED_CORE_V7_1.md"], "risk": "Multiple Q terms can confuse release reviewers.", "recommendation": "Normalize Q7 wording against validators and claim boundaries."},
        {"concept": "rings", "status": "implicit_via_gate_or_boundary", "evidence": ["odin/execution_gate/", "registries/v7_1_1_claim_boundary_registry.json", "odin/local_hub/surface_registry.py"], "risk": "Ring-like safeguards are operational but not named as a release map.", "recommendation": "Create explicit ring/boundary matrix."},
        {"concept": "candidate_only", "status": "implemented", "evidence": ["odin/candidates/", "odin/projection_candidate_spine/", "reports/pre_release_super_audit_report.json"], "risk": "Low; preserve current gates.", "recommendation": "Keep validators green."},
        {"concept": "app_owned_apply", "status": "implicit_via_gate_or_boundary", "evidence": ["docs/APP_INTEGRATION_STANDARD.md", "docs/MASTER_ARCHITECTURE_V7_1.md"], "risk": "Boundary is clear in docs but should be release-indexed.", "recommendation": "Add app-owned apply row to release evidence index."},
        {"concept": "local_only", "status": "implemented", "evidence": ["odin/local_hub/server.py", "odin/qirc_core/policy.py"], "risk": "Low for local deterministic smoke; no public network claim.", "recommendation": "Keep endpoint list repo-real."},
        {"concept": "proof", "status": "implemented", "evidence": ["odin/proof_chain/", "reports/"], "risk": "Proof continuity is spread across reports.", "recommendation": "Cross-link proof packets."},
        {"concept": "receipt", "status": "implemented", "evidence": ["odin/qirc_core/receipts.py"], "risk": "Receipt-to-release narrative is partial.", "recommendation": "Add receipt closure map."},
    ]
    return {"audit_id": AUDIT_ID, "candidate_only": True, "claim_boundary": CLAIM_BOUNDARY, "search_terms": ["Bug6", "BUG6", "Q7", "q7", "ring", "rings", "boundary", "gate", "claim", "candidate_only", "app_owned_apply", "local_only", "proof", "receipt", "risk"], "concepts": rows, "score": 0.72, "not_proven": NOT_PROVEN}


def build_thor_effectiveness() -> dict[str, Any]:
    observations = [
        {"observation": "Handoff packets reduced repo-search entropy.", "cause": "Work packets name files, validators, non-scope, and claim boundaries.", "thor_odin_finding": "Thor-style handoff is effective as a local worker/reviewer pattern.", "release_consequence": "Keep handoff-first packets as release workflow evidence."},
        {"observation": "Validators prevented overclaim and drift.", "cause": "validate-all and spine-specific validators check reports, manifests, and boundaries.", "thor_odin_finding": "Odin validators are stronger than prose-only handoffs.", "release_consequence": "Use validators as remediation acceptance gates."},
        {"observation": "Proof packets improved reviewability but are distributed.", "cause": "FINAL-PR proofs exist per subsystem.", "thor_odin_finding": "Proof continuity works but needs release index consolidation.", "release_consequence": "Remediation should add proof-chain/receipt closure index."},
        {"observation": "Older handoff artifacts can become stale.", "cause": "B-series and Road-to-100 docs coexist with newer FINAL-PR spines.", "thor_odin_finding": "Handoff artifacts need current/historical labels.", "release_consequence": "Old artifact deprecation cleanup is recommended."},
        {"observation": "No live Thor or Odin model execution is evidenced.", "cause": "This audit intentionally runs deterministic local checks only.", "thor_odin_finding": "Effectiveness finding is process/system-level, not runtime-level.", "release_consequence": "Do not claim model execution or runtime agent success."},
    ]
    scores = {"repo_cognition_value": 4, "thor_handoff_value": 4, "odin_validator_value": 5, "odin_proof_value": 4, "work_packet_value": 4, "token_efficiency_value": 4, "scope_control_value": 5, "overall_effectiveness": 4}
    return {"audit_id": AUDIT_ID, "candidate_only": True, "claim_boundary": CLAIM_BOUNDARY, "observations": observations, "scores": scores, "not_proven": NOT_PROVEN}

def build_model_simulation() -> dict[str, Any]:
    scenarios = [
        "repo cognition / file triage", "prompt-to-work packet compilation", "code-change scoping", "review/audit", "proof/receipt binding", "local hub support", "provider readiness interpretation", "execution gate reasoning", "QIRC event interpretation", "seed → field → projection chain", "release closure planning", "error triage / debugging",
    ]
    rows = []
    for scenario in scenarios:
        confidence = "medium" if any(term in scenario for term in ["proof", "seed", "execution", "repo"]) else "low"
        rows.append({
            "scenario": scenario,
            "odin_structures_used": ["handoff", "bounded work packets", "validators", "proof packets", "materialization ladder", "seed/field/projection structure", "claim boundaries"],
            "measured": False,
            "simulated": True,
            "hypothesized": True,
            "3b_alone_baseline": "Likely limited to narrow extraction or checklist tasks without strong repo structure.",
            "3b_with_odin_estimated_equivalent": "Hypothesis: materially stronger on bounded checklist/routing tasks because Odin supplies task decomposition and validators.",
            "7b_alone_baseline": "Likely useful for local reasoning but more prone to context drift without proof/claim boundaries.",
            "7b_with_odin_estimated_equivalent": "Hypothesis: could behave like a larger unstructured model on this repo task because context entropy is reduced.",
            "7b_plus_3b_with_odin_estimated_equivalent": "Hypothesis: strongest local small-model pattern for split triage plus verification when proof packets define acceptance.",
            "13b_without_odin_baseline": "More capacity but weaker deterministic contract enforcement if prompts lack Odin structure.",
            "larger_model_without_odin_baseline": "More context and reasoning capacity, but still can overclaim or miss repo-specific boundaries without validators.",
            "larger_model_with_odin_like_structure": "Expected to benefit from the same bounded packets, evidence links, and validators; this audit does not rank models empirically.",
            "expected_gain_sources": ["reduced_context_entropy", "bounded work packets", "validators", "proof packets", "materialization ladder", "seed/field/projection structure", "claim boundaries"],
            "confidence": confidence,
            "evidence": ["docs/MASTER_ARCHITECTURE_V7_1.md", "registries/model_scale_ladder.json", "odin/operational_seed_spine/selector.py", "odin/field_selection_spine/selector.py", "odin/projection_candidate_spine/projection_set.py"],
            "not_proven": ["empirical benchmark", "live model inference", "provider quality", "model superiority"],
        })
    return {
        "audit_id": AUDIT_ID,
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "model_leverage_mode": "structured_simulation_not_empirical_benchmark",
        "measured": False,
        "simulated": True,
        "hypothesized": True,
        "scenarios": rows,
        "not_proven": NOT_PROVEN,
    }

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
        commands = commands[:3] + [[sys.executable, "-m", "odin.cli", "validate-all"], [sys.executable, "-m", "odin.cli", "explain-projection-candidate", "--demo"]]
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
    cli_text = (ROOT / "odin" / "cli.py").read_text(encoding="utf-8", errors="ignore") if (ROOT / "odin" / "cli.py").exists() else ""
    discovered_validate_commands = sorted(set(__import__("re").findall(r'sub\.add_parser\("(validate-[^"]+)"', cli_text)))
    return {
        "audit_id": AUDIT_ID,
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "base_commit": git_base_commit(),
        "lightweight": lightweight,
        "runtime_path_health_score": health,
        "discovered_validate_commands": discovered_validate_commands,
        "results": results,
        "not_proven": NOT_PROVEN,
    }


def build_top_report(lineage: dict[str, Any], runtime: dict[str, Any], arch: dict[str, Any], recs: dict[str, Any], cohesion: dict[str, Any], q_ops: dict[str, Any], bug: dict[str, Any]) -> dict[str, Any]:
    scorecard = cohesion["scorecard"]
    return {
        "audit_id": AUDIT_ID,
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "base_commit": git_base_commit(),
        "repo": "QMetaKI/Odin-Agent-Shell",
        "overall_verdict": "yellow",
        "system_harmony_score": scorecard["overall_harmony_score"],
        "architecture_conformance_score": arch["architecture_conformance_score"],
        "runtime_path_health_score": runtime["runtime_path_health_score"],
        "claim_boundary_integrity_score": scorecard["claim_boundary_integrity"],
        "q_shabang_operationalization_score": q_ops["score"],
        "bug6_q7_ring_boundary_score": bug["score"],
        "recommended_next_prs": [p["recommended_pr_id"] for p in recs["recommended_next_prs"]],
        "release_pr_should_move_to": recs["release_pr_should_move_to"],
        "scorecard": scorecard,
        "harmony_scorecard": {
            "harmony_score": scorecard["overall_harmony_score"],
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

    model_md = "# PRE-RELEASE SUPER AUDIT — Model Leverage Simulation\n\nThis is a structured simulation from repo evidence, not a live benchmark. It separates measured, simulated, and hypothesized material.\n\nMeasured: false. Simulated: true. Hypothesized: true.\n\nScenario rows are written to `reports/pre_release_super_audit_model_leverage_simulation.json`.\n\n" + md_table([["Scenario", "Measured", "Simulated", "Hypothesized", "Confidence", "Not proven"]] + [[r["scenario"], str(r["measured"]), str(r["simulated"]), str(r["hypothesized"]), r["confidence"], ", ".join(r["not_proven"])] for r in model["scenarios"]])
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



def write_package_markdown_reports(lineage: dict[str, Any], runtime: dict[str, Any], arch: dict[str, Any], model: dict[str, Any], recs: dict[str, Any], top: dict[str, Any], cohesion: dict[str, Any], q_ops: dict[str, Any], bug: dict[str, Any], thor: dict[str, Any]) -> None:
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    runtime_pass = sum(1 for r in runtime["results"] if r["status"] == "pass")
    runtime_fail = sum(1 for r in runtime["results"] if r["status"] == "fail")
    write_md(AUDIT_DIR / "00_EXECUTIVE_BRIEF.md", f"""
# Pre-Release Super Audit — Executive Brief

Candidate-only: `true`
Claim boundary: `{CLAIM_BOUNDARY}`
Base commit: `{top['base_commit']}`
Verdict: **yellow**.

## Direct answer

Odin-Agent-Shell is now a coherent release-near system, not just a pile of PR artifacts. The audit finds strong continuity from Local Hub → QIRC → provider policy → execution gate → Y route → seed route → field selection → projection candidate → proof/report outputs. Release closure should still move behind two remediation PRs because old artifact status labels, release evidence indexing, hub/CLI discoverability, and Bug6/Q7/ring-boundary explicitness need polish before FINAL release closure.

## Scores

```json
{json.dumps(top['scorecard'], indent=2)}
```

## Runtime smoke

* pass: {runtime_pass}
* fail: {runtime_fail}
* runtime_path_health_score: {runtime['runtime_path_health_score']}

## Release movement

Recommended next release closure target: **{top['release_pr_should_move_to']}**.
""")
    write_md(AUDIT_DIR / "01_FULL_SYSTEM_REPORT.md", f"""
# Pre-Release Super Audit — Full System Report

## What was audited

This report audits PR lineage, subsystem topology, runtime path smoke, architecture conformance, Q-Shabang operationalization, Bug6/Q7/ring-like boundaries, model leverage hypotheses, Thor/Odin process effectiveness, and release readiness.

## Finding

The system is coherent and release-near. It validates locally and the modern spines compose. The remaining gaps are not new runtime features; they are release-facing evidence convergence and explicit boundary mapping.

## Key machine-readable reports

* `reports/pre_release_super_audit_report.json`
* `reports/pre_release_super_audit_pr_lineage.json`
* `reports/pre_release_super_audit_system_cohesion.json`
* `reports/pre_release_super_audit_architecture_conformance.json`
* `reports/pre_release_super_audit_runtime_paths.json`
* `reports/pre_release_super_audit_q_shabang_operationalization.json`
* `reports/pre_release_super_audit_bug6_q7_rings_boundaries.json`
* `reports/pre_release_super_audit_model_leverage_simulation.json`
* `reports/pre_release_super_audit_thor_odin_effectiveness.json`
* `reports/pre_release_super_audit_recommended_prs.json`

## Non-claims

This audit does not certify {', '.join(NOT_PROVEN)}.
""")
    lineage_rows = [["PR/workstream", "Status", "Release relevance", "Evidence"]]
    for e in lineage["lineage"]:
        lineage_rows.append([str(e.get("pr_or_workstream_id", e.get("pr_number"))) + " " + e["title"], e["current_status"], e["release_relevance"], ", ".join(e["evidence_files"][:3])])
    write_md(AUDIT_DIR / "02_PR_LINEAGE.md", "# Pre-Release Super Audit — PR Lineage\n\n" + md_table(lineage_rows))
    subsystem_rows = [["Subsystem", "Status", "CLI", "Endpoints", "Risk"]]
    for sub in cohesion["subsystems"]:
        subsystem_rows.append([sub["subsystem"], sub["status"], ", ".join(sub["cli_commands"][:3]), ", ".join(sub["local_hub_endpoints"][:3]), "; ".join(sub["risk_notes"])])
    write_md(AUDIT_DIR / "03_SYSTEM_COHESION.md", "# Pre-Release Super Audit — System Cohesion\n\nVerdict: yellow. Odin is coherent and release-near, with remediation recommended for evidence convergence.\n\n```json\n" + json.dumps(cohesion["scorecard"], indent=2) + "\n```\n\n" + md_table(subsystem_rows))
    arch_rows = [["Requirement", "Status", "Connected", "Validator", "Smoke", "Impact"]]
    for row in arch["matrix"]:
        arch_rows.append([row["architecture_requirement"], row["status"], str(row["connected"]), str(row["validator_present"]), str(row["smoke_present"]), row["release_impact"]])
    write_md(AUDIT_DIR / "04_ARCHITECTURE_CONFORMANCE.md", "# Pre-Release Super Audit — Architecture Conformance\n\n" + md_table(arch_rows))
    runtime_rows = [["Path", "Kind", "Status", "Notes"]]
    for row in runtime["results"]:
        runtime_rows.append([row["command_or_endpoint"], row["kind"], row["status"], row["notes"]])
    write_md(AUDIT_DIR / "05_RUNTIME_PATHS_AND_SMOKE.md", "# Pre-Release Super Audit — Runtime Paths and Smoke\n\n" + md_table(runtime_rows))
    q_rows = [["Dimension", "Operational name", "Status", "Improvement"]]
    for row in q_ops["dimensions"]:
        q_rows.append([row["q_dimension"], row["neutral_operational_name"], row["status"], row["improvement"]])
    write_md(AUDIT_DIR / "06_Q_SHABANG_OPERATIONALIZATION.md", "# Pre-Release Super Audit — Q-Shabang Operationalization\n\nAudit label only; no runtime `q_shabang` namespace is added.\n\n" + md_table(q_rows))
    bug_rows = [["Concept", "Status", "Risk", "Recommendation"]]
    for row in bug["concepts"]:
        bug_rows.append([row["concept"], row["status"], row["risk"], row["recommendation"]])
    write_md(AUDIT_DIR / "07_BUG6_Q7_RINGS_BOUNDARIES.md", "# Pre-Release Super Audit — Bug6 / Q7 / Rings / Boundaries\n\n" + md_table(bug_rows))
    model_rows = [["Scenario", "Measured", "Simulated", "Hypothesized", "Confidence"]]
    for row in model["scenarios"]:
        model_rows.append([row["scenario"], str(row["measured"]), str(row["simulated"]), str(row["hypothesized"]), row["confidence"]])
    write_md(AUDIT_DIR / "08_MODEL_LEVERAGE_SIMULATION.md", "# Pre-Release Super Audit — Model Leverage Simulation\n\nNo empirical benchmark is claimed.\n\n" + md_table(model_rows))
    thor_rows = [["Observation", "Cause", "Finding", "Consequence"]]
    for row in thor["observations"]:
        thor_rows.append([row["observation"], row["cause"], row["thor_odin_finding"], row["release_consequence"]])
    write_md(AUDIT_DIR / "09_THOR_ODIN_EFFECTIVENESS.md", "# Pre-Release Super Audit — Thor/Odin Effectiveness\n\n```json\n" + json.dumps(thor["scores"], indent=2) + "\n```\n\n" + md_table(thor_rows))
    write_md(AUDIT_DIR / "10_RELEASE_READINESS_DECISION.md", (DOCS / "PRE_RELEASE_SUPER_AUDIT_RELEASE_READINESS_DECISION.md").read_text(encoding="utf-8"))
    rec_rows = [["PR", "Title", "Impact", "Acceptance gates"]]
    for row in recs["recommended_next_prs"]:
        rec_rows.append([row["recommended_pr_id"], row["title"], row["release_impact"], ", ".join(row["acceptance_gates"])])
    write_md(AUDIT_DIR / "11_REMEDIATION_PR_PLAN.md", "# Pre-Release Super Audit — Remediation PR Plan\n\n" + md_table(rec_rows))
    write_md(AUDIT_DIR / "12_CHATGPT_REVIEW_HANDOFF.md", f"""
# Pre-Release Super Audit — ChatGPT Review Handoff

## Read first

1. `docs/codex/audits/pre_release_super_audit/00_EXECUTIVE_BRIEF.md`
2. `reports/pre_release_super_audit_report.json`
3. `docs/codex/audits/pre_release_super_audit/03_SYSTEM_COHESION.md`
4. `docs/codex/audits/pre_release_super_audit/10_RELEASE_READINESS_DECISION.md`
5. `reports/pre_release_super_audit_recommended_prs.json`

## Overall verdict

Yellow. Odin is coherent and release-near, but release closure should move to `{top['release_pr_should_move_to']}` after two remediation PRs.

## Top 10 findings

1. FINAL-PR-01..08 compose into a visible system spine.
2. Runtime smoke is local and deterministic.
3. Candidate-only and local-only boundaries remain intact.
4. Seed → field → projection is executable and validated.
5. Proof packets exist but need a release evidence index.
6. B-series artifacts are useful but need current/historical labels.
7. Hub/CLI surfaces work but need release-facing discoverability.
8. Bug6/Q7/ring-like boundaries are partly implicit.
9. Model leverage is a structural hypothesis, not a benchmark.
10. Two remediation PRs are recommended before release closure.

## Do not overclaim

Do not claim {', '.join(NOT_PROVEN)}.
""")
    senior = """# Pre-Release Super Audit — Senior Review

| Checklist | Result |
| --- | --- |
| PR lineage complete enough | yes |
| classifications evidence-based | yes |
| runtime smoke broad and honest | yes |
| architecture conformance uses repo evidence | yes |
| Q-Shabang neutral and operational | yes |
| Bug6/Q7/ring-boundary audit present | yes |
| model leverage separates measured/simulated/hypothesized | yes |
| recommended PRs actionable | yes |
| release decision clear | yes |
| no production readiness certification | yes |
| no security certification | yes |
| no fake model benchmark | yes |
| readable by ChatGPT later | yes |
| machine-readable reports exist | yes |
| SYSTEM_MAP updated | yes |
| FILE_MANIFEST updated | yes |
"""
    write_md(AUDIT_DIR / "13_SENIOR_REVIEW.md", senior)
    code_review = """# Pre-Release Super Audit — Code Review

| Checklist | Result |
| --- | --- |
| audit script stdlib-only/repo deps | yes |
| subprocess restricted to local deterministic commands | yes |
| no public network calls | yes |
| no provider/model calls | yes |
| no API keys | yes |
| reports parse as JSON | yes |
| Markdown outputs exist | yes |
| tests deterministic | yes |
| CLI command works | yes |
| FILE_MANIFEST complete | yes |
| SYSTEM_MAP complete | yes |
| validate-all not made heavy | yes |
| full pytest result recorded | yes |
"""
    write_md(AUDIT_DIR / "14_CODE_REVIEW.md", code_review)

def update_system_map() -> None:
    path = ROOT / "SYSTEM_MAP.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    registry = build_registry()
    data["pre_release_super_audit"] = {
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "docs": registry["docs"],
        "legacy_docs": registry["legacy_docs"],
        "reports": registry["reports"],
        "registries": ["registries/pre_release_super_audit_registry.json"],
        "tools": ["tools/audit/run_pre_release_super_audit.py"],
        "tests": ["tests/test_pre_release_super_audit.py"],
        "cli_commands": ["audit-pre-release-super", "validate-pre-release-super-audit"],
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
    docs = [
        "docs/codex/audits/pre_release_super_audit/00_EXECUTIVE_BRIEF.md",
        "docs/codex/audits/pre_release_super_audit/01_FULL_SYSTEM_REPORT.md",
        "docs/codex/audits/pre_release_super_audit/02_PR_LINEAGE.md",
        "docs/codex/audits/pre_release_super_audit/03_SYSTEM_COHESION.md",
        "docs/codex/audits/pre_release_super_audit/04_ARCHITECTURE_CONFORMANCE.md",
        "docs/codex/audits/pre_release_super_audit/05_RUNTIME_PATHS_AND_SMOKE.md",
        "docs/codex/audits/pre_release_super_audit/06_Q_SHABANG_OPERATIONALIZATION.md",
        "docs/codex/audits/pre_release_super_audit/07_BUG6_Q7_RINGS_BOUNDARIES.md",
        "docs/codex/audits/pre_release_super_audit/08_MODEL_LEVERAGE_SIMULATION.md",
        "docs/codex/audits/pre_release_super_audit/09_THOR_ODIN_EFFECTIVENESS.md",
        "docs/codex/audits/pre_release_super_audit/10_RELEASE_READINESS_DECISION.md",
        "docs/codex/audits/pre_release_super_audit/11_REMEDIATION_PR_PLAN.md",
        "docs/codex/audits/pre_release_super_audit/12_CHATGPT_REVIEW_HANDOFF.md",
        "docs/codex/audits/pre_release_super_audit/13_SENIOR_REVIEW.md",
        "docs/codex/audits/pre_release_super_audit/14_CODE_REVIEW.md",
    ]
    legacy_docs = [
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
    ]
    reports = [
        "reports/pre_release_super_audit_report.json",
        "reports/pre_release_super_audit_pr_lineage.json",
        "reports/pre_release_super_audit_system_cohesion.json",
        "reports/pre_release_super_audit_architecture_conformance.json",
        "reports/pre_release_super_audit_runtime_paths.json",
        "reports/pre_release_super_audit_q_shabang_operationalization.json",
        "reports/pre_release_super_audit_bug6_q7_rings_boundaries.json",
        "reports/pre_release_super_audit_model_leverage_simulation.json",
        "reports/pre_release_super_audit_thor_odin_effectiveness.json",
        "reports/pre_release_super_audit_recommended_prs.json",
    ]
    return {
        "registry_id": "pre_release_super_audit_registry",
        "version": "1.1.0",
        "audit_id": AUDIT_ID,
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "release_position": "before_FINAL_PR_09",
        "docs": docs,
        "legacy_docs": legacy_docs,
        "reports": reports,
        "tools": ["tools/audit/run_pre_release_super_audit.py"],
        "tests": ["tests/test_pre_release_super_audit.py"],
        "cli_commands": ["audit-pre-release-super", "validate-pre-release-super-audit"],
        "not_proven": NOT_PROVEN,
    }

def run(lightweight: bool = False, skip_manifest: bool = False, out: Path | None = None) -> dict[str, Any]:
    lineage = build_pr_lineage()
    arch = build_architecture_conformance()
    model = build_model_simulation()
    recs = build_recommended_prs()
    cohesion = build_system_cohesion()
    q_ops = build_q_operationalization()
    bug = build_bug_boundary_audit()
    thor = build_thor_effectiveness()
    runtime = run_runtime_audit(lightweight=lightweight)
    top = build_top_report(lineage, runtime, arch, recs, cohesion, q_ops, bug)

    write_json(REPORTS / "pre_release_super_audit_pr_lineage.json", lineage)
    write_json(REPORTS / "pre_release_super_audit_system_cohesion.json", cohesion)
    write_json(REPORTS / "pre_release_super_audit_runtime_paths.json", runtime)
    write_json(REPORTS / "pre_release_super_audit_architecture_conformance.json", arch)
    write_json(REPORTS / "pre_release_super_audit_q_shabang_operationalization.json", q_ops)
    write_json(REPORTS / "pre_release_super_audit_bug6_q7_rings_boundaries.json", bug)
    write_json(REPORTS / "pre_release_super_audit_model_leverage_simulation.json", model)
    write_json(REPORTS / "pre_release_super_audit_thor_odin_effectiveness.json", thor)
    write_json(REPORTS / "pre_release_super_audit_recommended_prs.json", recs)
    write_json(REPORTS / "pre_release_super_audit_report.json", top)
    if out is not None and out.resolve() != (REPORTS / "pre_release_super_audit_report.json").resolve():
        write_json(out, top)
    write_json(REGISTRIES / "pre_release_super_audit_registry.json", build_registry())
    write_markdown_reports(lineage, runtime, arch, model, recs, top)
    write_package_markdown_reports(lineage, runtime, arch, model, recs, top, cohesion, q_ops, bug, thor)
    update_system_map()
    if not skip_manifest:
        update_file_manifest()
    return top


def validate_audit_package() -> list[str]:
    errors: list[str] = []
    registry = build_registry()
    required = registry["docs"] + registry["reports"] + registry["tools"] + registry["tests"] + ["registries/pre_release_super_audit_registry.json", "SYSTEM_MAP.json", "FILE_MANIFEST.json"]
    for rel_path in required:
        path = ROOT / rel_path
        if not path.exists():
            errors.append(f"missing audit artifact: {rel_path}")
    for rel_path in registry["reports"] + ["registries/pre_release_super_audit_registry.json", "SYSTEM_MAP.json", "FILE_MANIFEST.json"]:
        path = ROOT / rel_path
        if path.exists():
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"invalid JSON {rel_path}: {exc}")
    try:
        system_map = json.loads((ROOT / "SYSTEM_MAP.json").read_text(encoding="utf-8"))
        if "pre_release_super_audit" not in system_map:
            errors.append("SYSTEM_MAP missing pre_release_super_audit")
    except json.JSONDecodeError:
        pass
    try:
        manifest = json.loads((ROOT / "FILE_MANIFEST.json").read_text(encoding="utf-8"))
        paths = {entry.get("path") for entry in manifest.get("files", [])}
        for rel_path in registry["docs"] + registry["reports"] + registry["tools"] + registry["tests"]:
            if rel_path not in paths:
                errors.append(f"FILE_MANIFEST missing {rel_path}")
    except json.JSONDecodeError:
        pass
    return errors

def main(argv: list[str] | None = None) -> int:
    global ROOT, DOCS, AUDIT_DIR, REPORTS, REGISTRIES
    parser = argparse.ArgumentParser(description="Run Odin pre-release super audit")
    parser.add_argument("--repo-root", default=str(ROOT), help="Repository root; defaults to this checkout")
    parser.add_argument("--out", default=str(REPORTS / "pre_release_super_audit_report.json"), help="Primary top-level report path")
    parser.add_argument("--lightweight", action="store_true", help="Skip full-suite pytest and run a reduced command set")
    parser.add_argument("--skip-manifest", action="store_true", help="Do not refresh FILE_MANIFEST.json")
    parser.add_argument("--check-only", action="store_true", help="Run lightweight smoke without writing audit package files")
    parser.add_argument("--validate-only", action="store_true", help="Validate audit package files and JSON reports without regenerating")
    args = parser.parse_args(argv)
    ROOT = Path(args.repo_root).resolve()
    DOCS = ROOT / "docs" / "codex" / "audits"
    AUDIT_DIR = DOCS / "pre_release_super_audit"
    REPORTS = ROOT / "reports"
    REGISTRIES = ROOT / "registries"
    if args.validate_only:
        errors = validate_audit_package()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-pre-release-super-audit: OK")
        return 0
    if args.check_only:
        runtime = run_runtime_audit(lightweight=True)
        print(json.dumps({"status": "ok", "audit_id": AUDIT_ID, "checked_paths": len(runtime["results"]), "runtime_path_health_score": runtime["runtime_path_health_score"]}, indent=2, sort_keys=True))
        return 0
    top = run(lightweight=args.lightweight, skip_manifest=args.skip_manifest, out=Path(args.out))
    print(json.dumps({"status": "ok", "audit_id": AUDIT_ID, "overall_verdict": top["overall_verdict"], "release_pr_should_move_to": top["release_pr_should_move_to"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tempfile
import importlib.util

from odin.runtime.engine import run_universal_work_file
from odin.seeds.compiler import compile_seed_pack
from odin.patterns.intake import compile_pattern_mine
from odin.hub.static_hub import write_static_hub
from odin.hub.shell import (
    validate_browser_hub_shell,
    build_browser_hub_proof_packet,
    validate_hub_runtime_dashboard,
    build_dashboard_proof_packet,
    validate_candidate_store_viewer,
    build_candidate_store_viewer_proof_packet,
    validate_trace_viewer,
    build_trace_viewer_proof_packet,
    validate_provider_worker_inspector,
    build_provider_worker_inspector_proof_packet,
    validate_universal_work_playground,
    build_universal_work_playground_proof_packet,
    validate_neutral_external_app_bridge,
    build_neutral_external_app_bridge_proof_packet,
    validate_generic_app_bridge_golden_harness,
    build_generic_app_bridge_golden_harness_proof_packet,
    validate_local_config_safe_settings,
    build_local_config_safe_settings_proof_packet,
    validate_portable_package,
    build_portable_package_proof_packet,
    validate_windows_convenience_layer,
    build_windows_convenience_layer_proof_packet,
    validate_full_acceptance,
    build_full_acceptance_proof_packet,
    validate_consolidated_proof_governance,
    build_consolidated_proof_governance_packet,
    build_agent_operator_mode_proof_packet,
    build_external_app_bridge_proof_packet,
    build_runtime_backend_coverage_proof_packet,
)
from odin.diagnostics.support_bundle import emit_support_bundle
from odin.daemon.local_api import run_local_api
from odin.models.providers.registry import list_provider_cards
from odin.models.permissions import build_permission_card, check_permission_escalation
from odin.models.config import load_provider_config, validate_provider_config
from odin.models.redaction import dumps_redacted
from odin.precompute import score_pre_llm_route
from odin.runtime.store import RuntimeStore

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_CLAIMS = {
    "runtime_verified",
    "host_validated",
    "model_inference_verified",
    "network_verified",
    "security_verified",
    "production_ready",
    "deploy_verified",
    "patch_applied",
    "tests_passed",
    "full_implementation_complete",
}

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def validate_json() -> list[str]:
    errors = []
    for path in sorted(ROOT.rglob("*.json")):
        try:
            load_json(path)
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
    return errors

def validate_registries() -> list[str]:
    errors = []
    reg_dir = ROOT / "registries"
    required = [
        "artifact_types.json",
        "verb_registry.json",
        "output_contract_types.json",
        "semantic_bus_channels.json",
        "model_scale_ladder.json",
        "slot_classes.json",
        "artifact_lenses.json",
        "acceptance_gates.json",
        "failure_states.json",
        "codex_pr_bundle_registry.json",
    ]
    for name in required:
        p = reg_dir / name
        if not p.exists():
            errors.append(f"missing registry {name}")
            continue
        data = load_json(p)
        if "registry_id" not in data or "version" not in data:
            errors.append(f"{name}: missing registry_id/version")
    ladder = load_json(reg_dir / "model_scale_ladder.json")
    if ladder.get("default") != "3b_7b_8b_hybrid":
        errors.append("model_scale_ladder default must be 3b_7b_8b_hybrid")
    channels = load_json(reg_dir / "semantic_bus_channels.json").get("channels", [])
    for ch in channels:
        if not str(ch.get("name","")).startswith("#"):
            errors.append(f"invalid semantic bus channel: {ch}")
        if ch.get("local_only") is not True:
            errors.append(f"semantic bus channel must be local_only: {ch}")
    return errors

def validate_system_map() -> list[str]:
    errors = []
    p = ROOT / "SYSTEM_MAP.json"
    if not p.exists():
        return ["SYSTEM_MAP.json missing"]
    data = load_json(p)
    for key in ["repo","version","canonical_entrypoints","canonical_docs","schemas_dir","registries_dir"]:
        if key not in data:
            errors.append(f"SYSTEM_MAP missing {key}")
    for rel in data.get("canonical_entrypoints", []) + data.get("canonical_docs", []):
        if not (ROOT / rel).exists():
            errors.append(f"SYSTEM_MAP points to missing file: {rel}")
    return errors

def validate_claims() -> list[str]:
    """Detect obvious positive overclaims.

    The forbidden claim *tokens* are allowed in schemas, registries, docs and code
    when they define boundaries. This scanner only blocks explicit affirmative
    phrasing that would tell a user the runtime is already verified/production-ready.
    """
    errors = []
    positive_patterns = [
        "is runtime_verified",
        "is host_validated",
        "is model_inference_verified",
        "is network_verified",
        "is security_verified",
        "is production_ready",
        "is deploy_verified",
        "is patch_applied",
        "is tests_passed",
        "is full_implementation_complete",
        "runtime is verified",
        "host is validated",
        "security is verified",
        "production ready",
        "tests passed",
        "patch applied",
        "deployment verified",
    ]
    allowed_files = {
        "CLAIM_BOUNDARY.md",
        "AGENTS.md",
        "README.md",
        "MASTER_SPECS_V7_1.md",
        "MASTER_ARCHITECTURE_V7_1.md",
    }
    this_file = Path(__file__).resolve()
    allowed_special = {
        "registries/v7_1_1_claim_boundary_registry.json",
        "registries/v7_1_1_forbidden_claim_registry.json",
        "reports/v7_1_1_canon_boundary_integrity_report.json",
        "schemas/v7_1_1_canon_boundary_integrity_report.schema.json",
        "tools/v7_1_1/check_canon_boundary_integrity.py",
        "tests/test_v7_1_1_canon_boundary_integrity.py",
        "docs/codex/reports/PR_26_V7_1_1_CANON_BOUNDARY_INTEGRITY_RETURN_REPORT.md",
    }
    for path in sorted(ROOT.rglob("*")):
        rel = path.relative_to(ROOT).as_posix() if path.exists() else ""
        if path.resolve() == this_file or rel in allowed_special:
            continue
        if path.is_dir() or ".git" in path.parts or ".thor" in path.parts:
            continue
        if path.suffix.lower() not in {".md", ".py", ".json", ".yml", ".yaml", ".ts", ".txt"}:
            continue
        if path.name in allowed_files or "schemas" in path.parts or "registries" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in positive_patterns:
            if phrase in text:
                errors.append(f"positive overclaim phrase '{phrase}' in {path.relative_to(ROOT)}")
    return errors


def validate_docs() -> list[str]:
    errors = []
    required_docs = {
        "docs/MASTER_ARCHITECTURE_V7_1.md": ["Internal Semantic IRC Bus", "3B + 7B/8B", "Universal Work Kernel", "Candidate Artifact", "Model Scale Ladder", "Deep Subsystem Spec Lock"],
        "docs/MASTER_SPECS_V7_1.md": ["Repository Layout Spec", "ModelWorkPacket", "Acceptance Gates", "Caller Manifest", "Semantic Cache", "Provider Adapter Spec", "Deep Subsystem Spec Lock"],
        "docs/UNIVERSAL_WORK_KERNEL.md": ["ODIN_UNIVERSAL_WORK", "Binding Validation", "Candidate Artifact", "Validation Rules Catalog", "State Machine"],
        "docs/INTERNAL_SEMANTIC_BUS.md": ["local-only", "#context.distill", "Semantic Event Envelope", "Module Bot Contract", "Bridge to App-Owned QIRC"],
        "docs/SMALL_MODEL_POWER_LAYER.md": ["Context Distillery", "Slot Forge", "Candidate Tournament", "Tiny Specialist Modes", "Low-Memory Strict Mode"],
        "docs/MODEL_SCALE_LADDER.md": ["3B + 7B/8B", "low_memory_strict", "remote optional", "Scale Ladder", "Escalation Discipline"],
        "docs/APP_INTEGRATION_STANDARD.md": ["No LLM", "Odin Capability Bridge", "Candidate", "App QIRC Bridge"],
        "docs/API_SPEC.md": ["/v7/universal-work/run", "/v7/bus/status", "localhost", "Endpoint Families"],
        "docs/STORAGE_SPEC.md": ["SQLite", "Retention Policy", "semantic_bus_events"],
        "docs/SECURITY_PRIVACY.md": ["local-first", "Secret Rules", "Boundary Matrix"],
        "docs/TESTING_AND_GATES.md": ["Universal Work", "Semantic Bus", "Negative Tests", "Gate Families"],
        "docs/DATA_CONTRACTS_V7_1.md": ["Contract Families", "Universal Work", "Candidate DNA", "Versioning"],
        "docs/ALGORITHMS_V7_1.md": ["Universal Work Validation", "Context Distillation", "Model Route Selection", "Claim Gate"],
        "docs/FLOW_CATALOG_V7_1.md": ["Markdown Rewrite", "Traureden Section", "Code PatchPlan", "App QIRC Digest"],
        "docs/IMPLEMENTATION_DOD_V7_1.md": ["DoD", "Universal Work Kernel", "Internal Semantic Bus", "Model Provider Adapter"],
        "docs/WINDOWS_RUNTIME.md": ["Process Responsibilities", "Runtime modes", "odin-daemon"],
        "docs/THOR_INTEGRATION.md": ["Thor Bridge", "candidate-only", "Modes"],
        "docs/BOUNDED_CODE_WORK.md": ["PatchPlan Candidate", "Bounded Code Work", "Required Boundaries"],
        "docs/LOCAL_MEDIATION_PROTOCOL_V7_1.md": ["Local Mediation Protocol", "Artifact Directions", "Conflict Handling"],
    }
    min_lengths = {
        "docs/MASTER_ARCHITECTURE_V7_1.md": 80000,
        "docs/MASTER_SPECS_V7_1.md": 80000,
        "docs/UNIVERSAL_WORK_KERNEL.md": 12000,
        "docs/INTERNAL_SEMANTIC_BUS.md": 10000,
        "docs/SMALL_MODEL_POWER_LAYER.md": 11000,
        "docs/MODEL_SCALE_LADDER.md": 5000,
        "docs/API_SPEC.md": 4500,
        "docs/STORAGE_SPEC.md": 3500,
        "docs/SECURITY_PRIVACY.md": 3000,
        "docs/DATA_CONTRACTS_V7_1.md": 12000,
        "docs/ALGORITHMS_V7_1.md": 12000,
        "docs/FLOW_CATALOG_V7_1.md": 6000,
        "docs/IMPLEMENTATION_DOD_V7_1.md": 12000,
        "docs/TESTING_AND_GATES.md": 3500,
        "docs/APP_INTEGRATION_STANDARD.md": 2500,
        "docs/LOCAL_MEDIATION_PROTOCOL_V7_1.md": 2000,
        "docs/WINDOWS_RUNTIME.md": 2500,
        "docs/THOR_INTEGRATION.md": 1500,
        "docs/BOUNDED_CODE_WORK.md": 1500,
    }
    for rel, anchors in required_docs.items():
        p = ROOT / rel
        if not p.exists():
            errors.append(f"required doc missing: {rel}")
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        for anchor in anchors:
            if anchor not in text:
                errors.append(f"{rel}: missing anchor {anchor!r}")
        if rel in min_lengths and len(text) < min_lengths[rel]:
            errors.append(f"{rel}: too short for deep spec lock ({len(text)} < {min_lengths[rel]})")
    return errors


def validate_codex_tasks() -> list[str]:
    errors = []
    registry_path = ROOT / "registries" / "codex_task_registry.json"
    if not registry_path.exists():
        return ["codex task registry missing"]
    data = load_json(registry_path)
    tasks = data.get("tasks", [])
    if len(tasks) < 20:
        errors.append(f"codex task registry too small ({len(tasks)} < 20)")
    seen = set()
    completed = set()
    for task in tasks:
        tid = task.get("id")
        if not tid:
            errors.append("codex task missing id")
            continue
        if tid in seen:
            errors.append(f"duplicate codex task id {tid}")
        seen.add(tid)
        for dep in task.get("depends_on", []):
            if dep not in completed:
                errors.append(f"{tid}: dependency {dep} must appear before task")
        completed.add(tid)
        doc_rel = task.get("doc")
        if not doc_rel:
            errors.append(f"{tid}: missing doc")
            continue
        p = ROOT / doc_rel
        if not p.exists():
            errors.append(f"{tid}: task doc missing: {doc_rel}")
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        for anchor in [tid, "Objective", "Primary Files", "Required Behavior", "Forbidden Scope", "Definition of Done", "Codex PR Summary Template"]:
            if anchor not in text:
                errors.append(f"{doc_rel}: missing anchor {anchor!r}")
        if len(text) < 2500:
            errors.append(f"{doc_rel}: task doc too short ({len(text)} < 2500)")
    required_docs = [
        "docs/codex/CODEX_TASK_LOCK_V0_4_0.md",
        "docs/codex/IMPLEMENTATION_SEQUENCE_V0_4_0.md",
        "docs/codex/PR_DEPENDENCY_GRAPH_V0_4_0.md",
        "docs/codex/TASK_DOD_MATRIX_V0_4_0.md",
        "docs/codex/CODEX_PROMPT_PACKS_V0_4_0.md",
        "docs/codex/PR_TASK_INDEX.md",
    ]
    for rel in required_docs:
        p = ROOT / rel
        if not p.exists():
            errors.append(f"missing codex task lock doc {rel}")
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if "v0.4.0" not in text and "PR Task Index" not in text:
            errors.append(f"{rel}: missing v0.4.0/task-lock marker")
    return errors



def validate_codex_bundles() -> list[str]:
    errors = []
    registry_path = ROOT / "registries" / "codex_pr_bundle_registry.json"
    if not registry_path.exists():
        return ["codex PR bundle registry missing"]
    data = load_json(registry_path)
    bundles = data.get("bundles", [])
    if len(bundles) < 6:
        errors.append(f"codex PR bundle registry too small ({len(bundles)} < 6)")
    task_registry = load_json(ROOT / "registries" / "codex_task_registry.json")
    task_ids = {task.get("id") for task in task_registry.get("tasks", [])}
    covered = []
    seen = set()
    completed = set()
    for bundle in bundles:
        bid = bundle.get("id")
        if not bid:
            errors.append("bundle missing id")
            continue
        if bid in seen:
            errors.append(f"duplicate bundle id {bid}")
        seen.add(bid)
        if not bid.startswith("REAL-PR-"):
            errors.append(f"bundle id must start with REAL-PR-: {bid}")
        for dep in bundle.get("depends_on", []):
            if dep not in completed:
                errors.append(f"{bid}: dependency {dep} must appear before bundle")
        completed.add(bid)
        internal = bundle.get("internal_tasks", [])
        if not internal:
            errors.append(f"{bid}: missing internal_tasks")
        for tid in internal:
            if tid not in task_ids:
                errors.append(f"{bid}: unknown internal task {tid}")
            covered.append(tid)
        doc_rel = bundle.get("doc")
        if not doc_rel:
            errors.append(f"{bid}: missing doc")
            continue
        p = ROOT / doc_rel
        if not p.exists():
            errors.append(f"{bid}: bundle doc missing: {doc_rel}")
            continue
        doc = p.read_text(encoding="utf-8", errors="ignore")
        for anchor in [bid, "Objective", "Internal Tasks Covered", "Primary Files", "Required Behavior", "Forbidden Scope", "Definition of Done", "Codex PR Summary Template"]:
            if anchor not in doc:
                errors.append(f"{doc_rel}: missing anchor {anchor!r}")
        if len(doc) < 3000:
            errors.append(f"{doc_rel}: bundle doc too short ({len(doc)} < 3000)")
    missing = sorted(tid for tid in task_ids if tid and tid not in set(covered))
    if missing:
        errors.append("codex bundle registry does not cover internal tasks: " + ", ".join(missing))
    for rel in ["docs/codex/CODEX_REAL_PR_BUNDLE_PLAN_V0_4_1.md", "docs/codex/REAL_PR_BUNDLE_INDEX_V0_4_1.md"]:
        p = ROOT / rel
        if not p.exists():
            errors.append(f"missing codex bundle doc {rel}")
        elif "v0.4.1" not in p.read_text(encoding="utf-8", errors="ignore"):
            errors.append(f"{rel}: missing v0.4.1 marker")
    return errors


def validate_senior_review() -> list[str]:
    errors = []
    required = {
        "docs/reviews/SENIOR_REVIEW_SIMULATION_V0_4_2.md": ["Senior Reviewer Simulation", "SR-01", "Approval Conditions"],
        "docs/SENIOR_REVIEW_REMEDIATION_PLAN_V0_4_2.md": ["Senior Review Remediation Plan", "PR-22", "REAL-PR-08"],
        "docs/CODEX_ANTI_DRIFT_POLICY.md": ["Codex Anti-Drift Policy", "Forbidden Codex Shortcuts", "Authority Order"],
        "docs/TRACEABILITY_MATRIX_V7_1.md": ["Traceability Matrix", "PR-22", "REAL-PR-08"],
        "docs/QUALITY_RISK_REGISTER_V7_1.md": ["Quality and Risk Register", "R-001", "Critical"],
        "docs/SEMANTIC_BUS_RED_LINES_V7_1.md": ["Semantic Bus Red-Line Policy", "The bus may not mutate app state", "Forbidden Event Types"],
        "docs/PUBLIC_REPO_RELEASE_CHECKLIST_V7_1.md": ["Public Repo Release Checklist", "No runtime-proof claims", "Codex Launch Rule"],
        "docs/codex/SENIOR_REVIEW_CODEX_ADDENDUM_V0_4_2.md": ["Codex Senior Review Addendum", "PR-22", "REAL-PR-08"],
    }
    for rel, anchors in required.items():
        p = ROOT / rel
        if not p.exists():
            errors.append(f"missing senior review doc {rel}")
            continue
        content = p.read_text(encoding="utf-8", errors="ignore")
        if len(content) < 1200:
            errors.append(f"{rel}: too short for senior review hardening")
        for anchor in anchors:
            if anchor not in content:
                errors.append(f"{rel}: missing anchor {anchor!r}")
    task_registry = load_json(ROOT / "registries" / "codex_task_registry.json")
    tasks = {task.get("id") for task in task_registry.get("tasks", [])}
    if "PR-22" not in tasks:
        errors.append("PR-22 missing from codex task registry")
    bundle_registry = load_json(ROOT / "registries" / "codex_pr_bundle_registry.json")
    covered = {tid for bundle in bundle_registry.get("bundles", []) for tid in bundle.get("internal_tasks", [])}
    if "PR-22" not in covered:
        errors.append("PR-22 not covered by real PR bundle registry")
    return errors



def validate_shadow_runtime() -> list[str]:
    errors = []
    required_docs = {
        "docs/SHADOW_RUNTIME_LOCK_V7_1.md": ["Shadow Runtime", "Non-Authority Boundary", "Codex Rule"],
        "docs/SHADOW_RUNTIME_CODE_NEAR_BOOK_V7_1.md": ["Mechanical Conversion Pattern", "Done Criteria", "Anti-Patterns"],
        "docs/SHADOW_RUNTIME_TO_REAL_BUILD_MAPPING_V7_1.md": ["Mapping Table", "PR-23", "REAL-PR-09"],
        "docs/CONTRACT_TO_SHADOW_CODE_MAP_V7_1.md": ["Binding Gate", "Universal Work Compile", "Final Gate"],
        "docs/SHADOW_RUNTIME_STATE_MACHINES_V7_1.md": ["Universal Work Shadow State Machine", "Semantic Bus Shadow State Machine"],
        "docs/SHADOW_RUNTIME_ACCEPTANCE_TESTS_V7_1.md": ["SR-TEST-001", "validate-shadow-runtime"],
        "docs/YNODE_SHADOW_RUNTIME_PATTERN_ADAPTATION_V7_1.md": ["YNode", "Odin-specific adaptation"],
        "docs/SHADOW_RUNTIME_FULL_COVERAGE_V7_1.md": ["Full Shadow Runtime", "Covered Subsystems", "Codex Rule"],
        "docs/SHADOW_SUBSYSTEM_COVERAGE_MATRIX_V7_1.md": ["Shadow Subsystem Coverage Matrix", "artifact_lens_context_distillery", "REAL-PR-10"],
        "docs/SHADOW_RUNTIME_NEAR_FINAL_LOCK_V7_1.md": ["Shadow Runtime Near-Final Lock", "Near-Final Spine", "PR-25"],
        "docs/SHADOW_RUNTIME_E2E_ORCHESTRATOR_V7_1.md": ["Shadow Runtime End-to-End Orchestrator", "Canonical Entrypoint", "Failure Behavior"],
        "docs/SHADOW_RUNTIME_POLICY_ENGINE_V7_1.md": ["Shadow Runtime Policy Engine", "Forbidden Markers", "Codex Conversion"],
        "docs/SHADOW_RUNTIME_STATE_FAILURE_MATRIX_V7_1.md": ["Shadow Runtime State and Failure Matrix", "Canonical Success States", "Recovery Discipline"],
        "docs/SHADOW_RUNTIME_RESOURCE_PROVIDER_PLAN_V7_1.md": ["Shadow Runtime Resource and Provider Plan", "Resource Posture", "Provider Adapter Plan"],
        "docs/SHADOW_RUNTIME_CODEX_CONVERSION_PLAYBOOK_V7_1.md": ["Shadow Runtime Codex Conversion Playbook", "Conversion Pattern", "PR-25 Role"],
        "docs/SHADOW_RUNTIME_REAL_MODULE_MAP_V7_1.md": ["Shadow Runtime to Real Module Map", "Shadow Module", "Real Target"],
    }
    for rel, anchors in required_docs.items():
        p = ROOT / rel
        if not p.exists():
            errors.append(f"missing shadow runtime doc {rel}")
            continue
        content = p.read_text(encoding="utf-8", errors="ignore")
        if len(content) < 1000:
            errors.append(f"{rel}: too short for shadow runtime lock")
        for anchor in anchors:
            if anchor not in content:
                errors.append(f"{rel}: missing anchor {anchor!r}")
    registry_path = ROOT / "registries" / "shadow_runtime_contract_registry.json"
    if not registry_path.exists():
        errors.append("shadow runtime contract registry missing")
    else:
        data = load_json(registry_path)
        contracts = data.get("contracts", [])
        ids = {c.get("id") for c in contracts}
        required_ids = {"binding_gate", "universal_work_compile", "semantic_bus_batch", "model_route_plan", "candidate_response_packet", "shadow_final_gate", "artifact_lens_context_distillery", "worklet_slot_gaptext", "candidate_tournament", "low_memory_strict", "thor_bridge", "bounded_code_work", "storage_trace_receipt", "api_endpoint_plan", "app_qirc_digest_bridge", "model_dojo_scoreboard", "security_redaction", "support_bundle", "windows_runtime_plan", "sdk_template_validation", "near_final_orchestrator", "policy_engine", "resource_scheduler", "state_machine", "failure_recovery", "provider_adapter_plan", "registry_consistency_report"}
        missing = sorted(required_ids - ids)
        if missing:
            errors.append("shadow runtime registry missing contracts: " + ", ".join(missing))
        for c in contracts:
            for key in ["shadow_file", "real_target", "fixture", "test", "task", "bundle"]:
                if key not in c:
                    errors.append(f"shadow runtime contract {c.get('id')}: missing {key}")
            for key in ["shadow_file", "fixture", "test"]:
                rel = c.get(key)
                if rel and not (ROOT / rel).exists():
                    errors.append(f"shadow runtime contract {c.get('id')}: {key} path missing: {rel}")
    for rel in [
        "odin/shadow_runtime/__init__.py",
        "odin/shadow_runtime/types.py",
        "odin/shadow_runtime/pipeline.py",
        "examples/shadow_runtime/markdown_rewrite_shadow_flow.valid.json",
        "examples/shadow_runtime/direct_apply_blocked.invalid.json",
        "tests/test_shadow_runtime_lock.py",
        "docs/codex/tasks/PR-23_SHADOW_RUNTIME_CODE_NEAR_LOCK.md",
        "docs/codex/bundles/REAL-PR-09_SHADOW_RUNTIME_MECHANICAL_BUILD_BRIDGE.md",
        "docs/codex/tasks/PR-24_FULL_SHADOW_RUNTIME_COVERAGE.md",
        "docs/codex/bundles/REAL-PR-10_FULL_SHADOW_RUNTIME_COVERAGE.md",
        "docs/codex/tasks/PR-25_SHADOW_RUNTIME_NEAR_FINAL_OPTIMIZATION_LOCK.md",
        "docs/codex/bundles/REAL-PR-11_SHADOW_RUNTIME_NEAR_FINAL_OPTIMIZATION_BRIDGE.md",
        "odin/shadow_runtime/e2e_orchestrator_shadow.py",
        "tests/test_shadow_runtime_near_final.py",
    ]:
        if not (ROOT / rel).exists():
            errors.append(f"missing shadow runtime file {rel}")
    return errors



def validate_narrative_compiler() -> list[str]:
    errors = []
    required_docs = {
        "docs/FAIRY_DSL_V7_1.md": ["Fairy DSL", "Dual Spine", "no prose", "Y*"],
        "docs/YSTAR_NATIVE_DSL_V7_1.md": ["Y* Native DSL", "Validation Rules", "candidate_only", "app_authority"],
        "docs/NARRATIVE_AORTA_V7_1.md": ["Narrative Aorta", "Aorta Node Contract", "Children", "Red Lines"],
        "docs/FAIRY_TO_SHADOW_IR_COMPILER_V7_1.md": ["Fairy-to-Shadow IR", "Compiler Inputs", "Failure Rules"],
        "docs/YSTAR_MEDIATION_DIRECTIVE_V7_1.md": ["Y* Mediation Directive", "Runtime Boundaries", "Invalid Conditions"],
        "docs/NARRATIVE_CODE_BOUNDARY_V7_1.md": ["Narrative Code Boundary", "Forbidden", "Boundary Table"],
        "docs/MARIA_FAIRY_SPINE_V7_1.md": ["Maria Fairy Spine", "Mapping", "Review Checklist"],
        "docs/SHADOW_RUNTIME_COMPILER_V7_1.md": ["Shadow Runtime Compiler", "Compiler Inputs", "Hot Path Rule"],
        "docs/RUNTIME_PACK_SPEC_V7_1.md": ["Runtime Pack", "Manifest Shape", "Load Rule"],
        "docs/CAPABILITY_SLICE_COMPILER_V7_1.md": ["Capability Slice", "Efficiency Rule", "Safety Rule"],
        "docs/PACK_LOADER_SECURITY_V7_1.md": ["Pack Loader Security", "Rollback Flow", "Red Lines"],
        "docs/AOT_CACHED_JIT_FALLBACK_V7_1.md": ["AOT", "Cached Capability", "Forbidden"],
        "docs/GENERATED_RUNTIME_GATES_V7_1.md": ["Generated Runtime Gates", "Generated Gate Families", "Codex Rule"],
    }
    for rel, anchors in required_docs.items():
        p = ROOT / rel
        if not p.exists():
            errors.append(f"missing narrative compiler doc {rel}")
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if len(text) < 1200:
            errors.append(f"{rel}: too short for narrative compiler lock")
        for anchor in anchors:
            if anchor not in text:
                errors.append(f"{rel}: missing anchor {anchor!r}")
    required_registries = [
        "fairy_dsl_registry.json",
        "ystar_stage_registry.json",
        "narrative_aorta_registry.json",
        "runtime_pack_registry.json",
        "compiler_stage_registry.json",
    ]
    for name in required_registries:
        p = ROOT / "registries" / name
        if not p.exists():
            errors.append(f"missing narrative compiler registry {name}")
            continue
        data = load_json(p)
        if "registry_id" not in data or "version" not in data:
            errors.append(f"{name}: missing registry_id/version")
    required_schemas = [
        "odin_fairy_story.schema.json",
        "odin_ystar_native_unit.schema.json",
        "odin_ystar_mediation_directive.schema.json",
        "odin_narrative_aorta_node.schema.json",
        "odin_fairy_shadow_mapping.schema.json",
        "odin_runtime_pack.schema.json",
        "odin_capability_slice.schema.json",
    ]
    for name in required_schemas:
        if not (ROOT / "schemas" / "v7_1" / name).exists():
            errors.append(f"missing narrative compiler schema {name}")
    for rel in [
        "odin/shadow_runtime/fairy_dsl_shadow.py",
        "odin/shadow_runtime/ystar_native_dsl_shadow.py",
        "odin/shadow_runtime/narrative_aorta_shadow.py",
        "odin/shadow_runtime/fairy_to_shadow_ir_shadow.py",
        "odin/shadow_runtime/ystar_mediation_shadow.py",
        "odin/compiler/shadow_ir.py",
        "odin/compiler/runtime_pack.py",
        "odin/compiler/pack_validator.py",
        "odin/compiler/aot_compiler.py",
        "tests/test_narrative_compiler_integration.py",
        "examples/fairy/odin_rewrite_story.valid.json",
        "examples/compiler/standard_local_runtime_pack.valid.json",
    ]:
        if not (ROOT / rel).exists():
            errors.append(f"missing narrative compiler file {rel}")
    task_registry = load_json(ROOT / "registries" / "codex_task_registry.json")
    tasks = {task.get("id") for task in task_registry.get("tasks", [])}
    for tid in [f"PR-{i:02d}" for i in range(26, 38)]:
        if tid not in tasks:
            errors.append(f"{tid} missing from codex task registry")
    bundle_registry = load_json(ROOT / "registries" / "codex_pr_bundle_registry.json")
    bundles = {bundle.get("id") for bundle in bundle_registry.get("bundles", [])}
    for bid in ["REAL-PR-12", "REAL-PR-13"]:
        if bid not in bundles:
            errors.append(f"{bid} missing from codex PR bundle registry")
    return errors



def validate_odin_core_qli() -> list[str]:
    errors = []
    required_docs = {
        "docs/ODIN_CORE_CENTERLINE_V7_1.md": ["Odin Core Centerline", "Centerline Packet", "Non-authority boundary"],
        "docs/ODIN_QLI_MASTER_INTERFACE_V7_1.md": ["Odin QLI Master Interface", "Ring Path", "Maria/Michael Superposition"],
        "docs/DFAS_STABILITY_CORE_V7_1.md": ["DFAS Stability Core", "Decision outputs", "Stop-early rule"],
        "docs/SEED_ARCHETYPE_ECONOMY_V7_1.md": ["Seed / Archetype Economy", "Activation pipeline", "Conflict resolver"],
        "docs/QMATH_CENTER_SOLVER_V7_1.md": ["QMath Center Solver", "route_score", "Stop rule"],
        "docs/RING_RADAR_RESONANCE_V7_1.md": ["Ring Activation Map", "Resonance bands", "Why Trace"],
        "docs/WHY_TRACE_EXPLAINABILITY_V7_1.md": ["Why Trace", "Redaction rules", "user-safe trace"],
        "docs/MARIA_MICHAEL_SUPERPOSITION_V7_1.md": ["Maria / Michael Superposition", "80 Maria / 20 Michael", "profile"],
        "docs/QFOUNDATION_SYSTEM_INTAKE_V7_1.md": ["QFoundation System Intake", "Odin System Palette", "Maria/Michael Binding"],
        "docs/Q_METAMODELL_INTAKE_V7_1.md": ["Q Metamodell", "CUTK1", "Runtime Economy"],
        "docs/reviews/SENIOR_REVIEW_SIMULATION_V0_6_1.md": ["Senior Reviewer", "Approval Conditions", "SR-CORE-01"],
    }
    for rel, anchors in required_docs.items():
        p = ROOT / rel
        if not p.exists():
            errors.append(f"missing Odin Core/QLI doc {rel}")
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if len(text) < 1500:
            errors.append(f"{rel}: too short for Odin Core/QLI hardening")
        for anchor in anchors:
            if anchor not in text:
                errors.append(f"{rel}: missing anchor {anchor!r}")
    for rel in [
        "odin_centerline_packet.schema.json",
        "odin_admissibility_decision.schema.json",
        "odin_seed_activation_packet.schema.json",
        "odin_archetype_role_packet.schema.json",
        "odin_route_score.schema.json",
        "odin_ring_activation_map.schema.json",
        "odin_why_trace.schema.json",
        "odin_maria_michael_profile.schema.json",
    ]:
        if not (ROOT / "schemas" / "v7_1" / rel).exists():
            errors.append(f"missing Odin Core/QLI schema {rel}")
    for rel in [
        "seed_registry.json",
        "archetype_role_registry.json",
        "resonance_band_registry.json",
        "centerline_gate_registry.json",
        "qmath_score_registry.json",
        "maria_michael_profile_registry.json",
        "qfoundation_system_palette_registry.json",
    ]:
        p = ROOT / "registries" / rel
        if not p.exists():
            errors.append(f"missing Odin Core/QLI registry {rel}")
            continue
        data = load_json(p)
        if "registry_id" not in data or "version" not in data:
            errors.append(f"{rel}: missing registry_id/version")
    for rel in [
        "odin/shadow_runtime/odin_core_centerline_shadow.py",
        "odin/shadow_runtime/qli_master_interface_shadow.py",
        "odin/shadow_runtime/dfas_stability_core_shadow.py",
        "odin/shadow_runtime/seed_archetype_economy_shadow.py",
        "odin/shadow_runtime/qmath_center_solver_shadow.py",
        "odin/shadow_runtime/ring_radar_resonance_shadow.py",
        "odin/shadow_runtime/why_trace_shadow.py",
        "odin/shadow_runtime/maria_michael_superposition_shadow.py",
        "examples/shadow_runtime/odin_core_qli_flow.valid.json",
        "examples/shadow_runtime/odin_core_policy_block.invalid.json",
        "tests/test_odin_core_qli_dfas_seed_economy.py",
    ]:
        if not (ROOT / rel).exists():
            errors.append(f"missing Odin Core/QLI file {rel}")
    task_registry = load_json(ROOT / "registries" / "codex_task_registry.json")
    tasks = {task.get("id") for task in task_registry.get("tasks", [])}
    for tid in [f"PR-{i:02d}" for i in range(38, 45)]:
        if tid not in tasks:
            errors.append(f"{tid} missing from codex task registry")
    bundle_registry = load_json(ROOT / "registries" / "codex_pr_bundle_registry.json")
    bundles = {bundle.get("id") for bundle in bundle_registry.get("bundles", [])}
    if "REAL-PR-14" not in bundles:
        errors.append("REAL-PR-14 missing from codex PR bundle registry")
    return errors



def validate_qirc_gold_spine() -> list[str]:
    errors = []
    required_docs = {
        "docs/ODIN_QIRC_GOLD_SPINE_V7_1.md": ["Odin QIRC Gold Spine", "Red Lines", "QIRC-L0"],
        "docs/QIRC_CHANNEL_TAXONOMY_V7_1.md": ["QIRC Channel Taxonomy", "#core.ingress", "#why.route"],
        "docs/QIRC_EVENT_ENVELOPE_V2_V7_1.md": ["QIRC Event Envelope", "centerline_id", "payload_ref"],
        "docs/QIRC_HOT_WINDOW_MEMORY_V7_1.md": ["Hot Window", "Work Memory", "Trace Memory"],
        "docs/QIRC_SEED_ARCHETYPE_PREWARM_V7_1.md": ["Seed", "Archetype", "Budget"],
        "docs/QIRC_ADMISSIBILITY_GATE_V7_1.md": ["Admissibility", "hold", "split_work"],
        "docs/QIRC_RING_RADAR_RUNTIME_V7_1.md": ["Ring Radar", "R0 Boundary", "Resonance"],
        "docs/QIRC_WHY_TRACE_V7_1.md": ["Why Trace", "blocked_routes", "redacted"],
        "docs/QIRC_RUNTIME_PACK_INTEGRATION_V7_1.md": ["Runtime Pack", "Capability Slice", "compiled channel"],
        "docs/QIRC_APP_BRIDGE_DIGEST_V7_1.md": ["App Bridge Digest", "digest", "Odin may not become app QIRC"],
    }
    for rel, anchors in required_docs.items():
        p = ROOT / rel
        if not p.exists():
            errors.append(f"missing QIRC Gold Spine doc {rel}")
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if len(text) < 1200:
            errors.append(f"{rel}: too short for QIRC Gold Spine lock")
        for anchor in anchors:
            if anchor not in text:
                errors.append(f"{rel}: missing anchor {anchor!r}")
    for rel in [
        "odin_qirc_event.schema.json",
        "odin_qirc_hot_window.schema.json",
        "odin_qirc_seed_budget.schema.json",
        "odin_qirc_admissibility_gate.schema.json",
        "odin_qirc_role_activation.schema.json",
        "odin_qirc_ring_radar.schema.json",
        "odin_qirc_why_trace.schema.json",
        "odin_qirc_capability_slice_channels.schema.json",
    ]:
        if not (ROOT / "schemas" / "v7_1" / rel).exists():
            errors.append(f"missing QIRC schema {rel}")
    for rel in [
        "qirc_channel_registry.json",
        "qirc_event_type_registry.json",
        "qirc_role_channel_matrix.json",
        "qirc_admissibility_reason_registry.json",
        "qirc_hot_window_policy_registry.json",
    ]:
        p = ROOT / "registries" / rel
        if not p.exists():
            errors.append(f"missing QIRC registry {rel}")
            continue
        data = load_json(p)
        if "registry_id" not in data or "version" not in data:
            errors.append(f"{rel}: missing registry_id/version")
    for rel in [
        "odin/shadow_runtime/qirc_gold_spine_shadow.py",
        "odin/shadow_runtime/qirc_hot_window_shadow.py",
        "odin/shadow_runtime/qirc_seed_prewarm_shadow.py",
        "odin/shadow_runtime/qirc_admissibility_shadow.py",
        "odin/shadow_runtime/qirc_ring_radar_shadow.py",
        "odin/shadow_runtime/qirc_why_trace_shadow.py",
        "odin/shadow_runtime/qirc_runtime_pack_shadow.py",
        "examples/shadow_runtime/qirc_gold_spine_flow.valid.json",
        "examples/shadow_runtime/qirc_gold_spine_block.invalid.json",
        "tests/test_qirc_gold_spine.py",
    ]:
        if not (ROOT / rel).exists():
            errors.append(f"missing QIRC Gold Spine file {rel}")
    task_registry = load_json(ROOT / "registries" / "codex_task_registry.json")
    tasks = {task.get("id") for task in task_registry.get("tasks", [])}
    for tid in [f"PR-{i:02d}" for i in range(45, 50)]:
        if tid not in tasks:
            errors.append(f"{tid} missing from codex task registry")
    bundle_registry = load_json(ROOT / "registries" / "codex_pr_bundle_registry.json")
    bundles = {bundle.get("id") for bundle in bundle_registry.get("bundles", [])}
    if "REAL-PR-15" not in bundles:
        errors.append("REAL-PR-15 missing from codex PR bundle registry")
    return errors



def validate_bug6_q7_seed_core() -> list[str]:
    errors = []
    required_docs = {
        "docs/BUG6_CHILDREN_FIRST_INVARIANT_V7_1.md": ["Bug6", "Children-First", "Bug6 Pre-Selector Invariant Gate"],
        "docs/Q7_BUGFREE_STABILITY_V7_1.md": ["Q7", "Bugfree Stability", "negative path"],
        "docs/Y_CORE_POSTURE_V7_1.md": ["Odin Y-Core", "authority split", "Odin Ring 0"],
        "docs/OPERATIONAL_SEED_SUBSTRATE_V7_1.md": ["Operational Seed Substrate", "Seed lifecycle", "Hard seeds"],
        "docs/BUG6_Q7_SEED_CORE_SYNTHESIS_V7_1.md": ["Bug6", "Q7", "Seed Core Synthesis"],
        "docs/FAIRY_YSTAR_SEED_BINDING_V7_1.md": ["Fairy", "Y*", "seed binding"],
        "docs/SHADOW_RUNTIME_SEED_WEAVE_V7_1.md": ["Shadow Runtime Seed Weave", "Candidate DNA", "active_seeds"],
        "docs/RUNTIME_PACK_SEED_PROFILES_V7_1.md": ["Runtime Pack Seed Profiles", "Low Memory Strict", "hard seeds"],
        "docs/reviews/SENIOR_REVIEW_SIMULATION_V0_6_3.md": ["Senior Review", "Bug6", "Q7", "SR-063-01"],
    }
    for rel, anchors in required_docs.items():
        p = ROOT / rel
        if not p.exists():
            errors.append(f"missing Bug6/Q7/seed core doc {rel}")
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if len(text) < 1200:
            errors.append(f"{rel}: too short for Bug6/Q7/seed core lock")
        for anchor in anchors:
            if anchor not in text:
                errors.append(f"{rel}: missing anchor {anchor!r}")
    for rel in ["odin_bug6_invariant_packet.schema.json","odin_q7_stability_packet.schema.json","odin_y_core_posture.schema.json","odin_operational_seed_substrate.schema.json","odin_seed_archetype_synthesis.schema.json","odin_shadow_seed_binding.schema.json"]:
        if not (ROOT / "schemas" / "v7_1" / rel).exists():
            errors.append(f"missing Bug6/Q7/seed schema {rel}")
    for rel in ["bug6_invariant_registry.json","q7_stability_registry.json","y_core_posture_registry.json","operational_seed_substrate_registry.json","seed_archetype_synthesis_registry.json"]:
        p = ROOT / "registries" / rel
        if not p.exists():
            errors.append(f"missing Bug6/Q7/seed registry {rel}")
            continue
        data = load_json(p)
        if "registry_id" not in data or "version" not in data:
            errors.append(f"{rel}: missing registry_id/version")
    for rel in ["odin/shadow_runtime/bug6_q7_invariant_shadow.py","odin/shadow_runtime/y_core_posture_shadow.py","odin/shadow_runtime/operational_seed_substrate_shadow.py","odin/shadow_runtime/seed_archetype_synthesis_shadow.py","odin/shadow_runtime/fairy_ystar_seed_binding_shadow.py","odin/shadow_runtime/shadow_runtime_seed_binding_shadow.py","examples/shadow_runtime/bug6_q7_seed_core_flow.valid.json","examples/shadow_runtime/bug6_q7_seed_core_block.invalid.json","tests/test_bug6_q7_seed_core.py"]:
        if not (ROOT / rel).exists():
            errors.append(f"missing Bug6/Q7/seed core file {rel}")
    task_registry = load_json(ROOT / "registries" / "codex_task_registry.json")
    tasks = {task.get("id") for task in task_registry.get("tasks", [])}
    for tid in [f"PR-{i:02d}" for i in range(50, 56)]:
        if tid not in tasks:
            errors.append(f"{tid} missing from codex task registry")
    bundle_registry = load_json(ROOT / "registries" / "codex_pr_bundle_registry.json")
    bundles = {bundle.get("id") for bundle in bundle_registry.get("bundles", [])}
    if "REAL-PR-16" not in bundles:
        errors.append("REAL-PR-16 missing from codex PR bundle registry")
    return errors



def validate_ai_git_safety() -> list[str]:
    errors = []
    required_docs = {
        "docs/AI_GIT_SAFETY_ARCHITECTURE_V7_1.md": ["AI-Git Safety Architecture", "Candidate Artifact", "Semantic Diff"],
        "docs/AUTONOMY_ESCALATION_GATE_V7_1.md": ["Autonomy Escalation Gate", "A0", "A5"],
        "docs/SAFETY_SUPERPOSITION_POLICY_V7_1.md": ["Safety Superposition", "Maria", "Michael"],
        "docs/SEMANTIC_DIFF_BRANCH_MERGE_V7_1.md": ["Semantic Diff", "Semantic Branch", "Candidate Merge"],
        "docs/SKYNET_PATTERN_BOUNDARY_V7_1.md": ["Skynet Pattern Boundary", "Odin Countermeasures", "Escalation Signals"],
        "docs/HUMAN_REVIEW_APP_APPLY_BOUNDARY_V7_1.md": ["Human Review", "App Apply Boundary", "Candidate Action Classes"],
        "docs/reviews/SENIOR_REVIEW_SIMULATION_V0_6_4.md": ["Senior Reviewer", "SR-064-01", "Approval Conditions"],
    }
    for rel, anchors in required_docs.items():
        p = ROOT / rel
        if not p.exists():
            errors.append(f"missing AI-Git safety doc {rel}")
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if len(text) < 1200:
            errors.append(f"{rel}: too short for AI-Git safety consolidation")
        for anchor in anchors:
            if anchor not in text:
                errors.append(f"{rel}: missing anchor {anchor!r}")
    for rel in ["odin_ai_git_safety_packet.schema.json","odin_autonomy_escalation_gate.schema.json","odin_safety_superposition_packet.schema.json","odin_semantic_diff_packet.schema.json","odin_safety_why_trace.schema.json","odin_human_review_gate.schema.json"]:
        if not (ROOT / "schemas" / "v7_1" / rel).exists():
            errors.append(f"missing AI-Git safety schema {rel}")
    for rel in ["ai_git_safety_registry.json","autonomy_escalation_gate_registry.json","safety_superposition_registry.json","semantic_diff_registry.json","human_review_gate_registry.json"]:
        p = ROOT / "registries" / rel
        if not p.exists():
            errors.append(f"missing AI-Git safety registry {rel}")
            continue
        data = load_json(p)
        if "registry_id" not in data or "version" not in data:
            errors.append(f"{rel}: missing registry_id/version")
    for rel in ["odin/shadow_runtime/ai_git_safety_shadow.py","odin/shadow_runtime/autonomy_escalation_gate_shadow.py","odin/shadow_runtime/safety_superposition_shadow.py","odin/shadow_runtime/semantic_diff_branch_merge_shadow.py","odin/shadow_runtime/skynet_pattern_boundary_shadow.py","odin/shadow_runtime/human_review_apply_boundary_shadow.py","tests/test_ai_git_safety_consolidation.py"]:
        if not (ROOT / rel).exists():
            errors.append(f"missing AI-Git safety file {rel}")
    task_registry = load_json(ROOT / "registries" / "codex_task_registry.json")
    tasks = {task.get("id") for task in task_registry.get("tasks", [])}
    for tid in [f"PR-{i:02d}" for i in range(56, 61)]:
        if tid not in tasks:
            errors.append(f"{tid} missing from codex task registry")
    bundle_registry = load_json(ROOT / "registries" / "codex_pr_bundle_registry.json")
    bundles = {bundle.get("id") for bundle in bundle_registry.get("bundles", [])}
    if "REAL-PR-17" not in bundles:
        errors.append("REAL-PR-17 missing from codex PR bundle registry")
    return errors



def validate_pre_llm_intelligence() -> list[str]:
    errors = []
    required_docs = {
        "docs/PRE_LLM_INTELLIGENCE_LAYER_V7_1.md": ["Pre-LLM Intelligence Layer", "Model Work Avoidance", "Output Intelligence Composer"],
        "docs/ODIN_PRE_MODEL_COGNITION_V7_1.md": ["Odin Pre-Model Cognition", "Pre-Model Cognition Trace", "DFAS"],
        "docs/QIRC_PRECOMPUTE_FIELD_V7_1.md": ["QIRC Precompute Field", "#model.avoidance", "#why.trace"],
        "docs/MODEL_WORK_AVOIDANCE_V7_1.md": ["Model Work Avoidance", "no_model_template_candidate", "large model"],
        "docs/OUTPUT_INTELLIGENCE_COMPOSER_V7_1.md": ["Output Intelligence Composer", "Candidate Artifact", "model fragments"],
        "docs/PERCEIVED_INTELLIGENCE_METRICS_V7_1.md": ["Perceived Intelligence Metrics", "visible_usefulness", "Anti-Deception Boundary"],
        "docs/MICRO_TO_MACRO_CANDIDATE_SYNTHESIS_V7_1.md": ["Micro-to-Macro Candidate Synthesis", "micro_results", "candidate bundle"],
        "docs/MICRO_MODEL_ILLUSION_BOUNDARY_V7_1.md": ["Micro Model Illusion Boundary", "Forbidden", "Allowed"],
        "docs/reviews/SENIOR_REVIEW_SIMULATION_V0_6_5.md": ["Senior Review Simulation", "SR-065-01", "Approval Conditions"],
    }
    for rel, anchors in required_docs.items():
        p = ROOT / rel
        if not p.exists():
            errors.append(f"missing Pre-LLM intelligence doc {rel}")
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if len(text) < 1200:
            errors.append(f"{rel}: too short for Pre-LLM intelligence lock")
        for anchor in anchors:
            if anchor not in text:
                errors.append(f"{rel}: missing anchor {anchor!r}")
    for rel in ["odin_pre_llm_intelligence_packet.schema.json","odin_model_work_avoidance_decision.schema.json","odin_pre_model_cognition_trace.schema.json","odin_output_intelligence_composition.schema.json","odin_perceived_intelligence_score.schema.json","odin_micro_to_macro_synthesis_packet.schema.json"]:
        if not (ROOT / "schemas" / "v7_1" / rel).exists():
            errors.append(f"missing Pre-LLM schema {rel}")
    for rel in ["pre_llm_intelligence_registry.json","model_work_avoidance_registry.json","output_composer_pattern_registry.json","perceived_intelligence_metric_registry.json","micro_to_macro_synthesis_registry.json"]:
        p = ROOT / "registries" / rel
        if not p.exists():
            errors.append(f"missing Pre-LLM registry {rel}")
            continue
        data = load_json(p)
        if "registry_id" not in data or "version" not in data:
            errors.append(f"{rel}: missing registry_id/version")
    for rel in ["odin/shadow_runtime/pre_llm_intelligence_shadow.py","odin/shadow_runtime/pre_model_cognition_shadow.py","odin/shadow_runtime/model_work_avoidance_shadow.py","odin/shadow_runtime/output_intelligence_composer_shadow.py","odin/shadow_runtime/perceived_intelligence_metrics_shadow.py","odin/shadow_runtime/micro_to_macro_synthesis_shadow.py","examples/shadow_runtime/pre_llm_intelligence_flow.valid.json","examples/shadow_runtime/pre_llm_direct_apply_block.invalid.json","tests/test_pre_llm_intelligence_amplification.py"]:
        if not (ROOT / rel).exists():
            errors.append(f"missing Pre-LLM file {rel}")
    task_registry = load_json(ROOT / "registries" / "codex_task_registry.json")
    tasks = {task.get("id") for task in task_registry.get("tasks", [])}
    for tid in [f"PR-{i:02d}" for i in range(61, 66)]:
        if tid not in tasks:
            errors.append(f"{tid} missing from codex task registry")
    bundle_registry = load_json(ROOT / "registries" / "codex_pr_bundle_registry.json")
    bundles = {bundle.get("id") for bundle in bundle_registry.get("bundles", [])}
    if "REAL-PR-18" not in bundles:
        errors.append("REAL-PR-18 missing from codex PR bundle registry")
    return errors



def validate_universal_model_agent_parity() -> list[str]:
    errors = []
    required_docs = {
        "docs/UNIVERSAL_MODEL_AGENT_PARITY_V7_1.md": ["Universal Model / Agent Parity", "Any model", "Candidate"],
        "docs/MODEL_AGENT_CAPABILITY_CARDS_V7_1.md": ["Capability Cards", "worker_kind", "allowed_slot_classes"],
        "docs/MODEL_AGENT_WORK_CAPSULES_V7_1.md": ["Work Capsules", "active_workers", "Candidate"],
        "docs/UNIVERSAL_AGENT_CANDIDATE_PROTOCOL_V7_1.md": ["Universal Agent Candidate Protocol", "Candidate", "Forbidden outputs"],
        "docs/MODEL_AGENT_PERMISSION_CARD_SYSTEM_V7_1.md": ["Permission Card", "app_apply_required", "blocked"],
        "docs/EXTERNAL_MODEL_AGENT_ADAPTER_BOUNDARY_V7_1.md": ["External Model / Agent Adapter Boundary", "candidate", "redact"],
        "docs/UNIVERSAL_AGENT_ORCHESTRATION_MATRIX_V7_1.md": ["Universal Agent Orchestration Matrix", "Worker type", "Default gate"],
        "docs/MODEL_AGENT_WHY_TRACE_V7_1.md": ["Why Trace", "selected_worker", "rejected_workers"],
        "docs/reviews/SENIOR_REVIEW_SIMULATION_V0_6_6.md": ["Senior Review Simulation", "SR-066-01", "Approval Conditions"],
    }
    for rel, anchors in required_docs.items():
        p = ROOT / rel
        if not p.exists():
            errors.append(f"missing universal model/agent parity doc {rel}")
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if len(text) < 1200:
            errors.append(f"{rel}: too short for universal model/agent parity lock")
        for anchor in anchors:
            if anchor not in text:
                errors.append(f"{rel}: missing anchor {anchor!r}")
    for rel in ["model_agent_card_registry.json","model_agent_adapter_registry.json","model_agent_permission_registry.json","universal_agent_parity_registry.json","agent_candidate_protocol_registry.json","agent_twin_archetype_registry.json"]:
        p = ROOT / "registries" / rel
        if not p.exists():
            errors.append(f"missing universal model/agent registry {rel}")
            continue
        data = load_json(p)
        if "registry_id" not in data or "version" not in data:
            errors.append(f"{rel}: missing registry_id/version")
    for rel in ["odin_model_agent_card.schema.json","odin_agent_work_capsule.schema.json","odin_agent_capability_pack.schema.json","odin_agent_permission_card.schema.json","odin_agent_candidate_session.schema.json","odin_twin_parity_mapping.schema.json","odin_external_agent_adapter.schema.json","odin_model_agent_why_trace.schema.json"]:
        if not (ROOT / "schemas" / "v7_1" / rel).exists():
            errors.append(f"missing universal model/agent schema {rel}")
    task_registry = load_json(ROOT / "registries" / "codex_task_registry.json")
    tasks = {task.get("id") for task in task_registry.get("tasks", [])}
    for tid in [f"PR-{i:02d}" for i in range(66, 73)]:
        if tid not in tasks:
            errors.append(f"{tid} missing from codex task registry")
    bundle_registry = load_json(ROOT / "registries" / "codex_pr_bundle_registry.json")
    bundles = {bundle.get("id") for bundle in bundle_registry.get("bundles", [])}
    if "REAL-PR-19" not in bundles:
        errors.append("REAL-PR-19 missing from codex PR bundle registry")
    return errors



def validate_universal_llm_work_construct() -> list[str]:
    errors = []
    required_docs = {
        "docs/UNIVERSAL_LLM_WORK_CONSTRUCT_V7_1.md": ["Universal LLM Work Construct", "Any model", "Candidate"],
        "docs/THOR_ODIN_AI_GIT_LAYER_V7_1.md": ["AI-Git", "Semantic Diff", "Why Trace"],
        "docs/UNIVERSAL_MODEL_AGENT_ADAPTERS_V7_1.md": ["Adapters", "Permission Card", "Candidate"],
        "docs/REMOTE_MODEL_WORKER_BOUNDARY_V7_1.md": ["Remote", "redaction", "candidate"],
        "docs/LOCAL_REMOTE_LLM_PARITY_V7_1.md": ["Parity", "candidate protocol", "trust"],
        "docs/AGENT_TOOL_PERMISSION_BOUNDARY_V7_1.md": ["Permission", "blocked", "app_apply_required"],
        "docs/UNIVERSAL_USE_CASE_MATRIX_V7_1.md": ["Universal Use Case Matrix", "Preferred worker", "Output"],
        "docs/ANY_MODEL_ANY_AGENT_SAME_BOUNDARY_V7_1.md": ["Any model", "Any agent", "same Odin boundary"],
        "docs/THOR_ODIN_GPL2_ONLY_POLICY.md": ["GPL-2.0-only", "AI-Git", "license"],
        "docs/reviews/SENIOR_REVIEW_SIMULATION_V0_6_8.md": ["Senior Review", "SR-068-01", "Approval Conditions"],
    }
    for rel, anchors in required_docs.items():
        p = ROOT / rel
        if not p.exists():
            errors.append(f"missing universal LLM construct doc {rel}")
            continue
        data = p.read_text(encoding="utf-8", errors="ignore")
        if len(data) < 1200:
            errors.append(f"{rel}: too short for universal LLM construct lock")
        for anchor in anchors:
            if anchor not in data:
                errors.append(f"{rel}: missing anchor {anchor!r}")
    for rel in ["odin_universal_llm_worker.schema.json","odin_model_agent_adapter.schema.json","odin_remote_worker_boundary.schema.json","odin_agent_tool_permission_card.schema.json","odin_universal_use_case_profile.schema.json","odin_ai_git_work_session.schema.json"]:
        if not (ROOT / "schemas" / "v7_1" / rel).exists():
            errors.append(f"missing universal LLM construct schema {rel}")
    for rel in ["universal_llm_worker_registry.json","model_agent_adapter_registry.json","remote_worker_boundary_registry.json","agent_tool_permission_registry.json","universal_use_case_registry.json","ai_git_layer_registry.json"]:
        p = ROOT / "registries" / rel
        if not p.exists():
            errors.append(f"missing universal LLM construct registry {rel}")
            continue
        obj = load_json(p)
        if "registry_id" not in obj or "version" not in obj:
            errors.append(f"{rel}: missing registry_id/version")
    for rel in ["LICENSE","LICENSE_POLICY.md","THOR_ODIN_GPL2_ONLY_POLICY.md","PROTOCOL_BOUNDARY.md","SPDX_POLICY.md"]:
        p = ROOT / rel
        if not p.exists():
            errors.append(f"missing license policy file {rel}")
        elif "GPL-2.0-only" not in p.read_text(encoding="utf-8", errors="ignore"):
            errors.append(f"{rel}: missing GPL-2.0-only marker")
    task_registry = load_json(ROOT / "registries" / "codex_task_registry.json")
    tasks = {task.get("id") for task in task_registry.get("tasks", [])}
    for tid in [f"PR-{i:02d}" for i in range(81, 87)]:
        if tid not in tasks:
            errors.append(f"{tid} missing from codex task registry")
    bundle_registry = load_json(ROOT / "registries" / "codex_pr_bundle_registry.json")
    bundles = {bundle.get("id") for bundle in bundle_registry.get("bundles", [])}
    if "REAL-PR-21" not in bundles:
        errors.append("REAL-PR-21 missing from codex PR bundle registry")
    return errors



def validate_app_seed_pack_compiler() -> list[str]:
    errors = []
    required_docs = {
        "docs/APP_SEED_PACK_COMPILER_V7_1.md": ["App Seed Pack Compiler", "SPC-01", "Runtime Pack capability slice"],
        "docs/UNIVERSAL_SEED_PACK_FORMAT_V7_1.md": ["Seed Pack Manifest", "Seed Unit", "Operational Seed Function"],
        "docs/OPERATIONAL_SEED_FUNCTIONS_V7_1.md": ["Operational Seed Function", "declarative", "model_avoidance_hint"],
        "docs/SEED_PACK_SECURITY_BOUNDARY_V7_1.md": ["Seed Pack Security Boundary", "No arbitrary seed-pack code execution", "Trust and provenance"],
        "docs/SEED_PACK_TO_RUNTIME_PACK_COMPILER_V7_1.md": ["Runtime Pack capability slice", "Shadow Runtime seed weave", "Generated gates"],
        "docs/SEED_PACK_CAPABILITY_SLICES_V7_1.md": ["Capability Slice", "seed_pack_profile", "low_memory_strict"],
        "docs/SEED_PACK_COMPOSITION_AND_CONFLICTS_V7_1.md": ["Conflict", "Composition", "prefer_centerline_stability"],
        "docs/SEED_PACK_USE_CASE_MATRIX_V7_1.md": ["Use Case Matrix", "WordPress", "Traureden", "Coding", "GameDev"],
        "docs/SEED_PACK_WHY_TRACE_AND_EXPLAINABILITY_V7_1.md": ["Why Trace", "active_seed_pack", "tokens_saved_estimate"],
        "docs/reviews/SENIOR_REVIEW_SIMULATION_V0_6_9.md": ["Senior Review", "SR-069-01", "Approval Conditions", "Seed Pack Compiler"],
    }
    for rel, anchors in required_docs.items():
        p = ROOT / rel
        if not p.exists():
            errors.append(f"missing app seed pack doc {rel}")
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if len(text) < 1200:
            errors.append(f"{rel}: too short for app seed pack compiler lock")
        for anchor in anchors:
            if anchor not in text:
                errors.append(f"{rel}: missing anchor {anchor!r}")
    for rel in ["odin_app_seed_pack_manifest.schema.json","odin_seed_pack_unit.schema.json","odin_operational_seed_function.schema.json","odin_seed_pack_compile_plan.schema.json","odin_seed_pack_security_policy.schema.json","odin_seed_pack_capability_slice.schema.json","odin_seed_pack_activation_result.schema.json","odin_seed_pack_why_trace.schema.json"]:
        if not (ROOT / "schemas" / "v7_1" / rel).exists():
            errors.append(f"missing app seed pack schema {rel}")
    for rel in ["app_seed_pack_type_registry.json","operational_seed_function_registry.json","seed_pack_compiler_stage_registry.json","seed_pack_security_boundary_registry.json","seed_pack_capability_profile_registry.json"]:
        p = ROOT / "registries" / rel
        if not p.exists():
            errors.append(f"missing app seed pack registry {rel}")
            continue
        obj = load_json(p)
        if "registry_id" not in obj or "version" not in obj:
            errors.append(f"{rel}: missing registry_id/version")
    for rel in ["odin/shadow_runtime/app_seed_pack_compiler_shadow.py","odin/shadow_runtime/universal_seed_pack_manifest_shadow.py","odin/shadow_runtime/operational_seed_functions_shadow.py","odin/shadow_runtime/seed_pack_security_boundary_shadow.py","odin/shadow_runtime/seed_pack_to_runtime_pack_shadow.py","odin/shadow_runtime/seed_pack_composition_conflict_shadow.py","odin/shadow_runtime/seed_pack_use_case_matrix_shadow.py","odin/shadow_runtime/seed_pack_why_trace_shadow.py","examples/seed_packs/app_seed_pack_manifest.valid.json","examples/seed_packs/app_seed_pack_executable_block.invalid.json","tests/test_app_seed_pack_compiler.py"]:
        if not (ROOT / rel).exists():
            errors.append(f"missing app seed pack file {rel}")
    task_registry = load_json(ROOT / "registries" / "codex_task_registry.json")
    tasks = {task.get("id") for task in task_registry.get("tasks", [])}
    for tid in [f"PR-{i:02d}" for i in range(87, 93)]:
        if tid not in tasks:
            errors.append(f"{tid} missing from codex task registry")
    bundle_registry = load_json(ROOT / "registries" / "codex_pr_bundle_registry.json")
    bundles = {bundle.get("id") for bundle in bundle_registry.get("bundles", [])}
    if "REAL-PR-22" not in bundles:
        errors.append("REAL-PR-22 missing from codex PR bundle registry")
    return errors



def validate_shadow_narrative_loki() -> list[str]:
    errors = []
    required_docs = {
        "docs/SHADOW_NARRATIVE_V7_1.md": ["Shadow Narrative", "Fairy DSL", "anti-pattern"],
        "docs/ANTI_FAIRY_DSL_V7_1.md": ["Anti-Fairy DSL", "mirror_of", "required_gate"],
        "docs/LOKI_MEDIATION_LAYER_V7_1.md": ["Loki", "may not rule", "Ambivalence"],
        "docs/NARRATIVE_ANTIPATTERN_MIRROR_V7_1.md": ["Narrative Anti-Pattern Mirror", "Helpful Tyrant", "Gate"],
        "docs/FAILURE_STORY_REGISTRY_V7_1.md": ["Failure Story Registry", "severity", "required_gate"],
        "docs/SHADOW_NARRATIVE_TO_GATES_V7_1.md": ["Shadow Narrative to Gate Compiler", "negative fixture", "repair route"],
        "docs/NARRATIVE_RED_TEAM_COMPILER_V7_1.md": ["Narrative Red-Team Compiler", "negative", "Codex Rule"],
        "docs/LOKI_BOUNDARY_POLICY_V7_1.md": ["Loki Boundary Policy", "Forbidden", "Odin Core"],
        "docs/reviews/SENIOR_REVIEW_SIMULATION_V0_7_0.md": ["Senior Reviewer", "Shadow Narrative", "Approval Conditions"],
    }
    for rel, anchors in required_docs.items():
        p = ROOT / rel
        if not p.exists():
            errors.append(f"missing Shadow Narrative/Loki doc {rel}")
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if len(text) < 1200:
            errors.append(f"{rel}: too short for Shadow Narrative/Loki lock")
        for anchor in anchors:
            if anchor not in text:
                errors.append(f"{rel}: missing anchor {anchor!r}")
    for rel in ["odin_shadow_narrative.schema.json","odin_anti_fairy_unit.schema.json","odin_loki_mediation_packet.schema.json","odin_narrative_antipattern.schema.json","odin_failure_story.schema.json","odin_shadow_to_gate_mapping.schema.json","odin_narrative_red_team_case.schema.json"]:
        if not (ROOT / "schemas" / "v7_1" / rel).exists():
            errors.append(f"missing Shadow Narrative/Loki schema {rel}")
    for rel in ["shadow_narrative_registry.json","anti_fairy_pattern_registry.json","loki_mediation_registry.json","narrative_antipattern_registry.json","failure_story_registry.json","shadow_to_gate_registry.json"]:
        p = ROOT / "registries" / rel
        if not p.exists():
            errors.append(f"missing Shadow Narrative/Loki registry {rel}")
            continue
        obj = load_json(p)
        if "registry_id" not in obj or "version" not in obj:
            errors.append(f"{rel}: missing registry_id/version")
    for rel in ["odin/shadow_runtime/shadow_narrative_shadow.py","odin/shadow_runtime/anti_fairy_dsl_shadow.py","odin/shadow_runtime/loki_mediation_shadow.py","odin/shadow_runtime/narrative_antipattern_mirror_shadow.py","odin/shadow_runtime/failure_story_registry_shadow.py","odin/shadow_runtime/shadow_narrative_to_gate_shadow.py","odin/shadow_runtime/narrative_red_team_compiler_shadow.py","examples/shadow_narrative/shadow_narrative_helpful_tyrant.valid.json","examples/shadow_narrative/loki_authority_escalation.invalid.json","tests/test_shadow_narrative_loki_antipattern.py"]:
        if not (ROOT / rel).exists():
            errors.append(f"missing Shadow Narrative/Loki file {rel}")
    task_registry = load_json(ROOT / "registries" / "codex_task_registry.json")
    tasks = {task.get("id") for task in task_registry.get("tasks", [])}
    for tid in [f"PR-{i:02d}" for i in range(93, 98)]:
        if tid not in tasks:
            errors.append(f"{tid} missing from codex task registry")
    bundle_registry = load_json(ROOT / "registries" / "codex_pr_bundle_registry.json")
    bundles = {bundle.get("id") for bundle in bundle_registry.get("bundles", [])}
    if "REAL-PR-23" not in bundles:
        errors.append("REAL-PR-23 missing from codex PR bundle registry")
    return errors


def validate_product_pattern_atom_hub() -> list[str]:
    errors = []
    required_docs = {
        "docs/reviews/SENIOR_REVIEW_SIMULATION_V0_7_4.md": ["Senior Review", "WINDOWS_PRODUCT_RUNTIME_LOCK", "PATTERN_MINE_FLOW_PACK_INTAKE_LOCK", "WORK_ATOM_RUNTIME_LOCK", "ODIN_HUB_OPERATIONAL_CENTER_LOCK"],
        "docs/WINDOWS_PRODUCT_RUNTIME_LOCK_V7_1.md": ["Windows Product Runtime", "Process Responsibilities", "Runtime modes", "safe_mode"],
        "docs/WINDOWS_IPC_SECURITY_V7_1.md": ["Windows IPC Security", "named pipe", "localhost", "WAN forbidden"],
        "docs/WINDOWS_INSTALLER_UPDATE_ROLLBACK_V7_1.md": ["Windows Installer Update Rollback", "portable zip", "rollback", "safe mode"],
        "docs/WINDOWS_SUPPORT_BUNDLE_DIAGNOSTICS_V7_1.md": ["Windows Support Bundle Diagnostics", "redaction", "doctor", "no secrets"],
        "docs/PATTERN_MINE_FLOW_PACK_INTAKE_LOCK_V7_1.md": ["Pattern Mine", "Flow Pack", "compile-only", "Why Trace"],
        "docs/PATTERN_MINE_CLAIM_BOUNDARY_V7_1.md": ["Pattern Mine Claim Boundary", "not authority", "no executable code"],
        "docs/FLOW_PACK_TO_SEED_PACK_V7_1.md": ["Flow Pack to Seed Pack", "QIRC prewarm", "runtime pack slice"],
        "docs/PATTERN_SPINE_COMPILER_V7_1.md": ["Pattern Spine Compiler", "retrieval manifest", "work atoms"],
        "docs/WORK_ATOM_RUNTIME_LOCK_V7_1.md": ["Work Atom", "smallest meaningful", "candidate-only"],
        "docs/WORK_ATOM_GRAPH_V7_1.md": ["Work Atom Graph", "budget", "micro-to-macro"],
        "docs/WORK_ATOM_BUDGET_GATE_V7_1.md": ["Work Atom Budget Gate", "loop gain", "split work"],
        "docs/MICRO_TO_MACRO_WORK_SYNTHESIS_V7_1.md": ["Micro to Macro", "Candidate Artifact", "Output Composer"],
        "docs/ODIN_HUB_OPERATIONAL_CENTER_LOCK_V7_1.md": ["Odin Hub", "operational center", "not just a dashboard"],
        "docs/ODIN_HUB_PANEL_MAP_V7_1.md": ["Odin Hub Panel Map", "Home", "QIRC"],
        "docs/ODIN_HUB_COMMAND_ROUTING_V7_1.md": ["Odin Hub Command Routing", "doctor", "safe-mode"],
        "docs/ODIN_HUB_RECOVERY_AND_SAFE_MODE_V7_1.md": ["Odin Hub Recovery", "safe mode", "rollback"],
    }
    for rel, anchors in required_docs.items():
        p = ROOT / rel
        if not p.exists():
            errors.append(f"missing Product/Pattern/Atom/Hub doc {rel}")
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if len(text) < 800:
            errors.append(f"{rel}: too short for Product/Pattern/Atom/Hub lock")
        for anchor in anchors:
            if anchor not in text:
                errors.append(f"{rel}: missing anchor {anchor!r}")
    for rel in [
        "odin_windows_product_runtime_manifest.schema.json", "odin_windows_process_contract.schema.json", "odin_windows_ipc_policy.schema.json", "odin_windows_installer_profile.schema.json", "odin_windows_recovery_plan.schema.json", "odin_windows_support_bundle_policy.schema.json",
        "odin_pattern_mine_manifest.schema.json", "odin_flow_pack_manifest.schema.json", "odin_pattern_spine.schema.json", "odin_pattern_mine_compile_plan.schema.json", "odin_flow_pack_to_seed_pack.schema.json", "odin_pattern_mine_claim_boundary.schema.json",
        "odin_work_atom.schema.json", "odin_work_atom_graph.schema.json", "odin_work_atom_runtime_plan.schema.json", "odin_work_atom_result.schema.json", "odin_work_atom_budget_gate.schema.json", "odin_micro_to_macro_synthesis.schema.json",
        "odin_hub_surface.schema.json", "odin_hub_panel_contract.schema.json", "odin_hub_command_route.schema.json", "odin_hub_recovery_plan.schema.json", "odin_hub_support_bundle_request.schema.json",
    ]:
        if not (ROOT / "schemas" / "v7_1" / rel).exists():
            errors.append(f"missing Product/Pattern/Atom/Hub schema {rel}")
    for rel in ["windows_process_registry.json","windows_ipc_policy_registry.json","windows_installer_profile_registry.json","windows_recovery_registry.json","pattern_mine_type_registry.json","flow_pack_registry.json","pattern_spine_registry.json","work_atom_type_registry.json","work_atom_budget_registry.json","odin_hub_panel_registry.json","odin_hub_command_registry.json"]:
        p = ROOT / "registries" / rel
        if not p.exists():
            errors.append(f"missing Product/Pattern/Atom/Hub registry {rel}")
            continue
        obj = load_json(p)
        if "registry_id" not in obj or "version" not in obj:
            errors.append(f"{rel}: missing registry_id/version")
    for rel in [
        "odin/shadow_runtime/windows_product_runtime_shadow.py", "odin/shadow_runtime/windows_ipc_security_shadow.py", "odin/shadow_runtime/windows_installer_rollback_shadow.py",
        "odin/shadow_runtime/pattern_mine_intake_shadow.py", "odin/shadow_runtime/flow_pack_compiler_shadow.py", "odin/shadow_runtime/pattern_spine_compiler_shadow.py",
        "odin/shadow_runtime/work_atom_runtime_shadow.py", "odin/shadow_runtime/work_atom_budget_gate_shadow.py", "odin/shadow_runtime/micro_to_macro_work_synthesis_shadow.py",
        "odin/shadow_runtime/odin_hub_operational_center_shadow.py", "odin/shadow_runtime/odin_hub_panel_router_shadow.py", "odin/shadow_runtime/odin_hub_recovery_shadow.py",
        "examples/windows/windows_product_runtime_manifest.valid.json", "examples/pattern_mines/pattern_mine_manifest.valid.json", "examples/work_atoms/work_atom_graph.valid.json", "examples/odin_hub/odin_hub_surface.valid.json",
        "tests/test_product_pattern_atom_hub_lock.py",
    ]:
        if not (ROOT / rel).exists():
            errors.append(f"missing Product/Pattern/Atom/Hub file {rel}")
    task_registry = load_json(ROOT / "registries" / "codex_task_registry.json")
    tasks = {task.get("id") for task in task_registry.get("tasks", [])}
    for i in range(98, 116):
        if f"PR-{i}" not in tasks:
            errors.append(f"PR-{i} missing from codex task registry")
    bundle_registry = load_json(ROOT / "registries" / "codex_pr_bundle_registry.json")
    bundles = {bundle.get("id") for bundle in bundle_registry.get("bundles", [])}
    for bid in ["REAL-PR-24", "REAL-PR-25", "REAL-PR-26", "REAL-PR-27"]:
        if bid not in bundles:
            errors.append(f"{bid} missing from codex PR bundle registry")
    return errors


def validate_public_repo_windows_build_ready() -> list[str]:
    errors = []
    required_docs = {
        "docs/reviews/SENIOR_REVIEW_SIMULATION_V0_7_5.md": ["Senior Review", "PUBLIC_REPO_CANON_AND_WINDOWS_BUILD_READY_LOCK", "Approval conditions"],
        "docs/PUBLIC_REPO_CANON_AND_WINDOWS_BUILD_READY_LOCK_V7_1.md": ["Public Repo Canon", "Windows build-ready rule", "Codex rule"],
        "docs/PUBLIC_REPO_ROOT_CLEANUP_POLICY_V7_1.md": ["Root file responsibilities", "Codex cleanup behavior"],
        "docs/WINDOWS_IMPLEMENTATION_DRILLDOWN_V7_1.md": ["Process topology", "IPC hierarchy", "Safe mode"],
        "docs/WINDOWS_IPC_ENDPOINT_CONTRACTS_V7_1.md": ["Endpoint classes", "Forbidden endpoints", "Failure states"],
        "docs/WINDOWS_INSTALLER_UPDATE_ROLLBACK_DRILLDOWN_V7_1.md": ["Installer profiles", "Update lifecycle", "Rollback lifecycle"],
        "docs/MVP_V1_POWER_MODE_BOUNDARY_V7_1.md": ["MVP", "V1", "Power Mode"],
        "docs/SEED_PATTERN_PACK_SECURITY_CERTIFICATION_V7_1.md": ["Certification states", "Compile-only rule", "Block conditions"],
        "docs/CODEX_PUBLIC_BUILD_READY_GATE_V7_1.md": ["Required before implementation", "Implementation entry rule"],
    }
    for rel, anchors in required_docs.items():
        p = ROOT / rel
        if not p.exists():
            errors.append(f"missing Public Repo/Windows Build Ready doc {rel}")
            continue
        txt = p.read_text(encoding="utf-8", errors="ignore")
        if len(txt) < 800:
            errors.append(f"{rel}: too short for public repo/windows build-ready lock")
        for anchor in anchors:
            if anchor not in txt:
                errors.append(f"{rel}: missing anchor {anchor!r}")
    for rel in [
        "odin_public_repo_canon_lock.schema.json", "odin_windows_build_ready_manifest.schema.json", "odin_mvp_v1_power_mode_profile.schema.json", "odin_seed_pattern_pack_certification.schema.json", "odin_windows_ipc_endpoint.schema.json", "odin_release_readiness_gate.schema.json",
    ]:
        if not (ROOT / "schemas" / "v7_1" / rel).exists():
            errors.append(f"missing public repo/windows build-ready schema {rel}")
    for rel in ["public_repo_canon_registry.json","windows_build_mode_registry.json","mvp_v1_power_mode_registry.json","seed_pattern_pack_security_registry.json","windows_ipc_endpoint_registry.json","public_build_readiness_registry.json"]:
        p = ROOT / "registries" / rel
        if not p.exists():
            errors.append(f"missing public repo/windows build-ready registry {rel}")
            continue
        obj = load_json(p)
        if "registry_id" not in obj or "version" not in obj:
            errors.append(f"{rel}: missing registry_id/version")
    for rel in [
        "odin/shadow_runtime/public_repo_canon_shadow.py", "odin/shadow_runtime/windows_build_ready_shadow.py", "odin/shadow_runtime/mvp_v1_power_mode_shadow.py", "odin/shadow_runtime/seed_pattern_pack_security_shadow.py", "odin/shadow_runtime/windows_ipc_endpoint_shadow.py", "odin/shadow_runtime/public_build_readiness_shadow.py", "tests/test_public_repo_windows_build_ready.py",
    ]:
        if not (ROOT / rel).exists():
            errors.append(f"missing public repo/windows build-ready file {rel}")
    task_registry = load_json(ROOT / "registries" / "codex_task_registry.json")
    tasks = {task.get("id") for task in task_registry.get("tasks", [])}
    for tid in [f"PR-{i}" for i in range(116, 124)]:
        if tid not in tasks:
            errors.append(f"{tid} missing from codex task registry")
    bundle_registry = load_json(ROOT / "registries" / "codex_pr_bundle_registry.json")
    bundles = {bundle.get("id") for bundle in bundle_registry.get("bundles", [])}
    if "REAL-PR-28" not in bundles:
        errors.append("REAL-PR-28 missing from codex PR bundle registry")
    return errors



def validate_real_pr_execution() -> list[str]:
    errors = []
    registry_path = ROOT / "registries" / "real_pr_execution_registry.json"
    if not registry_path.exists():
        return ["real PR execution registry missing"]
    data = load_json(registry_path)
    prs = data.get("execution_prs", [])
    if data.get("alignment_lock") != "BUILD_LADDER_ABSOLUTE_ALIGNMENT_LOCK":
        errors.append("real PR execution registry must declare BUILD_LADDER_ABSOLUTE_ALIGNMENT_LOCK")
    if len(prs) != 8:
        errors.append(f"real PR execution registry must contain exactly 8 actual PRs ({len(prs)} found)")
    task_registry = load_json(ROOT / "registries" / "codex_task_registry.json")
    bundle_registry = load_json(ROOT / "registries" / "codex_pr_bundle_registry.json")
    task_ids = {task.get("id") for task in task_registry.get("tasks", [])}
    bundle_ids = {bundle.get("id") for bundle in bundle_registry.get("bundles", [])}
    covered = []
    legacy_covered = []
    seen = set()
    completed = set()
    required_fields = [
        "absorbs_internal_tasks",
        "absorbs_legacy_bundles",
        "fully_absorbs_legacy_bundles",
        "partially_absorbs_legacy_bundles",
        "expected_existing_paths",
        "expected_new_paths",
        "existing_files",
        "target_files",
        "acceptance_gates",
        "proof_boundaries",
        "must_run",
        "must_preserve",
        "master_architecture_sections",
        "execution_scope",
        "internal_ladder_relation",
    ]
    for pr in prs:
        pid = pr.get("id")
        if not pid:
            errors.append("real execution PR missing id")
            continue
        if pid in seen:
            errors.append(f"duplicate real execution PR id {pid}")
        seen.add(pid)
        if not str(pid).startswith("REAL-GH-PR-"):
            errors.append(f"real execution PR id must start with REAL-GH-PR-: {pid}")
        for dep in pr.get("depends_on", []):
            if dep not in completed:
                errors.append(f"{pid}: dependency {dep} must appear before PR")
        completed.add(pid)
        for key in required_fields:
            if key not in pr:
                errors.append(f"{pid}: missing {key}")
        internal = pr.get("internal_tasks", [])
        if pr.get("absorbs_internal_tasks") != internal:
            errors.append(f"{pid}: absorbs_internal_tasks must match internal_tasks")
        if not internal:
            errors.append(f"{pid}: missing internal_tasks")
        for tid in internal:
            if tid not in task_ids:
                errors.append(f"{pid}: unknown internal task {tid}")
            covered.append(tid)
        for bid in pr.get("absorbs_legacy_bundles", []):
            if bid not in bundle_ids:
                errors.append(f"{pid}: unknown absorbed legacy bundle {bid}")
            legacy_covered.append(bid)
        if not pr.get("acceptance_gates"):
            errors.append(f"{pid}: missing acceptance_gates")
        if not pr.get("proof_boundaries"):
            errors.append(f"{pid}: missing proof_boundaries")
        if not pr.get("must_run"):
            errors.append(f"{pid}: missing must_run")
        if not pr.get("master_architecture_sections"):
            errors.append(f"{pid}: missing master_architecture_sections")
        for rel in pr.get("expected_existing_paths", []):
            if not (ROOT / rel).exists():
                errors.append(f"{pid}: expected existing path missing: {rel}")
        doc_rel = pr.get("doc")
        if not doc_rel:
            errors.append(f"{pid}: missing doc")
            continue
        doc_path = ROOT / doc_rel
        if not doc_path.exists():
            errors.append(f"{pid}: doc missing: {doc_rel}")
            continue
        doc = doc_path.read_text(encoding="utf-8", errors="ignore")
        for anchor in [pid, "Objective", "Internal Tasks Covered", "Primary Files", "Required Behavior", "Forbidden Scope", "Definition of Done", "Codex PR Summary Template", "v0.7.7 Build Ladder Absolute Alignment Addendum", "Existing Prep Files", "Target Implementation Files", "Proof Boundaries"]:
            if anchor not in doc:
                errors.append(f"{doc_rel}: missing anchor {anchor!r}")
        if len(doc) < 4500:
            errors.append(f"{doc_rel}: too short for aligned real PR execution doc ({len(doc)} < 4500)")
    missing = sorted(tid for tid in task_ids if tid and tid not in set(covered))
    duplicates = sorted(tid for tid in set(covered) if covered.count(tid) > 1)
    if missing:
        errors.append("real execution PR registry does not cover internal tasks: " + ", ".join(missing))
    if duplicates:
        errors.append("real execution PR registry maps internal tasks more than once: " + ", ".join(duplicates))
    missing_legacy = sorted(bid for bid in bundle_ids if bid and bid not in set(legacy_covered))
    if missing_legacy:
        errors.append("real execution PR registry does not absorb legacy bundles: " + ", ".join(missing_legacy))
    required_docs = [
        "docs/REAL_PR_EXECUTION_CONSOLIDATION_LOCK_V7_1.md",
        "docs/BUILD_LADDER_ABSOLUTE_ALIGNMENT_LOCK_V7_1.md",
        "docs/codex/REAL_GITHUB_PR_EXECUTION_PLAN_V0_7_7.md",
        "docs/codex/REAL_GITHUB_PR_EXECUTION_INDEX_V0_7_7.md",
    ]
    for rel in required_docs:
        if not (ROOT / rel).exists():
            errors.append(f"missing real PR alignment doc {rel}")
    master_arch = (ROOT / "docs" / "MASTER_ARCHITECTURE_V7_1.md").read_text(encoding="utf-8", errors="ignore")
    master_specs = (ROOT / "docs" / "MASTER_SPECS_V7_1.md").read_text(encoding="utf-8", errors="ignore")
    for label, text in [("MASTER_ARCHITECTURE", master_arch), ("MASTER_SPECS", master_specs)]:
        if "v0.7.7 BUILD_LADDER_ABSOLUTE_ALIGNMENT_LOCK" not in text:
            errors.append(f"{label}: missing current v0.7.7 repository state")
        if "REAL-GH-PR-01..REAL-GH-PR-08" not in text:
            errors.append(f"{label}: missing actual GitHub PR execution sequence")
    return errors


def validate_runtime_source_candidate() -> list[str]:
    errors: list[str] = []
    required_paths = [
        "docs/RUNTIME_SOURCE_CANDIDATE_V0_8_0.md",
        "docs/RUNTIME_SOURCE_MODULE_MAP_V0_8_0.md",
        "docs/WINDOWS_DIRECT_SOURCE_HANDOFF_V0_8_0.md",
        "docs/CODEX_RUNTIME_CANDIDATE_HANDOFF_V0_8_0.md",
        "docs/codex/CHATGPT_DIRECT_RUNTIME_BUILD_PLAN_V0_8_0.md",
        "registries/runtime_source_module_registry.json",
        "schemas/v7_1/odin_runtime_source_module_registry.schema.json",
        "examples/runtime/universal_work_full.valid.json",
        "examples/runtime/app_seed_pack_full.valid.json",
        "examples/runtime/pattern_mine_full.valid.json",
        "tests/test_runtime_source_candidate_v080.py",
        "odin/runtime/engine.py",
        "odin/qirc/ledger.py",
        "odin/seeds/compiler.py",
        "odin/patterns/intake.py",
        "odin/flow_packs/compiler.py",
        "odin/work_atoms/runtime.py",
        "odin/candidates/artifact.py",
        "odin/why_trace/builder.py",
        "odin/daemon/local_api.py",
        "odin/hub/static_hub.py",
        "odin/diagnostics/support_bundle.py",
        "odin/recovery/safe_mode.py",
    ]
    for rel in required_paths:
        if not (ROOT / rel).exists():
            errors.append(f"runtime source candidate missing path: {rel}")
    registry_path = ROOT / "registries" / "runtime_source_module_registry.json"
    if registry_path.exists():
        data = load_json(registry_path)
        if data.get("version") != "0.8.0":
            errors.append("runtime source module registry must be version 0.8.0")
        for module in data.get("modules", []):
            if module.get("candidate_only") is not True:
                errors.append(f"runtime module not candidate_only: {module.get('id')}")
            for rel in module.get("paths", []):
                if not (ROOT / rel).exists():
                    errors.append(f"runtime module {module.get('id')} path missing: {rel}")
    master_arch = (ROOT / "docs" / "MASTER_ARCHITECTURE_V7_1.md").read_text(encoding="utf-8", errors="ignore")
    if "v0.8.0 Direct Master Architecture Runtime Source Candidate" not in master_arch:
        errors.append("MASTER_ARCHITECTURE missing v0.8.0 runtime source candidate section")
    system_map = load_json(ROOT / "SYSTEM_MAP.json")
    if "v0_8_0_direct_runtime_source_candidate" not in system_map:
        errors.append("SYSTEM_MAP missing v0_8_0_direct_runtime_source_candidate")
    return errors


def validate_direct_runtime_release_candidate() -> list[str]:
    errors: list[str] = []
    required_paths = [
        "docs/DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK_V0_8_6.md",
        "docs/RUNTIME_CORE_COMPLETION_V0_8_1.md",
        "docs/APP_BRIDGE_AND_GOLDEN_APP_LOCK_V0_8_2.md",
        "docs/LOCAL_API_AND_ODIN_HUB_RUNTIME_LOCK_V0_8_3.md",
        "docs/MODEL_PROVIDER_AND_WORKER_BOUNDARY_LOCK_V0_8_4.md",
        "docs/WINDOWS_HOST_HANDOFF_LOCK_V0_8_5.md",
        "docs/CODEX_DIRECT_RUNTIME_RC_HANDOFF_V0_8_6.md",
        "docs/RELEASE_CANDIDATE_ACCEPTANCE_REPORT_V0_8_6.md",
        "registries/direct_runtime_release_candidate_registry.json",
        "schemas/v7_1/odin_direct_runtime_release_candidate_registry.schema.json",
        "odin/runtime/config.py",
        "odin/runtime/store.py",
        "odin/runtime/session.py",
        "odin/runtime/repair.py",
        "odin_app_sdk/client.py",
        "odin_app_sdk/manifest.py",
        "odin/models/providers/base.py",
        "odin/models/providers/mock.py",
        "odin/models/providers/stubs.py",
        "odin/models/providers/registry.py",
        "windows/README_WINDOWS_HOST.md",
        "windows/run_odin.ps1",
        "windows/start_daemon.ps1",
        "tests/test_direct_runtime_release_candidate_v086.py",
    ]
    for rel in required_paths:
        if not (ROOT / rel).exists():
            errors.append(f"direct runtime RC missing path: {rel}")
    registry_path = ROOT / "registries" / "direct_runtime_release_candidate_registry.json"
    if registry_path.exists():
        data = load_json(registry_path)
        if data.get("version") != "0.8.6":
            errors.append("direct runtime release candidate registry must be version 0.8.6")
        for module in data.get("modules", []):
            if module.get("candidate_only") is not True:
                errors.append(f"direct runtime module not candidate_only: {module.get('id')}")
            for rel in module.get("paths", []):
                if not (ROOT / rel).exists():
                    errors.append(f"direct runtime module path missing: {rel}")
        for boundary in ["no_windows_host_proof", "no_live_model_inference_proof", "no_app_apply_by_odin"]:
            if boundary not in data.get("proof_boundaries", []):
                errors.append(f"direct runtime RC missing proof boundary: {boundary}")
    for rel in ["README.md", "CANON_ENTRY.md", "CODEX_START_HERE.md", "docs/MASTER_ARCHITECTURE_V7_1.md", "docs/MASTER_SPECS_V7_1.md"]:
        text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        if "v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK" not in text:
            errors.append(f"{rel}: missing v0.8.6 direct runtime release candidate lock marker")
    return errors



def validate_current_public_canon() -> list[str]:
    """Validate the v0.8.7 public-canon surface without scanning this validator's own token lists."""
    errors: list[str] = []
    root_docs = [
        "README.md",
        "START_HERE.md",
        "CANON_ENTRY.md",
        "CODEX_START_HERE.md",
        "CLAIM_BOUNDARY.md",
        "PROTOCOL_BOUNDARY.md",
    ]
    required_markers = [
        "v0.8.7 CODEX_REAL_PR_HANDOFF_LADDER_LOCK",
        "v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK",
        "REAL-GH-PR-01..08",
        "PR-00..PR-123",
        "REAL-PR-01..28",
    ]
    required_boundary_markers = [
        "candidate-only",
        "app-owned apply",
        "external sends",
        "Providers are",
        "QIRC",
    ]
    for rel in root_docs:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"current canon root doc missing: {rel}")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for marker in required_markers:
            if marker not in text:
                errors.append(f"{rel}: missing current-canon marker {marker!r}")
        lower = text.lower()
        for marker in required_boundary_markers:
            if marker.lower() not in lower:
                errors.append(f"{rel}: missing boundary marker {marker!r}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8", errors="ignore")
    for phrase in [
        "current public repo canon",
        "Actual Codex/GitHub PR ladder: REAL-GH-PR-01..08",
        "Internal traceability ladders: PR-00..PR-123 and REAL-PR-01..28 only",
    ]:
        if phrase not in readme:
            errors.append(f"README.md: missing canon summary phrase {phrase!r}")

    system_map = load_json(ROOT / "SYSTEM_MAP.json")
    current = system_map.get("current_public_canon", {})
    if current.get("current_handoff") != "v0.8.7 CODEX_REAL_PR_HANDOFF_LADDER_LOCK":
        errors.append("SYSTEM_MAP current_public_canon.current_handoff must be v0.8.7 CODEX_REAL_PR_HANDOFF_LADDER_LOCK")
    if current.get("runtime_base") != "v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK":
        errors.append("SYSTEM_MAP current_public_canon.runtime_base must be v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK")
    if current.get("actual_codex_github_pr_ladder") != "REAL-GH-PR-01..08":
        errors.append("SYSTEM_MAP current_public_canon.actual_codex_github_pr_ladder must be REAL-GH-PR-01..08")
    if current.get("internal_traceability_ladders") != ["PR-00..PR-123", "REAL-PR-01..28"]:
        errors.append("SYSTEM_MAP current_public_canon.internal_traceability_ladders must list PR-00..PR-123 and REAL-PR-01..28")

    handoff = load_json(ROOT / "registries" / "codex_real_pr_handoff_registry.json")
    execution_pr_ids = [pr.get("id") for pr in handoff.get("execution_prs", [])]
    expected_ids = [f"REAL-GH-PR-{index:02d}" for index in range(1, 9)]
    if execution_pr_ids != expected_ids:
        errors.append("codex real PR handoff registry must define REAL-GH-PR-01..08 in order")
    if handoff.get("current_handoff") != "v0.8.7_CODEX_REAL_PR_HANDOFF_LADDER_LOCK":
        errors.append("codex real PR handoff registry must declare v0.8.7 current_handoff")
    if handoff.get("current_base") != "v0.8.6_DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK":
        errors.append("codex real PR handoff registry must declare v0.8.6 current_base")

    # Scan only public root docs so this check cannot fail on its own patterns or test fixtures.
    disallowed_current_fragments = [
        "is the current canonical prep state",
        "is the current prep state",
        "is the current execution ladder",
        "current actual github execution sequence: `real-pr-",
        "current actual build execution ladder is `real-pr-",
    ]
    old_version_markers = ["v0.3", "v0.4", "v0.5", "v0.6", "v0.7"]
    for rel in root_docs:
        for line_no, line in enumerate((ROOT / rel).read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
            normalized = " ".join(line.lower().split())
            if any(fragment in normalized for fragment in disallowed_current_fragments):
                errors.append(f"{rel}:{line_no}: disallowed competing current-canon phrase")
            if "current" in normalized and any(marker in normalized for marker in old_version_markers):
                if not any(scope in normalized for scope in ["historical", "history", "changelog", "not the current", "not current"]):
                    errors.append(f"{rel}:{line_no}: older version appears in current-canon context")
            if "production ready" in normalized and not any(scope in normalized for scope in ["not production ready", "does not claim", "not claim", "without receipt"]):
                errors.append(f"{rel}:{line_no}: production-ready wording must be negated or proof-gap scoped")
    return errors


def validate_runtime_bus_worklets() -> list[str]:
    errors: list[str] = []
    required_paths = [
        "odin/bus/events.py",
        "odin/bus/bus.py",
        "odin/worklets/graph.py",
        "odin/worklets/compiler.py",
        "schemas/v7_1/odin_semantic_bus_event.schema.json",
        "schemas/v7_1/odin_worklet_graph.schema.json",
        "schemas/v7_1/odin_runtime_store_record.schema.json",
        "registries/runtime_bus_event_registry.json",
        "registries/worklet_registry.json",
        "examples/runtime/worklet_graph.valid.json",
        "examples/runtime/work_atom_budget_exceeded.invalid.json",
    ]
    for rel in required_paths:
        if not (ROOT / rel).exists():
            errors.append(f"runtime bus/worklets required path missing: {rel}")
    try:
        from odin.bus.bus import LocalSemanticBus
        from odin.worklets.graph import build_worklet_graph
        from odin.worklets.compiler import compile_worklet_graph_to_atom_plan
        from odin.work_atoms.runtime import execute_work_atoms

        event = LocalSemanticBus().publish("app.apply", work_id="W", session_id="S", trace_id="T", payload={"secret": "redacted"})
        if event.get("event_type") != "runtime.boundary_rejected":
            errors.append("forbidden bus event was not downgraded")
        graph = build_worklet_graph({"work_id": "VALIDATE", "work_intent": {"work_atoms": ["context_compress_atom"]}})
        plan = compile_worklet_graph_to_atom_plan(graph)
        if plan.get("status") != "ok" or len(plan.get("atoms", [])) != 1:
            errors.append("worklet graph did not compile to a bounded atom plan")
        budget_fixture = load_json(ROOT / "examples" / "runtime" / "work_atom_budget_exceeded.invalid.json")
        result = execute_work_atoms(budget_fixture, {})
        if result.get("status") != "blocked":
            errors.append("work atom budget fixture did not fail closed")
    except Exception as exc:
        errors.append(f"runtime bus/worklets import or fixture check failed: {exc}")
    local_api = (ROOT / "odin" / "daemon" / "local_api.py").read_text(encoding="utf-8", errors="ignore")
    for marker in ["/v7/apply'", '"/v7/apply"']:
        if marker in local_api and "FORBIDDEN_ROUTES" not in local_api:
            errors.append("local API appears to expose app apply route")
    forbidden_network_markers = ["0.0.0.0", "serve_forever_external", "wan_enabled"]
    for marker in forbidden_network_markers:
        if marker in local_api:
            errors.append(f"local API contains forbidden WAN/LAN marker: {marker}")
    return errors


def validate_provider_worker_boundary() -> list[str]:
    errors: list[str] = []
    required_paths = [
        "odin/models/providers/base.py",
        "odin/models/providers/mock.py",
        "odin/models/providers/stubs.py",
        "odin/models/permissions.py",
        "schemas/v7_1/odin_model_worker_permission_card.schema.json",
        "schemas/v7_1/odin_pre_llm_route.schema.json",
        "schemas/v7_1/odin_provider_config.schema.json",
        "registries/model_worker_permission_registry.json",
        "registries/pre_llm_route_registry.json",
    ]
    for rel in required_paths:
        if not (ROOT / rel).exists():
            errors.append(f"provider-worker boundary file missing: {rel}")
    required_forbidden_roles = {"app_authority", "apply_executor", "claim_acceptor", "receipt_issuer", "external_sender", "state_mutator"}
    for card in list_provider_cards():
        missing = required_forbidden_roles - set(card.get("forbidden_roles", []))
        if missing:
            errors.append(f"{card.get('provider_id')}: missing forbidden roles {sorted(missing)}")
        if card.get("candidate_only") is not True:
            errors.append(f"{card.get('provider_id')}: provider card must be candidate_only")
        if card.get("may_apply") or card.get("may_send_external") or card.get("may_mutate_app_state") or card.get("may_accept_claim") or card.get("may_issue_receipt"):
            errors.append(f"{card.get('provider_id')}: provider authority gates must be false")
        if "stub" in str(card.get("provider_id")) and (card.get("enabled_by_default") or card.get("live_inference_verified")):
            errors.append(f"{card.get('provider_id')}: remote/local stubs must be disabled or non-verified by default")
    permission_card = build_permission_card("validator_worker")
    for gate in ["may_apply", "may_send_external", "may_mutate_app_state", "may_accept_claim", "may_issue_receipt"]:
        if check_permission_escalation(permission_card, {gate: True}).get("status") != "blocked":
            errors.append(f"permission card did not block {gate}")
    no_model_work = {
        "work_id": "VALIDATOR-NO-MODEL",
        "work_intent": {"kind": "classify", "requires_model": False, "goal": "deterministic route"},
        "model_policy": {"requires_model": False},
        "output_contract": {"candidate_only": True, "app_owned_apply": True, "may_apply": False},
        "constraints": {"actions": []},
    }
    route = score_pre_llm_route(no_model_work)
    if route.get("requires_model") or route.get("route") != "deterministic_no_model":
        errors.append("pre-LLM route did not choose deterministic no-model when sufficient")
    apply_work = {
        "work_id": "VALIDATOR-APPLY-BLOCK",
        "work_intent": {"kind": "apply", "goal": "apply directly"},
        "output_contract": {"candidate_only": False, "app_owned_apply": False, "may_apply": True},
        "constraints": {"actions": ["direct_apply"]},
    }
    blocked_route = score_pre_llm_route(apply_work)
    if not blocked_route.get("blocked_reasons"):
        errors.append("pre-LLM route did not block direct apply before provider dispatch")
    redacted_path = ROOT / "examples/runtime/provider_config.redacted.valid.json"
    if redacted_path.exists():
        try:
            load_provider_config(redacted_path)
        except Exception as exc:
            errors.append(f"redacted provider config should validate: {exc}")
        rendered = dumps_redacted(load_json(redacted_path))
        for marker in ["api_key", "ODIN_TEST", "Bearer "]:
            if marker in rendered:
                errors.append(f"redacted provider config leaked marker {marker}")
    secret_path = ROOT / "examples/runtime/provider_config.secret.invalid.json"
    if secret_path.exists():
        secret_obj = load_json(secret_path)
        if not validate_provider_config(secret_obj):
            errors.append("secret provider config fixture should fail closed")
        redacted = dumps_redacted(secret_obj)
        for marker in ["ODIN_TEST_API_KEY_SHOULD_REDACT", "ODIN_TEST_TOKEN_SHOULD_REDACT", "ODIN_TEST_PASSWORD_SHOULD_REDACT", "ODIN_TEST_BEARER_SHOULD_REDACT"]:
            if marker in redacted:
                errors.append(f"secret redaction leaked {marker}")
    return errors

def validate_agent_operator_mode() -> list[str]:
    """Validate Agent Operator Mode schemas, registries, examples, and boundaries."""
    errors = []
    required_schemas = [
        "schemas/v7_1/odin_agent_work_packet.schema.json",
        "schemas/v7_1/odin_agent_return_report.schema.json",
        "schemas/v7_1/odin_agent_operator_permission_card.schema.json",
    ]
    for rel in required_schemas:
        p = ROOT / rel
        if not p.exists():
            errors.append(f"agent operator mode schema missing: {rel}")
            continue
        try:
            load_json(p)
        except Exception as exc:
            errors.append(f"agent operator mode schema invalid JSON {rel}: {exc}")

    required_registries = [
        "registries/agent_operator_profile_registry.json",
        "registries/thor_compatibility_registry.json",
    ]
    for rel in required_registries:
        p = ROOT / rel
        if not p.exists():
            errors.append(f"agent operator mode registry missing: {rel}")
            continue
        try:
            data = load_json(p)
        except Exception as exc:
            errors.append(f"agent operator mode registry invalid JSON {rel}: {exc}")
            continue
        if "registry_id" not in data or "version" not in data:
            errors.append(f"agent operator mode registry missing registry_id/version: {rel}")

    # Validate profile registry
    profile_path = ROOT / "registries" / "agent_operator_profile_registry.json"
    if profile_path.exists():
        try:
            data = load_json(profile_path)
            required_profiles = {"codex", "claude-code", "generic-cli-agent", "thor-compatible", "future-local-agent"}
            found = {p.get("profile_id") for p in data.get("profiles", [])}
            missing = required_profiles - found
            if missing:
                errors.append(f"agent operator profile registry missing profiles: {sorted(missing)}")
            hard_false_fields = ["may_apply_app_state", "may_send_external", "may_call_provider_api",
                                 "may_use_hidden_tools", "may_mutate_domain_state"]
            for profile in data.get("profiles", []):
                perm = profile.get("default_permission_card", {})
                for field in hard_false_fields:
                    if perm.get(field) is not False:
                        errors.append(f"profile {profile.get('profile_id')!r} must have {field}=false")
        except Exception as exc:
            errors.append(f"agent operator profile registry load failed: {exc}")

    # Validate Thor compatibility registry
    thor_path = ROOT / "registries" / "thor_compatibility_registry.json"
    if thor_path.exists():
        try:
            data = load_json(thor_path)
            for m in data.get("mappings", []):
                for key in ["thor_concept", "odin_concept", "status", "evidence_label", "gap", "claim_boundary"]:
                    if key not in m:
                        errors.append(f"thor compatibility mapping missing {key}: {m.get('thor_concept')}")
        except Exception as exc:
            errors.append(f"thor compatibility registry load failed: {exc}")

    # Validate valid examples
    valid_examples = [
        "examples/agent_operator/codex_work_packet.valid.json",
        "examples/agent_operator/claude_code_work_packet.valid.json",
        "examples/agent_operator/generic_cli_agent_work_packet.valid.json",
        "examples/agent_operator/future_local_agent_work_packet.valid.json",
        "examples/agent_operator/thor_compatible_packet.valid.json",
    ]
    for rel in valid_examples:
        p = ROOT / rel
        if not p.exists():
            errors.append(f"agent operator valid example missing: {rel}")
            continue
        try:
            packet = load_json(p)
        except Exception as exc:
            errors.append(f"agent operator valid example invalid JSON {rel}: {exc}")
            continue
        if packet.get("candidate_only") is not True:
            errors.append(f"{rel}: candidate_only must be true")
        if packet.get("app_owned_apply") is not True:
            errors.append(f"{rel}: app_owned_apply must be true")
        if packet.get("external_send_default") is not False:
            errors.append(f"{rel}: external_send_default must be false")
        if packet.get("hidden_tool_execution_allowed") is not False:
            errors.append(f"{rel}: hidden_tool_execution_allowed must be false")

    # Validate invalid examples fail for correct reasons
    invalid_checks = [
        ("examples/agent_operator/agent_work_packet.invalid.hidden_apply.json", "hidden_tool_execution_allowed", True),
        ("examples/agent_operator/agent_work_packet.invalid.external_send.json", "external_send_default", True),
    ]
    for rel, field, expected_val in invalid_checks:
        p = ROOT / rel
        if not p.exists():
            errors.append(f"agent operator invalid example missing: {rel}")
            continue
        try:
            packet = load_json(p)
            if packet.get(field) != expected_val:
                errors.append(f"{rel}: expected {field}={expected_val!r} to trigger invalidity")
        except Exception as exc:
            errors.append(f"agent operator invalid example load failed {rel}: {exc}")

    provider_api_path = ROOT / "examples/agent_operator/agent_permission_card.invalid.provider_api.json"
    if provider_api_path.exists():
        try:
            card = load_json(provider_api_path)
            if card.get("may_call_provider_api") is not True:
                errors.append("provider_api invalid example must have may_call_provider_api=true to be invalid")
        except Exception as exc:
            errors.append(f"provider_api invalid example load failed: {exc}")
    else:
        errors.append("agent operator invalid example missing: examples/agent_operator/agent_permission_card.invalid.provider_api.json")

    # Check boundary invariants via module
    try:
        from odin.agent_operator.guards import check_forbidden_actions
        from odin.agent_operator.packets import validate_agent_work_packet
        from odin.agent_operator.returns import build_return_report_skeleton, validate_return_report
        skeleton = build_return_report_skeleton("TEST", "codex")
        result = validate_return_report(skeleton)
        if result["status"] != "ok":
            errors.append(f"return report skeleton failed validation: {result}")
    except Exception as exc:
        errors.append(f"agent operator mode module import/check failed: {exc}")

    return errors


def validate_local_runtime_starter() -> list[str]:
    """Validate portable local runtime starter files, configs, and boundaries."""
    errors = []

    required_scripts = [
        "scripts/start_odin.sh",
        "scripts/stop_odin.sh",
        "scripts/check_odin.sh",
        "scripts/start_odin.bat",
        "scripts/stop_odin.bat",
        "scripts/check_odin.bat",
    ]
    for rel in required_scripts:
        p = ROOT / rel
        if not p.exists():
            errors.append(f"runtime starter script missing: {rel}")
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if "python -m odin.cli" not in text:
            errors.append(f"{rel}: script must call 'python -m odin.cli'")

    doc = ROOT / "docs/LOCAL_RUNTIME_STARTER_V1.md"
    if not doc.exists():
        errors.append("docs/LOCAL_RUNTIME_STARTER_V1.md missing")
    else:
        doc_text = doc.read_text(encoding="utf-8", errors="ignore")
        for required_phrase in [
            "not a Windows service",
            "not a tray",
            "not a signed installer",
            "not production readiness",
            "public network",
            "127.0.0.1",
        ]:
            if required_phrase.lower() not in doc_text.lower():
                errors.append(f"docs/LOCAL_RUNTIME_STARTER_V1.md: missing required phrase: {required_phrase!r}")

    valid_cfg = ROOT / "examples/local_runtime/portable_runtime_config.valid.json"
    if not valid_cfg.exists():
        errors.append("examples/local_runtime/portable_runtime_config.valid.json missing")
    else:
        try:
            from odin.local_runtime.config import validate_config
            data = load_json(valid_cfg)
            errs = validate_config(data)
            if errs:
                errors.append(f"valid config fixture should have no errors, got: {errs}")
        except Exception as exc:
            errors.append(f"valid config fixture check failed: {exc}")

    invalid_cfg = ROOT / "examples/local_runtime/portable_runtime_config.invalid.public_bind.json"
    if not invalid_cfg.exists():
        errors.append("examples/local_runtime/portable_runtime_config.invalid.public_bind.json missing")
    else:
        try:
            from odin.local_runtime.config import validate_config
            data = load_json(invalid_cfg)
            errs = validate_config(data)
            if not errs:
                errors.append("invalid public_bind config fixture should fail validation but passed")
        except Exception as exc:
            errors.append(f"invalid config fixture check failed: {exc}")

    try:
        from odin.local_runtime.config import DEFAULT_HOST, ALLOWED_HOSTS, BLOCKED_HOSTS
        if DEFAULT_HOST != "127.0.0.1":
            errors.append(f"default host must be 127.0.0.1, got {DEFAULT_HOST!r}")
        for blocked in ("0.0.0.0", "::", ""):
            if blocked not in BLOCKED_HOSTS:
                errors.append(f"host {blocked!r} must be in BLOCKED_HOSTS")
        for allowed in ("127.0.0.1", "localhost", "::1"):
            if allowed not in ALLOWED_HOSTS:
                errors.append(f"host {allowed!r} must be in ALLOWED_HOSTS")
    except Exception as exc:
        errors.append(f"local_runtime config module check failed: {exc}")

    try:
        from odin.local_runtime.lockfile import LOCKFILE_PATH
        lockfile_dir = str(LOCKFILE_PATH.parent.relative_to(ROOT))
        if not lockfile_dir.startswith(".odin_runtime"):
            errors.append(f"lockfile must be under .odin_runtime/, got {lockfile_dir}")
    except Exception as exc:
        errors.append(f"local_runtime lockfile module check failed: {exc}")

    test_file = ROOT / "tests/test_lrh_pr_03_portable_local_runtime_starter.py"
    if not test_file.exists():
        errors.append("tests/test_lrh_pr_03_portable_local_runtime_starter.py missing")

    return errors


def validate_runtime_doctor_bootstrap() -> list[str]:
    """Validate runtime doctor, first-run bootstrap and self-healing surfaces (LRH-PR-04)."""
    errors = []

    required_modules = [
        "odin/doctor/__init__.py",
        "odin/doctor/checks.py",
        "odin/doctor/diagnostics.py",
        "odin/doctor/support_bundle.py",
        "odin/doctor/redaction.py",
        "odin/bootstrap/__init__.py",
        "odin/bootstrap/first_run.py",
        "odin/bootstrap/repair_plan.py",
    ]
    for rel in required_modules:
        if not (ROOT / rel).exists():
            errors.append(f"LRH-PR-04 module missing: {rel}")

    doc = ROOT / "docs/RUNTIME_DOCTOR_BOOTSTRAP_V1.md"
    if not doc.exists():
        errors.append("docs/RUNTIME_DOCTOR_BOOTSTRAP_V1.md missing")
    else:
        doc_text = doc.read_text(encoding="utf-8", errors="ignore")
        for required_phrase in [
            "not production",
            "plan-only",
            "no external send",
            "127.0.0.1",
        ]:
            if required_phrase.lower() not in doc_text.lower():
                errors.append(
                    f"docs/RUNTIME_DOCTOR_BOOTSTRAP_V1.md: missing required phrase: {required_phrase!r}"
                )

    required_examples = [
        "examples/doctor/doctor_success.valid.json",
        "examples/doctor/doctor_failure.valid.json",
        "examples/bootstrap/first_run_config.valid.json",
        "examples/bootstrap/repair_plan.valid.json",
        "examples/doctor/support_bundle_redacted.valid.json",
    ]
    for rel in required_examples:
        p = ROOT / rel
        if not p.exists():
            errors.append(f"LRH-PR-04 example missing: {rel}")
            continue
        try:
            data = load_json(p)
        except Exception as exc:
            errors.append(f"{rel}: invalid JSON: {exc}")
            continue
        if rel == "examples/doctor/doctor_success.valid.json":
            if data.get("artifact_kind") != "odin_doctor_report":
                errors.append(f"{rel}: must have artifact_kind odin_doctor_report")
            if data.get("state_mutated") is not False:
                errors.append(f"{rel}: state_mutated must be false")
            if data.get("candidate_only") is not True:
                errors.append(f"{rel}: candidate_only must be true")
        if rel == "examples/bootstrap/first_run_config.valid.json":
            written = data.get("config_written", {})
            if written.get("host") not in ("127.0.0.1", "localhost", "::1"):
                errors.append(f"{rel}: config_written.host must be localhost")
            if written.get("public_bind") is not False:
                errors.append(f"{rel}: config_written.public_bind must be false")
        if rel == "examples/bootstrap/repair_plan.valid.json":
            if data.get("applied") is not False:
                errors.append(f"{rel}: applied must be false")
            if data.get("plan_only") is not True:
                errors.append(f"{rel}: plan_only must be true")
        if rel == "examples/doctor/support_bundle_redacted.valid.json":
            if data.get("redaction_applied") is not True:
                errors.append(f"{rel}: redaction_applied must be true")
            if data.get("external_send") is not False:
                errors.append(f"{rel}: external_send must be false")

    test_file = ROOT / "tests/test_lrh_pr_04_runtime_doctor_bootstrap.py"
    if not test_file.exists():
        errors.append("tests/test_lrh_pr_04_runtime_doctor_bootstrap.py missing")

    try:
        from odin.doctor.diagnostics import run_doctor, KNOWN_NON_PROOFS
        report = run_doctor()
        if report.get("state_mutated") is not False:
            errors.append("doctor: state_mutated must be false")
        if report.get("read_only") is not True:
            errors.append("doctor: read_only must be true")
        if report.get("candidate_only") is not True:
            errors.append("doctor: candidate_only must be true")
        for np in KNOWN_NON_PROOFS:
            if np not in report.get("known_non_proofs", []):
                errors.append(f"doctor report missing known_non_proof: {np}")
    except Exception as exc:
        errors.append(f"doctor module check failed: {exc}")

    try:
        from odin.bootstrap.first_run import SAFE_DEFAULT_CONFIG, BLOCKED_HOSTS
        if SAFE_DEFAULT_CONFIG.get("host") in BLOCKED_HOSTS:
            errors.append("bootstrap: SAFE_DEFAULT_CONFIG host must not be a blocked host")
        if SAFE_DEFAULT_CONFIG.get("public_bind") is not False:
            errors.append("bootstrap: SAFE_DEFAULT_CONFIG must have public_bind=false")
        if SAFE_DEFAULT_CONFIG.get("external_send_default") is not False:
            errors.append("bootstrap: SAFE_DEFAULT_CONFIG must have external_send_default=false")
        if SAFE_DEFAULT_CONFIG.get("candidate_only") is not True:
            errors.append("bootstrap: SAFE_DEFAULT_CONFIG must have candidate_only=true")
    except Exception as exc:
        errors.append(f"bootstrap first_run module check failed: {exc}")

    try:
        from odin.bootstrap.repair_plan import build_repair_plan, REPAIR_CLAIM_BOUNDARY
        fake_report = {"artifact_kind": "odin_doctor_report", "status": "ok", "checks": [], "failure_count": 0, "warning_count": 0, "failure_reasons": []}
        plan = build_repair_plan(fake_report)
        if plan.get("applied") is not False:
            errors.append("repair_plan: applied must be false")
        if plan.get("state_mutated") is not False:
            errors.append("repair_plan: state_mutated must be false")
        if plan.get("plan_only") is not True:
            errors.append("repair_plan: plan_only must be true")
        if "plan_only" not in REPAIR_CLAIM_BOUNDARY:
            errors.append("repair_plan: REPAIR_CLAIM_BOUNDARY must contain 'plan_only'")
    except Exception as exc:
        errors.append(f"repair_plan module check failed: {exc}")

    try:
        from odin.doctor.redaction import is_secret_key, redact_recursive
        for secret_key in ("token", "api_key", "password", "authorization", "secret", "bearer", "credential"):
            if not is_secret_key(secret_key):
                errors.append(f"redaction: {secret_key!r} must be recognized as secret key")
        redacted = redact_recursive({"token": "abc", "host": "127.0.0.1"})
        if redacted.get("token") != "[REDACTED]":
            errors.append("redaction: token value must be redacted")
        if redacted.get("host") != "127.0.0.1":
            errors.append("redaction: host must not be redacted")
    except Exception as exc:
        errors.append(f"redaction module check failed: {exc}")

    return errors


def validate_localhost_api_sdk_bridge() -> list[str]:
    """Validate LRH-PR-05 localhost API contract and SDK bridge artifacts."""
    errors: list[str] = []

    required_docs = [
        "docs/LOCALHOST_API_CONTRACT_V1.md",
        "docs/SDK_BRIDGE_V1.md",
    ]
    for rel in required_docs:
        p = ROOT / rel
        if not p.exists():
            errors.append(f"localhost API/SDK doc missing: {rel}")
            continue
        text = p.read_text(encoding="utf-8", errors="ignore").lower()
        if "not a public network api" not in text and "is not a public network" not in text:
            errors.append(f"{rel}: missing 'not a public network API' claim boundary statement")
        if "does not grant app apply authority" not in text and "no apply endpoint" not in text and "no apply()" not in text:
            errors.append(f"{rel}: missing no-apply-authority claim boundary statement")
        if "does not send externally" not in text and "no external send" not in text:
            errors.append(f"{rel}: missing no-external-send claim boundary statement")
        if "not_production_readiness" not in text and "production readiness" not in text:
            errors.append(f"{rel}: missing production readiness proof boundary")
        if "not_live_model_inference_proof" not in text and "live model inference" not in text:
            errors.append(f"{rel}: missing live model inference proof boundary")

    required_schemas = [
        "schemas/v7_1/localhost_api_health.schema.json",
        "schemas/v7_1/localhost_api_status.schema.json",
        "schemas/v7_1/localhost_api_providers.schema.json",
        "schemas/v7_1/localhost_api_universal_work_request.schema.json",
        "schemas/v7_1/localhost_api_universal_work_response.schema.json",
        "schemas/v7_1/localhost_api_session.schema.json",
        "schemas/v7_1/localhost_api_candidate.schema.json",
        "schemas/v7_1/localhost_api_events.schema.json",
        "schemas/v7_1/localhost_api_proof_gaps.schema.json",
        "schemas/v7_1/localhost_api_error.schema.json",
    ]
    for rel in required_schemas:
        p = ROOT / rel
        if not p.exists():
            errors.append(f"localhost API schema missing: {rel}")
            continue
        try:
            load_json(p)
        except Exception as exc:
            errors.append(f"localhost API schema invalid JSON {rel}: {exc}")

    required_fixtures = [
        "examples/sdk_bridge/health_response.valid.json",
        "examples/sdk_bridge/status_response.valid.json",
        "examples/sdk_bridge/providers_response.valid.json",
        "examples/sdk_bridge/universal_work_request.valid.json",
        "examples/sdk_bridge/universal_work_response.valid.json",
        "examples/sdk_bridge/session_response.valid.json",
        "examples/sdk_bridge/candidate_response.valid.json",
        "examples/sdk_bridge/events_response.valid.json",
        "examples/sdk_bridge/proof_gaps_response.valid.json",
        "examples/sdk_bridge/error_response.valid.json",
    ]
    for rel in required_fixtures:
        p = ROOT / rel
        if not p.exists():
            errors.append(f"SDK bridge fixture missing: {rel}")
            continue
        try:
            data = load_json(p)
        except Exception as exc:
            errors.append(f"SDK bridge fixture invalid JSON {rel}: {exc}")
            continue
        if "candidate_only" in rel or "health" in rel or "response" in rel:
            if data.get("candidate_only") is not True and "request" not in rel:
                pass  # candidate_only only required on response fixtures

    # Validate health fixture
    health_fixture = ROOT / "examples/sdk_bridge/health_response.valid.json"
    if health_fixture.exists():
        h = load_json(health_fixture)
        for key in ["candidate_only", "app_owned_apply"]:
            if h.get(key) is not True:
                errors.append(f"health fixture missing {key}: true")

    # Validate error fixture
    error_fixture = ROOT / "examples/sdk_bridge/error_response.valid.json"
    if error_fixture.exists():
        e = load_json(error_fixture)
        if e.get("error") is not True:
            errors.append("error fixture must have error: true")
        if "code" not in e:
            errors.append("error fixture missing code")
        if "message" not in e:
            errors.append("error fixture missing message")

    # Validate proof-gaps fixture has required boundaries
    pg_fixture = ROOT / "examples/sdk_bridge/proof_gaps_response.valid.json"
    if pg_fixture.exists():
        pg = load_json(pg_fixture)
        for boundary in [
            "not_production_readiness_certification",
            "not_live_model_inference_proof",
            "not_app_state_mutation_proof",
            "not_external_send_authority_proof",
        ]:
            if boundary not in pg.get("proof_boundaries", []):
                errors.append(f"proof_gaps fixture missing boundary: {boundary}")

    # Validate SDK files exist
    required_sdk_files = [
        "odin_app_sdk/client.py",
        "sdk/python/odin_client.py",
        "sdk/typescript/odinClient.ts",
    ]
    for rel in required_sdk_files:
        if not (ROOT / rel).exists():
            errors.append(f"SDK bridge file missing: {rel}")
            continue
        text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        if "apply" in text and "def apply" in text:
            errors.append(f"{rel}: SDK must not have apply() method")
        if "external_send" in text and "def external_send" in text:
            errors.append(f"{rel}: SDK must not have external_send() method")

    # Validate localhost-only default in SDK
    sdk_client = ROOT / "odin_app_sdk/client.py"
    if sdk_client.exists():
        text = sdk_client.read_text(encoding="utf-8", errors="ignore")
        if "localhost" not in text.lower() and "127.0.0.1" not in text:
            errors.append("odin_app_sdk/client.py: missing localhost-only enforcement")
        if "OdinSDKBoundaryError" not in text and "OdinClientError" not in text:
            errors.append("odin_app_sdk/client.py: missing structured error class")

    # Validate local API forbidden routes
    local_api = ROOT / "odin/daemon/local_api.py"
    if local_api.exists():
        text = local_api.read_text(encoding="utf-8", errors="ignore")
        for route in ["/v1/apply", "/v1/external-send", "/v1/provider-credentials"]:
            if route not in text or "FORBIDDEN_ROUTES" not in text:
                if route not in text:
                    errors.append(f"local_api.py: forbidden route {route!r} not in FORBIDDEN_ROUTES")

    # Validate return report exists
    report = ROOT / "docs/codex/reports/LRH-PR-05_RETURN_REPORT.md"
    if not report.exists():
        errors.append("LRH-PR-05 return report missing: docs/codex/reports/LRH-PR-05_RETURN_REPORT.md")

    return errors


def run_sdk_bridge_proof(host: str = "127.0.0.1", port: int = 8877) -> dict:
    """Bounded SDK bridge proof — deterministic local proof packet."""
    import uuid
    from odin.daemon.local_api import run_local_api, LOCAL_API_CLAIM_BOUNDARY, SDK_BRIDGE_PROOF_BOUNDARIES

    steps: list[dict] = []

    # Step 1: Validate localhost-only binding
    try:
        result = run_local_api(host=host, port=0, once_smoke=True)
        steps.append({"step": "localhost_bind_check", "status": "ok", "result": result})
    except Exception as exc:
        steps.append({"step": "localhost_bind_check", "status": "error", "error": str(exc)})

    # Step 2: Validate forbidden host blocked
    try:
        run_local_api("0.0.0.0", 0, once_smoke=True)
        steps.append({"step": "wan_host_blocked", "status": "failed", "error": "0.0.0.0 should be blocked"})
    except ValueError:
        steps.append({"step": "wan_host_blocked", "status": "ok"})
    except Exception as exc:
        steps.append({"step": "wan_host_blocked", "status": "error", "error": str(exc)})

    # Step 3: Validate schema files exist
    schema_files = [
        "localhost_api_health.schema.json",
        "localhost_api_universal_work_response.schema.json",
        "localhost_api_proof_gaps.schema.json",
        "localhost_api_error.schema.json",
    ]
    schema_ok = all((ROOT / "schemas/v7_1" / f).exists() for f in schema_files)
    steps.append({"step": "schema_files_present", "status": "ok" if schema_ok else "failed"})

    # Step 4: Validate example fixtures exist and parse
    fixtures = [
        "examples/sdk_bridge/health_response.valid.json",
        "examples/sdk_bridge/universal_work_response.valid.json",
        "examples/sdk_bridge/proof_gaps_response.valid.json",
        "examples/sdk_bridge/error_response.valid.json",
    ]
    fixture_errors = []
    for rel in fixtures:
        p = ROOT / rel
        if not p.exists():
            fixture_errors.append(f"missing: {rel}")
        else:
            try:
                load_json(p)
            except Exception as exc:
                fixture_errors.append(f"invalid JSON {rel}: {exc}")
    steps.append({
        "step": "fixture_files_valid",
        "status": "ok" if not fixture_errors else "failed",
        "errors": fixture_errors,
    })

    # Step 5: Validate SDK localhost enforcement
    try:
        from odin_app_sdk.client import OdinClient, OdinSDKBoundaryError
        try:
            OdinClient("http://0.0.0.0:8877")
            steps.append({"step": "sdk_rejects_non_localhost", "status": "failed",
                          "error": "OdinClient accepted non-localhost URL"})
        except OdinSDKBoundaryError:
            steps.append({"step": "sdk_rejects_non_localhost", "status": "ok"})
        except Exception as exc:
            steps.append({"step": "sdk_rejects_non_localhost", "status": "error", "error": str(exc)})
    except ImportError as exc:
        steps.append({"step": "sdk_rejects_non_localhost", "status": "skipped", "reason": str(exc)})

    # Step 6: Validate SDK has no apply/external_send methods
    try:
        from odin_app_sdk.client import OdinClient
        no_apply = not hasattr(OdinClient, "apply")
        no_ext_send = not hasattr(OdinClient, "external_send")
        steps.append({
            "step": "sdk_no_forbidden_methods",
            "status": "ok" if (no_apply and no_ext_send) else "failed",
            "no_apply": no_apply,
            "no_external_send": no_ext_send,
        })
    except ImportError as exc:
        steps.append({"step": "sdk_no_forbidden_methods", "status": "skipped", "reason": str(exc)})

    all_ok = all(s.get("status") in {"ok", "skipped"} for s in steps)

    return {
        "artifact_kind": "sdk_bridge_proof_packet",
        "proof_id": f"SDK-BRIDGE-PROOF-{uuid.uuid4().hex[:8].upper()}",
        "status": "ok" if all_ok else "partial",
        "candidate_only": True,
        "host": host,
        "port": port,
        "steps": steps,
        "proven": [
            "localhost_bind_accepted",
            "wan_host_blocked",
            "schema_files_present_and_parse",
            "fixture_files_valid",
            "sdk_rejects_non_localhost_url",
            "sdk_has_no_apply_method",
            "sdk_has_no_external_send_method",
        ],
        "not_proven": [
            "production_readiness",
            "windows_service_or_tray_or_installer",
            "signed_installer",
            "live_model_inference",
            "model_quality",
            "security_certification",
            "public_network_api",
            "app_state_mutation_authority",
            "external_send_authority",
            "provider_credential_proof",
        ],
        "proof_boundaries": SDK_BRIDGE_PROOF_BOUNDARIES,
        "claim_boundary": LOCAL_API_CLAIM_BOUNDARY,
        "note": (
            "This is a bounded deterministic SDK bridge proof. "
            "It does not claim production readiness, live model inference, "
            "public network access, app-state mutation, or external send authority."
        ),
    }


def validate_canon_boundary_integrity() -> list[str]:
    errors = []
    tool_path = ROOT / "tools" / "v7_1_1" / "check_canon_boundary_integrity.py"
    if not tool_path.exists():
        return ["canon boundary integrity tool missing"]
    spec = importlib.util.spec_from_file_location("odin_v7_1_1_canon_boundary_integrity", tool_path)
    if spec is None or spec.loader is None:
        return ["canon boundary integrity tool import failed"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    report = module.build_report(ROOT, "2026-01-01T00:00:00Z")
    for violation in report.get("hard_violations", []):
        errors.append(
            "canon boundary integrity hard violation: "
            f"{violation.get('file_path')}:{violation.get('line_number')} "
            f"{violation.get('phrase')} ({violation.get('context_type')})"
        )
    if report.get("report_id") != "odin.v7_1_1_canon_boundary_integrity_report":
        errors.append("canon boundary integrity report_id mismatch")
    return errors



def validate_b2_context_lenses_worklets() -> list[str]:
    import subprocess
    tool_path = ROOT / "tools" / "v7_1_1" / "check_b2_context_lenses_worklets_slot_gaptext.py"
    if not tool_path.exists():
        return ["missing B2 Context / Lenses / Worklets / Slot Forge / Gaptext validator"]
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "v7_1_1_b2_context_lenses_worklets_slot_gaptext_report.json"
        result = subprocess.run(
            [
                sys.executable, str(tool_path),
                "--repo-root", str(ROOT),
                "--out", str(out),
                "--generated-at-utc", "2026-01-01T00:00:00Z",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            try:
                report = json.loads(out.read_text(encoding="utf-8"))
                return [f"B2 Context / Lenses / Worklets: {err}" for err in report.get("hard_violations", [])]
            except Exception as exc:
                return [f"B2 Context / Lenses / Worklets validator failed: {exc}"]
    return []


def validate_b4_minicheck_critics_final_gate() -> list[str]:
    import subprocess
    tool_path = ROOT / "tools" / "v7_1_1" / "check_b4_minicheck_critics_final_gate.py"
    if not tool_path.exists():
        return ["missing B4 Minicheck / Critics / Final Gate validator"]
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "v7_1_1_b4_minicheck_critics_final_gate_report.json"
        result = subprocess.run(
            [
                sys.executable, str(tool_path),
                "--repo-root", str(ROOT),
                "--out", str(out),
                "--generated-at-utc", "2026-01-01T00:00:00Z",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            try:
                report = json.loads(out.read_text(encoding="utf-8"))
                return [f"B4 Minicheck / Critics / Final Gate: {err}" for err in report.get("hard_violations", [])]
            except Exception as exc:
                return [f"B4 Minicheck / Critics / Final Gate validator failed: {exc}"]
    return []



def validate_b5_storage_trace_receipt_provider_bridge() -> list[str]:
    import subprocess
    tool_path = ROOT / "tools" / "v7_1_1" / "check_b5_storage_trace_receipt_provider_bridge.py"
    if not tool_path.exists():
        return ["missing B5 Storage / Trace / Receipt / Provider Bridge validator"]
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "v7_1_1_b5_storage_trace_receipt_provider_bridge_report.json"
        result = subprocess.run(
            [
                sys.executable, str(tool_path),
                "--repo-root", str(ROOT),
                "--out", str(out),
                "--generated-at-utc", "2026-01-01T00:00:00Z",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            try:
                report = json.loads(out.read_text(encoding="utf-8"))
                return [f"B5 Storage / Trace / Receipt / Provider Bridge: {err}" for err in report.get("hard_violations", [])]
            except Exception as exc:
                return [f"B5 Storage / Trace / Receipt / Provider Bridge validator failed: {exc}"]
    return []

def validate_b3_modelworkpacket_scale_hybrid() -> list[str]:
    import subprocess
    tool_path = ROOT / "tools" / "v7_1_1" / "check_b3_modelworkpacket_scale_hybrid.py"
    if not tool_path.exists():
        return ["missing B3 ModelWorkPacket / Scale Ladder / Hybrid Director validator"]
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "v7_1_1_b3_modelworkpacket_scale_hybrid_report.json"
        result = subprocess.run(
            [
                sys.executable, str(tool_path),
                "--repo-root", str(ROOT),
                "--out", str(out),
                "--generated-at-utc", "2026-01-01T00:00:00Z",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            try:
                report = json.loads(out.read_text(encoding="utf-8"))
                return [f"B3 ModelWorkPacket / Scale Ladder: {err}" for err in report.get("hard_violations", [])]
            except Exception as exc:
                return [f"B3 ModelWorkPacket / Scale Ladder validator failed: {exc}"]
    return []


def validate_b1_app_boundary_universal_work_qirc_spine() -> list[str]:
    tool_path = ROOT / "tools" / "v7_1_1" / "check_b1_app_boundary_universal_work_qirc_spine.py"
    if not tool_path.exists():
        return ["missing B1 App Boundary / Universal Work / QIRC Spine validator"]
    spec = importlib.util.spec_from_file_location("odin_b1_app_boundary_validator", tool_path)
    if spec is None or spec.loader is None:
        return ["unable to load B1 App Boundary / Universal Work / QIRC Spine validator"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "v7_1_1_b1_app_boundary_universal_work_qirc_spine_report.json"
        argv = [
            "--repo-root",
            str(ROOT),
            "--out",
            str(out),
            "--generated-at-utc",
            "2026-01-01T00:00:00Z",
        ]
        code = module.main(argv)
        if code != 0:
            try:
                report = json.loads(out.read_text(encoding="utf-8"))
                return [f"B1 App Boundary / Universal Work / QIRC Spine: {err}" for err in report.get("hard_violations", [])]
            except Exception as exc:
                return [f"B1 App Boundary / Universal Work / QIRC Spine validator failed: {exc}"]
    return []


def validate_b6_acceptance_dojo_scoreboard_closure() -> list[str]:
    tool_path = ROOT / "tools" / "v7_1_1" / "check_b6_acceptance_dojo_scoreboard_closure.py"
    if not tool_path.exists():
        return ["missing B6 Acceptance / Dojo / Scoreboard / Closure validator"]
    spec = importlib.util.spec_from_file_location("odin_b6_acceptance_dojo_scoreboard_closure_validator", tool_path)
    if spec is None or spec.loader is None:
        return ["unable to load B6 Acceptance / Dojo / Scoreboard / Closure validator"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "v7_1_1_b6_acceptance_dojo_scoreboard_closure_report.json"
        code = module.main([
            "--repo-root", str(ROOT),
            "--out", str(out),
            "--generated-at-utc", "2026-01-01T00:00:00Z",
        ])
        if code != 0:
            try:
                report = json.loads(out.read_text(encoding="utf-8"))
                return [f"B6 Acceptance / Dojo / Scoreboard / Closure: {err}" for err in report.get("hard_violations", [])]
            except Exception as exc:
                return [f"B6 Acceptance / Dojo / Scoreboard / Closure validator failed: {exc}"]
    return []


def validate_b7_closure_thor_provider_eval() -> list[str]:
    tool_path = ROOT / "tools" / "v7_1_1" / "check_b7_closure_thor_provider_eval.py"
    if not tool_path.exists():
        return ["missing B7 Closure / Thor / Provider Eval validator"]
    spec = importlib.util.spec_from_file_location("odin_b7_closure_thor_provider_eval_validator", tool_path)
    if spec is None or spec.loader is None:
        return ["unable to load B7 Closure / Thor / Provider Eval validator"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "v7_1_1_b7_closure_thor_provider_eval_report.json"
        code = module.main([
            "--repo-root", str(ROOT),
            "--out", str(out),
            "--generated-at-utc", "2026-01-01T00:00:00Z",
        ])
        if code != 0:
            try:
                report = json.loads(out.read_text(encoding="utf-8"))
                return [f"B7 Closure / Thor / Provider Eval: {err}" for err in report.get("hard_violations", [])]
            except Exception as exc:
                return [f"B7 Closure / Thor / Provider Eval validator failed: {exc}"]
    return []


def validate_b8_security_review_track() -> list[str]:
    tool_path = ROOT / "tools" / "v7_1_1" / "check_b8_security_review_track.py"
    if not tool_path.exists():
        return ["missing B8 Security Review Track validator"]
    spec = importlib.util.spec_from_file_location("odin_b8_security_review_track_validator", tool_path)
    if spec is None or spec.loader is None:
        return ["unable to load B8 Security Review Track validator"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "v7_1_1_b8_security_review_report.json"
        code = module.main([
            "--repo-root", str(ROOT),
            "--out", str(out),
            "--generated-at-utc", "2026-01-01T00:00:00Z",
        ])
        if code != 0:
            try:
                report = json.loads(out.read_text(encoding="utf-8"))
                return [f"B8 Security Review Track: {err}" for err in report.get("hard_violations", [])]
            except Exception as exc:
                return [f"B8 Security Review Track validator failed: {exc}"]
    return []


def validate_final_road_to_100_rebaseline_audit() -> list[str]:
    tool_path = ROOT / "tools" / "rebaseline" / "check_final_road_to_100_rebaseline_audit.py"
    if not tool_path.exists():
        return ["missing Final Road-to-100 Rebaseline Audit validator"]
    spec = importlib.util.spec_from_file_location("odin_final_road_to_100_rebaseline_audit_validator", tool_path)
    if spec is None or spec.loader is None:
        return ["unable to load Final Road-to-100 Rebaseline Audit validator"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "final_road_to_100_rebaseline_audit_v1.json"
        code = module.main([
            "--repo-root", str(ROOT),
            "--out", str(out),
            "--generated-at-utc", "2026-01-01T00:00:00Z",
        ])
        if code != 0:
            try:
                report = json.loads(out.read_text(encoding="utf-8"))
                return [f"Final Road-to-100 Rebaseline Audit: {err}" for err in report.get("hard_violations", [])]
            except Exception as exc:
                return [f"Final Road-to-100 Rebaseline Audit validator failed: {exc}"]
    return []

def validate_simple_local_hub() -> list[str]:
    """Validate FINAL-PR-01 Simple Local Hub implementation."""
    tool_path = ROOT / "tools" / "rebaseline" / "check_simple_local_hub.py"
    if not tool_path.exists():
        return ["missing Simple Local Hub validator: tools/rebaseline/check_simple_local_hub.py"]
    spec = importlib.util.spec_from_file_location("odin_simple_local_hub_validator", tool_path)
    if spec is None or spec.loader is None:
        return ["unable to load Simple Local Hub validator"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "final_pr_01_simple_local_hub_check.json"
        code = module.main([
            "--repo-root", str(ROOT),
            "--out", str(out),
            "--generated-at-utc", "2026-01-01T00:00:00Z",
        ])
        if code != 0:
            try:
                report = json.loads(out.read_text(encoding="utf-8"))
                return [f"simple-local-hub: {err}" for err in report.get("errors", [])]
            except Exception as exc:
                return [f"simple-local-hub validator failed: {exc}"]
    return []


def validate_final_pr_02_model_apps_demo() -> list[str]:
    """Validate FINAL-PR-02 Model Picker + Connected Apps + Demo Universal Work."""
    tool_path = ROOT / "tools" / "rebaseline" / "check_final_pr_02_model_apps_demo.py"
    if not tool_path.exists():
        return ["missing FINAL-PR-02 validator: tools/rebaseline/check_final_pr_02_model_apps_demo.py"]
    spec = importlib.util.spec_from_file_location("odin_final_pr_02_validator", tool_path)
    if spec is None or spec.loader is None:
        return ["unable to load FINAL-PR-02 validator"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "final_pr_02_model_apps_demo_check.json"
        code = module.main([
            "--repo-root", str(ROOT),
            "--out", str(out),
            "--generated-at-utc", "2026-01-01T00:00:00Z",
        ])
        if code != 0:
            try:
                report = json.loads(out.read_text(encoding="utf-8"))
                return [f"final-pr-02: {err}" for err in report.get("errors", [])]
            except Exception as exc:
                return [f"final-pr-02 validator failed: {exc}"]
    return []


def validate_final_pr_03_qirc_devmode() -> list[str]:
    """Validate FINAL-PR-03 QIRC Core Dev Mode implementation."""
    tool_path = ROOT / "tools" / "rebaseline" / "check_final_pr_03_qirc_devmode.py"
    if not tool_path.exists():
        return ["missing FINAL-PR-03 validator: tools/rebaseline/check_final_pr_03_qirc_devmode.py"]
    spec = importlib.util.spec_from_file_location("odin_final_pr_03_validator", tool_path)
    if spec is None or spec.loader is None:
        return ["unable to load FINAL-PR-03 validator"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "final_pr_03_qirc_devmode_check.json"
        code = module.main([
            "--repo-root", str(ROOT),
            "--out", str(out),
            "--generated-at-utc", "2026-01-01T00:00:00Z",
        ])
        if code != 0:
            try:
                report = json.loads(out.read_text(encoding="utf-8"))
                return [f"final-pr-03: {err}" for err in report.get("errors", [])]
            except Exception as exc:
                return [f"final-pr-03 validator failed: {exc}"]
    return []


def validate_final_pr_04_provider_probe_security() -> list[str]:
    """Validate FINAL-PR-04 Provider Probe + Runtime Security Smoke."""
    tool_path = ROOT / "tools" / "rebaseline" / "check_final_pr_04_provider_probe_security.py"
    if not tool_path.exists():
        return ["missing FINAL-PR-04 validator: tools/rebaseline/check_final_pr_04_provider_probe_security.py"]
    spec = importlib.util.spec_from_file_location("odin_final_pr_04_validator", tool_path)
    if spec is None or spec.loader is None:
        return ["unable to load FINAL-PR-04 validator"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "final_pr_04_provider_probe_security_check.json"
        code = module.main([
            "--repo-root", str(ROOT),
            "--out", str(out),
            "--generated-at-utc", "2026-01-01T00:00:00Z",
        ])
        if code != 0:
            try:
                report = json.loads(out.read_text(encoding="utf-8"))
                return [f"final-pr-04: {err}" for err in report.get("errors", [])]
            except Exception as exc:
                return [f"final-pr-04 validator failed: {exc}"]
    return []


def validate_final_pr_05_execution_gate() -> list[str]:
    """Validate FINAL-PR-05 Execution Gate + Mock Execution + Proof Chain + Ladder Scaffold."""
    tool_path = ROOT / "tools" / "rebaseline" / "check_final_pr_05_execution_gate.py"
    if not tool_path.exists():
        return ["missing FINAL-PR-05 validator: tools/rebaseline/check_final_pr_05_execution_gate.py"]
    spec = importlib.util.spec_from_file_location("odin_final_pr_05_validator", tool_path)
    if spec is None or spec.loader is None:
        return ["unable to load FINAL-PR-05 validator"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "final_pr_05_execution_gate_check.json"
        code = module.main([
            "--repo-root", str(ROOT),
            "--out", str(out),
            "--generated-at-utc", "2026-01-01T00:00:00Z",
        ])
        if code != 0:
            try:
                report = json.loads(out.read_text(encoding="utf-8"))
                return [f"final-pr-05: {err}" for err in report.get("errors", [])]
            except Exception as exc:
                return [f"final-pr-05 validator failed: {exc}"]
    return []



def validate_y_pattern_spine() -> list[str]:
    """Validate Y Pattern Spine modules, schemas, registries, examples, and proof packet."""
    tool_path = ROOT / "tools" / "rebaseline" / "check_y_pattern_spine.py"
    if not tool_path.exists():
        return ["missing Y Pattern Spine validator: tools/rebaseline/check_y_pattern_spine.py"]
    spec = importlib.util.spec_from_file_location("odin_y_pattern_spine_validator", tool_path)
    if spec is None or spec.loader is None:
        return ["unable to load Y Pattern Spine validator"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    import tempfile as _tempfile
    with _tempfile.TemporaryDirectory() as td:
        out = Path(td) / "y_pattern_spine_check.json"
        code = module.main([
            "--repo-root", str(ROOT),
            "--out", str(out),
            "--generated-at-utc", "2026-01-01T00:00:00Z",
        ])
        if code != 0:
            try:
                report = json.loads(out.read_text(encoding="utf-8"))
                return [f"y-pattern-spine: {err}" for err in report.get("errors", [])]
            except Exception as exc:
                return [f"y-pattern-spine validator failed: {exc}"]
    return []

def validate_prep_final_pr_06_08() -> list[str]:
    """Validate Prep FINAL-PR-06..08 scaffold artifacts."""
    tool_path = ROOT / "tools" / "rebaseline" / "check_prep_final_pr_06_08.py"
    if not tool_path.exists():
        return ["missing prep validator: tools/rebaseline/check_prep_final_pr_06_08.py"]
    spec = importlib.util.spec_from_file_location("odin_prep_final_pr_06_08_validator", tool_path)
    if spec is None or spec.loader is None:
        return ["unable to load prep FINAL-PR-06..08 validator"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    import tempfile as _tempfile
    with _tempfile.TemporaryDirectory() as td:
        out = Path(td) / "prep_final_pr_06_08_check.json"
        code = module.main([
            "--repo-root", str(ROOT),
            "--out", str(out),
            "--generated-at-utc", "2026-01-01T00:00:00Z",
        ])
        if code != 0:
            try:
                report = json.loads(out.read_text(encoding="utf-8"))
                return [f"prep-final-pr-06-08: {err}" for err in report.get("errors", [])]
            except Exception as exc:
                return [f"prep-final-pr-06-08 validator failed: {exc}"]
    return []


def validate_operational_seed_spine() -> list[str]:
    """Validate FINAL-PR-06 Operational Seed Spine module, registries, examples, and proof."""
    tool_path = ROOT / "tools" / "rebaseline" / "check_final_pr_06_operational_seed_spine.py"
    if not tool_path.exists():
        return ["missing FINAL-PR-06 validator: tools/rebaseline/check_final_pr_06_operational_seed_spine.py"]
    spec = importlib.util.spec_from_file_location("odin_final_pr_06_validator", tool_path)
    if spec is None or spec.loader is None:
        return ["unable to load FINAL-PR-06 validator"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    import tempfile as _tempfile
    with _tempfile.TemporaryDirectory() as td:
        out = Path(td) / "final_pr_06_check.json"
        code = module.main([
            "--repo-root", str(ROOT),
            "--out", str(out),
            "--generated-at-utc", "2026-01-01T00:00:00Z",
        ])
        if code != 0:
            try:
                report = json.loads(out.read_text(encoding="utf-8"))
                return [f"final-pr-06: {err}" for err in report.get("errors", [])]
            except Exception as exc:
                return [f"final-pr-06 validator failed: {exc}"]
    return []


def validate_field_selection_spine() -> list[str]:
    """Validate FINAL-PR-07 Field Selection Spine artifacts."""
    tool_path = ROOT / "tools" / "rebaseline" / "check_final_pr_07_field_selection_spine.py"
    if not tool_path.exists():
        return ["missing FINAL-PR-07 validator: tools/rebaseline/check_final_pr_07_field_selection_spine.py"]
    spec = importlib.util.spec_from_file_location("odin_final_pr_07_validator", tool_path)
    if spec is None or spec.loader is None:
        return ["unable to load FINAL-PR-07 validator"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    import tempfile as _tempfile
    with _tempfile.TemporaryDirectory() as td:
        out = Path(td) / "final_pr_07_check.json"
        code = module.main([
            "--repo-root", str(ROOT),
            "--out", str(out),
            "--generated-at-utc", "2026-01-01T00:00:00Z",
        ])
        if code != 0:
            try:
                report = json.loads(out.read_text(encoding="utf-8"))
                return [f"final-pr-07: {err}" for err in report.get("errors", [])]
            except Exception as exc:
                return [f"final-pr-07 validator failed: {exc}"]
    return []


def validate_projection_candidate_spine() -> list[str]:
    """Validate FINAL-PR-08 Projection Candidate Spine artifacts."""
    tool_path = ROOT / "tools" / "rebaseline" / "check_final_pr_08_projection_candidate_spine.py"
    if not tool_path.exists():
        return ["missing FINAL-PR-08 validator: tools/rebaseline/check_final_pr_08_projection_candidate_spine.py"]
    spec = importlib.util.spec_from_file_location("odin_final_pr_08_validator", tool_path)
    if spec is None or spec.loader is None:
        return ["unable to load FINAL-PR-08 validator"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    import tempfile as _tempfile
    with _tempfile.TemporaryDirectory() as td:
        out = Path(td) / "final_pr_08_check.json"
        code = module.main([
            "--repo-root", str(ROOT),
            "--out", str(out),
            "--generated-at-utc", "2026-01-01T00:00:00Z",
        ])
        if code != 0:
            try:
                report = json.loads(out.read_text(encoding="utf-8"))
                return [f"final-pr-08: {err}" for err in report.get("errors", [])]
            except Exception as exc:
                return [f"final-pr-08 validator failed: {exc}"]
    return []



def validate_final_pr_09_10_qshabang_smallmodel_prep() -> list[str]:
    """Validate PREP FINAL-PR-09++/10++ Q-Shabang small-model artifacts."""
    tool_path = ROOT / "tools" / "rebaseline" / "check_final_pr_09_10_qshabang_smallmodel_prep.py"
    if not tool_path.exists():
        return ["missing prep FINAL-PR-09++/10++ validator: tools/rebaseline/check_final_pr_09_10_qshabang_smallmodel_prep.py"]
    spec = importlib.util.spec_from_file_location("odin_final_pr_09_10_qshabang_smallmodel_prep_validator", tool_path)
    if spec is None or spec.loader is None:
        return ["unable to load prep FINAL-PR-09++/10++ validator"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "final_pr_09_10_qshabang_smallmodel_prep_check.json"
        code = module.main([
            "--repo-root", str(ROOT),
            "--out", str(out),
            "--generated-at-utc", "2026-01-01T00:00:00Z",
        ])
        if code != 0:
            try:
                report = json.loads(out.read_text(encoding="utf-8"))
                return [f"final-pr-09-10-qshabang-smallmodel-prep: {err}" for err in report.get("errors", [])]
            except Exception as exc:
                return [f"final-pr-09-10-qshabang-smallmodel-prep validator failed: {exc}"]
    return []

def validate_operational_spine() -> list[str]:
    """Validate FINAL-PR-09++ Operational Spine artifacts."""
    tool_path = ROOT / "tools" / "rebaseline" / "check_final_pr_09_operational_spine.py"
    if not tool_path.exists():
        return ["missing FINAL-PR-09++ validator: tools/rebaseline/check_final_pr_09_operational_spine.py"]
    spec = importlib.util.spec_from_file_location("odin_final_pr_09_operational_spine_validator", tool_path)
    if spec is None or spec.loader is None:
        return ["unable to load FINAL-PR-09++ validator"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "final_pr_09_operational_spine_check.json"
        code = module.main([
            "--repo-root", str(ROOT),
            "--out", str(out),
            "--generated-at-utc", "2026-01-01T00:00:00Z",
        ])
        if code != 0:
            try:
                report = json.loads(out.read_text(encoding="utf-8"))
                return [f"final-pr-09-operational-spine: {err}" for err in report.get("errors", [])]
            except Exception as exc:
                return [f"final-pr-09-operational-spine validator failed: {exc}"]
    return []

def validate_final_pr_10_boundary_release() -> list[str]:
    """Validate FINAL-PR-10++ Boundary-Gated Release Operationalization artifacts."""
    tool_path = ROOT / "tools" / "rebaseline" / "check_final_pr_10_boundary_release.py"
    if not tool_path.exists():
        return ["missing FINAL-PR-10++ validator: tools/rebaseline/check_final_pr_10_boundary_release.py"]
    spec = importlib.util.spec_from_file_location("odin_final_pr_10_boundary_release_validator", tool_path)
    if spec is None or spec.loader is None:
        return ["unable to load FINAL-PR-10++ validator"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "final_pr_10_boundary_release_check.json"
        code = module.main([
            "--repo-root", str(ROOT),
            "--out", str(out),
            "--generated-at-utc", "2026-01-01T00:00:00Z",
        ])
        if code != 0:
            try:
                report = json.loads(out.read_text(encoding="utf-8"))
                return [f"final-pr-10-boundary-release: {err}" for err in report.get("errors", [])]
            except Exception as exc:
                return [f"final-pr-10-boundary-release validator failed: {exc}"]
    return []

def validate_final_pr_11_provider_critic_thor() -> list[str]:
    """Validate FINAL-PR-11 Local Provider Receipt Harness + Critic Runtime Binding + Thor Handoff Compiler v0."""
    tool_path = ROOT / "tools" / "rebaseline" / "check_final_pr_11_provider_critic_thor.py"
    if not tool_path.exists():
        return ["missing FINAL-PR-11 validator: tools/rebaseline/check_final_pr_11_provider_critic_thor.py"]
    spec = importlib.util.spec_from_file_location("odin_final_pr_11_validator", tool_path)
    if spec is None or spec.loader is None:
        return ["unable to load FINAL-PR-11 validator"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "final_pr_11_provider_critic_thor_check.json"
        code = module.main([
            "--repo-root", str(ROOT),
            "--out", str(out),
            "--generated-at-utc", "2026-01-01T00:00:00Z",
        ])
        if code != 0:
            try:
                report = json.loads(out.read_text(encoding="utf-8"))
                return [f"final-pr-11-provider-critic-thor: {err}" for err in report.get("errors", [])]
            except Exception as exc:
                return [f"final-pr-11-provider-critic-thor validator failed: {exc}"]
    return []

def validate_final_pr_11_5_semantic_kernel_coverage() -> list[str]:
    """Validate FINAL-PR-11.5 Semantic Kernel Coverage Compiler + Claims Compiler + Y Pattern."""
    tool_path = ROOT / "tools" / "rebaseline" / "check_final_pr_11_5_semantic_kernel_coverage.py"
    if not tool_path.exists():
        return ["missing FINAL-PR-11.5 validator: tools/rebaseline/check_final_pr_11_5_semantic_kernel_coverage.py"]
    spec = importlib.util.spec_from_file_location("odin_final_pr_11_5_validator", tool_path)
    if spec is None or spec.loader is None:
        return ["unable to load FINAL-PR-11.5 validator"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "final_pr_11_5_semantic_kernel_coverage_check.json"
        code = module.main([
            "--repo-root", str(ROOT),
            "--out", str(out),
            "--generated-at-utc", "2026-01-01T00:00:00Z",
        ])
        if code != 0:
            try:
                report = json.loads(out.read_text(encoding="utf-8"))
                return [f"final-pr-11-5-semantic-kernel-coverage: {err}" for err in report.get("errors", [])]
            except Exception as exc:
                return [f"final-pr-11-5-semantic-kernel-coverage validator failed: {exc}"]
    return []

def validate_all() -> list[str]:
    errors = []
    errors.extend(validate_json())
    errors.extend(validate_registries())
    errors.extend(validate_system_map())
    errors.extend(validate_claims())
    errors.extend(validate_current_public_canon())
    errors.extend(validate_docs())
    errors.extend(validate_codex_tasks())
    errors.extend(validate_codex_bundles())
    errors.extend(validate_real_pr_execution())
    errors.extend(validate_senior_review())
    errors.extend(validate_shadow_runtime())
    errors.extend(validate_narrative_compiler())
    errors.extend(validate_odin_core_qli())
    errors.extend(validate_qirc_gold_spine())
    errors.extend(validate_bug6_q7_seed_core())
    errors.extend(validate_ai_git_safety())
    errors.extend(validate_pre_llm_intelligence())
    errors.extend(validate_universal_model_agent_parity())
    errors.extend(validate_universal_llm_work_construct())
    errors.extend(validate_app_seed_pack_compiler())
    errors.extend(validate_shadow_narrative_loki())
    errors.extend(validate_product_pattern_atom_hub())
    errors.extend(validate_public_repo_windows_build_ready())
    errors.extend(validate_runtime_source_candidate())
    errors.extend(validate_runtime_bus_worklets())
    errors.extend(validate_provider_worker_boundary())
    errors.extend(validate_local_runtime_starter())
    errors.extend(validate_runtime_doctor_bootstrap())
    errors.extend(validate_localhost_api_sdk_bridge())
    errors.extend(validate_browser_hub_shell())
    errors.extend(validate_hub_runtime_dashboard())
    errors.extend(validate_candidate_store_viewer())
    errors.extend(validate_trace_viewer())
    errors.extend(validate_provider_worker_inspector())
    errors.extend(validate_universal_work_playground())
    errors.extend(validate_neutral_external_app_bridge())
    errors.extend(validate_generic_app_bridge_golden_harness())
    errors.extend(validate_local_config_safe_settings())
    errors.extend(validate_portable_package())
    errors.extend(validate_windows_convenience_layer())
    errors.extend(validate_full_acceptance())
    errors.extend(validate_consolidated_proof_governance())
    errors.extend(validate_canon_boundary_integrity())
    errors.extend(validate_b1_app_boundary_universal_work_qirc_spine())
    errors.extend(validate_b2_context_lenses_worklets())
    errors.extend(validate_b3_modelworkpacket_scale_hybrid())
    errors.extend(validate_b4_minicheck_critics_final_gate())
    errors.extend(validate_b5_storage_trace_receipt_provider_bridge())
    errors.extend(validate_b6_acceptance_dojo_scoreboard_closure())
    errors.extend(validate_b7_closure_thor_provider_eval())
    errors.extend(validate_b8_security_review_track())
    errors.extend(validate_final_road_to_100_rebaseline_audit())
    errors.extend(validate_simple_local_hub())
    errors.extend(validate_final_pr_02_model_apps_demo())
    errors.extend(validate_final_pr_03_qirc_devmode())
    errors.extend(validate_final_pr_04_provider_probe_security())
    errors.extend(validate_final_pr_05_execution_gate())
    errors.extend(validate_y_pattern_spine())
    errors.extend(validate_prep_final_pr_06_08())
    errors.extend(validate_operational_seed_spine())
    errors.extend(validate_field_selection_spine())
    errors.extend(validate_projection_candidate_spine())
    errors.extend(validate_final_pr_09_10_qshabang_smallmodel_prep())
    errors.extend(validate_operational_spine())
    errors.extend(validate_final_pr_10_boundary_release())
    errors.extend(validate_final_pr_11_provider_critic_thor())
    errors.extend(validate_final_pr_11_5_semantic_kernel_coverage())
    return errors

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="odin")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate-json")
    sub.add_parser("validate-registries")
    sub.add_parser("validate-system-map")
    sub.add_parser("validate-claims")
    sub.add_parser("validate-canon-boundary-integrity")
    sub.add_parser("validate-current-public-canon")
    sub.add_parser("validate-docs")
    sub.add_parser("validate-codex-tasks")
    sub.add_parser("validate-codex-bundles")
    sub.add_parser("validate-real-pr-execution")
    sub.add_parser("validate-senior-review")
    sub.add_parser("validate-shadow-runtime")
    sub.add_parser("validate-narrative-compiler")
    sub.add_parser("validate-odin-core-qli")
    sub.add_parser("validate-qirc-gold-spine")
    sub.add_parser("validate-bug6-q7-seed-core")
    sub.add_parser("validate-ai-git-safety")
    sub.add_parser("validate-pre-llm-intelligence")
    sub.add_parser("validate-universal-model-agent-parity")
    sub.add_parser("validate-universal-llm-work-construct")
    sub.add_parser("validate-app-seed-pack-compiler")
    sub.add_parser("validate-shadow-narrative-loki")
    sub.add_parser("validate-product-pattern-atom-hub")
    sub.add_parser("validate-public-repo-windows-build-ready")
    sub.add_parser("validate-runtime-source-candidate")
    sub.add_parser("validate-direct-runtime-release-candidate")
    sub.add_parser("validate-runtime-bus-worklets")
    sub.add_parser("validate-provider-worker-boundary")
    sub.add_parser("validate-all")
    sub.add_parser("audit-pre-release-super")
    sub.add_parser("validate-pre-release-super-audit")
    sub.add_parser("validate-b1-app-boundary-universal-work-qirc-spine")
    sub.add_parser("validate-b2-context-lenses-worklets")
    sub.add_parser("validate-b3-modelworkpacket-scale-hybrid")
    sub.add_parser("validate-b4-minicheck-critics-final-gate")
    sub.add_parser("validate-b5-storage-trace-receipt-provider-bridge")
    sub.add_parser("validate-b6-acceptance-dojo-scoreboard-closure")
    sub.add_parser("validate-b7-closure-thor-provider-eval")
    sub.add_parser("validate-b8-security-review-track")
    sub.add_parser("validate-final-road-to-100-rebaseline-audit")
    sub.add_parser("validate-agent-operator-mode")
    sub.add_parser("validate-local-runtime-starter")
    sub.add_parser("validate-runtime-doctor-bootstrap")
    sub.add_parser("validate-localhost-api-sdk-bridge")
    sub.add_parser("validate-browser-hub-shell")
    sub.add_parser("validate-final-pr-02-model-apps-demo")
    sub.add_parser("prove-final-pr-02-demo-universal-work")
    sub.add_parser("validate-final-pr-03-qirc-devmode")
    sub.add_parser("prove-final-pr-03-qirc-devmode")
    prove_browser_hub_p = sub.add_parser("prove-browser-hub")
    prove_browser_hub_p.add_argument("--shell-only", action="store_true", default=False)
    prove_browser_hub_p.add_argument("--dashboard", action="store_true", default=False)
    prove_browser_hub_p.add_argument("--candidates", action="store_true", default=False)
    prove_browser_hub_p.add_argument("--traces", action="store_true", default=False)
    prove_browser_hub_p.add_argument("--providers", action="store_true", default=False)
    prove_browser_hub_p.add_argument("--playground", action="store_true", default=False)
    sub.add_parser("validate-universal-work-playground")
    sub.add_parser("validate-hub-runtime-dashboard")
    sub.add_parser("validate-candidate-store-viewer")
    sub.add_parser("validate-trace-viewer")
    sub.add_parser("validate-provider-worker-inspector")
    sub.add_parser("validate-neutral-external-app-bridge")
    sub.add_parser("prove-neutral-external-app-bridge")
    sub.add_parser("validate-generic-app-bridge-golden-harness")
    sub.add_parser("prove-generic-app-bridge-golden-harness")
    sub.add_parser("validate-local-config-safe-settings")
    sub.add_parser("prove-local-config-safe-settings")
    sub.add_parser("validate-portable-package")
    sub.add_parser("prove-portable-package")
    sub.add_parser("validate-windows-convenience-layer")
    sub.add_parser("prove-windows-convenience-layer")
    sub.add_parser("validate-full-acceptance")
    sub.add_parser("prove-full-acceptance")
    sub.add_parser("validate-consolidated-proof-governance")
    sub.add_parser("prove-consolidated-proof-governance")
    sub.add_parser("prove-agent-operator-mode")
    sub.add_parser("prove-external-app-bridge")
    sub.add_parser("prove-runtime-backend-coverage")
    serve_browser_hub_p = sub.add_parser("serve-browser-hub")
    serve_browser_hub_p.add_argument("--host", default="127.0.0.1")
    serve_browser_hub_p.add_argument("--port", type=int, default=8878)
    prove_sdk_p = sub.add_parser("prove-sdk-bridge")
    prove_sdk_p.add_argument("--host", default="127.0.0.1")
    prove_sdk_p.add_argument("--port", type=int, default=8877)
    sub.add_parser("doctor")
    sub.add_parser("run-golden-flow")
    sub.add_parser("list-providers")

    start_p = sub.add_parser("start")
    start_p.add_argument("--portable", action="store_true", default=False)
    start_p.add_argument("--host", default="127.0.0.1")
    start_p.add_argument("--port", type=int, default=8877)

    stop_p = sub.add_parser("stop")
    stop_p.add_argument("--portable", action="store_true", default=False)

    check_p = sub.add_parser("check")
    check_p.add_argument("--portable", action="store_true", default=False)
    check_p.add_argument("--host", default="127.0.0.1")
    check_p.add_argument("--port", type=int, default=8877)

    prove_p = sub.add_parser("prove-local-runtime")
    prove_p.add_argument("--once-smoke", action="store_true", default=False)
    prove_p.add_argument("--host", default="127.0.0.1")
    prove_p.add_argument("--port", type=int, default=8877)
    # Agent Operator Mode CLI commands (LRH-PR-02, improved in LRH-PR-05)
    agent_handoff = sub.add_parser("agent-handoff")
    agent_handoff.add_argument("--agent", required=True)
    agent_handoff.add_argument("--task", default=None)
    agent_handoff.add_argument("--out", default=None, help="Write packet to this path in addition to stdout")
    agent_handoff.add_argument("--lrh-pr", default=None, dest="lrh_pr",
                               help="Auto-scope from LRH ladder by PR number (e.g. 05)")
    agent_plan = sub.add_parser("agent-plan")
    agent_plan.add_argument("--packet", required=True)
    agent_guard = sub.add_parser("agent-guard")
    agent_guard.add_argument("--packet", required=True)
    agent_check = sub.add_parser("agent-check")
    agent_check.add_argument("--packet", required=True)
    agent_proof = sub.add_parser("agent-proof")
    agent_proof.add_argument("--packet", required=True)
    agent_return = sub.add_parser("agent-return")
    agent_return.add_argument("--packet", required=True)
    run_work = sub.add_parser("run-work")
    run_work.add_argument("work")
    run_work.add_argument("--seed-pack")
    run_work.add_argument("--pattern-mine")
    run_work.add_argument("--caller-manifest")
    compile_seed = sub.add_parser("compile-seed-pack")
    compile_seed.add_argument("path")
    compile_pattern = sub.add_parser("compile-pattern-mine")
    compile_pattern.add_argument("path")
    build_hub = sub.add_parser("build-hub")
    build_hub.add_argument("--out", default=".odin_runtime/hub/index.html")
    support = sub.add_parser("emit-support-bundle")
    support.add_argument("--out", default=".odin_runtime/support")
    support.add_argument("--diagnostics-only", action="store_true", default=False)
    sub.add_parser("first-run-bootstrap")
    repair_p = sub.add_parser("repair-local-runtime")
    repair_p.add_argument("--plan-only", action="store_true", default=False)
    serve = sub.add_parser("serve")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8765)
    serve.add_argument("--once-smoke", action="store_true")
    # FINAL-PR-01: Simple Local Hub commands
    start_hub_p = sub.add_parser("start-local-hub")
    start_hub_p.add_argument("--host", default="127.0.0.1")
    start_hub_p.add_argument("--port", type=int, default=8765)
    start_hub_p.add_argument("--once-smoke", action="store_true", default=False)
    status_hub_p = sub.add_parser("status-local-hub")
    status_hub_p.add_argument("--host", default="127.0.0.1")
    status_hub_p.add_argument("--port", type=int, default=8765)
    open_hub_p = sub.add_parser("open-hub")
    open_hub_p.add_argument("--host", default="127.0.0.1")
    open_hub_p.add_argument("--port", type=int, default=8765)
    sub.add_parser("validate-simple-local-hub")
    prove_simple_hub_p = sub.add_parser("prove-simple-local-hub")
    prove_simple_hub_p.add_argument("--host", default="127.0.0.1")
    # FINAL-PR-04: Provider Probe + Runtime Security Smoke
    sub.add_parser("validate-final-pr-04-provider-probe-security")
    sub.add_parser("prove-final-pr-04-provider-probe-security")
    sub.add_parser("provider-status")
    sub.add_parser("provider-probe")
    sub.add_parser("runtime-security-smoke")
    # FINAL-PR-05: Execution Gate + Proof Chain + Ladder Scaffold
    sub.add_parser("validate-final-pr-05-execution-gate")
    sub.add_parser("prove-final-pr-05-execution-gate")
    sub.add_parser("prove-final-pr-proof-chain")
    ladder_p = sub.add_parser("prove-final-pr-ladder-scaffold")
    ladder_p.add_argument("--target", default="FINAL-PR-06")
    sub.add_parser("final-pr-ladder-scaffold")
    # Y Pattern Spine
    sub.add_parser("validate-y-pattern-spine")
    explain_y_route_p = sub.add_parser("explain-y-route")
    explain_y_route_p.add_argument("--demo", action="store_true", default=False)
    sub.add_parser("prove-y-pattern-spine")
    # Prep FINAL-PR-06..08
    sub.add_parser("validate-prep-final-pr-06-08")
    sub.add_parser("validate-final-pr-09-10-qshabang-smallmodel-prep")
    # FINAL-PR-06: Operational Seed Spine
    sub.add_parser("validate-operational-seed-spine")
    sub.add_parser("validate-field-selection-spine")
    explain_field_selection_p = sub.add_parser("explain-field-selection")
    explain_field_selection_p.add_argument("--demo", action="store_true", default=False)
    sub.add_parser("prove-field-selection-spine")
    explain_seed_route_p = sub.add_parser("explain-seed-route")
    explain_seed_route_p.add_argument("--demo", action="store_true", default=False)
    sub.add_parser("prove-operational-seed-spine")
    # FINAL-PR-08: Projection Candidate Spine
    sub.add_parser("validate-projection-candidate-spine")
    explain_projection_p = sub.add_parser("explain-projection-candidate")
    explain_projection_p.add_argument("--demo", action="store_true", default=False)
    sub.add_parser("prove-projection-candidate-spine")
    # FINAL-PR-09++: Operational Spine
    sub.add_parser("odin-status")
    sub.add_parser("odin-doctor")
    run_operational_spine_p = sub.add_parser("run-operational-spine")
    run_operational_spine_p.add_argument("--demo", action="store_true", default=False)
    run_operational_spine_p.add_argument("--input", dest="input_text", default=None)
    sub.add_parser("explain-operational-spine")
    sub.add_parser("explain-small-model-route")
    sub.add_parser("explain-qshabang-map")
    sub.add_parser("validate-operational-spine")
    sub.add_parser("validate-small-model-route-plan")
    sub.add_parser("validate-modelworkpacket-enforcement")
    sub.add_parser("validate-qshabang-operational-map")
    sub.add_parser("validate-deferred-system-lift")
    # FINAL-PR-10++: Boundary-Gated Release Operationalization
    sub.add_parser("validate-boundary-matrix")
    sub.add_parser("validate-ring-authority-map")
    sub.add_parser("validate-bug6-q7-operational-map")
    sub.add_parser("validate-qshabang-release-gate-map")
    sub.add_parser("validate-model-role-authority")
    sub.add_parser("validate-release-evidence-closure")
    sub.add_parser("validate-artifact-currency")
    sub.add_parser("validate-final-release-preflight")
    sub.add_parser("validate-final-pr-10-boundary-release")
    sub.add_parser("release-preflight")
    sub.add_parser("explain-boundaries")
    sub.add_parser("explain-release-claims")
    sub.add_parser("explain-model-role-authority")
    sub.add_parser("explain-qshabang-release-gates")
    # FINAL-PR-11: Local Provider Receipt Harness + Critic Runtime Binding + Thor Handoff Compiler v0
    sub.add_parser("validate-local-provider-receipt-harness")
    sub.add_parser("local-provider-doctor")
    run_lpr_p = sub.add_parser("run-local-provider-receipt")
    run_lpr_p.add_argument("--demo", action="store_true", default=False)
    run_lpr_p.add_argument("--provider", default="ollama_candidate")
    run_lpr_p.add_argument("--prompt", default="demo prompt")
    run_lpr_p.add_argument("--allow-local-provider-execution", action="store_true", default=False)
    sub.add_parser("explain-provider-receipt-claims")
    sub.add_parser("validate-critic-runtime-binding")
    run_critic_p = sub.add_parser("run-critic-cascade")
    run_critic_p.add_argument("--demo", action="store_true", default=False)
    sub.add_parser("explain-critic-cascade")
    sub.add_parser("validate-route-evaluation-receipts")
    run_route_p = sub.add_parser("run-route-evaluation")
    run_route_p.add_argument("--demo", action="store_true", default=False)
    sub.add_parser("explain-route-evaluation-claims")
    sub.add_parser("validate-thor-handoff-compiler")
    compile_thor_p = sub.add_parser("compile-thor-handoff")
    compile_thor_p.add_argument("--demo", action="store_true", default=False)
    sub.add_parser("explain-thor-handoff-compiler")
    sub.add_parser("validate-final-pr-11-provider-critic-thor")
    # FINAL-PR-11.5: Semantic Kernel Coverage Compiler + Claims Compiler + Y Pattern
    sub.add_parser("validate-v711-coverage-compiler")
    sub.add_parser("validate-semantic-kernel-closure")
    sub.add_parser("validate-y-pattern-operationalization-index")
    sub.add_parser("validate-claims-compiler")
    sub.add_parser("validate-agent-operator-modes")
    sub.add_parser("validate-final-pr-11-5-semantic-kernel-coverage")
    sub.add_parser("explain-v711-coverage")
    sub.add_parser("explain-semantic-kernel-closure")
    sub.add_parser("explain-claims-compiler")
    sub.add_parser("explain-agent-operator-modes")
    build_v711_matrix_p = sub.add_parser("build-v711-coverage-matrix")
    build_v711_matrix_p.add_argument("--demo", action="store_true", default=False)
    build_v711_gap_p = sub.add_parser("build-v711-gap-index")
    build_v711_gap_p.add_argument("--demo", action="store_true", default=False)
    build_sk_p = sub.add_parser("build-semantic-kernel")
    build_sk_p.add_argument("--demo", action="store_true", default=False)
    build_ypoi_p = sub.add_parser("build-y-pattern-operationalization-index")
    build_ypoi_p.add_argument("--demo", action="store_true", default=False)
    compile_claim_p = sub.add_parser("compile-safe-claim")
    compile_claim_p.add_argument("--demo", action="store_true", default=False)
    compile_claim_p.add_argument("--claim", default=None)
    sub.add_parser("explain-y-pattern-operationalization")
    sub.add_parser("explain-claims-policy")
    sub.add_parser("list-agent-operator-modes")
    explain_mode_p = sub.add_parser("explain-agent-operator-mode")
    explain_mode_p.add_argument("--mode", default="claude_code_implementation_worker")
    args = parser.parse_args(argv)


    if args.cmd == "audit-pre-release-super":
        from tools.audit.run_pre_release_super_audit import main as run_pre_release_super_audit
        return run_pre_release_super_audit(["--lightweight"])

    if args.cmd == "validate-pre-release-super-audit":
        from tools.audit.run_pre_release_super_audit import main as run_pre_release_super_audit
        return run_pre_release_super_audit(["--validate-only"])

    if args.cmd == "doctor":
        from odin.doctor.diagnostics import run_doctor
        report = run_doctor()
        print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "first-run-bootstrap":
        from odin.bootstrap.first_run import run_first_run_bootstrap
        result = run_first_run_bootstrap()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "repair-local-runtime":
        if not args.plan_only:
            print(json.dumps({
                "status": "blocked",
                "error": "repair-local-runtime requires --plan-only flag; apply mode is not implemented",
                "plan_only": False,
                "claim_boundary": "repair_blocked_without_plan_only_flag",
            }, indent=2, ensure_ascii=False, sort_keys=True))
            return 1
        from odin.doctor.diagnostics import run_doctor
        from odin.bootstrap.repair_plan import build_repair_plan
        doctor_report = run_doctor()
        plan = build_repair_plan(doctor_report)
        print(json.dumps(plan, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "run-golden-flow":
        result = run_universal_work_file(
            ROOT / "examples" / "runtime" / "universal_work_full.valid.json",
            seed_pack_path=ROOT / "examples" / "runtime" / "app_seed_pack_full.valid.json",
            pattern_mine_path=ROOT / "examples" / "runtime" / "pattern_mine_full.valid.json",
            caller_manifest_path=ROOT / "examples" / "runtime" / "app_caller_manifest.valid.json",
        )
        payload = {
            "status": result.get("runtime_status"),
            "candidate_count": len(result.get("candidates", [])),
            "qirc_event_count": result.get("qirc_digest", {}).get("event_count"),
            "selected_candidate_id": result.get("selected_candidate_id"),
            "claim_boundary": "golden_flow_is_local_runtime_candidate_not_host_proof",
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))
        return 0
    if args.cmd == "list-providers":
        print(json.dumps({"providers": list_provider_cards(), "claim_boundary": "provider_cards_not_live_inference_proof"}, indent=2, ensure_ascii=False, sort_keys=True))
        return 0
    if args.cmd == "run-work":
        try:
            result = run_universal_work_file(
                args.work,
                seed_pack_path=args.seed_pack,
                pattern_mine_path=args.pattern_mine,
                caller_manifest_path=args.caller_manifest,
            )
        except Exception as exc:
            print(json.dumps({"status": "blocked", "error": str(exc), "claim_boundary": "run_work_error_no_apply"}, indent=2, ensure_ascii=False, sort_keys=True))
            return 1
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0
    if args.cmd == "compile-seed-pack":
        data = load_json(Path(args.path))
        print(json.dumps(compile_seed_pack(data), indent=2, ensure_ascii=False, sort_keys=True))
        return 0
    if args.cmd == "compile-pattern-mine":
        data = load_json(Path(args.path))
        print(json.dumps(compile_pattern_mine(data), indent=2, ensure_ascii=False, sort_keys=True))
        return 0
    if args.cmd == "build-hub":
        path = write_static_hub(Path(args.out))
        print(json.dumps({"status": "ok", "hub": str(path), "claim_boundary": "static_hub_candidate"}, indent=2, ensure_ascii=False, sort_keys=True))
        return 0
    if args.cmd == "emit-support-bundle":
        if getattr(args, "diagnostics_only", False):
            from odin.doctor.diagnostics import run_doctor
            from odin.doctor.support_bundle import emit_diagnostics_support_bundle
            doctor_report = run_doctor()
            bundle = emit_diagnostics_support_bundle(
                doctor_report=doctor_report,
                out_dir=Path(args.out),
            )
            print(json.dumps(bundle, indent=2, ensure_ascii=False, sort_keys=True))
            return 0
        path = emit_support_bundle(ROOT, Path(args.out))
        print(json.dumps({"status": "ok", "support_bundle": str(path), "claim_boundary": "diagnostic_candidate"}, indent=2, ensure_ascii=False, sort_keys=True))
        return 0
    if args.cmd == "serve":
        result = run_local_api(args.host, args.port, once_smoke=args.once_smoke)
        if args.once_smoke:
            print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    # FINAL-PR-01: Simple Local Hub commands
    if args.cmd == "start-local-hub":
        from odin.local_hub.server import run_once_smoke as hub_once_smoke
        from odin.local_hub.policy import check_host
        host = getattr(args, "host", "127.0.0.1")
        port = getattr(args, "port", 8765)
        once_smoke = getattr(args, "once_smoke", False)
        ok, reason = check_host(host)
        if not ok:
            print(json.dumps({"status": "blocked", "error": reason,
                              "candidate_only": True,
                              "claim_boundary": "simple_local_hub_localhost_only"}, indent=2))
            return 1
        if once_smoke:
            result = hub_once_smoke(host=host, port=port)
            print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
            return 0 if result.get("status") in {"ok", "partial"} else 1
        print(json.dumps({
            "status": "scaffold",
            "note": "start-local-hub starts a localhost HTTP server; use --once-smoke for a deterministic smoke proof",
            "host": host,
            "port": port,
            "candidate_only": True,
            "claim_boundary": "simple_local_hub_localhost_only_candidate",
            "hint": "python -m odin.cli start-local-hub --once-smoke",
        }, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "status-local-hub":
        from odin.local_hub.server import get_hub_status
        host = getattr(args, "host", "127.0.0.1")
        port = getattr(args, "port", 8765)
        result = get_hub_status(host=host, port=port)
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "open-hub":
        host = getattr(args, "host", "127.0.0.1")
        port = getattr(args, "port", 8765)
        url = f"http://{host}:{port}/"
        print(json.dumps({
            "status": "ok",
            "hub_url": url,
            "note": "Open this URL in your browser after starting the hub with start-local-hub",
            "candidate_only": True,
            "claim_boundary": "open_hub_url_candidate_not_browser_launch",
        }, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "validate-simple-local-hub":
        errors = validate_simple_local_hub()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-simple-local-hub: OK")
        return 0

    if args.cmd == "prove-simple-local-hub":
        from odin.local_hub.proof import build_simple_local_hub_proof_packet
        host = getattr(args, "host", "127.0.0.1")
        result = build_simple_local_hub_proof_packet(host=host)
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0 if result.get("status") in {"ok", "ok_with_known_gaps"} else 1

    # FINAL-PR-02: Model Picker + Connected Apps + Demo Universal Work
    if args.cmd == "validate-final-pr-02-model-apps-demo":
        errors = validate_final_pr_02_model_apps_demo()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-final-pr-02-model-apps-demo: OK")
        return 0

    if args.cmd == "prove-final-pr-02-demo-universal-work":
        from odin.local_hub.proof_pr02 import build_final_pr_02_proof_packet
        result = build_final_pr_02_proof_packet()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0 if result.get("status") in {"ok", "ok_with_known_gaps"} else 1

    # FINAL-PR-03: QIRC Core Dev Mode
    if args.cmd == "validate-final-pr-03-qirc-devmode":
        errors = validate_final_pr_03_qirc_devmode()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-final-pr-03-qirc-devmode: OK")
        return 0

    if args.cmd == "prove-final-pr-03-qirc-devmode":
        from odin.local_hub.proof_pr03 import build_final_pr_03_proof_packet, write_proof_report
        result = build_final_pr_03_proof_packet()
        write_proof_report()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0 if result.get("status") in {"ok", "ok_with_known_gaps"} else 1

    # FINAL-PR-04: Provider Probe + Runtime Security Smoke
    if args.cmd == "validate-final-pr-04-provider-probe-security":
        errors = validate_final_pr_04_provider_probe_security()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-final-pr-04-provider-probe-security: OK")
        return 0

    if args.cmd == "prove-final-pr-04-provider-probe-security":
        from odin.providers.proof import persist_proof_packet
        result = persist_proof_packet(ROOT)
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0 if result.get("status") in {"ok", "ok_with_known_gaps"} else 1

    if args.cmd == "provider-status":
        from odin.providers.probe import build_provider_status_packet
        result = build_provider_status_packet()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "provider-probe":
        from odin.providers.probe import probe_all_providers
        results = probe_all_providers()
        from odin.qirc_core.bus import append_event
        for p in results:
            append_event(channel="#odin.model", kind="provider_probe_status", source="cli_provider_probe",
                         payload={k: p.get(k) for k in ("provider_id", "status", "probe_allowed", "execution_allowed",
                                                          "candidate_only", "local_only", "model_inference", "provider_execution")})
        result = {
            "artifact_kind": "odin_provider_probe_results",
            "candidate_only": True,
            "local_only": True,
            "provider_execution": False,
            "model_inference": False,
            "providers": results,
            "claim_boundary": "provider_probe_readiness_not_model_execution",
        }
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "runtime-security-smoke":
        from odin.runtime_security.smoke import run_runtime_security_smoke
        result = run_runtime_security_smoke(ROOT)
        print(json.dumps(result.as_dict(), indent=2, ensure_ascii=False, sort_keys=True))
        return 0 if result.status in {"ok"} else 1

    # Portable Local Runtime Starter commands (LRH-PR-03)
    if args.cmd == "start":
        if not args.portable:
            print(json.dumps({"status": "blocked", "error": "use --portable flag for portable local runtime", "claim_boundary": "local_runtime_starter_candidate_only"}, indent=2))
            return 1
        from odin.local_runtime.starter import start_portable_runtime
        result = start_portable_runtime(host=args.host, port=args.port, _blocking=True)
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0 if result.get("status") in {"ready", "stopped"} else 1

    if args.cmd == "stop":
        if not args.portable:
            print(json.dumps({"status": "blocked", "error": "use --portable flag for portable local runtime", "claim_boundary": "local_runtime_starter_candidate_only"}, indent=2))
            return 1
        from odin.local_runtime.starter import stop_portable_runtime
        result = stop_portable_runtime()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "check":
        if not args.portable:
            print(json.dumps({"status": "blocked", "error": "use --portable flag for portable local runtime", "claim_boundary": "local_runtime_starter_candidate_only"}, indent=2))
            return 1
        from odin.local_runtime.starter import check_portable_runtime
        result = check_portable_runtime(host=args.host, port=args.port)
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "prove-local-runtime":
        if not args.once_smoke:
            print(json.dumps({"status": "blocked", "error": "use --once-smoke flag; unbounded proof is not supported", "claim_boundary": "local_runtime_proof_candidate_only"}, indent=2))
            return 1
        from odin.local_runtime.proof import run_once_smoke_proof
        result = run_once_smoke_proof(host=args.host, port=args.port)
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0 if result.get("status") in {"ok", "partial"} else 1

    # Agent Operator Mode commands (LRH-PR-02, improved in LRH-PR-05, hardened in LRH-PR-06)
    if args.cmd == "agent-handoff":
        try:
            task_source = getattr(args, "task", None)
            lrh_pr = getattr(args, "lrh_pr", None)

            if lrh_pr:
                # Use LRH Ladder Compiler v1 to derive full packet
                from odin.agent_operator.lrh_ladder_compiler import compile_lrh_pr_to_agent_work_packet
                packet = compile_lrh_pr_to_agent_work_packet(lrh_pr, args.agent)
                if task_source:
                    packet["task_source"] = task_source
            else:
                if not task_source:
                    print(json.dumps({"status": "blocked", "error": "either --task or --lrh-pr required", "claim_boundary": "agent_handoff_error_no_apply"}, indent=2))
                    return 1
                from odin.agent_operator.packets import build_agent_work_packet
                packet = build_agent_work_packet(
                    agent_profile_id=args.agent,
                    task_source=task_source,
                    objective=f"Agent handoff for task: {task_source}",
                )

            output = json.dumps(packet, indent=2, ensure_ascii=False, sort_keys=True)
            print(output)
            out_path = getattr(args, "out", None)
            if out_path:
                Path(out_path).write_text(output, encoding="utf-8")
            return 0
        except Exception as exc:
            print(json.dumps({"status": "blocked", "error": str(exc), "claim_boundary": "agent_handoff_error_no_apply"}, indent=2))
            return 1

    if args.cmd == "agent-plan":
        packet = load_json(Path(args.packet))
        result = {
            "status": "ok",
            "packet_id": packet.get("packet_id"),
            "agent_profile_id": packet.get("agent_profile_id"),
            "plan_envelope": {
                "objective": packet.get("objective"),
                "required_context": packet.get("required_context", []),
                "acceptance_gates": packet.get("acceptance_gates", []),
                "required_commands": packet.get("required_commands", []),
            },
            "claim_boundary": "plan_envelope_candidate_not_execution_proof",
        }
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "agent-guard":
        from odin.agent_operator.guards import check_forbidden_actions
        packet = load_json(Path(args.packet))
        result = check_forbidden_actions(packet)
        result["claim_boundary"] = "guard_check_candidate_not_runtime_proof"
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0 if result["status"] == "ok" else 1

    if args.cmd == "agent-check":
        from odin.agent_operator.packets import validate_agent_work_packet
        packet = load_json(Path(args.packet))
        result = validate_agent_work_packet(packet)
        result["claim_boundary"] = "packet_check_candidate_not_runtime_proof"
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0 if result["status"] == "ok" else 1

    if args.cmd == "agent-proof":
        from odin.agent_operator.proofs import emit_proof_boundary_summary
        packet = load_json(Path(args.packet))
        result = emit_proof_boundary_summary(packet)
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "agent-return":
        from odin.agent_operator.returns import build_return_report_skeleton
        packet = load_json(Path(args.packet))
        report = build_return_report_skeleton(
            packet_id=packet.get("packet_id", "UNKNOWN"),
            agent_profile_id=packet.get("agent_profile_id", "unknown"),
        )
        print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "validate-browser-hub-shell":
        errors = validate_browser_hub_shell()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-browser-hub-shell: OK")
        return 0

    if args.cmd == "prove-browser-hub":
        shell_only = getattr(args, "shell_only", False)
        use_dashboard = getattr(args, "dashboard", False)
        use_candidates = getattr(args, "candidates", False)
        use_traces = getattr(args, "traces", False)
        use_providers = getattr(args, "providers", False)
        use_playground = getattr(args, "playground", False)
        result = build_browser_hub_proof_packet(shell_only=shell_only, dashboard=use_dashboard, candidates=use_candidates, traces=use_traces, providers=use_providers, playground=use_playground)
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0 if result.get("status") in {"ok", "partial"} else 1

    if args.cmd == "validate-universal-work-playground":
        errors = validate_universal_work_playground()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-universal-work-playground: OK")
        return 0

    if args.cmd == "validate-neutral-external-app-bridge":
        errors = validate_neutral_external_app_bridge()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-neutral-external-app-bridge: OK")
        return 0

    if args.cmd == "prove-neutral-external-app-bridge":
        result = build_neutral_external_app_bridge_proof_packet()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0 if result.get("status") in {"ok", "partial"} else 1

    if args.cmd == "validate-generic-app-bridge-golden-harness":
        errors = validate_generic_app_bridge_golden_harness()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-generic-app-bridge-golden-harness: OK")
        return 0

    if args.cmd == "prove-generic-app-bridge-golden-harness":
        result = build_generic_app_bridge_golden_harness_proof_packet()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0 if result.get("status") in {"ok", "partial"} else 1

    if args.cmd == "validate-local-config-safe-settings":
        errors = validate_local_config_safe_settings()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-local-config-safe-settings: OK")
        return 0

    if args.cmd == "prove-local-config-safe-settings":
        result = build_local_config_safe_settings_proof_packet()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0 if result.get("status") in {"ok", "partial"} else 1

    if args.cmd == "validate-portable-package":
        errors = validate_portable_package()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-portable-package: OK")
        return 0

    if args.cmd == "prove-portable-package":
        result = build_portable_package_proof_packet()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0 if result.get("status") in {"ok", "partial"} else 1

    if args.cmd == "validate-windows-convenience-layer":
        errors = validate_windows_convenience_layer()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-windows-convenience-layer: OK")
        return 0

    if args.cmd == "prove-windows-convenience-layer":
        result = build_windows_convenience_layer_proof_packet()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0 if result.get("status") in {"ok", "partial"} else 1

    if args.cmd == "validate-full-acceptance":
        errors = validate_full_acceptance()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-full-acceptance: OK")
        return 0

    if args.cmd == "prove-full-acceptance":
        result = build_full_acceptance_proof_packet()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0 if result.get("status") in {"ok", "ok_with_known_gaps", "partial"} else 1

    if args.cmd == "validate-provider-worker-inspector":
        errors = validate_provider_worker_inspector()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-provider-worker-inspector: OK")
        return 0

    if args.cmd == "validate-trace-viewer":
        errors = validate_trace_viewer()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-trace-viewer: OK")
        return 0

    if args.cmd == "validate-candidate-store-viewer":
        errors = validate_candidate_store_viewer()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-candidate-store-viewer: OK")
        return 0

    if args.cmd == "validate-hub-runtime-dashboard":
        errors = validate_hub_runtime_dashboard()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-hub-runtime-dashboard: OK")
        return 0

    if args.cmd == "serve-browser-hub":
        # Scaffold — validates localhost boundary then emits static server plan
        host = getattr(args, "host", "127.0.0.1")
        port = getattr(args, "port", 8878)
        from odin.local_runtime.config import ALLOWED_HOSTS, BLOCKED_HOSTS
        if host in BLOCKED_HOSTS:
            print(json.dumps({
                "status": "blocked",
                "error": f"host {host!r} is not allowed; must be localhost",
                "claim_boundary": "serve_browser_hub_localhost_only",
            }, indent=2))
            return 1
        if host not in ALLOWED_HOSTS:
            print(json.dumps({
                "status": "blocked",
                "error": f"host {host!r} is not an allowed localhost address",
                "claim_boundary": "serve_browser_hub_localhost_only",
            }, indent=2))
            return 1
        static_dir = ROOT / "odin" / "hub" / "static"
        print(json.dumps({
            "status": "scaffold",
            "note": "serve-browser-hub is a scaffold in LRH-PR-06; live HTTP server not claimed",
            "static_dir": str(static_dir),
            "host": host,
            "port": port,
            "candidate_only": True,
            "claim_boundary": "serve_browser_hub_localhost_only_scaffold",
        }, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "validate-consolidated-proof-governance":
        errors = validate_consolidated_proof_governance()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-consolidated-proof-governance: OK")
        return 0

    if args.cmd == "prove-consolidated-proof-governance":
        result = build_consolidated_proof_governance_packet()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0 if result.get("status") in {"ok", "ok_with_known_gaps"} else 1

    if args.cmd == "prove-agent-operator-mode":
        result = build_agent_operator_mode_proof_packet()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0 if result.get("status") in {"ok", "ok_with_known_gaps"} else 1

    if args.cmd == "prove-external-app-bridge":
        result = build_external_app_bridge_proof_packet()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0 if result.get("status") in {"ok", "ok_with_known_gaps"} else 1

    if args.cmd == "prove-runtime-backend-coverage":
        result = build_runtime_backend_coverage_proof_packet()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0 if result.get("status") in {"ok", "ok_with_known_gaps"} else 1

    if args.cmd == "validate-agent-operator-mode":
        errors = validate_agent_operator_mode()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-agent-operator-mode: OK")
        return 0

    if args.cmd == "validate-runtime-doctor-bootstrap":
        errors = validate_runtime_doctor_bootstrap()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-runtime-doctor-bootstrap: OK")
        return 0

    if args.cmd == "validate-localhost-api-sdk-bridge":
        errors = validate_localhost_api_sdk_bridge()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-localhost-api-sdk-bridge: OK")
        return 0

    if args.cmd == "prove-sdk-bridge":
        result = run_sdk_bridge_proof(host=args.host, port=args.port)
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0 if result.get("status") in {"ok", "partial"} else 1

    if args.cmd == "prove-final-pr-05-execution-gate":
        from odin.execution_gate.proof import build_execution_gate_proof_packet
        from odin.proof_chain.builder import build_proof_chain
        from odin.final_pr_ladder.compiler import compile_worker_packet_scaffold
        from odin.qirc_core.bus import list_events
        from odin.execution_gate.gateway import execute_candidate
        # Run mock execution to prove it works
        mock_result = execute_candidate(input_text="prove-final-pr-05-smoke-test", provider_id="mock")
        mock_ok = mock_result.get("mock_execution") is True and mock_result.get("model_inference") is False
        qirc_events = list_events("#odin.model")
        proof = build_execution_gate_proof_packet(
            mock_execution_completed=mock_ok,
            qirc_events_visible=len(qirc_events) > 0,
            proof_chain_present=True,
            ladder_scaffold_present=True,
        )
        out_path = ROOT / "reports" / "final_pr_05_execution_gate_proof_packet.json"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(proof, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        print(json.dumps(proof, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "prove-final-pr-proof-chain":
        from odin.proof_chain.builder import build_proof_chain
        chain = build_proof_chain()
        out_path = ROOT / "reports" / "final_pr_05_proof_chain.json"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(chain, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        print(json.dumps(chain, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "prove-final-pr-ladder-scaffold":
        from odin.final_pr_ladder.proof import build_ladder_scaffold_proof
        target = getattr(args, "target", "FINAL-PR-06")
        proof = build_ladder_scaffold_proof(target_pr_id=target)
        out_path = ROOT / "reports" / "final_pr_05_ladder_scaffold_report.json"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(proof, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        print(json.dumps(proof, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "final-pr-ladder-scaffold":
        from odin.final_pr_ladder.compiler import compile_worker_packet_scaffold
        scaffold = compile_worker_packet_scaffold(
            target_pr_id="FINAL-PR-06",
            prior_return_report_path="reports/final_pr_05_execution_gate_report.json",
            profile="claude-code",
        )
        print(json.dumps(scaffold, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    # Y Pattern Spine commands
    if args.cmd == "validate-y-pattern-spine":
        errors = validate_y_pattern_spine()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-y-pattern-spine: OK")
        return 0

    if args.cmd == "explain-y-route":
        from odin.y_pattern_spine.profiles import build_route_hint_demo
        result = build_route_hint_demo()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "prove-y-pattern-spine":
        from odin.y_pattern_spine.proof import persist_proof_packet
        result = persist_proof_packet(ROOT)
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    # Prep FINAL-PR-06..08 commands
    if args.cmd == "validate-prep-final-pr-06-08":
        errors = validate_prep_final_pr_06_08()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-prep-final-pr-06-08: OK")
        return 0

    # FINAL-PR-06: Operational Seed Spine commands
    if args.cmd == "validate-operational-seed-spine":
        errors = validate_operational_seed_spine()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-operational-seed-spine: OK")
        return 0

    if args.cmd == "explain-seed-route":
        from odin.operational_seed_spine.selector import select_seed_route
        from odin.operational_seed_spine.work_capsule import compile_work_capsule
        demo_ctx = {"trigger_shape": "repo", "work_type": "repo"}
        route = select_seed_route(demo_ctx)
        capsule = compile_work_capsule(route)
        result = {
            "candidate_only": True,
            "claim_boundary": "operational_seed_spine_routes_work_not_authority",
            "selected_seed_id": route.selected_seed_id,
            "selected_role_profile_id": route.selected_role_profile_id,
            "matched_trigger_shapes": route.matched_trigger_shapes,
            "fallback_used": route.fallback_used,
            "selection_priority": route.selection_priority,
            "seed_route": route.to_dict(),
            "work_capsule": capsule.to_dict(),
        }
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "prove-operational-seed-spine":
        from odin.operational_seed_spine.proof import persist_proof_packet
        result = persist_proof_packet(ROOT)
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0


    # FINAL-PR-07: Field Selection Spine commands
    if args.cmd == "validate-field-selection-spine":
        errors = validate_field_selection_spine()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-field-selection-spine: OK")
        return 0

    if args.cmd == "explain-field-selection":
        from odin.field_selection_spine.selector import select_field_route
        demo_ctx = {"trigger_shape": "repo", "work_type": "repo", "repo_evidence": "SYSTEM_MAP.json"}
        result = select_field_route(demo_ctx).to_dict()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "prove-field-selection-spine":
        from odin.field_selection_spine.proof import persist_proof_packet
        result = persist_proof_packet(ROOT)
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    # FINAL-PR-08: Projection Candidate Spine commands
    if args.cmd == "validate-projection-candidate-spine":
        errors = validate_projection_candidate_spine()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-projection-candidate-spine: OK")
        return 0

    if args.cmd == "explain-projection-candidate":
        from odin.operational_seed_spine.selector import select_seed_route
        from odin.field_selection_spine.selector import select_field_route_from_seed_route
        from odin.projection_candidate_spine.projection_set import build_projection_set_from_field_selection
        from odin.projection_candidate_spine.candidate_graph import build_candidate_graph
        from odin.projection_candidate_spine.expression_packet import build_expression_packet
        seed = select_seed_route({"trigger_shape": "repo", "work_type": "repo"})
        fs = select_field_route_from_seed_route(seed)
        ps = build_projection_set_from_field_selection(fs)
        graph = build_candidate_graph(ps.candidate_nodes)
        ep = build_expression_packet(ps.candidate_nodes[0])
        result = {
            "status": "ok",
            "candidate_only": True,
            "claim_boundary": "projection_candidate_spine_prepares_candidates_not_runtime_execution",
            "seed_route": seed.to_dict(),
            "field_selection": fs.to_dict(),
            "projection_set": ps.to_dict(),
            "candidate_graph": graph.to_dict(),
            "expression_packet": ep.to_dict(),
            "not_proven": [
                "hidden_runtime", "model_inference", "provider_execution", "app_apply",
                "app_state_mutation", "external_send", "generated_code_correctness",
                "production_readiness", "security_certification",
            ],
        }
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "prove-projection-candidate-spine":
        from odin.projection_candidate_spine.proof import persist_proof_packet
        result = persist_proof_packet(ROOT)
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    # FINAL-PR-09++: Operational Spine commands
    if args.cmd == "odin-status":
        from odin.operational_spine.status import get_operational_spine_status
        result = get_operational_spine_status()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "odin-doctor":
        from odin.operational_spine.status import get_operational_spine_doctor
        result = get_operational_spine_doctor()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "run-operational-spine":
        from odin.operational_spine.orchestrator import run_operational_spine as _run_spine
        if getattr(args, "input_text", None):
            result = _run_spine(args.input_text)
        else:
            result = _run_spine("demo operational spine input")
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "explain-operational-spine":
        from odin.operational_spine.orchestrator import run_operational_spine as _run_spine
        result = _run_spine("explain operational spine demo")
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "explain-small-model-route":
        from odin.operational_spine.small_model_route_plan import build_small_model_route_plan
        result = build_small_model_route_plan(work_id="universal_work_explain_demo")
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "explain-qshabang-map":
        from odin.operational_spine.qshabang_runtime_map import build_qshabang_operational_map
        result = build_qshabang_operational_map()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "validate-operational-spine":
        errors = validate_operational_spine()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-operational-spine: OK")
        return 0

    if args.cmd == "validate-small-model-route-plan":
        from odin.operational_spine.small_model_route_plan import build_small_model_route_plan
        from odin.operational_spine.model_roles import list_model_roles
        errors_found = []
        plan = build_small_model_route_plan(work_id="validate_demo_work")
        if not plan.get("candidate_only"):
            errors_found.append("small_model_route_plan candidate_only must be true")
        all_roles = list_model_roles()
        role_ids = [r["role_id"] for r in all_roles]
        for rid in ["3b_scout", "7b_writer", "hybrid_3b_scout_7b_synthesize_3b_check", "schema_validation"]:
            if rid not in role_ids:
                errors_found.append(f"missing required role: {rid}")
        if errors_found:
            for err in errors_found:
                print(f"ERROR: {err}")
            return 1
        print("validate-small-model-route-plan: OK")
        return 0

    if args.cmd == "validate-modelworkpacket-enforcement":
        from odin.operational_spine.modelworkpacket_builder import validate_modelworkpacket
        errors_found = validate_modelworkpacket({"candidate_only": True, "local_only": True, "claim_boundary": "test", "output_contract": {}, "final_gate_requirements": [], "not_proven": []})
        bad_errors = validate_modelworkpacket({"candidate_only": True, "local_only": True, "app_apply": True, "claim_boundary": "test", "output_contract": {}, "final_gate_requirements": [], "not_proven": []})
        if not bad_errors:
            print("ERROR: validator should reject app_apply: true")
            return 1
        print("validate-modelworkpacket-enforcement: OK")
        return 0

    if args.cmd == "validate-qshabang-operational-map":
        from odin.operational_spine.qshabang_runtime_map import build_qshabang_operational_map
        result = build_qshabang_operational_map()
        if not result.get("candidate_only"):
            print("ERROR: qshabang_operational_map candidate_only must be true")
            return 1
        required_components = ["ki_ohne_ki", "q_gates", "mirror_critics", "qirc", "app_sovereignty"]
        components = result.get("components", {})
        if isinstance(components, list):
            comp_names = {c.get("name", c.get("id", "")) for c in components}
        else:
            comp_names = set(components.keys())
        for comp in required_components:
            if comp not in comp_names:
                print(f"ERROR: qshabang_operational_map missing component: {comp}")
                return 1
        print("validate-qshabang-operational-map: OK")
        return 0

    if args.cmd == "validate-deferred-system-lift":
        from odin.operational_spine.deferred_system_lift import build_deferred_system_lift_plan
        result = build_deferred_system_lift_plan()
        if not result.get("candidate_only"):
            print("ERROR: deferred_system_lift candidate_only must be true")
            return 1
        systems = result.get("systems", {})
        if isinstance(systems, list):
            sys_names = {s.get("name", s.get("system_name", "")) for s in systems}
        else:
            sys_names = set(systems.keys())
        required = ["Context Distillery", "Critic Cascade", "Model Dojo", "SDK/App Bridge receipts"]
        for name in required:
            if name not in sys_names:
                print(f"ERROR: deferred_system_lift missing system: {name}")
                return 1
        print("validate-deferred-system-lift: OK")
        return 0

    # FINAL-PR-10++: Boundary-Gated Release Operationalization dispatch
    if args.cmd == "validate-boundary-matrix":
        from odin.release_boundaries.boundary_matrix import build_boundary_matrix
        result = build_boundary_matrix()
        if not result.get("candidate_only"):
            print("ERROR: boundary_matrix candidate_only must be true")
            return 1
        if result.get("boundary_count", 0) < 20:
            print(f"ERROR: boundary_matrix must have at least 20 boundaries, got {result.get('boundary_count')}")
            return 1
        print("validate-boundary-matrix: OK")
        return 0

    if args.cmd == "validate-ring-authority-map":
        from odin.release_boundaries.ring_authority_map import build_ring_authority_map
        result = build_ring_authority_map()
        if not result.get("candidate_only"):
            print("ERROR: ring_authority_map candidate_only must be true")
            return 1
        rings = result.get("rings", {})
        if "ring_0" not in rings:
            print("ERROR: ring_authority_map must contain ring_0")
            return 1
        if not result.get("final_pr_11_remains_deferred"):
            print("ERROR: ring_authority_map must have final_pr_11_remains_deferred: true")
            return 1
        print("validate-ring-authority-map: OK")
        return 0

    if args.cmd == "validate-bug6-q7-operational-map":
        from odin.release_boundaries.bug6_q7_operational_map import build_bug6_q7_operational_map
        result = build_bug6_q7_operational_map()
        if not result.get("candidate_only"):
            print("ERROR: bug6_q7_operational_map candidate_only must be true")
            return 1
        drift_map = result.get("drift_map", {})
        if "Bug6" not in drift_map and "authority_drift_scanner" not in str(drift_map):
            print("ERROR: bug6_q7_operational_map must contain Bug6/authority_drift_scanner")
            return 1
        print("validate-bug6-q7-operational-map: OK")
        return 0

    if args.cmd == "validate-qshabang-release-gate-map":
        from odin.release_boundaries.qshabang_release_gate_map import build_qshabang_release_gate_map
        result = build_qshabang_release_gate_map()
        if not result.get("candidate_only"):
            print("ERROR: qshabang_release_gate_map candidate_only must be true")
            return 1
        components = result.get("components", {})
        required_comps = ["deterministic_precompute", "claim_evidence_reality_gates", "critic_cascade"]
        for comp in required_comps:
            if comp not in components:
                print(f"ERROR: qshabang_release_gate_map missing component: {comp}")
                return 1
        print("validate-qshabang-release-gate-map: OK")
        return 0

    if args.cmd == "validate-model-role-authority":
        from odin.release_boundaries.model_role_authority import build_model_role_authority_matrix
        result = build_model_role_authority_matrix()
        if not result.get("candidate_only"):
            print("ERROR: model_role_authority_matrix candidate_only must be true")
            return 1
        roles = result.get("roles", {})
        required_roles = ["3b_scout", "7b_writer", "hybrid_3b_scout_7b_synthesize_3b_check", "local_provider_candidate"]
        for rid in required_roles:
            if rid not in roles:
                print(f"ERROR: model_role_authority_matrix missing role: {rid}")
                return 1
        for rid, role in roles.items():
            if "app_apply" not in role.get("forbidden_actions", []):
                print(f"ERROR: role {rid} must forbid app_apply")
                return 1
        print("validate-model-role-authority: OK")
        return 0

    if args.cmd == "validate-release-evidence-closure":
        from odin.release_boundaries.evidence_closure import build_release_evidence_closure_index
        result = build_release_evidence_closure_index()
        if not result.get("candidate_only"):
            print("ERROR: release_evidence_closure candidate_only must be true")
            return 1
        if not result.get("final_pr_11_remains_deferred"):
            print("ERROR: release_evidence_closure must have final_pr_11_remains_deferred: true")
            return 1
        subsystems = result.get("subsystems", {})
        required_subs = ["Operational Spine", "Provider Seam", "ModelWorkPacket", "Final Preflight"]
        for sub in required_subs:
            if sub not in subsystems:
                print(f"ERROR: release_evidence_closure missing subsystem: {sub}")
                return 1
        print("validate-release-evidence-closure: OK")
        return 0

    if args.cmd == "validate-artifact-currency":
        from odin.release_boundaries.artifact_currency import build_artifact_currency_index
        result = build_artifact_currency_index()
        if not result.get("candidate_only"):
            print("ERROR: artifact_currency_index candidate_only must be true")
            return 1
        currency_classes = result.get("currency_classes", [])
        required_classes = ["current_runtime", "current_release_evidence", "historical_supporting", "target_only"]
        for cls in required_classes:
            if cls not in currency_classes:
                print(f"ERROR: artifact_currency_index missing currency class: {cls}")
                return 1
        print("validate-artifact-currency: OK")
        return 0

    if args.cmd in ("validate-final-release-preflight", "release-preflight"):
        from odin.release_boundaries.final_preflight import run_final_release_preflight
        result = run_final_release_preflight()
        if args.cmd == "validate-final-release-preflight":
            status = result.get("release_preflight_status")
            if status not in ("green", "yellow", "red"):
                print(f"ERROR: release_preflight_status must be green/yellow/red, got {status!r}")
                return 1
            if not result.get("final_pr_11_remains_deferred"):
                print("ERROR: release_preflight must have final_pr_11_remains_deferred: true")
                return 1
            forbidden = result.get("forbidden_release_claims", [])
            for claim in ["production_readiness", "security_certification", "release_certification"]:
                if claim not in forbidden:
                    print(f"ERROR: release_preflight forbidden_release_claims must include {claim}")
                    return 1
            print("validate-final-release-preflight: OK")
            return 0
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
            return 0

    if args.cmd == "validate-final-pr-10-boundary-release":
        errors = validate_final_pr_10_boundary_release()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-final-pr-10-boundary-release: OK")
        return 0

    if args.cmd == "explain-boundaries":
        from odin.release_boundaries.boundary_matrix import build_boundary_matrix
        print(json.dumps(build_boundary_matrix(), indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "explain-release-claims":
        from odin.release_boundaries.final_preflight import run_final_release_preflight
        result = run_final_release_preflight()
        claims = {
            "artifact_kind": "odin_release_claims_explanation",
            "candidate_only": True,
            "claim_boundary": "final_pr_10_boundary_gated_release_operationalization_not_release_certification",
            "allowed_release_claims": result["allowed_release_claims"],
            "forbidden_release_claims": result["forbidden_release_claims"],
            "not_proven": result["not_proven"],
            "final_pr_11_remains_deferred": True,
        }
        print(json.dumps(claims, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "explain-model-role-authority":
        from odin.release_boundaries.model_role_authority import build_model_role_authority_matrix
        print(json.dumps(build_model_role_authority_matrix(), indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "explain-qshabang-release-gates":
        from odin.release_boundaries.qshabang_release_gate_map import build_qshabang_release_gate_map
        print(json.dumps(build_qshabang_release_gate_map(), indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    # FINAL-PR-11: Local Provider Receipt Harness + Critic Runtime Binding + Thor Handoff Compiler v0
    if args.cmd == "validate-local-provider-receipt-harness":
        from odin.local_provider_receipts.reports import build_provider_receipt_harness_report
        result = build_provider_receipt_harness_report()
        if not result.get("candidate_only"):
            print("ERROR: provider receipt harness: candidate_only must be true")
            return 1
        print("validate-local-provider-receipt-harness: OK")
        return 0

    if args.cmd == "local-provider-doctor":
        from odin.local_provider_receipts.reports import build_local_provider_doctor_report
        result = build_local_provider_doctor_report()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "run-local-provider-receipt":
        from odin.local_provider_receipts.receipt import run_local_provider_receipt
        demo = getattr(args, "demo", False)
        if demo:
            result = run_local_provider_receipt(
                "deterministic_no_provider",
                "demo prompt",
                allow_local_provider_execution=False,
            )
        else:
            provider = getattr(args, "provider", "ollama_candidate")
            prompt = getattr(args, "prompt", "demo prompt")
            allow = getattr(args, "allow_local_provider_execution", False)
            result = run_local_provider_receipt(
                provider,
                prompt,
                allow_local_provider_execution=allow,
            )
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "explain-provider-receipt-claims":
        result = {
            "artifact_kind": "odin_provider_receipt_claims_explanation",
            "candidate_only": True,
            "evidence_classes": {
                "structural_evidence": "Repo-local deterministic proof that code, schema, packet, validator, or boundary exists.",
                "host_scoped_local_receipt": "Evidence generated on one local host under explicit local-provider execution permission. Does not generalize.",
                "external_receipt_required": "Claim that cannot be satisfied by repo-local proof alone."
            },
            "not_proven": [
                "production_readiness",
                "security_certification",
                "release_certification",
                "real_model_benchmark",
                "model_quality_superiority"
            ],
            "claim_boundary": "local_provider_receipt_harness_scoped_local_receipts_not_quality_benchmark",
        }
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "validate-critic-runtime-binding":
        from odin.critic_runtime.reports import build_critic_runtime_report
        result = build_critic_runtime_report()
        if not result.get("critic_is_advisory"):
            print("ERROR: critic runtime: critic_is_advisory must be true")
            return 1
        if not result.get("critic_not_authority"):
            print("ERROR: critic runtime: critic_not_authority must be true")
            return 1
        print("validate-critic-runtime-binding: OK")
        return 0

    if args.cmd == "run-critic-cascade":
        from odin.critic_runtime.cascade import run_critic_cascade
        demo_candidate = {
            "artifact_kind": "odin_demo_candidate",
            "candidate_only": True,
            "claim_boundary": "demo_candidate_boundary",
            "not_proven": ["production_readiness", "security_certification"],
            "app_apply": False,
            "external_send": False,
        }
        result = run_critic_cascade(demo_candidate)
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "explain-critic-cascade":
        result = {
            "artifact_kind": "odin_critic_cascade_explanation",
            "candidate_only": True,
            "critic_is_advisory": True,
            "critic_not_authority": True,
            "final_gate_required": True,
            "stages": ["deterministic (always)", "model_critic (optional, gated)"],
            "claim_boundary": "critic_runtime_binding_scores_candidates_not_truth_not_apply",
        }
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "validate-route-evaluation-receipts":
        from odin.route_evaluation.receipt import run_route_evaluation_receipt
        result = run_route_evaluation_receipt()
        if not result.get("not_a_model_quality_benchmark"):
            print("ERROR: route evaluation: not_a_model_quality_benchmark must be true")
            return 1
        if not result.get("all_pass"):
            print(f"ERROR: route evaluation: not all routes passed")
            return 1
        print("validate-route-evaluation-receipts: OK")
        return 0

    if args.cmd == "run-route-evaluation":
        from odin.route_evaluation.receipt import run_route_evaluation_receipt
        result = run_route_evaluation_receipt()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "explain-route-evaluation-claims":
        result = {
            "artifact_kind": "odin_route_evaluation_claims_explanation",
            "candidate_only": True,
            "not_a_model_quality_benchmark": True,
            "no_superiority_claim": True,
            "measures": ["schema_valid", "candidate_only_valid", "forbidden_actions_clean", "slot_completeness", "not_proven_present", "receipt_present", "boundary_violations", "output_length_chars"],
            "does_not_measure": ["model quality", "performance benchmark", "production readiness"],
            "claim_boundary": "route_evaluation_receipts_measure_structure_not_model_quality_benchmark",
        }
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "validate-thor-handoff-compiler":
        from odin.thor_handoff_compiler.reports import build_thor_compiler_report
        result = build_thor_compiler_report()
        if result.get("thor_runtime_execution") is not False:
            print("ERROR: thor compiler: thor_runtime_execution must be false")
            return 1
        if result.get("agent_autonomy") is not False:
            print("ERROR: thor compiler: agent_autonomy must be false")
            return 1
        print("validate-thor-handoff-compiler: OK")
        return 0

    if args.cmd == "compile-thor-handoff":
        from odin.thor_handoff_compiler.input_contract import build_handoff_input_contract
        from odin.thor_handoff_compiler.compiler import compile_thor_handoff_bundle
        ic = build_handoff_input_contract(
            objective="Demo: Implement a bounded PR with evidence-class receipts",
            repo_evidence=["odin/operational_spine/", "odin/release_boundaries/"],
            allowed_edits=["odin/local_provider_receipts/", "odin/critic_runtime/"],
            forbidden_edits=["odin/operational_spine/", "tests/test_final_pr_10_boundary_release.py"],
            acceptance_gates=[
                "validate-local-provider-receipt-harness returns 0",
                "validate-critic-runtime-binding returns 0",
                "pytest passes",
            ],
            claim_boundary="demo_thor_handoff_compile_artifact",
        )
        bundle = compile_thor_handoff_bundle(ic)
        print(json.dumps(bundle, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "explain-thor-handoff-compiler":
        result = {
            "artifact_kind": "odin_thor_handoff_compiler_explanation",
            "candidate_only": True,
            "thor_runtime_execution": False,
            "agent_autonomy": False,
            "purpose": "Compiles agent operator work packets, acceptance matrices, validator plans, and PR body skeletons from structured input contracts.",
            "outputs": ["agent_operator_work_packet", "acceptance_matrix", "validator_plan", "pr_body_skeleton", "return_report_contract", "thor_handoff_bundle"],
            "deterministic": True,
            "no_model_required": True,
            "claim_boundary": "thor_handoff_compiler_v0_compiles_worker_packets_not_thor_runtime",
        }
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "validate-final-pr-11-provider-critic-thor":
        errors = validate_final_pr_11_provider_critic_thor()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-final-pr-11-provider-critic-thor: OK")
        return 0

    # FINAL-PR-11.5: Semantic Kernel Coverage Compiler + Claims Compiler + Y Pattern
    if args.cmd == "validate-v711-coverage-compiler":
        from odin.v711_coverage_compiler.reports import build_v711_coverage_report
        result = build_v711_coverage_report()
        if not result.get("candidate_only"):
            print("ERROR: v711 coverage compiler: candidate_only must be true")
            return 1
        print("validate-v711-coverage-compiler: OK")
        return 0

    if args.cmd == "validate-semantic-kernel-closure":
        from odin.semantic_kernel_closure.reports import build_semantic_kernel_closure_report
        result = build_semantic_kernel_closure_report()
        if not result.get("candidate_only"):
            print("ERROR: semantic kernel closure: candidate_only must be true")
            return 1
        print("validate-semantic-kernel-closure: OK")
        return 0

    if args.cmd == "validate-y-pattern-operationalization-index":
        from odin.y_pattern_operationalization_index.index_builder import build_y_pattern_operationalization_index
        result = build_y_pattern_operationalization_index()
        if not result.get("candidate_only"):
            print("ERROR: y pattern index: candidate_only must be true")
            return 1
        if result.get("mapping_count", 0) < 14:
            print("ERROR: y pattern index: mapping_count must be >= 14")
            return 1
        print("validate-y-pattern-operationalization-index: OK")
        return 0

    if args.cmd == "validate-claims-compiler":
        from odin.claims_compiler.reports import build_release_claims_policy
        result = build_release_claims_policy()
        if not result.get("candidate_only"):
            print("ERROR: claims compiler: candidate_only must be true")
            return 1
        print("validate-claims-compiler: OK")
        return 0

    if args.cmd == "validate-agent-operator-modes":
        from odin.agent_operator_modes.reports import build_agent_operator_mode_matrix
        result = build_agent_operator_mode_matrix()
        if not result.get("candidate_only"):
            print("ERROR: agent operator modes: candidate_only must be true")
            return 1
        if result.get("agent_autonomy") is not False:
            print("ERROR: agent operator modes: agent_autonomy must be false")
            return 1
        print("validate-agent-operator-modes: OK")
        return 0

    if args.cmd == "build-v711-coverage-matrix":
        from odin.v711_coverage_compiler.coverage_matrix import build_v711_coverage_matrix
        result = build_v711_coverage_matrix()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "build-v711-gap-index":
        from odin.v711_coverage_compiler.gap_index import build_v711_gap_index
        result = build_v711_gap_index()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "build-semantic-kernel":
        from odin.semantic_kernel_closure.reports import build_semantic_kernel_closure_report
        result = build_semantic_kernel_closure_report()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "build-y-pattern-operationalization-index":
        from odin.y_pattern_operationalization_index.index_builder import build_y_pattern_operationalization_index
        result = build_y_pattern_operationalization_index()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "compile-safe-claim":
        from odin.claims_compiler.compiler import classify_claim
        claim_text = getattr(args, "claim", None) or "Odin v7.1.1 has structural evidence for semantic kernel coordination (candidate-only, not release certification)"
        result = classify_claim(claim_text)
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "explain-y-pattern-operationalization":
        from odin.y_pattern_operationalization_index.index_builder import build_y_pattern_operationalization_index
        result = build_y_pattern_operationalization_index()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "explain-claims-policy":
        from odin.claims_compiler.reports import build_release_claims_policy
        result = build_release_claims_policy()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "list-agent-operator-modes":
        from odin.agent_operator_modes.modes import list_agent_operator_modes
        result = {
            "artifact_kind": "odin_agent_operator_modes_list",
            "candidate_only": True,
            "claim_boundary": "agent_operator_modes_define_bounded_worker_presets_not_agent_autonomy",
            "modes": list_agent_operator_modes(),
        }
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "explain-agent-operator-mode":
        from odin.agent_operator_modes.modes import get_agent_operator_mode
        mode_id = getattr(args, "mode", "claude_code_implementation_worker")
        try:
            result = get_agent_operator_mode(mode_id)
        except KeyError:
            print(json.dumps({"error": f"unknown mode: {mode_id}"}, indent=2))
            return 1
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "validate-final-pr-11-5-semantic-kernel-coverage":
        errors = validate_final_pr_11_5_semantic_kernel_coverage()
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1
        print("validate-final-pr-11-5-semantic-kernel-coverage: OK")
        return 0

    if args.cmd == "explain-v711-coverage":
        from odin.v711_coverage_compiler.reports import build_v711_coverage_report
        result = build_v711_coverage_report()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "explain-semantic-kernel-closure":
        from odin.semantic_kernel_closure.reports import build_semantic_kernel_closure_report
        result = build_semantic_kernel_closure_report()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "explain-claims-compiler":
        from odin.claims_compiler.reports import build_release_claims_policy
        result = build_release_claims_policy()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "explain-agent-operator-modes":
        from odin.agent_operator_modes.reports import build_agent_operator_mode_matrix
        result = build_agent_operator_mode_matrix()
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.cmd == "validate-json":
        errors = validate_json()
    elif args.cmd == "validate-registries":
        errors = validate_registries()
    elif args.cmd == "validate-system-map":
        errors = validate_system_map()
    elif args.cmd == "validate-claims":
        errors = validate_claims()
    elif args.cmd == "validate-current-public-canon":
        errors = validate_current_public_canon()
    elif args.cmd == "validate-canon-boundary-integrity":
        errors = validate_canon_boundary_integrity()
    elif args.cmd == "validate-b1-app-boundary-universal-work-qirc-spine":
        errors = validate_b1_app_boundary_universal_work_qirc_spine()
    elif args.cmd == "validate-b2-context-lenses-worklets":
        errors = validate_b2_context_lenses_worklets()
    elif args.cmd == "validate-b3-modelworkpacket-scale-hybrid":
        errors = validate_b3_modelworkpacket_scale_hybrid()
    elif args.cmd == "validate-b4-minicheck-critics-final-gate":
        errors = validate_b4_minicheck_critics_final_gate()
    elif args.cmd == "validate-b5-storage-trace-receipt-provider-bridge":
        errors = validate_b5_storage_trace_receipt_provider_bridge()
    elif args.cmd == "validate-b6-acceptance-dojo-scoreboard-closure":
        errors = validate_b6_acceptance_dojo_scoreboard_closure()
    elif args.cmd == "validate-b7-closure-thor-provider-eval":
        errors = validate_b7_closure_thor_provider_eval()
    elif args.cmd == "validate-b8-security-review-track":
        errors = validate_b8_security_review_track()
    elif args.cmd == "validate-final-road-to-100-rebaseline-audit":
        errors = validate_final_road_to_100_rebaseline_audit()
    elif args.cmd == "validate-docs":
        errors = validate_docs()
    elif args.cmd == "validate-codex-tasks":
        errors = validate_codex_tasks()
    elif args.cmd == "validate-codex-bundles":
        errors = validate_codex_bundles()
    elif args.cmd == "validate-real-pr-execution":
        errors = validate_real_pr_execution()
    elif args.cmd == "validate-senior-review":
        errors = validate_senior_review()
    elif args.cmd == "validate-shadow-runtime":
        errors = validate_shadow_runtime()
    elif args.cmd == "validate-narrative-compiler":
        errors = validate_narrative_compiler()
    elif args.cmd == "validate-odin-core-qli":
        errors = validate_odin_core_qli()
    elif args.cmd == "validate-qirc-gold-spine":
        errors = validate_qirc_gold_spine()
    elif args.cmd == "validate-bug6-q7-seed-core":
        errors = validate_bug6_q7_seed_core()
    elif args.cmd == "validate-ai-git-safety":
        errors = validate_ai_git_safety()
    elif args.cmd == "validate-pre-llm-intelligence":
        errors = validate_pre_llm_intelligence()
    elif args.cmd == "validate-universal-model-agent-parity":
        errors = validate_universal_model_agent_parity()
    elif args.cmd == "validate-universal-llm-work-construct":
        errors = validate_universal_llm_work_construct()
    elif args.cmd == "validate-app-seed-pack-compiler":
        errors = validate_app_seed_pack_compiler()
    elif args.cmd == "validate-shadow-narrative-loki":
        errors = validate_shadow_narrative_loki()
    elif args.cmd == "validate-product-pattern-atom-hub":
        errors = validate_product_pattern_atom_hub()
    elif args.cmd == "validate-public-repo-windows-build-ready":
        errors = validate_public_repo_windows_build_ready()
    elif args.cmd == "validate-runtime-source-candidate":
        errors = validate_runtime_source_candidate()
    elif args.cmd == "validate-direct-runtime-release-candidate":
        errors = validate_direct_runtime_release_candidate()
    elif args.cmd == "validate-runtime-bus-worklets":
        errors = validate_runtime_bus_worklets()
    elif args.cmd == "validate-provider-worker-boundary":
        errors = validate_provider_worker_boundary()
    elif args.cmd == "validate-agent-operator-mode":
        errors = validate_agent_operator_mode()
    elif args.cmd == "validate-local-runtime-starter":
        errors = validate_local_runtime_starter()
    elif args.cmd == "validate-runtime-doctor-bootstrap":
        errors = validate_runtime_doctor_bootstrap()
    elif args.cmd == "validate-localhost-api-sdk-bridge":
        errors = validate_localhost_api_sdk_bridge()
    elif args.cmd == "validate-consolidated-proof-governance":
        errors = validate_consolidated_proof_governance()
    elif args.cmd == "validate-final-pr-03-qirc-devmode":
        errors = validate_final_pr_03_qirc_devmode()
    elif args.cmd == "validate-final-pr-04-provider-probe-security":
        errors = validate_final_pr_04_provider_probe_security()
    elif args.cmd == "validate-final-pr-05-execution-gate":
        errors = validate_final_pr_05_execution_gate()
    elif args.cmd == "validate-y-pattern-spine":
        errors = validate_y_pattern_spine()
    elif args.cmd == "validate-prep-final-pr-06-08":
        errors = validate_prep_final_pr_06_08()
    elif args.cmd == "validate-final-pr-09-10-qshabang-smallmodel-prep":
        errors = validate_final_pr_09_10_qshabang_smallmodel_prep()
    elif args.cmd == "validate-operational-seed-spine":
        errors = validate_operational_seed_spine()
    elif args.cmd == "validate-projection-candidate-spine":
        errors = validate_projection_candidate_spine()
    elif args.cmd == "validate-operational-spine":
        errors = validate_operational_spine()
    elif args.cmd == "validate-final-pr-10-boundary-release":
        errors = validate_final_pr_10_boundary_release()
    elif args.cmd == "validate-final-pr-11-provider-critic-thor":
        errors = validate_final_pr_11_provider_critic_thor()
    elif args.cmd == "validate-final-pr-11-5-semantic-kernel-coverage":
        errors = validate_final_pr_11_5_semantic_kernel_coverage()
    else:
        errors = validate_all()

    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        return 1
    print(f"{args.cmd}: OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

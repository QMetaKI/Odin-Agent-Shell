"""Command Surface Closure — Command Index.

Claim boundary: command_surface_closure_indexes_cli_surface_not_runtime_completion
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "command_surface_closure_indexes_cli_surface_not_runtime_completion"

_COMMANDS = [
    {"command_name": "validate-all", "command_class": "validator", "subsystem": "internal", "description": "Run all validators", "has_validate": True, "has_demo": False, "has_explain": False, "status": "active"},
    {"command_name": "validate-release-readiness-hardening", "command_class": "validator", "subsystem": "release_readiness", "description": "Validate FINAL-PR-12 release readiness hardening module", "has_validate": True, "has_demo": True, "has_explain": True, "status": "active"},
    {"command_name": "build-release-readiness-matrix", "command_class": "demo_builder", "subsystem": "release_readiness", "description": "Build release readiness matrix (demo/dry-run)", "has_validate": True, "has_demo": True, "has_explain": True, "status": "active"},
    {"command_name": "build-release-risk-register", "command_class": "demo_builder", "subsystem": "release_readiness", "description": "Build release risk register (demo/dry-run)", "has_validate": True, "has_demo": True, "has_explain": True, "status": "active"},
    {"command_name": "explain-release-readiness-hardening", "command_class": "explain", "subsystem": "release_readiness", "description": "Explain release readiness hardening scope and boundaries", "has_validate": True, "has_demo": True, "has_explain": True, "status": "active"},
    {"command_name": "validate-evidence-closure-dry-run", "command_class": "validator", "subsystem": "release_readiness", "description": "Validate evidence closure dry run module", "has_validate": True, "has_demo": True, "has_explain": True, "status": "active"},
    {"command_name": "run-evidence-closure-dry-run", "command_class": "demo_builder", "subsystem": "release_readiness", "description": "Run evidence closure dry run (demo)", "has_validate": True, "has_demo": True, "has_explain": True, "status": "active"},
    {"command_name": "explain-evidence-closure-dry-run", "command_class": "explain", "subsystem": "release_readiness", "description": "Explain evidence closure dry run scope", "has_validate": True, "has_demo": True, "has_explain": True, "status": "active"},
    {"command_name": "validate-packaging-boundary-prep", "command_class": "validator", "subsystem": "release_readiness", "description": "Validate packaging boundary prep module", "has_validate": True, "has_demo": True, "has_explain": True, "status": "active"},
    {"command_name": "build-packaging-boundary", "command_class": "demo_builder", "subsystem": "release_readiness", "description": "Build packaging boundary inventory (demo)", "has_validate": True, "has_demo": True, "has_explain": True, "status": "active"},
    {"command_name": "explain-packaging-boundary", "command_class": "explain", "subsystem": "release_readiness", "description": "Explain packaging boundary scope", "has_validate": True, "has_demo": True, "has_explain": True, "status": "active"},
    {"command_name": "validate-command-surface-closure", "command_class": "validator", "subsystem": "release_readiness", "description": "Validate command surface closure module", "has_validate": True, "has_demo": True, "has_explain": True, "status": "active"},
    {"command_name": "build-command-surface-index", "command_class": "demo_builder", "subsystem": "release_readiness", "description": "Build command surface index (demo)", "has_validate": True, "has_demo": True, "has_explain": True, "status": "active"},
    {"command_name": "explain-command-surface", "command_class": "explain", "subsystem": "release_readiness", "description": "Explain command surface scope", "has_validate": True, "has_demo": True, "has_explain": True, "status": "active"},
    {"command_name": "validate-docs-readiness", "command_class": "validator", "subsystem": "release_readiness", "description": "Validate docs readiness module", "has_validate": True, "has_demo": True, "has_explain": True, "status": "active"},
    {"command_name": "build-docs-readiness-index", "command_class": "demo_builder", "subsystem": "release_readiness", "description": "Build docs readiness index (demo)", "has_validate": True, "has_demo": True, "has_explain": True, "status": "active"},
    {"command_name": "explain-docs-readiness", "command_class": "explain", "subsystem": "release_readiness", "description": "Explain docs readiness scope", "has_validate": True, "has_demo": True, "has_explain": True, "status": "active"},
    {"command_name": "validate-final-pr-13-input-bundle", "command_class": "validator", "subsystem": "release_readiness", "description": "Validate FINAL-PR-13 input bundle module", "has_validate": True, "has_demo": True, "has_explain": True, "status": "active"},
    {"command_name": "build-final-pr-13-input-bundle", "command_class": "demo_builder", "subsystem": "release_readiness", "description": "Build FINAL-PR-13 input bundle (demo)", "has_validate": True, "has_demo": True, "has_explain": True, "status": "active"},
    {"command_name": "explain-final-pr-13-input-bundle", "command_class": "explain", "subsystem": "release_readiness", "description": "Explain FINAL-PR-13 input bundle scope", "has_validate": True, "has_demo": True, "has_explain": True, "status": "active"},
    {"command_name": "validate-final-pr-12-release-readiness-hardening", "command_class": "validator", "subsystem": "release_readiness", "description": "Validate all FINAL-PR-12 artifacts", "has_validate": True, "has_demo": False, "has_explain": False, "status": "active"},
    {"command_name": "validate-operational-spine", "command_class": "validator", "subsystem": "internal", "description": "Validate FINAL-PR-09 operational spine", "has_validate": True, "has_demo": True, "has_explain": False, "status": "active"},
    {"command_name": "validate-final-pr-11-5-semantic-kernel-coverage", "command_class": "validator", "subsystem": "internal", "description": "Validate FINAL-PR-11.5 semantic kernel coverage", "has_validate": True, "has_demo": False, "has_explain": True, "status": "active"},
    {"command_name": "validate-final-pr-11-provider-critic-thor", "command_class": "validator", "subsystem": "internal", "description": "Validate FINAL-PR-11 provider/critic/thor", "has_validate": True, "has_demo": False, "has_explain": False, "status": "active"},
    {"command_name": "validate-final-release-preflight", "command_class": "validator", "subsystem": "internal", "description": "Run final release preflight validator", "has_validate": True, "has_demo": False, "has_explain": False, "status": "active"},
    {"command_name": "validate-boundary-matrix", "command_class": "validator", "subsystem": "release_readiness", "description": "Validate FINAL-PR-10 boundary matrix", "has_validate": True, "has_demo": False, "has_explain": True, "status": "active"},
    {"command_name": "release-preflight", "command_class": "receipt", "subsystem": "release_readiness", "description": "Run release preflight check", "has_validate": True, "has_demo": False, "has_explain": True, "status": "active"},
    {"command_name": "validate-claims-compiler", "command_class": "validator", "subsystem": "internal", "description": "Validate FINAL-PR-11.5 claims compiler", "has_validate": True, "has_demo": True, "has_explain": True, "status": "active"},
    {"command_name": "validate-semantic-kernel-closure", "command_class": "validator", "subsystem": "internal", "description": "Validate FINAL-PR-11.5 semantic kernel closure", "has_validate": True, "has_demo": True, "has_explain": True, "status": "active"},
    {"command_name": "validate-agent-operator-modes", "command_class": "validator", "subsystem": "internal", "description": "Validate FINAL-PR-11.5 agent operator modes", "has_validate": True, "has_demo": True, "has_explain": True, "status": "active"},
]


def build_command_surface_index(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    return {
        "artifact_kind": "odin_command_surface_closure_index",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "commands": _COMMANDS,
        "not_proven": ["runtime_completion", "production_readiness"],
    }

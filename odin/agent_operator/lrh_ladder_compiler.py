"""LRH Ladder Compiler v1 — compile LRH ladder metadata to Agent Work Packets.

Claim boundary: lrh_ladder_compiler_candidate_only_no_app_apply_no_external_send
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[2]

_LADDER_REGISTRY_PATH = _ROOT / "registries" / "local_runtime_hub_build_ladder_v1.json"
_LADDER_MARKDOWN_PATH = _ROOT / "docs" / "rebaseline" / "LOCAL_RUNTIME_HUB_BUILD_LADDER_V1.md"

# Key variants supported for the ladder list
_LADDER_LIST_KEYS = ("ladder", "prs", "items", "slices", "entries")

# Key variants supported for allowed-file lists
_ALLOWED_FILE_KEYS = ("target_files", "allowed_new_files", "allowed_files", "existing_files")

# Key variants supported for forbidden scope
_FORBIDDEN_KEYS = ("forbidden_scope", "forbidden", "forbidden_actions")

# Key variants supported for required commands
_REQUIRED_CMD_KEYS = ("required_commands",)

# Key variants supported for acceptance gates
_GATE_KEYS = ("acceptance_gates", "definition_of_done")

# Key variants supported for proof boundaries
_PROOF_KEYS = ("proof_boundaries",)

# Key variants for objective
_OBJECTIVE_KEYS = ("objective", "goal", "summary")

_DEFAULT_PROOF_BOUNDARIES = [
    "no_production_readiness_proof",
    "no_public_network_api_proof",
    "no_app_state_mutation_proof",
    "no_external_send_authority_proof",
    "no_live_model_inference_proof",
    "no_security_certification_proof",
]

def _get_default_forbidden_actions() -> list[str]:
    try:
        from odin.agent_operator.guards import HARD_FORBIDDEN_ACTIONS
        return sorted(HARD_FORBIDDEN_ACTIONS)
    except Exception:
        return [
            "app_state_apply",
            "claiming_proof_without_receipt",
            "domain_state_mutation",
            "external_send",
            "hidden_tool_execution",
            "network_transport_by_default",
            "provider_api_call_without_receipt",
            "secret_exfiltration",
            "unbounded_file_edit",
        ]


def load_lrh_ladder() -> tuple[dict[str, Any], list[str]]:
    """Load LRH ladder from registry JSON with fallback to markdown.

    Returns (data, missing_keys_list).
    """
    missing: list[str] = []
    if _LADDER_REGISTRY_PATH.exists():
        try:
            with _LADDER_REGISTRY_PATH.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return data, missing
        except Exception as exc:
            missing.append(f"registry_parse_error: {exc}")

    missing.append("ladder_registry_missing_or_unparseable")

    # Fallback: parse markdown
    if _LADDER_MARKDOWN_PATH.exists():
        try:
            data = _parse_ladder_markdown(_LADDER_MARKDOWN_PATH)
            return data, missing
        except Exception as exc:
            missing.append(f"markdown_fallback_parse_error: {exc}")

    return {}, missing + ["ladder_source_unavailable"]


def _parse_ladder_markdown(path: Path) -> dict[str, Any]:
    """Minimal markdown fallback: extract PR sections as structured entries."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    entries: list[dict] = []
    # Find headings like ## LRH-PR-06 or ### LRH-PR-06
    sections = re.split(r"\n#{1,3}\s+(LRH-PR-\d+)", text)
    i = 1
    while i < len(sections) - 1:
        pr_id = sections[i].strip()
        body = sections[i + 1] if i + 1 < len(sections) else ""
        entry: dict[str, Any] = {"id": pr_id}
        # Extract objective
        obj_match = re.search(r"[Oo]bjective[:\s]+(.+)", body)
        if obj_match:
            entry["objective"] = obj_match.group(1).strip()
        # Extract bullet-listed target files
        file_lines = re.findall(r"-\s+`?(odin/[^\s`]+|docs/[^\s`]+|tests/[^\s`]+|schemas/[^\s`]+|examples/[^\s`]+)`?", body)
        if file_lines:
            entry["target_files"] = file_lines
        entries.append(entry)
        i += 2
    return {"artifact_kind": "odin_local_runtime_hub_build_ladder", "ladder": entries, "_source": "markdown_fallback"}


def _get_pr_list(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Return the PR list from a ladder dict using any supported key."""
    for key in _LADDER_LIST_KEYS:
        if key in data:
            val = data[key]
            if isinstance(val, list):
                return val
    return []


def find_lrh_pr(pr_id: str, data: dict[str, Any] | None = None) -> tuple[dict[str, Any] | None, list[str]]:
    """Find a single PR entry by normalised ID (e.g. '06' → 'LRH-PR-06').

    Returns (pr_entry_or_None, missing_keys_list).
    """
    missing: list[str] = []
    if data is None:
        data, extra_missing = load_lrh_ladder()
        missing.extend(extra_missing)

    normalised = _normalise_pr_id(pr_id)
    pr_list = _get_pr_list(data)

    if not pr_list:
        missing.append("no_pr_list_found_in_ladder_data")
        return None, missing

    for entry in pr_list:
        if isinstance(entry, dict) and entry.get("id") == normalised:
            return entry, missing

    missing.append(f"pr_id_{normalised}_not_found_in_ladder")
    return None, missing


def _normalise_pr_id(pr_id: str) -> str:
    """Convert '6', '06', 'LRH-PR-06' to canonical 'LRH-PR-06'."""
    s = str(pr_id).strip()
    if s.startswith("LRH-PR-"):
        return s
    try:
        n = int(s)
        return f"LRH-PR-{n:02d}"
    except ValueError:
        return s


def _pick(entry: dict, keys: tuple, missing: list[str], label: str) -> Any:
    """Pick first present key from a tuple of candidates; record if all missing."""
    for k in keys:
        if k in entry:
            return entry[k]
    missing.append(f"optional_field_missing: {label} ({', '.join(keys)})")
    return None


def compile_lrh_pr_to_agent_task(pr_id: str) -> tuple[str, list[str]]:
    """Return the objective string for a PR. Falls back to a generated description."""
    entry, missing = find_lrh_pr(pr_id)
    if entry is None:
        return f"LRH {_normalise_pr_id(pr_id)} — objective not found in ladder", missing
    obj = _pick(entry, _OBJECTIVE_KEYS, missing, "objective")
    if obj:
        return str(obj), missing
    title = entry.get("title", "")
    return f"{_normalise_pr_id(pr_id)}: {title}", missing


def compile_lrh_pr_to_allowed_files(pr_id: str) -> tuple[list[str], list[str]]:
    """Return allowed files list for a PR."""
    entry, missing = find_lrh_pr(pr_id)
    if entry is None:
        return [], missing
    result: list[str] = []
    for key in _ALLOWED_FILE_KEYS:
        val = entry.get(key)
        if isinstance(val, list):
            result.extend(v for v in val if v not in result)
    if not result:
        missing.append(f"optional_field_missing: allowed_files ({', '.join(_ALLOWED_FILE_KEYS)})")
    return result, missing


def compile_lrh_pr_to_forbidden_scope(pr_id: str) -> tuple[list[str], list[str]]:
    """Return forbidden scope list for a PR."""
    entry, missing = find_lrh_pr(pr_id)
    if entry is None:
        return _get_default_forbidden_actions(), missing
    scope = _pick(entry, _FORBIDDEN_KEYS, missing, "forbidden_scope")
    if isinstance(scope, list):
        return scope, missing
    return _get_default_forbidden_actions(), missing


def compile_lrh_pr_to_required_commands(pr_id: str) -> tuple[list[str], list[str]]:
    """Return required commands list for a PR."""
    entry, missing = find_lrh_pr(pr_id)
    if entry is None:
        return [], missing
    cmds = _pick(entry, _REQUIRED_CMD_KEYS, missing, "required_commands")
    if isinstance(cmds, list):
        return cmds, missing
    return [], missing


def compile_lrh_pr_to_acceptance_gates(pr_id: str) -> tuple[list[str], list[str]]:
    """Return acceptance gates for a PR."""
    entry, missing = find_lrh_pr(pr_id)
    if entry is None:
        return ["validate-all passes", "pytest passes"], missing
    gates = _pick(entry, _GATE_KEYS, missing, "acceptance_gates")
    if isinstance(gates, list):
        return gates, missing
    return ["validate-all passes", "pytest passes"], missing


def compile_lrh_pr_to_proof_boundaries(pr_id: str) -> tuple[list[str], list[str]]:
    """Return proof boundaries for a PR."""
    entry, missing = find_lrh_pr(pr_id)
    if entry is None:
        return _DEFAULT_PROOF_BOUNDARIES[:], missing
    bounds = _pick(entry, _PROOF_KEYS, missing, "proof_boundaries")
    if isinstance(bounds, list):
        return bounds, missing
    missing.append("proof_boundaries_defaulted")
    return _DEFAULT_PROOF_BOUNDARIES[:], missing


def compile_lrh_pr_to_agent_work_packet(
    pr_id: str,
    agent_profile_id: str = "claude-code",
) -> dict[str, Any]:
    """Compile a full Agent Work Packet from LRH ladder metadata for a PR."""
    normalised = _normalise_pr_id(pr_id)
    all_missing: list[str] = []

    objective, m = compile_lrh_pr_to_agent_task(pr_id)
    all_missing.extend(m)

    allowed_files, m = compile_lrh_pr_to_allowed_files(pr_id)
    all_missing.extend(m)

    forbidden_scope, m = compile_lrh_pr_to_forbidden_scope(pr_id)
    all_missing.extend(m)

    required_commands, m = compile_lrh_pr_to_required_commands(pr_id)
    all_missing.extend(m)

    acceptance_gates, m = compile_lrh_pr_to_acceptance_gates(pr_id)
    all_missing.extend(m)

    proof_boundaries, m = compile_lrh_pr_to_proof_boundaries(pr_id)
    all_missing.extend(m)

    # Ensure forbidden_actions always include hard Odin boundaries
    _default_forbidden = _get_default_forbidden_actions()
    forbidden_actions = list(set(_default_forbidden) | set(
        f for f in forbidden_scope if isinstance(f, str) and not f.startswith("no ")
    ))

    packet: dict[str, Any] = {
        "artifact_kind": "odin_agent_work_packet",
        "schema_version": "1.0",
        "packet_id": f"AWP-{agent_profile_id.upper()}-{normalised}-CANDIDATE",
        "agent_profile_id": agent_profile_id,
        "task_source": f"lrh_ladder_compiler_v1_{normalised}",
        "lrh_pr": pr_id,
        "lrh_pr_id": normalised,
        "objective": objective,
        "repo_scope": {"root": ".", "branch": "main"},
        "allowed_files": allowed_files,
        "forbidden_files": [],
        "forbidden_actions": sorted(set(forbidden_actions)),
        "forbidden_scope": forbidden_scope,
        "required_context": [
            "AGENTS.md", "CODEX_START_HERE.md", "CLAIM_BOUNDARY.md",
            "docs/AGENT_OPERATOR_MODE_V1.md",
            f"registries/local_runtime_hub_build_ladder_v1.json (entry {normalised})",
        ],
        "required_commands": required_commands,
        "acceptance_gates": acceptance_gates,
        "proof_boundaries": proof_boundaries,
        "claim_boundaries": [
            "candidate_patch_only",
            "no_runtime_proof_claimed",
            "no_host_validation_claimed",
            f"lrh_ladder_compiler_v1_{normalised}_candidate_only",
        ],
        "senior_reviewer_required": True,
        "senior_code_reviewer_required": True,
        "thor_compatibility": {
            "status": "advisory_only",
            "claim_boundary": "thor_output_advisory_not_odin_authority",
        },
        "future_target_flags": [],
        "candidate_only": True,
        "app_owned_apply": True,
        "external_send_default": False,
        "network_transport_default": False,
        "hidden_tool_execution_allowed": False,
        "created_by": f"odin.agent_operator.lrh_ladder_compiler (pr={normalised}, agent={agent_profile_id})",
        "created_at_policy": "deterministic_fixture",
        "compiler_metadata": {
            "source": str(_LADDER_REGISTRY_PATH.relative_to(_ROOT)) if _LADDER_REGISTRY_PATH.exists() else "missing",
            "fallback_source": str(_LADDER_MARKDOWN_PATH.relative_to(_ROOT)) if _LADDER_MARKDOWN_PATH.exists() else "missing",
            "missing_optional_keys": sorted(set(all_missing)),
        },
    }
    return packet

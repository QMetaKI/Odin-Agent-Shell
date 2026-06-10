from __future__ import annotations
from odin.quality.boundaries import scan_forbidden_markers
from odin.runtime.ids import stable_id
from .spine import build_pattern_spine


def validate_pattern_mine(mine: dict) -> list[str]:
    errors: list[str] = []
    if mine.get("artifact_kind") not in {"odin_pattern_mine", "pattern_mine_manifest"}:
        errors.append("pattern mine artifact_kind must be odin_pattern_mine or pattern_mine_manifest")
    if not mine.get("patterns") and not mine.get("flow_packs"):
        errors.append("pattern mine must contain patterns or flow_packs")
    forbidden = set(scan_forbidden_markers(mine)) & {"direct_apply", "external_send", "network_send", "mutate_app_state"}
    if forbidden:
        errors.append("forbidden pattern mine markers: " + ", ".join(sorted(forbidden)))
    if mine.get("truth_authority") is True:
        errors.append("pattern mine may not declare truth_authority")
    return errors


def _normalize_pattern(pattern: dict | str) -> dict:
    if isinstance(pattern, str):
        pattern = {"id": pattern, "label": pattern}
    pid = pattern.get("id") or stable_id("PAT", pattern, 10)
    return {
        "id": pid,
        "label": pattern.get("label", pid),
        "tags": list(pattern.get("tags", [])),
        "operators": list(pattern.get("operators", [])),
        "failure_modes": list(pattern.get("failure_modes", [])),
        "candidate_template": pattern.get("candidate_template", pid),
    }


def compile_pattern_mine(mine: dict) -> dict:
    errors = validate_pattern_mine(mine)
    patterns = [_normalize_pattern(p) for p in mine.get("patterns", [])]
    flow_packs = mine.get("flow_packs", [])
    spine = build_pattern_spine(patterns, flow_packs)
    return {
        "artifact_kind": "odin_compiled_pattern_mine",
        "protocol_version": "7.1",
        "mine_id": mine.get("mine_id", mine.get("id", stable_id("MINE", mine, 10))),
        "status": "blocked" if errors else "compiled_candidate",
        "errors": errors,
        "patterns": patterns,
        "flow_packs": flow_packs,
        "pattern_spine": spine,
        "candidate_only": True,
        "claim_boundary": "pattern_mines_are_optional_pattern_priors_not_domain_truth",
    }

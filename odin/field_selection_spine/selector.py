"""Deterministic field route selector for FINAL-PR-07.

Field Selection scores candidate routing fields. It does not decide, authorize,
claim truth, claim probability, execute, mutate app state, or send externally.
"""
from __future__ import annotations

from dataclasses import dataclass

from odin.field_selection_spine.coherence import CoherenceScore, score_coherence
from odin.field_selection_spine.fields import CLAIM_BOUNDARY, FIELD_DEFINITIONS, FIELD_IDS, DominantField, FieldSignal, SuppressedField, bound_score
from odin.field_selection_spine.proof import REQUIRED_NOT_PROVEN
from odin.field_selection_spine.review_axes import REVIEW_AXIS_IDS
from odin.field_selection_spine.why_trace import FieldWhyTrace, build_field_why_trace

_SEED_TO_FIELD = {
    "repo_cognition": "repo_reality_alignment",
    "review_audit": "evidence_sufficiency",
    "proof_receipt": "evidence_sufficiency",
    "execution_gate": "app_authority_boundary",
    "provider_probe": "runtime_truth_alignment",
    "qirc_event": "locality_preservation",
    "release_closure": "release_readiness_boundary",
    "doc_architecture": "scope_control",
    "prompt_to_work": "scope_control",
    "code_change": "candidate_integrity",
    "local_hub_ui": "locality_preservation",
    "debug_error_triage": "runtime_truth_alignment",
}

_WORK_TYPE_TO_FIELD = {
    "repo": "repo_reality_alignment",
    "review": "evidence_sufficiency",
    "proof": "evidence_sufficiency",
    "gate": "app_authority_boundary",
    "provider": "runtime_truth_alignment",
    "event": "locality_preservation",
    "release": "release_readiness_boundary",
    "doc": "scope_control",
    "prompt": "scope_control",
    "code": "candidate_integrity",
    "hub": "locality_preservation",
    "debug": "runtime_truth_alignment",
}


@dataclass(frozen=True)
class FieldSelection:
    dominant_field: DominantField
    suppressed_fields: list[SuppressedField]
    coherence_score: CoherenceScore
    review_axes_applied: list[str]
    why_trace: FieldWhyTrace
    route_recommendation: str
    candidate_only: bool = True
    app_owned_apply: bool = True
    claim_boundary: str = CLAIM_BOUNDARY

    def to_dict(self) -> dict:
        return {
            "dominant_field": self.dominant_field.to_dict(),
            "suppressed_fields": [field.to_dict() for field in self.suppressed_fields],
            "coherence_score": self.coherence_score.to_dict(),
            "review_axes_applied": list(self.review_axes_applied),
            "why_trace": self.why_trace.to_dict(),
            "route_recommendation": self.route_recommendation,
            "candidate_only": self.candidate_only,
            "app_owned_apply": self.app_owned_apply,
            "claim_boundary": self.claim_boundary,
        }


def _seed_route_to_context(seed_route) -> dict:
    if hasattr(seed_route, "to_dict"):
        data = seed_route.to_dict()
    elif isinstance(seed_route, dict):
        data = dict(seed_route)
    else:
        data = {name: getattr(seed_route, name) for name in ("selected_seed_id", "selected_role_profile_id", "matched_trigger_shapes", "missing_input_requirements", "fallback_used", "selection_priority") if hasattr(seed_route, name)}
    data["seed_route_available"] = True
    data.setdefault("candidate_only", True)
    data.setdefault("app_owned_apply", True)
    data.setdefault("local_only", True)
    data.setdefault("release_deferred", True)
    return data


def _context_evidence(context: dict) -> list[str]:
    evidence: list[str] = []
    for key in sorted(context):
        value = context[key]
        if value is None or value == "":
            continue
        if key == "selected_seed_id":
            evidence.append(f"seed_route.selected_seed_id={value}")
        elif key == "family":
            evidence.append(f"seed_route.family={value}")
        elif key in {"work_type", "trigger_shape", "selection_priority", "repo_evidence", "claim_boundary"}:
            evidence.append(f"{key}={value}")
        elif key in {"candidate_only", "app_owned_apply", "local_only", "release_deferred", "seed_route_available"}:
            evidence.append(f"{key}={value}")
    return evidence


def _choose_field(context: dict, evidence_items: list[str]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    risk_text = " ".join(str(context.get(key, "")).lower() for key in ("risk", "claim_risk", "warning", "intent"))
    if "claim" in risk_text or "truth" in risk_text or "authority" in risk_text or context.get("claim_boundary_risk") is True:
        return "claim_boundary_integrity", ["claim_boundary_risk"]
    if context.get("repo_evidence_missing") is True:
        return "repo_reality_alignment", ["repo_evidence_missing"]
    if not evidence_items:
        return "evidence_sufficiency", ["missing_repo_evidence"]
    seed_id = str(context.get("selected_seed_id", ""))
    if seed_id in _SEED_TO_FIELD:
        reasons.extend(["seed_route_available", f"seed_id:{seed_id}"])
        return _SEED_TO_FIELD[seed_id], reasons
    family = str(context.get("family", ""))
    if family in {"evidence", "boundary", "economy"}:
        mapped = {"evidence": "evidence_sufficiency", "boundary": "claim_boundary_integrity", "economy": "token_efficiency"}[family]
        return mapped, ["seed_family_available", f"family:{family}"]
    work_type = str(context.get("work_type", "")).lower()
    if work_type in _WORK_TYPE_TO_FIELD:
        return _WORK_TYPE_TO_FIELD[work_type], ["work_type_available", f"work_type:{work_type}"]
    return "scope_control", ["deterministic_fallback"]


def _build_signals(dominant_field_id: str, evidence_items: list[str]) -> list[FieldSignal]:
    signals: list[FieldSignal] = []
    for field_id in FIELD_IDS:
        definition = FIELD_DEFINITIONS[field_id]
        is_dominant = field_id == dominant_field_id
        signals.append(FieldSignal(
            field_id=field_id,
            field_name=definition["field_name"],
            signal_weight=0.9 if is_dominant else 0.25,
            evidence_list=list(evidence_items) if is_dominant else [],
            suppression_reason=None if is_dominant else "lower_priority_candidate_field",
        ))
    return signals


def select_field_route(work_context: dict) -> FieldSelection:
    context = dict(work_context or {})
    context.setdefault("candidate_only", True)
    context.setdefault("app_owned_apply", True)
    context.setdefault("local_only", True)
    context.setdefault("release_deferred", True)
    evidence_items = _context_evidence(context)
    dominant_field_id, reason_tokens = _choose_field(context, evidence_items)
    field_definition = FIELD_DEFINITIONS[dominant_field_id]
    required_evidence = list(field_definition["default_evidence_requirement"])
    if dominant_field_id == "repo_reality_alignment" and any("selected_seed_id" in item for item in evidence_items):
        required_evidence = ["selected_seed_id"]
    coherence = score_coherence(required_evidence, evidence_items, context)
    signals = _build_signals(dominant_field_id, evidence_items)
    suppressed = [SuppressedField(signal.field_id, signal.suppression_reason or "not_selected") for signal in signals if signal.field_id != dominant_field_id]
    trace = build_field_why_trace(dominant_field_id, reason_tokens, evidence_items, REQUIRED_NOT_PROVEN)
    dominant = DominantField(dominant_field_id, bound_score(coherence.route_confidence), REVIEW_AXIS_IDS, trace.trace_id)
    recommendation = f"route_hint:{dominant_field_id}"
    return FieldSelection(dominant, suppressed, coherence, REVIEW_AXIS_IDS, trace, recommendation)


def select_field_route_from_seed_route(seed_route) -> FieldSelection:
    return select_field_route(_seed_route_to_context(seed_route))

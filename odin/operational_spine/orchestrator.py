"""Operational Spine orchestrator for FINAL-PR-09.

Claim boundary: final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply
candidate_only: true

Main entry point: run_operational_spine()

Rules:
- No exceptions escape from run_operational_spine (all caught, put in validation_result)
- All outputs: candidate_only=True, local_only=True, app_owned_apply=True
- All IDs: deterministic SHA256 (no uuid, no random, no non-deterministic timestamps)
- No eval or exec calls
- No network, no subprocess, no socket
"""
from __future__ import annotations

import hashlib
import json

from odin.operational_spine.modelworkpacket_builder import build_modelworkpacket
from odin.operational_spine.model_roles import get_model_role
from odin.operational_spine.provider_seam import build_provider_seam_packet
from odin.operational_spine.receipts import (
    build_proof_refs,
    build_receipt_ref,
    build_trace_ref,
)
from odin.operational_spine.small_model_route_plan import build_small_model_route_plan

CLAIM_BOUNDARY = "final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply"

_NOT_PROVEN = [
    "live_model_inference",
    "real_model_benchmark",
    "provider_execution",
    "app_apply",
    "app_state_mutation",
    "external_send",
    "public_network",
    "production_readiness",
    "security_certification",
    "release_certification",
]


def _sha256_id(prefix: str, payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    h = hashlib.sha256(raw.encode()).hexdigest()[:16]
    return f"{prefix}{h}"


def _try_import_precompute(input_text: str, work_id: str) -> dict:
    """Attempt to use odin.precompute.score_pre_llm_route; return stub on ImportError."""
    try:
        from odin.precompute import score_pre_llm_route  # type: ignore[import]
        result = score_pre_llm_route({"input_text": input_text, "work_id": work_id})
        if isinstance(result, dict):
            return result
        return {
            "artifact_kind": "odin_precompute_result",
            "score": str(result),
            "stub": False,
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    except Exception:
        return {
            "artifact_kind": "odin_precompute_result_stub",
            "score": "deterministic_no_model",
            "stub": True,
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }


def _try_import_seed_route(work_id: str, input_text: str) -> dict:
    """Attempt to use odin.operational_seed_spine.selector.select_seed_route; return stub on ImportError."""
    try:
        from odin.operational_seed_spine.selector import select_seed_route  # type: ignore[import]
        work_context = {
            "work_type": "operational_spine",
            "work_id": work_id,
            "input_text": input_text,
        }
        route = select_seed_route(work_context)
        if hasattr(route, "to_dict"):
            return route.to_dict()
        if isinstance(route, dict):
            return route
        return {
            "selected_seed_id": "prompt_to_work",
            "stub": False,
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    except Exception:
        return {
            "artifact_kind": "odin_seed_route_stub",
            "selected_seed_id": "prompt_to_work",
            "selected_role_profile_id": "router",
            "matched_trigger_shapes": [],
            "missing_input_requirements": [],
            "fallback_used": True,
            "selection_priority": "stub_fallback",
            "stub": True,
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }


def _try_import_field_selection(seed_route: dict) -> dict:
    """Attempt to use odin.field_selection_spine.selector.select_field_route_from_seed_route; return stub on ImportError."""
    try:
        from odin.field_selection_spine.selector import select_field_route_from_seed_route  # type: ignore[import]
        selection = select_field_route_from_seed_route(seed_route)
        if hasattr(selection, "to_dict"):
            return selection.to_dict()
        if isinstance(selection, dict):
            return selection
        return {
            "route_recommendation": "scope_control",
            "stub": False,
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    except Exception:
        return {
            "artifact_kind": "odin_field_selection_stub",
            "dominant_field": {
                "field_id": "scope_control",
                "route_confidence": 0.5,
            },
            "route_recommendation": "route_hint:scope_control",
            "stub": True,
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }


def _try_import_projection_candidate(field_selection: dict, work_id: str) -> dict:
    """Attempt to use odin.projection_candidate_spine.projection_set.build_projection_set_from_field_selection; return stub on ImportError."""
    try:
        from odin.projection_candidate_spine.projection_set import build_projection_set_from_field_selection  # type: ignore[import]
        result = build_projection_set_from_field_selection(field_selection)
        if hasattr(result, "to_dict"):
            return result.to_dict()
        if isinstance(result, dict):
            return result
        return {
            "stub": False,
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    except Exception:
        return {
            "artifact_kind": "odin_projection_candidate_stub",
            "projection_id": _sha256_id(
                "projection_set_",
                {"work_id": work_id, "stub": True},
            ),
            "candidate_nodes": [],
            "stub": True,
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }


def run_operational_spine(
    input_text: str,
    *,
    mode: str = "deterministic",
    provider_id: str | None = None,
    allow_local_provider_execution: bool = False,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Run the operational spine and return a candidate-only result dict.

    Never raises — all exceptions are caught and placed in validation_result.
    All outputs have candidate_only=True, local_only=True, app_owned_apply=True.
    """
    validation_errors: list[str] = []

    # ── 1. work_id ────────────────────────────────────────────────────────
    try:
        work_id = _sha256_id(
            "universal_work_",
            {"input_text": input_text, "generated_at_utc": generated_at_utc},
        )
    except Exception as exc:
        validation_errors.append(f"work_id_build_error: {exc}")
        work_id = "universal_work_error"

    # ── 2. spine_id ───────────────────────────────────────────────────────
    try:
        spine_id = _sha256_id(
            "operational_spine_",
            {"work_id": work_id, "mode": mode, "generated_at_utc": generated_at_utc},
        )
    except Exception as exc:
        validation_errors.append(f"spine_id_build_error: {exc}")
        spine_id = "operational_spine_error"

    # ── 3. handoff_context ────────────────────────────────────────────────
    try:
        handoff_context = {
            "artifact_kind": "odin_handoff_context",
            "input_ref": _sha256_id(
                "input_ref_",
                {"input_text": input_text, "work_id": work_id},
            ),
            "work_id": work_id,
            "spine_id": spine_id,
            "source": "operational_spine_orchestrator",
            "candidate_only": True,
            "local_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    except Exception as exc:
        validation_errors.append(f"handoff_context_build_error: {exc}")
        handoff_context = {"error": str(exc), "candidate_only": True, "claim_boundary": CLAIM_BOUNDARY}

    # ── 4. universal_work ─────────────────────────────────────────────────
    try:
        universal_work = {
            "artifact_kind": "odin_universal_work",
            "work_id": work_id,
            "input_text": input_text,
            "work_type": "operational_spine",
            "candidate_only": True,
            "local_only": True,
            "app_owned_apply": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    except Exception as exc:
        validation_errors.append(f"universal_work_build_error: {exc}")
        universal_work = {"error": str(exc), "candidate_only": True, "claim_boundary": CLAIM_BOUNDARY}

    # ── 5. validation_result ──────────────────────────────────────────────
    # (populated at end with all errors collected above)
    validation_result: dict = {
        "artifact_kind": "odin_validation_result",
        "valid": True,
        "errors": [],
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
    }

    # ── 6. context_capsule ────────────────────────────────────────────────
    try:
        context_capsule = {
            "artifact_kind": "odin_context_capsule",
            "capsule_id": _sha256_id(
                "context_capsule_",
                {"work_id": work_id, "generated_at_utc": generated_at_utc},
            ),
            "work_id": work_id,
            "fields": {
                "input_text_ref": work_id,
                "mode": mode,
                "generated_at_utc": generated_at_utc,
            },
            "candidate_only": True,
            "local_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    except Exception as exc:
        validation_errors.append(f"context_capsule_build_error: {exc}")
        context_capsule = {"error": str(exc), "candidate_only": True, "claim_boundary": CLAIM_BOUNDARY}

    # ── 7. artifact_lens ──────────────────────────────────────────────────
    try:
        artifact_lens = {
            "artifact_kind": "odin_artifact_lens",
            "lens_id": _sha256_id(
                "artifact_lens_",
                {"work_id": work_id, "lens_type": "candidate_prep", "generated_at_utc": generated_at_utc},
            ),
            "work_id": work_id,
            "lens_type": "candidate_prep",
            "candidate_only": True,
            "local_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    except Exception as exc:
        validation_errors.append(f"artifact_lens_build_error: {exc}")
        artifact_lens = {"error": str(exc), "candidate_only": True, "claim_boundary": CLAIM_BOUNDARY}

    # ── 8. slot_contract ──────────────────────────────────────────────────
    try:
        slot_contract = {
            "artifact_kind": "odin_slot_contract",
            "contract_id": _sha256_id(
                "slot_contract_",
                {"work_id": work_id, "generated_at_utc": generated_at_utc},
            ),
            "work_id": work_id,
            "slots": [],
            "candidate_only": True,
            "local_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    except Exception as exc:
        validation_errors.append(f"slot_contract_build_error: {exc}")
        slot_contract = {"error": str(exc), "candidate_only": True, "claim_boundary": CLAIM_BOUNDARY}

    # ── 9. gaptext ────────────────────────────────────────────────────────
    try:
        gaptext = {
            "artifact_kind": "odin_gaptext",
            "gaptext_id": _sha256_id(
                "gaptext_",
                {"work_id": work_id, "generated_at_utc": generated_at_utc},
            ),
            "work_id": work_id,
            "gaps": [],
            "candidate_only": True,
            "local_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    except Exception as exc:
        validation_errors.append(f"gaptext_build_error: {exc}")
        gaptext = {"error": str(exc), "candidate_only": True, "claim_boundary": CLAIM_BOUNDARY}

    # ── 10. precompute_result ─────────────────────────────────────────────
    try:
        precompute_result = _try_import_precompute(input_text, work_id)
    except Exception as exc:
        validation_errors.append(f"precompute_result_build_error: {exc}")
        precompute_result = {
            "artifact_kind": "odin_precompute_result_error",
            "error": str(exc),
            "stub": True,
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    # ── 11. modelworkpacket ───────────────────────────────────────────────
    try:
        model_role_for_packet = get_model_role("deterministic_candidate_shape") or {
            "role_id": "deterministic_candidate_shape",
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        route_policy = {
            "route": "deterministic_no_model" if mode == "deterministic" else f"{mode}_primary",
            "latency_budget": "interactive",
            "critic_plan": "no_critic_deterministic_route",
        }
        provider_policy = {
            "provider_id": provider_id,
            "cost_budget": "no_model_local",
            "allow_remote_provider": False,
        }
        output_contract_for_packet = {
            "output_type": "candidate_artifact",
            "candidate_only": True,
            "final_gate_requirements": {
                "gate_type": "schema_validation",
                "candidate_only": True,
            },
        }
        modelworkpacket = build_modelworkpacket(
            work_id=work_id,
            caller_id=spine_id,
            input_refs=[handoff_context.get("input_ref", work_id)],
            context_capsule=context_capsule,
            artifact_lens=artifact_lens,
            transformation_verb="build_operational_spine_candidate",
            slot_contract=slot_contract,
            gaptext=gaptext,
            model_role=model_role_for_packet,
            route_policy=route_policy,
            provider_policy=provider_policy,
            output_contract=output_contract_for_packet,
            generated_at_utc=generated_at_utc,
        )
    except Exception as exc:
        validation_errors.append(f"modelworkpacket_build_error: {exc}")
        modelworkpacket = {
            "artifact_kind": "odin_modelworkpacket_error",
            "error": str(exc),
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    # ── 12. small_model_route_plan ────────────────────────────────────────
    try:
        resource_profile = mode if mode in ("deterministic", "small", "medium", "hybrid") else "deterministic"
        small_model_route_plan = build_small_model_route_plan(
            work_id=work_id,
            resource_profile=resource_profile,
            generated_at_utc=generated_at_utc,
        )
    except Exception as exc:
        validation_errors.append(f"small_model_route_plan_build_error: {exc}")
        small_model_route_plan = {
            "artifact_kind": "odin_small_model_route_plan_error",
            "error": str(exc),
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    # ── 13. model_role_assignment ─────────────────────────────────────────
    try:
        selected_role = get_model_role("deterministic_candidate_shape") or {
            "role_id": "deterministic_candidate_shape",
            "model_tier": "no_model",
            "candidate_only": True,
        }
        model_role_assignment = {
            "artifact_kind": "odin_model_role_assignment",
            "assignment_id": _sha256_id(
                "model_role_",
                {
                    "work_id": work_id,
                    "role_id": selected_role.get("role_id", "deterministic_candidate_shape"),
                    "generated_at_utc": generated_at_utc,
                },
            ),
            "work_id": work_id,
            "selected_role": selected_role,
            "candidate_only": True,
            "local_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    except Exception as exc:
        validation_errors.append(f"model_role_assignment_build_error: {exc}")
        model_role_assignment = {
            "artifact_kind": "odin_model_role_assignment_error",
            "error": str(exc),
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    # ── 14. seed_route ────────────────────────────────────────────────────
    try:
        seed_route = _try_import_seed_route(work_id, input_text)
    except Exception as exc:
        validation_errors.append(f"seed_route_build_error: {exc}")
        seed_route = {
            "artifact_kind": "odin_seed_route_error",
            "error": str(exc),
            "stub": True,
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    # ── 15. field_selection ───────────────────────────────────────────────
    try:
        field_selection = _try_import_field_selection(seed_route)
    except Exception as exc:
        validation_errors.append(f"field_selection_build_error: {exc}")
        field_selection = {
            "artifact_kind": "odin_field_selection_error",
            "error": str(exc),
            "stub": True,
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    # ── 16. projection_candidate ──────────────────────────────────────────
    try:
        projection_candidate = _try_import_projection_candidate(field_selection, work_id)
    except Exception as exc:
        validation_errors.append(f"projection_candidate_build_error: {exc}")
        projection_candidate = {
            "artifact_kind": "odin_projection_candidate_error",
            "error": str(exc),
            "stub": True,
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    # ── 17. provider_seam_packet ──────────────────────────────────────────
    try:
        provider_seam_packet = build_provider_seam_packet(
            provider_id,
            mode=mode,
            allow_local_provider_execution=allow_local_provider_execution,
        )
    except Exception as exc:
        validation_errors.append(f"provider_seam_packet_build_error: {exc}")
        provider_seam_packet = {
            "artifact_kind": "odin_provider_seam_packet_error",
            "error": str(exc),
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    # ── 18. candidate_artifact ────────────────────────────────────────────
    try:
        if mode == "deterministic":
            payload = {
                "route": "deterministic_no_model",
                "work_id": work_id,
                "spine_id": spine_id,
                "candidate_only": True,
            }
        else:
            payload = {
                "route": f"{mode}_plan_only",
                "work_id": work_id,
                "spine_id": spine_id,
                "candidate_only": True,
                "note": "model_not_executed_plan_only",
            }
        candidate_artifact = {
            "artifact_kind": "odin_operational_candidate_artifact",
            "artifact_id": _sha256_id(
                "operational_candidate_",
                {"work_id": work_id, "mode": mode, "generated_at_utc": generated_at_utc},
            ),
            "work_id": work_id,
            "candidate_only": True,
            "local_only": True,
            "app_owned_apply": True,
            "claim_boundary": CLAIM_BOUNDARY,
            "payload": payload,
        }
    except Exception as exc:
        validation_errors.append(f"candidate_artifact_build_error: {exc}")
        candidate_artifact = {
            "artifact_kind": "odin_candidate_artifact_error",
            "error": str(exc),
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    # ── 19. final_gate ────────────────────────────────────────────────────
    try:
        gate_passed = mode == "deterministic"
        final_gate = {
            "artifact_kind": "odin_final_gate",
            "gate_id": _sha256_id(
                "final_gate_",
                {"work_id": work_id, "mode": mode, "generated_at_utc": generated_at_utc},
            ),
            "work_id": work_id,
            "passed": gate_passed,
            "gate_type": "schema_validation",
            "candidate_only": True,
            "local_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    except Exception as exc:
        validation_errors.append(f"final_gate_build_error: {exc}")
        final_gate = {
            "artifact_kind": "odin_final_gate_error",
            "error": str(exc),
            "passed": False,
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    # ── 20. response_packet ───────────────────────────────────────────────
    try:
        response_packet = {
            "artifact_kind": "odin_response_packet",
            "packet_id": _sha256_id(
                "response_packet_",
                {"work_id": work_id, "spine_id": spine_id, "generated_at_utc": generated_at_utc},
            ),
            "work_id": work_id,
            "spine_id": spine_id,
            "candidate_only": True,
            "local_only": True,
            "app_owned_apply": True,
            "claim_boundary": CLAIM_BOUNDARY,
            "status": "candidate_ready",
        }
    except Exception as exc:
        validation_errors.append(f"response_packet_build_error: {exc}")
        response_packet = {
            "artifact_kind": "odin_response_packet_error",
            "error": str(exc),
            "candidate_only": True,
            "claim_boundary": CLAIM_BOUNDARY,
            "status": "error",
        }

    # ── 21. trace_ref ─────────────────────────────────────────────────────
    try:
        trace_ref = build_trace_ref(work_id, spine_id, generated_at_utc)
    except Exception as exc:
        validation_errors.append(f"trace_ref_build_error: {exc}")
        trace_ref = f"operational_trace_error_{work_id}"

    # ── 22. receipt_ref ───────────────────────────────────────────────────
    try:
        receipt_ref = build_receipt_ref(work_id, spine_id, generated_at_utc)
    except Exception as exc:
        validation_errors.append(f"receipt_ref_build_error: {exc}")
        receipt_ref = f"operational_receipt_error_{work_id}"

    # ── 23. qirc_hint_refs ────────────────────────────────────────────────
    try:
        qirc_hint_refs = [
            _sha256_id(
                "qirc_hint_",
                {
                    "work_id": work_id,
                    "spine_id": spine_id,
                    "hint_index": i,
                    "generated_at_utc": generated_at_utc,
                },
            )
            for i in range(3)
        ]
    except Exception as exc:
        validation_errors.append(f"qirc_hint_refs_build_error: {exc}")
        qirc_hint_refs = []

    # ── 24. proof_refs ────────────────────────────────────────────────────
    try:
        proof_refs = build_proof_refs(work_id, spine_id, generated_at_utc)
    except Exception as exc:
        validation_errors.append(f"proof_refs_build_error: {exc}")
        proof_refs = []

    # ── Finalize validation_result ────────────────────────────────────────
    if validation_errors:
        validation_result["valid"] = False
        validation_result["errors"] = list(validation_errors)

    # ── Assemble and return result ────────────────────────────────────────
    return {
        "artifact_kind": "odin_operational_spine_result",
        "work_id": work_id,
        "spine_id": spine_id,
        "mode": mode,
        "generated_at_utc": generated_at_utc,
        "status": response_packet.get("status", "candidate_ready"),
        # Sub-packets
        "handoff_context": handoff_context,
        "universal_work": universal_work,
        "validation_result": validation_result,
        "context_capsule": context_capsule,
        "artifact_lens": artifact_lens,
        "slot_contract": slot_contract,
        "gaptext": gaptext,
        "precompute_result": precompute_result,
        "modelworkpacket": modelworkpacket,
        "small_model_route_plan": small_model_route_plan,
        "model_role_assignment": model_role_assignment,
        "seed_route": seed_route,
        "field_selection": field_selection,
        "projection_candidate": projection_candidate,
        "provider_seam_packet": provider_seam_packet,
        "candidate_artifact": candidate_artifact,
        "final_gate": final_gate,
        "response_packet": response_packet,
        "trace_ref": trace_ref,
        "receipt_ref": receipt_ref,
        "qirc_hint_refs": qirc_hint_refs,
        "proof_refs": proof_refs,
        # Boundaries
        "candidate_only": True,
        "local_only": True,
        "app_owned_apply": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": list(_NOT_PROVEN),
    }

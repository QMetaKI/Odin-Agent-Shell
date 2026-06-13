"""Critic cascade — FINAL-PR-11.

Runs deterministic critic, optionally followed by model critic via provider receipt harness.
Critic cascade is advisory. Not authority. Cannot apply. Cannot certify quality.
"""
from __future__ import annotations

from odin.critic_runtime.critic_packet import CLAIM_BOUNDARY, _NOT_PROVEN
from odin.critic_runtime.deterministic_critic import run_deterministic_critic


def run_critic_cascade(
    candidate: dict,
    *,
    include_model_critic: bool = False,
    allow_local_provider_execution: bool = False,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Run critic cascade: deterministic first, then optional model critic.

    Model critic only if include_model_critic=True AND allow_local_provider_execution=True.
    If model critic unavailable, cascade continues with deterministic only.
    Cascade is advisory. Not authority. Cannot certify quality.
    """
    deterministic_result = run_deterministic_critic(candidate, generated_at_utc=generated_at_utc)
    stages: list[dict] = [{"stage": "deterministic", "result": deterministic_result}]

    model_critic_result = None
    if include_model_critic and allow_local_provider_execution:
        # Attempt model critic via provider receipt harness
        try:
            from odin.local_provider_receipts.receipt import run_local_provider_receipt
            prompt = (
                f"Critic review of candidate boundary:\n"
                f"claim_boundary={candidate.get('claim_boundary')}\n"
                f"candidate_only={candidate.get('candidate_only')}\n"
                f"not_proven={candidate.get('not_proven')}\n"
                "Return: pass/fail and one reason."
            )
            provider_receipt = run_local_provider_receipt(
                "ollama_candidate",
                prompt,
                allow_local_provider_execution=allow_local_provider_execution,
                generated_at_utc=generated_at_utc,
            )
            model_critic_result = {
                "stage": "model_critic",
                "provider_receipt_status": provider_receipt.get("status"),
                "execution_performed": provider_receipt.get("execution_performed", False),
                "evidence_class": provider_receipt.get("evidence_class", "structural_evidence"),
                "not_authority": True,
                "model_critic_is_advisory": True,
                "note": "Model critic output is advisory. Critic is not final authority.",
            }
        except Exception as exc:
            model_critic_result = {
                "stage": "model_critic",
                "status": "error",
                "error": str(exc),
                "execution_performed": False,
                "not_authority": True,
            }
        stages.append(model_critic_result)
    elif include_model_critic:
        stages.append({
            "stage": "model_critic",
            "status": "skipped_execution_not_allowed",
            "execution_performed": False,
            "not_authority": True,
        })

    overall_errors = deterministic_result.get("errors", [])
    overall_recommendation = "pass" if not overall_errors else "fail"

    return {
        "artifact_kind": "odin_critic_cascade_result",
        "candidate_only": True,
        "local_only": True,
        "app_owned_apply": True,
        "app_apply": False,
        "external_send": False,
        "public_network": False,
        "not_authority": True,
        "final_gate_required": True,
        "cascade_stages": stages,
        "overall_recommendation": overall_recommendation,
        "overall_errors": overall_errors,
        "evidence_class": "structural_evidence",
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": list(_NOT_PROVEN),
        "generated_at_utc": generated_at_utc,
        "cascade_advisory_note": (
            "This cascade result is advisory. "
            "Critic cannot certify quality, apply, or send. "
            "App owns apply authority."
        ),
    }

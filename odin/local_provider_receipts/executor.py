"""Optional local provider executor — FINAL-PR-11.

Execution is disabled by default. Requires:
- allow_local_provider_execution=True
- ODIN_ENABLE_LOCAL_PROVIDER_EXECUTION=1 environment variable
- provider_id in EXECUTABLE_PROVIDER_IDS
- timeout_seconds <= 60
- max_input_chars <= 8000

Subprocess runs with shell disabled. Never contacts remote URLs. Never reads API keys.
Never sends externally. Never mutates app state.
"""
from __future__ import annotations

import hashlib
import os

from odin.local_provider_receipts.provider_ids import (
    CLAIM_BOUNDARY,
    EXECUTABLE_PROVIDER_IDS,
    NOT_PROVEN_BASE,
    RECOGNIZED_PROVIDER_IDS,
)

_NOT_PROVEN_EXEC = list(NOT_PROVEN_BASE) + [
    "general_live_model_inference",
    "provider_execution_without_explicit_receipt",
]

_NOT_PROVEN_SCOPED = [
    "production_readiness",
    "security_certification",
    "release_certification",
    "real_model_benchmark",
    "model_quality_superiority",
    "app_apply",
    "app_state_mutation",
    "external_send",
    "public_network",
    "general_live_model_inference",
]


def _execution_gate(
    provider_id: str,
    allow_local_provider_execution: bool,
    timeout_seconds: int,
    max_input_chars: int,
) -> tuple[bool, str]:
    """Return (allowed, reason). All conditions must pass."""
    if not allow_local_provider_execution:
        return False, "allow_local_provider_execution_flag_not_set"
    env_flag = os.environ.get("ODIN_ENABLE_LOCAL_PROVIDER_EXECUTION", "0")
    if env_flag != "1":
        return False, "ODIN_ENABLE_LOCAL_PROVIDER_EXECUTION_env_not_set"
    if provider_id not in EXECUTABLE_PROVIDER_IDS:
        return False, f"provider_id_not_in_executable_set: {provider_id}"
    if timeout_seconds > 60:
        return False, f"timeout_seconds_exceeds_60: {timeout_seconds}"
    if max_input_chars > 8000:
        return False, f"max_input_chars_exceeds_8000: {max_input_chars}"
    return True, "all_gates_passed"


def run_executor(
    provider_id: str,
    prompt: str,
    *,
    allow_local_provider_execution: bool = False,
    model_hint: str | None = None,
    timeout_seconds: int = 30,
    max_input_chars: int = 4000,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    """Attempt optional local provider execution.

    Returns a receipt dict. Never raises. Subprocess runs with shell disabled.
    Never contacts remote URLs. No API keys. No public network.
    """
    clamped_chars = min(max_input_chars, 8000)
    clamped_timeout = min(timeout_seconds, 60)
    truncated = prompt[:clamped_chars]
    input_hash = hashlib.sha256(truncated.encode()).hexdigest()[:32]

    allowed, gate_reason = _execution_gate(
        provider_id, allow_local_provider_execution, clamped_timeout, clamped_chars
    )

    if not allowed:
        return {
            "artifact_kind": "odin_provider_execution_receipt",
            "status": "execution_not_enabled",
            "gate_reason": gate_reason,
            "provider_id": provider_id,
            "input_hash": input_hash,
            "execution_allowed": False,
            "execution_performed": False,
            "model_inference": False,
            "provider_execution": False,
            "candidate_only": True,
            "local_only": True,
            "app_owned_apply": True,
            "app_apply": False,
            "external_send": False,
            "public_network": False,
            "evidence_class": "structural_evidence",
            "claim_boundary": CLAIM_BOUNDARY,
            "not_proven": _NOT_PROVEN_EXEC,
            "generated_at_utc": generated_at_utc,
        }

    if provider_id not in RECOGNIZED_PROVIDER_IDS:
        return {
            "artifact_kind": "odin_provider_execution_receipt",
            "status": "provider_not_allowed",
            "provider_id": provider_id,
            "input_hash": input_hash,
            "execution_allowed": False,
            "execution_performed": False,
            "model_inference": False,
            "provider_execution": False,
            "candidate_only": True,
            "local_only": True,
            "app_owned_apply": True,
            "app_apply": False,
            "external_send": False,
            "public_network": False,
            "evidence_class": "structural_evidence",
            "claim_boundary": CLAIM_BOUNDARY,
            "not_proven": _NOT_PROVEN_EXEC,
            "generated_at_utc": generated_at_utc,
        }

    # Attempt actual execution — only reaches here if all gates pass
    return _attempt_provider_execution(
        provider_id=provider_id,
        prompt=truncated,
        input_hash=input_hash,
        model_hint=model_hint,
        timeout_seconds=clamped_timeout,
        generated_at_utc=generated_at_utc,
    )


def _attempt_provider_execution(
    provider_id: str,
    prompt: str,
    input_hash: str,
    model_hint: str | None,
    timeout_seconds: int,
    generated_at_utc: str,
) -> dict:
    """Try subprocess-based local provider execution. Shell disabled. No remote URL."""
    import subprocess

    if provider_id == "ollama_candidate":
        cmd = ["ollama", "run", model_hint or "llama3", prompt]
    elif provider_id == "llama_cpp_candidate":
        cmd = ["llama-cli", "--prompt", prompt, "-n", "64"]
    else:
        return _unavailable_receipt(provider_id, input_hash, "unrecognized_for_exec", generated_at_utc)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            shell=False,  # required: no shell execution
        )
    except FileNotFoundError:
        return _unavailable_receipt(provider_id, input_hash, "provider_binary_not_found", generated_at_utc)
    except subprocess.TimeoutExpired:
        return _unavailable_receipt(provider_id, input_hash, "provider_timeout", generated_at_utc)
    except Exception as exc:
        return _unavailable_receipt(provider_id, input_hash, f"provider_error: {exc}", generated_at_utc)

    if result.returncode != 0:
        return _unavailable_receipt(
            provider_id, input_hash, f"provider_nonzero_exit: {result.returncode}", generated_at_utc
        )

    output = result.stdout.strip()
    output_hash = hashlib.sha256(output.encode()).hexdigest()[:32]

    return {
        "artifact_kind": "odin_provider_execution_receipt",
        "status": "scoped_local_provider_receipt",
        "provider_id": provider_id,
        "input_hash": input_hash,
        "output_hash": output_hash,
        "model_hint": model_hint,
        "timeout_seconds": timeout_seconds,
        "execution_allowed": True,
        "execution_performed": True,
        "model_inference": True,
        "provider_execution": True,
        "candidate_only": True,
        "local_only": True,
        "app_owned_apply": True,
        "app_apply": False,
        "external_send": False,
        "public_network": False,
        "evidence_class": "host_scoped_local_receipt",
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": _NOT_PROVEN_SCOPED,
        "generated_at_utc": generated_at_utc,
        "scope_note": (
            "This receipt is host-scoped. "
            "It does not generalize to other hosts. "
            "It does not prove model quality, production readiness, or security."
        ),
    }


def _unavailable_receipt(
    provider_id: str, input_hash: str, reason: str, generated_at_utc: str
) -> dict:
    return {
        "artifact_kind": "odin_provider_execution_receipt",
        "status": "provider_unavailable",
        "unavailable_reason": reason,
        "provider_id": provider_id,
        "input_hash": input_hash,
        "execution_allowed": True,
        "execution_performed": False,
        "model_inference": False,
        "provider_execution": False,
        "candidate_only": True,
        "local_only": True,
        "app_owned_apply": True,
        "app_apply": False,
        "external_send": False,
        "public_network": False,
        "evidence_class": "structural_evidence",
        "claim_boundary": CLAIM_BOUNDARY,
        "not_proven": list(NOT_PROVEN_BASE),
        "generated_at_utc": generated_at_utc,
    }

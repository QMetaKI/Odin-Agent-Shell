"""Provider probe — safe readiness detection without model execution — FINAL-PR-04.

Claim boundary: provider_probe_readiness_not_model_execution
candidate_only: true
local_only: true

This module only probes binary availability. It does NOT run models, chat,
generate, embed, or read API keys.
"""
from __future__ import annotations

import shutil
import subprocess

from .policy import PROVIDER_POLICIES, CLAIM_BOUNDARY
from .registry import REQUIRED_PROVIDER_IDS

_OLLAMA_BINARY_CANDIDATES = ["ollama"]
_LLAMA_BINARY_CANDIDATES = ["llama-cli", "llama", "llama.cpp"]

# Subprocess allowlist: only --version or --help, timeout 2s, no model args
_SUBPROCESS_TIMEOUT = 2


def _safe_version_check(binary: str, args: list[str] | None = None) -> tuple[bool, str]:
    """Run binary --version with strict safety constraints. Returns (success, output)."""
    cmd = [binary] + (args or ["--version"])
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=_SUBPROCESS_TIMEOUT,
        )
        return True, (result.stdout or result.stderr or "").strip()[:200]
    except FileNotFoundError:
        return False, "not_found"
    except subprocess.TimeoutExpired:
        return False, "timeout"
    except Exception as exc:
        return False, f"error:{exc}"


def _probe_none() -> dict:
    return {
        "provider_id": "none",
        "status": "available",
        "probe_allowed": True,
        "execution_allowed": False,
        "candidate_only": True,
        "local_only": True,
        "remote": False,
        "requires_api_key": False,
        "binary_found": None,
        "version_checked": False,
        "model_inference": False,
        "provider_execution": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _probe_mock() -> dict:
    return {
        "provider_id": "mock",
        "status": "available",
        "probe_allowed": True,
        "execution_allowed": False,
        "candidate_only": True,
        "local_only": True,
        "remote": False,
        "requires_api_key": False,
        "binary_found": None,
        "version_checked": False,
        "model_inference": False,
        "provider_execution": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _probe_ollama_candidate() -> dict:
    binary = shutil.which("ollama")
    if binary is None:
        return {
            "provider_id": "ollama_candidate",
            "status": "not_found",
            "probe_allowed": True,
            "execution_allowed": False,
            "candidate_only": True,
            "local_only": True,
            "remote": False,
            "requires_api_key": False,
            "binary_found": False,
            "version_checked": False,
            "model_inference": False,
            "provider_execution": False,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    # Binary exists — safe version check only
    version_ok, version_str = _safe_version_check("ollama", ["--version"])
    return {
        "provider_id": "ollama_candidate",
        "status": "available",
        "probe_allowed": True,
        "execution_allowed": False,
        "candidate_only": True,
        "local_only": True,
        "remote": False,
        "requires_api_key": False,
        "binary_found": True,
        "binary_path": binary,
        "version_checked": version_ok,
        "version_output": version_str,
        "model_inference": False,
        "provider_execution": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _probe_llama_cpp_candidate() -> dict:
    binary = None
    binary_name = None
    for candidate in _LLAMA_BINARY_CANDIDATES:
        found = shutil.which(candidate)
        if found:
            binary = found
            binary_name = candidate
            break

    if binary is None:
        return {
            "provider_id": "llama_cpp_candidate",
            "status": "not_found",
            "probe_allowed": True,
            "execution_allowed": False,
            "candidate_only": True,
            "local_only": True,
            "remote": False,
            "requires_api_key": False,
            "binary_found": False,
            "version_checked": False,
            "model_inference": False,
            "provider_execution": False,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    version_ok, version_str = _safe_version_check(binary_name or binary, ["--version"])
    return {
        "provider_id": "llama_cpp_candidate",
        "status": "available",
        "probe_allowed": True,
        "execution_allowed": False,
        "candidate_only": True,
        "local_only": True,
        "remote": False,
        "requires_api_key": False,
        "binary_found": True,
        "binary_path": binary,
        "binary_name": binary_name,
        "version_checked": version_ok,
        "version_output": version_str,
        "model_inference": False,
        "provider_execution": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }


_PROBE_DISPATCH = {
    "none": _probe_none,
    "mock": _probe_mock,
    "ollama_candidate": _probe_ollama_candidate,
    "llama_cpp_candidate": _probe_llama_cpp_candidate,
}


def list_provider_candidates() -> list[str]:
    return list(PROVIDER_POLICIES.keys())


def probe_provider(provider_id: str) -> dict:
    policy = PROVIDER_POLICIES.get(provider_id)
    if policy is None:
        return {
            "provider_id": provider_id,
            "status": "unknown",
            "probe_allowed": False,
            "execution_allowed": False,
            "candidate_only": True,
            "local_only": True,
            "model_inference": False,
            "provider_execution": False,
            "claim_boundary": CLAIM_BOUNDARY,
            "error": f"unknown provider_id: {provider_id}",
        }
    if not policy.probe_allowed:
        return {
            "provider_id": provider_id,
            "status": "blocked",
            "probe_allowed": False,
            "execution_allowed": False,
            "candidate_only": True,
            "local_only": True,
            "model_inference": False,
            "provider_execution": False,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    fn = _PROBE_DISPATCH.get(provider_id)
    if fn is None:
        return {
            "provider_id": provider_id,
            "status": "disabled",
            "probe_allowed": True,
            "execution_allowed": False,
            "candidate_only": True,
            "local_only": True,
            "model_inference": False,
            "provider_execution": False,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    return fn()


def probe_all_providers() -> list[dict]:
    results = []
    for pid in REQUIRED_PROVIDER_IDS:
        result = probe_provider(pid)
        results.append(result)
    return results


def build_provider_status_packet() -> dict:
    results = probe_all_providers()
    return {
        "artifact_kind": "odin_provider_status_packet",
        "candidate_only": True,
        "local_only": True,
        "provider_execution": False,
        "model_inference": False,
        "api_key_reads": False,
        "external_network": False,
        "providers": results,
        "claim_boundary": CLAIM_BOUNDARY,
    }

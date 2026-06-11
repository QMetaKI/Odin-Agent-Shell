"""Generic App Bridge — Golden Harness.

Claim boundary: generic_app_bridge_golden_harness_candidate_only_local_only_no_apply_no_external_send

Runs both neutral generic bridge examples as pure local fixture flows.
Deterministic, local-only, fixture-safe, neutral, claim-bound, repeatable.
No network. No provider. No state mutation. No concrete app names.
Host app owns apply, state, and external send.

Output JSON includes:
  artifact_kind, status, candidate_only, local_only, neutral_examples,
  host_app_owns_apply, host_app_owns_state, host_app_owns_external_send,
  odin_app_apply, odin_external_send, host_state_mutated, external_send_performed,
  concrete_app_names_present, proof_boundaries, known_non_proofs
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent

sys.path.insert(0, str(_HERE))

import generic_bridge_flow_one as flow_one
import generic_bridge_flow_two as flow_two

CANDIDATE_ONLY = True
LOCAL_ONLY = True
HOST_APP_OWNS_APPLY = True
HOST_APP_OWNS_STATE = True
HOST_APP_OWNS_EXTERNAL_SEND = True

PROOF_BOUNDARIES = [
    "not_production_readiness_certification",
    "not_security_certification",
    "not_hosted_bridge_proof",
    "not_public_gateway_proof",
    "not_specific_external_app_integration_proof",
    "not_signed_distribution_proof",
    "not_windows_service_tray_installer_proof",
    "not_app_apply_proof",
    "not_host_state_mutation_proof",
    "not_external_send_authority_proof",
    "not_provider_execution_proof",
    "not_live_model_inference_proof",
    "not_model_quality_proof",
    "candidate_artifact_not_applied_truth",
    "host_app_owns_apply_state_external_send",
]

KNOWN_NON_PROOFS = [
    "production_readiness",
    "security_certification",
    "signed_distribution",
    "windows_service_tray_installer",
    "hosted_bridge",
    "public_network_api",
    "specific_external_app_integration",
    "live_model_inference",
    "model_quality",
    "provider_execution",
    "real_app_state_mutation",
    "external_send_authority",
]


def run_flow_one() -> dict:
    """Run Generic Bridge Flow One. Returns its receipt."""
    return flow_one.run()


def run_flow_two() -> dict:
    """Run Generic Bridge Flow Two. Returns its receipt."""
    return flow_two.run()


def run() -> dict:
    """Run the golden harness — both flows, local-only, deterministic.

    Returns a harness receipt JSON dict.
    """
    receipt_one = run_flow_one()
    receipt_two = run_flow_two()

    flow_one_ok = receipt_one.get("status") == "ok"
    flow_two_ok = receipt_two.get("status") == "ok"
    all_ok = flow_one_ok and flow_two_ok

    return {
        "artifact_kind": "generic_app_bridge_golden_harness_receipt",
        "status": "ok" if all_ok else "partial",
        "candidate_only": CANDIDATE_ONLY,
        "local_only": LOCAL_ONLY,
        "neutral_examples": 2,
        "host_app_owns_apply": HOST_APP_OWNS_APPLY,
        "host_app_owns_state": HOST_APP_OWNS_STATE,
        "host_app_owns_external_send": HOST_APP_OWNS_EXTERNAL_SEND,
        "odin_app_apply": False,
        "odin_external_send": False,
        "host_state_mutated": False,
        "external_send_performed": False,
        "concrete_app_names_present": False,
        "flow_one_ok": flow_one_ok,
        "flow_two_ok": flow_two_ok,
        "proof_boundaries": PROOF_BOUNDARIES,
        "known_non_proofs": KNOWN_NON_PROOFS,
        "claim_boundary": "generic_app_bridge_golden_harness_candidate_only_local_only_no_apply_no_external_send",
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2))

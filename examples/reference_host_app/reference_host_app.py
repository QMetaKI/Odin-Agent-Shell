"""Reference Host App — Neutral fake host app demonstrating bridge boundary.

Claim boundary: reference_host_app_candidate_only_no_apply_no_external_send_no_state_mutation

This is a neutral reference host app for generic app bridge demonstration.
It simulates a host app that:
- maintains a local state fixture (no real state mutation)
- receives Candidate Artifacts into a candidate inbox
- inspects candidates using host-owned apply policy
- decides independently whether to use candidates (plan-only demo)
- does NOT apply actual state
- does NOT send externally
- does NOT include concrete app names

This is not a concrete product integration.
This is not a production-certified release.
This does not prove any real app integration.
"""

from __future__ import annotations

import json
from pathlib import Path

_HERE = Path(__file__).resolve().parent

HOST_APP_OWNS_APPLY = True
HOST_APP_OWNS_STATE = True
HOST_APP_OWNS_EXTERNAL_SEND = True

_NEUTRAL_HOST_STATE = {
    "neutral_host_state_fixture": True,
    "state_mutated": False,
    "state_kind": "example_reference_state",
    "note": "This is a fixture state, not real host app state.",
}


def load_host_policy() -> dict:
    """Load the host-owned apply policy from the policy fixture."""
    policy_path = _HERE / "reference_host_policy.json"
    with open(policy_path, encoding="utf-8") as fh:
        return json.load(fh)


def get_neutral_host_state() -> dict:
    """Return the neutral host state fixture.

    This is not real app state. Nothing is mutated.
    """
    return dict(_NEUTRAL_HOST_STATE)


def receive_candidate(candidate_artifact: dict) -> dict:
    """Receive a Candidate Artifact into the host app candidate inbox.

    Does not apply the candidate. Does not mutate state. Does not send externally.
    Host app owns the decision.
    """
    return {
        "candidate_inbox": "received",
        "candidate_kind": candidate_artifact.get("artifact", {}).get("kind", "unknown"),
        "applied_truth": False,
        "state_mutated": False,
        "external_send_performed": False,
        "host_app_owns_apply": True,
        "note": "Candidate received in inbox. Host app has not applied it.",
    }


def inspect_candidate_with_policy(candidate_artifact: dict, policy: dict) -> dict:
    """Inspect a Candidate Artifact against the host-owned apply policy.

    Returns a plan-only inspection record. No state is mutated.
    """
    proof_gaps = candidate_artifact.get("proof_gaps", [])
    proof_boundaries = candidate_artifact.get("proof_boundaries", [])

    return {
        "host_owned_apply_demo": policy.get("host_owned_apply_demo", "plan_only"),
        "candidate_inspected": True,
        "proof_gaps_found": proof_gaps,
        "proof_boundaries_checked": proof_boundaries,
        "policy_allows_apply": False,
        "app_state_mutated": policy.get("app_state_mutated", False),
        "external_send_performed": policy.get("external_send_performed", False),
        "odin_apply_allowed": policy.get("odin_apply_allowed", False),
        "note": (
            "Host app has inspected the candidate. "
            "Policy is plan-only. No state mutation performed. "
            "Host app decides independently."
        ),
    }


def host_owned_apply_decision(inspection: dict) -> dict:
    """Host app makes its own apply decision based on the inspection.

    This is a plan-only demonstration. No state is mutated. No external send.
    """
    return {
        "host_owned_apply_demo": "plan_only",
        "decision": "deferred_to_host_app",
        "applied": False,
        "app_state_mutated": False,
        "external_send_performed": False,
        "candidate_artifact_is_applied_truth": False,
        "note": "Host app owns the apply decision. This demonstration does not apply any state.",
    }


def run(candidate_artifact: dict | None = None) -> dict:
    """Run the reference host app demonstration.

    Local-only, fixture-based, deterministic. No network, no provider, no state mutation.
    """
    if candidate_artifact is None:
        candidate_artifact = {
            "candidate_only": True,
            "applied_truth": False,
            "proof_gaps": ["production_readiness", "live_model_inference"],
            "artifact": {"kind": "example_reference_candidate", "result": "example"},
            "proof_boundaries": ["candidate_artifact_not_applied_truth"],
        }

    policy = load_host_policy()
    host_state = get_neutral_host_state()
    inbox_receipt = receive_candidate(candidate_artifact)
    inspection = inspect_candidate_with_policy(candidate_artifact, policy)
    decision = host_owned_apply_decision(inspection)

    return {
        "artifact_kind": "reference_host_app_receipt",
        "status": "ok",
        "candidate_only": True,
        "local_only": True,
        "host_app_owns_apply": HOST_APP_OWNS_APPLY,
        "host_app_owns_state": HOST_APP_OWNS_STATE,
        "host_app_owns_external_send": HOST_APP_OWNS_EXTERNAL_SEND,
        "app_state_mutated": False,
        "external_send_performed": False,
        "odin_app_apply": False,
        "odin_external_send": False,
        "candidate_artifact_is_applied_truth": False,
        "host_state": host_state,
        "inbox_receipt": inbox_receipt,
        "policy_inspection": inspection,
        "apply_decision": decision,
        "claim_boundary": (
            "reference_host_app_candidate_only_no_apply_no_external_send_no_state_mutation"
        ),
        "proof_boundaries": policy.get("proof_boundaries", []),
        "known_non_proofs": policy.get("known_non_proofs", []),
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2))

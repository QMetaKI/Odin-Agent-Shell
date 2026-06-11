"""Generic App Bridge — Flow One: Minimal Candidate Flow.

Claim boundary: generic_app_bridge_flow_one_candidate_only_no_apply_no_external_send

Demonstrates:
- load request fixture
- construct Universal Work request
- produce/read Candidate Artifact fixture
- display proof boundaries
- host app owns apply/state/external send
- candidate artifact is not applied truth

Does NOT:
- apply candidate
- mutate host app state
- send externally
- use concrete app names
- call provider or model
- use credentials
"""

from __future__ import annotations

import json
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_FIXTURES = _HERE / "fixtures"
_ODIN_LOCAL_URL = "http://127.0.0.1:7700"

CANDIDATE_ONLY = True
HOST_APP_OWNS_APPLY = True
HOST_APP_OWNS_STATE = True
HOST_APP_OWNS_EXTERNAL_SEND = True
APPLIED_TRUTH = False


def load_request_fixture() -> dict:
    """Load the generic bridge flow one request fixture."""
    fixture_path = _FIXTURES / "generic_bridge_flow_one_request.valid.json"
    with open(fixture_path, encoding="utf-8") as fh:
        return json.load(fh)


def load_candidate_fixture() -> dict:
    """Load the generic bridge flow one candidate artifact fixture."""
    fixture_path = _FIXTURES / "generic_bridge_flow_one_candidate.valid.json"
    with open(fixture_path, encoding="utf-8") as fh:
        return json.load(fh)


def construct_universal_work_request(request_fixture: dict) -> dict:
    """Construct a Universal Work request from the loaded fixture.

    Returns a candidate-only request dict. Does not call any provider or model.
    Host app owns apply.
    """
    return {
        "candidate_only": True,
        "local_only": True,
        "host_app_owns_apply": True,
        "host_app_owns_state": True,
        "host_app_owns_external_send": True,
        "applied_truth": False,
        "work": request_fixture.get("work", {}),
        "claim_boundary": request_fixture.get("claim_boundary", ""),
    }


def read_candidate_artifact(candidate_fixture: dict) -> dict:
    """Read the Candidate Artifact from the loaded fixture.

    This is not applied truth. Host app decides whether to use this result.
    """
    return {
        "candidate_only": candidate_fixture.get("candidate_only", True),
        "applied_truth": candidate_fixture.get("applied_truth", False),
        "local_only": candidate_fixture.get("local_only", True),
        "host_app_owns_apply": candidate_fixture.get("host_app_owns_apply", True),
        "artifact": candidate_fixture.get("artifact", {}),
        "proof_boundaries": candidate_fixture.get("proof_boundaries", []),
        "known_non_proofs": candidate_fixture.get("known_non_proofs", []),
    }


def display_proof_boundaries(candidate: dict) -> None:
    """Display proof boundaries and known non-proofs from the candidate artifact."""
    print("Proof Boundaries:")
    for boundary in candidate.get("proof_boundaries", []):
        print(f"  - {boundary}")
    print("Known Non-Proofs:")
    for non_proof in candidate.get("known_non_proofs", []):
        print(f"  - {non_proof}")


def host_app_apply_decision(candidate: dict) -> dict:
    """Host app inspects candidate and makes its own apply decision.

    Host app owns apply. Odin does not apply.
    This function returns a plan-only record. No state is mutated.
    """
    return {
        "host_owned_apply_demo": "plan_only",
        "candidate_reviewed": True,
        "applied_truth": False,
        "app_state_mutated": False,
        "external_send_performed": False,
        "host_decision": "host_app_decides_independently",
        "candidate_kind": candidate.get("artifact", {}).get("kind", "unknown"),
        "note": (
            "Host app has reviewed the candidate artifact and makes its own apply decision. "
            "Odin does not apply. This is a plan-only demonstration."
        ),
    }


def run() -> dict:
    """Run Generic Bridge Flow One — Minimal Candidate Flow.

    Local-only, fixture-based, deterministic. No network, no provider, no state mutation.
    """
    request_fixture = load_request_fixture()
    universal_work = construct_universal_work_request(request_fixture)

    candidate_fixture = load_candidate_fixture()
    candidate = read_candidate_artifact(candidate_fixture)

    display_proof_boundaries(candidate)

    host_decision = host_app_apply_decision(candidate)

    return {
        "artifact_kind": "generic_bridge_flow_one_receipt",
        "status": "ok",
        "candidate_only": CANDIDATE_ONLY,
        "local_only": True,
        "host_app_owns_apply": HOST_APP_OWNS_APPLY,
        "host_app_owns_state": HOST_APP_OWNS_STATE,
        "host_app_owns_external_send": HOST_APP_OWNS_EXTERNAL_SEND,
        "odin_app_apply": False,
        "odin_external_send": False,
        "host_state_mutated": False,
        "external_send_performed": False,
        "applied_truth": APPLIED_TRUTH,
        "universal_work_constructed": True,
        "candidate_read": True,
        "proof_boundaries": candidate.get("proof_boundaries", []),
        "known_non_proofs": candidate.get("known_non_proofs", []),
        "host_decision": host_decision,
        "claim_boundary": "generic_app_bridge_flow_one_candidate_only_no_apply_no_external_send",
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2))

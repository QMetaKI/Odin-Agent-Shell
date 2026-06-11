"""Generic App Bridge — Flow Two: Proof-Gap-Aware Flow.

Claim boundary: generic_app_bridge_flow_two_candidate_only_no_apply_no_external_send_proof_gap_aware

Demonstrates:
- read proof gaps from candidate artifact
- construct Universal Work request
- read Candidate Artifact
- show known non-proofs
- show app-owned apply boundary
- show no external send by Odin

Does NOT:
- close proof gaps by display
- claim production readiness
- claim security certification
- claim specific external app integration
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
    """Load the generic bridge flow two request fixture."""
    fixture_path = _FIXTURES / "generic_bridge_flow_two_request.valid.json"
    with open(fixture_path, encoding="utf-8") as fh:
        return json.load(fh)


def load_candidate_fixture() -> dict:
    """Load the generic bridge flow two candidate artifact fixture."""
    fixture_path = _FIXTURES / "generic_bridge_flow_two_candidate.valid.json"
    with open(fixture_path, encoding="utf-8") as fh:
        return json.load(fh)


def read_proof_gaps(candidate_fixture: dict) -> list:
    """Read proof gaps from the candidate artifact.

    Displaying proof gaps does not close them. They remain non-proofs.
    """
    return candidate_fixture.get("proof_gaps", [])


def construct_universal_work_request(request_fixture: dict) -> dict:
    """Construct a proof-gap-aware Universal Work request from the loaded fixture."""
    return {
        "candidate_only": True,
        "local_only": True,
        "host_app_owns_apply": True,
        "host_app_owns_state": True,
        "host_app_owns_external_send": True,
        "applied_truth": False,
        "proof_gap_aware": True,
        "work": request_fixture.get("work", {}),
        "claim_boundary": request_fixture.get("claim_boundary", ""),
    }


def read_candidate_artifact(candidate_fixture: dict) -> dict:
    """Read the Candidate Artifact with proof gap information.

    Proof gaps are surfaced but not closed. Host app decides whether to use this result.
    """
    return {
        "candidate_only": candidate_fixture.get("candidate_only", True),
        "applied_truth": candidate_fixture.get("applied_truth", False),
        "local_only": candidate_fixture.get("local_only", True),
        "host_app_owns_apply": candidate_fixture.get("host_app_owns_apply", True),
        "proof_gap_aware": candidate_fixture.get("proof_gap_aware", True),
        "proof_gaps": candidate_fixture.get("proof_gaps", []),
        "artifact": candidate_fixture.get("artifact", {}),
        "proof_boundaries": candidate_fixture.get("proof_boundaries", []),
        "known_non_proofs": candidate_fixture.get("known_non_proofs", []),
    }


def display_proof_gap_summary(candidate: dict) -> None:
    """Display proof gap summary.

    Surfacing proof gaps does not close them. They remain as listed known non-proofs.
    """
    print("Proof Gaps (not closed by display):")
    for gap in candidate.get("proof_gaps", []):
        print(f"  gap: {gap} (not proven)")
    print("Proof Boundaries:")
    for boundary in candidate.get("proof_boundaries", []):
        print(f"  - {boundary}")
    print("Known Non-Proofs:")
    for non_proof in candidate.get("known_non_proofs", []):
        print(f"  - {non_proof}")
    print()
    print("Note: Displaying proof gaps does not close them. Host app decides whether to use this candidate.")


def show_app_owned_apply_boundary() -> dict:
    """Show the app-owned apply boundary as a plan-only demonstration.

    Host app owns apply. Odin does not apply. No state is mutated.
    """
    return {
        "host_owned_apply_boundary": "demonstrated",
        "host_owned_apply_demo": "plan_only",
        "app_state_mutated": False,
        "external_send_performed": False,
        "odin_applies": False,
        "odin_sends_externally": False,
        "note": "Host app owns apply, state, and external send. Odin produces candidates only.",
    }


def run() -> dict:
    """Run Generic Bridge Flow Two — Proof-Gap-Aware Flow.

    Local-only, fixture-based, deterministic. No network, no provider, no state mutation.
    Surfaces proof gaps without closing them.
    """
    request_fixture = load_request_fixture()
    universal_work = construct_universal_work_request(request_fixture)

    candidate_fixture = load_candidate_fixture()
    proof_gaps = read_proof_gaps(candidate_fixture)
    candidate = read_candidate_artifact(candidate_fixture)

    display_proof_gap_summary(candidate)

    apply_boundary = show_app_owned_apply_boundary()

    return {
        "artifact_kind": "generic_bridge_flow_two_receipt",
        "status": "ok",
        "candidate_only": CANDIDATE_ONLY,
        "local_only": True,
        "proof_gap_aware": True,
        "host_app_owns_apply": HOST_APP_OWNS_APPLY,
        "host_app_owns_state": HOST_APP_OWNS_STATE,
        "host_app_owns_external_send": HOST_APP_OWNS_EXTERNAL_SEND,
        "odin_app_apply": False,
        "odin_external_send": False,
        "host_state_mutated": False,
        "external_send_performed": False,
        "applied_truth": APPLIED_TRUTH,
        "proof_gaps_surfaced": proof_gaps,
        "proof_gaps_closed": False,
        "universal_work_constructed": True,
        "candidate_read": True,
        "proof_boundaries": candidate.get("proof_boundaries", []),
        "known_non_proofs": candidate.get("known_non_proofs", []),
        "apply_boundary_demo": apply_boundary,
        "claim_boundary": (
            "generic_app_bridge_flow_two_candidate_only_no_apply_no_external_send_proof_gap_aware"
        ),
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2))

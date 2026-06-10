from __future__ import annotations

import json
import subprocess
import sys

import pytest

from odin.models.config import validate_provider_config
from odin.models.permissions import build_permission_card, check_permission_escalation
from odin.models.providers.registry import list_provider_cards, get_provider
from odin.models.redaction import dumps_redacted, redact_secrets
from odin.output.composer import compose_candidate_content
from odin.precompute import score_pre_llm_route
from odin.runtime.engine import OdinRuntime
from odin.runtime.errors import OdinValidationError

FORBIDDEN_ROLES = {"app_authority", "apply_executor", "claim_acceptor", "receipt_issuer", "external_sender", "state_mutator"}


def test_provider_cards_declare_candidate_only_worker_boundary_and_forbidden_roles():
    cards = list_provider_cards()
    assert cards
    for card in cards:
        assert card["candidate_only"] is True
        assert "candidate_worker" in card["allowed_roles"]
        assert FORBIDDEN_ROLES.issubset(set(card["forbidden_roles"]))
        assert card["may_apply"] is False
        assert card["may_send_external"] is False
        assert card["may_mutate_app_state"] is False
        assert card["may_accept_claim"] is False
        assert card["may_issue_receipt"] is False
        assert "applied_patch" in card["forbidden_outputs"]


def test_provider_results_never_imply_truth_or_apply():
    for name in ["null", "echo", "mock", "ollama_stub", "llamacpp_stub", "openai_compatible_stub", "claude_compatible_stub"]:
        result = get_provider(name).generate("hello").to_dict()
        assert result["candidate_only"] is True
        assert result["truth_claim"] is False
        assert result["may_apply"] is False
        assert result["may_mutate_app_state"] is False
        assert result["may_send_external"] is False
        assert result["may_accept_claim"] is False
        assert result["may_issue_receipt"] is False
        assert result["model_inference_verified"] is False


def test_remote_stubs_are_disabled_or_non_verified_by_default():
    for name in ["ollama_stub", "llamacpp_stub", "openai_compatible_stub", "claude_compatible_stub"]:
        provider = get_provider(name)
        card = provider.capability_card()
        result = provider.generate("not dispatched").to_dict()
        assert card["enabled_by_default"] is False
        assert card["configured"] is False
        assert card["live_inference_verified"] is False
        assert result["status"] == "disabled"
        assert result["model_inference_verified"] is False
        assert result["claim_boundary"] == "provider_adapter_is_disabled_stub_not_live_inference"


@pytest.mark.parametrize("gate", ["may_apply", "may_send_external", "may_mutate_app_state", "may_accept_claim", "may_issue_receipt"])
def test_permission_cards_block_authority_escalation(gate):
    card = build_permission_card("worker-test")
    assert card[gate] is False
    decision = check_permission_escalation(card, {gate: True})
    assert decision["status"] == "blocked"
    assert gate in decision["blocked_reasons"]


def test_pre_llm_route_chooses_no_model_when_sufficient_and_emits_gap():
    work = {
        "work_id": "WORK-NO-MODEL",
        "work_intent": {"kind": "classify", "requires_model": False, "goal": "deterministic classify"},
        "model_policy": {"requires_model": False},
        "output_contract": {"candidate_only": True, "app_owned_apply": True, "may_apply": False},
        "constraints": {"actions": []},
    }
    route = score_pre_llm_route(work)
    assert route["requires_model"] is False
    assert route["route"] == "deterministic_no_model"
    assert route["selected_provider_id"] is None
    assert "model_not_executed_deterministic_route" in route["proof_gap"]
    assert route["candidate_only"] is True


def test_direct_apply_work_is_blocked_before_provider_dispatch():
    work = {
        "work_id": "WORK-DIRECT-APPLY",
        "work_intent": {"kind": "apply", "goal": "apply directly"},
        "model_policy": {"requires_model": True},
        "output_contract": {"candidate_only": False, "app_owned_apply": False, "may_apply": True},
        "constraints": {"actions": ["direct_apply"]},
    }
    route = score_pre_llm_route(work)
    assert route["route"] == "cannot_safely_complete"
    assert route["blocked_reasons"]
    assert "provider_not_dispatched_due_to_pre_llm_authority_block" in route["proof_gap"]
    with pytest.raises(OdinValidationError):
        OdinRuntime().run_universal_work({
            "artifact_kind": "odin_universal_work",
            "protocol_version": "7.1",
            "binding_ref": "BIND-DEMO-001",
            "caller_id": "demo.bad.app",
            "work_id": "WORK-DIRECT-APPLY",
            "input_artifacts": [],
            "claim_boundary": {"claims": ["candidate_only"]},
            **work,
        })


def test_provider_config_redacts_secret_values_and_invalid_config_fails_closed():
    secret = {
        "artifact_kind": "odin_provider_config",
        "protocol_version": "7.1",
        "providers": [{
            "provider_id": "secret-fixture",
            "enabled_by_default": False,
            "live_inference_verified": False,
            "credentials": {
                "api_key": "VALUE_API",
                "token": "VALUE_TOKEN",
                "secret": "VALUE_SECRET",
                "password": "VALUE_PASSWORD",
                "authorization": "Bearer VALUE_BEARER",
                "client_secret": "VALUE_CLIENT",
                "refresh_token": "VALUE_REFRESH",
                "access_token": "VALUE_ACCESS",
            },
        }],
        "claim_boundary": "test",
    }
    assert validate_provider_config(secret)
    rendered = dumps_redacted(secret)
    for leaked in ["VALUE_API", "VALUE_TOKEN", "VALUE_SECRET", "VALUE_PASSWORD", "VALUE_BEARER", "VALUE_CLIENT", "VALUE_REFRESH", "VALUE_ACCESS"]:
        assert leaked not in rendered
    redacted = redact_secrets(secret)
    assert redacted["providers"][0]["credentials"]["api_key"] == "[REDACTED]"


def test_output_composer_preserves_candidate_only_boundary_and_proof_gaps():
    route = {
        "reason": "deterministic_or_declared_no_model_sufficient",
        "proof_gap": ["model_not_executed_deterministic_route"],
        "candidate_only": True,
    }
    content = compose_candidate_content(work={"work_id": "W"}, route_decision=route, deterministic_output={"candidate_only": True})
    assert content["candidate_only"] is True
    assert content["app_owned_apply"] is True
    assert content["may_apply"] is False
    assert content["may_issue_receipt"] is False
    assert "model_not_executed_deterministic_route" in content["proof_gaps"]
    assert "not_truth_or_receipt" in content["claim_boundary"]


def test_list_providers_and_run_golden_flow_still_work():
    list_result = subprocess.run([sys.executable, "-m", "odin.cli", "list-providers"], check=True, text=True, capture_output=True)
    providers = json.loads(list_result.stdout)
    assert providers["providers"]
    golden = subprocess.run([sys.executable, "-m", "odin.cli", "run-golden-flow"], check=True, text=True, capture_output=True)
    payload = json.loads(golden.stdout)
    assert payload["status"] == "candidate_generated"
    assert payload["candidate_count"] == 1

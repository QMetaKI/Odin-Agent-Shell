"""Execution gateway — FINAL-PR-05.

Claim boundary: final_pr_05_execution_gate_mock_only_not_model_quality_not_production
candidate_only: true
local_only: true
"""
from __future__ import annotations

import hashlib
import json
import time

from .policy import ExecutionGatePolicy, DEFAULT_EXECUTION_GATE_POLICY
from .mock_provider import MockProvider

CLAIM_BOUNDARY = "final_pr_05_execution_gate_mock_only_not_model_quality_not_production"


def _make_trace_ref(provider_id: str, input_ref: str) -> str:
    raw = json.dumps({"provider_id": provider_id, "input_ref": input_ref, "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    return "TRACE-" + hashlib.sha256(raw.encode()).hexdigest()[:16]


def _make_receipt_ref(trace_ref: str) -> str:
    return "RCPT-" + hashlib.sha256(trace_ref.encode()).hexdigest()[:16]


def _make_input_ref(input_text: str) -> str:
    return "INREF-" + hashlib.sha256(input_text.encode()).hexdigest()[:12]


class ExecutionGateway:
    def __init__(self, policy: ExecutionGatePolicy | None = None) -> None:
        self.policy = policy or DEFAULT_EXECUTION_GATE_POLICY
        self._mock_provider = MockProvider()

    def execute(self, input_text: str, provider_id: str = "mock") -> dict:
        input_ref = _make_input_ref(input_text)
        trace_ref = _make_trace_ref(provider_id, input_ref)
        receipt_ref = _make_receipt_ref(trace_ref)

        # Emit QIRC gate check event
        self._emit_qirc(
            channel="#odin.model",
            kind="execution_gate_checked",
            provider_id=provider_id,
            input_ref=input_ref,
            trace_ref=trace_ref,
        )

        if provider_id == "mock":
            allowed, reason = self.policy.check_mock_execution()
            if not allowed:
                return self._blocked_response(provider_id, reason, input_ref, trace_ref, receipt_ref)
            self._emit_qirc(
                channel="#odin.model",
                kind="mock_execution_allowed",
                provider_id=provider_id,
                input_ref=input_ref,
                trace_ref=trace_ref,
            )
            result = self._mock_provider.execute(input_text=input_text, trace_ref=trace_ref, receipt_ref=receipt_ref)
            self._emit_qirc(
                channel="#odin.model",
                kind="mock_execution_completed",
                provider_id=provider_id,
                input_ref=input_ref,
                trace_ref=trace_ref,
                receipt_ref=receipt_ref,
            )
            self._emit_qirc(
                channel="#odin.trace",
                kind="mock_execution_trace",
                provider_id=provider_id,
                input_ref=input_ref,
                trace_ref=trace_ref,
            )
            self._emit_qirc(
                channel="#odin.receipt",
                kind="mock_execution_receipt",
                provider_id=provider_id,
                input_ref=input_ref,
                receipt_ref=receipt_ref,
            )
            return result

        if provider_id in ("ollama_candidate", "llama_cpp_candidate"):
            _allowed, reason = self.policy.check_local_candidate()
            self._emit_qirc(
                channel="#odin.model",
                kind="local_candidate_execution_blocked",
                provider_id=provider_id,
                input_ref=input_ref,
                trace_ref=trace_ref,
                gate_decision="blocked",
                reason=reason,
            )
            self._emit_qirc(
                channel="#odin.warning",
                kind="local_candidate_execution_blocked",
                provider_id=provider_id,
                input_ref=input_ref,
                gate_decision="blocked",
            )
            return self._local_candidate_blocked_response(provider_id, reason, input_ref, trace_ref, receipt_ref)

        # Remote/unknown providers blocked
        self._emit_qirc(
            channel="#odin.model",
            kind="remote_execution_blocked",
            provider_id=provider_id,
            input_ref=input_ref,
            trace_ref=trace_ref,
        )
        return self._blocked_response(provider_id, "remote_execution_blocked", input_ref, trace_ref, receipt_ref)

    def _emit_qirc(self, channel: str, kind: str, **kwargs: object) -> None:
        try:
            from odin.qirc_core.bus import append_event
            payload = {
                "provider_id": kwargs.get("provider_id", "unknown"),
                "gate_decision": kwargs.get("gate_decision", "allowed"),
                "execution_kind": "mock_deterministic" if kwargs.get("provider_id") == "mock" else "blocked",
                "mock_execution": kwargs.get("provider_id") == "mock",
                "real_provider_execution": False,
                "model_inference": False,
                "candidate_only": True,
                "local_only": True,
                "app_apply": False,
            }
            if "input_ref" in kwargs:
                payload["input_ref"] = kwargs["input_ref"]
            if "trace_ref" in kwargs:
                payload["trace_ref"] = kwargs["trace_ref"]
            if "receipt_ref" in kwargs:
                payload["receipt_ref"] = kwargs["receipt_ref"]
            if "reason" in kwargs:
                payload["reason"] = kwargs["reason"]
            append_event(channel=channel, kind=kind, source="execution_gateway", payload=payload)
        except Exception:
            pass

    def _blocked_response(self, provider_id: str, reason: str, input_ref: str, trace_ref: str, receipt_ref: str) -> dict:
        return {
            "artifact_kind": "odin_execution_gate_blocked_response",
            "provider_id": provider_id,
            "gate_decision": "blocked",
            "reason": reason,
            "mock_execution": False,
            "real_provider_execution": False,
            "model_inference": False,
            "candidate_only": True,
            "local_only": True,
            "app_apply": False,
            "external_send": False,
            "input_ref": input_ref,
            "trace_ref": trace_ref,
            "receipt_ref": receipt_ref,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    def _local_candidate_blocked_response(self, provider_id: str, reason: str, input_ref: str, trace_ref: str, receipt_ref: str) -> dict:
        return {
            "artifact_kind": "odin_local_candidate_blocked_response",
            "provider_id": provider_id,
            "gate_decision": "blocked",
            "reason": reason,
            "local_candidate_execution_allowed": False,
            "requires_explicit_future_gate": True,
            "mock_execution": False,
            "real_provider_execution": False,
            "model_inference": False,
            "candidate_only": True,
            "local_only": True,
            "app_apply": False,
            "external_send": False,
            "input_ref": input_ref,
            "trace_ref": trace_ref,
            "receipt_ref": receipt_ref,
            "claim_boundary": CLAIM_BOUNDARY,
        }


def execute_candidate(input_text: str, provider_id: str = "mock", policy: ExecutionGatePolicy | None = None) -> dict:
    gw = ExecutionGateway(policy=policy)
    return gw.execute(input_text=input_text, provider_id=provider_id)

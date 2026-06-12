"""QIRC Core policy — local-only, no public network, no federation.

Claim boundary: qirc_core_first_slice_local_only_not_public_network_not_app_apply
"""
from __future__ import annotations
from dataclasses import dataclass

CLAIM_BOUNDARY = "qirc_core_first_slice_local_only_not_public_network_not_app_apply"

@dataclass(frozen=True)
class QircPolicy:
    local_only: bool = True
    allow_public_network: bool = False
    allow_federation: bool = False
    allow_lan_bind: bool = False
    allow_wan_bind: bool = False
    allow_external_broker: bool = False
    allow_app_apply: bool = False
    allow_external_send: bool = False
    allow_provider_execution: bool = False
    allow_model_inference: bool = False

    def check(self) -> list[str]:
        errors = []
        if self.allow_public_network:
            errors.append("policy violation: allow_public_network must be False")
        if self.allow_federation:
            errors.append("policy violation: allow_federation must be False")
        if self.allow_lan_bind:
            errors.append("policy violation: allow_lan_bind must be False")
        if self.allow_wan_bind:
            errors.append("policy violation: allow_wan_bind must be False")
        if self.allow_external_broker:
            errors.append("policy violation: allow_external_broker must be False")
        if self.allow_app_apply:
            errors.append("policy violation: allow_app_apply must be False")
        if self.allow_external_send:
            errors.append("policy violation: allow_external_send must be False")
        if self.allow_provider_execution:
            errors.append("policy violation: allow_provider_execution must be False")
        if self.allow_model_inference:
            errors.append("policy violation: allow_model_inference must be False")
        return errors

    def is_safe(self) -> bool:
        return len(self.check()) == 0

DEFAULT_POLICY = QircPolicy()

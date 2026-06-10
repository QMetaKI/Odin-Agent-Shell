"""Fairy/Y* to Shadow IR lowering.

This is a deterministic preview. It does not generate executable runtime code.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class FairyShadowMapping:
    fairy_node: str
    ystar_node: str
    runtime_contract: str
    authority: str
    forbidden: tuple[str, ...]
    shadow_module: str


def lower_mapping_to_shadow_fragment(mapping: FairyShadowMapping) -> dict:
    forbidden = set(mapping.forbidden)
    if "app_mutation" not in forbidden:
        forbidden.add("app_mutation")
    if "external_send" not in forbidden:
        forbidden.add("external_send")
    return {
        "artifact_kind": "odin_shadow_ir_fragment",
        "source_fairy_node": mapping.fairy_node,
        "source_ystar_node": mapping.ystar_node,
        "runtime_contract": mapping.runtime_contract,
        "shadow_module": mapping.shadow_module,
        "authority": mapping.authority,
        "forbidden": sorted(forbidden),
        "claim_boundary": "shadow_ir_fragment_is_blueprint_only",
    }

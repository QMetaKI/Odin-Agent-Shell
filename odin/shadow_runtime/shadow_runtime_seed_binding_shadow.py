from __future__ import annotations
def build_shadow_seed_binding(shadow_contract: str, active_seeds: list[str], archetype_roles: list[str]) -> dict:
    return {"artifact_kind":"odin_shadow_seed_binding","binding_id":f"seedbind::{shadow_contract}","shadow_contract":shadow_contract,"active_seeds":active_seeds,"archetype_roles":archetype_roles,"bug6_status":"preserved" if "children_family_first" in active_seeds else "missing","q7_status":"tracked","why_trace_ref":f"why::{shadow_contract}"}

from __future__ import annotations
def bind_fairy_node_to_seeds(fairy_node: str, ystar_node: str, seeds: list[str]) -> dict:
    if not fairy_node or not ystar_node:
        return {"ok": False, "reason": "missing fairy or ystar node"}
    if "candidate_only" not in seeds:
        return {"ok": False, "reason": "candidate_only seed required"}
    return {"ok": True, "fairy_node": fairy_node, "ystar_node": ystar_node, "active_seeds": seeds, "shadow_contract": ystar_node.replace(".", "_")}

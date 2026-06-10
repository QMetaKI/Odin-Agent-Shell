from __future__ import annotations

from odin.runtime.ids import stable_id
from odin.work_atoms.atoms import ATOM_FUNCTIONS
from odin.work_atoms.runtime import MAX_TOTAL_ATOMS, plan_work_atoms_from_types
from .graph import validate_worklet_graph


def compile_worklet_graph_to_atom_plan(graph: dict, *, allow_unknown_atoms: bool = False) -> dict:
    errors = validate_worklet_graph(graph)
    atoms: list[dict] = []
    skipped: list[dict] = []
    for worklet in graph.get("worklets", []):
        for atom_type in worklet.get("atoms", []):
            if atom_type not in ATOM_FUNCTIONS:
                if allow_unknown_atoms:
                    skipped.append({"worklet_id": worklet.get("worklet_id"), "atom_type": atom_type, "reason": "unknown_atom_skipped_candidate"})
                    continue
                errors.append(f"unknown_atom:{atom_type}")
                continue
            atoms.append({"worklet_id": worklet.get("worklet_id"), "atom_type": atom_type})
    if len(atoms) > MAX_TOTAL_ATOMS:
        errors.append(f"too_many_total_atoms:{len(atoms)}>{MAX_TOTAL_ATOMS}")
    if errors:
        return {
            "artifact_kind": "odin_work_atom_plan",
            "protocol_version": "7.1",
            "plan_id": stable_id("ATOMPLAN", {"graph_id": graph.get("graph_id"), "errors": errors}, 12),
            "work_id": graph.get("work_id"),
            "atoms": [],
            "skipped_atoms": skipped,
            "status": "blocked",
            "errors": sorted(set(errors)),
            "candidate_only": True,
            "claim_boundary": "worklet_compile_failed_closed_no_side_effects",
        }
    plan = plan_work_atoms_from_types(graph.get("work_id"), atoms)
    plan["worklet_graph_id"] = graph.get("graph_id")
    plan["skipped_atoms"] = skipped
    plan["status"] = "ok"
    return plan

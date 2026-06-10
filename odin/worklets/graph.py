from __future__ import annotations

from odin.runtime.ids import stable_id
from odin.work_atoms.runtime import DEFAULT_ATOM_PLAN

MAX_WORKLETS = 8
MAX_ATOMS_PER_WORKLET = 12


def build_worklet_graph(work: dict) -> dict:
    intent = work.get("work_intent", {})
    supplied = intent.get("worklets") or work.get("worklets")
    if supplied:
        worklets = supplied
    else:
        requested = intent.get("work_atoms") or DEFAULT_ATOM_PLAN
        worklets = [{"worklet_id": "WORKLET-00-main", "depends_on": [], "atoms": requested}]
    normalized = []
    for idx, worklet in enumerate(worklets):
        normalized.append(
            {
                "worklet_id": worklet.get("worklet_id") or f"WORKLET-{idx:02d}",
                "depends_on": list(worklet.get("depends_on", [])),
                "atoms": list(worklet.get("atoms", [])),
            }
        )
    return {
        "artifact_kind": "odin_worklet_graph",
        "protocol_version": "7.1",
        "graph_id": stable_id("WORKLETGRAPH", {"work_id": work.get("work_id"), "worklets": normalized}, 12),
        "work_id": work.get("work_id", "UNKNOWN"),
        "worklets": normalized,
        "candidate_only": True,
        "claim_boundary": "worklets_are_bounded_local_plan_segments_not_agents_or_apply_units",
    }


def validate_worklet_graph(graph: dict, *, max_worklets: int = MAX_WORKLETS, max_atoms_per_worklet: int = MAX_ATOMS_PER_WORKLET) -> list[str]:
    errors: list[str] = []
    if graph.get("artifact_kind") != "odin_worklet_graph":
        errors.append("invalid_worklet_graph_kind")
    worklets = graph.get("worklets", [])
    if len(worklets) > max_worklets:
        errors.append(f"too_many_worklets:{len(worklets)}>{max_worklets}")
    ids = [w.get("worklet_id") for w in worklets]
    if len(ids) != len(set(ids)):
        errors.append("duplicate_worklet_id")
    id_set = set(ids)
    adjacency = {w.get("worklet_id"): list(w.get("depends_on", [])) for w in worklets}
    for worklet in worklets:
        wid = worklet.get("worklet_id")
        atoms = worklet.get("atoms", [])
        if not wid:
            errors.append("missing_worklet_id")
        if len(atoms) > max_atoms_per_worklet:
            errors.append(f"too_many_atoms_in_worklet:{wid}:{len(atoms)}>{max_atoms_per_worklet}")
        for dep in worklet.get("depends_on", []):
            if dep not in id_set:
                errors.append(f"unknown_worklet_dependency:{wid}->{dep}")
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            errors.append(f"cycle_detected:{node}")
            return
        if node in visited:
            return
        visiting.add(node)
        for dep in adjacency.get(node, []):
            visit(dep)
        visiting.remove(node)
        visited.add(node)

    for node in id_set:
        visit(node)
    return sorted(set(errors))

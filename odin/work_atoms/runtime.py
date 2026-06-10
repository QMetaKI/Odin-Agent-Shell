from __future__ import annotations
from dataclasses import dataclass, field
from odin.runtime.ids import stable_id
from .atoms import ATOM_FUNCTIONS

DEFAULT_ATOM_PLAN = [
    "context_compress_atom",
    "boundary_scan_atom",
    "seed_activation_atom",
    "pattern_match_atom",
    "slot_forge_atom",
    "candidate_variant_atom",
    "why_trace_atom",
]


def plan_work_atoms(work: dict, compiled_seed_pack: dict | None = None, compiled_pattern_mine: dict | None = None) -> dict:
    intent = work.get("work_intent", {})
    requested = intent.get("work_atoms") or DEFAULT_ATOM_PLAN
    atoms = []
    for idx, atom_type in enumerate(requested):
        atoms.append({
            "atom_id": f"ATOM-{idx:02d}-{atom_type}",
            "atom_type": atom_type,
            "budget": {"max_ms_shadow": 25, "model_required": atom_type == "candidate_variant_atom" and intent.get("requires_model", False)},
        })
    return {
        "artifact_kind": "odin_work_atom_plan",
        "protocol_version": "7.1",
        "plan_id": stable_id("ATOMPLAN", {"work": work.get("work_id"), "atoms": requested}, 12),
        "work_id": work.get("work_id"),
        "atoms": atoms,
        "compiled_seed_pack_ref": (compiled_seed_pack or {}).get("pack_id"),
        "compiled_pattern_mine_ref": (compiled_pattern_mine or {}).get("mine_id"),
        "claim_boundary": "work_atoms_are_candidate_micro_ops",
    }

@dataclass
class WorkAtomRuntime:
    results: list[dict] = field(default_factory=list)

    def execute_atom(self, atom: dict, payload: dict) -> dict:
        atom_type = atom.get("atom_type")
        fn = ATOM_FUNCTIONS.get(atom_type)
        if not fn:
            result = {"status": "skipped", "reason": f"unknown_atom:{atom_type}"}
        else:
            result = fn(payload)
            result["status"] = "ok"
        wrapped = {"atom_id": atom.get("atom_id"), "atom_type": atom_type, "result": result, "candidate_only": True}
        self.results.append(wrapped)
        return wrapped

    def execute_plan(self, plan: dict, payload: dict) -> dict:
        for atom in plan.get("atoms", []):
            self.execute_atom(atom, payload)
        return {
            "artifact_kind": "odin_work_atom_execution",
            "protocol_version": "7.1",
            "plan_id": plan.get("plan_id"),
            "results": self.results,
            "claim_boundary": "work_atom_execution_has_no_side_effects",
        }

def execute_work_atoms(plan: dict, payload: dict) -> dict:
    return WorkAtomRuntime().execute_plan(plan, payload)

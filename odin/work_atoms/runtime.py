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

MAX_TOTAL_ATOMS = 32
MAX_ATOMS_PER_WORKLET = 12


def _wrap_atom(idx: int, atom_type: str, worklet_id: str = "WORKLET-00-main", requires_model: bool = False) -> dict:
    return {
        "atom_id": f"{worklet_id}-ATOM-{idx:02d}-{atom_type}",
        "worklet_id": worklet_id,
        "atom_type": atom_type,
        "budget": {"max_ms_shadow": 25, "model_required": bool(requires_model)},
    }


def plan_work_atoms_from_types(work_id: str | None, atom_refs: list[dict]) -> dict:
    atoms = [
        _wrap_atom(idx, ref["atom_type"], ref.get("worklet_id", "WORKLET-00-main"), ref.get("model_required", False))
        for idx, ref in enumerate(atom_refs)
    ]
    return {
        "artifact_kind": "odin_work_atom_plan",
        "protocol_version": "7.1",
        "plan_id": stable_id("ATOMPLAN", {"work": work_id, "atoms": atom_refs}, 12),
        "work_id": work_id,
        "atoms": atoms,
        "candidate_only": True,
        "claim_boundary": "work_atoms_are_candidate_micro_ops_no_side_effects",
    }


def plan_work_atoms(work: dict, compiled_seed_pack: dict | None = None, compiled_pattern_mine: dict | None = None) -> dict:
    intent = work.get("work_intent", {})
    requested = intent.get("work_atoms") or DEFAULT_ATOM_PLAN
    atom_refs = [
        {
            "atom_type": atom_type,
            "worklet_id": "WORKLET-00-main",
            "model_required": bool(intent.get("atom_model_execution_required", False)),
        }
        for atom_type in requested
    ]
    plan = plan_work_atoms_from_types(work.get("work_id"), atom_refs)
    plan["compiled_seed_pack_ref"] = (compiled_seed_pack or {}).get("pack_id")
    plan["compiled_pattern_mine_ref"] = (compiled_pattern_mine or {}).get("mine_id")
    plan.setdefault("status", "ok")
    return plan


@dataclass
class WorkAtomRuntime:
    max_total_atoms: int = MAX_TOTAL_ATOMS
    allow_unknown_atoms: bool = False
    provider_execution_proof: bool = False
    results: list[dict] = field(default_factory=list)

    def _fail_closed(self, plan: dict, reason: str, errors: list[str]) -> dict:
        return {
            "artifact_kind": "odin_work_atom_execution",
            "protocol_version": "7.1",
            "plan_id": plan.get("plan_id"),
            "status": "blocked",
            "reason": reason,
            "errors": errors,
            "results": list(self.results),
            "candidate_only": True,
            "side_effects": [],
            "claim_boundary": "work_atom_execution_failed_closed_no_side_effects_no_app_apply_no_external_send",
        }

    def validate_plan(self, plan: dict) -> list[str]:
        errors: list[str] = []
        if plan.get("status") == "blocked":
            errors.extend(plan.get("errors") or ["plan_blocked"])
        atoms = plan.get("atoms", [])
        if len(atoms) > self.max_total_atoms:
            errors.append(f"atom_budget_exceeded:{len(atoms)}>{self.max_total_atoms}")
        per_worklet: dict[str, int] = {}
        for atom in atoms:
            atom_type = atom.get("atom_type")
            wid = atom.get("worklet_id", "WORKLET-00-main")
            per_worklet[wid] = per_worklet.get(wid, 0) + 1
            if atom_type not in ATOM_FUNCTIONS and not self.allow_unknown_atoms:
                errors.append(f"unknown_atom:{atom_type}")
            if atom.get("budget", {}).get("model_required") and not self.provider_execution_proof:
                errors.append(f"model_required_without_provider_execution_proof:{atom_type}")
        for wid, count in per_worklet.items():
            if count > MAX_ATOMS_PER_WORKLET:
                errors.append(f"worklet_atom_budget_exceeded:{wid}:{count}>{MAX_ATOMS_PER_WORKLET}")
        return sorted(set(errors))

    def execute_atom(self, atom: dict, payload: dict) -> dict:
        atom_type = atom.get("atom_type")
        fn = ATOM_FUNCTIONS.get(atom_type)
        if not fn:
            result = {"status": "skipped", "reason": f"unknown_atom:{atom_type}"}
        else:
            result = fn(payload)
            result["status"] = "ok"
        wrapped = {"atom_id": atom.get("atom_id"), "worklet_id": atom.get("worklet_id"), "atom_type": atom_type, "result": result, "candidate_only": True}
        self.results.append(wrapped)
        return wrapped

    def execute_plan(self, plan: dict, payload: dict) -> dict:
        errors = self.validate_plan(plan)
        if errors:
            return self._fail_closed(plan, "plan_validation_failed", errors)
        for atom in plan.get("atoms", []):
            self.execute_atom(atom, payload)
        return {
            "artifact_kind": "odin_work_atom_execution",
            "protocol_version": "7.1",
            "plan_id": plan.get("plan_id"),
            "status": "ok",
            "results": self.results,
            "candidate_only": True,
            "side_effects": [],
            "claim_boundary": "work_atom_execution_has_no_side_effects",
        }


def execute_work_atoms(plan: dict, payload: dict, *, provider_execution_proof: bool = False) -> dict:
    return WorkAtomRuntime(provider_execution_proof=provider_execution_proof).execute_plan(plan, payload)

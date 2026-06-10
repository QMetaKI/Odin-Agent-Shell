from __future__ import annotations
from odin.runtime.ids import stable_id


def compile_flow_pack(flow_pack: dict) -> dict:
    steps = flow_pack.get("steps", [])
    work_atoms = []
    for idx, step in enumerate(steps):
        atom_type = step.get("atom_type", step.get("type", "context_compress_atom")) if isinstance(step, dict) else "context_compress_atom"
        work_atoms.append({"atom_id": f"{flow_pack.get('id','flow')}_{idx:02d}", "atom_type": atom_type, "input": step})
    return {
        "artifact_kind": "odin_compiled_flow_pack",
        "protocol_version": "7.1",
        "flow_pack_id": flow_pack.get("id", stable_id("FLOW", flow_pack, 10)),
        "work_atoms": work_atoms,
        "candidate_output_patterns": flow_pack.get("candidate_output_patterns", []),
        "why_trace_template": flow_pack.get("why_trace_template", "flow_pack_candidate_trace"),
        "claim_boundary": "flow_pack_compiles_to_candidate_work_atoms_only",
    }


def compile_flow_packs(flow_packs: list[dict]) -> list[dict]:
    return [compile_flow_pack(fp) for fp in flow_packs]

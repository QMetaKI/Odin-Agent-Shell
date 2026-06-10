from __future__ import annotations
from odin.runtime.ids import stable_id
from .security import certify_seed_pack


def validate_seed_pack(seed_pack: dict) -> list[str]:
    errors: list[str] = []
    if seed_pack.get("artifact_kind") not in {"odin_app_seed_pack", "app_seed_pack_manifest", "odin_seed_pack"}:
        errors.append("seed pack artifact_kind must be odin_app_seed_pack/app_seed_pack_manifest/odin_seed_pack")
    if not seed_pack.get("seeds") and not seed_pack.get("seed_units"):
        errors.append("seed pack must contain seeds or seed_units")
    cert = certify_seed_pack(seed_pack)
    if cert["status"] == "blocked":
        errors.extend(cert["reasons"])
    return errors


def _normalize_seed(seed: dict | str) -> dict:
    if isinstance(seed, str):
        seed = {"id": seed, "purpose": seed}
    sid = seed.get("id") or stable_id("seed", seed, 10)
    return {
        "seed_id": sid,
        "purpose": seed.get("purpose", seed.get("label", sid)),
        "activation_tags": list(seed.get("activation_tags", seed.get("tags", []))),
        "weight": float(seed.get("weight", 1.0)),
        "functions": list(seed.get("functions", [])),
        "source": seed.get("source", "app_seed_pack"),
    }


def compile_seed_pack(seed_pack: dict, work: dict | None = None) -> dict:
    errors = validate_seed_pack(seed_pack)
    seeds = seed_pack.get("seed_units") or seed_pack.get("seeds") or []
    normalized = [_normalize_seed(s) for s in seeds]
    tags = set()
    if work:
        tags |= set(work.get("work_intent", {}).get("tags", []))
        tags |= set(work.get("constraints", {}).get("tags", []))
    active = []
    for seed in normalized:
        if not tags or tags & set(seed["activation_tags"]) or "always" in seed["activation_tags"]:
            active.append(seed)
    return {
        "artifact_kind": "odin_compiled_seed_pack",
        "protocol_version": "7.1",
        "pack_id": seed_pack.get("pack_id", seed_pack.get("id", stable_id("SEEDPACK", seed_pack, 10))),
        "status": "blocked" if errors else "compiled_candidate",
        "errors": errors,
        "seed_count": len(normalized),
        "active_seeds": active,
        "all_seeds": normalized,
        "candidate_only": True,
        "no_code_execution": True,
        "claim_boundary": "compiled_seed_pack_is_pre_llm_prior_not_authority",
    }

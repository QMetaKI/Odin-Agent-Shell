from __future__ import annotations
import json
from odin.core.claim_boundary import filter_claims
from odin.runtime.ids import stable_id


def context_compress_atom(payload: dict) -> dict:
    text = json.dumps(payload.get("context", payload), ensure_ascii=False, sort_keys=True)
    max_len = int(payload.get("max_len", 500))
    return {"compressed_context": text[:max_len], "source_length": len(text), "truncated": len(text) > max_len}


def boundary_scan_atom(payload: dict) -> dict:
    claims = payload.get("claims", [])
    allowed, blocked = filter_claims(claims)
    forbidden_actions = [a for a in payload.get("actions", []) if a in {"direct_apply", "external_send", "mutate_app_state"}]
    return {"allowed_claims": allowed, "blocked_claims": blocked, "forbidden_actions": forbidden_actions, "ok": not blocked and not forbidden_actions}


def seed_activation_atom(payload: dict) -> dict:
    seeds = payload.get("seeds", [])
    tags = set(payload.get("tags", []))
    active = [s for s in seeds if not tags or tags & set(s.get("activation_tags", [])) or "always" in s.get("activation_tags", [])]
    return {"active_seeds": active, "active_count": len(active)}


def pattern_match_atom(payload: dict) -> dict:
    patterns = payload.get("patterns", [])
    tags = set(payload.get("tags", []))
    matched = [p for p in patterns if not tags or tags & set(p.get("tags", []))]
    return {"matched_patterns": matched, "matched_count": len(matched)}


def candidate_variant_atom(payload: dict) -> dict:
    base = payload.get("base", "candidate")
    variants = payload.get("variants") or ["safe", "compact", "detailed"]
    return {"variants": [{"variant_id": stable_id("VAR", {"base": base, "v": v}, 8), "label": v, "content": f"{base}:{v}"} for v in variants]}


def why_trace_atom(payload: dict) -> dict:
    return {"trace_notes": payload.get("notes", []), "decision": payload.get("decision", "candidate_generated")}

ATOM_FUNCTIONS = {
    "context_compress_atom": context_compress_atom,
    "boundary_scan_atom": boundary_scan_atom,
    "seed_activation_atom": seed_activation_atom,
    "pattern_match_atom": pattern_match_atom,
    "candidate_variant_atom": candidate_variant_atom,
    "why_trace_atom": why_trace_atom,
    "json_repair_atom": lambda payload: {"json_repair": "not_needed", "payload_type": type(payload).__name__},
    "claim_check_atom": boundary_scan_atom,
    "slot_forge_atom": lambda payload: {"slot_id": stable_id("SLOT", payload, 8), "slot_class": payload.get("slot_class", "general_candidate")},
}

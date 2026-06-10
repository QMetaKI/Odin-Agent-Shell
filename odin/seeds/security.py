from __future__ import annotations
from odin.quality.boundaries import scan_forbidden_markers

FORBIDDEN_SEED_KEYS = {"code", "script", "exec", "shell", "network", "apply"}


def certify_seed_pack(seed_pack: dict) -> dict:
    reasons: list[str] = []
    serialized_hits = scan_forbidden_markers(seed_pack)
    for hit in serialized_hits:
        if hit in {"direct_apply", "external_send", "mutate_app_state", "network_send"}:
            reasons.append(f"forbidden_marker:{hit}")
    def walk(obj, path=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                lk = str(k).lower()
                if lk in FORBIDDEN_SEED_KEYS:
                    reasons.append(f"forbidden_key:{path + '/' + lk}")
                walk(v, path + "/" + lk)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                walk(v, f"{path}/{i}")
    walk(seed_pack)
    status = "blocked" if reasons else "trusted_local_candidate"
    return {
        "artifact_kind": "odin_seed_pack_certification",
        "protocol_version": "7.1",
        "status": status,
        "reasons": sorted(set(reasons)),
        "candidate_only": True,
        "no_code_execution": True,
        "claim_boundary": "seed_packs_are_declarative_candidate_priors",
    }

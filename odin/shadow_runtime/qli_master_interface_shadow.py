from __future__ import annotations
from .odin_core_centerline_shadow import build_centerline_packet
from .dfas_stability_core_shadow import decide_admissibility
from .seed_archetype_economy_shadow import activate_seed_archetype_economy
from .qmath_center_solver_shadow import score_routes
from .ring_radar_resonance_shadow import build_ring_activation_map
from .why_trace_shadow import build_why_trace

def run_qli_master_shadow(work: dict, resource_profile: str = "standard_local") -> dict:
    admissibility = decide_admissibility(work)
    seed_packet, role_packet = activate_seed_archetype_economy(work)
    route_score = score_routes(work, seed_packet, resource_profile)
    centerline = build_centerline_packet(work, admissibility)
    rings = build_ring_activation_map(work, route_score)
    why = build_why_trace(work, centerline, seed_packet, role_packet, route_score, rings)
    return {"ok": admissibility["decision"] != "block", "admissibility": admissibility, "seed_packet": seed_packet, "archetype_role_packet": role_packet, "route_score": route_score, "centerline_packet": centerline, "ring_activation_map": rings, "why_trace": why}

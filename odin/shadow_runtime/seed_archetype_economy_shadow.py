from __future__ import annotations

def activate_seed_archetype_economy(work: dict, budget_profile: str = "standard") -> tuple[dict, dict]:
    verb = work.get("work_intent", {}).get("verb", "work")
    base = [
        {"seed_id":"claim_boundary","family":"boundary","score":0.95,"reason":"candidate-only work requires claim boundary"},
        {"seed_id":"minimal_sufficient_route","family":"economy","score":0.90,"reason":"smallest sufficient worker law"},
        {"seed_id":"no_invention","family":"evidence","score":0.88,"reason":"avoid unsupported claims"},
    ]
    if verb in {"rewrite","summarize","draft"}:
        base.append({"seed_id":"context_clarity","family":"context","score":0.84,"reason":"text transformation requires clear context"})
    roles = ["boundary_guard","context_weaver","slot_smith","scout_router","mirror_critic","candidate_messenger"]
    seed_packet={"artifact_kind":"odin_seed_activation_packet","protocol_version":"7.1","packet_id":"SEED-"+work.get("work_id","WORK"),"work_id":work.get("work_id","WORK"),"budget_profile":budget_profile,"active_seeds":base[:16],"conflicts_resolved":[]}
    role_packet={"artifact_kind":"odin_archetype_role_packet","protocol_version":"7.1","packet_id":"ROLE-"+work.get("work_id","WORK"),"work_id":work.get("work_id","WORK"),"active_roles":roles,"role_reasons":{"boundary_guard":"protect candidate-only and app authority","context_weaver":"distill app context","slot_smith":"forge bounded work slots"}}
    return seed_packet, role_packet

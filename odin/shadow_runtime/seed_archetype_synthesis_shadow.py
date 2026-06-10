from __future__ import annotations
ROLE_MAP = {"boundary":"boundary_guard","context":"context_weaver","economy":"scout_router","evidence":"mirror_critic","style":"quality_scribe","compiler":"slot_smith","qirc":"trace_keeper","fairy":"fairy_mapper"}
def synthesize_seed_archetype_roles(active_seeds: list[str]) -> dict:
    roles = {"boundary_guard", "invariant_keeper"}
    for seed in active_seeds:
        for key, role in ROLE_MAP.items():
            if key in seed:
                roles.add(role)
    return {"artifact_kind":"odin_seed_archetype_synthesis","active_seeds":active_seeds,"active_roles":sorted(roles),"decision":"allow","why":["hard seeds preserved","roles synthesized"]}

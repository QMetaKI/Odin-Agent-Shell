# Odin Core Centerline v7.1

## Purpose

The Odin Core Centerline is the internal Ring-0-like center for Odin's LLM work only. It is not app authority. It is the boundary, admissibility, center-selection and final-gate spine for model work.

## Why it exists

Odin contains many subsystems: Universal Work, Semantic Bus, Small Model Power, Shadow Runtime, Fairy/Y*, Runtime Pack Compiler, Candidate Artifacts, Model Scale Ladder and Thor Bridge. Without a typed centerline, these systems can all be locally correct but globally inconsistent. The Centerline makes every flow answer:

1. What is the center?
2. Is work admissible?
3. What boundary is active?
4. What is the smallest sufficient route?
5. Which seeds/archetypes are allowed?
6. Which model route is cost-justified?
7. Why did Odin choose this route?
8. What is forbidden?

## Non-authority boundary

Odin Core owns:

- LLM work admissibility
- candidate-only gate
- model route permission
- seed/archetype activation limits
- claim/evidence boundary
- model escalation discipline
- why-trace production

Odin Core does not own:

- app state
- app apply
- external sends
- domain truth
- user identity
- app event bus

## Centerline Packet

Each non-trivial work item produces an `odin_centerline_packet` before model routing.

Fields:

- packet_id
- work_id
- caller_id
- active_center
- admissibility_decision
- authority_boundary
- app_authority_boundary
- model_authority_boundary
- active_ring_path
- active_maria_michael_profile
- active_seed_packet_ref
- active_archetype_role_packet_ref
- qmath_route_score_ref
- why_trace_ref
- allowed_routes
- blocked_routes
- forbidden_claims
- final_gate_required

## Center selection

A center is a concise description of the stable purpose of the work.

Examples:

- rewrite selected markdown for clarity without changing meaning
- generate candidate speech opening from known story anchors
- summarize error log into debug hypothesis without claiming fix
- create patchplan candidate without applying code
- validate workflow state and produce risk report candidate

Invalid centers:

- do everything
- make it better
- fix app
- prove it works
- apply patch

## Centerline lifecycle

1. receive Universal Work
2. validate binding
3. read event digest
4. propose centers
5. score centers
6. select smallest stable center
7. run admissibility gate
8. activate seeds/archetypes
9. compute route score
10. produce why-trace
11. pass/fail final pre-model gate

## Failure behavior

If no stable center exists, Odin must return one of:

- ask_context_candidate
- split_work_candidate
- cannot_safely_complete_candidate
- conflict_candidate

It must not call a larger model merely to compensate for missing center.

## Codex Rule

Codex must ensure every complex pipeline has a Centerline Packet before model route. If a path bypasses the centerline, it is invalid.

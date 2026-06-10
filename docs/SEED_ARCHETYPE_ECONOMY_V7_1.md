# Seed / Archetype Economy v7.1

## Purpose

Seed / Archetype Economy turns Odin's narrative and pattern intelligence into typed, bounded, scored precompute. Seeds and archetype roles become compact control packets that improve small-model work without expanding context chaos.

## Seed definition

A seed is a compact activation hint with a source, score, reason, decay, conflict state and boundary. Seeds do not authorize. Seeds guide.

Seed fields:

- seed_id
- family
- source
- score
- reason
- decay_class
- freshness
- conflict_tags
- boundary_tags
- related_archetype_roles
- max_token_budget

## Archetype role definition

An archetype role is a typed operational role, not mythology.

Default roles:

- boundary_guard
- context_weaver
- slot_smith
- scout_router
- quality_scribe
- mirror_critic
- candidate_messenger
- trace_keeper
- center_solver
- recovery_keeper

## Economy budgets

Odin must cap:

- max_active_seeds
- max_active_archetype_roles
- max_conflicting_seed_pairs
- max_role_fanout
- max_seed_tokens_in_context
- max_seed_carryover_age

Recommended defaults:

- strict: 8 seeds, 3 roles
- standard: 16 seeds, 5 roles
- quality: 24 seeds, 7 roles
- explore/debug: 36 seeds, 9 roles

## Activation pipeline

1. classify intent and artifact lens
2. gather candidate seeds
3. score by context match and boundary relevance
4. apply decay
5. resolve conflicts
6. cap top-k
7. map seeds to archetype roles
8. write Seed Activation Packet
9. write Archetype Role Packet
10. link both to Candidate DNA

## Conflict resolver

If seeds conflict, Odin must prefer:

1. claim boundary
2. app authority
3. privacy
4. centerline stability
5. smallest sufficient route
6. style preference
7. creative variation

## Example

For a rewrite task:

- seed: clarity
- seed: preserve_meaning
- seed: no_invention
- role: context_weaver
- role: boundary_guard
- role: quality_scribe

For a code patchplan:

- seed: file_scope
- seed: no_apply
- seed: verification_required
- role: boundary_guard
- role: slot_smith
- role: mirror_critic

## Codex Rule

No seed or archetype may enter prompt/gaptext without typed packet entry and budget check.

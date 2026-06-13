# FINAL-PR-08 Thor-Style Field-to-Projection Handoff

claim_boundary: projection_candidate_spine_prepares_candidates_not_runtime_execution
candidate_only: true

## Repo Evidence

- PR07 merged: `odin/field_selection_spine/` present and confirmed read-only for PR08.
- PR06 merged: `odin/operational_seed_spine/` present and confirmed read-only for PR08.
- Y materialization ladder confirmed: 10 levels M0_raw_input through M9_release_evidence.
- Local Hub endpoint pattern confirmed: `GET /demo/*.json`.
- CLI validator pattern confirmed: `validate_*() -> list[str]`.

## PR07 FieldSelection Public Interface

- `select_field_route(seed_route) -> FieldSelection`
- `FieldSelection`: dominant_field, coherence_score, why_trace
- PR08 entry point: `build_projection_set_from_field_selection(field_selection) -> ProjectionSet`

## PR06 SeedRoute Upstream Evidence

- `selected_seed_id`, `selected_role_profile_id` available on SeedRoute
- Chain: PR06 select_seed_route() → PR07 select_field_route() → PR08 build_projection_set_from_field_selection()

## Y Materialization Ladder M0–M9

M0_raw_input, M1_parsed_input, M2_seed_route, M3_field_selection,
M4_projection_target, M5_projection_set, M6_candidate_artifact,
M7_expression_packet, M8_comparison_result, M9_release_evidence.
ProjectionSet = M5.

## Projection Target

`odin/projection_candidate_spine/` — organizes candidate artifacts on the materialization ladder.

## Scope (Allowed)

8 module files, registry entry, schema file, examples (valid + invalid),
validator (`validate_projection_candidate_spine`), 40 tests,
CLI (3 commands: validate, explain, prove), hub endpoint, prep validator update,
docs and reports, SYSTEM_MAP.json, FILE_MANIFEST.json.

## Non-Scope

- PR09 Release Closure (deferred)
- Runtime execution or model inference
- App apply or external send
- Modification of `odin/field_selection_spine/` or `odin/operational_seed_spine/`

## Forbidden Files

- `odin/field_selection_spine/` — no modification
- `odin/operational_seed_spine/` — no modification
- `odin/execution_gate/` — no modification
- `odin/proof_chain/` — no modification

## Acceptance Gates

1. `validate-projection-candidate-spine` exits 0
2. `explain-projection-candidate --demo` returns valid JSON
3. `prove-projection-candidate-spine` exits 0
4. `validate-all` exits 0
5. All 40 tests pass

## Proof Boundary

`projection_candidate_spine_prepares_candidates_not_runtime_execution`

## Validator Expectations

- Check all 10 materialization levels present
- Check candidate_only=True on ProjectionSet
- Check no forbidden names (no q_*, no eval, no exec, no subprocess)

## Test Expectations

40 tests covering all 8 module structures, PR06→PR07→PR08 chain, and validator.

## PR09 Release Boundary

Release Closure is deferred to FINAL-PR-09. PR08 implements only M0–M9 candidate organization.

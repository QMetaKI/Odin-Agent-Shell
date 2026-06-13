# FINAL-PR-08 Odin Agent Operator Work Packet

candidate_only: true
app_owned_apply: true
claim_boundary: projection_candidate_spine_prepares_candidates_not_runtime_execution

## Objective

Implement Projection Candidate Spine organizing candidate artifacts on the Y materialization ladder
(M0–M9). Produces candidate-only ProjectionSet from PR07 FieldSelection. Does not execute, apply,
or release.

## Inputs

- PR07 FieldSelection: `select_field_route()`, `FieldSelection.to_dict()`
- PR06 SeedRoute: `select_seed_route()`, `compile_work_capsule()`
- Y materialization ladder: 10 levels M0_raw_input through M9_release_evidence
- Prep validator current state: `IMPLEMENTED_PR_MODULE_DIRS` (add projection_candidate_spine)

## Allowed Edits

- `odin/projection_candidate_spine/` (new module — all 8 files)
- `odin/cli.py` (add 3 commands)
- `odin/local_hub/server.py` (add hub endpoint)
- `odin/local_hub/ui.py` (add hub UI entry)
- `tools/rebaseline/check_prep_final_pr_06_08.py` (add projection_candidate_spine to IMPLEMENTED_PR_MODULE_DIRS)
- `SYSTEM_MAP.json`, `FILE_MANIFEST.json`
- New test files, validator files, docs, and reports

## Forbidden Edits

- `odin/field_selection_spine/` — no modification
- `odin/operational_seed_spine/` — no modification
- `odin/execution_gate/` — no modification
- `odin/proof_chain/` — no modification

## Implementation Order

1. 8 module files in `odin/projection_candidate_spine/`
2. Registry entry and schema file
3. Fixture examples (valid + invalid JSON)
4. Validator (`validate_projection_candidate_spine`)
5. 40 tests
6. CLI (3 commands: validate-projection-candidate-spine, explain-projection-candidate, prove-projection-candidate-spine)
7. Hub endpoint: `GET /demo/projection-candidate.json`
8. Prep validator update
9. Docs and return report
10. SYSTEM_MAP.json and FILE_MANIFEST.json updates
11. Proof packet generation

## Acceptance Gates

| Gate | Expected |
|---|---|
| `validate-projection-candidate-spine` | exit 0 |
| `explain-projection-candidate --demo` | valid JSON |
| `prove-projection-candidate-spine` | exit 0 |
| `validate-all` | exit 0 |
| pytest full suite | 40 new tests pass, all existing tests pass |

## Proof Boundary

`projection_candidate_spine_prepares_candidates_not_runtime_execution`

## Return-Report Contract

Include exact full-suite pytest result inline (not deferred). Do not mark ready if any gate fails.

## Risk Controls

- No modification of PR06 or PR07 modules
- Keep PR09 deferred: `final_pr_09` stays in `RUNTIME_MODULE_DIRS_FOR_FUTURE_PRS`
- No forbidden names: no q_*, no eval, no exec, no subprocess in PR08 modules
- candidate_only=True on all ProjectionSet instances
- No datetime.now() or uuid4() in deterministic outputs

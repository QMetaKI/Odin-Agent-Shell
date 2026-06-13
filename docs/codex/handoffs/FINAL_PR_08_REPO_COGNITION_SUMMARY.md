# FINAL-PR-08 Repo Cognition Summary

## Base State

- base commit: 5b10d10 (Merge pull request #46 FINAL-PR-07)
- PR46/FINAL-PR-07: confirmed merged
- PR45/FINAL-PR-06: confirmed merged

## Files Read

All 8 new module files (materialization.py, candidate_graph.py, projection_set.py,
expression_packet.py, compare.py, receipt_link.py, proof.py, __init__.py),
plus registries, schemas, examples, CLI (odin/cli.py), local hub (odin/local_hub/server.py, ui.py).

## Files Intentionally Avoided (read-only)

- `odin/field_selection_spine/` — no modification
- `odin/operational_seed_spine/` — no modification
- `odin/execution_gate/` — out of scope
- `odin/proof_chain/` — out of scope

## Existing PR07 Public Interfaces

- `select_field_route(seed_route) -> FieldSelection`
- `select_field_route_from_seed_route(seed_route) -> FieldSelection`
- `FieldSelection.to_dict()` — includes dominant_field, coherence_score, why_trace

## Existing PR06 Public Interfaces

- `select_seed_route(work_capsule) -> SeedRoute`
- `compile_work_capsule(raw) -> WorkCapsule`

## Y Materialization Ladder

10 levels M0–M9: M0_raw_input through M9_release_evidence.
ProjectionSet sits at M5_projection_set.

## Existing Local Hub Endpoint Pattern

`GET /demo/*.json` returns `{status, candidate_only, claim_boundary, payload}`.

## Existing CLI Validator Pattern

`validate_*() -> list[str]` errors. Early-return handler before elif chain in main().

## Existing Proof Packet Pattern

`build_proof_packet() + persist_proof_packet(repo_root)` — proven/not_proven/claim_boundary.

## Prep Validator Implications

Add `odin/projection_candidate_spine` to `IMPLEMENTED_PR_MODULE_DIRS`.
Keep `final_pr_09` in `RUNTIME_MODULE_DIRS_FOR_FUTURE_PRS` (deferred/protected).

## Implementation Plan

8 module files → registry → schema → examples → validator → tests → CLI → hub →
prep update → docs → SYSTEM_MAP/FILE_MANIFEST → proof packet → reports.

## Known Non-Claims

- No runtime execution
- No model inference
- No app apply

# FINAL-PR-07 Thor-Style Repo Field Handoff

## Repo evidence
PR #45 merge at `590e28c`; FINAL-PR-06 Operational Seed Spine is present with `SeedRoute` and proof artifacts.

## PR06 SeedRoute interface
Use `select_seed_route({"trigger_shape":"repo","work_type":"repo"})`; adapt via `to_dict()` without modifying PR06.

## Field selection target
Convert work context or SeedRoute into field signals, review axes, coherence score, hole density, dominant/suppressed fields, public why trace, candidate recommendation, and proof packet.

## Scope
Only FINAL-PR-07 module, validator, tests, CLI commands, Local Hub demo endpoint/UI copy, registry/schema/examples, reports/docs/audits/handoffs, SYSTEM_MAP, FILE_MANIFEST, and prep-validator implemented skips.

## Non-scope
No PR08 projection module, no release closure, no provider/model execution, no app mutation, no external send.

## Allowed files
`odin/field_selection_spine/`, `odin/cli.py`, `odin/local_hub/server.py`, `odin/local_hub/ui.py`, PR07 docs/reports/audits/examples/schema/registry/tests/validator, SYSTEM_MAP, FILE_MANIFEST, prep validator/test.

## Forbidden files
Do not modify PR06 source, Y Pattern source, execution gate, proof chain, final PR ladder, or create `odin/projection_candidate_spine/`.

## Acceptance gates
PR07 validator ok, PR06 validator ok, prep validator ok, Y Pattern validator ok, validate-all ok, PR07/PR06/prep/full pytest commands ok.

## Proof boundary
Proof packet proves only deterministic scaffold properties and records not-proven runtime/security/authority claims.

## Downstream PR08 boundary
PR08 remains separate and protected as future leakage.

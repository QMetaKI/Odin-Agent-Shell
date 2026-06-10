# PR-75 — Y Handoff Bridge and Centerline Packet Compiler

## Objective

Build the handoff compiler surface for Y Handoff Bridge and Centerline Packet Compiler. The task exists to make Odin's original Thor-handoff-compiler identity mechanically useful for Codex and future workers while preserving candidate-only authority boundaries.

## Primary Files

- docs/THOR_Y_HANDOFF_COMPILER_CORE_V7_1.md
- docs/THOR_PROMPT_EXTRACTION_AND_PULL_V7_1.md
- docs/THOR_RETURN_REVIEW_RECEIPT_PIPELINE_V7_1.md
- docs/Y_HANDOFF_COMPILER_BRIDGE_V7_1.md
- docs/MJOLNIR_STRIKE_HANDOFF_BRIDGE_V7_1.md
- schemas/v7_1/
- registries/
- odin/shadow_runtime/
- examples/handoff/
- tests/test_thor_y_handoff_compiler.py

## Required Behavior

- Pull prompt intent into typed handoff atoms.
- Preserve Thor candidate-only kernel-bound mediation rules.
- Preserve Y-Core-like centerline and ring-path constraints for Y handoffs.
- Convert Mjölnir focused strikes into narrow candidate proposals, not direct actions.
- Compile every valid handoff into Universal Work or a blocked/ask-context/split-work report.
- Preserve non-claims, denied claims and return contracts.
- Emit Why Trace and Semantic Diff for postprocessing.
- Update internal PR ladder and real PR bundle coverage.

## Forbidden Scope

- No autonomous delegation.
- No hidden execution.
- No app mutation.
- No direct apply.
- No auto-merge.
- No returned-code execution.
- No claim acceptance.
- No receipt issuance from mediation alone.
- No production/runtime/security/deployment proof claim.

## Definition of Done

- Documentation updated with this task's scope.
- Schemas present and JSON-valid.
- Registries include handoff modes and source classes.
- Shadow Runtime module exists and is candidate-only.
- Fixture exists for valid and invalid handoff flows.
- Tests validate presence, red lines and registry coverage.
- `python -m odin.cli validate-all` passes.
- `python -m pytest -q -p no:cacheprovider` passes.

## Codex PR Summary Template

- Scope:
- Handoff source types covered:
- Return contracts added:
- Boundaries preserved:
- Tests run:
- Non-claims:

## Detailed Implementation Notes

Codex must implement this task as a deterministic boundary layer. Handoff input must be parsed, narrowed and normalized before any model or agent worker sees it. The handoff compiler must never use a model to decide its own authority. It may use configured pattern registries, schemas, caller manifests, Odin Core centerline packets, QIRC hot windows, seed/archetype state and static return-contract maps. Any ambiguous handoff must be narrowed, split, blocked or routed to ask-context rather than broadened.

Every handoff output must be candidate work. A Thor return is not a receipt. A Y handoff does not make Odin app authority. A Mjölnir focused strike is not an apply operation. Every pathway must record a Why Trace, rejected routes and the app-owned apply boundary.

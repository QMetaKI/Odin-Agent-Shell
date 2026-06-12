# FINAL-PR-07 Odin Agent Operator Work Packet

## Objective
Implement a deterministic candidate-only Field Selection Spine after FINAL-PR-06.

## Inputs
FINAL-PR-07 prompt, PR06 SeedRoute API, prep plan, Y Pattern structure, Local Hub and CLI validator patterns.

## Allowed edits
PR07 module/artifacts, CLI, Local Hub endpoint/UI copy, prep validator/test implemented markers, SYSTEM_MAP, FILE_MANIFEST.

## Forbidden edits
No PR06 source edits, no PR08 module, no release closure, no broad rewrites, no provider/model/app execution paths.

## Implementation order
Repo cognition, handoffs, module, SeedRoute adapter, registry/schema/examples, CLI, Local Hub, validator, tests, docs/audits/reports, manifest/system map, validation.

## Acceptance gates
All required validators and pytest commands return zero locally.

## Proof boundary
`field_selection_scores_routes_not_truth`; candidate-only, app-owned apply, route hints only.

## Return-report contract
Record branch/base, files, implementation, PR06 integration, validators/tests, gaps, not-proven, review fixes, PR08 recommendations.

## Risk controls
No randomness, time, network, model/provider calls, app mutation, external send, forbidden runtime names, hidden chain-of-thought fields, or authority language.

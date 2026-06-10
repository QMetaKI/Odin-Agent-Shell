# PR-61 — Pre-LLM Intelligence Layer

## Objective
Implement pre-model cognition as a first-class candidate-only pipeline.

## Primary Files
- docs/PRE_LLM_INTELLIGENCE_LAYER_V7_1.md
- docs/ODIN_PRE_MODEL_COGNITION_V7_1.md
- docs/MODEL_WORK_AVOIDANCE_V7_1.md
- docs/OUTPUT_INTELLIGENCE_COMPOSER_V7_1.md
- schemas/v7_1/
- odin/shadow_runtime/
- registries/
- tests/

## Required Behavior
- Preserve candidate-only output.
- Preserve app-owned apply and external-send boundary.
- Record route reasons and model-work-avoidance reasons.
- Prefer no-model, 3B, or split-work when quality and safety permit.
- Never use perceived intelligence to hide uncertainty.

## Forbidden Scope
- No real model provider implementation in this PR unless explicitly part of later provider bundle.
- No direct apply.
- No external send.
- No hot-path runtime generation.
- No false verification or test-passed claim.

## Definition of Done
- Schemas validate.
- Shadow modules import and return candidate-only packets.
- Tests cover positive and direct-apply negative path.
- Registries and SYSTEM_MAP updated.
- FILE_MANIFEST refreshed.

## Codex PR Summary Template
Summary: Implement Pre-LLM Intelligence Layer as part of v0.6.5 Pre-LLM Intelligence Amplification Lock.
Tests: `python -m odin.cli validate-all`; `python -m pytest -q -p no:cacheprovider`.
Boundary: candidate-only; app-owned apply; no false perceived intelligence.


## Senior Reviewer Notes
This task is not a UI polish task. It is part of the v0.6.5 pre-model cognition spine. Codex must implement it mechanically from the docs and schemas, not by inventing a new runtime pattern. The route must remain deterministic, local-first, candidate-only, and compatible with QIRC Gold Spine, DFAS Stability Core, QMath route scoring, Bug6/Q7 invariants, and app-owned apply.

## Required Negative Paths
- direct apply marker blocks the flow
- external send marker blocks the flow
- unsupported verification claim is downgraded or blocked
- missing trace_id fails validation
- perceived intelligence metrics cannot override claim boundaries
- model dispatch before admissibility is invalid

## Traceability Requirements
Update or preserve links across SYSTEM_MAP, codex task registry, REAL-PR bundle registry, shadow runtime contract registry, FILE_MANIFEST, relevant schemas, relevant tests, and Master Specs addendum. Any added public-facing wording must preserve the Micro Model Illusion Boundary: user-visible quality may improve only from actual orchestration work, not false claims.

## Review Checklist
- Is there a schema?
- Is there a shadow module?
- Is there a valid fixture and an invalid fixture where relevant?
- Is there a test?
- Is it mapped to REAL-PR-18?
- Does validate-all pass?
- Does pytest pass?
- Does the candidate-only boundary remain explicit?

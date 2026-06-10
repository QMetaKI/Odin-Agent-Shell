# PR-60 — Skynet Pattern Boundary and AI-Git Why Trace

## Objective

Implement and preserve the Skynet Pattern Boundary and AI-Git Why Trace scope as part of the v0.6.4 Senior Review AI-Git Safety Consolidation. This task is internal PR-ladder granularity, not necessarily a real external pull request by itself.

## Depends On

PR-59

## Primary Files

- docs/SKYNET_PATTERN_BOUNDARY_V7_1.md
- odin/shadow_runtime/skynet_pattern_boundary_shadow.py
- schemas/v7_1/odin_safety_why_trace.schema.json

## Required Behavior

- Preserve candidate-only output.
- Preserve app-owned apply and app-owned state.
- Preserve local-first posture.
- Preserve Bug6 / Children-First and Q7 stability gates.
- Add traceable, reviewable AI-Git safety semantics.
- Ensure every safety decision has a Why Trace or blocked reason.
- Keep Odin as Y-Core for LLM orchestration only, not app authority.

## Forbidden Scope

- No app mutation.
- No external send.
- No public QIRC expansion.
- No prose-only execution.
- No unvalidated runtime pack loading.
- No model-generated executable code.
- No silent apply.

## Definition of Done

- The relevant docs exist and include red lines.
- The relevant schemas exist and validate as JSON.
- The relevant registries exist with registry_id and version.
- Shadow Runtime module exists and is imported by tests.
- Tests pass with `python -m pytest -q -p no:cacheprovider`.
- `python -m odin.cli validate-all` passes.
- FILE_MANIFEST is refreshed.

## Codex PR Summary Template

```text
Implemented PR-60 — Skynet Pattern Boundary and AI-Git Why Trace.
Preserved candidate-only/app-owned-apply/local-first boundaries.
Updated docs/schemas/registries/shadow/tests as required.
Ran validation and tests.
```


## Implementation Notes

Codex must treat this task as a boundary-preserving implementation step. The purpose is not to add autonomous behavior. The purpose is to make the existing Odin v7.1 architecture more reviewable, more deterministic, and safer to translate into real code. Each implementation must keep generated artifacts separate from app-owned actions and must preserve the exact distinction between candidate, preview, apply request, and app-owned apply.

## Required Test Coverage

- Positive candidate path where the output remains candidate-only.
- Negative path where direct apply is rejected.
- Negative path where external send is rejected.
- Trace path where the Why Trace identifies the chosen route and blocked alternatives.
- Registry path where the task is represented in both internal PR ladder and real PR bundle coverage.

## Review Checklist

- Does the task weaken no-LLM-in-app? If yes, reject.
- Does it allow Odin to mutate app state? If yes, reject.
- Does it hide the model route? If yes, reject.
- Does it preserve Bug6/Children-First and Q7 stability? If no, reject.
- Does it update SYSTEM_MAP and FILE_MANIFEST? If no, reject.

## Senior Reviewer Constraint

The implementation may improve explainability and orchestration, but it may not expand Odin authority. Better safety means less invisible autonomy, not more clever autonomous behavior.

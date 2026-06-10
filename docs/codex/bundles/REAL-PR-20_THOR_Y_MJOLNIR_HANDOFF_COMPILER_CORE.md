# REAL-PR-20 — Thor/Y/Mjölnir Handoff Compiler Core

## Objective

Restore Odin's original handoff-compiler identity as a first-class build unit. This real PR bundle compiles Thor handoffs, Y handoffs and Mjölnir focused-strike requests into bounded Universal Work, Candidate Artifacts, review gates and Why Traces. It is the bridge between prompt-shaped intent, repo/codex handoff work, Y-Core centerline routing, Thor candidate mediation and app-owned review/apply.

## Internal Tasks Covered

- PR-73 — Thor Prompt Pull and Handoff Compiler Core
- PR-74 — Thor Return Review and Receipt Boundary Pipeline
- PR-75 — Y Handoff Bridge and Centerline Packet Compiler
- PR-76 — Mjölnir Focused Strike Handoff Bridge
- PR-77 — Handoff Prompt Canonicalization and Pattern Registry
- PR-78 — Handoff to Universal Work Conversion
- PR-79 — Handoff Postprocessing Candidate Pipeline
- PR-80 — Thor Y Mjolnir Consolidated Handoff Gates

## Primary Files

- docs/THOR_Y_HANDOFF_COMPILER_CORE_V7_1.md
- docs/THOR_PROMPT_EXTRACTION_AND_PULL_V7_1.md
- docs/THOR_RETURN_REVIEW_RECEIPT_PIPELINE_V7_1.md
- docs/Y_HANDOFF_COMPILER_BRIDGE_V7_1.md
- docs/MJOLNIR_STRIKE_HANDOFF_BRIDGE_V7_1.md
- docs/HANDOFF_PROMPT_CANONICALIZATION_V7_1.md
- docs/HANDOFF_TO_UNIVERSAL_WORK_FLOW_V7_1.md
- docs/HANDOFF_POSTPROCESSING_CANDIDATE_PIPELINE_V7_1.md
- docs/THOR_Y_MJOLNIR_CONSOLIDATION_V7_1.md
- schemas/v7_1/
- registries/
- odin/shadow_runtime/
- examples/handoff/
- tests/test_thor_y_handoff_compiler.py

## Required Behavior

- Thor handoffs are kernel-bound, candidate-only and non-executing.
- Y handoffs preserve centerline, ring path, QIRC trace and smallest-sufficient-worker posture.
- Mjölnir focused strikes remain narrow candidate proposals requiring review.
- Prompt pull reduces ambiguity instead of expanding scope.
- Return packets are reviewed, not accepted as receipts.
- All handoff flows can compile to Universal Work or blocked/ask-context/split-work reports.
- Why Trace explains selected and rejected handoff routes.
- App-owned Apply remains the only path to state change.

## Forbidden Scope

- No agent swarm.
- No live chat loop.
- No autonomous action.
- No hidden execution.
- No returned-code execution.
- No auto-apply.
- No auto-merge.
- No claim acceptance.
- No receipt issuance by mediation alone.
- No runtime/deploy/security/prod-ready claim.

## Definition of Done

- All docs, schemas, registries, shadow modules and fixtures exist.
- Tests verify red lines and registry coverage.
- Internal task registry covers PR-73 through PR-80.
- Real PR bundle registry covers PR-73 through PR-80.
- Validate-all and pytest pass.

## Codex PR Summary Template

- Scope:
- Internal tasks covered:
- Handoff kinds added:
- Return contracts added:
- Boundary gates preserved:
- Tests run:
- Non-claims:

## Bundle Review Depth

Reviewers must verify that handoff compiler work reduces ambiguity and never increases authority. Thor, Y and Mjölnir lanes may have different semantic styles, but they must converge into the same Odin laws: candidate-only, app-owned apply, no hidden execution, no claim acceptance and full Why Trace. The bundle is incomplete if a handoff can bypass Universal Work, QIRC precompute, Odin Core/DFAS admissibility, model/agent capability cards, postprocessing, review gate or Candidate Artifact normalization.

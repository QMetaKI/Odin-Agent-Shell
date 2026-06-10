# REAL-PR-17 — AI-Git Safety Consolidation and Autonomy Boundary

## Objective

Consolidate Odin v7.1 as a Git-like control plane for AI work: candidate branches, semantic diffs, why traces, autonomy escalation gates, Maria/Michael safety superposition and app-owned apply boundaries.

## Internal Tasks Covered

- PR-56 — AI-Git Safety Architecture Consolidation
- PR-57 — Autonomy Escalation Gate Lock
- PR-58 — Safety Superposition Policy Lock
- PR-59 — Semantic Diff Branch Merge and Human Review Boundary
- PR-60 — Skynet Pattern Boundary and AI-Git Why Trace

## Primary Files

- docs/AI_GIT_SAFETY_ARCHITECTURE_V7_1.md
- docs/AUTONOMY_ESCALATION_GATE_V7_1.md
- docs/SAFETY_SUPERPOSITION_POLICY_V7_1.md
- docs/SEMANTIC_DIFF_BRANCH_MERGE_V7_1.md
- docs/SKYNET_PATTERN_BOUNDARY_V7_1.md
- docs/HUMAN_REVIEW_APP_APPLY_BOUNDARY_V7_1.md
- schemas/v7_1/odin_ai_git_safety_packet.schema.json
- registries/ai_git_safety_registry.json
- odin/shadow_runtime/ai_git_safety_shadow.py
- tests/test_ai_git_safety_consolidation.py

## Required Behavior

- Odin outputs remain candidate-only.
- App-owned apply remains the only apply path.
- Every autonomy escalation is gated.
- Every semantic merge remains candidate synthesis, not app mutation.
- Every high-risk candidate can carry Why Trace, Candidate DNA and Semantic Diff.
- Maria/Michael superposition is policy vector, not persona simulation.

## Forbidden Scope

- No hidden tool use.
- No external send by Odin.
- No public QIRC.
- No app-state mirror.
- No model-controlled runtime generation.
- No claim that all AI risk is impossible.

## Definition of Done

- All PR-56 through PR-60 docs exist.
- All new schemas and registries are present.
- Shadow Runtime modules exist and tests cover allow/block cases.
- Codex task registry covers PR-56 through PR-60.
- Real PR bundle registry covers PR-56 through PR-60 in REAL-PR-17.
- `python -m odin.cli validate-all` passes.
- `python -m pytest -q -p no:cacheprovider` passes.

## Codex PR Summary Template

```text
Implemented REAL-PR-17 AI-Git Safety Consolidation.
Added autonomy escalation gate, safety superposition, semantic diff/branch/merge, human review/app apply boundary and Skynet pattern boundary docs/schemas/registries/shadow tests.
Preserved candidate-only/app-owned-apply/local-first boundaries.
```


## Bundle Review Expansion

This real PR bundle is the point where Odin's safety story becomes mechanically reviewable. It must not be implemented as a public claim or branding layer. It must be implemented as concrete docs, schemas, registries, shadow modules, fixtures and tests. The final reviewer must be able to answer these questions from repository artifacts alone:

1. Which route produced the candidate?
2. Which routes were blocked and why?
3. Which autonomy level was requested?
4. Which gate reduced or blocked unsafe output?
5. Which app-owned review or apply boundary remains?
6. Which Maria/Michael safety posture was active?
7. Which Candidate DNA and Why Trace records connect the output to its source?

## Bundle Negative Gates

The bundle is not complete if any of the following are true:

- A model response can imply that an action was already applied.
- A runtime pack can load without validation.
- A semantic bus event can mutate app state.
- A candidate merge can be treated as app apply.
- Fairy or Y* prose can produce executable behavior without typed validation.
- A trace can be omitted for high-risk work.

## Bundle Acceptance Statement

REAL-PR-17 is complete only when Odin's AI-Git metaphor is backed by enforceable structures: semantic branch, semantic diff, candidate merge, autonomy gate, safety superposition, Why Trace and human/app-owned apply boundary.

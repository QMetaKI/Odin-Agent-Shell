# PR-66 — Universal Model / Agent Parity Matrix

## Objective

Generalize ChatGPT/Odin twin parity to all model and agent surfaces.

## Primary Files

- docs/
- schemas/v7_1/
- registries/
- odin/shadow_runtime/
- tests/
- SYSTEM_MAP.json
- FILE_MANIFEST.json

## Required Behavior

- Preserve v7.1 candidate-only rules.
- Treat every model and agent as a bounded worker.
- Require Capability Cards and Permission Cards for every worker class.
- Normalize all worker output into Candidate Artifacts.
- Preserve App-owned Apply and external-send boundaries.
- Preserve Why Trace, Semantic Diff and Candidate DNA.
- Update internal PR ladder and real PR bundle coverage.

## Forbidden Scope

- No app mutation.
- No autonomous external send.
- No provider-specific bypass.
- No hidden tool/action channel.
- No persona-authority inflation.
- No unvalidated runtime-pack or adapter load.

## Definition of Done

- Documentation updated.
- Schemas present and JSON-valid.
- Registries include the new contract surfaces.
- Shadow Runtime module exists.
- Test coverage validates file presence and red lines.
- `python -m odin.cli validate-all` passes.
- `python -m pytest -q -p no:cacheprovider` passes.

## Codex PR Summary Template

- Scope:
- Files changed:
- Tests run:
- Boundaries preserved:
- Known non-claims:
- Follow-up:

## Notes

This task belongs to REAL-PR-19. The goal is universal parity for model and agent workers, not model-specific behavior. The architecture must keep Odin as the controller of candidate work and keep all app-authority outside Odin.


## Detailed Implementation Notes

Codex must treat this task as a mechanical boundary-expansion step. The implementation may add adapters, cards, schemas, registries, fixtures and tests, but it must not introduce real model calls or agent execution in the prep repository. Every worker class must be normalized into a bounded Odin candidate relation. This means the adapter must prove what the worker is allowed to read, what kind of candidate it may return, what permission card applies, which routes are blocked, which gates ran, and which app-owned apply boundary remains in force.

The task must update system-map visibility, Codex ladder coverage, real-bundle coverage and shadow-runtime mapping. Any new worker family must appear in a registry and must have an explicit non-authority statement. Raw provider behavior must never be treated as truth. If a worker emits an action-like output, Codex must convert it to an Action Card Candidate, PatchPlan Candidate, Research Candidate, Review Candidate or Blocked Route Report. No generated or external agent response may claim that it applied, sent, deleted, deployed, purchased, verified runtime, passed tests or completed production readiness.

The senior-review expectation is that this task reduces provider-specific branching. A good implementation has one normalized path and small provider adapters. A bad implementation adds separate special cases for every model brand, coding assistant or research agent. The correct path is: model/agent card -> permission card -> work capsule -> adapter boundary -> candidate protocol -> why trace -> app apply boundary.

## Additional Acceptance Detail

- The task must be deterministic under repeated validation.
- Every new schema must be parseable JSON Schema.
- Every new registry must include registry_id and version.
- Every added shadow module must declare candidate_only true and app_apply false.
- Every added fixture must preserve blocked-action examples.
- Every added doc must state that Odin is not app authority and not agent authority.
- The real implementation target must be a later Codex step, not an implied runtime claim.

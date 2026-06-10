# PR-96 — Shadow Narrative to Gate Compiler

## Objective
Implement Shadow Narrative to Gate Compiler as part of v0.7.0 Shadow Narrative / Loki / Anti-Pattern Lock.

## Internal Tasks Covered
- PR-96

## Primary Files
- docs/SHADOW_NARRATIVE_TO_GATES_V7_1.md
- registries/shadow_to_gate_registry.json
- odin/shadow_runtime/shadow_narrative_to_gate_shadow.py

## Required Behavior
- Preserve candidate-only semantics.
- Treat Shadow Narrative as typed negative IR, not executable prose.
- Map every anti-pattern to signal, gate, negative fixture, repair route and Why Trace note.
- Loki may reveal ambiguity but must not become authority.
- Update schemas, registries, tests, System Map and FILE_MANIFEST.

## Forbidden Scope
- No prose-only execution.
- No app-state mutation.
- No external send.
- No Loki authority escalation.
- No Odin Final Gate bypass.
- No unvalidated runtime pack load.
- No GPL-2.0-only weakening.

## Definition of Done
- python -m odin.cli validate-all passes.
- pytest suite completes successfully.
- Required docs, schemas, registries, fixtures and shadow modules are present.
- Negative tests prove unsafe narrative paths are blocked.
- PR remains bounded to declared files and behavior.

## Codex PR Summary Template
```text
PR-96: Shadow Narrative to Gate Compiler
Summary:
Validation:
Risks:
Boundaries preserved:
```

## Detailed Implementation Notes
Codex must implement this task mechanically from the shadow module and schema. The implementation should prefer deterministic registry and gate logic before model calls. Any unresolved narrative hole must become an explicit hole field, not implicit behavior. If a Shadow Narrative conflicts with Odin Core, Bug6, Q7, App Apply Boundary, Claim Boundary or GPL-2.0-only policy, the harder boundary wins. The correct implementation creates more explainability and safer negative paths without turning Odin into a pessimistic blocker.


## Extended Codex Notes
The PR must preserve Odin v7.1 as a bounded AI-Git layer. Shadow Narrative and Loki are not agents, not executors and not reviewers with authority. The implementation must keep every artifact candidate-only and must route every negative pattern through a typed signal, an explicit gate, a fixture, a repair route and a Why Trace annotation. The purpose is not to make Odin more negative; the purpose is to reveal hidden failure paths early enough that small models, large models and external agents receive safer, narrower work. Codex must update registries, schemas, fixture coverage, shadow contracts and bundle coverage in the same change. If a new anti-pattern appears without a machine-readable gate mapping, Codex must leave it as documentation-only and mark the hole explicitly.

## Review Checklist
- Does the task add or preserve a schema?
- Does the task add or preserve a registry entry?
- Does the task include at least one valid or invalid fixture?
- Does the task preserve app-owned apply?
- Does the task preserve no-Loki-authority?
- Does the task preserve no prose-only execution?
- Does the task preserve GPL-2.0-only identity?

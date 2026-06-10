# Senior Review Remediation Plan v0.4.2

## Purpose

This document turns the Senior Reviewer Simulation into persistent build obligations.

The plan does not replace Master Architecture v7.1 or Master Specs v7.1. It adds an anti-drift layer so Codex can implement without weakening the canon.

## Remediation Table

| ID | Finding | Remediation | Internal Task | Real Bundle | Gate |
|---|---|---|---|---|---|
| SR-01 | Traceability drift | Add traceability matrix and PR summary checklist | PR-22 | REAL-PR-08 | Senior Review Gate |
| SR-02 | Semantic bus authority drift | Add semantic bus red-line policy | PR-22 | REAL-PR-08 | Bus Boundary Gate |
| SR-03 | Model escalation drift | Add model escalation decision requirement | PR-22 | REAL-PR-08 | Model Route Gate |
| SR-04 | Candidate status drift | Add candidate-only surface checklist | PR-22 | REAL-PR-08 | Candidate Output Gate |
| SR-05 | Low-memory ambiguity | Add Low-Memory Strict enforcement checklist | PR-22 | REAL-PR-08 | Resource Profile Gate |
| SR-06 | Support bundle privacy | Add redaction default checklist | PR-22 | REAL-PR-08 | Privacy Gate |
| SR-07 | Bundle review breadth | Add internal-task checklist per bundle | PR-22 | REAL-PR-08 | Bundle Gate |
| SR-08 | Runtime overclaim | Add release-note claim-boundary checklist | PR-22 | REAL-PR-08 | Claim Gate |

## Required Repository Updates

Every future architecture, implementation or documentation change must update all affected surfaces:

```text
Architecture / Specs
Schemas
Registries
Internal PR ladder
Real PR bundle plan
Tests / Gates
SYSTEM_MAP.json
FILE_MANIFEST.json
```

## Required Real PR Summary Addendum

Every real Codex PR must include:

```text
Architecture sections touched:
Specs touched:
Internal tasks touched:
Real bundle:
Schemas changed:
Registries changed:
Tests added/changed:
Invariants preserved:
Candidate-only status preserved: yes/no
App-owned apply preserved: yes/no
Semantic bus local-only preserved: yes/no
Model escalation discipline preserved: yes/no
Claim boundary preserved: yes/no
```

## Non-Negotiable Senior Review Invariants

```text
No LLM in App.
Candidate-only outputs.
App owns state/apply/external send.
Odin owns LLM preparation and candidate construction.
Semantic Bus is local-only coordination.
3B + 7B/8B hybrid remains default sweet spot.
Bigger models are escalation routes only.
Remote is explicit opt-in only.
Support bundles are redacted by default.
Runtime claims require receipts.
```

## Close Criteria

The remediation is considered locked when:

- PR-22 exists.
- PR-22 is covered by REAL-PR-08.
- `registries/codex_task_registry.json` includes PR-22.
- `registries/codex_pr_bundle_registry.json` maps PR-22 into a real bundle.
- `docs/TRACEABILITY_MATRIX_V7_1.md` exists.
- `docs/CODEX_ANTI_DRIFT_POLICY.md` exists.
- validation and tests pass.

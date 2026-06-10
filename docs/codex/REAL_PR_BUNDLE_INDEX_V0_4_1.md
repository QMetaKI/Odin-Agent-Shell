# Codex Real PR Bundle Index v0.4.1

Status: bundle overlay on top of v0.4.0 internal PR ladder.

The existing PR-00 through PR-21 tasks remain the internal fine-grained ladder. They are not deleted, renamed, or weakened. v0.4.1 adds the practical future Codex PR grouping that should be used when opening real pull requests.

## Rule

Use REAL-PR bundles as actual pull request units. Use PR-00 through PR-21 as internal checklist items inside those bundles.

## Bundle Table

| Real PR | Title | Internal Tasks | Depends On |
|---|---|---|---|
| REAL-PR-01 | Foundation, Canon Gates, Schemas, Protocol Boundary | PR-00, PR-01, PR-02 | - |
| REAL-PR-02 | Universal Work and Candidate Core | PR-03, PR-04 | REAL-PR-01 |
| REAL-PR-03 | Internal Semantic Bus, Lenses, Context and Worklets | PR-05, PR-06, PR-07 | REAL-PR-02 |
| REAL-PR-04 | Model Routing, Mock Provider, Small-Model Core and Low-Memory Mode | PR-08, PR-09, PR-14, PR-15 | REAL-PR-03 |
| REAL-PR-05 | Thor Bridge, Bounded Code Work, Storage and Local API | PR-10, PR-11, PR-12 | REAL-PR-04 |
| REAL-PR-06 | SDKs, App Templates and App-QIRC Digest Bridge | PR-13, PR-16 | REAL-PR-05 |
| REAL-PR-07 | Model Dojo, Scoreboard, Control Center and Windows Runtime Prep | PR-17, PR-18, PR-19 | REAL-PR-06 |
| REAL-PR-08 | End-to-End Golden Flows, Release Prep Hygiene and Support Bundle | PR-20, PR-21 | REAL-PR-07 |

## Invariants

- Do not collapse candidate-only boundaries to implementation convenience.
- Do not let app templates contain LLM runtime or model routing.
- Do not make the semantic bus public or network-facing by default.
- Do not hardcode hardware names into model routing; use measured resource posture.
- Do not skip internal PR ladder checks just because a bundle is broader.

# v0.4.2 Bundle Index Addendum

```text
REAL-PR-08 = PR-20 + PR-21 + PR-22
```


## v0.5.0 Shadow Runtime Bundle Addition

- `REAL-PR-09` covers `PR-23` and locks the code-near Shadow Runtime Mechanical Build Bridge.


## v0.5.1 Full Shadow Runtime Coverage Update

- Added PR-24 — Full Shadow Runtime Coverage.
- Added REAL-PR-10 — Full Shadow Runtime Coverage.
- Rule: all future changes must update architecture/specs, internal PR ladder, REAL-PR bundle registry, shadow contract registry, System Map, tests and FILE_MANIFEST.


## v0.7.0 Shadow Narrative / Loki / Anti-Pattern Lock

Adds PR-93 through PR-97 and REAL-PR-23 for typed narrative anti-patterns, Loki mediation, gate mapping and narrative red-team fixtures. Candidate-only and no-Loki-authority boundaries are mandatory.

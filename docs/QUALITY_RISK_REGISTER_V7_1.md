# Quality and Risk Register v7.1

## Purpose

This register lists risks that must stay visible during implementation.

## Risk Levels

```text
Critical = can break Odin authority model
High = can break candidate-only or local-first behavior
Medium = can degrade usability or maintainability
Low = documentation or polish risk
```

## Register

| ID | Risk | Level | Mitigation | Owner Task |
|---|---|---:|---|---|
| R-001 | App templates accidentally include LLM provider logic | Critical | no-LLM-in-app scan and app template review | PR-13 |
| R-002 | Semantic Bus becomes app-state owner | Critical | bus boundary gate and local-only channel validation | PR-05 |
| R-003 | Response packets imply applied state | Critical | candidate-only gate and action contract | PR-04 |
| R-004 | Larger models become default route | High | model ladder tests and default-route assertion | PR-08 |
| R-005 | Remote route enabled silently | High | caller manifest and provider policy gate | PR-14 |
| R-006 | Support bundle leaks raw payloads | High | redaction by default and explicit export mode | PR-21 |
| R-007 | Low-memory mode attempts heavy local route | High | resource profile gate | PR-15 |
| R-008 | Candidate DNA omitted | Medium | response packet and trace tests | PR-04 |
| R-009 | Registries drift from schemas | Medium | registry parity validation | PR-01 |
| R-010 | Real PR bundle too broad for review | Medium | internal task checklist per bundle | PR-22 |
| R-011 | Control Center weakens boundary labels | Medium | UI copy review and candidate status chips | PR-18 |
| R-012 | Provider adapters overclaim model quality | Medium | Model Dojo profiles are local observations only | PR-17 |
| R-013 | API endpoint performs hidden apply | Critical | API test matrix and final gate | PR-12 |
| R-014 | App QIRC bridge mirrors too much | High | digest-only bridge validator | PR-16 |
| R-015 | Release notes imply completed runtime proof | High | claim-boundary release checklist | PR-21 |

## Review Rule

Before merging a real PR bundle, any risk touched by the bundle must be listed in the PR summary with mitigation evidence.

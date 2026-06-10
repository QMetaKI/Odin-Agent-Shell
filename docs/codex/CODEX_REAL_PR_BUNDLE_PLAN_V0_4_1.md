# Codex Real PR Bundle Plan v0.4.1

## Purpose

v0.4.0 intentionally defined PR-00 through PR-21 as a fine-grained internal implementation ladder. That ladder is excellent for sequencing and review discipline, but too granular for future real pull requests in the public repository.

v0.4.1 adds a bundle layer:

```text
REAL-PR bundles = actual future Codex pull requests
PR-00..PR-21 = internal checklist/tasks inside each bundle
```

## Operating Model

Codex should open a real PR per REAL-PR bundle, not a real PR for every internal task unless the bundle grows too large during implementation. Each real PR must still complete all mapped internal tasks and run their required tests.

## Bundle Discipline

Each REAL-PR must include:

- objective
- internal tasks covered
- dependency boundary
- primary files
- required behavior
- forbidden scope
- required tests
- documentation touched
- summary template
- rollback notes
- claim boundary review

## Split Rule

A REAL-PR may be split only if:

- it becomes too large for review,
- a dependency was mis-estimated,
- a subsystem requires isolated runtime proof,
- or CI failures indicate a cleaner boundary is required.

If split, preserve the internal PR task mapping and update `registries/codex_pr_bundle_registry.json`.

## Merge Rule

A REAL-PR may only be merged when:

- `python -m odin.cli validate-all` is green,
- `python -m pytest -q -p no:cacheprovider` is green,
- all internal task DoD rows mapped to the bundle are satisfied,
- no forbidden scope item was introduced,
- documentation and registry references remain in parity,
- and claim boundaries are preserved.

# v0.4.2 Bundle Plan Addendum

REAL-PR-08 now includes PR-22 Senior Review Hardening and Anti-Drift Lock. This keeps the real PR bundle count stable while ensuring final release-prep includes senior review remediation.


## v0.5.0 Shadow Runtime Bundle Addition

- `REAL-PR-09` covers `PR-23` and locks the code-near Shadow Runtime Mechanical Build Bridge.


## v0.5.1 Full Shadow Runtime Coverage Update

- Added PR-24 — Full Shadow Runtime Coverage.
- Added REAL-PR-10 — Full Shadow Runtime Coverage.
- Rule: all future changes must update architecture/specs, internal PR ladder, REAL-PR bundle registry, shadow contract registry, System Map, tests and FILE_MANIFEST.


## v0.7.0 Shadow Narrative / Loki / Anti-Pattern Lock

Adds PR-93 through PR-97 and REAL-PR-23 for typed narrative anti-patterns, Loki mediation, gate mapping and narrative red-team fixtures. Candidate-only and no-Loki-authority boundaries are mandatory.

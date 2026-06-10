# Codex Senior Review Addendum v0.4.2

## Rule

PR-00..PR-22 are now the internal implementation ladder. REAL-PR-01..REAL-PR-08 are the real future Codex PR bundles.

## New Internal Task

```text
PR-22 Senior Review Hardening and Anti-Drift Lock
```

## Bundle Mapping

PR-22 belongs to:

```text
REAL-PR-08 End-to-End Golden Flows, Release Prep Hygiene and Support Bundle
```

## Why PR-22 Is Not a Separate Real Bundle

Senior review hardening is a release-prep and anti-drift layer. It belongs with final golden-flow and support-bundle hardening rather than creating a new user-visible subsystem.

## Required Codex Behavior

Codex must keep both layers synchronized:

```text
Internal task ladder: PR-00..PR-22
Real review bundles: REAL-PR-01..REAL-PR-08
```

Any future addition must modify both layers and must be covered by validation.

## Codex Execution Notes

PR-22 should be executed as a final hardening pass after PR-21. It is not a feature PR and must not introduce model providers, API behavior, UI behavior or Windows runtime changes. Its purpose is to make the repository harder to misbuild.

Required outputs:

```text
senior review docs
anti-drift docs
traceability docs
risk docs
updated registries
updated validation
updated tests
updated manifest
```

Codex must use PR-22 as a checklist when preparing the future public repository. If a later real PR adds a new subsystem, route, mode or bridge, the same pattern applies: update the internal ladder, update the real bundle mapping, update docs, update registries, update tests and refresh the manifest.

## Preservation Rule

The senior review addendum preserves the existing architecture. It does not replace the Master Architecture, Master Specs, Deep Subsystem Specs or Codex Task Lock. It makes the whole stack more resistant to implementation drift.

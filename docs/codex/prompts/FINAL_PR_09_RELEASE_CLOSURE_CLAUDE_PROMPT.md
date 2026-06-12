# FINAL-PR-09: Release / Closure / Full Acceptance

## Purpose / Objective

FINAL-PR-09 runs after FINAL-PR-06, FINAL-PR-07, and FINAL-PR-08. It verifies full acceptance and binds docs, validators, proof chain, release checklist, and claim boundaries.

## Base rule

Base: current main after FINAL-PR-08 merge. Do not base on open PR branches. Do not rewrite historical merged PRs.

## Allowed scope

Release / Closure / Full Acceptance verification, documentation binding, validator aggregation, proof-chain binding, release checklist updates, acceptance definition updates, and claim-boundary checks.

## Forbidden scope

Do not add new architecture unless required to fix closure gaps. No provider execution, model inference, API key reads, external network, public QIRC/network/federation, no app apply, app state mutation, external send, production readiness claim without receipts, security certification claim, hidden authority, religious interpretation, persona injection, or source-pattern runtime import.

## Files to create

The final prompt must be completed in FINAL-PR-09. Expected categories: release checklist, full acceptance report, proof-chain report, senior review, code review, and final return report.

## CLI commands

The full FINAL-PR-09 prompt must specify exact validator and proof commands after PR06..08 land.

## Validator requirement

The full FINAL-PR-09 prompt must specify release/closure validators and include `python -m odin.cli validate-all`.

## Tests requirement

The full FINAL-PR-09 prompt must specify focused and full pytest commands.

## Proof packet requirement

The full FINAL-PR-09 prompt must specify a release/closure proof packet and proof-chain integration.

## Senior review loop

Before finalizing FINAL-PR-09, simulate senior reviewer and senior code reviewer. Apply fixes before the final response.

## Final response format

Return release/closure findings, acceptance state, non-claims, blockers, and exact tests run. Each test/check command must be prefixed with pass/warn/fail status.

# PREP FINAL-PR-06..08 Operational Seed / DFAS / Projection Plan

Artifact id: `prep_final_pr_06_08_operational_seed_dfas_projection_plan`.

Claim boundary: planning-only. This artifact prepares implementation prompts and validation acceptance for future PRs. It is not runtime, provider/model execution, public network, app apply/state/external-send, production readiness, security certification, or release proof.

## Roadmap amendment

- FINAL-PR-06: Operational Seed Spine + Role Profiles + Seed-to-Work-Capsule Compiler.
- FINAL-PR-07: DFAS Field Selection + Coherence / Review Axes + Route Scoring.
- FINAL-PR-08: Projection Spine + Expression Packet + Shadow Candidate Graph.
- FINAL-PR-09: Release / Closure / Full Acceptance.

PR06..09 are not complete. This prep PR only prepares handoff artifacts, validators, and tests.

## FINAL-PR-06 objective

Implement neutral operational intent seeds, role profiles, seed packs, seed routes, and a seed-to-work-capsule compiler that improves Handoff Context quality, Universal Work preparation, ModelWorkPacket preparation, Work Capsule generation, QIRC/event routing hints, and local worker token efficiency.

## FINAL-PR-07 objective

Implement deterministic DFAS-derived field selection, dominance and suppression metadata, coherence scores, review axes, route scoring, hole density, and center-first routing.

## FINAL-PR-08 objective

Implement projection layers that map a selected seed/field route into human-clear projection, expression packet, machine projection, shadow candidate graph, materialization bridge, and projection receipt.

## FINAL-PR-09 release / closure objective

Run final acceptance only after PR06..08. Bind docs, validators, proof chain, release checklist, and claim boundaries. Do not add new architecture unless required to close release gaps.

## Dependencies

- FINAL-PR-06 depends on this prep PR and existing FINAL-PR-05 baseline.
- FINAL-PR-07 depends on FINAL-PR-06.
- FINAL-PR-08 depends on FINAL-PR-07.
- FINAL-PR-09 depends on FINAL-PR-06, FINAL-PR-07, and FINAL-PR-08.

## Non-goals

- No PR06..08 runtime implementation in this prep PR.
- No provider execution or model inference.
- No API key reads.
- No public network, public QIRC, federation, or remote calls.
- No app apply, app state mutation, or external send.
- No production readiness or security certification claim.
- No hidden authority, religious interpretation, persona injection, or source-pattern runtime import.

## Allowed scopes

Docs, registries, reports, prep validator, prep tests, CLI hook, `SYSTEM_MAP.json`, and `FILE_MANIFEST.json`.

## Forbidden scopes

Runtime implementations for `odin/operational_seed_spine/`, `odin/field_selection/`, and `odin/projection_spine/` in this prep PR; provider/model execution; network/public federation; app authority.

## Expected files, CLI, validators, tests, proof packets, audits

The machine-readable registry `registries/prep_final_pr_06_08_plan.v1.json` is authoritative for expected files, CLI commands, validators, tests, proof packets, and audits. Future PRs must produce their own reports and must not mark PR06..09 complete in this prep PR.

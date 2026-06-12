# PREP FINAL-PR-06..08 Repo Reality Intake

Artifact id: `prep_final_pr_06_08_repo_reality_intake`.

Claim boundary: repo-real planning evidence only. This intake does not implement FINAL-PR-06, FINAL-PR-07, FINAL-PR-08, or FINAL-PR-09 runtime behavior. It does not prove runtime, provider execution, model inference, app apply, app state mutation, external send, public network, production readiness, or security certification.

## Current main/base SHA

- Requested base rule: use current `main` after latest merged PR.
- Workspace reality: no `main` ref and no remote are present in this container; `git checkout main` could not resolve a branch. The prep branch was created from the available repo-real worktree head.
- Base SHA observed before edits: `a58c6f6dddab803c427149e7696d9361bb52790c`.
- Branch created: `codex/prepare-final-pr-06-08-seed-dfas-projection`.

## Prior FINAL PRs present

- FINAL-PR-01 Simple Local Hub artifacts are present: `odin/local_hub/`, docs/reports, registry, tests, and CLI validator.
- FINAL-PR-02 Model Apps Demo artifacts are present: model picker, connected apps, demo Universal Work docs/reports, registry, tests, and CLI validator.
- FINAL-PR-03 QIRC Core / Dev Mode artifacts are present: `odin/qirc_core/`, Dev Mode reports/audits, registry, tests, and CLI validator.
- FINAL-PR-04 Provider Probe / Runtime Security artifacts are present: `odin/providers/`, `odin/runtime_security/`, reports/audits, registry, tests, and CLI validator.
- FINAL-PR-05 Execution Gate artifacts are present: `odin/execution_gate/`, `odin/proof_chain/`, `odin/final_pr_ladder/`, reports/audits, registry, tests, and CLI validator.

## Existing surfaces

- `odin/y_pattern_spine/` exists and is treated as available repo-real baseline where future prompts may reference the neutral Y Pattern precondition without depending on an open branch.
- `odin/proof_chain/` exists and provides a proof chain aggregation surface for future proof packets.
- `odin/execution_gate/` exists and preserves mock-only/local-candidate-blocked boundaries.
- `odin/shadow_runtime/` exists with candidate-only shadow modules, including seed, handoff, candidate, DFAS-adjacent, and work capsule scaffolds.
- Historical seed/archetype/DFAS/projection concepts are present in docs, registries, schemas, and shadow modules, but not as the neutral PR06..08 runtime modules requested here.

## Existing seed / role / profile / DFAS / projection surfaces found

- Seed-related: `odin/seeds/`, `registries/seed_registry.json`, `registries/operational_seed_function_registry.json`, `registries/operational_seed_substrate_registry.json`, seed pack compiler registries, app seed pack surfaces, and shadow seed modules.
- Role/profile-related: `registries/archetype_role_registry.json`, `registries/agent_operator_profile_registry.json`, and historical role/archetype docs.
- DFAS/field-adjacent: `docs/DFAS_STABILITY_CORE_V7_1.md`, `odin/shadow_runtime/dfas_stability_core_shadow.py`, centerline, qmath score, resonance band, and route scoring registries.
- Projection/shadow-adjacent: `odin/shadow_runtime/candidate_shadow.py`, narrative compiler docs/registries, fairy/narrative shadow modules, and ModelWorkPacket / Candidate Artifact surfaces.

## Missing operational seed surfaces

The repo does not yet contain neutral implementation modules for `odin/operational_seed_spine/`, `odin/field_selection/`, or `odin/projection_spine/`. It also does not yet contain the requested PR06..08 validators, proof packets, tests, and Claude-Code-ready prompts.

## Release / closure gap summary

FINAL-PR-05 currently points at release/closure-like follow-up work, but the repo-real audits identify gaps before closure: operational intent seed preparation, deterministic field/route explanation, review axes, hole-density checks, and expression-level projection candidate structure. Moving closure to FINAL-PR-09 gives these layers bounded PR slots before full acceptance.

## Why PR06..08 are justified

- FINAL-PR-06 improves Handoff Context quality, Work Capsule generation, Universal Work preparation, ModelWorkPacket preparation, QIRC/event routing hints, and local worker token efficiency without granting seed authority.
- FINAL-PR-07 improves route selection and reviewer explanation with deterministic field selection, coherence scores, review axes, route scores, dominance/suppression metadata, and hole-density signals without granting apply/model/external-send authority.
- FINAL-PR-08 improves human-clear and machine-near candidate preparation through projection spine, expression packet, materialization bridge, and shadow candidate graph without treating projection as code truth, model truth, or runtime proof.

## Files to create

- Prep handoff, pattern-mine synthesis, master prep plan, JSON registry/report artifacts.
- Claude-Code-ready prompt files for FINAL-PR-06, FINAL-PR-07, FINAL-PR-08, and a skeleton prompt for FINAL-PR-09.
- Prep validator, CLI hook, and tests.
- Senior review, code review, roadmap audit, return report, system map entry, and file manifest entries.

## Files to avoid

- No new PR06..08 runtime packages in `odin/operational_seed_spine/`, `odin/field_selection/`, or `odin/projection_spine/` in this prep PR.
- No provider/model execution code.
- No public network/federation code.
- No app apply, app state mutation, or external-send code.
- No source-pattern runtime import.

## Non-claims

- Not runtime completion proof.
- Not provider execution proof.
- Not model inference proof.
- Not app apply/state/external-send authority.
- Not public network proof.
- Not production readiness.
- Not security certification.
- Not source-pattern authority.
- Not religious interpretation.
- Not hidden authority.

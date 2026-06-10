# REAL-GH-PR-06 — Odin Core, QIRC Gold Spine, Seeds, Pattern Mines and Flow Packs

## Objective

Implement Odin Core Centerline, QLI/DFAS/QMath route scoring, QIRC Gold Spine, Bug6/Q7 invariant layer, operational seed/archetype substrate, App Seed Pack compiler, Pattern Mine intake and Flow Pack bridge.

## Position in the Real Execution Chain

- Execution PR: `REAL-GH-PR-06`
- Depends on: REAL-GH-PR-05
- Legacy internal tasks covered: PR-38, PR-39, PR-40, PR-41, PR-42, PR-43, PR-44, PR-45, PR-46, PR-47, PR-48, PR-49, PR-50, PR-51, PR-52, PR-53, PR-54, PR-55, PR-87, PR-88, PR-89, PR-90, PR-91, PR-92, PR-103, PR-104, PR-105, PR-106, PR-107, PR-121

This document is the Codex-facing real GitHub PR bundle. The older `PR-00..PR-123` task ladder and the older `REAL-PR-01..REAL-PR-28` bundle ladder are retained as internal planning detail only. Codex should build from this document when executing the real repository sequence.

## Internal Tasks Covered

- `PR-38` — Odin Core Centerline and QLI Master Interface
- `PR-39` — DFAS Stability Core and Admissibility Gate
- `PR-40` — Seed / Archetype Economy and Conflict Resolver
- `PR-41` — QMath Center Solver and Route Score Engine
- `PR-42` — Ring Radar / Resonance / Why Trace
- `PR-43` — Maria / Michael Superposition Policy
- `PR-44` — QFoundation / Q Metamodell Intake Binding
- `PR-45` — QIRC Gold Spine Channel Taxonomy
- `PR-46` — QIRC Event Envelope v2 and Hot Window Memory
- `PR-47` — QIRC Seed / Archetype Prewarm and Budget Gates
- `PR-48` — QIRC Admissibility / QMath / Ring Radar Flow
- `PR-49` — QIRC Why Trace and Runtime Pack Integration
- `PR-50` — Bug6 / Q7 invariant lock
- `PR-51` — Y-Core posture lock
- `PR-52` — Operational seed substrate lock
- `PR-53` — Seed / archetype synthesis lock
- `PR-54` — Fairy / Y* seed binding lock
- `PR-55` — Shadow Runtime seed weave and runtime pack seed profiles
- `PR-87` — App Seed Pack Compiler Core
- `PR-88` — Universal Seed Pack Format and Manifest Validation
- `PR-89` — Operational Seed Functions and Security Boundary
- `PR-90` — Seed Pack to Runtime Pack Compiler
- `PR-91` — Seed Pack Composition Conflict and Capability Slices
- `PR-92` — Seed Pack Why Trace and Use Case Matrix
- `PR-103` — Pattern Mine Manifest and Claim Boundary
- `PR-104` — Flow Pack Compiler and Seed Pack Bridge
- `PR-105` — Pattern Spine Compiler
- `PR-106` — Pattern Mine Intake Shadow and Fixtures
- `PR-107` — Pattern Mine Runtime Pack Integration
- `PR-121` — Seed Pattern Pack Security Certification

## Primary Files

- `odin/core/`
- `odin/qirc/`
- `odin/seeds/`
- `odin/patterns/`
- `odin/flow_packs/`
- `registries/qirc_*`
- `registries/seed_*`
- `registries/pattern_*`
- `registries/flow_pack_registry.json`
- `docs/ODIN_CORE_CENTERLINE_V7_1.md`
- `docs/APP_SEED_PACK_COMPILER_V7_1.md`
- `docs/PATTERN_MINE_FLOW_PACK_INTAKE_LOCK_V7_1.md`
- `tests/`

## Required Behavior

- centerline/admissibility gates run before dispatch
- QIRC stays local/internal and trace-bound
- seed and pattern packs are declarative, signed/classified or review-required
- Pattern Mines compile to pattern spines/flow packs without becoming truth authority

## Forbidden Scope

- no executable seed pack code
- no religious/domain truth leakage from pattern mines
- no QIRC network expansion
- no unbounded seed fanout
- no bypass of Odin final gate

## Acceptance / Definition of Done

- seed pack invalid executable example fails closed
- pattern mine claim-boundary examples validate
- QIRC event envelope requires trace_id
- Bug6/Q7 gates remain present in route decisions

Additional Definition of Done:

- `python -m odin.cli validate-all` returns no errors.
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider` returns a green suite.
- No new file claims runtime proof, host validation, production status, network proof, model-inference proof, security certification, or app-apply authority.
- All created schemas, registries, fixtures, docs and tests are included in `FILE_MANIFEST.json`.
- The PR summary explicitly separates implemented code, shadow/prep contracts, fixtures, validation results, and known proof gaps.

## Codex PR Summary Template

```text
{b['id']} — {b['title']}

Scope:
- ...

Implemented:
- ...

Validation:
- python -m odin.cli validate-all: ...
- PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider: ...

Proof gaps / non-claims:
- no runtime proof unless actually executed on host
- no model-inference proof unless actual local/remote model run is evidenced
- no app-apply authority for Odin
```

## Senior Reviewer Notes

This PR is intentionally large enough to be real-reviewable as a GitHub PR but not so large that unrelated runtime, Windows, model and release concerns are mixed without a dependency boundary. Do not split it back into the internal micro-ladder unless Codex is blocked by file-size or review-size constraints.
---

## v0.7.7 Build Ladder Absolute Alignment Addendum


This addendum is authoritative for the actual GitHub execution ladder. It separates existing prep files from target implementation paths and binds this PR to Master Architecture v7.1.

### Absorbed Internal Tasks

- `PR-38`
- `PR-39`
- `PR-40`
- `PR-41`
- `PR-42`
- `PR-43`
- `PR-44`
- `PR-45`
- `PR-46`
- `PR-47`
- `PR-48`
- `PR-49`
- `PR-50`
- `PR-51`
- `PR-52`
- `PR-53`
- `PR-54`
- `PR-55`
- `PR-87`
- `PR-88`
- `PR-89`
- `PR-90`
- `PR-91`
- `PR-92`
- `PR-103`
- `PR-104`
- `PR-105`
- `PR-106`
- `PR-107`
- `PR-121`

### Absorbed Legacy Bundles

Full absorption:

- `REAL-PR-14`
- `REAL-PR-15`
- `REAL-PR-16`
- `REAL-PR-22`
- `REAL-PR-25`

Partial absorption:

- `REAL-PR-28` — covers PR-121 of 8 internal tasks

### Existing Prep Files / Paths

- `odin/core/`
- `registries/flow_pack_registry.json`
- `docs/ODIN_CORE_CENTERLINE_V7_1.md`
- `docs/APP_SEED_PACK_COMPILER_V7_1.md`
- `docs/PATTERN_MINE_FLOW_PACK_INTAKE_LOCK_V7_1.md`
- `tests/`

### Target Implementation Files / Paths

- `odin/qirc/`
- `odin/seeds/`
- `odin/patterns/`
- `odin/flow_packs/`
- `registries/qirc_*`
- `registries/seed_*`
- `registries/pattern_*`

### Master Architecture Sections

- `Odin Core / QLI / DFAS`
- `QIRC Gold Spine`
- `Seed/Archetype Economy`
- `Pattern Mine / Flow Pack Intake`

### Acceptance Gates

- `seed pack invalid executable example fails closed`
- `pattern mine claim-boundary examples validate`
- `QIRC event envelope requires trace_id`
- `Bug6/Q7 gates remain present in route decisions`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`
- `every created or updated artifact is registered in FILE_MANIFEST.json`
- `all proof gaps and non-claims are stated in the PR summary`

### Must Run

- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`

### Must Preserve

- `no_llm_in_app`
- `candidate_only`
- `local_first`
- `app_owns_state`
- `semantic_bus_local_only`
- `qirc_digest_only_bridge`
- `bug6_children_first`
- `q7_stability`
- `app_owns_apply`
- `seed_packs_declarative_only`
- `gpl_2_0_only`
- `no_runtime_proof`

### Proof Boundaries

- `no_runtime_proof_without_host_receipts`
- `no_model_inference_proof_without_actual_model_receipts`
- `no_app_apply_authority_for_odin`
- `no_external_send_by_odin`
- `no_network_qirc_by_default`
- `no_production_readiness_claim`
- `no_executable_seed_pack_code`
- `no_religious/domain_truth_leakage_from_pattern_mines`
- `no_qirc_network_expansion`
- `no_unbounded_seed_fanout`
- `no_bypass_of_odin_final_gate`

### Codex Stop Conditions

- stop if a target path would bypass the app-owned apply boundary
- stop if a model, agent, seed pack, flow pack, runtime pack or Windows component attempts to become authority
- stop if the implementation requires external network behavior not explicitly authorized by the current PR
- stop if validation cannot distinguish implemented code from shadow/prep contracts
- stop if public docs would imply host proof, model proof, security certification, or completed product behavior without receipts


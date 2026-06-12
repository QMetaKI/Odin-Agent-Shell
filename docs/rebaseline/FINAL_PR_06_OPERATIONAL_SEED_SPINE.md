# FINAL-PR-06: Operational Seed Spine + Role Profiles + Seed-to-Work Capsule Compiler

**Claim boundary:** `operational_seed_spine_routes_work_not_authority`
**candidate_only:** true
**app_owned_apply:** true

---

## What PR06 Implemented

PR06 added `odin/operational_seed_spine/` — a deterministic routing module that maps work contexts to intent seeds, role profiles, and bounded work capsules.

### Module files created

| File | Purpose |
|---|---|
| `__init__.py` | Public API — exports CLAIM_BOUNDARY, all types |
| `intent_seeds.py` | 12 IntentSeed dataclasses with routing metadata |
| `role_profiles.py` | 10 RoleProfile dataclasses with behavioral contracts |
| `seed_packs.py` | 6 SeedPack groupings (validated on construction) |
| `selector.py` | Deterministic 4-priority seed route selector |
| `work_capsule.py` | SeedWorkCapsule compiler (SHA256 deterministic IDs) |
| `qirc_hints.py` | Hint-only QIRC record builder (no bus mutation) |
| `token_budget.py` | Per-seed token budget hints (5 keys) |
| `proof.py` | Proof packet builder + persist function |

### Supporting artifacts created

- `registries/final_pr_06_operational_seed_spine_registry.json`
- `schemas/final_pr_06_operational_seed_spine_proof_packet.schema.json`
- `examples/final_pr_06/` (4 example files)
- `tools/rebaseline/check_final_pr_06_operational_seed_spine.py`
- `tests/test_final_pr_06_operational_seed_spine.py` (29 tests)
- `reports/final_pr_06_operational_seed_spine_report.json`
- `reports/final_pr_06_operational_seed_spine_proof_packet.json`
- `SYSTEM_MAP.json` — PR06 entry added
- `FILE_MANIFEST.json` — PR06 files added

### CLI commands added

| Command | Purpose |
|---|---|
| `validate-operational-seed-spine` | Validator gate |
| `explain-seed-route --demo` | Demo route explanation (deterministic JSON) |
| `prove-operational-seed-spine` | Proof packet printer/writer |

### Local Hub endpoint added

`GET /demo/seed-route.json` — returns deterministic seed route + work capsule JSON.

---

## What PR06 Did NOT Implement

- `odin/field_selection_spine/` — reserved for FINAL-PR-07
- `odin/projection_candidate_spine/` — reserved for FINAL-PR-08
- Release/Closure — reserved for FINAL-PR-09
- Autonomous reasoning, model inference, provider execution
- App apply, app state mutation, external send, public network

---

## How PR06 Uses PR44 Prep Artifacts

- `registries/prep_final_pr_06_08_plan.v1.json` — used as scope authority for allowed/forbidden files list
- `docs/codex/handoffs/PREP_FINAL_PR_06_08_REPO_REALITY_INTAKE.md` — used for repo shape confirmation
- `tools/rebaseline/check_prep_final_pr_06_08.py` — updated to skip PR06 dirs now that they're implemented

---

## How PR06 Uses Y Pattern Spine Structurally

PR06 mirrors the Y Pattern Spine structural pattern:
- Dataclasses with `to_dict()` methods
- Deterministic IDs (SHA256 instead of string constants)
- 4-priority selection (mirrors Y Pattern's `confidence` + `center_first_posture` approach)
- Proof packet with `persist_proof_packet(ROOT)` to `reports/`
- CLI pattern: `prove-*` command writing to `reports/` and printing result

PR06 does NOT import from `odin/y_pattern_spine/`. The patterns are mirrored, not shared.

---

## How PR06 Coexists with Legacy odin/seeds/

- `odin/seeds/` contains a legacy `SeedPack` + `SeedSlot` compiler for an older architecture.
- PR06's `odin/operational_seed_spine/` is a completely separate module.
- No imports cross between them.
- Legacy `odin/seeds/` is not modified or deprecated in PR06.

---

## Why PR07 Still Remains Separate

PR07 (Field Selection Spine) involves a field-level routing layer on top of seed routing. It requires its own selectors, field pack definitions, and QIRC-channel-aware field emission. PR06 deliberately stops at the seed/role/capsule level to keep scope bounded.

## Why PR08 Still Remains Separate

PR08 (Projection Candidate Spine) involves materialization of projections from field selections. It requires a separate proof chain and materialization layer. PR06 does not implement any projection logic.

## Why Release Remains FINAL-PR-09

The release closure PR (FINAL-PR-09) requires a full audit of all PRs, final manifest reconciliation, and public release gating. No implementation PR should merge closure work.

---

## What Is Not Proven

- autonomous_reasoning
- model_inference
- provider_execution
- app_apply
- app_state_mutation
- external_send
- production_readiness
- security_certification
- live_model_inference
- external_send_authority

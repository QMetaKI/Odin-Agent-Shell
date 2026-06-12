# FINAL-PR-06 — Operational Seed Spine + Role Profiles + Seed-to-Work Capsule Compiler

**Claim boundary:** `operational_seed_spine_routes_work_not_authority`
**candidate_only:** true
**app_owned_apply:** true
**generated_at_utc:** 2026-01-01T00:00:00Z
**depends_on:** Y-Pattern-Spine (merged), FINAL-PR-05 (merged)

---

## Purpose

This prompt instructs a new Claude Code session to implement the Operational Seed Spine:
a deterministic layer that routes work via intent seeds and role profiles, producing
bounded work capsules. Seeds are operational routing signals, not autonomous agents.
Role profiles are neutral behavioral specs, not runtime personas.

---

## 0. Repo-Real Intake Steps (MANDATORY — do before any edit)

1. `git status` — confirm clean working tree on the designated branch.
2. `git log --oneline -10` — confirm base is the Y Pattern Spine merge commit.
3. Inspect: `odin/y_pattern_spine/`, `odin/execution_gate/`, `odin/proof_chain/`, `odin/final_pr_ladder/`.
4. Inspect: `odin/seeds/`, `odin/patterns/`, `odin/packets/`, `odin/universal_work/`.
5. Read: `registries/y_pattern_spine.v1.json`, `registries/y_materialization_ladder.v1.json`.
6. Read: `registries/operational_seed_function_registry.json`, `registries/seed_registry.json`.
7. Read: `docs/codex/handoffs/PREP_FINAL_PR_06_08_REPO_REALITY_INTAKE.md`.
8. Read: `registries/prep_final_pr_06_08_plan.v1.json` — confirm PR06 entry.
9. Run: `python -m odin.cli validate-y-pattern-spine` — must pass before starting.
10. Run: `python -m pytest -q tests/test_y_pattern_spine.py -p no:cacheprovider` — must pass.

Do NOT proceed if validate-y-pattern-spine fails.

---

## 1. Scope

Implement a deterministic Operational Seed Spine module with:

- Intent seeds with trigger shapes, input requirements, output shapes.
- Role profiles as neutral behavioral contracts (not runtime personas).
- Seed packs grouping seeds by domain.
- Selector: routes a work context to a seed + role profile.
- Work capsule compiler: packages seed + role profile + QIRC hints + token budget into a bounded work capsule.
- Token budget: per-seed budget constraints.
- QIRC hints: seed-derived event hints for the QIRC bus.
- Proof module: records proof boundaries, not-proven list.

---

## 2. Non-Scope

- Do NOT implement autonomous reasoning or model inference.
- Do NOT execute providers or call external APIs.
- Do NOT mutate app state, apply patches, or send external messages.
- Do NOT claim seeds are intelligent agents.
- Do NOT import Q Metamodell / cutk1 as runtime truth.
- Do NOT add new Q-style runtime names (q_shabang, qmath, q_state, qgit, qcode, qli, qstar, q_*).
- Do NOT connect to public networks.
- Do NOT implement Field Selection (PR07) or Projection (PR08) in this PR.
- Do NOT modify Local Hub server.py beyond adding demo endpoint wiring.

---

## 3. Allowed Files

**Create (new):**
- `odin/operational_seed_spine/__init__.py`
- `odin/operational_seed_spine/intent_seeds.py`
- `odin/operational_seed_spine/role_profiles.py`
- `odin/operational_seed_spine/seed_packs.py`
- `odin/operational_seed_spine/selector.py`
- `odin/operational_seed_spine/work_capsule.py`
- `odin/operational_seed_spine/qirc_hints.py`
- `odin/operational_seed_spine/token_budget.py`
- `odin/operational_seed_spine/proof.py`
- `schemas/final_pr_06_operational_seed_spine_proof_packet.schema.json`
- `registries/final_pr_06_operational_seed_spine_registry.json`
- `examples/final_pr_06/intent_seed.example.json`
- `examples/final_pr_06/role_profile.example.json`
- `examples/final_pr_06/seed_work_capsule.example.json`
- `examples/final_pr_06/seed_proof_packet.example.json`
- `docs/rebaseline/FINAL_PR_06_OPERATIONAL_SEED_SPINE.md`
- `docs/codex/audits/FINAL_PR_06_OPERATIONAL_SEED_SPINE_AUDIT.md`
- `docs/codex/audits/FINAL_PR_06_SENIOR_REVIEW.md`
- `docs/codex/reports/FINAL_PR_06_OPERATIONAL_SEED_SPINE_RETURN_REPORT.md`
- `docs/codex/handoffs/FINAL_PR_06_REPO_COGNITION_SUMMARY.md`
- `docs/codex/handoffs/FINAL_PR_06_ODIN_AGENT_OPERATOR_WORK_PACKET.md`
- `reports/final_pr_06_operational_seed_spine_report.json`
- `reports/final_pr_06_operational_seed_spine_proof_packet.json`
- `tests/test_final_pr_06_operational_seed_spine.py`
- `tools/rebaseline/check_final_pr_06_operational_seed_spine.py`

**Update (existing):**
- `odin/cli.py` — add `validate-operational-seed-spine`, `explain-seed-route`, `prove-operational-seed-spine`
- `odin/local_hub/server.py` — add `GET /demo/seed-route.json` endpoint
- `odin/local_hub/ui.py` — add Dev Mode seed spine section
- `SYSTEM_MAP.json` — add `final_pr_06_operational_seed_spine` entry
- `FILE_MANIFEST.json` — add new files

---

## 4. Forbidden Changes

- Do NOT modify: `odin/y_pattern_spine/`, `odin/execution_gate/`, `odin/proof_chain/`, `odin/final_pr_ladder/`
- Do NOT modify: existing schemas, registries, or tests unless adding precise new entries.
- Do NOT delete any existing file.
- Do NOT add files outside the allowed list.
- Do NOT introduce new `q_*` named modules, keys, or CLI commands.

---

## 5. Required Concepts

### IntentSeed (dataclass)
Fields:
- `seed_id: str` — unique identifier (e.g., `"repo_cognition"`)
- `family: str` — seed family grouping
- `trigger_shapes: list[str]` — input patterns that activate this seed
- `input_requirements: list[str]` — required context fields
- `output_shape: str` — describes output structure
- `preferred_surfaces: list[str]` — Odin surfaces this seed routes to
- `allowed_use: list[str]`
- `forbidden_use: list[str]`
- `qirc_event_hints: list[str]`
- `validator_expectations: list[str]`
- `proof_boundary: str`
- `token_budget_key: str`
- `fallback_behavior: str`

### RoleProfile (dataclass)
Fields:
- `role_profile_id: str`
- `family: str`
- `allowed_use: list[str]`
- `forbidden_use: list[str]`
- `review_axes: list[str]`
- `output_shape: str`
- `claim_boundary: str`

### SeedPack
A named collection of intent seeds grouped by domain.

Required seed packs:
- `repo_cognition`
- `prompt_to_work`
- `code_change`
- `review_audit`
- `proof_receipt`
- `local_hub_ui`
- `provider_probe`
- `execution_gate`
- `qirc_event`
- `release_closure`
- `doc_architecture`
- `debug_error_triage`

### Required role profiles:
- `builder`, `reviewer`, `guard`, `router`, `materializer`
- `proof_binder`, `scope_compressor`, `lineage_tracker`, `devmode_explainer`, `risk_scanner`

### SeedWorkCapsule
Output of the compiler. Must include:
- `seed_id`, `role_profile_id`, `qirc_hints`, `token_budget`, `proof_boundary`, `candidate_only: true`, `claim_boundary`

---

## 6. Required Local Hub Surfaces

### Endpoint
```
GET /demo/seed-route.json
```
Returns a demo `SeedWorkCapsule` JSON with `candidate_only: true` and `claim_boundary`.

### Dev Mode UI section
Label: `"Operational Seed Spine: available"`
Dev Mode copy: `"Operational Seed Spine explains why a seed route and work capsule were selected."`
Normal user copy: `"Odin prepares work with compact route hints."`

---

## 7. Required CLI Commands

```
python -m odin.cli validate-operational-seed-spine
python -m odin.cli explain-seed-route --demo
python -m odin.cli prove-operational-seed-spine
```

All three must be wired into `odin/cli.py`.
`validate-operational-seed-spine` must be called from `validate_all()`.

---

## 8. Required Validator

File: `tools/rebaseline/check_final_pr_06_operational_seed_spine.py`

Requirements:
- stdlib only
- accepts `--repo-root`, `--out`, optional `--generated-at-utc`
- validates all required module files exist
- validates registry JSON parses and has required seed pack IDs
- validates role profile IDs are present
- validates schema file exists
- validates example files exist
- validates no forbidden Q-style names in new files
- validates `candidate_only: true` in work capsule examples
- validates proof packet has `not_proven` list
- writes `reports/final_pr_06_operational_seed_spine_report.json`

---

## 9. Required Tests

File: `tests/test_final_pr_06_operational_seed_spine.py`

Minimum 12 tests covering:
1. Module `odin/operational_seed_spine/__init__.py` importable
2. All required seed packs defined
3. All required role profiles defined
4. Selector returns a SeedWorkCapsule for a test input
5. Work capsule has `candidate_only: True`
6. Work capsule has `claim_boundary`
7. Token budget present on capsule
8. QIRC hints list present on capsule
9. Proof boundary present
10. Proof module not_proven list includes required entries
11. Validator returns ok (no errors)
12. CLI `validate-operational-seed-spine` returns 0

---

## 10. Required Reports

- `reports/final_pr_06_operational_seed_spine_report.json`
- `reports/final_pr_06_operational_seed_spine_proof_packet.json`

Both must include `candidate_only: true`, `claim_boundary`, `not_proven` list.

---

## 11. Proof Packet Expectations

The proof packet must include:
```json
{
  "proven": ["seed_packs_defined", "role_profiles_defined", "selector_deterministic", "work_capsule_compiled"],
  "not_proven": ["autonomous_reasoning", "model_inference", "provider_execution", "app_apply", "app_state_mutation", "external_send", "production_readiness", "security_certification"],
  "claim_boundary": "operational_seed_spine_routes_work_not_authority",
  "candidate_only": true
}
```

---

## 12. Not-Proven List

- autonomous_reasoning_proof
- model_inference
- provider_execution
- app_apply
- app_state_mutation
- external_send_authority
- public_network_access
- production_readiness
- security_certification
- generated_code_correctness

---

## 13. Senior Reviewer Checklist

- [ ] Seeds have all required fields (trigger_shapes, input_requirements, output_shape, preferred_surfaces, allowed_use, forbidden_use, qirc_event_hints, validator_expectations, proof_boundary, token_budget_key, fallback_behavior)
- [ ] Role profiles do NOT have names like "Thor", "Odin", "Loki" — must be neutral operational names
- [ ] Work capsule always has `candidate_only: true`
- [ ] Selector is purely deterministic (no model calls, no randomness)
- [ ] Token budget is enforced per seed, not global
- [ ] QIRC hints are suggestions only, not authority
- [ ] No new q_* runtime names introduced
- [ ] Local Hub demo endpoint returns valid JSON with claim_boundary
- [ ] Proof packet not_proven list includes production_readiness, live_model_inference, app_state_mutation, external_send_authority
- [ ] validate_all() calls validate_operational_seed_spine()

---

## 14. Code Reviewer Checklist

- [ ] No runtime module execution (no subprocess calls to models)
- [ ] No provider API calls
- [ ] No app state mutation
- [ ] No public network access
- [ ] No hidden authority
- [ ] No forbidden naming drift (q_shabang, qmath, etc.)
- [ ] Validator is stdlib-only
- [ ] All new imports use existing odin.* modules only
- [ ] Tests are deterministic (no random, no network, no model calls)
- [ ] FILE_MANIFEST and SYSTEM_MAP updated with precise new entries

---

## 15. Acceptance Gates

1. `python -m odin.cli validate-operational-seed-spine` exits 0
2. `python -m odin.cli explain-seed-route --demo` prints valid JSON
3. `python -m odin.cli prove-operational-seed-spine` exits 0
4. `python -m odin.cli validate-all` exits 0
5. `python -m pytest -q tests/test_final_pr_06_operational_seed_spine.py -p no:cacheprovider` passes all tests
6. `python -m pytest -q -p no:cacheprovider` full suite passes
7. `reports/final_pr_06_operational_seed_spine_proof_packet.json` exists with valid structure
8. `GET /demo/seed-route.json` returns valid JSON when hub server is running

---

## 16. Claim Boundary

`operational_seed_spine_routes_work_not_authority`

This PR does NOT claim:
- autonomous reasoning
- model inference or provider execution
- app apply, app state mutation, or external send
- public network access
- production readiness
- security certification
- that seeds are intelligent agents
- that role profiles are runtime personas

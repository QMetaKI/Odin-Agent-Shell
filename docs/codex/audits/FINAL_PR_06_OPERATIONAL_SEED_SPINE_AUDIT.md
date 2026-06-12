# FINAL-PR-06 Operational Seed Spine Audit

**Claim boundary:** `operational_seed_spine_routes_work_not_authority`
**candidate_only:** true

---

## Module Audit

### odin/operational_seed_spine/intent_seeds.py

- 12 IntentSeed definitions covering all required seed IDs
- Each seed has trigger_shapes, input_requirements, output_shape, preferred_surfaces, allowed_use, forbidden_use, qirc_event_hints, validator_expectations, proof_boundary, token_budget_key, fallback_behavior
- `get_seed(seed_id)` lookup — O(1) dict-based
- No model calls. No provider calls. No external imports.

### odin/operational_seed_spine/role_profiles.py

- 10 RoleProfile definitions covering all required role profile IDs
- FORBIDDEN_PROFILE_IDS frozenset enforced at construction (`__post_init__`)
- None of thor, odin, loki, maria, michael, y, mjolnir, q, qstar used as profile IDs
- `get_role_profile(role_profile_id)` lookup — O(1) dict-based

### odin/operational_seed_spine/seed_packs.py

- 6 SeedPack definitions including the required IDs
- Missing seed references are validated at construction time (`__post_init__`)
- `validate_seed_packs()` function for external validation
- `full_spine` pack includes all 12 required seeds

### odin/operational_seed_spine/selector.py

- 4-priority selection: exact_trigger_shape → family_surface_match → preferred_default_work_type → deterministic_fallback
- `FALLBACK_SEED_ID = "prompt_to_work"` constant — not random
- `fallback_used: bool` visible in output
- No randomness. No timestamps. No model calls. Pure deterministic dict lookup.

### odin/operational_seed_spine/work_capsule.py

- `_deterministic_capsule_id(route)` uses `sha256(canonical_json(payload))[:16]`
- Canonical JSON: `sort_keys=True, separators=(",", ":")` — order-independent
- `NOT_PROVEN` list hardcoded — includes 8 required non-claims
- `candidate_only = True`, `app_owned_apply = True` hardcoded

### odin/operational_seed_spine/qirc_hints.py

- `build_qirc_hints(event_hint_names)` returns list of dicts
- Each hint: `authority: "hint_only"`, `candidate_only: True`
- No import of `odin.qirc_core.bus`. No event emission.

### odin/operational_seed_spine/token_budget.py

- 5 budget keys: tiny, small, medium, large, audit
- Each budget: deterministic dict with hint fields
- No provider/model dependency. No external tokenizer.

### odin/operational_seed_spine/proof.py

- `build_proof_packet()` returns dict with PROVEN and NOT_PROVEN lists
- `persist_proof_packet(repo_root)` writes to `reports/final_pr_06_operational_seed_spine_proof_packet.json`
- No randomness. No timestamps.

---

## Claim Boundary Audit

All files in `odin/operational_seed_spine/` include:
```
CLAIM_BOUNDARY = "operational_seed_spine_routes_work_not_authority"
```

All `to_dict()` outputs include `claim_boundary` and `candidate_only: True`.

All capsules include `app_owned_apply: True`.

---

## Scope Audit

Files created: 9 module files + 7 support files + 17+ doc files
Files modified (additive only): `odin/cli.py`, `odin/local_hub/server.py`, `odin/local_hub/ui.py`, `SYSTEM_MAP.json`, `FILE_MANIFEST.json`, `tools/rebaseline/check_prep_final_pr_06_08.py`, `tests/test_prep_final_pr_06_08.py`
Files modified (update for PR06 completion): prep validator + prep test

No modifications to: `odin/y_pattern_spine/`, `odin/execution_gate/`, `odin/proof_chain/`, `odin/final_pr_ladder/`, `odin/seeds/`, `odin/patterns/`

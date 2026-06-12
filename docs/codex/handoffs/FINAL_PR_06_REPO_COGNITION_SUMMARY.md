# FINAL-PR-06 Repo Cognition Summary

**Claim boundary:** `operational_seed_spine_routes_work_not_authority`
**candidate_only:** true
**Base commit:** `7cb6f2e` (Merge pull request #44)

---

## Files Read

- `CLAUDE.md`, `AGENTS.md`, `CODEX_START_HERE.md`, `CLAIM_BOUNDARY.md`
- `docs/codex/prompts/FINAL_PR_06_OPERATIONAL_SEED_SPINE.md`
- `registries/prep_final_pr_06_08_plan.v1.json`
- `registries/operational_seed_function_registry.json`
- `registries/operational_seed_substrate_registry.json`
- `odin/local_hub/server.py` — full read (endpoint pattern)
- `odin/local_hub/ui.py` — full read (REQUIRED_IDS, HTML pattern)
- `odin/y_pattern_spine/capsules.py` — full read (capsule pattern)
- `odin/y_pattern_spine/profiles.py` — full read (route hint pattern)
- `odin/cli.py` — relevant sections (insertion points, validate_all, subparsers)
- `tools/rebaseline/check_prep_final_pr_06_08.py` — for prep validator awareness

## Files Intentionally Avoided

- `odin/y_pattern_spine/*.py` (read-only, not modified except via reference)
- `odin/execution_gate/*.py` (read-only reference)
- `odin/proof_chain/*.py` (read-only reference)
- `odin/final_pr_ladder/*.py` (read-only reference)
- `odin/seeds/*.py` (legacy, not imported by PR06)
- `odin/patterns/*.py` (legacy, not imported by PR06)

---

## Existing Surfaces Reused

- **Local Hub server pattern:** `BaseHTTPRequestHandler`, `do_GET()` with `elif self.path == ...` dispatch. Used verbatim for `/demo/seed-route.json`.
- **CLI pattern:** `sub.add_parser("command-name")` + early-return handler before the `validate_all` fallback.
- **Validator pattern:** `importlib.util.spec_from_file_location` + `tempfile.TemporaryDirectory` for subprocess-free import.
- **Proof packet pattern:** `persist_proof_packet(ROOT)` writing to `reports/`.
- **Y Pattern Spine dataclass pattern:** `@dataclass` with `to_dict()` method, stdlib-only.

## Existing Surfaces Not Modified

- `odin/y_pattern_spine/` — no changes
- `odin/execution_gate/` — no changes
- `odin/proof_chain/` — no changes
- `odin/final_pr_ladder/` — no changes
- `odin/seeds/` — no changes
- `odin/patterns/` — no changes
- `odin/qirc_core/` — no changes

---

## Relevant CLI Commands Discovered

| Command | Status |
|---|---|
| `validate-final-pr-05-execution-gate` | Existing, passes |
| `validate-y-pattern-spine` | Existing, passes |
| `validate-prep-final-pr-06-08` | Existing, passes (updated for PR06) |
| `explain-y-route --demo` | Existing pattern, mirrored for `explain-seed-route --demo` |
| `prove-y-pattern-spine` | Existing pattern, mirrored for `prove-operational-seed-spine` |

---

## Existing Local Hub Endpoint Pattern

`server.py` uses a flat `elif self.path == "..."` dispatch inside `do_GET()`. Each endpoint imports its dependencies lazily and returns `json.dumps(...).encode("utf-8")`. New endpoint `/demo/seed-route.json` follows this pattern exactly.

## Existing QIRC Pattern

`odin/qirc_core/bus.py` holds an in-process event list. PR06 does NOT import or mutate the QIRC bus. QIRC hints in PR06 are record dicts only — no bus interaction.

## Existing Y Pattern Spine Pattern

`YWorkCapsule` + `YRouteHint` dataclasses with explicit `to_dict()`. Selection is deterministic (no randomness). Proof packet is written to `reports/`. PR06 mirrors this pattern for `SeedWorkCapsule` + `SeedRoute`.

## Existing Execution Gate / Proof Pattern

`odin/execution_gate/proof.py` writes proof to `reports/`. `odin/cli.py` calls `persist_proof_packet(ROOT)` and prints result. PR06 follows the same pattern.

## Legacy odin/seeds/ and odin/patterns/ Status

- `odin/seeds/` — legacy seed compiler for old `SeedPack` concept. Not imported by PR06.
- `odin/patterns/` — legacy pattern intake. Not imported by PR06.
- PR06 creates `odin/operational_seed_spine/` as a fully independent module.

---

## PR06 Implementation Plan (Derived from Repo Reality)

1. Create `odin/operational_seed_spine/` (9 files) — stdlib only, dataclass-based.
2. Create registry, schema, examples.
3. Update `odin/cli.py` — add 3 subparsers + 3 early-return handlers + `validate_all` call.
4. Update `odin/local_hub/server.py` — add `elif /demo/seed-route.json`.
5. Update `odin/local_hub/ui.py` — add `REQUIRED_IDS` entry + HTML section + REQUIRED_COPY entry.
6. Create `tools/rebaseline/check_final_pr_06_operational_seed_spine.py` — stdlib-only validator.
7. Create `tests/test_final_pr_06_operational_seed_spine.py` — 29 deterministic tests.
8. Update `SYSTEM_MAP.json` + `FILE_MANIFEST.json` — PR06 entries only.
9. Update `tools/rebaseline/check_prep_final_pr_06_08.py` — skip PR06 dirs now that they're implemented.
10. Create reports, docs, audits, handoffs.

---

## Known Non-Claims

- No autonomous reasoning.
- No model inference.
- No provider execution.
- No app apply.
- No app state mutation.
- No external send.
- No public network.
- Seeds are routing signals, not agents.
- Role profiles are contracts, not personas.
- QIRC hints do not authorize anything.
- Production readiness is not claimed.
- Security certification is not claimed.

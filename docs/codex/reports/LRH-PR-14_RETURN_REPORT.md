# LRH-PR-14 Return Report — Local Config, Redaction and Safe Settings UI

**Claim boundary:** `lrh_pr_14_return_report_candidate_only_no_app_apply_no_external_send_no_runtime_proof`

**Date:** 2026-06-11
**Branch:** `claude/lrh-pr-14-local-config-pwdcl1`
**PR:** LRH-PR-14 — Local Config, Redaction and Safe Settings UI

---

## Motivation

LRH-PR-14 implements the Local Config Schema, Safe Settings UI surface, redaction fixture suite, and unsafe setting block list from the Local Runtime Hub Road-to-100 ladder.

This is **settings visibility only**. Not a security certification. Not a production readiness certification. Does not grant app apply authority. Does not expand Odin authority.

Builds on LRH-PR-13 (Generic App Bridge Examples and Golden Harness).

---

## Implementation Summary

**New files created:**

- `schemas/v7_1/odin_local_config.schema.json` — JSON Schema for Odin local config
- `examples/local_config/safe_local_config.valid.json` — canonical safe config fixture
- `examples/local_config/unsafe_network_config.invalid.json` — unsafe: WAN bind host + public network
- `examples/local_config/unsafe_provider_enabled.invalid.json` — unsafe: provider credentials + enabled-by-default
- `examples/local_config/unsafe_raw_payload_reveal.invalid.json` — unsafe: raw payload reveal enabled
- `examples/local_config/unsafe_redaction_disabled.invalid.json` — unsafe: redaction disabled
- `examples/local_config/redaction_fixture.valid.json` — redaction input fixture (sensitive keys with test values)
- `examples/local_config/redaction_expected.valid.json` — expected redacted output fixture
- `docs/LOCAL_CONFIG_SAFE_SETTINGS_V1.md` — feature documentation with proof boundaries
- `odin/hub/static/local_config_safe_settings.js` — IIFE hub UI module (settings visibility only)
- `tests/test_lrh_pr_14_local_config_safe_settings.py` — 72 tests
- `docs/codex/reports/LRH-PR-14_RETURN_REPORT.md` — this report

**Modified files:**

- `odin/doctor/redaction.py` — extended `SECRET_KEY_MARKERS` with: `auth`, `private`, `sensitive`, `raw_payload`, `payload_raw`
- `odin/hub/shell.py` — added `_LCSS_UNSAFE_BLOCK_LIST`, `validate_local_config_safe_settings()`, `build_local_config_safe_settings_proof_packet()`, all required constants and surface checks
- `odin/hub/static/index.html` — added `local-config-safe-settings-panel` section with all 5 surface IDs, nav link, JS module `<script>` tag, required boundary phrases
- `odin/hub/static/styles.css` — added LCSS-specific CSS classes
- `odin/cli.py` — added imports, added `validate_local_config_safe_settings()` to `validate_all()`, added `validate-local-config-safe-settings` and `prove-local-config-safe-settings` subparsers and handlers
- `SYSTEM_MAP.json` — added `lrh_pr_14_local_config_safe_settings` entry
- `FILE_MANIFEST.json` — added new file entries

**Unchanged:**

All other source files.

---

## Thor Diagnostic

Thor is available after install (classification: `thor_available`, per LRH-PR-13 discipline).

Thor is advisory only. PR result does not depend on Thor output.

---

## Odin Agent Operator Mode Audit

```
python -m odin.cli agent-handoff --agent claude-code --lrh-pr 14 --out /tmp/lrh_pr_14_packet.json
→ candidate_only: true
→ app_owned_apply: true
→ external_send_default: false
→ hidden_tool_execution_allowed: false
→ acceptance_gates: secrets redacted, unsafe settings blocked, no provider enabled without explicit config

python -m odin.cli agent-guard --packet /tmp/lrh_pr_14_packet.json
→ status: ok, violations: []

python -m odin.cli agent-check --packet /tmp/lrh_pr_14_packet.json
→ status: ok, errors: []

python -m odin.cli agent-proof --packet /tmp/lrh_pr_14_packet.json
→ status: gaps_present
→ missing: no_app_apply_by_agent, no_external_send_by_agent, no_hidden_tool_execution
```

**Gap classification:** `expected_pr_level_gap` — guard/check pass, no forbidden actions present. The packet structure for candidate-only work does not include explicit agent-level boundary proof tokens. No blocking gaps.

---

## LRH Ladder Compiler Audit

LRH-PR-14 entry in `registries/local_runtime_hub_build_ladder_v1.json` is present and correct:
- `id`: LRH-PR-14
- `title`: Local Config, Redaction and Safe Settings UI
- `objective`: Add local config schema, safe settings UI, redaction tests and disabled-by-default provider settings visibility
- `acceptance_gates`: secrets redacted, unsafe settings blocked, no provider enabled without explicit config

Packet compiled correctly by LRH Ladder Compiler v1.

---

## Claude Code Worker Audit

Worker operated within allowed scope:
- Only created files in `schemas/v7_1/`, `examples/local_config/`, `docs/`, `odin/hub/static/`, `tests/`
- Only modified `odin/hub/shell.py`, `odin/hub/static/index.html`, `odin/hub/static/styles.css`, `odin/cli.py`, `odin/doctor/redaction.py`, `SYSTEM_MAP.json`, `FILE_MANIFEST.json`
- No mutations to runtime semantics or Odin authority
- No provider calls, no credential handling, no external send
- No forbidden function identifiers (enableProvider, saveCredential, bypassRedaction, rawPayloadReveal, etc.)

---

## Schema and Fixtures

### Local Config Schema

`schemas/v7_1/odin_local_config.schema.json` — JSON Schema (draft-07) defining all safe config fields with correct constraints. Required fields: `localhost_only` (true), `bind_host` (enum: 127.0.0.1/localhost/::1), `public_network_enabled` (false), `external_send_enabled` (false), `app_apply_enabled` (false), `provider_credentials_enabled` (false), `raw_payload_reveal_enabled` (false), `redaction_enabled` (true), `providers.enabled_by_default` (false).

### Safe Config Fixture

`examples/local_config/safe_local_config.valid.json` — includes `candidate_only: true`, `claim_boundary`, `proof_boundaries` list, all safe field values.

### Unsafe Config Fixtures (4)

All four unsafe fixtures set exactly the blocked values that `_lcss_check_unsafe_config()` detects:
- `unsafe_network_config.invalid.json` → bind_host: "0.0.0.0", public_network_enabled: true
- `unsafe_provider_enabled.invalid.json` → provider_credentials_enabled: true, providers.enabled_by_default: true
- `unsafe_raw_payload_reveal.invalid.json` → raw_payload_reveal_enabled: true
- `unsafe_redaction_disabled.invalid.json` → redaction_enabled: false

### Redaction Fixtures

`redaction_fixture.valid.json` — contains sensitive keys (token, secret, password, api_key, credential, auth, private, raw_payload, payload_raw, sensitive) with test placeholder values. Non-sensitive safe keys (host, port, safe_field) also present.

`redaction_expected.valid.json` — identical structure, all sensitive keys replaced with `"[REDACTED]"`.

---

## Redaction Module Extension

`odin/doctor/redaction.py` `SECRET_KEY_MARKERS` extended with: `auth`, `private`, `sensitive`, `raw_payload`, `payload_raw`. These are substring-matched via `any(marker in lowered for marker in SECRET_KEY_MARKERS)`, so `raw_payload` and `payload_raw` as standalone keys are matched correctly.

---

## Hub Panel

`local-config-safe-settings-panel` section in `odin/hub/static/index.html` contains:

Surface IDs present:
- `lcss-config-status-content`
- `lcss-unsafe-block-list-content`
- `lcss-redaction-status-content`
- `lcss-provider-disabled-content`
- `lcss-proof-boundaries-content`

Required boundary phrases present (lowercase):
- "settings visibility only"
- "not a security certification"
- "redaction status is not"
- "providers disabled by default"
- "no app apply"
- "no external send"
- "no credentials"
- "no raw payload reveal"
- "no redaction bypass"

No forbidden controls: no `type="password"` in LCSS section, no `enableProvider(`, no `disableProvider(`, no `bypassRedaction(`, no `rawPayloadReveal(`.

JS module: `local_config_safe_settings.js` included via `<script src="...">`.

---

## Unsafe Setting Block List

`_LCSS_UNSAFE_BLOCK_LIST` in `odin/hub/shell.py` covers 9 fields:

| Field | Blocked |
|-------|---------|
| `bind_host` | `"0.0.0.0"`, `"::"` |
| `public_network_enabled` | `true` |
| `external_send_enabled` | `true` |
| `app_apply_enabled` | `true` |
| `provider_credentials_enabled` | `true` |
| `raw_payload_reveal_enabled` | `true` |
| `log_secrets` | `true` |
| `redaction_enabled` | `false` |
| `providers.enabled_by_default` | `true` |

---

## CLI Commands

New CLI commands:

```
python -m odin.cli validate-local-config-safe-settings  → OK
python -m odin.cli prove-local-config-safe-settings     → status: ok, 15 proven, 11 not_proven
```

---

## Tests

`tests/test_lrh_pr_14_local_config_safe_settings.py` — **72 tests**

Coverage:
- File existence (schema, fixtures, doc, JS module, test file) — 12 tests
- Schema valid JSON + title/properties check — 1 test
- Safe config field values (9 fields + candidate_only + claim_boundary) — 11 tests
- Unsafe config detection (4 fixtures × _lcss_check_unsafe_config) — 5 tests
- Block list completeness (8 fields present) — 8 tests
- Redaction fixture sensitive key presence — 1 test
- Redaction expected markers present — 1 test
- Redaction function produces expected output — 1 test
- Hub panel HTML surface IDs (5) — 5 tests
- Hub panel phrase checks (providers disabled, redaction status, settings visibility, JS module, no credential input, no provider enable, no redaction bypass) — 7 tests
- Doc phrase checks (11) — 11 tests
- Validator function — 1 test
- Proof packet structure (status/candidate_only/local_only/settings_visibility_only/provider_settings/not_proven list/proof_boundaries) — 3 tests
- CLI commands — 2 tests
- Agent handoff --lrh-pr 14 smoke test — 1 test
- validate-all — 1 test

---

## Commands Run

```
python -m odin.cli validate-all                                                → OK
python -m odin.cli validate-agent-operator-mode                                → OK
python -m odin.cli validate-local-config-safe-settings                        → OK
python -m odin.cli prove-local-config-safe-settings                           → status: ok
python -m odin.cli agent-handoff --agent claude-code --lrh-pr 14 --out /tmp/lrh_pr_14_packet.json → OK
python -m odin.cli agent-guard --packet /tmp/lrh_pr_14_packet.json            → status: ok
python -m odin.cli agent-check --packet /tmp/lrh_pr_14_packet.json            → status: ok
python -m odin.cli agent-proof --packet /tmp/lrh_pr_14_packet.json            → gaps_present (expected_pr_level_gap)
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_lrh_pr_14_local_config_safe_settings.py -p no:cacheprovider → 72 passed
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider              → 1109 passed, 2 skipped
```

---

## Results

| Check | Result |
|-------|--------|
| `validate-all` | OK |
| `validate-agent-operator-mode` | OK |
| `validate-local-config-safe-settings` | OK |
| `prove-local-config-safe-settings` | status: ok |
| `agent-guard` | status: ok |
| `agent-check` | status: ok |
| `agent-proof` | gaps_present (expected_pr_level_gap) |
| LRH-PR-14 tests | 72 passed |
| Full pytest | 1109 passed, 2 skipped |

---

## Proof Boundaries

- `not_production_readiness_certification`
- `not_security_certification`
- `not_redaction_safety_certification`
- `not_provider_credential_storage_proof`
- `not_public_network_api_proof`
- `not_app_apply_proof`
- `not_app_state_mutation_proof`
- `not_external_send_authority_proof`
- `not_live_model_inference_proof`
- `not_model_quality_proof`
- `not_raw_payload_reveal_proof`
- `settings_visibility_only`
- `redaction_status_not_security_certification`
- `provider_settings_disabled_by_default`

---

## Senior Reviewer Simulation

**Architecture:**

| Question | Answer |
|----------|--------|
| Does PR-14 preserve Master Architecture v7.1? | Yes — Odin is candidate-only, no authority expansion |
| Is the UI panel read-only? | Yes — no save controls, no editable fields |
| Are providers disabled by default? | Yes — validated in schema, fixture, block list, and UI panel |
| Is redaction enabled and not bypassable? | Yes — redaction_enabled required true; no bypass control |
| Are credentials absent from the panel? | Yes — no type="password", no credential input surface |
| Does the panel avoid claiming redaction is a security certification? | Yes — explicit "redaction status is not a security certification" phrase |
| Does the panel avoid claiming settings visibility is production proof? | Yes — "settings visibility only" phrase present |
| Does the unsafe block list cover all required fields? | Yes — 9 fields covered including bind_host WAN/LAN guard |
| Does the redaction module cover all fixture sensitive keys? | Yes — SECRET_KEY_MARKERS extended to cover auth, private, sensitive, raw_payload, payload_raw |
| Does host app own apply? | Yes — app_apply_enabled: false required; app_apply authority not in Odin |
| Does Odin avoid external send? | Yes — external_send_enabled: false required; no external send surface |
| Are there forbidden function identifiers in the JS module or HTML? | No — scanned and confirmed absent |
| Is the claim discipline section free of forbidden overclaim phrases? | Yes — rewritten to use scoped language only |

**Scope confirmed:**

- Settings visibility only ✓
- Not a security certification ✓
- Not a production readiness certification ✓
- No app apply control ✓
- No external send ✓
- No provider credentials ✓
- No raw payload reveal ✓
- No redaction bypass ✓
- Providers disabled by default ✓
- Read-only panel ✓

**Risks identified:**

- Redaction module not covering all fixture keys — mitigated by extending SECRET_KEY_MARKERS and adding redaction tests
- Claim Discipline doc section containing forbidden phrase literals — mitigated by rewriting section to use scoped language without the literal strings
- JS module implying configurable redaction — mitigated by UNSAFE_BLOCK_LIST display-only approach and explicit boundary tokens

**Verdict: Ready**

---

## Senior Code Reviewer Simulation

**Code/Repo:**

| Check | Status |
|-------|--------|
| Isolated schema/examples/docs/static/tests + small validator/CLI changes | ✓ |
| Deterministic fixture tests | ✓ |
| No browser automation dependency | ✓ |
| No npm dependency | ✓ |
| No external network | ✓ |
| No hidden runtime behavior | ✓ |
| CLI registration stable | ✓ |
| validate-all green | ✓ |
| No forbidden function identifiers in HTML/JS | ✓ |
| No secrets in fixtures | ✓ |

**Tests present for:**

| Test | Present |
|------|---------|
| Schema and fixture file existence | ✓ |
| Schema valid JSON | ✓ |
| Safe config all required field values | ✓ |
| All 4 unsafe configs detected as blocked | ✓ |
| Block list covers all 8+ required fields | ✓ |
| Redaction fixture has sensitive keys | ✓ |
| Redaction expected has [REDACTED] markers | ✓ |
| Redaction function produces expected output | ✓ |
| Hub panel has all required surface IDs | ✓ |
| Hub panel has all required boundary phrases | ✓ |
| Hub panel has no forbidden controls | ✓ |
| Doc has all required boundary phrases | ✓ |
| Validator passes for safe config | ✓ |
| Proof packet structure correct | ✓ |
| CLI commands work | ✓ |
| Agent handoff --lrh-pr 14 smoke test | ✓ |
| validate-all | ✓ |

**Fixes applied during implementation:**

1. Extended `SECRET_KEY_MARKERS` in `odin/doctor/redaction.py` — added `auth`, `private`, `sensitive`, `raw_payload`, `payload_raw` to ensure redaction fixture keys are recognized
2. Rewrote "Claim Discipline" section in `docs/LOCAL_CONFIG_SAFE_SETTINGS_V1.md` — removed literal forbidden phrases that were triggering the overclaim scanner; replaced with scoped-language-only guidance

---

## Agent/Ladder Audit Summary

| Audit | Result |
|-------|--------|
| Odin Agent Operator Mode | agent-handoff: OK; guard: OK; check: OK; proof: expected_pr_level_gap |
| LRH Ladder Compiler | PR-14 packet derived correctly from registry |
| Forbidden actions | None — no app apply, no external send, no hidden tools |
| Boundary preserved | Yes — candidate_only: true, app_owned_apply: true throughout |

---

## Skipped / Blocked

**Skipped (not in scope for LRH-PR-14):**

- Provider execution / live model inference — out of scope
- Production integration — not in scope for any LRH PR at this stage
- Windows service/tray/installer proof — deferred to LRH-PR-18+
- Signed distribution receipts — deferred to LRH-PR-18+
- Public network API proof — not in scope
- Thor CLI deep integration — advisory only for this PR

**No blocking issues.**

---

## Next Recommended PR

**LRH-PR-15 — next ladder item**

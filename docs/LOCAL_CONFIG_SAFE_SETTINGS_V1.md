# Local Config, Redaction and Safe Settings UI — V1

**Claim boundary:** `local_config_safe_settings_candidate_only_local_only_settings_visibility_only_no_app_apply_no_external_send_no_credentials_no_wan_lan_default`

**LRH-PR-14**

---

## What This Is

This document describes the Odin Local Runtime Hub local configuration schema, safe settings UI surface, redaction fixture suite, and unsafe setting block list.

This is **settings visibility only**. It is not a security certification. It is not a production readiness certification. It is not a provider credential storage proof. It is not a redaction safety certification.

---

## What This Is Not

- Not a production readiness certification
- Not a security certification
- Not a redaction safety certification
- Not a provider credential storage proof
- Not a public network API proof
- Not an app apply authority proof
- Not an external send authority proof
- Not a live model inference proof
- Not a model quality proof
- Not a raw payload reveal control
- Not a redaction bypass control
- Not a provider enable control
- Not a credential input surface

---

## Local Config Schema

Schema: `schemas/v7_1/odin_local_config.schema.json`

A safe local config must have all of the following:

| Field | Required Value | Reason |
|-------|----------------|--------|
| `localhost_only` | `true` | Odin hub is localhost-only by default |
| `bind_host` | `"127.0.0.1"` or `"localhost"` | Unsafe WAN/LAN default is blocked |
| `public_network_enabled` | `false` | Public network is not Odin authority |
| `external_send_enabled` | `false` | External send is not Odin authority |
| `app_apply_enabled` | `false` | App apply is host-owned |
| `provider_credentials_enabled` | `false` | Provider credentials must not be enabled by default |
| `raw_payload_reveal_enabled` | `false` | Raw payload reveal is not allowed |
| `redaction_enabled` | `true` | Redaction must remain enabled |
| `providers.enabled_by_default` | `false` | Providers are disabled by default |

---

## Unsafe Setting Block List

The following settings are blocked by the local config validator:

| Field | Blocked Value | Reason |
|-------|--------------|--------|
| `bind_host` | `"0.0.0.0"` or `"::"` | blocked because unsafe network default |
| `public_network_enabled` | `true` | blocked because external send is not Odin authority |
| `external_send_enabled` | `true` | blocked because external send is not Odin authority |
| `app_apply_enabled` | `true` | blocked because app apply is host-owned |
| `provider_credentials_enabled` | `true` | blocked because provider credentials must not be enabled by default |
| `raw_payload_reveal_enabled` | `true` | blocked because raw payload reveal is not allowed |
| `log_secrets` | `true` | blocked because secrets must not appear in logs |
| `redaction_enabled` | `false` | blocked because redaction must remain enabled |
| `providers.enabled_by_default` | `true` | blocked because provider credentials must not be enabled by default |

---

## Redaction

Redaction markers replace sensitive field values with `[REDACTED]`.

Sensitive keys recognized by the redaction module include:
`token`, `secret`, `password`, `api_key`, `credential`, `auth`, `private`, `raw_payload`, `payload_raw`, `sensitive`, `authorization`, `bearer`

The redaction status surface shows whether redaction is active. Redaction status is not a security certification.

No redaction bypass control exists. No raw sensitive payload is displayed.

---

## Safe Settings UI

Hub surface: `local-config-safe-settings-panel`

The panel shows:

- Local config status (read-only)
- Localhost-only enforcement
- Bind host
- Public network disabled
- External send disabled
- App apply disabled
- Provider credentials disabled
- Raw payload reveal disabled
- Redaction enabled
- Provider settings disabled by default
- Unsafe setting block list
- Redaction status (not a security certification)
- Proof boundaries
- Known non-proofs

The panel is **read-only**. No save control. No editable credential fields. No provider enable toggle. No redaction bypass control.

---

## Provider Disabled-by-Default Panel

Surface: `lcss-provider-disabled-panel`

Providers are disabled by default. Explicit config required before provider enablement. This does not prove provider execution. This does not store credentials. This is provider settings visibility only.

No provider run button. No provider enable toggle. No credential field. No API key field.

---

## Proof Boundaries

This PR proves:

- `local_config_schema_exists`
- `safe_config_fixture_exists`
- `unsafe_config_fixtures_exist`
- `redaction_fixtures_exist`
- `safe_settings_ui_exists`
- `unsafe_settings_blocked`
- `secrets_redacted`
- `no_secrets_in_logs`
- `providers_disabled_by_default`
- `no_provider_enabled_without_explicit_config`
- `no_unsafe_wan_lan_default`
- `no_security_certification_claim`
- `no_raw_payload_reveal_control`
- `no_redaction_bypass_control`
- `no_provider_credential_input`

This PR does not prove:

- `production_readiness`
- `security_certification`
- `redaction_safety_certification`
- `provider_credential_storage`
- `public_network_api`
- `app_apply_authority`
- `external_send_authority`
- `live_model_inference`
- `model_quality`
- `windows_service_tray_installer`
- `signed_distribution`

---

## Claim Discipline

Use scoped language only. Overclaim phrases are not permitted in Odin output.

Permitted: green locally, not_proven, known non-proof, not a certification, settings visibility only, redaction status only, local receipt, candidate only.

---

## Boundaries

- does not grant app apply authority
- does not send externally
- does not execute providers
- does not store provider credentials
- does not display raw sensitive payloads
- does not prove production readiness
- does not prove security certification
- not a hosted cloud UI
- not a public network API
- not_production_readiness_certification
- redaction status is not a security certification
- provider settings are disabled by default
- settings visibility only

proof boundaries: see above

not_production_readiness — this PR does not claim production readiness.

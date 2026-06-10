# Runtime Doctor, First-Run Bootstrap and Self-Healing — V1

**LRH-PR-04 — Odin Agent Shell v7.1**

This document describes the runtime doctor, first-run bootstrap, plan-only repair and diagnostics support bundle surfaces added in LRH-PR-04.

---

## Purpose

LRH-PR-04 adds deterministic local readiness diagnostics, safe first-run bootstrap and plan-only repair surfaces for Odin's portable local runtime.

These surfaces help operators understand runtime readiness without mutating state, creating production claims, or bypassing Odin's candidate-only and permission-gated boundaries.

---

## Commands

### `python -m odin.cli doctor`

Runs a deterministic read-only health check of the local runtime environment.

Checks performed:
- Python version (3.9+ required)
- Required package imports
- Runtime directory presence
- Lockfile status
- Local runtime config file validity
- Host safety (localhost-only)
- Port availability
- Optional local API health (skipped if runtime not running)

Doctor is **read-only**. Doctor does not create config. Doctor does not repair. Doctor does not delete lockfiles. Doctor does not mutate app state.

Doctor is not production readiness certification.

### `python -m odin.cli first-run-bootstrap`

Creates a safe localhost-only default config at `.odin_runtime/local_runtime_config.json` if it does not already exist.

Default config values:
- `host: 127.0.0.1`
- `port: 8877`
- `runtime_mode: portable`
- `candidate_only: true`
- `app_owned_apply: true`
- `public_bind: false`
- `external_send_default: false`
- `provider_live_default: false`

Bootstrap is **idempotent** — if config already exists it skips without overwriting.

Bootstrap writes only a safe local config file. Bootstrap does not enable public bind defaults. Bootstrap does not enable provider/live model. Bootstrap does not send externally.

Bootstrap is local-only and safe-by-default. Bootstrap is not production readiness proof.

### `python -m odin.cli repair-local-runtime --plan-only`

Inspects doctor failures and emits a structured repair plan without applying any changes.

Repair plan items include:
- The failing check name
- The failure reason
- A suggested fix
- `plan_only: true`
- `apply_gate_required: true`

Repair is **plan-only**. Repair does not apply changes. Repair does not mutate app or domain state. Repair does not edit files automatically.

The `--plan-only` flag is required. Without it the command fails closed.

No automatic repair is implemented. An explicit apply gate is required for any real repair.

### `python -m odin.cli emit-support-bundle --diagnostics-only`

Emits a diagnostics support bundle manifest with redacted doctor report.

Support bundle includes:
- Bundle ID
- Included reports list
- Redacted doctor report (secrets removed)
- Redaction metadata
- Known non-proofs list

Support bundle is **local and redacted**. No external send. No private tokens or secrets included. No app state collected.

### `python -m odin.cli validate-runtime-doctor-bootstrap`

Validates that all LRH-PR-04 module files, example fixtures and doc surfaces are present and correct.

Runs as part of `validate-all`.

---

## Doctor Checks

| Check | Description | Read-Only |
|-------|-------------|-----------|
| `python_version` | Python 3.9+ required | Yes |
| `package_imports` | Required Odin packages importable | Yes |
| `runtime_dir` | `.odin_runtime/` directory present | Yes |
| `lockfile` | Lockfile valid/stale/absent | Yes |
| `config_file` | Config valid, host safe, parseable | Yes |
| `host_safety` | Host is localhost-only | Yes |
| `port_availability` | Port not in use | Yes |
| `local_api_health` | Optional HTTP health check (skip if not running) | Yes |

Doctor status values:
- `ok` — all checks pass
- `warn` — no failures but warnings present (e.g., stale lockfile, absent config)
- `fail` — one or more checks failed

---

## First-Run Bootstrap Behavior

Bootstrap writes only `host: 127.0.0.1`. Public bind addresses (`0.0.0.0`, `::`) are blocked by default.

Bootstrap does not overwrite existing user config. Force overwrite is not implemented in this PR.

Bootstrap mutation scope is limited to the local config file at `.odin_runtime/local_runtime_config.json`.

---

## Repair Plan — Plan-Only

Repair plan is advisory only. Every item is marked:
- `plan_only: true`
- `apply_gate_required: true`
- `applied: false`
- `state_mutated: false`

The Failure Reason Catalog maps known failure reasons to human-readable suggested fixes.

---

## Support Bundle — Diagnostics Only

Support bundle redacts keys matching or containing:
- `token`, `secret`, `password`, `authorization`, `api_key`, `apikey`
- `bearer`, `client_secret`, `refresh_token`, `access_token`, `credential`

No external send is performed. Bundle is local and written to `.odin_runtime/support/` by default.

---

## Redaction Policy

All doctor output and support bundle content is processed through `odin.doctor.redaction.redact_recursive` before emission.

Redaction replaces secret key values with `[REDACTED]`.

No raw secret values appear in doctor reports, support bundles or logs.

---

## Failure Reason Catalog

| Pattern | Suggested Fix |
|---------|--------------|
| stale lockfile — process not alive | Remove `.odin_runtime/local_runtime.lock` after confirming runtime is not running |
| config absent | Run `python -m odin.cli first-run-bootstrap` |
| config validation failed | Edit config to fix listed errors, ensure `host: 127.0.0.1` |
| blocked host | Update host to `127.0.0.1` or `localhost` |
| port in use | Check conflicting process or change port |
| packages not importable | Run `python -m pip install -e .` |
| Python version too old | Upgrade Python to 3.9+ |

---

## What This Proves

LRH-PR-04 provides:
- Local runtime readiness diagnostics
- Safe first-run config generation
- Plan-only repair guidance
- Redacted local diagnostics bundle

---

## What This Does Not Prove

Doctor is **not production readiness certification**.

Bootstrap is **not a Windows service**, **not a tray application**, **not a signed installer**, and **not production readiness proof**.

Repair is **plan-only**. No automatic repair or apply mode is implemented.

Support bundle is **local and redacted**. No external send authority. No app-state mutation authority.

No provider/live model proof. No public network API proof. No security certification.

---

## Proof Boundaries

```
not_production_readiness_certification
not_windows_service_tray_installer_proof
not_provider_live_model_proof
not_public_network_api_proof
not_app_state_mutation_proof
not_external_send_authority_proof
not_security_certification
not_automatic_repair
```

---

## Troubleshooting

**`config absent` warning:**
Run `python -m odin.cli first-run-bootstrap` to create safe defaults. Then re-run `python -m odin.cli doctor`.

**`stale lockfile` warning:**
The runtime crashed or was killed. Remove `.odin_runtime/local_runtime.lock` manually. Then retry.

**`port in use` warning:**
Another process is using the default port 8877. Change the port in config or stop the conflicting process.

**`packages not importable` failure:**
Run `python -m pip install -e .` from the repo root.

**`host blocked` failure:**
Edit `.odin_runtime/local_runtime_config.json` to set `host: "127.0.0.1"`.

---

## Claim Boundary

```
doctor_report_read_only_candidate_not_production_readiness_proof
first_run_bootstrap_local_config_only_no_app_apply_no_external_send_localhost_safe_default_not_production_readiness_proof
repair_plan_only_no_apply_no_state_mutation_no_external_send_explicit_apply_gate_required_for_any_real_repair
support_bundle_diagnostics_only_local_redacted_no_external_send_no_secret_values
```

Odin outputs candidates only. Apps own state, apply, external sends, storage, domain authority.

# Local Runtime Starter V1

**Version:** v1.0 — LRH-PR-03  
**Claim boundary:** local_runtime_starter_doc_candidate_only_no_production_readiness_claim  
**Status:** Implementation candidate

---

## Purpose

The Portable Local Runtime Starter makes Odin locally startable, stoppable and checkable
in a portable, localhost-only, proof-bound way.

It provides one clear local start/check path without requiring a Windows service,
tray app, signed installer, or admin privileges.

---

## What This Is Not

- **Not a Windows service.** Odin does not register as a Windows service.
- **Not a tray app.** Odin does not run as a system tray application.
- **Not a signed installer.** No installer is shipped or required.
- **Not production readiness proof.** Starting locally does not prove production readiness.
- **Not a live model claim.** Starting does not claim model inference is active.
- **Not a security certification.** Local start does not constitute a security audit pass.
- **Does not enable public network access.** Odin binds 127.0.0.1 only by default.
- **Does not apply external app state.** Odin outputs candidates only.
- **Does not send externally.** No external send occurs.

---

## Quick Start

```bash
# Start the local runtime (blocking; binds 127.0.0.1:8877)
python -m odin.cli start --portable

# Check runtime health
python -m odin.cli check --portable

# Stop the runtime
python -m odin.cli stop --portable

# Run bounded once-smoke proof
python -m odin.cli prove-local-runtime --once-smoke
```

Or use the included shell scripts:

```bash
# POSIX
bash scripts/start_odin.sh
bash scripts/check_odin.sh
bash scripts/stop_odin.sh

# Windows
scripts\start_odin.bat
scripts\check_odin.bat
scripts\stop_odin.bat
```

---

## Commands

### `python -m odin.cli start --portable [--host HOST] [--port PORT]`

Starts the portable local runtime.

- Default host: `127.0.0.1`
- Default port: `8877`
- Validates host is localhost only (rejects `0.0.0.0`, `::`, external IPs)
- Checks port availability before binding
- Writes a runtime lockfile at `.odin_runtime/local_runtime.lock`
- Blocks until stopped (SIGTERM or Ctrl-C)
- Cleans the lockfile on exit

**Does not:**
- Bind to `0.0.0.0` or external interfaces
- Require admin privileges
- Start a Windows service

### `python -m odin.cli stop --portable`

Stops the portable local runtime.

- Reads the lockfile to find the PID
- Sends SIGTERM to the process
- Removes the lockfile
- Safely reports `not_running` if no lockfile is found

### `python -m odin.cli check --portable [--host HOST] [--port PORT]`

Checks runtime health and reports structured status.

- Validates config (host/port)
- Checks lockfile presence
- Checks if process is alive
- Checks port status
- Returns structured JSON status

### `python -m odin.cli prove-local-runtime --once-smoke [--host HOST] [--port PORT]`

Runs a bounded local smoke proof.

- Validates config
- Verifies public bind is rejected
- Checks port availability
- Attempts `once_smoke` server bind (if port available)
- Emits `local_runtime_proof_packet` with:
  - `proven`: what is actually demonstrated
  - `not_proven`: explicit list of things NOT claimed
  - `candidate_only: true`
  - `claim_boundary`

### `python -m odin.cli validate-local-runtime-starter`

Validates the runtime starter installation:

- Scripts exist and call `python -m odin.cli`
- Config fixtures validate correctly
- Invalid public-bind fixture fails validation
- Default host is `127.0.0.1`
- Blocked hosts are blocked
- Lockfile is under `.odin_runtime/`
- Test file exists

---

## Scripts

All scripts call `python -m odin.cli` and do not embed secrets or require admin.

| Script                   | Platform | Purpose                    |
|--------------------------|----------|----------------------------|
| `scripts/start_odin.sh`  | POSIX    | Start runtime              |
| `scripts/stop_odin.sh`   | POSIX    | Stop runtime               |
| `scripts/check_odin.sh`  | POSIX    | Check runtime              |
| `scripts/start_odin.bat` | Windows  | Start runtime              |
| `scripts/stop_odin.bat`  | Windows  | Stop runtime               |
| `scripts/check_odin.bat` | Windows  | Check runtime              |

Environment variable overrides:
- `ODIN_HOST` — override default host (`127.0.0.1`)
- `ODIN_PORT` — override default port (`8877`)

---

## Runtime Directory

Runtime state is stored under `.odin_runtime/` (excluded from git).

| Path                                | Purpose                    |
|-------------------------------------|----------------------------|
| `.odin_runtime/local_runtime.lock`  | Runtime lockfile (JSON)    |

The lockfile contains:

```json
{
  "pid": 12345,
  "host": "127.0.0.1",
  "port": 8877,
  "started_by": "odin.local_runtime.starter",
  "runtime_mode": "portable_local",
  "created_at_policy": "deterministic_fixture",
  "claim_boundary": "local_runtime_lockfile_candidate_no_app_apply",
  "candidate_only": true
}
```

---

## Localhost-Only Default

Odin binds `127.0.0.1` only by default.

**Allowed hosts:** `127.0.0.1`, `localhost`, `::1`  
**Blocked by default:** `0.0.0.0`, `::`, empty string, external IPs

Attempting to start with a non-localhost host returns a structured error.
There is no override for public binding in this PR.

---

## Port-in-Use Handling

If the requested port is already in use:

- The start command returns a structured error (does not crash silently)
- The error includes `guidance` on how to resolve
- Odin does not kill other processes to claim the port
- Odin does not silently choose a random alternative port

Example structured error:

```json
{
  "status": "blocked",
  "error": "port 8877 on 127.0.0.1 is already in use",
  "error_code": "port_in_use",
  "candidate_only": true,
  "claim_boundary": "local_runtime_starter_candidate_only_no_app_apply_no_external_send"
}
```

---

## Once-Smoke Proof

`prove-local-runtime --once-smoke` runs a bounded local smoke test.

**Proven by once-smoke:**
- `config_validates_localhost_only`
- `public_bind_rejected`
- `port_availability_check_structured`
- `lockfile_semantics_deterministic`
- `local_api_once_smoke_binds_localhost`

**Not proven by once-smoke:**
- `production_readiness`
- `windows_service_or_tray_or_installer`
- `signed_installer`
- `live_model_inference`
- `security_certification`
- `public_network_api`
- `app_state_mutation`
- `external_send_authority`
- `deploy_readiness`

---

## Module Layout

```
odin/local_runtime/
  __init__.py      — exports
  config.py        — PortableRuntimeConfig, validate_config
  lockfile.py      — write/read/remove lockfile
  ports.py         — port-in-use detection
  starter.py       — start/stop/check logic
  proof.py         — once-smoke proof packet
```

---

## Troubleshooting

**Port in use:**  
Check if another Odin instance is running (`check --portable`), or choose a different port.

**Stale lockfile:**  
If `check --portable` shows `stale_lockfile`, run `stop --portable` to clean it.

**Cannot bind localhost:**  
Ensure no firewall rule blocks loopback. Try `127.0.0.1` explicitly instead of `localhost`.

**Script not executable (POSIX):**  
Run `chmod +x scripts/start_odin.sh scripts/stop_odin.sh scripts/check_odin.sh`.

---

## Proof Boundaries

This starter provides a bounded local proof only.

It does not claim:
- The runtime is production-ready
- The runtime is Windows-service-qualified
- The runtime passed a security audit
- The runtime is ready for public deployment
- Any live model inference has occurred
- Any external application has been integrated

Odin outputs candidates only. The app owns apply, state, and external sends.

---

## Next Steps

This starter is the foundation for:

- **LRH-PR-04** — Runtime Doctor, First-Run Bootstrap and Self-Healing
- **LRH-PR-05** — Localhost API Contract Hardening

---

*claim_boundary: local_runtime_starter_doc_candidate_only_no_production_readiness_claim*

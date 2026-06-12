# FINAL-PR-01: Simple Local Hub Start + Normal User Browser UI

**claim_boundary:** simple_local_hub_local_receipt_not_runtime_completion_not_production
**pr:** FINAL-PR-01
**branch:** claude/final-pr-01-local-hub-ui-sumtsa
**base:** PR #36 / SHA 9962bbe393fbf658d00be6021ad7dbceca51d2e0

---

## What Was Implemented

FINAL-PR-01 adds the first final Local Runtime Hub build slice:

1. **`odin/local_hub/` package** — Simple Local Hub server, UI generator, localhost policy, and proof packet builder (Python stdlib only, no external deps)
2. **5 new CLI commands** — `start-local-hub`, `status-local-hub`, `open-hub`, `validate-simple-local-hub`, `prove-simple-local-hub`
3. **Browser Hub HTML** — Localhost-only static page with 11 required stable IDs, normal-user copy, and Dev Mode placeholder
4. **Smoke proof** — `start-local-hub --once-smoke` starts, tests, and stops the server deterministically
5. **Proof packet** — `prove-simple-local-hub` emits `odin_simple_local_hub_proof_packet`
6. **Validator** — `validate-simple-local-hub` (integrated into `validate-all`)
7. **34-test suite** — `tests/test_simple_local_hub.py`
8. **All handoff/audit/report/schema/registry/example artifacts**

---

## Normal-User UX

When the hub is running, a normal user sees:

- **Odin is running locally.** Odin returns candidates; apps decide what to apply.
- **Runtime status:** Running — localhost only
- **Local API:** Available at 127.0.0.1:8765
- **Model:** No model is active yet. *(deferred to FINAL-PR-02)*
- **Connected Apps:** No apps are connected yet. *(deferred to FINAL-PR-02)*
- **Activity:** No recent activity. *(deferred to FINAL-PR-03)*
- **QIRC:** QIRC core is planned for a later final slice. *(deferred to FINAL-PR-03)*
- **Handoff-First:** Handoff-First prepares work before Universal Work. *(placeholder)*
- **Dev Mode:** Contains traces, receipts, proof gaps, validators, and handoff details.

---

## CLI Commands

| Command | Description |
|---|---|
| `start-local-hub --once-smoke` | Start, smoke-test, and stop the hub deterministically |
| `start-local-hub` | Scaffold: emit status and hint to use --once-smoke |
| `status-local-hub` | Check if hub is reachable; returns stopped/running JSON |
| `open-hub` | Emit the browser URL to open |
| `validate-simple-local-hub` | Run full structural validation |
| `prove-simple-local-hub` | Emit the proof packet |

---

## Server Details

- Host: 127.0.0.1 (default; configurable, localhost-only)
- Port: 8765 (default; configurable)
- Endpoints: `GET /`, `GET /status.json`, `GET /healthz`
- Implementation: Python `http.server.HTTPServer` (stdlib only)
- Localhost policy: 0.0.0.0 and public hosts rejected

---

## Localhost-Only Policy

`odin/local_hub/policy.py`:
- `ALLOWED_HOSTS`: `127.0.0.1`, `localhost`, `::1`
- `BLOCKED_HOSTS`: `0.0.0.0`, `::`, `""` (empty)
- `check_host(host)` → `(ok: bool, reason: str)`
- All forbidden hosts raise a blocked response; no public bind possible

---

## QIRC Placeholder Boundary

QIRC status in the hub is a **non-authoritative placeholder**. QIRC Core runtime is deferred to FINAL-PR-03. The hub displays: "QIRC core is planned for a later final slice." This is not a runtime proof.

---

## Handoff-First Placeholder Boundary

Handoff-First status in the hub is a **non-authoritative placeholder**. Deep handoff viewer and runtime mapping are deferred to FINAL-PR-03 or later. The hub displays: "Handoff-First prepares work before Universal Work."

---

## Proof Packet

`prove-simple-local-hub` emits:
```json
{
  "artifact_kind": "odin_simple_local_hub_proof_packet",
  "status": "ok_with_known_gaps",
  "candidate_only": true,
  "local_only": true,
  "not_proven": [
    "provider_execution", "model_inference", "qirc_core_runtime",
    "handoff_compiler_runtime", "app_bridge_runtime", "app_apply",
    "app_state_mutation", "external_send", "public_network",
    "production_readiness", "security_certification"
  ]
}
```

---

## Known Gaps

| Gap | Deferred To |
|---|---|
| Model picker behavior | FINAL-PR-02 |
| Connected apps runtime | FINAL-PR-02 |
| Demo Universal Work | FINAL-PR-02 |
| QIRC Core runtime | FINAL-PR-03 |
| Deep Handoff Viewer | FINAL-PR-03 |
| Activity/trace/receipt deep viewer | FINAL-PR-03 |
| File/spool and CLI/agent pipe | FINAL-PR-04 |
| Provider probe | FINAL-PR-04 |
| Final acceptance cleanup | FINAL-PR-05 |

---

## Non-Claims

- No production readiness
- No security certification
- No release certification
- No target-host proof
- No Windows service/tray/installer
- No provider execution
- No model inference
- No QIRC Core runtime
- No Handoff-First compiler runtime
- No external Thor/Y/Mjölnir runtime
- No real connected app integration
- No app apply/state/external-send authority
- No public network behavior

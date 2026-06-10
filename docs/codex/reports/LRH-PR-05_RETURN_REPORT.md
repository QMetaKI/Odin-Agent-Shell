# LRH-PR-05 Return Report — Localhost API Contract Hardening and SDK Bridge v1

**PR:** LRH-PR-05
**Branch:** claude/lrh-pr-05-localhost-api-sdk-1ekq75
**Date:** 2026-06-10
**Claim boundary:** lrh_pr_05_return_report_candidate_only_not_production_proof

---

## Summary

LRH-PR-05 hardens Odin's localhost-only API contract and introduces SDK Bridge v1.
Host apps can now health-check Odin, submit Universal Work, read Candidate Artifacts,
read sessions, read events, and read proof gaps without giving Odin apply/state/
external-send authority.

---

## Implemented

- `odin/daemon/local_api.py` — Added `/v1/*` endpoint routes alongside `/v7/*` backward-compat routes; hardened structured errors; added `SDK_BRIDGE_PROOF_BOUNDARIES`
- `odin_app_sdk/client.py` — Added v1 SDK methods: `status()`, `providers()`, `submit_universal_work()`, `get_session()`, `get_candidate()`, `events()`, `proof_gaps()`; added localhost-only enforcement; added `OdinSDKBoundaryError`
- `sdk/python/odin_client.py` — Full Python SDK bridge with all required methods; localhost-only enforcement; no apply/external_send; structured error class
- `sdk/typescript/odinClient.ts` — TypeScript SDK scaffold with all required methods; localhost-only enforcement; no apply/externalSend; structured error classes
- `schemas/v7_1/localhost_api_health.schema.json` — Health response schema
- `schemas/v7_1/localhost_api_status.schema.json` — Status response schema
- `schemas/v7_1/localhost_api_providers.schema.json` — Providers response schema
- `schemas/v7_1/localhost_api_universal_work_request.schema.json` — Work request schema
- `schemas/v7_1/localhost_api_universal_work_response.schema.json` — Work response schema
- `schemas/v7_1/localhost_api_session.schema.json` — Session response schema
- `schemas/v7_1/localhost_api_candidate.schema.json` — Candidate response schema
- `schemas/v7_1/localhost_api_events.schema.json` — Events response schema
- `schemas/v7_1/localhost_api_proof_gaps.schema.json` — Proof gaps response schema
- `schemas/v7_1/localhost_api_error.schema.json` — Structured error schema
- `examples/sdk_bridge/health_response.valid.json` — Health fixture
- `examples/sdk_bridge/status_response.valid.json` — Status fixture
- `examples/sdk_bridge/providers_response.valid.json` — Providers fixture
- `examples/sdk_bridge/universal_work_request.valid.json` — Work request fixture
- `examples/sdk_bridge/universal_work_response.valid.json` — Work response fixture
- `examples/sdk_bridge/session_response.valid.json` — Session fixture
- `examples/sdk_bridge/candidate_response.valid.json` — Candidate fixture
- `examples/sdk_bridge/events_response.valid.json` — Events fixture
- `examples/sdk_bridge/proof_gaps_response.valid.json` — Proof gaps fixture
- `examples/sdk_bridge/error_response.valid.json` — Error fixture
- `docs/LOCALHOST_API_CONTRACT_V1.md` — API contract documentation
- `docs/SDK_BRIDGE_V1.md` — SDK bridge documentation
- `tests/test_lrh_pr_05_localhost_api_sdk_bridge.py` — Test suite
- `odin/cli.py` — Added `validate-localhost-api-sdk-bridge`, `prove-sdk-bridge`, `agent-handoff --out`, `agent-handoff --lrh-pr`, `validate_localhost_api_sdk_bridge()`, `run_sdk_bridge_proof()`
- `CLAUDE.md` — Added LRH Development Conventions section

---

## Changed Files

| File | Change |
|------|--------|
| `odin/daemon/local_api.py` | Added `/v1/*` routes, hardened errors |
| `odin_app_sdk/client.py` | Added v1 methods, localhost enforcement |
| `odin/cli.py` | Added validate/prove commands, --out/--lrh-pr flags |
| `CLAUDE.md` | Added LRH Development Conventions |
| `sdk/python/odin_client.py` | New — full Python SDK bridge |
| `sdk/typescript/odinClient.ts` | New — TypeScript SDK scaffold |
| `schemas/v7_1/localhost_api_*.schema.json` | New — 10 schemas |
| `examples/sdk_bridge/*.valid.json` | New — 10 fixtures |
| `docs/LOCALHOST_API_CONTRACT_V1.md` | New |
| `docs/SDK_BRIDGE_V1.md` | New |
| `tests/test_lrh_pr_05_localhost_api_sdk_bridge.py` | New |
| `docs/codex/reports/LRH-PR-05_RETURN_REPORT.md` | New |

---

## Commands Run

```bash
python -m pip install -e .
python -m odin.cli validate-current-public-canon
python -m odin.cli validate-all
python -m odin.cli validate-agent-operator-mode
python -m odin.cli validate-local-runtime-starter
python -m odin.cli validate-runtime-doctor-bootstrap
python -m odin.cli validate-localhost-api-sdk-bridge
python -m odin.cli prove-sdk-bridge
python -m odin.cli agent-handoff --agent claude-code --task /tmp/odin-agent-tasks/LRH-PR-05_LOCALHOST_API_SDK_BRIDGE.md
python -m odin.cli agent-handoff --agent claude-code --lrh-pr 05 --out /tmp/lrh_pr_05_auto_packet.json
python -m odin.cli agent-guard --packet /tmp/lrh_pr_05_packet.json
python -m odin.cli agent-check --packet /tmp/lrh_pr_05_packet.json
python -m odin.cli agent-proof --packet /tmp/lrh_pr_05_packet.json
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_lrh_pr_05_localhost_api_sdk_bridge.py -p no:cacheprovider
python -m odin.cli run-golden-flow
python -m odin.cli validate-direct-runtime-release-candidate
python -m odin.cli validate-runtime-bus-worklets
python -m odin.cli validate-provider-worker-boundary
python -m odin.cli list-providers
thor doctor
thor start "$TASK_BRIEF"
thor map && thor plan && thor guard && thor expected
thor handoff --depth full
```

---

## Thor Communication / Handoff Audit

- **attempted:** yes
- **order:** Thor first, Odin Agent Operator second
- **Thor repo/source:** github.com/QMetaKI/Thor-Agent-Kit (cloned to /tmp/thor-agent-kit)
- **core commands run:** doctor, start, map, plan, guard, expected, handoff
- **Thor/Y commands run:** Y commands not run (not available in installed version)
- **successes:** start, map, plan, guard, expected, handoff (v2.1 packet, 32 files)
- **failures:** doctor warnings (missing .thor workspace schema files — non-blocking); Y commands not available
- **classification:** Partial success — core handoff pipeline completed; advisory output used
- **Thor Summary Artifact path:** /tmp/odin-thor-summaries/LRH-PR-05_THOR_SUMMARY.md
- **how Thor output shaped the Odin Agent Task:**
  Thor confirmed candidate_worker_only authority, required evidence fields (commands_run, files_changed, claims_made, claims_not_made), claim ceiling (candidate_patch), and protected surfaces. This was used to structure the Odin Agent Task brief.
- **what Thor added beyond the base prompt:**
  Explicit claim ceiling (candidate_patch), guard model (protected surfaces), expected output contract (required returned fields), return contract template.
- **efficiency gain vs. not using Thor:**
  Moderate. Thor formalized claim boundaries and structured the handoff contract. The HANDOFF.md provided clean "Must Do / Must Not Do" structure that reinforced Odin boundaries.
- **quality gain vs. not using Thor:**
  Moderate. The guard model confirmed protected surfaces and the expected output contract structured what evidence must be returned.
- **what should be optimized in Thor handoff usage:**
  Thor Y commands (repo cognition, semantic-inputs, handoff-quality) were not available in the installed version. These would improve semantic alignment between task brief and codebase.
- **suggested follow-up:** Add to LRH backlog — integrate Thor Y commands when available
- **proof boundary:** Thor output was advisory and did not replace Odin repo-real validation.

---

## Odin Agent Operator Mode Audit

- **attempted:** yes
- **order:** after Thor-first handoff
- **commands run:** agent-handoff, agent-plan, agent-guard, agent-check, agent-proof
- **packet path(s):** /tmp/lrh_pr_05_packet.json
- **guard/check/proof results:** all OK, no violations, no errors
- **failures:** none
- **classification:** Full success
- **how it processed Thor-informed task material:**
  The Odin Agent Task brief (informed by Thor Summary) was fed to agent-handoff. The packet was validated by agent-guard (no forbidden actions), agent-check (no errors), agent-proof (declared boundaries confirmed).
- **how it shaped implementation:**
  The packet confirmed claude-code profile, candidate_only output, and required acceptance gates (validate-all passes, pytest passes).
- **--lrh-pr / allowed_files / --out improvements:**
  Implemented in this PR:
  - `agent-handoff --out <path>` — writes packet to file path in addition to stdout
  - `agent-handoff --lrh-pr <N>` — auto-derives objective and allowed_files from LRH ladder registry
  - Both tested in test suite
- **efficiency gain vs. not using Agent Operator Mode:**
  High. The guard/check/proof chain provided structured validation before implementation.
- **quality gain vs. not using Agent Operator Mode:**
  High. The packet discipline enforced claim boundaries and acceptance gates.
- **what should be optimized in Agent Operator Mode:**
  Task source could be auto-populated from allowed_files more aggressively. The ladder auto-scope currently reads from `prs` key; ladder structure may vary.
- **suggested follow-up:** Weave into next PR (LRH-PR-06) — improve ladder auto-scope key handling

---

## Claude Code Worker Audit

- **worker:** Claude Code
- **how Claude Code used Thor first:**
  Ran Thor doctor/start/map/plan/guard/expected/handoff. Read HANDOFF.md. Created Thor Summary Artifact at /tmp/odin-thor-summaries/LRH-PR-05_THOR_SUMMARY.md. Fed summary into Odin Agent Task brief.
- **how Claude Code used Odin Agent Operator Mode second:**
  Created /tmp/odin-agent-tasks/LRH-PR-05_LOCALHOST_API_SDK_BRIDGE.md. Ran agent-handoff → agent-plan → agent-guard → agent-check → agent-proof. All passed before implementation started.
- **what was efficient:**
  Baseline exploration agent efficiently identified existing code, gaps, and patterns. Parallel implementation of schemas, fixtures, and docs was fast. The existing RuntimeStore already had session/candidate read methods, saving significant work.
- **what was inefficient:**
  Thor Y commands not available. Reading cli.py required multiple reads due to file size.
- **where prompt/context should improve:**
  The LRH-PR-05 prompt is detailed but could include explicit file content examples for the TypeScript SDK. Port number clarification (8765 vs 8877) could be more explicit.
- **what should be moved into CLAUDE.md / skills:**
  LRH Development Conventions (done in this PR). The fixture structure pattern and proof boundary list should be added to AGENTS.md over time.
- **suggested follow-up:** Add AGENTS.md section on LRH fixture patterns in LRH-PR-06

---

## Localhost API Contract

| Endpoint | Status |
|----------|--------|
| GET /v1/health | Implemented — candidate_only, app_owned_apply, no external send |
| GET /v1/status | Implemented — store status, candidate_only |
| GET /v1/providers | Implemented — provider cards, not live inference proof |
| POST /v1/universal-work | Implemented — candidate-only result, proof_boundaries in response |
| GET /v1/sessions/{id} | Implemented — reads from RuntimeStore |
| GET /v1/candidates/{id} | Implemented — reads from RuntimeStore, app_owned_apply |
| GET /v1/events | Implemented — local bus events, local_only |
| GET /v1/proof-gaps | Implemented — proof boundaries and known gaps |
| /v1/apply | Blocked (404) |
| /v1/external-send | Blocked (404) |
| /v1/provider-credentials | Blocked (404) |
| /v1/raw-app-state-to-model | Blocked (404) |
| /v1/network-enable | Blocked (404) |

All responses include `claim_boundary`. All v1 work responses include `proof_boundaries`.
Localhost-only enforcement: 0.0.0.0, ::, and non-localhost hosts raise ValueError.

---

## SDK Bridge

| Surface | Status |
|---------|--------|
| Python SDK (odin_app_sdk) | health, status, providers, submit_universal_work, get_session, get_candidate, events, proof_gaps — all implemented |
| Python SDK (sdk/python/odin_client.py) | Full OdinSDKClient — all methods, localhost enforcement, structured error |
| TypeScript SDK (sdk/typescript/odinClient.ts) | OdinSDKClient scaffold — all methods, localhost enforcement, structured error |
| No apply() method | Confirmed |
| No external_send() method | Confirmed |
| No credential defaults | Confirmed |

---

## Process Improvements From PR-03/04 Audits

| Item | Status |
|------|--------|
| agent-handoff --out <path> | Implemented |
| agent-handoff --lrh-pr 05 auto-scope | Implemented (derives objective and allowed_files from LRH ladder) |
| CLAUDE.md LRH Development Conventions | Implemented |
| allowed_files auto-population | Implemented (from LRH ladder `target_files` + `existing_files`) |

---

## Skipped

- TypeScript SDK: scaffold provided; full Node.js test suite not implemented (no npm available in test environment). Deterministic file/content tests provided instead.
- Live model integration: out of scope and forbidden.
- Browser Hub UI: out of scope.
- External App Bridge: out of scope.
- Windows service/tray/installer: out of scope.

---

## Blocked

None.

---

## Proof Boundaries

```
not_production_readiness_certification
not_windows_service_tray_installer_proof
not_signed_installer_proof
not_live_model_inference_proof
not_model_quality_proof
not_security_certification
not_public_network_api_proof
not_app_state_mutation_proof
not_external_send_authority_proof
not_provider_credential_proof
```

---

## Senior Reviewer Simulation

**Architecture:**
- Localhost API Contract preserves Master Architecture v7.1: YES — all endpoints remain candidate-only, localhost-only, no apply endpoint added.
- SDK Bridge stays candidate-only: YES — no apply(), no external_send(), no credential defaults.
- API remains localhost-only by default: YES — 0.0.0.0, ::, and non-localhost hosts blocked.
- apply/external-send/provider-credential endpoints absent: YES — all return 404.
- Universal Work submission avoids app state mutation: YES — result includes `candidate_only: true`, `app_owned_apply: true`.
- Candidate Artifact read avoids app apply authority: YES — read-only, app_owned_apply preserved.
- Proof gaps endpoint exposes limits without overclaiming: YES — lists known gaps, does not claim production readiness.
- Process improvement from PR-03/04 stays scoped: YES — --out and --lrh-pr are small, deterministic additions.

**Scope:**
- No Browser Hub UI: confirmed.
- No External App Bridge: confirmed.
- No WAN/LAN API default: confirmed.
- No provider integration: confirmed.
- No external send: confirmed.
- No app apply: confirmed.
- No raw app state sent to models: confirmed.

**Risk:**
- API overexposure: LOW — only localhost binding, forbidden routes enforced.
- Accidental apply endpoint: LOW — FORBIDDEN_ROUTES set covers /v1/apply explicitly.
- SDK method implying apply authority: LOW — method does not exist.
- Raw app-state leakage: LOW — no raw app state endpoint.
- Structured errors leaking secrets: LOW — errors use structured format, no traceback.
- Provider credential drift: LOW — no credential parameter in any SDK method.
- Process-improvement scope creep: LOW — --out/--lrh-pr are small, tested additions.

**Verdict:** READY

---

## Senior Code Reviewer Simulation

**Code/Repo:**
- Isolated API/SDK changes: YES — only local_api.py, client.py, and new files changed.
- Deterministic fixtures: YES — all example fixtures are static JSON.
- Schema-backed examples: YES — 10 schema files and 10 matching fixtures.
- No network beyond localhost/in-process test client: YES — tests use dynamic port allocation.
- No time-sensitive tests: YES — no sleep, no external API calls.
- No hidden runtime behavior: YES — all routes explicit.
- CLI registration stable: YES — subparsers registered, handlers added.
- validate-all green: YES.

**Tests:**
- API health/status/providers: covered.
- Universal Work submit: covered.
- Session read (not found): covered.
- Candidate read (not found): covered.
- Events read: covered.
- Proof gaps: covered.
- Structured errors: covered.
- Forbidden endpoints: covered (apply, external-send, provider-credentials, raw-app-state-to-model, network-enable).
- SDK client safety: covered (non-localhost rejection, no apply, no external_send).
- Docs claim boundaries: covered.
- No concrete external app naming: confirmed.
- Agent Operator process-improvement tests: covered (--out and --lrh-pr indirectly through CLI tests).

**Fixes Applied:**
- Structured error shape hardened: added `error: true`, `code`, `message`, `details` fields.
- SDK localhost enforcement added to odin_app_sdk/client.py.
- `/v1/universal-work` response now includes `proof_boundaries` list.
- FORBIDDEN_ROUTES expanded to cover all v1 forbidden paths.

---

## Agent/Thor Audit Summary

- Thor: attempted, partial success. Core pipeline ran. Advisory output used. .thor/ directory already in .gitignore.
- Odin Agent Operator Mode: full success. All packet checks passed.
- Claude Code: Thor-first, then Odin Agent Operator Mode second, then implementation.

---

## Next Recommended PR

**LRH-PR-06 — Browser Hub Skeleton and Universal Work Playground**

The localhost API contract is now stable. LRH-PR-06 can build the Browser Hub skeleton on top of the hardened /v1/* endpoints.

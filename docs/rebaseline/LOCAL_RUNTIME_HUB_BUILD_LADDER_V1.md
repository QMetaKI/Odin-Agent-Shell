# Local Runtime Hub Build Ladder v1

Canonical Road-to-100 ladder from current repo state to the Master Architecture v7.1-aligned Odin Local Runtime Hub target. Detailed deterministic data lives in `registries/local_runtime_hub_build_ladder_v1.json`.

This is a control-plane and planning artifact. It does not implement runtime, webapp, SDK, provider, app bridge, packaging or agent commands.

## Canonical LRH numbering

- LRH-PR-01 — Rebaseline, Legacy Quarantine, Local Runtime Hub Target
- LRH-PR-02 — Odin Agent Operator Mode
- LRH-PR-03 — Portable Local Runtime Starter
- LRH-PR-04 — Runtime Doctor, First-Run Bootstrap and Self-Healing
- LRH-PR-05 — Localhost API Contract Hardening and SDK Bridge v1
- LRH-PR-06 — Browser Odin Hub Shell
- LRH-PR-07 — Hub Runtime Dashboard and Health Surfaces
- LRH-PR-08 — Sessions, Candidates, Store and Proof Gap Viewer
- LRH-PR-09 — Bus / Worklet / Atom Trace Viewer
- LRH-PR-10 — Provider / Worker / Pre-LLM Inspector
- LRH-PR-11 — Universal Work Playground
- LRH-PR-12 — Neutral External App Bridge Pack
- LRH-PR-13 — Generic App Bridge Examples and Golden Harness
- LRH-PR-14 — Local Config, Redaction and Safe Settings UI
- LRH-PR-15 — Portable Packaging and Release ZIP
- LRH-PR-16 — Windows Convenience Layer without Full Windows App
- LRH-PR-17 — Full Acceptance, E2E Golden Flows and User Start Proof

## Agent Operator Mode insertion

LRH-PR-02 is Odin Agent Operator Mode. It defines the Codex-first / Claude-Code-equivalent repository workflow surface, Thor-compatible protocol surface and general agent boundary before portable runtime implementation begins. This is planning only: no `odin agent-*` commands, webapp, SDK bridge, provider integration or runtime behavior are implemented in this PR.

### Conceptual split

- Odin for Apps: Universal Work → Candidate Artifact.
- Odin for Coding Agents: Agent Task → Agent Work Packet → Guarded Patch/PR → Return Report.
- Odin for Agent Systems: Agent Packet → Permission Gate → Candidate Work → Proof / Return Packet.

## LRH-PR-01 — Rebaseline, Legacy Quarantine, Local Runtime Hub Target

**Objective:** Finalize the repo-real control-plane rebaseline, preserve Master Architecture v7.1, define the Local Runtime Hub target, classify current coverage, and publish the executable LRH Road-to-100 ladder without changing runtime behavior.

**Why this slice exists:** A precise, neutral, evidence-labeled baseline is required before implementation PRs can safely build toward 100 percent Local Runtime Hub coverage.

**Depends on:** none

**Current coverage:** This PR creates planning, governance, manifest, coverage, harness and prompt artifacts only; runtime behavior remains unchanged.

**Missing work:**
- future implementation receipts remain pending
- CI must re-run after merge
- manual reviewer confirmation of public naming neutrality remains required

**Target files:**
- `docs/rebaseline/`
- `registries/local_runtime_hub_build_ladder_v1.json`
- `registries/rebaseline_manifest_v1.json`
- `registries/rebaseline_coverage_matrix_v1.json`
- `registries/road_to_100_acceptance_harness_v1.json`
- `legacy/LEGACY_MAP.json`
- `tests/test_local_runtime_hub_rebaseline.py`
- `SYSTEM_MAP.json`
- `FILE_MANIFEST.json`

**Allowed new files:**
- `docs/rebaseline/`
- `docs/rebaseline/prompts/`
- `registries/local_runtime_hub_build_ladder_v1.json`
- `registries/rebaseline_manifest_v1.json`
- `registries/rebaseline_coverage_matrix_v1.json`
- `registries/road_to_100_acceptance_harness_v1.json`
- `legacy/LEGACY_INDEX.md`
- `legacy/LEGACY_MAP.json`
- `tests/test_local_runtime_hub_rebaseline.py`

**Forbidden scope:**
- no runtime behavior changes
- no webapp implementation
- no SDK bridge implementation
- no provider execution
- no app bridge implementation
- no packaging implementation
- no agent commands

**Required behavior:**
- publish neutral Road-to-100 artifacts
- preserve candidate-only and app-owned apply boundaries
- record proof gaps rather than closing them by documentation
- keep legacy quarantine as quarantine-not-delete

**Required tests:**
- test required rebaseline docs exist
- test ladder IDs and dependencies are deterministic
- test no stale current-state values remain
- test public naming neutrality in rebaseline artifacts
- test harness JSON is valid

**Required commands:**
- `python -m pip install -e .`
- `python -m odin.cli validate-current-public-canon`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_local_runtime_hub_rebaseline.py -p no:cacheprovider`
- `python -m odin.cli run-golden-flow`

**Acceptance gates:**
- current-state audit matches PR #5 branch/head policy
- LRH-PR-01..17 ladder is deterministic
- all rebaseline registries parse as JSON
- no live source file is moved to legacy
- validate-all and pytest pass

**Proof boundaries:**
- no production readiness proof
- no Windows service/tray/installer proof
- no signed installer proof
- no live model inference proof
- no model quality proof
- no security certification proof
- no public network API proof
- no app-state mutation proof
- no external send authority proof

**Senior reviewer focus:**
- confirm LRH-PR-01 preserves Master Architecture v7.1 boundaries
- confirm candidate-only and app-owned apply/state/external-send boundaries remain explicit
- confirm proof gaps are listed rather than closed by assertion

**Senior code reviewer focus:**
- confirm files touched match allowed scope
- confirm tests are deterministic and local-only
- confirm no hidden network/provider/apply behavior is added

**Expected branch name:** `codex/rebaseline-local-runtime-hub`

**Expected PR title:** REBASELINE: Local Runtime Hub Target, Legacy Quarantine and 100% Build Ladder

**Old ladder mapping:** REAL-GH-PR-01..08 plus PR-00..PR-123 and REAL-PR-01..28 traceability; this LRH slice is the forward Road-to-100 mapping.

**Definition of done:**
- current-state audit matches PR #5 branch/head policy
- LRH-PR-01..17 ladder is deterministic
- all rebaseline registries parse as JSON
- no live source file is moved to legacy
- validate-all and pytest pass
- required tests pass
- validate-all passes
- proof boundaries retained

**Next slice unlock:** LRH-PR-02 can define the agent-facing handoff/plan/guard/proof/return protocol.

## LRH-PR-02 — Odin Agent Operator Mode

**Objective:** Create the CLI/file-protocol planning surface that lets Codex, Claude Code and future coding agents use Odin as a repo-local handoff, plan, guard, proof and return-report layer, with Thor-compatible packet normalization where verified.

**Why this slice exists:** Later Codex-authored implementation PRs should operate through Odin scope/proof discipline before runtime work accelerates.

**Depends on:** LRH-PR-01

**Current coverage:** Conceptual only; partially represented through Thor-style handoff practices, Codex prompts and existing return-report discipline.

**Missing work:**
- agent-handoff command
- agent-plan command
- agent-guard command
- agent-check command
- agent-proof command
- agent-return command
- agent work packet schema
- agent return report schema
- agent permission card schema
- allowed files packet
- forbidden scope packet
- acceptance gate packet
- proof boundary packet
- Codex agent profile
- Claude Code agent profile
- generic CLI agent profile
- Thor-compatible handoff normalization
- Thor-compatible return packet mapping

**Target files:**
- `odin/agent_operator/`
- `schemas/v7_1/odin_agent_work_packet.schema.json`
- `schemas/v7_1/odin_agent_return_report.schema.json`
- `schemas/v7_1/odin_agent_permission_card.schema.json`
- `registries/agent_operator_profile_registry.json`
- `registries/thor_compatibility_registry.json`
- `examples/agent_operator/codex_work_packet.valid.json`
- `examples/agent_operator/claude_code_work_packet.valid.json`
- `examples/agent_operator/thor_compatible_packet.valid.json`
- `tests/test_lrh_pr_02_agent_operator_mode.py`
- `docs/AGENT_OPERATOR_MODE_V1.md`

**Allowed new files:**
- `odin/agent_operator/`
- `schemas/v7_1/odin_agent_work_packet.schema.json`
- `schemas/v7_1/odin_agent_return_report.schema.json`
- `schemas/v7_1/odin_agent_permission_card.schema.json`
- `registries/agent_operator_profile_registry.json`
- `registries/thor_compatibility_registry.json`
- `examples/agent_operator/`
- `tests/test_lrh_pr_02_agent_operator_mode.py`
- `docs/AGENT_OPERATOR_MODE_V1.md`

**Forbidden scope:**
- no autonomous external execution
- no hidden tool execution
- no network send by default
- no app apply authority
- no provider API integration claim
- no full Thor protocol support claim without verified mapping
- no replacement of Local Runtime Hub

**Required behavior:**
- support Codex, Claude Code and generic CLI agent profiles
- define Agent Work Packet, Permission Card and Return Report contracts
- normalize Thor-style handoff concepts only where verified
- record Thor incompatibilities as protocol gaps
- keep agents as external workers, not providers or app authority

**Required tests:**
- valid and invalid Agent Work Packet fixtures
- permission card rejects hidden tool use and external send
- Codex, Claude Code and generic CLI profiles exist
- Thor compatibility registry labels verified mappings and gaps
- return report remains candidate-only

**Required commands:**
- `future target: python -m odin.cli agent-handoff --agent codex`
- `future target: python -m odin.cli agent-handoff --agent claude-code`
- `future target: python -m odin.cli agent-plan`
- `future target: python -m odin.cli agent-guard`
- `future target: python -m odin.cli agent-check`
- `future target: python -m odin.cli agent-proof`
- `future target: python -m odin.cli agent-return`
- `python -m pip install -e .`
- `python -m odin.cli validate-current-public-canon`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_lrh_pr_02_agent_operator_mode.py -p no:cacheprovider`

**Acceptance gates:**
- Codex profile exists
- Claude Code profile exists
- generic CLI profile exists
- Thor-compatible mapping exists with verified/gap labels
- no hidden tool execution
- no autonomous external execution
- no app apply
- no provider API claim
- validate-all and pytest pass

**Proof boundaries:**
- no production readiness proof
- no Windows service/tray/installer proof
- no signed installer proof
- no live model inference proof
- no model quality proof
- no security certification proof
- no public network API proof
- no app-state mutation proof
- no external send authority proof
- no agent autonomy proof
- no full Thor protocol support proof
- Codex and Claude Code remain external workers

**Senior reviewer focus:**
- confirm LRH-PR-02 preserves Master Architecture v7.1 boundaries
- confirm candidate-only and app-owned apply/state/external-send boundaries remain explicit
- confirm proof gaps are listed rather than closed by assertion

**Senior code reviewer focus:**
- confirm files touched match allowed scope
- confirm tests are deterministic and local-only
- confirm no hidden network/provider/apply behavior is added

**Expected branch name:** `codex/lrh-pr-02-odin-agent-operator-mode`

**Expected PR title:** LRH-PR-02: Odin Agent Operator Mode

**Old ladder mapping:** REAL-GH-PR-01..08 plus PR-00..PR-123 and REAL-PR-01..28 traceability; this LRH slice is the forward Road-to-100 mapping.

**Definition of done:**
- Codex profile exists
- Claude Code profile exists
- generic CLI profile exists
- Thor-compatible mapping exists with verified/gap labels
- no hidden tool execution
- no autonomous external execution
- no app apply
- no provider API claim
- validate-all and pytest pass
- required tests pass
- validate-all passes
- proof boundaries retained

**Next slice unlock:** LRH-PR-03 can use the agent workflow discipline while adding portable start/stop/check surfaces.

## LRH-PR-03 — Portable Local Runtime Starter

**Objective:** Add portable start, stop, check and one-shot smoke surfaces for a localhost-only Odin runtime without claiming Windows service, tray, installer or production deployment proof.

**Why this slice exists:** Users need one clear local start path before doctor, API, Hub and bridge surfaces can be verified end-to-end.

**Depends on:** LRH-PR-01, LRH-PR-02

**Current coverage:** Partial runtime and local API modules exist, but no completed portable LRH start/stop/check package is claimed by this rebaseline.

**Missing work:**
- cross-platform start scripts
- cross-platform stop scripts
- cross-platform check scripts
- portable runtime config fixture
- runtime lockfile policy
- port-in-use handling
- localhost-only binding proof
- one-shot local runtime smoke proof

**Target files:**
- `scripts/start_odin.bat`
- `scripts/stop_odin.bat`
- `scripts/check_odin.bat`
- `scripts/start_odin.sh`
- `scripts/stop_odin.sh`
- `scripts/check_odin.sh`
- `odin/local_runtime/`
- `docs/LOCAL_RUNTIME_STARTER_V1.md`
- `examples/local_runtime/portable_runtime_config.valid.json`
- `tests/test_lrh_pr_03_portable_local_runtime_starter.py`

**Allowed new files:**
- `scripts/start_odin.bat`
- `scripts/stop_odin.bat`
- `scripts/check_odin.bat`
- `scripts/start_odin.sh`
- `scripts/stop_odin.sh`
- `scripts/check_odin.sh`
- `odin/local_runtime/`
- `docs/LOCAL_RUNTIME_STARTER_V1.md`
- `examples/local_runtime/`
- `tests/test_lrh_pr_03_portable_local_runtime_starter.py`

**Forbidden scope:**
- no Windows service implementation
- no tray app
- no installer claim
- no WAN/LAN binding by default
- no production readiness claim

**Required behavior:**
- one start command binds only to 127.0.0.1 by default
- stop command shuts down only the portable local runtime
- check command reports health and proof gaps
- lockfile prevents ambiguous duplicate runtime starts
- port-in-use handling returns structured guidance

**Required tests:**
- start/check smoke with local-only host fixture
- port-in-use handling test
- lockfile creation/removal test
- WAN/LAN binding rejection test
- no service/tray/installer claim test

**Required commands:**
- `future target: python -m odin.cli start --portable --host 127.0.0.1 --port 8877`
- `future target: python -m odin.cli stop --portable`
- `future target: python -m odin.cli check --portable`
- `future target: python -m odin.cli prove-local-runtime --once-smoke`
- `python -m pip install -e .`
- `python -m odin.cli validate-current-public-canon`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`

**Acceptance gates:**
- one clear start command exists
- localhost only by default
- runtime lockfile exists
- port-in-use handling exists
- health endpoint smoke works
- no WAN/LAN binding by default
- no Windows service/tray/installer claim

**Proof boundaries:**
- no production readiness proof
- no Windows service/tray/installer proof
- no signed installer proof
- no live model inference proof
- no model quality proof
- no security certification proof
- no public network API proof
- no app-state mutation proof
- no external send authority proof

**Senior reviewer focus:**
- confirm LRH-PR-03 preserves Master Architecture v7.1 boundaries
- confirm candidate-only and app-owned apply/state/external-send boundaries remain explicit
- confirm proof gaps are listed rather than closed by assertion

**Senior code reviewer focus:**
- confirm files touched match allowed scope
- confirm tests are deterministic and local-only
- confirm no hidden network/provider/apply behavior is added

**Expected branch name:** `codex/lrh-pr-03-portable-local-runtime-starter`

**Expected PR title:** LRH-PR-03: Portable Local Runtime Starter

**Old ladder mapping:** REAL-GH-PR-01..08 plus PR-00..PR-123 and REAL-PR-01..28 traceability; this LRH slice is the forward Road-to-100 mapping.

**Definition of done:**
- one clear start command exists
- localhost only by default
- runtime lockfile exists
- port-in-use handling exists
- health endpoint smoke works
- no WAN/LAN binding by default
- no Windows service/tray/installer claim
- required tests pass
- validate-all passes
- proof boundaries retained

**Next slice unlock:** LRH-PR-04 can add doctor/bootstrap checks on top of a portable start surface.

## LRH-PR-04 — Runtime Doctor, First-Run Bootstrap and Self-Healing

**Objective:** Add deterministic doctor, first-run bootstrap and plan-only repair surfaces for local runtime readiness without silently mutating user state.

**Why this slice exists:** Users need explainable setup diagnostics and safe remediation plans before API, Hub and bridge layers depend on local configuration.

**Depends on:** LRH-PR-01, LRH-PR-02, LRH-PR-03

**Current coverage:** Validation CLIs exist, but first-run bootstrap and repair planning are not a completed LRH product surface.

**Missing work:**
- doctor module
- bootstrap module
- safe first-run config generation
- plan-only repair report
- diagnostic support bundle inputs
- secret redaction checks

**Target files:**
- `odin/doctor/`
- `odin/bootstrap/`
- `docs/RUNTIME_DOCTOR_BOOTSTRAP_V1.md`
- `tests/test_lrh_pr_04_runtime_doctor_bootstrap.py`

**Allowed new files:**
- `odin/doctor/`
- `odin/bootstrap/`
- `docs/RUNTIME_DOCTOR_BOOTSTRAP_V1.md`
- `examples/doctor/`
- `tests/test_lrh_pr_04_runtime_doctor_bootstrap.py`

**Forbidden scope:**
- no automatic repair without explicit apply gate
- no secret leakage in diagnostics
- no production security claim
- no host validation claim beyond local receipts

**Required behavior:**
- self-check Python/package/import/config/store/port status
- generate safe first-run config when absent
- emit repair plan without applying changes
- support bundle includes diagnostics without secrets

**Required tests:**
- doctor success and failure fixtures
- bootstrap idempotence test
- repair plan is plan-only test
- support bundle redaction test

**Required commands:**
- `future target: python -m odin.cli doctor`
- `future target: python -m odin.cli first-run-bootstrap`
- `future target: python -m odin.cli repair-local-runtime --plan-only`
- `python -m pip install -e .`
- `python -m odin.cli validate-current-public-canon`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`

**Acceptance gates:**
- self-checks Python/package/imports/config/store/port
- first-run config generated safely
- repair is plan-only unless explicit apply gate exists
- support bundle includes diagnostics without secrets

**Proof boundaries:**
- no production readiness proof
- no Windows service/tray/installer proof
- no signed installer proof
- no live model inference proof
- no model quality proof
- no security certification proof
- no public network API proof
- no app-state mutation proof
- no external send authority proof

**Senior reviewer focus:**
- confirm LRH-PR-04 preserves Master Architecture v7.1 boundaries
- confirm candidate-only and app-owned apply/state/external-send boundaries remain explicit
- confirm proof gaps are listed rather than closed by assertion

**Senior code reviewer focus:**
- confirm files touched match allowed scope
- confirm tests are deterministic and local-only
- confirm no hidden network/provider/apply behavior is added

**Expected branch name:** `codex/lrh-pr-04-runtime-doctor-first-run-bootstrap-and-self-healing`

**Expected PR title:** LRH-PR-04: Runtime Doctor, First-Run Bootstrap and Self-Healing

**Old ladder mapping:** REAL-GH-PR-01..08 plus PR-00..PR-123 and REAL-PR-01..28 traceability; this LRH slice is the forward Road-to-100 mapping.

**Definition of done:**
- self-checks Python/package/imports/config/store/port
- first-run config generated safely
- repair is plan-only unless explicit apply gate exists
- support bundle includes diagnostics without secrets
- required tests pass
- validate-all passes
- proof boundaries retained

**Next slice unlock:** LRH-PR-05 can harden the localhost API and SDK Bridge using doctor-confirmed local configuration.

## LRH-PR-05 — Localhost API Contract Hardening and SDK Bridge v1

**Objective:** Harden the localhost-only API contract and SDK Bridge so host apps can health-check Odin, submit Universal Work and read Candidate Artifacts without giving Odin apply/state/external-send authority.

**Why this slice exists:** The Local Runtime Hub needs a stable app-facing contract before Browser Hub, playground, external app bridge and acceptance harness work.

**Depends on:** LRH-PR-03, LRH-PR-04

**Current coverage:** `odin/daemon/local_api.py`, `odin_app_sdk/` and `sdk/` exist, but this rebaseline does not claim the final LRH API/SDK contract is complete.

**Missing work:**
- schema-backed GET /v1/health
- schema-backed GET /v1/status
- schema-backed GET /v1/providers
- schema-backed POST /v1/universal-work
- schema-backed GET /v1/sessions/{id}
- schema-backed GET /v1/candidates/{id}
- schema-backed GET /v1/events
- schema-backed GET /v1/proof-gaps
- SDK health check
- SDK Universal Work submit
- SDK candidate read
- structured error contract

**Target files:**
- `odin/daemon/local_api.py`
- `odin_app_sdk/client.py`
- `sdk/python/`
- `sdk/typescript/`
- `docs/LOCALHOST_API_CONTRACT_V1.md`
- `docs/SDK_BRIDGE_V1.md`
- `tests/test_lrh_pr_05_localhost_api_sdk_bridge.py`

**Allowed new files:**
- `odin/daemon/local_api.py`
- `odin_app_sdk/client.py`
- `sdk/python/`
- `sdk/typescript/`
- `docs/LOCALHOST_API_CONTRACT_V1.md`
- `docs/SDK_BRIDGE_V1.md`
- `examples/sdk_bridge/`
- `tests/test_lrh_pr_05_localhost_api_sdk_bridge.py`

**Forbidden scope:**
- no WAN/LAN API by default
- no app apply endpoint
- no external send endpoint
- no raw app state sent to models
- no provider credential defaults

**Required behavior:**
- GET /v1/health
- GET /v1/status
- GET /v1/providers
- POST /v1/universal-work
- GET /v1/sessions/{id}
- GET /v1/candidates/{id}
- GET /v1/events
- GET /v1/proof-gaps
- SDK health check
- SDK submit universal work
- SDK read candidate
- structured errors

**Required tests:**
- API contract positive and negative tests
- localhost-only binding test
- SDK health check test
- SDK Universal Work submit test
- candidate read test
- structured error test
- no apply/external-send endpoint test

**Required commands:**
- `future target: python -m odin.cli prove-sdk-bridge`
- `python -m pip install -e .`
- `python -m odin.cli validate-current-public-canon`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_lrh_pr_05_localhost_api_sdk_bridge.py -p no:cacheprovider`

**Acceptance gates:**
- localhost-only default
- schema-backed request/response
- SDK health check
- SDK submit universal work
- SDK read candidate
- errors are structured
- no app apply
- no external send

**Proof boundaries:**
- no production readiness proof
- no Windows service/tray/installer proof
- no signed installer proof
- no live model inference proof
- no model quality proof
- no security certification proof
- no public network API proof
- no app-state mutation proof
- no external send authority proof

**Senior reviewer focus:**
- confirm LRH-PR-05 preserves Master Architecture v7.1 boundaries
- confirm candidate-only and app-owned apply/state/external-send boundaries remain explicit
- confirm proof gaps are listed rather than closed by assertion

**Senior code reviewer focus:**
- confirm files touched match allowed scope
- confirm tests are deterministic and local-only
- confirm no hidden network/provider/apply behavior is added

**Expected branch name:** `codex/lrh-pr-05-localhost-api-contract-hardening-and-sdk-bridge-v1`

**Expected PR title:** LRH-PR-05: Localhost API Contract Hardening and SDK Bridge v1

**Old ladder mapping:** REAL-GH-PR-01..08 plus PR-00..PR-123 and REAL-PR-01..28 traceability; this LRH slice is the forward Road-to-100 mapping.

**Definition of done:**
- localhost-only default
- schema-backed request/response
- SDK health check
- SDK submit universal work
- SDK read candidate
- errors are structured
- no app apply
- no external send
- required tests pass
- validate-all passes
- proof boundaries retained

**Next slice unlock:** LRH-PR-06 can serve a local browser shell against a stable API contract.

## LRH-PR-06 — Browser Odin Hub Shell

**Objective:** Create the local browser Hub shell and read-only navigation surface against the localhost API without adding app apply actions or remote networking defaults.

**Why this slice exists:** The product target requires a local web surface before dashboards, viewers and playgrounds can be layered in separate PRs.

**Depends on:** LRH-PR-04, LRH-PR-05

**Current coverage:** `odin/hub/` exists as a scaffold area, but this rebaseline does not claim browser UI runtime proof.

**Missing work:**
- static browser shell
- local asset serving
- API status client
- health panel placeholder
- navigation shell
- no-write-action constraints

**Target files:**
- `odin/hub/`
- `odin/hub/static/`
- `odin/hub/api_client.js`
- `docs/BROWSER_ODIN_HUB_SHELL_V1.md`
- `tests/test_lrh_pr_06_browser_hub_shell.py`

**Allowed new files:**
- `odin/hub/`
- `odin/hub/static/`
- `odin/hub/api_client.js`
- `docs/BROWSER_ODIN_HUB_SHELL_V1.md`
- `tests/test_lrh_pr_06_browser_hub_shell.py`

**Forbidden scope:**
- no hosted cloud UI
- no remote network default
- no app apply button
- no auth/security certification claim
- no provider execution

**Required behavior:**
- serve static/browser shell locally
- render API status
- show health panel and navigation shell
- avoid write/apply actions

**Required tests:**
- static shell served locally
- API status render test
- no write/apply control test
- no remote network default test

**Required commands:**
- `future target: python -m odin.cli prove-browser-hub --shell-only`
- `python -m pip install -e .`
- `python -m odin.cli validate-current-public-canon`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`

**Acceptance gates:**
- static/browser shell served locally
- no auth claim
- no remote network default
- health panel
- navigation shell
- API status rendering
- no write/apply actions

**Proof boundaries:**
- no production readiness proof
- no Windows service/tray/installer proof
- no signed installer proof
- no live model inference proof
- no model quality proof
- no security certification proof
- no public network API proof
- no app-state mutation proof
- no external send authority proof

**Senior reviewer focus:**
- confirm LRH-PR-06 preserves Master Architecture v7.1 boundaries
- confirm candidate-only and app-owned apply/state/external-send boundaries remain explicit
- confirm proof gaps are listed rather than closed by assertion

**Senior code reviewer focus:**
- confirm files touched match allowed scope
- confirm tests are deterministic and local-only
- confirm no hidden network/provider/apply behavior is added

**Expected branch name:** `codex/lrh-pr-06-browser-odin-hub-shell`

**Expected PR title:** LRH-PR-06: Browser Odin Hub Shell

**Old ladder mapping:** REAL-GH-PR-01..08 plus PR-00..PR-123 and REAL-PR-01..28 traceability; this LRH slice is the forward Road-to-100 mapping.

**Definition of done:**
- static/browser shell served locally
- no auth claim
- no remote network default
- health panel
- navigation shell
- API status rendering
- no write/apply actions
- required tests pass
- validate-all passes
- proof boundaries retained

**Next slice unlock:** LRH-PR-07 can populate runtime dashboard, health, doctor and proof-gap surfaces.

## LRH-PR-07 — Hub Runtime Dashboard and Health Surfaces

**Objective:** Populate the Hub with runtime dashboard, health surface, doctor surface, support bundle surface and proof-gap summary.

**Why this slice exists:** Users must see whether Odin is running, what is validated, what is missing and how to export diagnostics.

**Depends on:** LRH-PR-06

**Current coverage:** Dashboard content is not implemented or claimed by this rebaseline.

**Missing work:**
- runtime dashboard
- validation status panel
- doctor result panel
- support bundle export surface
- proof gap summary
- missing capability explanation

**Target files:**
- `odin/hub/`
- `odin/hub/static/dashboard.js`
- `docs/HUB_RUNTIME_DASHBOARD_V1.md`
- `tests/test_lrh_pr_07_hub_runtime_dashboard.py`

**Allowed new files:**
- `odin/hub/`
- `docs/HUB_RUNTIME_DASHBOARD_V1.md`
- `tests/test_lrh_pr_07_hub_runtime_dashboard.py`

**Forbidden scope:**
- no mutation through dashboard
- no hidden diagnostic upload
- no production health claim
- no browser UI proof beyond local receipts

**Required behavior:**
- show running/not-running state
- show validation status
- show missing capabilities
- export local support bundle
- summarize proof gaps

**Required tests:**
- dashboard renders health fixture
- doctor surface renders proof gaps
- support bundle export path test
- no mutation control test

**Required commands:**
- `future target: python -m odin.cli prove-browser-hub --dashboard`
- `python -m pip install -e .`
- `python -m odin.cli validate-current-public-canon`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`

**Acceptance gates:**
- user can see if Odin is running
- user can see validation status
- user can see missing capabilities
- user can export support bundle

**Proof boundaries:**
- no production readiness proof
- no Windows service/tray/installer proof
- no signed installer proof
- no live model inference proof
- no model quality proof
- no security certification proof
- no public network API proof
- no app-state mutation proof
- no external send authority proof

**Senior reviewer focus:**
- confirm LRH-PR-07 preserves Master Architecture v7.1 boundaries
- confirm candidate-only and app-owned apply/state/external-send boundaries remain explicit
- confirm proof gaps are listed rather than closed by assertion

**Senior code reviewer focus:**
- confirm files touched match allowed scope
- confirm tests are deterministic and local-only
- confirm no hidden network/provider/apply behavior is added

**Expected branch name:** `codex/lrh-pr-07-hub-runtime-dashboard-and-health-surfaces`

**Expected PR title:** LRH-PR-07: Hub Runtime Dashboard and Health Surfaces

**Old ladder mapping:** REAL-GH-PR-01..08 plus PR-00..PR-123 and REAL-PR-01..28 traceability; this LRH slice is the forward Road-to-100 mapping.

**Definition of done:**
- user can see if Odin is running
- user can see validation status
- user can see missing capabilities
- user can export support bundle
- required tests pass
- validate-all passes
- proof boundaries retained

**Next slice unlock:** LRH-PR-08 can add sessions/candidates/store/proof-gap viewers.

## LRH-PR-08 — Sessions, Candidates, Store and Proof Gap Viewer

**Objective:** Add read-only Hub views for sessions, candidate artifacts, store records and proof gaps with explicit candidate boundary banners.

**Why this slice exists:** Candidate-only output is central to Odin; users must inspect candidates and proof gaps without treating them as applied truth.

**Depends on:** LRH-PR-05, LRH-PR-07

**Current coverage:** Runtime store/candidate modules exist, but Hub candidate/store/proof-gap viewers are not complete.

**Missing work:**
- session list view
- candidate artifact viewer
- store browser
- proof gap viewer
- candidate boundary banner
- not-applied truth warnings

**Target files:**
- `odin/hub/`
- `odin/runtime/`
- `docs/HUB_CANDIDATE_STORE_VIEWER_V1.md`
- `tests/test_lrh_pr_08_candidate_store_viewer.py`

**Allowed new files:**
- `odin/hub/`
- `docs/HUB_CANDIDATE_STORE_VIEWER_V1.md`
- `tests/test_lrh_pr_08_candidate_store_viewer.py`

**Forbidden scope:**
- no apply action from candidate viewer
- no candidate shown as truth
- no store mutation through UI
- no raw sensitive payload display

**Required behavior:**
- list sessions
- display candidate artifacts
- browse store metadata
- show proof gaps
- display candidate-only boundary banner

**Required tests:**
- session list fixture test
- candidate viewer banner test
- proof gap visibility test
- no apply action test

**Required commands:**
- `future target: python -m odin.cli prove-browser-hub --candidates`
- `python -m pip install -e .`
- `python -m odin.cli validate-current-public-canon`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`

**Acceptance gates:**
- candidate artifacts visible
- proof gaps visible
- no candidate is shown as applied truth

**Proof boundaries:**
- no production readiness proof
- no Windows service/tray/installer proof
- no signed installer proof
- no live model inference proof
- no model quality proof
- no security certification proof
- no public network API proof
- no app-state mutation proof
- no external send authority proof

**Senior reviewer focus:**
- confirm LRH-PR-08 preserves Master Architecture v7.1 boundaries
- confirm candidate-only and app-owned apply/state/external-send boundaries remain explicit
- confirm proof gaps are listed rather than closed by assertion

**Senior code reviewer focus:**
- confirm files touched match allowed scope
- confirm tests are deterministic and local-only
- confirm no hidden network/provider/apply behavior is added

**Expected branch name:** `codex/lrh-pr-08-sessions-candidates-store-and-proof-gap-viewer`

**Expected PR title:** LRH-PR-08: Sessions, Candidates, Store and Proof Gap Viewer

**Old ladder mapping:** REAL-GH-PR-01..08 plus PR-00..PR-123 and REAL-PR-01..28 traceability; this LRH slice is the forward Road-to-100 mapping.

**Definition of done:**
- candidate artifacts visible
- proof gaps visible
- no candidate is shown as applied truth
- required tests pass
- validate-all passes
- proof boundaries retained

**Next slice unlock:** LRH-PR-09 can add trace viewers for bus/worklet/atom activity.

## LRH-PR-09 — Bus / Worklet / Atom Trace Viewer

**Objective:** Add read-only trace inspection for bus events, worklets, work atoms and runtime digests.

**Why this slice exists:** Traceability is required for proof discipline and debugging without granting UI mutation authority.

**Depends on:** LRH-PR-05, LRH-PR-07

**Current coverage:** Bus/worklet/work-atom structures exist, but Hub trace viewers are not complete.

**Missing work:**
- bus event viewer
- worklet trace viewer
- work atom trace viewer
- runtime digest viewer
- local-only trace filters

**Target files:**
- `odin/hub/`
- `odin/bus/`
- `odin/worklets/`
- `odin/work_atoms/`
- `docs/HUB_TRACE_VIEWER_V1.md`
- `tests/test_lrh_pr_09_trace_viewer.py`

**Allowed new files:**
- `odin/hub/`
- `docs/HUB_TRACE_VIEWER_V1.md`
- `tests/test_lrh_pr_09_trace_viewer.py`

**Forbidden scope:**
- no event mutation through UI
- no public bus exposure
- no LAN/WAN trace endpoint by default
- no sensitive raw payload display

**Required behavior:**
- display bus event timeline
- display worklet trace
- display work atom trace
- display runtime digest
- keep viewer local-only

**Required tests:**
- bus event fixture render test
- worklet trace render test
- work atom render test
- no mutation endpoint test
- local-only trace access test

**Required commands:**
- `future target: python -m odin.cli validate-runtime-bus-worklets`
- `python -m pip install -e .`
- `python -m odin.cli validate-current-public-canon`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`

**Acceptance gates:**
- trace is inspectable
- no event mutation through UI
- local-only

**Proof boundaries:**
- no production readiness proof
- no Windows service/tray/installer proof
- no signed installer proof
- no live model inference proof
- no model quality proof
- no security certification proof
- no public network API proof
- no app-state mutation proof
- no external send authority proof

**Senior reviewer focus:**
- confirm LRH-PR-09 preserves Master Architecture v7.1 boundaries
- confirm candidate-only and app-owned apply/state/external-send boundaries remain explicit
- confirm proof gaps are listed rather than closed by assertion

**Senior code reviewer focus:**
- confirm files touched match allowed scope
- confirm tests are deterministic and local-only
- confirm no hidden network/provider/apply behavior is added

**Expected branch name:** `codex/lrh-pr-09-bus-worklet-atom-trace-viewer`

**Expected PR title:** LRH-PR-09: Bus / Worklet / Atom Trace Viewer

**Old ladder mapping:** REAL-GH-PR-01..08 plus PR-00..PR-123 and REAL-PR-01..28 traceability; this LRH slice is the forward Road-to-100 mapping.

**Definition of done:**
- trace is inspectable
- no event mutation through UI
- local-only
- required tests pass
- validate-all passes
- proof boundaries retained

**Next slice unlock:** LRH-PR-10 can add provider/worker/pre-LLM inspection with agent boundaries already defined.

## LRH-PR-10 — Provider / Worker / Pre-LLM Inspector

**Objective:** Expose provider cards, worker permission cards, pre-LLM route decisions, model-work avoidance and redaction status as bounded worker visibility, not model authority.

**Why this slice exists:** The Hub must show model/provider readiness and proof gaps while preserving disabled-by-default and candidate-worker boundaries.

**Depends on:** LRH-PR-02, LRH-PR-05

**Current coverage:** Provider capability cards and provider-worker validation exist, but LRH inspector UI/API proof is not complete.

**Missing work:**
- provider card viewer
- worker permission card viewer
- pre-LLM route decision viewer
- model-work avoidance panel
- redaction status panel
- disabled-by-default visibility

**Target files:**
- `odin/hub/`
- `odin/models/`
- `odin/precompute/`
- `registries/provider_registry.json`
- `docs/PROVIDER_WORKER_INSPECTOR_V1.md`
- `tests/test_lrh_pr_10_provider_worker_inspector.py`

**Allowed new files:**
- `odin/hub/`
- `docs/PROVIDER_WORKER_INSPECTOR_V1.md`
- `tests/test_lrh_pr_10_provider_worker_inspector.py`

**Forbidden scope:**
- no live inference claim without receipt
- no provider treated as authority
- no provider credentials by default
- no agent worker/provider role confusion

**Required behavior:**
- show providers as workers
- show disabled/enabled status
- show pre-LLM route decisions
- show redaction status
- show model-work avoidance rationale

**Required tests:**
- provider card render test
- disabled-by-default fixture test
- worker permission boundary test
- no live inference claim test
- redaction status fixture test

**Required commands:**
- `future target: python -m odin.cli validate-provider-worker-boundary`
- `future target: python -m odin.cli list-providers`
- `python -m pip install -e .`
- `python -m odin.cli validate-current-public-canon`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`

**Acceptance gates:**
- providers shown as workers not authority
- disabled-by-default status visible
- live inference not claimed unless receipted

**Proof boundaries:**
- no production readiness proof
- no Windows service/tray/installer proof
- no signed installer proof
- no live model inference proof
- no model quality proof
- no security certification proof
- no public network API proof
- no app-state mutation proof
- no external send authority proof

**Senior reviewer focus:**
- confirm LRH-PR-10 preserves Master Architecture v7.1 boundaries
- confirm candidate-only and app-owned apply/state/external-send boundaries remain explicit
- confirm proof gaps are listed rather than closed by assertion

**Senior code reviewer focus:**
- confirm files touched match allowed scope
- confirm tests are deterministic and local-only
- confirm no hidden network/provider/apply behavior is added

**Expected branch name:** `codex/lrh-pr-10-provider-worker-pre-llm-inspector`

**Expected PR title:** LRH-PR-10: Provider / Worker / Pre-LLM Inspector

**Old ladder mapping:** REAL-GH-PR-01..08 plus PR-00..PR-123 and REAL-PR-01..28 traceability; this LRH slice is the forward Road-to-100 mapping.

**Definition of done:**
- providers shown as workers not authority
- disabled-by-default status visible
- live inference not claimed unless receipted
- required tests pass
- validate-all passes
- proof boundaries retained

**Next slice unlock:** LRH-PR-11 can provide a safe Universal Work playground backed by visible worker boundaries.

## LRH-PR-11 — Universal Work Playground

**Objective:** Add a local-only Universal Work playground for safe demo work packets, candidate results and proof boundary panels.

**Why this slice exists:** Users and reviewers need a controlled local flow to see Universal Work become Candidate Artifacts without app apply or external send.

**Depends on:** LRH-PR-05, LRH-PR-07

**Current coverage:** Universal Work runtime paths exist, but local Hub playground is not complete.

**Missing work:**
- local-only Universal Work form
- example work packet fixtures
- candidate result panel
- proof boundary panel
- safe demo work validation

**Target files:**
- `odin/hub/`
- `examples/universal_work_playground/`
- `docs/UNIVERSAL_WORK_PLAYGROUND_V1.md`
- `tests/test_lrh_pr_11_universal_work_playground.py`

**Allowed new files:**
- `odin/hub/`
- `examples/universal_work_playground/`
- `docs/UNIVERSAL_WORK_PLAYGROUND_V1.md`
- `tests/test_lrh_pr_11_universal_work_playground.py`

**Forbidden scope:**
- no external send
- no app apply
- no arbitrary shell execution
- no live model quality claim

**Required behavior:**
- render local-only Universal Work form
- submit safe demo Universal Work
- display candidate artifact result
- display proof boundary panel

**Required tests:**
- safe demo Universal Work fixture test
- candidate result panel test
- proof boundary panel test
- no external send/apply test

**Required commands:**
- `future target: python -m odin.cli run-golden-flow`
- `python -m pip install -e .`
- `python -m odin.cli validate-current-public-canon`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`

**Acceptance gates:**
- can submit safe demo Universal Work
- returns candidate artifact
- no app apply
- no external send

**Proof boundaries:**
- no production readiness proof
- no Windows service/tray/installer proof
- no signed installer proof
- no live model inference proof
- no model quality proof
- no security certification proof
- no public network API proof
- no app-state mutation proof
- no external send authority proof

**Senior reviewer focus:**
- confirm LRH-PR-11 preserves Master Architecture v7.1 boundaries
- confirm candidate-only and app-owned apply/state/external-send boundaries remain explicit
- confirm proof gaps are listed rather than closed by assertion

**Senior code reviewer focus:**
- confirm files touched match allowed scope
- confirm tests are deterministic and local-only
- confirm no hidden network/provider/apply behavior is added

**Expected branch name:** `codex/lrh-pr-11-universal-work-playground`

**Expected PR title:** LRH-PR-11: Universal Work Playground

**Old ladder mapping:** REAL-GH-PR-01..08 plus PR-00..PR-123 and REAL-PR-01..28 traceability; this LRH slice is the forward Road-to-100 mapping.

**Definition of done:**
- can submit safe demo Universal Work
- returns candidate artifact
- no app apply
- no external send
- required tests pass
- validate-all passes
- proof boundaries retained

**Next slice unlock:** LRH-PR-12 can formalize neutral external app bridge behavior.

## LRH-PR-12 — Neutral External App Bridge Pack

**Objective:** Create neutral external app bridge docs, SDK helper, examples and tests showing how any host app can health-check Odin, submit Universal Work and read Candidate Artifacts while owning apply/state/external send.

**Why this slice exists:** The public architecture must be reusable by external apps without binding Odin to a concrete third-party or project-specific app name.

**Depends on:** LRH-PR-05, LRH-PR-11

**Current coverage:** SDK scaffolds exist, but no neutral external app bridge pack is complete.

**Missing work:**
- external app bridge helper
- neutral bridge examples
- external app health-check fixture
- Universal Work submit fixture
- Candidate Artifact read fixture
- no concrete external app naming guard

**Target files:**
- `examples/external_app_bridge/`
- `docs/EXTERNAL_APP_BRIDGE_PACK_V1.md`
- `odin_app_sdk/external_app_bridge.py`
- `tests/test_lrh_pr_12_external_app_bridge_pack.py`

**Allowed new files:**
- `examples/external_app_bridge/`
- `docs/EXTERNAL_APP_BRIDGE_PACK_V1.md`
- `odin_app_sdk/external_app_bridge.py`
- `tests/test_lrh_pr_12_external_app_bridge_pack.py`

**Forbidden scope:**
- no concrete external app/product/project name in public artifacts
- no direct app state mutation
- no app apply in Odin
- no external send by Odin
- no hidden provider dependency

**Required behavior:**
- external app can health-check Odin
- external app can submit Universal Work
- external app can read Candidate Artifact
- external app owns apply/state/external send
- examples use neutral naming

**Required tests:**
- external app health-check fixture
- Universal Work submit fixture
- Candidate Artifact read fixture
- no direct app state mutation test
- public naming neutrality test

**Required commands:**
- `future target: python -m odin.cli prove-external-app-bridge`
- `python -m pip install -e .`
- `python -m odin.cli validate-current-public-canon`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`

**Acceptance gates:**
- external app can health-check Odin
- external app can submit Universal Work
- external app can read Candidate Artifact
- external app owns apply/state/external send
- no direct app state mutation
- no concrete external app/product/project name in public artifacts

**Proof boundaries:**
- no production readiness proof
- no Windows service/tray/installer proof
- no signed installer proof
- no live model inference proof
- no model quality proof
- no security certification proof
- no public network API proof
- no app-state mutation proof
- no external send authority proof
- no specific external app integration proof

**Senior reviewer focus:**
- confirm LRH-PR-12 preserves Master Architecture v7.1 boundaries
- confirm candidate-only and app-owned apply/state/external-send boundaries remain explicit
- confirm proof gaps are listed rather than closed by assertion

**Senior code reviewer focus:**
- confirm files touched match allowed scope
- confirm tests are deterministic and local-only
- confirm no hidden network/provider/apply behavior is added

**Expected branch name:** `codex/lrh-pr-12-neutral-external-app-bridge-pack`

**Expected PR title:** LRH-PR-12: Neutral External App Bridge Pack

**Old ladder mapping:** REAL-GH-PR-01..08 plus PR-00..PR-123 and REAL-PR-01..28 traceability; this LRH slice is the forward Road-to-100 mapping.

**Definition of done:**
- external app can health-check Odin
- external app can submit Universal Work
- external app can read Candidate Artifact
- external app owns apply/state/external send
- no direct app state mutation
- no concrete external app/product/project name in public artifacts
- required tests pass
- validate-all passes
- proof boundaries retained

**Next slice unlock:** LRH-PR-13 can add repeatable generic app bridge examples and golden harness flows.

## LRH-PR-13 — Generic App Bridge Examples and Golden Harness

**Objective:** Add neutral reference app examples and a repeatable golden harness for generic app bridge flows.

**Why this slice exists:** Bridge behavior needs repeatable examples and test receipts without naming or depending on any concrete external product.

**Depends on:** LRH-PR-05, LRH-PR-12

**Current coverage:** Generic examples exist in templates, but LRH-specific neutral app bridge golden harness is not complete.

**Missing work:**
- generic app bridge example one
- reference host app example
- golden app bridge harness
- neutral naming guard
- app-owned apply demonstration

**Target files:**
- `examples/generic_app_bridge/`
- `examples/reference_host_app/`
- `docs/GENERIC_APP_BRIDGE_GOLDEN_HARNESS_V1.md`
- `tests/test_lrh_pr_13_generic_app_bridge_golden_harness.py`

**Allowed new files:**
- `examples/generic_app_bridge/`
- `examples/reference_host_app/`
- `docs/GENERIC_APP_BRIDGE_GOLDEN_HARNESS_V1.md`
- `tests/test_lrh_pr_13_generic_app_bridge_golden_harness.py`

**Forbidden scope:**
- no concrete external app/product/project name
- no production integration claim
- no app state mutation by Odin
- no external send by Odin

**Required behavior:**
- provide at least two neutral reference app examples
- run repeatable bridge golden flow
- show app-owned apply boundary
- keep examples local-only

**Required tests:**
- two neutral example fixtures
- golden app bridge flow test
- app-owned apply boundary test
- public naming neutrality test

**Required commands:**
- `future target: python -m odin.cli prove-external-app-bridge --golden-harness`
- `python -m pip install -e .`
- `python -m odin.cli validate-current-public-canon`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`

**Acceptance gates:**
- at least two neutral reference app examples
- repeatable golden app bridge flow
- no concrete external app/product/project name
- app-owned apply preserved

**Proof boundaries:**
- no production readiness proof
- no Windows service/tray/installer proof
- no signed installer proof
- no live model inference proof
- no model quality proof
- no security certification proof
- no public network API proof
- no app-state mutation proof
- no external send authority proof
- no specific external app integration proof

**Senior reviewer focus:**
- confirm LRH-PR-13 preserves Master Architecture v7.1 boundaries
- confirm candidate-only and app-owned apply/state/external-send boundaries remain explicit
- confirm proof gaps are listed rather than closed by assertion

**Senior code reviewer focus:**
- confirm files touched match allowed scope
- confirm tests are deterministic and local-only
- confirm no hidden network/provider/apply behavior is added

**Expected branch name:** `codex/lrh-pr-13-generic-app-bridge-examples-and-golden-harness`

**Expected PR title:** LRH-PR-13: Generic App Bridge Examples and Golden Harness

**Old ladder mapping:** REAL-GH-PR-01..08 plus PR-00..PR-123 and REAL-PR-01..28 traceability; this LRH slice is the forward Road-to-100 mapping.

**Definition of done:**
- at least two neutral reference app examples
- repeatable golden app bridge flow
- no concrete external app/product/project name
- app-owned apply preserved
- required tests pass
- validate-all passes
- proof boundaries retained

**Next slice unlock:** LRH-PR-14 can add safe local settings and redaction surfaces.

## LRH-PR-14 — Local Config, Redaction and Safe Settings UI

**Objective:** Add local config schema, safe settings UI, redaction tests and disabled-by-default provider settings visibility.

**Why this slice exists:** Users need safe local configuration and proof of redaction boundaries before packaging and final acceptance.

**Depends on:** LRH-PR-05, LRH-PR-07, LRH-PR-10

**Current coverage:** Config/redaction concepts exist across docs and modules, but a cohesive LRH safe settings UI is not complete.

**Missing work:**
- local config schema
- safe settings UI
- redaction fixture suite
- unsafe setting block list
- provider settings disabled-by-default panel

**Target files:**
- `schemas/v7_1/odin_local_config.schema.json`
- `odin/hub/`
- `docs/LOCAL_CONFIG_SAFE_SETTINGS_V1.md`
- `tests/test_lrh_pr_14_local_config_safe_settings.py`

**Allowed new files:**
- `schemas/v7_1/odin_local_config.schema.json`
- `odin/hub/`
- `docs/LOCAL_CONFIG_SAFE_SETTINGS_V1.md`
- `examples/local_config/`
- `tests/test_lrh_pr_14_local_config_safe_settings.py`

**Forbidden scope:**
- no secrets in logs
- no provider enabled without explicit config
- no unsafe WAN/LAN default
- no security certification claim

**Required behavior:**
- validate local config
- show safe settings UI
- redact secrets
- block unsafe settings
- show provider settings as disabled by default

**Required tests:**
- local config schema tests
- redaction tests
- unsafe settings blocked tests
- provider disabled-by-default tests

**Required commands:**
- `future target: python -m odin.cli doctor --redaction-check`
- `python -m pip install -e .`
- `python -m odin.cli validate-current-public-canon`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`

**Acceptance gates:**
- secrets redacted
- unsafe settings blocked
- no provider enabled without explicit config

**Proof boundaries:**
- no production readiness proof
- no Windows service/tray/installer proof
- no signed installer proof
- no live model inference proof
- no model quality proof
- no security certification proof
- no public network API proof
- no app-state mutation proof
- no external send authority proof

**Senior reviewer focus:**
- confirm LRH-PR-14 preserves Master Architecture v7.1 boundaries
- confirm candidate-only and app-owned apply/state/external-send boundaries remain explicit
- confirm proof gaps are listed rather than closed by assertion

**Senior code reviewer focus:**
- confirm files touched match allowed scope
- confirm tests are deterministic and local-only
- confirm no hidden network/provider/apply behavior is added

**Expected branch name:** `codex/lrh-pr-14-local-config-redaction-and-safe-settings-ui`

**Expected PR title:** LRH-PR-14: Local Config, Redaction and Safe Settings UI

**Old ladder mapping:** REAL-GH-PR-01..08 plus PR-00..PR-123 and REAL-PR-01..28 traceability; this LRH slice is the forward Road-to-100 mapping.

**Definition of done:**
- secrets redacted
- unsafe settings blocked
- no provider enabled without explicit config
- required tests pass
- validate-all passes
- proof boundaries retained

**Next slice unlock:** LRH-PR-15 can package the portable local runtime with safe configuration included.

## LRH-PR-15 — Portable Packaging and Release ZIP

**Objective:** Create portable package generation, package manifest, checksums, included start/check scripts, support bundle path and release verification report.

**Why this slice exists:** A portable Local Runtime Hub target needs a reproducible ZIP-style package before convenience layers and final acceptance.

**Depends on:** LRH-PR-03, LRH-PR-04, LRH-PR-14

**Current coverage:** No portable release ZIP proof is claimed by this rebaseline.

**Missing work:**
- portable package build script
- package manifest
- checksums
- start/check scripts included
- support bundle included
- release verification report
- cache/build junk exclusion

**Target files:**
- `scripts/build_portable_package.py`
- `dist_manifest/`
- `docs/PORTABLE_PACKAGE_RELEASE_ZIP_V1.md`
- `tests/test_lrh_pr_15_portable_package.py`

**Allowed new files:**
- `scripts/build_portable_package.py`
- `dist_manifest/`
- `docs/PORTABLE_PACKAGE_RELEASE_ZIP_V1.md`
- `tests/test_lrh_pr_15_portable_package.py`

**Forbidden scope:**
- no signed installer proof
- no app store readiness claim
- no production deployment claim
- no generated cache/build junk committed

**Required behavior:**
- build portable package manifest
- emit checksums
- include start/check scripts
- include support bundle command path
- emit release verification report

**Required tests:**
- package manifest test
- checksum test
- start/check script inclusion test
- junk exclusion test
- support bundle path test

**Required commands:**
- `future target: python -m odin.cli prove-portable-package`
- `python -m pip install -e .`
- `python -m odin.cli validate-current-public-canon`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`

**Acceptance gates:**
- portable ZIP created
- file manifest stable
- start/check scripts included
- no generated cache/build junk

**Proof boundaries:**
- no production readiness proof
- no Windows service/tray/installer proof
- no signed installer proof
- no live model inference proof
- no model quality proof
- no security certification proof
- no public network API proof
- no app-state mutation proof
- no external send authority proof

**Senior reviewer focus:**
- confirm LRH-PR-15 preserves Master Architecture v7.1 boundaries
- confirm candidate-only and app-owned apply/state/external-send boundaries remain explicit
- confirm proof gaps are listed rather than closed by assertion

**Senior code reviewer focus:**
- confirm files touched match allowed scope
- confirm tests are deterministic and local-only
- confirm no hidden network/provider/apply behavior is added

**Expected branch name:** `codex/lrh-pr-15-portable-packaging-and-release-zip`

**Expected PR title:** LRH-PR-15: Portable Packaging and Release ZIP

**Old ladder mapping:** REAL-GH-PR-01..08 plus PR-00..PR-123 and REAL-PR-01..28 traceability; this LRH slice is the forward Road-to-100 mapping.

**Definition of done:**
- portable ZIP created
- file manifest stable
- start/check scripts included
- no generated cache/build junk
- required tests pass
- validate-all passes
- proof boundaries retained

**Next slice unlock:** LRH-PR-16 can add Windows convenience helpers without claiming a full Windows app.

## LRH-PR-16 — Windows Convenience Layer without Full Windows App

**Objective:** Add optional Windows helper scripts, shortcut/manual starter docs and convenience checks without claiming service, tray, signing or installer proof.

**Why this slice exists:** Windows users need easy manual local start while the full Windows app remains a later optional shell.

**Depends on:** LRH-PR-03, LRH-PR-15

**Current coverage:** Windows directories/docs exist, but this rebaseline does not claim Windows convenience or full app proof.

**Missing work:**
- Windows helper scripts
- optional shortcut docs
- manual starter docs
- Windows convenience smoke notes
- no service/tray/signing claim guard

**Target files:**
- `windows/`
- `scripts/start_odin.bat`
- `scripts/check_odin.bat`
- `docs/WINDOWS_CONVENIENCE_LAYER_V1.md`
- `tests/test_lrh_pr_16_windows_convenience_layer.py`

**Allowed new files:**
- `windows/`
- `scripts/start_odin.bat`
- `scripts/check_odin.bat`
- `docs/WINDOWS_CONVENIENCE_LAYER_V1.md`
- `tests/test_lrh_pr_16_windows_convenience_layer.py`

**Forbidden scope:**
- no Windows service proof
- no tray proof
- no signed installer proof
- no full Windows app claim
- no Microsoft Store claim

**Required behavior:**
- provide easy manual start on Windows
- document optional shortcut
- reuse portable start/check path
- retain proof gaps for service/tray/signing/installer

**Required tests:**
- Windows helper script lint/shape test
- manual starter doc test
- no service/tray/signing claim test

**Required commands:**
- `future target: scripts\start_odin.bat`
- `future target: scripts\check_odin.bat`
- `python -m pip install -e .`
- `python -m odin.cli validate-current-public-canon`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`

**Acceptance gates:**
- Windows user has easy manual start
- no service/tray/signing claim

**Proof boundaries:**
- no production readiness proof
- no Windows service/tray/installer proof
- no signed installer proof
- no live model inference proof
- no model quality proof
- no security certification proof
- no public network API proof
- no app-state mutation proof
- no external send authority proof

**Senior reviewer focus:**
- confirm LRH-PR-16 preserves Master Architecture v7.1 boundaries
- confirm candidate-only and app-owned apply/state/external-send boundaries remain explicit
- confirm proof gaps are listed rather than closed by assertion

**Senior code reviewer focus:**
- confirm files touched match allowed scope
- confirm tests are deterministic and local-only
- confirm no hidden network/provider/apply behavior is added

**Expected branch name:** `codex/lrh-pr-16-windows-convenience-layer-without-full-windows-app`

**Expected PR title:** LRH-PR-16: Windows Convenience Layer without Full Windows App

**Old ladder mapping:** REAL-GH-PR-01..08 plus PR-00..PR-123 and REAL-PR-01..28 traceability; this LRH slice is the forward Road-to-100 mapping.

**Definition of done:**
- Windows user has easy manual start
- no service/tray/signing claim
- required tests pass
- validate-all passes
- proof boundaries retained

**Next slice unlock:** LRH-PR-17 can run all acceptance harness proofs in a suitable environment.

## LRH-PR-17 — Full Acceptance, E2E Golden Flows and User Start Proof

**Objective:** Run the final Road-to-100 acceptance harness across local runtime, Agent Operator Mode, SDK Bridge, Browser Hub, external app bridge, portable package and support bundle proof commands.

**Why this slice exists:** The Road-to-100 target is not complete until all prior LRH gates pass with receipts and remaining external proof gaps are visible.

**Depends on:** LRH-PR-01, LRH-PR-02, LRH-PR-03, LRH-PR-04, LRH-PR-05, LRH-PR-06, LRH-PR-07, LRH-PR-08, LRH-PR-09, LRH-PR-10, LRH-PR-11, LRH-PR-12, LRH-PR-13, LRH-PR-14, LRH-PR-15, LRH-PR-16

**Current coverage:** Not implemented; this rebaseline only defines the future acceptance model.

**Missing work:**
- prove-local-runtime command
- prove-agent-operator-mode command
- prove-sdk-bridge command
- prove-browser-hub command
- prove-external-app-bridge command
- prove-portable-package command
- emit-support-bundle command
- E2E golden flow receipts
- remaining proof gap report
- public naming neutrality proof

**Target files:**
- `docs/rebaseline/ROAD_TO_100_ACCEPTANCE_HARNESS_V1.md`
- `registries/road_to_100_acceptance_harness_v1.json`
- `tests/test_lrh_pr_17_full_acceptance.py`
- `docs/FULL_ACCEPTANCE_E2E_GOLDEN_FLOWS_V1.md`

**Allowed new files:**
- `docs/rebaseline/ROAD_TO_100_ACCEPTANCE_HARNESS_V1.md`
- `registries/road_to_100_acceptance_harness_v1.json`
- `tests/test_lrh_pr_17_full_acceptance.py`
- `docs/FULL_ACCEPTANCE_E2E_GOLDEN_FLOWS_V1.md`

**Forbidden scope:**
- no production readiness claim
- no release certification claim
- no live model quality claim
- no external app-specific integration claim
- no public network API proof claim

**Required behavior:**
- run all prior LRH gates in accepting environment
- emit final proof report
- emit support bundle
- preserve candidate-only/app-owned apply boundaries
- list remaining external proof gaps

**Required tests:**
- acceptance harness schema test
- all proof commands registered
- remaining proof gaps retained
- public naming neutrality test
- candidate-only boundary test

**Required commands:**
- `future target: python -m odin.cli prove-local-runtime`
- `future target: python -m odin.cli prove-agent-operator-mode`
- `future target: python -m odin.cli prove-sdk-bridge`
- `future target: python -m odin.cli prove-browser-hub`
- `future target: python -m odin.cli prove-external-app-bridge`
- `future target: python -m odin.cli prove-portable-package`
- `future target: python -m odin.cli emit-support-bundle`
- `python -m pip install -e .`
- `python -m odin.cli validate-current-public-canon`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`

**Acceptance gates:**
- all prior LRH gates pass
- E2E local runtime proof passes in accepting environment
- candidate-only boundary preserved
- 100 percent definition satisfied
- remaining external proofs listed
- no concrete external app/product/project name in public artifacts

**Proof boundaries:**
- no production readiness proof
- no Windows service/tray/installer proof
- no signed installer proof
- no live model inference proof
- no model quality proof
- no security certification proof
- no public network API proof
- no app-state mutation proof
- no external send authority proof

**Senior reviewer focus:**
- confirm LRH-PR-17 preserves Master Architecture v7.1 boundaries
- confirm candidate-only and app-owned apply/state/external-send boundaries remain explicit
- confirm proof gaps are listed rather than closed by assertion

**Senior code reviewer focus:**
- confirm files touched match allowed scope
- confirm tests are deterministic and local-only
- confirm no hidden network/provider/apply behavior is added

**Expected branch name:** `codex/lrh-pr-17-full-acceptance-e2e-golden-flows-and-user-start-proof`

**Expected PR title:** LRH-PR-17: Full Acceptance, E2E Golden Flows and User Start Proof

**Old ladder mapping:** REAL-GH-PR-01..08 plus PR-00..PR-123 and REAL-PR-01..28 traceability; this LRH slice is the forward Road-to-100 mapping.

**Definition of done:**
- all prior LRH gates pass
- E2E local runtime proof passes in accepting environment
- candidate-only boundary preserved
- 100 percent definition satisfied
- remaining external proofs listed
- no concrete external app/product/project name in public artifacts
- required tests pass
- validate-all passes
- proof boundaries retained

**Next slice unlock:** Post-100 work can consider optional shells, deployment tracks and external proof campaigns without changing the baseline architecture.


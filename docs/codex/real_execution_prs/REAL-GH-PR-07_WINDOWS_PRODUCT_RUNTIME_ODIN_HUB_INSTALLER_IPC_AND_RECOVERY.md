# REAL-GH-PR-07 — Windows Product Runtime, Odin Hub, Installer, IPC and Recovery

## Objective

Build the Windows product shape: host/daemon/tray/control center, Odin Hub panels, process contracts, named-pipe/localhost IPC, pairing/auth policy, installer/update/rollback, safe mode, diagnostics and support bundles.

## Position in the Real Execution Chain

- Execution PR: `REAL-GH-PR-07`
- Depends on: REAL-GH-PR-06
- Legacy internal tasks covered: PR-18, PR-19, PR-98, PR-99, PR-100, PR-101, PR-102, PR-112, PR-113, PR-114, PR-115, PR-117, PR-118, PR-119, PR-120

This document is the Codex-facing real GitHub PR bundle. The older `PR-00..PR-123` task ladder and the older `REAL-PR-01..REAL-PR-28` bundle ladder are retained as internal planning detail only. Codex should build from this document when executing the real repository sequence.

## Internal Tasks Covered

- `PR-18` — Control Center Skeleton
- `PR-19` — Windows Runtime Tray and Installer Prep
- `PR-98` — Windows Product Runtime Process Model
- `PR-99` — Windows IPC Security and Pairing
- `PR-100` — Installer Update Rollback and Safe Mode
- `PR-101` — Windows Diagnostics and Support Bundle
- `PR-102` — Windows Product Runtime Consolidation Gates
- `PR-112` — Odin Hub Operational Center Core
- `PR-113` — Odin Hub Panel Map and Command Routing
- `PR-114` — Odin Hub Recovery Safe Mode and Diagnostics
- `PR-115` — Product Pattern Atom Hub Consolidation Gates
- `PR-117` — Windows Implementation Drilldown
- `PR-118` — Windows IPC Endpoint Contracts
- `PR-119` — Windows Installer Update Rollback Drilldown
- `PR-120` — MVP V1 Power Mode Boundary

## Primary Files

- `odin/windows/`
- `odin/hub/`
- `odin/diagnostics/`
- `odin/recovery/`
- `examples/windows/`
- `registries/windows_*`
- `registries/odin_hub_*`
- `docs/WINDOWS_PRODUCT_RUNTIME_LOCK_V7_1.md`
- `docs/WINDOWS_IMPLEMENTATION_DRILLDOWN_V7_1.md`
- `docs/ODIN_HUB_OPERATIONAL_CENTER_LOCK_V7_1.md`
- `tests/`

## Required Behavior

- Windows processes have explicit responsibilities
- IPC endpoints are local and capability-scoped
- Odin Hub is operational center not uncontrolled dashboard
- safe mode and rollback are available for failed packs or model/runtime issues

## Forbidden Scope

- no WAN IPC
- no privileged global mutation by tray/UI
- no installer production claim without host proof
- no support bundle secret leak
- no daemon ownership of app state

## Acceptance / Definition of Done

- Windows runtime manifest fixtures validate
- IPC endpoint contracts validate
- support bundle redaction policy exists
- MVP/V1/Power-Mode boundaries are machine-readable

Additional Definition of Done:

- `python -m odin.cli validate-all` returns no errors.
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider` returns a green suite.
- No new file claims runtime proof, host validation, production status, network proof, model-inference proof, security certification, or app-apply authority.
- All created schemas, registries, fixtures, docs and tests are included in `FILE_MANIFEST.json`.
- The PR summary explicitly separates implemented code, shadow/prep contracts, fixtures, validation results, and known proof gaps.

## Codex PR Summary Template

```text
{b['id']} — {b['title']}

Scope:
- ...

Implemented:
- ...

Validation:
- python -m odin.cli validate-all: ...
- PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider: ...

Proof gaps / non-claims:
- no runtime proof unless actually executed on host
- no model-inference proof unless actual local/remote model run is evidenced
- no app-apply authority for Odin
```

## Senior Reviewer Notes

This PR is intentionally large enough to be real-reviewable as a GitHub PR but not so large that unrelated runtime, Windows, model and release concerns are mixed without a dependency boundary. Do not split it back into the internal micro-ladder unless Codex is blocked by file-size or review-size constraints.
---

## v0.7.7 Build Ladder Absolute Alignment Addendum


This addendum is authoritative for the actual GitHub execution ladder. It separates existing prep files from target implementation paths and binds this PR to Master Architecture v7.1.

### Absorbed Internal Tasks

- `PR-18`
- `PR-19`
- `PR-98`
- `PR-99`
- `PR-100`
- `PR-101`
- `PR-102`
- `PR-112`
- `PR-113`
- `PR-114`
- `PR-115`
- `PR-117`
- `PR-118`
- `PR-119`
- `PR-120`

### Absorbed Legacy Bundles

Full absorption:

- `REAL-PR-24`
- `REAL-PR-27`

Partial absorption:

- `REAL-PR-07` — covers PR-18, PR-19 of 3 internal tasks
- `REAL-PR-28` — covers PR-117, PR-118, PR-119, PR-120 of 8 internal tasks

### Existing Prep Files / Paths

- `examples/windows/`
- `docs/WINDOWS_PRODUCT_RUNTIME_LOCK_V7_1.md`
- `docs/WINDOWS_IMPLEMENTATION_DRILLDOWN_V7_1.md`
- `docs/ODIN_HUB_OPERATIONAL_CENTER_LOCK_V7_1.md`
- `tests/`

### Target Implementation Files / Paths

- `odin/windows/`
- `odin/hub/`
- `odin/diagnostics/`
- `odin/recovery/`
- `registries/windows_*`
- `registries/odin_hub_*`

### Master Architecture Sections

- `Windows Product Runtime`
- `Odin Hub Operational Center`
- `IPC Contracts`
- `Installer / Rollback / Recovery`

### Acceptance Gates

- `Windows runtime manifest fixtures validate`
- `IPC endpoint contracts validate`
- `support bundle redaction policy exists`
- `MVP/V1/Power-Mode boundaries are machine-readable`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`
- `every created or updated artifact is registered in FILE_MANIFEST.json`
- `all proof gaps and non-claims are stated in the PR summary`

### Must Run

- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`

### Must Preserve

- `no_llm_in_app`
- `candidate_only`
- `local_first`
- `app_owns_state`
- `semantic_bus_local_only`
- `app_owns_apply`
- `gpl_2_0_only`
- `no_runtime_proof`

### Proof Boundaries

- `no_runtime_proof_without_host_receipts`
- `no_model_inference_proof_without_actual_model_receipts`
- `no_app_apply_authority_for_odin`
- `no_external_send_by_odin`
- `no_network_qirc_by_default`
- `no_production_readiness_claim`
- `no_wan_ipc`
- `no_privileged_global_mutation_by_tray/ui`
- `no_installer_production_claim_without_host_proof`
- `no_support_bundle_secret_leak`
- `no_daemon_ownership_of_app_state`

### Codex Stop Conditions

- stop if a target path would bypass the app-owned apply boundary
- stop if a model, agent, seed pack, flow pack, runtime pack or Windows component attempts to become authority
- stop if the implementation requires external network behavior not explicitly authorized by the current PR
- stop if validation cannot distinguish implemented code from shadow/prep contracts
- stop if public docs would imply host proof, model proof, security certification, or completed product behavior without receipts


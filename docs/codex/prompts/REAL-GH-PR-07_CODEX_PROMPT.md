# Codex Prompt — REAL-GH-PR-07 — Windows Product Runtime, Odin Hub, Installer, IPC and Recovery — Host-Real Track

## Base state

You are working in `Odin-Agent-Shell` after:

```text
v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK
```

This is a running runtime candidate. Do not restart from architecture-only assumptions.

## Objective

Build the Windows product shape: host/daemon/tray/control center, Odin Hub panels, process contracts, named-pipe/localhost IPC, pairing/auth policy, installer/update/rollback, safe mode, diagnostics and support bundles. Post-v0.8.6 focus: complete and harden the direct runtime candidate already materialized by ChatGPT.

## Already materialized by ChatGPT

- static Odin Hub builder
- Local API smoke path
- diagnostics/support bundle
- safe mode module
- PowerShell scripts
- service/tray stubs and Windows host docs

## Codex completion focus

- make Windows scripts robust on real Windows
- implement or scaffold real service/tray project path without overclaiming host proof
- harden localhost auth and optional named-pipe plan
- add update/rollback/safe-mode receipts
- document exact host-proof commands

## Expected deliverables

- Windows smoke scripts
- service/tray implementation path or explicit stub boundary
- Hub navigation polish
- support bundle redaction test
- host-proof checklist with receipts required

## Existing files to preserve and inspect first

- `examples/windows/`
- `docs/WINDOWS_PRODUCT_RUNTIME_LOCK_V7_1.md`
- `docs/WINDOWS_IMPLEMENTATION_DRILLDOWN_V7_1.md`
- `docs/ODIN_HUB_OPERATIONAL_CENTER_LOCK_V7_1.md`
- `tests/`

## Target/new paths allowed for this PR

- `odin/windows/`
- `odin/hub/`
- `odin/diagnostics/`
- `odin/recovery/`
- `registries/windows_*`
- `registries/odin_hub_*`

## Forbidden scope

- no WAN IPC
- no privileged global mutation by tray/UI
- no installer production claim without host proof
- no support bundle secret leak
- no daemon ownership of app state

## Required behavior

- Windows processes have explicit responsibilities
- IPC endpoints are local and capability-scoped
- Odin Hub is operational center not uncontrolled dashboard
- safe mode and rollback are available for failed packs or model/runtime issues

## Acceptance gates

- All modified registries and schemas remain JSON-valid
- Codex return report separates implemented, prepared, skipped and blocked work
- IPC endpoint contracts validate
- MVP/V1/Power-Mode boundaries are machine-readable
- No host/model/provider proof is claimed without a receipt produced in that environment
- PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
- Windows runtime manifest fixtures validate
- all proof gaps and non-claims are stated in the PR summary
- every created or updated artifact is registered in FILE_MANIFEST.json
- python -m odin.cli validate-all
- support bundle redaction policy exists

## Required commands

- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`
- `python -m odin.cli build-hub`
- `python -m odin.cli emit-support-bundle`
- `python -m odin.cli serve --host 127.0.0.1 --port 8877 --once-smoke || true`
- `python -m odin.cli validate-all`

## Must preserve

- no_llm_in_app
- candidate_only
- local_first
- app_owns_state
- semantic_bus_local_only
- app_owns_apply
- gpl_2_0_only
- no_runtime_proof

## Proof boundaries

- ChatGPT-built runtime candidate is not a substitute for host-real Codex proof
- Codex must keep app-owned apply boundary intact
- Codex must preserve GPL-2.0-only policy and no-hidden-authority posture
- no_app_apply_authority_for_odin
- no_daemon_ownership_of_app_state
- no_external_send_by_odin
- no_installer_production_claim_without_host_proof
- no_model_inference_proof_without_actual_model_receipts
- no_network_qirc_by_default
- no_privileged_global_mutation_by_tray/ui
- no_production_readiness_claim
- no_runtime_proof_without_host_receipts
- no_support_bundle_secret_leak
- no_wan_ipc

## Senior reviewer focus

- no claim of Windows service/tray/install proof without actual receipts
- local-only default
- support bundle redacts secrets
- Hub remains operational center not authority

## Return format

```text
PR: REAL-GH-PR-07
Branch:
Implemented:
Changed files:
Commands run:
Results:
Skipped:
Blocked:
Proof boundaries:
Next recommended PR:
```

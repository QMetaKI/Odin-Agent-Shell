# Road-to-100 Acceptance Harness v1

This harness defines future target proof commands for the Local Runtime Hub Road to 100 percent. Unless a future PR implements and receipts a command, each command below is a target command, not current runtime proof.

| Future proof command | Capability | Required prior LRH PR | Expected output | Proof boundary | Known non-proof |
|---|---|---|---|---|---|
| `python -m odin.cli prove-local-runtime` | portable local runtime start/check/health proof | LRH-PR-03 | local_runtime_proof_packet | candidate-only local proof receipt; app-owned apply/state/external send preserved | local proof only; not production readiness |
| `python -m odin.cli prove-agent-operator-mode` | agent handoff/plan/guard/proof/return contract proof | LRH-PR-02 | agent_operator_proof_packet | candidate-only local proof receipt; app-owned apply/state/external send preserved | not agent autonomy or provider integration |
| `python -m odin.cli prove-sdk-bridge` | SDK health/submit/read candidate proof | LRH-PR-05 | sdk_bridge_proof_packet | candidate-only local proof receipt; app-owned apply/state/external send preserved | not app apply/state/external-send proof |
| `python -m odin.cli prove-browser-hub` | local browser Hub shell/dashboard/viewer proof | LRH-PR-06..LRH-PR-09 | browser_hub_proof_packet | candidate-only local proof receipt; app-owned apply/state/external send preserved | not hosted UI or production security proof |
| `python -m odin.cli prove-external-app-bridge` | neutral external app bridge proof | LRH-PR-12..LRH-PR-13 | external_app_bridge_proof_packet | candidate-only local proof receipt; app-owned apply/state/external send preserved | not specific external app integration proof |
| `python -m odin.cli prove-portable-package` | portable ZIP/package manifest/checksum proof | LRH-PR-15 | portable_package_proof_packet | candidate-only local proof receipt; app-owned apply/state/external send preserved | not signed installer or store readiness proof |
| `python -m odin.cli emit-support-bundle` | redacted support bundle emission proof | LRH-PR-04, LRH-PR-07, LRH-PR-17 | support_bundle_manifest | candidate-only local proof receipt; app-owned apply/state/external send preserved | not security certification or support organization readiness |

## Boundaries

- The harness does not prove production readiness by existing as documentation.
- The harness does not prove Windows service/tray/installer behavior.
- The harness does not prove signed artifacts, store readiness, live model quality, public network API behavior, app-state mutation, external send authority or specific external app integration.
- Proof commands must emit receipts in future LRH implementation PRs before any capability is claimed complete.

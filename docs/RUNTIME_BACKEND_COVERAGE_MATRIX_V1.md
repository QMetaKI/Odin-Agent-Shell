# Runtime Backend Coverage Matrix V1

**Claim boundary:** `runtime_backend_coverage_local_matrix_not_production_coverage`

**LRH-PR:** LRH-PR-18  
**Status:** local coverage matrix  
**Candidate-only:** true  
**Local-only:** true

---

## What This Is

Local runtime backend coverage matrix for Odin Local Runtime Hub. Documents which backend capabilities have local receipts, which are partial, and which are retained gaps.

This is a local coverage matrix only.

---

## What This Is Not

- Not production runtime coverage
- Not target-host coverage
- Not live model execution
- Not performance certification
- Not public network API proof
- Not specific external app integration proof

---

## Coverage Summary

| Backend | LRH-PR | Status | Proof Command |
|---------|--------|--------|---------------|
| `local_api_server` | LRH-PR-05 | covered_with_receipt | `prove-sdk-bridge` |
| `runtime_store` | LRH-PR-08 | covered_with_receipt | — |
| `browser_hub_shell` | LRH-PR-06 | covered_with_receipt | `prove-browser-hub` |
| `provider_worker_pipeline` | LRH-PR-10 | covered_with_receipt | — |
| `universal_work_engine` | LRH-PR-11 | covered_with_receipt | — |
| `trace_viewer` | LRH-PR-09 | covered_with_receipt | — |
| `external_app_bridge` | LRH-PR-12 | covered_with_receipt | `prove-external-app-bridge` |
| `portable_package` | LRH-PR-15 | covered_with_receipt | `prove-portable-package` |
| `windows_convenience_layer` | LRH-PR-16 | covered_with_receipt | `prove-windows-convenience-layer` |
| `runtime_doctor_bootstrap` | LRH-PR-04 | covered_with_receipt | — |
| `agent_operator_mode` | LRH-PR-02 | covered_with_receipt | `prove-agent-operator-mode` |
| `live_model_inference` | none | retained_gap | non-goal boundary |
| `production_api_server` | none | retained_gap | non-goal boundary |
| `target_host_runtime` | none | retained_gap | non-goal boundary |

---

## Not Proven

- `production_runtime_coverage`
- `target_host_coverage`
- `live_model_execution`
- `performance_certification`
- `public_network_api_proof`
- `specific_external_app_integration_proof`

---

## Registry Location

`registries/runtime_backend_coverage_matrix_v1.json`

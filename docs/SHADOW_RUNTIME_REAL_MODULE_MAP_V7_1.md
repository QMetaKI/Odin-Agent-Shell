# Shadow Runtime to Real Module Map v7.1

| Shadow Module | Real Target | Purpose |
|---|---|---|
| policy_engine_shadow.py | odin/core/policy_engine.py | candidate-only and policy gates |
| resource_scheduler_shadow.py | odin/core/resource_posture.py | model route ceiling and resource mode |
| state_machine_shadow.py | odin/core/state_machine.py | canonical states |
| failure_recovery_shadow.py | odin/core/failure_recovery.py | safe recovery planning |
| provider_adapter_shadow.py | odin/models/providers/* | provider interface shape |
| registry_consistency_shadow.py | odin/cli.py + registry validators | drift detection |
| e2e_orchestrator_shadow.py | odin/daemon + core pipeline | near-final end-to-end flow |
| universal_work_shadow.py | odin/universal_work/* | validation and compile |
| semantic_bus_shadow.py | odin/semantic_bus/* | local bus event batch |
| candidate_shadow.py | odin/packets/* | candidate output |
| storage_trace_shadow.py | odin/storage/* | trace and receipt projection |
| api_shadow.py | odin/api/* | local API endpoint planning |

## Build Rule

Real modules should be smaller than the shadow orchestrator but preserve the same sequence, status names, failure names, boundary names and response shapes.

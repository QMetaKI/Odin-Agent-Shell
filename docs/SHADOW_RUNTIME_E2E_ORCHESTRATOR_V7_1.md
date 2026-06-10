# Shadow Runtime End-to-End Orchestrator v7.1

## Canonical Entrypoint

`odin.shadow_runtime.e2e_orchestrator_shadow.run_near_final_shadow_runtime` is the code-near map of the finished Odin runtime.

It orchestrates the full no-side-effect path:

```text
Universal Work
→ Policy Decision
→ Resource Posture
→ Secret Redaction Preview
→ Universal Work Spine
→ Semantic Bus Batch
→ Lens Selection
→ Context Distillation Plan
→ Worklet Plan
→ Gaptext Plan
→ Model Route Plan
→ Provider Adapter Plan
→ Candidate Tournament
→ Candidate Artifact
→ Candidate DNA
→ Response Packet
→ Trace Record
→ Support Bundle Plan
→ Windows Runtime Plan
```

## Contract

Input:

- `work: dict`
- `resource_profile`
- `latency_mode`
- `quality_target`
- `provider`
- `remote_allowed`

Output:

- `odin_near_final_shadow_runtime_result`

## Output Families

The output contains:

- `policy`
- `resource_posture`
- `redaction`
- `state_machine`
- `active_lenses`
- `context_plan`
- `worklet_plan`
- `gaptext`
- `provider_plan`
- `api_plan`
- `tournament`
- `trace`
- `support_bundle`
- `windows_runtime_plan`
- `model_dojo_profile`
- `thor_plan`
- `bounded_code_plan`
- `low_memory_plan`
- `app_qirc_validation`
- `spine`
- `response_packet`

## Conversion Target

Codex should split the orchestrator into real runtime services only after the invariants are tested:

- `odin/core/final_gate.py`
- `odin/protocol/binding.py`
- `odin/universal_work/universal_work_compiler.py`
- `odin/semantic_bus/bus.py`
- `odin/small_model_power/context_distillery.py`
- `odin/small_model_power/worklet_graph.py`
- `odin/small_model_power/slot_forge.py`
- `odin/models/model_router.py`
- `odin/models/providers/mock.py`
- `odin/packets/response_packet.py`
- `odin/storage/sqlite_store.py`
- `odin/api/http_server.py`

## Failure Behavior

If policy fails, the orchestrator must return a failure projection before model routing. This is required because policy failure is cheaper and safer than route selection.

Failure projection must include:

- policy result
- resource posture
- redaction result
- state machine current failure state
- failure recovery plan

## Boundary

The orchestrator remains pure. No sockets, no provider calls, no app mutation, no file writes, no external sends.

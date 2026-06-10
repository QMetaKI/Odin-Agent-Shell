# Shadow Subsystem Coverage Matrix v7.1

## Matrix

| Contract | Shadow Module | Real Target | Fixture | Internal PR | REAL Bundle |
|---|---|---|---|---|---|
| binding_gate | odin/shadow_runtime/boundary.py | odin/protocol/binding.py | direct_apply_blocked.invalid.json | PR-23 | REAL-PR-09 |
| universal_work_compile | odin/shadow_runtime/universal_work_shadow.py | odin/universal_work/universal_work_compiler.py | markdown_rewrite_shadow_flow.valid.json | PR-23 | REAL-PR-09 |
| semantic_bus_batch | odin/shadow_runtime/semantic_bus_shadow.py | odin/semantic_bus/bus.py | semantic_bus_shadow_batch.valid.json | PR-23 | REAL-PR-09 |
| model_route_plan | odin/shadow_runtime/model_route_shadow.py | odin/models/model_router.py | model_route_standard.valid.json | PR-23 | REAL-PR-09 |
| candidate_response_packet | odin/shadow_runtime/candidate_shadow.py | odin/packets/response_packet.py | markdown_rewrite_shadow_flow.valid.json | PR-23 | REAL-PR-09 |
| artifact_lens_context_distillery | odin/shadow_runtime/artifact_lens_context_shadow.py | odin/small_model_power/context_distillery.py | artifact_lens_context_shadow.valid.json | PR-24 | REAL-PR-10 |
| worklet_slot_gaptext | odin/shadow_runtime/worklet_slot_shadow.py | odin/small_model_power/worklet_graph.py | worklet_slot_gaptext_shadow.valid.json | PR-24 | REAL-PR-10 |
| candidate_tournament | odin/shadow_runtime/candidate_tournament_shadow.py | odin/small_model_power/candidate_tournament.py | candidate_tournament_shadow.valid.json | PR-24 | REAL-PR-10 |
| low_memory_strict | odin/shadow_runtime/low_memory_shadow.py | odin/models/fallback_ladder.py | low_memory_shadow.valid.json | PR-24 | REAL-PR-10 |
| thor_bridge | odin/shadow_runtime/thor_bridge_shadow.py | odin/thor_bridge/thor_adapter.py | thor_bridge_shadow.valid.json | PR-24 | REAL-PR-10 |
| bounded_code_work | odin/shadow_runtime/bounded_code_shadow.py | odin/thor_bridge/bounded_code_work.py | bounded_code_shadow.valid.json | PR-24 | REAL-PR-10 |
| storage_trace_receipt | odin/shadow_runtime/storage_trace_shadow.py | odin/storage/sqlite_store.py | storage_trace_shadow.valid.json | PR-24 | REAL-PR-10 |
| api_endpoint_plan | odin/shadow_runtime/api_shadow.py | odin/api/http_server.py | api_shadow.valid.json | PR-24 | REAL-PR-10 |
| app_qirc_digest_bridge | odin/shadow_runtime/app_qirc_bridge_shadow.py | odin/apps/app_qirc_bridge.py | app_qirc_bridge_shadow.valid.json | PR-24 | REAL-PR-10 |
| model_dojo_scoreboard | odin/shadow_runtime/model_dojo_shadow.py | odin/small_model_power/model_dojo.py | model_dojo_shadow.valid.json | PR-24 | REAL-PR-10 |
| security_redaction | odin/shadow_runtime/security_redaction_shadow.py | odin/core/claim_boundary.py | security_redaction_shadow.valid.json | PR-24 | REAL-PR-10 |
| support_bundle | odin/shadow_runtime/support_bundle_shadow.py | odin/storage/object_store.py | support_bundle_shadow.valid.json | PR-24 | REAL-PR-10 |
| windows_runtime_plan | odin/shadow_runtime/windows_runtime_shadow.py | odin/daemon.py | windows_runtime_shadow.valid.json | PR-24 | REAL-PR-10 |
| sdk_template_validation | odin/shadow_runtime/sdk_template_shadow.py | templates/app_connector/ | sdk_template_shadow.valid.json | PR-24 | REAL-PR-10 |

## Boundary

The full coverage matrix is a build bridge. It is not proof of live runtime behavior. All entries are pure, deterministic, in-memory candidate shapes.

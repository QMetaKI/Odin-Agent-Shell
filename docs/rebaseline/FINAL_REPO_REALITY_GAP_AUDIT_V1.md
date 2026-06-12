# Final Repo-Reality Gap Audit v1

Artifact id: `final_repo_reality_gap_audit_v1`.

Claim boundary: `planning_audit_only_not_runtime_provider_network_target_host_security_release_or_model_quality_proof`. This artifact is a repo-real planning/audit artifact only. It does not start runtime, run providers, call models, call network, read secrets, mutate app state, certify security, certify release status, prove target hosts, or prove live model quality.

Supersedes and source references are machine-readable in the matching registry.

## Summary

- implemented_without_recent_local_proof: 8
- partially_implemented: 18
- schema_or_doc_only: 5
- missing: 6
- deferred_non_goal: 1

## Capability Rows

| capability | status | recommended slice | missing work |
|---|---|---|---|
| `clone_install_path` | `partially_implemented` | `docs_quickstart_polish` | Build or finish clone_install_path in the mapped final slice and attach scoped receipts. |
| `one_command_start` | `implemented_without_recent_local_proof` | `simple_local_hub_start` | No missing work beyond receipt refresh. |
| `localhost_runtime_api` | `implemented_without_recent_local_proof` | `simple_local_hub_start` | No missing work beyond receipt refresh. |
| `browser_hub_ui` | `partially_implemented` | `browser_hub_normal_user_ui` | Build or finish browser_hub_ui in the mapped final slice and attach scoped receipts. |
| `model_picker` | `partially_implemented` | `model_picker_provider_status` | Build or finish model_picker in the mapped final slice and attach scoped receipts. |
| `multiple_models` | `schema_or_doc_only` | `model_picker_provider_status` | Build or finish multiple_models in the mapped final slice and attach scoped receipts. |
| `provider_status` | `partially_implemented` | `model_picker_provider_status` | Build or finish provider_status in the mapped final slice and attach scoped receipts. |
| `connected_apps_view` | `partially_implemented` | `connected_apps_bridge_view` | Build or finish connected_apps_view in the mapped final slice and attach scoped receipts. |
| `app_bridge` | `partially_implemented` | `connected_apps_bridge_view` | Build or finish app_bridge in the mapped final slice and attach scoped receipts. |
| `sdk_bridge` | `implemented_without_recent_local_proof` | `connected_apps_bridge_view` | No missing work beyond receipt refresh. |
| `universal_work_submit` | `implemented_without_recent_local_proof` | `demo_universal_work_flow` | No missing work beyond receipt refresh. |
| `candidate_artifact_response` | `implemented_without_recent_local_proof` | `demo_universal_work_flow` | No missing work beyond receipt refresh. |
| `response_packet_view` | `partially_implemented` | `demo_universal_work_flow` | Build or finish response_packet_view in the mapped final slice and attach scoped receipts. |
| `activity_feed` | `missing` | `activity_trace_receipt_view` | Build or finish activity_feed in the mapped final slice and attach scoped receipts. |
| `trace_viewer` | `partially_implemented` | `activity_trace_receipt_view` | Build or finish trace_viewer in the mapped final slice and attach scoped receipts. |
| `receipt_viewer` | `schema_or_doc_only` | `activity_trace_receipt_view` | Build or finish receipt_viewer in the mapped final slice and attach scoped receipts. |
| `proof_gap_viewer` | `partially_implemented` | `dev_mode_diagnostics` | Build or finish proof_gap_viewer in the mapped final slice and attach scoped receipts. |
| `support_bundle` | `implemented_without_recent_local_proof` | `dev_mode_diagnostics` | No missing work beyond receipt refresh. |
| `dev_mode_toggle` | `missing` | `dev_mode_diagnostics` | Build or finish dev_mode_toggle in the mapped final slice and attach scoped receipts. |
| `local_provider_probe` | `missing` | `local_provider_probe` | Build or finish local_provider_probe in the mapped final slice and attach scoped receipts. |
| `mock_provider` | `partially_implemented` | `model_picker_provider_status` | Build or finish mock_provider in the mapped final slice and attach scoped receipts. |
| `ollama_candidate` | `schema_or_doc_only` | `local_provider_probe` | Build or finish ollama_candidate in the mapped final slice and attach scoped receipts. |
| `llama_cpp_candidate` | `schema_or_doc_only` | `local_provider_probe` | Build or finish llama_cpp_candidate in the mapped final slice and attach scoped receipts. |
| `no_remote_fallback` | `partially_implemented` | `runtime_security_smoke` | Build or finish no_remote_fallback in the mapped final slice and attach scoped receipts. |
| `qirc_semantic_bus` | `partially_implemented` | `activity_trace_receipt_view` | Build or finish qirc_semantic_bus in the mapped final slice and attach scoped receipts. |
| `worklet_slot_gaptext_visibility` | `schema_or_doc_only` | `dev_mode_diagnostics` | Build or finish worklet_slot_gaptext_visibility in the mapped final slice and attach scoped receipts. |
| `ki_ohne_ki_precompute_visibility` | `partially_implemented` | `dev_mode_diagnostics` | Build or finish ki_ohne_ki_precompute_visibility in the mapped final slice and attach scoped receipts. |
| `agent_operator_mode` | `implemented_without_recent_local_proof` | `final_acceptance_cleanup` | No missing work beyond receipt refresh. |
| `thor_compatibility` | `partially_implemented` | `final_acceptance_cleanup` | Build or finish thor_compatibility in the mapped final slice and attach scoped receipts. |
| `golden_flow` | `partially_implemented` | `final_acceptance_cleanup` | Build or finish golden_flow in the mapped final slice and attach scoped receipts. |
| `full_acceptance_local_receipt` | `partially_implemented` | `final_acceptance_cleanup` | Build or finish full_acceptance_local_receipt in the mapped final slice and attach scoped receipts. |
| `security_static_review` | `implemented_without_recent_local_proof` | `runtime_security_smoke` | No missing work beyond receipt refresh. |
| `runtime_security_review` | `missing` | `runtime_security_smoke` | Build or finish runtime_security_review in the mapped final slice and attach scoped receipts. |
| `target_host_review` | `missing` | `target_host_smoke` | Build or finish target_host_review in the mapped final slice and attach scoped receipts. |
| `dependency_tooling` | `missing` | `runtime_security_smoke` | Build or finish dependency_tooling in the mapped final slice and attach scoped receipts. |
| `release_package` | `partially_implemented` | `docs_quickstart_polish` | Build or finish release_package in the mapped final slice and attach scoped receipts. |
| `windows_convenience` | `deferred_non_goal` | `target_host_smoke` | Build or finish windows_convenience in the mapped final slice and attach scoped receipts. |
| `normal_user_docs` | `partially_implemented` | `docs_quickstart_polish` | Build or finish normal_user_docs in the mapped final slice and attach scoped receipts. |

## Plain Answer

Architecture and contracts are broad; normal-user runtime hub completion is not yet fully visible. Missing blockers are the unified normal-user Hub path, activity/dev diagnostics integration, local provider probe receipts, and final acceptance receipts.

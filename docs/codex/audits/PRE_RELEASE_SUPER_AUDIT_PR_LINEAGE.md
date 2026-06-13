# PRE-RELEASE SUPER AUDIT — PR Lineage

| PR/workstream | Status | Release relevance | Evidence |
| --- | --- | --- | --- |
| 1 FINAL-PR-01 Simple Local Hub | active | required | odin/local_hub/server.py, odin/local_hub/ui.py |
| 2 FINAL-PR-02 Model Picker + Connected Apps + Demo Universal Work | active | required | odin/local_hub/model_picker.py, odin/local_hub/connected_apps.py, odin/local_hub/demo_universal_work.py |
| 3 FINAL-PR-03 QIRC Core + Activity/Trace/Receipt + Dev Mode | active | required | odin/qirc_core/bus.py |
| 4 FINAL-PR-04 Local Candidate Provider Probe + Policy | active | required | odin/runtime_security/smoke.py |
| 5 FINAL-PR-05 Execution Gate + Mock Provider + Proof Chain | active | required | odin/execution_gate/gateway.py, odin/execution_gate/mock_provider.py, odin/proof_chain/registry.py |
| 42 Y Pattern Spine | active | required | odin/y_pattern_spine/profiles.py |
| 44 Prep FINAL-PR-06..08 | active | required | tools/rebaseline/check_prep_final_pr_06_08.py |
| 45 FINAL-PR-06 Operational Seed Spine | active | required | odin/operational_seed_spine/selector.py, odin/operational_seed_spine/work_capsule.py |
| 46 FINAL-PR-07 Field Selection Spine | active | required | odin/field_selection_spine/selector.py, odin/field_selection_spine/coherence.py |
| 47 FINAL-PR-08 Projection Candidate Spine | active | required | odin/projection_candidate_spine/projection_set.py, odin/projection_candidate_spine/candidate_graph.py |
| 34 PR #34 / B8 Static Security Review Track | active_but_partial | useful | tools/v7_1_1/check_b8_security_review_track.py, reports/v7_1_1_b8_security_review_report.json |
| 35 PR #35 Final Road-to-100 Audit | unknown | useful |  |
| 36 PR #36 Handoff-First Layer | unknown | required |  |
| 27 B1 App Boundary + Universal Work + QIRC Spine | active | required | tools/v7_1_1/check_b1_app_boundary_universal_work_qirc_spine.py, reports/v7_1_1_b1_app_boundary_universal_work_qirc_spine_report.json |
| 28 B2 Context / Lenses / Worklets / Slot Forge / Gaptext | active_but_partial | useful | registries/v7_1_1_artifact_lens_registry.json |
| 29 B3 ModelWorkPacket / Scale Ladder / Hybrid Director | active | required | registries/v7_1_1_model_scale_ladder_registry.json, schemas/v7_1_1_modelworkpacket.schema.json |
| 30 B4 Minicheck / Critics / Tournament / Candidate Final Gate | active_but_partial | useful | odin/candidates/tournament.py, odin/core/final_gate.py |
| 31 B5 Storage Trace Receipt Provider Bridge Prep | active_but_partial | useful | odin/runtime/store.py, reports/v7_1_1_b5_storage_trace_receipt_provider_bridge_report.json |
| 32 B6 Acceptance Dojo Scoreboard Closure Prep | active_but_partial | useful | reports/v7_1_1_b6_acceptance_dojo_scoreboard_closure_report.json |
| 33 B7 Closure Thor Provider Eval Gates | active_but_partial | useful | reports/v7_1_1_b7_closure_thor_provider_eval_report.json |

Classifications are audit estimates from repo files and recent git history, not assumptions that every historical artifact remains active.

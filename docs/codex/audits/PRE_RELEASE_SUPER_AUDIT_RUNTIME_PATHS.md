# PRE-RELEASE SUPER AUDIT — Runtime Paths

All paths are local deterministic smoke paths. Public network, provider calls, API keys, and app-owned apply are out of scope.

| Path | Kind | Status | Duration | Excerpt |
| --- | --- | --- | --- | --- |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli validate-projection-candidate-spine | cli | pass | 0.189 | {   "candidate_only": true,   "checked_files": [     "docs/codex/audits/FINAL_PR_08_CODE_REVIEW.md",     "docs/codex/aud |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli validate-field-selection-spine | cli | pass | 0.196 | {   "candidate_only": true,   "checked_files": [     "docs/codex/audits/FINAL_PR_07_CODE_REVIEW.md",     "docs/codex/aud |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli validate-operational-seed-spine | cli | pass | 0.192 | validate-operational-seed-spine: OK |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli validate-all | cli | pass | 2.27 | {   "candidate_only": true,   "claim_boundary": "simple_local_hub_validator_candidate_only_no_app_apply_no_external_send |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli explain-projection-candidate --demo | cli | pass | 0.213 | {   "candidate_graph": {     "candidate_only": true,     "claim_boundary": "projection_candidate_spine_prepares_candidat |
| PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider --tb=no | pytest | skipped | 0.0 | Skipped in lightweight audit mode; run without --lightweight for full smoke. |
| GET /healthz | endpoint | pass | 0.005 | {"status":"ok","hub":"simple_local_hub","version":"final_pr_02"} |
| GET /status.json | endpoint | pass | 0.001 | {   "status": "ok",   "hub": "simple_local_hub",   "version": "final_pr_01",   "candidate_only": true,   "local_only": t |
| GET / | endpoint | pass | 0.001 | <!DOCTYPE html> <html lang="en"> <head>   <meta charset="UTF-8">   <meta name="viewport" content="width=device-width, in |
| GET /demo/universal-work.json | endpoint | pass | 0.004 | {   "artifact_kind": "odin_demo_universal_work_info",   "candidate_only": true,   "description": "POST to /demo/universa |
| GET /activity.json | endpoint | pass | 0.001 | {   "artifact_kind": "odin_activity_list",   "candidate_only": true,   "local_only": true,   "events": [     {       "ev |
| GET /receipts.json | endpoint | pass | 0.001 | {   "artifact_kind": "odin_receipts",   "candidate_only": true,   "local_only": true,   "events": [],   "claim_boundary" |
| GET /providers/probe.json | endpoint | pass | 0.004 | {   "artifact_kind": "odin_provider_status_packet",   "candidate_only": true,   "local_only": true,   "provider_executio |
| GET /execution-gate/status.json | endpoint | pass | 0.005 | {   "artifact_kind": "odin_execution_gate_policy",   "execution_gate_enabled": true,   "mock_execution_allowed": true,   |
| POST /execution-gate/mock | endpoint | pass | 0.001 | {   "artifact_kind": "odin_mock_execution_response_packet",   "provider_id": "mock",   "execution_kind": "mock_determini |
| GET /final-pr-ladder/scaffold.json | endpoint | pass | 0.002 | {   "artifact_kind": "odin_final_pr_worker_packet_scaffold",   "target_pr_id": "FINAL-PR-06",   "source_return_report":  |
| GET /demo/y-route.json | endpoint | pass | 0.011 | {   "artifact_kind": "y_route_explanation_demo",   "candidate_only": true,   "input_kind": "demo_universal_work",   "can |
| GET /demo/seed-route.json | endpoint | pass | 0.007 | {   "status": "ok",   "candidate_only": true,   "claim_boundary": "operational_seed_spine_routes_work_not_authority",    |
| GET /demo/field-selection.json | endpoint | pass | 0.01 | {   "status": "ok",   "candidate_only": true,   "claim_boundary": "field_selection_scores_routes_not_truth",   "field_se |
| GET /demo/projection-candidate.json | endpoint | pass | 0.007 | {   "status": "ok",   "candidate_only": true,   "claim_boundary": "projection_candidate_spine_prepares_candidates_not_ru |
| import odin | import | pass | 0.046 | import ok |
| import odin.cli | import | pass | 0.154 | import ok |
| import odin.local_hub.server | import | pass | 0.113 | import ok |
| import odin.qirc_core.bus | import | pass | 0.079 | import ok |
| import odin.execution_gate.gateway | import | pass | 0.08 | import ok |
| import odin.providers.probe | import | pass | 0.084 | import ok |
| import odin.operational_seed_spine.selector | import | pass | 0.087 | import ok |
| import odin.field_selection_spine.selector | import | pass | 0.084 | import ok |
| import odin.projection_candidate_spine.projection_set | import | pass | 0.08 | import ok |
| import odin.proof_chain.registry | import | pass | 0.053 | import ok |

# PRE-RELEASE SUPER AUDIT — Runtime Paths

All paths are local deterministic smoke paths. Public network, provider calls, API keys, and app-owned apply are out of scope.

| Path | Kind | Status | Duration | Excerpt |
| --- | --- | --- | --- | --- |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli validate-projection-candidate-spine | cli | pass | 0.278 | {   "candidate_only": true,   "checked_files": [     "docs/codex/audits/FINAL_PR_08_CODE_REVIEW.md",     "docs/codex/aud |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli validate-field-selection-spine | cli | pass | 0.271 | {   "candidate_only": true,   "checked_files": [     "docs/codex/audits/FINAL_PR_07_CODE_REVIEW.md",     "docs/codex/aud |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli validate-operational-seed-spine | cli | pass | 0.274 | validate-operational-seed-spine: OK |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli validate-prep-final-pr-06-08 | cli | pass | 0.265 | check_prep_final_pr_06_08: OK validate-prep-final-pr-06-08: OK |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli validate-y-pattern-spine | cli | pass | 0.252 | {   "candidate_only": true,   "claim_boundary": "y_pattern_spine_validator_candidate_only_no_provider_no_app_apply",   " |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli validate-final-pr-05-execution-gate | cli | pass | 0.257 | validate-final-pr-05-execution-gate: OK |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli validate-all | cli | pass | 3.033 | {   "candidate_only": true,   "claim_boundary": "simple_local_hub_validator_candidate_only_no_app_apply_no_external_send |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli explain-projection-candidate --demo | cli | pass | 0.307 | {   "candidate_graph": {     "candidate_only": true,     "claim_boundary": "projection_candidate_spine_prepares_candidat |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli prove-projection-candidate-spine | cli | pass | 0.246 | {   "app_owned_apply": true,   "artifact_kind": "odin_projection_candidate_spine_proof_packet",   "candidate_only": true |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli explain-field-selection --demo | cli | pass | 0.249 | {   "app_owned_apply": true,   "candidate_only": true,   "claim_boundary": "field_selection_scores_routes_not_truth",    |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli prove-field-selection-spine | cli | pass | 0.265 | {   "app_owned_apply": true,   "artifact_kind": "odin_field_selection_spine_proof_packet",   "candidate_only": true,   " |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli explain-seed-route --demo | cli | pass | 0.255 | {   "candidate_only": true,   "claim_boundary": "operational_seed_spine_routes_work_not_authority",   "fallback_used": f |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli prove-operational-seed-spine | cli | pass | 0.246 | {   "app_owned_apply": true,   "artifact_kind": "odin_operational_seed_spine_proof_packet",   "candidate_only": true,    |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli doctor | cli | pass | 0.269 | {   "artifact_kind": "odin_doctor_report",   "candidate_only": true,   "checks": [     {       "check": "python_version" |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli provider-status | cli | pass | 0.236 | {   "api_key_reads": false,   "artifact_kind": "odin_provider_status_packet",   "candidate_only": true,   "claim_boundar |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli runtime-security-smoke | cli | pass | 0.258 | {   "api_key_reads": false,   "artifact_kind": "odin_runtime_security_smoke_result",   "candidate_only": true,   "claim_ |
| /root/.pyenv/versions/3.12.13/bin/python -m pytest -q -p no:cacheprovider --tb=no | pytest | pass | 435.074 | ........................................................................ [  3%] ........................................ |
| GET /healthz | endpoint | pass | 0.006 | {"status":"ok","hub":"simple_local_hub","version":"final_pr_02"} |
| GET /status.json | endpoint | pass | 0.002 | {   "status": "ok",   "hub": "simple_local_hub",   "version": "final_pr_01",   "candidate_only": true,   "local_only": t |
| GET / | endpoint | pass | 0.002 | <!DOCTYPE html> <html lang="en"> <head>   <meta charset="UTF-8">   <meta name="viewport" content="width=device-width, in |
| GET /demo/universal-work.json | endpoint | pass | 0.006 | {   "artifact_kind": "odin_demo_universal_work_info",   "candidate_only": true,   "description": "POST to /demo/universa |
| GET /activity.json | endpoint | pass | 0.002 | {   "artifact_kind": "odin_activity_list",   "candidate_only": true,   "local_only": true,   "events": [     {       "ev |
| GET /receipts.json | endpoint | pass | 0.001 | {   "artifact_kind": "odin_receipts",   "candidate_only": true,   "local_only": true,   "events": [],   "claim_boundary" |
| GET /providers/probe.json | endpoint | pass | 0.005 | {   "artifact_kind": "odin_provider_status_packet",   "candidate_only": true,   "local_only": true,   "provider_executio |
| GET /execution-gate/status.json | endpoint | pass | 0.006 | {   "artifact_kind": "odin_execution_gate_policy",   "execution_gate_enabled": true,   "mock_execution_allowed": true,   |
| POST /execution-gate/mock | endpoint | pass | 0.002 | {   "artifact_kind": "odin_mock_execution_response_packet",   "provider_id": "mock",   "execution_kind": "mock_determini |
| GET /final-pr-ladder/scaffold.json | endpoint | pass | 0.003 | {   "artifact_kind": "odin_final_pr_worker_packet_scaffold",   "target_pr_id": "FINAL-PR-06",   "source_return_report":  |
| GET /demo/y-route.json | endpoint | pass | 0.018 | {   "artifact_kind": "y_route_explanation_demo",   "candidate_only": true,   "input_kind": "demo_universal_work",   "can |
| GET /demo/seed-route.json | endpoint | pass | 0.013 | {   "status": "ok",   "candidate_only": true,   "claim_boundary": "operational_seed_spine_routes_work_not_authority",    |
| GET /demo/field-selection.json | endpoint | pass | 0.016 | {   "status": "ok",   "candidate_only": true,   "claim_boundary": "field_selection_scores_routes_not_truth",   "field_se |
| GET /demo/projection-candidate.json | endpoint | pass | 0.015 | {   "status": "ok",   "candidate_only": true,   "claim_boundary": "projection_candidate_spine_prepares_candidates_not_ru |
| import odin | import | pass | 0.0 | import ok |
| import odin.cli | import | pass | 0.006 | import ok |
| import odin.local_hub.server | import | pass | 0.0 | import ok |
| import odin.qirc_core.bus | import | pass | 0.0 | import ok |
| import odin.execution_gate.gateway | import | pass | 0.0 | import ok |
| import odin.providers.probe | import | pass | 0.0 | import ok |
| import odin.operational_seed_spine.selector | import | pass | 0.0 | import ok |
| import odin.field_selection_spine.selector | import | pass | 0.0 | import ok |
| import odin.projection_candidate_spine.projection_set | import | pass | 0.0 | import ok |
| import odin.proof_chain.registry | import | pass | 0.001 | import ok |

## Post-generation required command receipts

| Command | Status | Result |
| --- | --- | --- |
| `python -m odin.cli audit-pre-release-super` | pass | status ok; overall_verdict yellow; release_pr_should_move_to FINAL-PR-11 |
| `python -m odin.cli validate-projection-candidate-spine` | pass | validate-projection-candidate-spine: OK |
| `python -m odin.cli validate-field-selection-spine` | pass | validate-field-selection-spine: OK |
| `python -m odin.cli validate-operational-seed-spine` | pass | validate-operational-seed-spine: OK |
| `python -m odin.cli validate-y-pattern-spine` | pass | validate-y-pattern-spine: OK |
| `python -m odin.cli validate-prep-final-pr-06-08` | pass | validate-prep-final-pr-06-08: OK |
| `python -m odin.cli validate-final-pr-05-execution-gate` | pass | validate-final-pr-05-execution-gate: OK |
| `python -m odin.cli validate-all` | pass | validate-all: OK |
| `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_pre_release_super_audit.py -p no:cacheprovider` | pass | 20 passed in 8.22s; 20 passed in 6.95s after report receipt update |
| `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider --tb=no` | pass | 2375 passed, 2 skipped in 435.33s (0:07:15) |


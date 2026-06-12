# FINAL-PR-01 Odin Agent Operator Work Packet

```yaml
task_id: final_pr_01_simple_local_hub
intent: |
  Implement FINAL-PR-01: Simple Local Hub Start + Normal User Browser UI.
  Make Odin locally startable and understandable as the first final Road-to-100 slice.

input_handoff: docs/codex/handoffs/FINAL_PR_01_COMPILED_THOR_Y_HANDOFF.md

universal_work_boundary:
  candidate_only: true
  local_only: true
  app_owned_apply: true
  external_send_default: false
  claim_boundary: simple_local_hub_local_receipt_not_runtime_completion_not_production

allowed_actions:
  - read any file in the repo for orientation
  - write to allowed implementation and doc files
  - run validators: python -m odin.cli validate-*
  - run tests: python -m pytest
  - run CLI commands: python -m odin.cli start-local-hub --once-smoke
  - commit candidate implementation to working branch
  - create new files in allowed paths

forbidden_actions:
  - app_state_apply
  - external_send
  - hidden_tool_execution
  - provider_api_call_without_receipt
  - claiming_proof_without_receipt
  - domain_state_mutation
  - public_bind (0.0.0.0)
  - model_inference_execution
  - qirc_core_runtime_execution
  - real_app_bridge_runtime
  - windows_service_install
  - signing_or_release

expected_artifacts:
  implementation:
    - odin/local_hub/__init__.py
    - odin/local_hub/policy.py
    - odin/local_hub/ui.py
    - odin/local_hub/server.py
    - odin/local_hub/proof.py
    - odin/cli.py (updated)
    - tools/rebaseline/check_simple_local_hub.py
    - tests/test_simple_local_hub.py
  schemas_examples_registries:
    - schemas/final_pr_01_simple_local_hub_proof_packet.schema.json
    - registries/final_pr_01_simple_local_hub_registry.json
    - examples/final_pr_01/simple_local_hub_proof_packet.example.json
  reports:
    - reports/final_pr_01_simple_local_hub_report.json
    - reports/final_pr_01_thor_odin_y_effectiveness_audit.json
  docs:
    - docs/rebaseline/FINAL_PR_01_SIMPLE_LOCAL_HUB.md
    - docs/codex/audits/FINAL_PR_01_SIMPLE_LOCAL_HUB_AUDIT.md
    - docs/codex/audits/FINAL_PR_01_THOR_ODIN_Y_EFFECTIVENESS_AUDIT.md
    - docs/codex/reports/FINAL_PR_01_SIMPLE_LOCAL_HUB_RETURN_REPORT.md
  handoffs:
    - docs/codex/handoffs/FINAL_PR_01_REPO_COGNITION_SUMMARY.md
    - docs/codex/handoffs/FINAL_PR_01_THOR_Y_HANDOFF_REQUEST.md
    - docs/codex/handoffs/FINAL_PR_01_COMPILED_THOR_Y_HANDOFF.md
    - docs/codex/handoffs/FINAL_PR_01_ODIN_AGENT_OPERATOR_WORK_PACKET.md
    - docs/codex/handoffs/FINAL_PR_01_Y_MJOLNIR_PROFILE_NOTES.md
  manifests:
    - SYSTEM_MAP.json (updated)
    - FILE_MANIFEST.json (updated)

validators:
  - python -m odin.cli validate-simple-local-hub
  - python -m odin.cli validate-all
  - python tools/rebaseline/check_simple_local_hub.py --repo-root . --out reports/final_pr_01_simple_local_hub_report.json

tests:
  - python -m pytest tests/test_simple_local_hub.py -q -p no:cacheprovider
  - python -m pytest -q -p no:cacheprovider

proof_packets:
  - python -m odin.cli prove-simple-local-hub
  - python -m odin.cli start-local-hub --once-smoke

return_report:
  path: docs/codex/reports/FINAL_PR_01_SIMPLE_LOCAL_HUB_RETURN_REPORT.md
  required_sections:
    - implemented
    - commands_run_with_results
    - senior_reviewer_simulation
    - senior_code_reviewer_simulation
    - known_gaps
    - next_pr_handoff

failure_policy: |
  If validate-all fails, do not mark ready.
  If pytest fails, do not mark ready.
  If smoke test hangs, investigate root cause before committing.
  Record all failures with exact error text.

token_minimization_policy:
  - read only target files; do not dump the whole repo
  - use grep and manifests to locate surfaces before reading
  - summarize before coding; implement smallest safe slice
  - run focused validator before full pytest
  - do not regenerate unrelated artifacts
  - batch file writes where possible
```

# FINAL-PR-02 Odin Agent Operator Work Packet

**claim_boundary:** odin_agent_operator_work_packet_not_runtime_proof_not_app_approval

---

```yaml
task_id: final_pr_02_model_apps_demo
intent: >
  Extend the FINAL-PR-01 Simple Local Hub with model picker UI, connected apps panel,
  and a deterministic demo Universal Work flow. Show Odin accepting work and returning
  a candidate response packet without model inference, provider execution, app apply,
  or external send.

input_handoff: docs/codex/handoffs/FINAL_PR_02_COMPILED_THOR_Y_HANDOFF.md

universal_work_boundary:
  candidate_only: true
  local_only: true
  model_execution: false
  provider_execution: false
  app_apply: false
  external_send: false
  qirc_core_runtime: false
  hidden_tool_execution: false

candidate_only: true
local_only: true

allowed_actions:
  - read targeted files (odin/local_hub/*, tests/, tools/, docs/, schemas/, registries/)
  - create new Python modules in odin/local_hub/
  - modify odin/local_hub/ui.py (extend HTML)
  - modify odin/local_hub/server.py (add GET endpoints)
  - modify odin/local_hub/__init__.py (expose symbols)
  - modify odin/cli.py (add subparser entries + handlers + validator call)
  - create tools/rebaseline/check_final_pr_02_model_apps_demo.py
  - create tests/test_final_pr_02_model_apps_demo.py
  - create docs, reports, schemas, registries, examples
  - modify SYSTEM_MAP.json (add new file references)
  - run validate-all, pytest, validate-simple-local-hub, start-local-hub --once-smoke
  - commit and push to branch

forbidden_actions:
  - app_state_apply
  - external_send
  - hidden_tool_execution
  - provider_api_call_without_receipt
  - claiming_proof_without_receipt
  - domain_state_mutation
  - model_inference (no Ollama, llama.cpp, OpenAI, Claude, or any provider execution)
  - reading API keys or environment credentials
  - accessing external network beyond localhost
  - real app integration
  - real app bridge runtime
  - QIRC Core runtime
  - Windows service/tray/installer
  - modifying docs/MASTER_* files
  - modifying registries/codex_* files
  - modifying tests/test_simple_local_hub.py
  - modifying odin/local_hub/proof.py (FINAL-PR-01 proof kept intact)

expected_artifacts:
  code:
    - odin/local_hub/model_picker.py
    - odin/local_hub/connected_apps.py
    - odin/local_hub/demo_universal_work.py
    - odin/local_hub/proof_pr02.py
  modified:
    - odin/local_hub/ui.py
    - odin/local_hub/server.py
    - odin/local_hub/__init__.py
    - odin/cli.py
    - SYSTEM_MAP.json
  validator:
    - tools/rebaseline/check_final_pr_02_model_apps_demo.py
  tests:
    - tests/test_final_pr_02_model_apps_demo.py
  docs:
    - docs/codex/handoffs/FINAL_PR_02_REPO_COGNITION_SUMMARY.md
    - docs/codex/handoffs/FINAL_PR_02_HUB_SURFACE_DECISION.md
    - docs/codex/handoffs/FINAL_PR_02_THOR_Y_HANDOFF_REQUEST.md
    - docs/codex/handoffs/FINAL_PR_02_COMPILED_THOR_Y_HANDOFF.md
    - docs/codex/handoffs/FINAL_PR_02_ODIN_AGENT_OPERATOR_WORK_PACKET.md
    - docs/rebaseline/FINAL_PR_02_MODEL_APPS_DEMO.md
    - docs/codex/reports/FINAL_PR_02_MODEL_APPS_DEMO_RETURN_REPORT.md
    - docs/codex/audits/FINAL_PR_02_MODEL_APPS_DEMO_AUDIT.md
    - docs/codex/audits/FINAL_PR_02_THOR_EFFECTIVENESS_AUDIT.md
    - docs/codex/audits/FINAL_PR_02_ODIN_EFFECTIVENESS_AUDIT.md
  reports:
    - reports/final_pr_02_model_apps_demo_report.json
    - reports/final_pr_02_thor_effectiveness_audit.json
    - reports/final_pr_02_odin_effectiveness_audit.json
  schemas:
    - schemas/final_pr_02_demo_universal_work_response_packet.schema.json
  registries:
    - registries/final_pr_02_model_apps_demo_registry.json
  examples:
    - examples/final_pr_02/demo_universal_work_response_packet.example.json

validators:
  - python -m odin.cli validate-final-pr-02-model-apps-demo
  - python -m odin.cli validate-simple-local-hub
  - python -m odin.cli validate-all
  - python tools/rebaseline/check_final_pr_02_model_apps_demo.py --repo-root . --out reports/final_pr_02_model_apps_demo_report.json --generated-at-utc 2026-01-01T00:00:00Z

tests:
  - PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_final_pr_02_model_apps_demo.py -p no:cacheprovider
  - PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider

proof_packets:
  - python -m odin.cli prove-final-pr-02-demo-universal-work

return_report: docs/codex/reports/FINAL_PR_02_MODEL_APPS_DEMO_RETURN_REPORT.md

failure_policy:
  - if validate-all fails before changes: record and continue only if unrelated to FINAL-PR-02
  - if validate-all fails after changes: fix immediately before marking done
  - if pytest fails after changes: fix immediately before marking done
  - if any forbidden action is attempted: stop and report to operator
  - do not mark ready if validate-all or pytest fails

token_minimization_policy:
  - reuse FINAL-PR-01 handoff artifacts as templates
  - read only targeted files (not full repo)
  - deterministic demo only (no model wait)
  - focused pytest before full pytest
  - handoff docs compact — functional not verbose
  - regenerate only required reports/manifest/system map
```

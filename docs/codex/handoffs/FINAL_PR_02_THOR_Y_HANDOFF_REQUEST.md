# FINAL-PR-02 Thor/Y Handoff Request

**claim_boundary:** thor_y_handoff_request_not_runtime_proof_not_app_approval

---

```yaml
handoff_request_id: final_pr_02_thor_y_handoff_request

primary_profile: thor
secondary_profiles:
  - generic
  - y
  - mjolnir

source_truth:
  - FINAL-PR-01 return report (docs/codex/reports/FINAL_PR_01_SIMPLE_LOCAL_HUB_RETURN_REPORT.md)
  - FINAL-PR-01 Thor/Odin/Y audit (docs/codex/audits/FINAL_PR_01_THOR_ODIN_Y_EFFECTIVENESS_AUDIT.md)
  - FINAL-PR-02 roadmap slice (docs/rebaseline/FINAL_MINIMAL_ROAD_TO_100_PR_ROADMAP_V1.md)
  - Local Runtime Hub target (docs/rebaseline/FINAL_LOCAL_RUNTIME_HUB_TARGET_V1.md)

repo_cognition_input:
  - docs/codex/handoffs/FINAL_PR_02_REPO_COGNITION_SUMMARY.md

task_intent: |
  Build model picker UI, connected apps panel, and deterministic demo Universal Work flow
  on top of the FINAL-PR-01 Simple Local Hub (port 8765).

  The model picker shows None / Mock / Local Candidate options.
  No model is executed. No provider binary is called. No API key is used.

  Connected apps shows Generic / Browser / File placeholder slots.
  No real app is connected. No app state is mutated. No external send happens.

  The demo Universal Work flow is deterministic:
  raw input → Handoff Context → Universal Work Packet → Candidate Artifact → Response Packet.
  This shows the shape of Odin's work without calling a real model or provider.

allowed_scope:
  - model picker UI with None / Mock / Local Candidate options
  - provider status panel (placeholder status only)
  - mock deterministic candidate mode (not executed)
  - local candidate provider listed but not executed
  - connected app demo slots (Generic, Browser, File)
  - generic app bridge placeholder/status
  - demo Universal Work section with input → handoff → UW → candidate → response
  - deterministic candidate response (hard-coded, not model output)
  - /models.json, /apps.json, /demo/universal-work.json GET endpoints
  - proof packet for demo universal work flow
  - validator (check_final_pr_02_model_apps_demo.py)
  - tests (test_final_pr_02_model_apps_demo.py, 30 minimum)
  - docs/reports/schemas/registries/examples
  - Hub Surface Decision
  - Improved Thor Effectiveness Audit
  - Improved Odin Effectiveness Audit
  - Return Report
  - SYSTEM_MAP and FILE_MANIFEST updates

forbidden_scope:
  - provider execution (Ollama, llama.cpp, OpenAI, Claude, any model binary)
  - model inference (no model output, no API call)
  - API key reads or environment credential reads
  - external network beyond localhost
  - real external app integration
  - real app bridge runtime
  - app apply
  - app state mutation
  - external send
  - full QIRC Core runtime
  - QIRC public rooms/network/federation
  - Windows service/tray/installer
  - production readiness claim
  - security certification claim

handoff_output_required:
  - compiled handoff context (FINAL_PR_02_COMPILED_THOR_Y_HANDOFF.md)
  - implementation plan (in compiled handoff)
  - acceptance gates (in compiled handoff)
  - proof commands (python -m odin.cli prove-final-pr-02-demo-universal-work)
  - Thor audit questions (FINAL_PR_02_THOR_EFFECTIVENESS_AUDIT.md)
  - Odin audit questions (FINAL_PR_02_ODIN_EFFECTIVENESS_AUDIT.md)

quality_goal: |
  Make Odin visibly able to accept a demo work request and return a candidate packet
  without claiming provider execution, model inference, real app integration, app apply,
  or QIRC Core runtime. The UI should clearly distinguish demo/placeholder from live.

token_goal: |
  Reuse FINAL-PR-01 handoff pattern. Focused repo cognition (not full repo read).
  Deterministic demo only (no model wait time). Focused tests before full pytest.
  Handoff docs compact — functional not verbose.

worker_profile:
  worker_id: claude-code
  candidate_only: true
  local_only: true
  app_owned_apply: true
  external_send_default: false
  hidden_tool_execution_allowed: false
```

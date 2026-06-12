# FINAL-PR-01 Thor/Y Handoff Request

```yaml
handoff_request_id: final_pr_01_thor_y_handoff_request
primary_profile: thor
secondary_profiles:
  - generic
  - y
  - mjolnir

task_intent: |
  Build FINAL-PR-01: Simple Local Hub Start + Normal User Browser UI.
  This is the first final Local Runtime Hub build slice. It makes Odin visibly
  local and understandable without overbuilding or claiming provider/model/runtime
  completion.

repo_cognition_input:
  link: docs/codex/handoffs/FINAL_PR_01_REPO_COGNITION_SUMMARY.md

source_truth:
  - Odin v7.1.1 Local Runtime Hub target
  - PR #35 Road-to-100 audit
  - PR #36 Handoff-First amendment (merged, SHA 9962bbe393fbf658d00be6021ad7dbceca51d2e0)
  - FINAL-PR-01 slice definition in FINAL_BUILDABLE_SLICE_CATALOG_V1.md

allowed_scope:
  - local hub server shell (Python stdlib, localhost only, port 8765)
  - localhost browser UI (HTML with required stable IDs)
  - status/proof placeholders (QIRC, Handoff-First, model, apps, activity)
  - smoke proof (start-local-hub --once-smoke)
  - proof packet (prove-simple-local-hub)
  - validator (validate-simple-local-hub in cli.py + tools/rebaseline/check_simple_local_hub.py)
  - tests (tests/test_simple_local_hub.py, 34 tests)
  - docs/reports (see suggested file list)
  - Thor/Y/Odin handoff artifacts for this PR
  - Senior Review / Senior Code Review audit artifacts
  - Thor/Odin/Y effectiveness audit

forbidden_scope:
  - actual model inference or provider execution
  - external network beyond localhost smoke
  - full QIRC Core runtime
  - real app bridge runtime
  - app apply, app state mutation, external send
  - public bind (0.0.0.0)
  - Windows service/tray/installer
  - signed release
  - production readiness or security certification
  - target-host proof
  - Godot/YNode/Mjölnir runtime proof
  - Ollama/llama.cpp runtime proof

handoff_output_required:
  - Compiled Handoff Context (FINAL_PR_01_COMPILED_THOR_Y_HANDOFF.md)
  - Odin Agent Operator Work Packet (FINAL_PR_01_ODIN_AGENT_OPERATOR_WORK_PACKET.md)
  - Y/Mjölnir Profile Notes (FINAL_PR_01_Y_MJOLNIR_PROFILE_NOTES.md)
  - Implementation plan (in Work Packet)
  - Acceptance gates (in Work Packet)
  - Proof commands (validate-simple-local-hub, prove-simple-local-hub, start-local-hub --once-smoke)
  - Return report contract (in Work Packet)
  - Thor/Odin/Y Effectiveness Audit (post-implementation)

quality_goal: |
  Use the smallest safe implementation that makes Odin locally startable and
  understandable by a normal user. The Browser Hub must be readable without
  understanding handoff internals. Dev Mode holds the deeper content.

token_goal: |
  Minimize token consumption by using focused repo cognition, compact handoff
  context, validators that catch errors early, and targeted tests. Read only
  target files. Use grep and manifests instead of broad context dumps. Implement
  the smallest safe slice.

important_notes:
  - Do not use external Thor clone or install Thor
  - Do not call external Thor runtime
  - Use repo-internal Thor/Y/Mjölnir handoff artifacts as profile awareness only
  - If a repo-internal compiler exists, map this request into that shape
  - If no compiler exists, manually compile the handoff context using repo-internal docs as guidance
  - Claude Code is the bounded implementation worker under Odin discipline
```

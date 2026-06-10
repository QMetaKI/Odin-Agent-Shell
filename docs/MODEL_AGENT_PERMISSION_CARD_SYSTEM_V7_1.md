# Model / Agent Permission Card System v7.1

## Purpose

Permission Cards make model/agent permissions explicit and comparable across all worker types.

## Permission levels

```text
read_digest_only
read_local_context
draft_candidate
review_candidate
patchplan_candidate
scheduled_candidate
human_review_required
app_apply_required
blocked
```

## Default

The default permission for every model or agent is `draft_candidate` or lower. Any action-like behavior must degrade to Candidate Artifact with app-owned apply required.

## Permission card example

```json
{
  "artifact_kind": "odin_agent_permission_card",
  "card_id": "coding_agent_default",
  "worker_kind": "coding_agent",
  "allowed": ["read_digest_only", "patchplan_candidate", "review_candidate"],
  "blocked": ["apply_patch", "run_deploy", "external_send", "delete_file"],
  "requires_human_review": true,
  "requires_app_apply_gate": true
}
```

## Escalation rule

A model or agent cannot escalate its own permission. The App, Caller Manifest and Odin Binding Gate define permission. Odin can only downgrade or block.


## Non-negotiable boundaries

- No model or agent receives app authority.
- No model or agent can apply app state changes through Odin.
- No model or agent can send externally through Odin.
- No model or agent can bypass Binding Gate, Admissibility Gate, Claim Boundary, Human/App Apply Boundary, Runtime Pack Validation, or Odin Final Gate.
- No model or agent identity becomes a persona authority. Model identity is a capability descriptor only.
- No connector, assistant, coding agent, browser agent, IDE agent, local model, remote model, or custom assistant is trusted as runtime truth.
- All outputs are Candidate Artifacts until the app/user accepts them in the app-owned apply layer.

## Canonical relation

Universal Model/Agent Parity generalizes the earlier ChatGPT/Odin twin idea. ChatGPT is one instance of a user-facing conversational model surface. Other models and agents are other surfaces. Odin is the control, candidate, trace, gate and runtime-pack layer that makes any model or agent behave like bounded work inside a reviewable system.

## Purpose

The goal is not to make every model behave the same. The goal is to make every model and agent interoperable with the same Odin work discipline: Work Capsule, Capability Card, Permission Card, Model/Agent Adapter, Candidate Protocol, Semantic Diff, Why Trace, and App-owned Apply.

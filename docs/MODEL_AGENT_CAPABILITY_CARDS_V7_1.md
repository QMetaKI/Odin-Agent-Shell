# Model / Agent Capability Cards v7.1

## Purpose

Capability Cards describe what a model or agent may be asked to do in Odin. They are not marketing metadata. They are routing, permission, safety, resource, and quality contracts.

## Capability Card fields

```json
{
  "artifact_kind": "odin_model_agent_card",
  "id": "local_3b_micro",
  "worker_kind": "local_model",
  "size_class": "3b",
  "best_for": ["route", "extract", "schema_repair", "claim_critic"],
  "avoid_for": ["long_synthesis", "external_action", "authority_decision"],
  "allowed_slot_classes": ["label.slot", "json_fill.slot", "claim_scan.slot"],
  "blocked_slot_classes": ["deep_synthesis.slot", "app_apply.slot"],
  "permission_profile": "candidate_only_local",
  "resource_profile": "low_memory_strict_or_standard",
  "trace_required": true
}
```

## Worker classes

- local_model
- hosted_model
- coding_agent
- browser_agent
- research_agent
- app_agent
- workflow_agent
- human_review_surface

## Routing use

Odin routes based on cards, not brand aura. A larger model may be blocked if the card says a smaller model is sufficient or safer. A coding agent may be restricted to patchplan candidates. A hosted model may be blocked for local-only privacy class.

## Capability dimensions

- semantic skill
- schema adherence
- context window
- latency profile
- cost profile
- privacy class
- action risk
- output risk
- traceability quality
- safe slot classes
- prohibited output claims


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
